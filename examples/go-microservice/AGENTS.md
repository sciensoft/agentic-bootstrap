# quill

Accept order events from the storefront and forward fulfilment requests to the warehouse.

## Purpose

Quill sits between the storefront and the warehouse. It accepts placed-order events (HTTP + a Kafka topic), validates them against the catalog, computes the fulfilment plan, and forwards a reservation request to the warehouse API. Built for the order-flow team; ~30 RPS sustained, 200 RPS peak. Core dependencies: chi (HTTP), franz-go (Kafka), pgx (Postgres), OpenTelemetry.

## Rules

Always follow the rules in `.agents/rules/`:

- [`workflow.md`](.agents/rules/workflow.md) — prompt file + ADR + telemetry + commit + push, one bundle per request.
- [`workflow-todos.md`](.agents/rules/workflow-todos.md) — deferred ideas as files in `.docs/todos/`.
- [`workflow-security.md`](.agents/rules/workflow-security.md) — security rubric before commit; full audits dated under `.docs/security/`.
- [`workflow-testing.md`](.agents/rules/workflow-testing.md) — pyramid-shaped; bug fixes start with a failing regression test; tests + code in the same commit.
- [`workflow-metrics.md`](.agents/rules/workflow-metrics.md) — golden signals per surface (RPS, error rate, p95 latency); no PII in labels.
- [`best-practices.md`](.agents/rules/best-practices.md) — Go + chi + pgx idioms; error wrapping; context propagation; small interfaces at boundaries.
- [`layered-architecture.md`](.agents/rules/layered-architecture.md) — 4-Layer DDD internals + cross-service surface (health/readiness, retries with backoff + circuit breakers, distributed tracing, consumer-driven contracts, deploy-manifest discipline).

ADRs in [`.docs/adrs/`](.docs/adrs/) — read before structural changes.

## Run

```bash
go build ./...
go test ./...
make run        # starts on :8080; readyz pings DB + warehouse
```

Postgres + Kafka required (local docker-compose). Set `DATABASE_URL` + `KAFKA_BROKERS` + `WAREHOUSE_API_URL` + `OTEL_EXPORTER_OTLP_ENDPOINT` in `.env`.

## Architecture map

- `internal/presentation/`:
  - `http/` — chi routers + middleware (request-id, tracing, rate-limit)
  - `health/` — `/healthz` (liveness) + `/readyz` (readiness)
  - `messaging/` — Kafka consumer for `orders.placed`
- `internal/application/services/` — order orchestration, fulfilment computation
- `internal/domain/` — `Order`, `Reservation`, `FulfilmentPlan`; repository + client protocols
- `internal/infrastructure/`:
  - `repositories/` — Postgres adapters
  - `clients/` — outbound HTTP to the warehouse API (with retries, circuit breaker, tracing)
  - `telemetry/` — OpenTelemetry tracing + Prometheus metrics adapters
- `contracts/`:
  - `provider/` — what quill promises to its callers (storefront's consumer pact)
  - `consumer/` — what quill expects from the warehouse API
- `cmd/quill/` — process entrypoint (wires the above, launches HTTP + Kafka consumer)
