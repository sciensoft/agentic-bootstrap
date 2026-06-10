# Workflow: keeping security checks honest

This rule supplements `workflow.md` for changes that touch a security-sensitive surface. The discipline: a lightweight per-request rubric pass before commit, full audits as dated sibling files re-run on cadence, findings that introduce a new mitigation pattern promoted to an ADR. The rubric, severity scale, and framework references all live in [`.docs/security/methodology.md`](../../.docs/security/methodology.md) — this rule says *when and how* to use it, not *what* it contains.

## When this rule applies

If your change touches any of these surfaces, walk the matching `§5.X` block of `methodology.md` before commit:

- **Authentication / sessions** — login, signup, OAuth, session storage, cookie flags (web).
- **Authorisation / access control** — owner-scoping, permission checks, multi-tenant boundaries (web).
- **Input validation** — request bodies, file uploads, URLs, free-form strings, CLI args, env vars (always).
- **SQL / data layer** — query construction, migrations, connection pool tuning (web / persistence).
- **Output encoding / templating** — HTML / Markdown rendering, sanitiser config, autoescape settings (web).
- **HTTP transport / browser-side** — security headers, CORS, CSRF, SRI, TrustedHost (web).
- **Secrets and configuration** — env vars, `.env.example` defaults, credential storage, boot-time logging of config (always).
- **Logging** — structured payload contents, levels, redaction discipline (always).
- **Rate limiting / resource caps** — per-actor limits, decode caps, generation budgets, agent-loop iteration caps (always — generalised to per-process / per-actor when not HTTP).
- **Dependency hygiene** — adding / upgrading deps, lockfile churn, CVE-scanner output (always).
- **LLM context** — system prompts, tool definitions, tool outputs reaching the model, agent loops, model supply chain (only when an LLM sits in the request path).

## When this rule does NOT apply

- Pure docs / copy edits, refactors with no behaviour change.
- Test additions that don't change production code paths.
- ADR or workflow-rule edits.
- Bug fixes that restore intended behaviour without changing the security model.

## Per-request: how the rubric pass works

The rubric in `methodology.md §5` is grouped by surface. For each surface your change touches:

1. Locate the matching `§5.X` block.
2. Walk each bullet and ask: *"does my change still satisfy this?"*. If yes, fine. If no, the change either fixes the regression *before* commit or includes a same-commit `.docs/todos/` entry citing the gap with a severity assessed per `§4` of `methodology.md`.
3. The pass is a self-review — no separate artefact is produced. The discipline is the act of walking the rubric, not a file you generate.

If your change introduces a *new* security-sensitive surface not yet covered (a new dependency layer, a new untrusted input source, a new tool the LLM can call), update `methodology.md §5` in the same commit so the next change has something to grep against. Treat that update like any other rule edit.

## Cadenced full audits

A full audit is a dated sibling file:
