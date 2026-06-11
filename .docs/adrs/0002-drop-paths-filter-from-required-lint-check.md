# 2. Drop paths filter from the required lint workflow

- **Status**: Accepted
- **Date**: 2026-06-11

## Context

`.github/workflows/lint-bootstrap.yml` originally fired only when one of four watched files changed (`AGENTIC-BOOTSTRAP.md`, `CHANGELOG.md`, `scripts/lint_bootstrap.py`, the workflow file itself). The intent was cost-saving — skip CI when nothing relevant moved. After the develop-branch ruleset (see [ADR-0001](./0001-develop-trunk-with-ruleset-protection.md)) made `lint` a **required status check**, the trade-off changed: GitHub waits indefinitely for a required check to report, but a path-filtered workflow never runs at all on PRs touching files outside its filter. Both ends of the gate then sit forever, and the PR is stuck in "Waiting for status to be reported."

## Decision

Remove the `paths:` filter from both the `pull_request:` and `push:` triggers. The workflow now runs unconditionally on every PR and on every push to `main` / `develop`. The lint takes ~3 seconds; the cost is negligible.

A header comment in the workflow file documents *why* the filter is absent so it doesn't get re-added by reflex.

## Consequences

- Required status check (`lint`) reports on every PR, so the ruleset never gets stuck waiting.
- Marginal CI cost — three seconds per PR; no GitHub Actions billing risk for an open-source repo.
- Alternative considered and rejected: a tiny always-runs "satisfy the required check" job that reports success when the real lint is skipped. More config, more confusion, no benefit over running the real lint every time.
