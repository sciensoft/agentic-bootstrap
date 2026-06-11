# Agentic Bootstrap

Single-file scaffold that hands AI coding agents a disciplined workflow.

## Purpose

Agentic Bootstrap is a one-file artifact (`AGENTIC-BOOTSTRAP.md`) an engineer pastes into a fresh repo so an AI coding agent (Claude Code, Cursor, Aider, Codex CLI, Continue, Windsurf, Copilot, OpenCode) can scaffold the project with a consistent posture: a tool-agnostic spine in `AGENTS.md` + `.agents/rules/`, per-tool adapters that point back at it, ADRs under `.docs/adrs/`, a security methodology under `.docs/security/`, and conventional repo files (`README`, `LICENSE`, `SECURITY.md`, `CHANGELOG.md`, `.gitignore`, `.editorconfig`, etc.) sized to the answers from a short interview. The project is *self-applied*: this very repo is bootstrapped from its own `AGENTIC-BOOTSTRAP.md`.

## Rules

Always follow the rules in `.agents/rules/`:

- [`workflow.md`](.agents/rules/workflow.md) — every artifact-producing request gets a timestamped prompt file under `.docs/prompts/`, an optional new-or-updated ADR under `.docs/adrs/`, telemetry kept current (logs added/updated for new and changed code paths, at log levels that match each event's signal — DEBUG / INFO / WARNING / ERROR / CRITICAL — with sensitive-data redaction discipline covering credentials, PII, billing identifiers, and request bodies), a single git commit bundling the lot, and a push. Also defines how do-later ideas get captured proactively.
- [`workflow-todos.md`](.agents/rules/workflow-todos.md) — the discipline for managing deferred ideas. Entries live as one file per idea under [`.docs/todos/`](.docs/todos/). Capture entries proactively when the user defers something ("for now / later / hold this"), sweep entries when a commit satisfies their *Revisit when* trigger, `git rm` rather than archive (git log is canonical).
- [`workflow-security.md`](.agents/rules/workflow-security.md) — companion to `workflow.md` for security-sensitive changes. Before commit, walk the rubric in [`.docs/security/methodology.md`](.docs/security/methodology.md) for surfaces your change touches (auth, inputs, SQL, output, transport, secrets, logging, rate limits, deps, LLM context). Full audits live as dated sibling files under `.docs/security/<YYYY-MM-DD>-<slug>.md` and re-run on cadence.
- [`best-practices.md`](.agents/rules/best-practices.md) — naming, dependency injection, repository / service patterns, language idioms, do/don't lists.
- [`workflow-changes.md`](.agents/rules/workflow-changes.md) — companion to `workflow.md` for *product-affecting* changes. When a change alters anything a user can see, the surfaces that describe it must move in the same commit.

Architecture decisions and their trade-offs live in [`.docs/adrs/`](.docs/adrs/) — read these before making structural changes.

## Run

`python scripts/lint_bootstrap.py`; open `docs/index.html` for the landing-page preview

## Architecture map

[Short pointer to where the main pieces live. Add an `ARCHITECTURE.md` at the repo root if the project grows enough to need its own tree + diagram.]

## Conventions (summary)

See [`.agents/rules/best-practices.md`](.agents/rules/best-practices.md) for full detail.

## Maintenance notes

The bootstrap file IS the artifact; modify only via deliberate PRs that bump the `<!-- bootstrap-version: -->` header. The lint script at `scripts/lint_bootstrap.py` validates four cross-reference invariants and runs in CI on every PR.
