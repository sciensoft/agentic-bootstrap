// Inbound entry — Fastify route. Thin: parse, call service, format response.

import { FastifyInstance, FastifyRequest } from 'fastify';

import { logger } from '../../shared/observability/logger';

import { IssueTokenService } from './service';
import {
  IssueTokenRequest,
  InvalidCapabilityError,
  TtlOutOfRangeError,
} from './model';

interface Body {
  caller_id: string;
  audience: string;
  capabilities: string[];
  ttl_seconds: number;
}

export function registerIssueTokenRoute(app: FastifyInstance, service: IssueTokenService): void {
  app.post('/tokens', async (req: FastifyRequest<{ Body: Body }>, reply) => {
    const body = req.body;
    const dto: IssueTokenRequest = {
      callerId: body.caller_id,
      audience: body.audience,
      capabilities: body.capabilities,
      ttlSeconds: body.ttl_seconds,
    };

    try {
      const out = await service.issue(dto);
      return reply.code(201).send(out);
    } catch (err) {
      if (err instanceof InvalidCapabilityError) {
        return reply.code(403).send({ error: 'invalid_capability', capability: err.capability });
      }
      if (err instanceof TtlOutOfRangeError) {
        return reply.code(400).send({ error: 'ttl_out_of_range', max_ttl_seconds: err.maxTtlSeconds });
      }
      logger.error({ err }, 'unhandled error issuing token');
      return reply.code(500).send({ error: 'internal_error' });
    }
  });
}
