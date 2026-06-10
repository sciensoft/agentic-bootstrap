# Copilot instructions — quill

This project follows the **agentic-bootstrap** workflow discipline. The canonical, full brief lives in [`AGENTS.md`](../AGENTS.md) and the rule files under [`.agents/rules/`](../.agents/rules/). Read those before any non-trivial change.

## Workflow (summary — full text in `.agents/rules/workflow.md`)

Every artifact-producing request bundles:

1. A **prompt file** at `.docs/prompts/<unix-timestamp>.<slug>.md` capturing the request, reasoning, and output.
2. A **new or updated ADR** under `.docs/adrs/` when the change is architecturally significant (new module / pattern / dependency / contract).
3. **Telemetry kept current** — logs added/updated for new and changed code paths, at log levels matching the event's signal (DEBUG / INFO / WARNING / ERROR / CRITICAL), with no credentials / PII / billing IDs / request bodies in log output.
4. A **single commit** bundling all of the above, with an explicit `git add` (never `git add -A`).
5. A **push** to the remote when the commit succeeds.

Deferred ideas go to `.docs/todos/` as one file per entry — never as inline TODO comments or undocumented promises.

## Best practices (summary — full text in `.agents/rules/best-practices.md`)

- Dependency injection at the composition root; never instantiate infrastructure inside business logic.
- Repositories own data access; services own use cases; presentation orchestrates.
- Names are intent-revealing; comments are reserved for non-obvious *why*, not *what*.
- Tests cover behaviour at the right layer; mock at boundaries, not internals.

## Security (summary — full text in `.agents/rules/workflow-security.md`)

Before any security-sensitive commit, walk the rubric in [`.docs/security/methodology.md`](../.docs/security/methodology.md) for the surfaces your change touches (auth, inputs, SQL, output, transport, secrets, logging, rate limits, deps, LLM context). Full dated audits live as sibling files under `.docs/security/`.

## Testing (summary — full text in `.agents/rules/workflow-testing.md`)

Every artifact-producing change ships with its tests in the same commit. Pyramid shape: unit-heavy, integration-light, e2e-thin. Mock at boundaries (HTTP, clock, randomness, third-party SDKs) — never internals. Bug fixes start with a failing regression test. TDD is encouraged but not mandated; the hard rule is *tests + code in the same commit*. Coverage is tracked, not gated by a percentage. Flaky tests are P1 — fix or quarantine with a dated entry under `.docs/todos/`.

When this file and `AGENTS.md` disagree, `AGENTS.md` wins.
