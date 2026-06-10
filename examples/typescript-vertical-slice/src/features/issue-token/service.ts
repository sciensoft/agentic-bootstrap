// Business logic for issuing a token.
// Imports only its own slice's types + shared/.

import { randomUUID } from 'node:crypto';

import { SigningKey } from '../../shared/auth/signing-key';
import { Clock } from '../../shared/infrastructure/clock';
import { CapabilityRegistry } from '../../shared/auth/capability-registry';

import {
  IssueTokenRequest,
  IssueTokenResponse,
  InvalidCapabilityError,
  TtlOutOfRangeError,
} from './model';

const MAX_TTL_SECONDS = 60 * 60; // 1 hour

export interface IssueTokenService {
  issue(req: IssueTokenRequest): Promise<IssueTokenResponse>;
}

export class IssueTokenServiceImpl implements IssueTokenService {
  constructor(
    private readonly signingKey: SigningKey,
    private readonly capabilities: CapabilityRegistry,
    private readonly clock: Clock,
  ) {}

  async issue(req: IssueTokenRequest): Promise<IssueTokenResponse> {
    if (req.ttlSeconds <= 0 || req.ttlSeconds > MAX_TTL_SECONDS) {
      throw new TtlOutOfRangeError(req.ttlSeconds, MAX_TTL_SECONDS);
    }

    const allowed = await this.capabilities.allowedFor(req.callerId);
    for (const cap of req.capabilities) {
      if (!allowed.has(cap)) throw new InvalidCapabilityError(cap);
    }

    const now = this.clock.nowSeconds();
    const jti = randomUUID();
    const token = await this.signingKey.sign({
      iss: 'helix',
      sub: req.callerId,
      aud: req.audience,
      cap: [...req.capabilities],
      jti,
      iat: now,
      exp: now + req.ttlSeconds,
    });

    return {
      token,
      jti,
      expiresAt: new Date((now + req.ttlSeconds) * 1000).toISOString(),
    };
  }
}
