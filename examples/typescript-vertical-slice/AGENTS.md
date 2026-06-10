# helix

Issue and verify ephemeral access tokens for a mesh of internal services.

## Purpose

Helix is an internal token-service. It issues short-lived JWTs scoped to caller + audience + capability, and exposes a verify endpoint that downstream services use to gate sensitive operations. Built for the platform team; consumed by ~40 internal services. Core dependencies: Fastify (HTTP), `jose` (JWT), Redis (rate limit + revocation list).

## Rules

Always follow the rules in `.agents/rules/`:

- [`workflow.md`](.agents/rules/workflow.md) — every artifact-producing request gets a timestamped prompt file under `.docs/prompts/`, an optional new-or-updated ADR under `.docs/adrs/`, a single commit, a push.
- [`workflow-todos.md`](.agents/rules/workflow-todos.md) — deferred ideas as files in `.docs/todos/`.
- [`workflow-security.md`](.agents/rules/workflow-security.md) — security rubric before commit; `.docs/security/methodology.md` for the full rubric.
- [`workflow-testing.md`](.agents/rules/workflow-testing.md) — pyramid-shaped; tests + code in the same commit.
- [`best-practices.md`](.agents/rules/best-practices.md) — TypeScript + Fastify + `jose` idioms.
- [`layered-architecture.md`](.agents/rules/layered-architecture.md) — feature-first; **features may only import from `shared/`, never from each other**.

ADRs in [`.docs/adrs/`](.docs/adrs/) — read before structural changes.

## Run

```bash
npm install
npm run dev      # starts the HTTP server on :8080
npm test         # vitest
npm run check    # lint + type-check
```

Redis required (local or via docker-compose). Set `REDIS_URL` + `SIGNING_KEY_DER_B64` in `.env`.

## Architecture map

- `src/features/` — each subdirectory is one self-contained slice:
  - `issue-token/` — issues a JWT scoped to caller + audience + capability
  - `verify-token/` — verifies a JWT, checks the revocation list, returns claims
  - `revoke-token/` — adds a token's `jti` to the revocation list
- `src/shared/` — the only cross-cutting dependency features may import:
  - `auth/` — signing-key, JWT envelope, claim shapes
  - `infrastructure/` — Redis client, Fastify plugin
  - `observability/` — logger, tracer, metrics
