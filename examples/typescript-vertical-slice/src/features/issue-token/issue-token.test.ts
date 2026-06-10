// All tests for this slice, co-located.
// Unit-tests the service against fake shared/ collaborators — no infra needed.

import { describe, expect, it } from 'vitest';

import { IssueTokenServiceImpl } from './service';
import { InvalidCapabilityError, TtlOutOfRangeError } from './model';

class FakeSigningKey {
  async sign(payload: Record<string, unknown>): Promise<string> {
    return `fake.${JSON.stringify(payload)}.sig`;
  }
}

class FakeCapabilityRegistry {
  constructor(private readonly map: Map<string, Set<string>>) {}
  async allowedFor(callerId: string): Promise<Set<string>> {
    return this.map.get(callerId) ?? new Set();
  }
}

class FrozenClock {
  constructor(private readonly when: number) {}
  nowSeconds(): number {
    return this.when;
  }
}

const NOW = 1_750_000_000;

function buildService(capsForCaller: Iterable<string>): IssueTokenServiceImpl {
  return new IssueTokenServiceImpl(
    new FakeSigningKey(),
    new FakeCapabilityRegistry(new Map([['caller-1', new Set(capsForCaller)]])),
    new FrozenClock(NOW),
  );
}

describe('IssueTokenService', () => {
  it('signs a token with the requested claims when capabilities are permitted', async () => {
    const svc = buildService(['orders:read', 'orders:write']);

    const out = await svc.issue({
      callerId: 'caller-1',
      audience: 'orders-api',
      capabilities: ['orders:read'],
      ttlSeconds: 300,
    });

    expect(out.token.startsWith('fake.')).toBe(true);
    expect(out.jti).toMatch(/^[0-9a-f-]{36}$/);
    expect(new Date(out.expiresAt).getTime() / 1000).toBe(NOW + 300);
  });

  it('rejects capabilities the caller is not permitted', async () => {
    const svc = buildService(['orders:read']);

    await expect(
      svc.issue({
        callerId: 'caller-1',
        audience: 'orders-api',
        capabilities: ['orders:write'],
        ttlSeconds: 300,
      }),
    ).rejects.toBeInstanceOf(InvalidCapabilityError);
  });

  it('rejects TTLs above one hour', async () => {
    const svc = buildService(['orders:read']);

    await expect(
      svc.issue({
        callerId: 'caller-1',
        audience: 'orders-api',
        capabilities: ['orders:read'],
        ttlSeconds: 7200,
      }),
    ).rejects.toBeInstanceOf(TtlOutOfRangeError);
  });
});
