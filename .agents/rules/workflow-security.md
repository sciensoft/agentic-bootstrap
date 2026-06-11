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

```text
.docs/security/<YYYY-MM-DD>-<slug>.md
```

The audit:

- Cites this rule + `methodology.md` for framework, severity, and rubric definitions (don't re-state them).
- Walks every `§5` surface in the order defined by `methodology.md §3`.
- Captures findings as `(severity, file:line, what, risk, recommendation)`.
- Captures an `[Info]` note for surfaces with no findings — so absences are explicit, not implicit.
- Closes with a prioritised recommendation list (highest risk reduction per hour first).
- Has an explicit "out of scope" section.

Cadence triggers:

- **Calendar** — every N months (3 / 6 / 12, depending on project risk profile).
- **Significant surface change** — a new auth provider, the first user-uploaded content endpoint, the first LLM tool call, a new external integration that broadens the trust boundary.
- **Pre-release** — before the first public deploy; before tier expansions that materially change exposure.
- **Reactive** — after a CVE drops on a high-velocity dep the project uses, after a security-relevant incident anywhere in the stack.

Previous audits stay where they are; the new audit is a sibling. The diff between audits is the project's security trend over time. A re-run after the prioritised recommendations from the previous audit ship should produce a noticeably shorter `[High]` list — that's the signal the previous audit caught real risk, not just style.

## Findings → ADRs

When a finding's fix introduces a *pattern future code is expected to follow* — a new middleware, a new repository-layer check, a new sanitiser, a new dependency convention — promote the decision to an ADR under `.docs/adrs/`. The ADR captures the pattern; the audit file captures the finding that motivated it. Cross-link both ways.

When a finding is fixed *without* introducing a load-bearing pattern (a one-off config tweak, a one-off bug fix), the audit file plus the regular workflow.md commit are enough — no ADR needed.

## Why this rule exists

Security regressions are slow and silent — a missing `Secure` flag on a cookie, a forgotten owner-scope on a new endpoint, a `trust_remote_code=True` snuck in by a careless model swap, a SQL query that grew an f-string when it was refactored. None of these crash the test suite; all of them produce real incidents.

Coupling the rubric to every security-relevant commit (lightweight, surface-scoped) and to scheduled audits (deep, whole-surface) keeps the security posture from drifting while staying proportional to project shape — small projects don't pay an OAuth-review cost if they have no auth.
