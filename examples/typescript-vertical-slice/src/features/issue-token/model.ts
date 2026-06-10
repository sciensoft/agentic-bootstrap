// Feature-internal types. Lives with the rest of the slice; not exposed cross-feature.

export interface IssueTokenRequest {
  callerId: string;
  audience: string;
  capabilities: ReadonlyArray<string>;
  ttlSeconds: number;
}

export interface IssueTokenResponse {
  token: string;
  jti: string;
  expiresAt: string;
}

export class InvalidCapabilityError extends Error {
  constructor(public readonly capability: string) {
    super(`Capability not permitted for this caller: ${capability}`);
    this.name = 'InvalidCapabilityError';
  }
}

export class TtlOutOfRangeError extends Error {
  constructor(public readonly ttlSeconds: number, public readonly maxTtlSeconds: number) {
    super(`TTL ${ttlSeconds}s exceeds maximum allowed ${maxTtlSeconds}s`);
    this.name = 'TtlOutOfRangeError';
  }
}
