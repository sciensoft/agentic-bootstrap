# Example — Python + 4-Layer DDD

A trimmed sample of what the bootstrap produces for `LANG=Python` + `ARCH=4_LAYER_DDD`.

## Interview answers (relevant subset)

- `Q1 PROJECT_NAME` = `orbital`
- `Q1 ONE_LINE_PURPOSE` = `Track and analyse satellite orbital decay events.`
- `Q2 AGENTS_USED` = `[CLAUDE]`
- `Q3 POSTURE` = `TRUSTED_DEV`
- `Q4 LANG` = `Python`
- `Q5 ARCH` = `4_LAYER_DDD`
- `Q7 LLM` = `false`
- `Q12 TESTING` = `true`

## What's shown here

| File | What it demonstrates |
| --- | --- |
| `AGENTS.md` | The primary brief. Every agent reads this. |
| `presentation/routes/orders.py` | Route handler — orchestrates: resolves the viewer, calls the service, renders the response. No business logic. |
| `application/services/order_service.py` | Application service — constructor-injected dependencies; orchestrates domain + infrastructure through interfaces. |
| `domain/model/order.py` | Pure domain types. Zero outward imports. |
| `domain/interfaces/order_repository.py` | The contract the application depends on; the infrastructure implements. |
| `infrastructure/repositories/order_postgres_repository.py` | Concrete adapter. The only layer that talks to the outside world. |
| `tests/test_order_service.py` | Service tested against an in-memory fake repository — no DB needed for unit-level coverage. |

## What's NOT shown here

A real bootstrap run also produces: `.agents/rules/{workflow,workflow-todos,workflow-security,workflow-testing,best-practices,layered-architecture}.md`, `.docs/{adrs,prompts,todos,security}/`, `CLAUDE.md` adapter, `.claude/settings.json`, `pyproject.toml`, `ruff.toml`, `Makefile`, `.gitignore`, `.env.example`, `tests/conftest.py`, and the conventional repo files (`README.md`, `LICENSE`, `SECURITY.md`, `CHANGELOG.md`, `.pre-commit-config.yaml`, `.gitattributes`, `.editorconfig`).

Browse the full template set in [`AGENTIC_BOOTSTRAP.md` Part 4](../../AGENTIC_BOOTSTRAP.md).
