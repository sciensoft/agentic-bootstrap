# Example — Go + Microservice

A trimmed sample of what the bootstrap produces for `LANG=Go` + `ARCH=MICROSERVICE`.

## Interview answers (relevant subset)

- `Q1 PROJECT_NAME` = `quill`
- `Q1 ONE_LINE_PURPOSE` = `Accept order events from the storefront and forward fulfilment requests to the warehouse.`
- `Q2 AGENTS_USED` = `[CLAUDE, COPILOT]`
- `Q4 LANG` = `Go`
- `Q5 ARCH` = `MICROSERVICE`
- `Q11 METRICS` = `true`
- `Q12 TESTING` = `true`

## What's shown here

| File | What it demonstrates |
| --- | --- |
| `AGENTS.md` | Primary brief. Claude reads it via `CLAUDE.md` adapter; Copilot reads it via `.github/copilot-instructions.md`. |
| `internal/presentation/http/orders_handler.go` | HTTP route. Validates request, calls service, formats response. No business logic. |
| `internal/presentation/health/health_handler.go` | `/healthz` (liveness — always 200) + `/readyz` (readiness — pings dependencies). |
| `internal/application/services/order_service.go` | Application service — orchestrates domain + infrastructure through interfaces. |
| `internal/infrastructure/clients/warehouse_client.go` | Outbound HTTP client to the warehouse service. Retries with backoff + circuit breaker + tracing propagation. |
| `contracts/provider/orders_api_test.go` | Consumer-driven contract test — verifies this service still honours the orders API. |

## What's NOT shown here

A real bootstrap run also produces: `.agents/rules/{workflow,workflow-todos,workflow-security,workflow-testing,best-practices,workflow-metrics,layered-architecture}.md`, `.docs/{adrs,prompts,todos,security}/`, `CLAUDE.md`, `.claude/settings.json`, `.github/copilot-instructions.md`, `go.mod`, `Dockerfile`, deploy manifest (Helm chart / Kubernetes YAML), `.golangci.yml`, `Makefile`, `.gitignore`, plus conventional repo files.

Browse the full template set in [`AGENTIC-BOOTSTRAP.md` Part 4](../../AGENTIC-BOOTSTRAP.md).
