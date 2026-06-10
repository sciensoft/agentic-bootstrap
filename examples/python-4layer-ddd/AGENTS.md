# orbital

Track and analyse satellite orbital decay events.

## Purpose

Orbital ingests TLE (two-line element) updates from public catalogs, computes decay predictions per object, and exposes per-object timelines via an HTTP API. Built for satellite operators who need decay-risk visibility without standing up their own propagation pipeline. Core dependencies: FastAPI (HTTP), SGP4 (propagation), Postgres (persistence).

## Rules

Always follow the rules in `.agents/rules/`:

- [`workflow.md`](.agents/rules/workflow.md) — every artifact-producing request gets a timestamped prompt file under `.docs/prompts/`, an optional new-or-updated ADR under `.docs/adrs/`, telemetry kept current, a single git commit bundling the lot, and a push.
- [`workflow-todos.md`](.agents/rules/workflow-todos.md) — deferred ideas as one-file-per-entry under `.docs/todos/`.
- [`workflow-security.md`](.agents/rules/workflow-security.md) — security rubric pass before commit; full audits under `.docs/security/<YYYY-MM-DD>-<slug>.md`.
- [`workflow-testing.md`](.agents/rules/workflow-testing.md) — pyramid-shaped tests; bug fixes start with a failing regression test; tests + code in the same commit.
- [`best-practices.md`](.agents/rules/best-practices.md) — Python + FastAPI idioms, DI patterns, naming, repository/service shape.
- [`layered-architecture.md`](.agents/rules/layered-architecture.md) — `presentation → application → domain ← infrastructure`, plus `shared` available to all but depending on none. Inward dependencies only.

Architecture decisions live in [`.docs/adrs/`](.docs/adrs/) — read these before making structural changes.

## Run

```bash
# Install
uv sync

# Run the API
uv run uvicorn orbital.main:app --reload

# Tests
make test
```

Postgres required (local or via docker-compose). Set `DATABASE_URL` in `.env`.

## Architecture map

- `presentation/` — FastAPI routes, response shaping
- `application/` — services (`OrderService`, `PropagationService`), DI container
- `domain/` — `Order`, `Satellite`, `DecayEvent`; repository protocols
- `infrastructure/` — Postgres repositories, SGP4 propagator adapter, external catalog clients
- `shared/` — cross-cutting types, error classes
