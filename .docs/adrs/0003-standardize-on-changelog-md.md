# 3. Standardize on `CHANGELOG.md` (drop the `BOOTSTRAP_` prefix)

- **Status**: Accepted
- **Date**: 2026-06-11

## Context

The version log started life as `BOOTSTRAP_CHANGELOG.md` early in development — at the time, "bootstrap" felt load-bearing in the name because the file was the only versioned thing in a single-file project. By June 2026 the justification had eroded: the whole repo IS the bootstrap; the `BOOTSTRAP_` prefix was redundant. `CHANGELOG.md` is the universal convention — GitHub auto-detects it for the Releases sidebar, contributors look there by reflex, and the bootstrap itself scaffolds a `CHANGELOG.md` for downstream projects under the same convention. The repo not following its own convention was a credibility smell.

## Decision

Rename `BOOTSTRAP_CHANGELOG.md` → `CHANGELOG.md` via `git mv` (preserves 98% file similarity for `git log --follow`). Update all 22 references across 8 files (README, QUICKSTART, CONTRIBUTING, AGENTIC-BOOTSTRAP.md, docs/index.html, scripts/lint_bootstrap.py, .github/workflows/lint-bootstrap.yml, plus a self-reference inside the changelog itself).

## Consequences

- GitHub Releases sidebar now picks up the file automatically.
- The project eats its own dog food — its top-level convention matches what it scaffolds downstream.
- One-shot rename via bulk `sed` plus the `git mv`; lint script's four checks stayed green throughout.
- Future PRs adding `[Unreleased]` entries (per CONTRIBUTING.md) cite `CHANGELOG.md` everywhere; no stale path references remain.
- Downstream contract: anyone who deep-linked to `BOOTSTRAP_CHANGELOG.md` will 404 against the live repo, but git history preserves the old name via `git log --follow CHANGELOG.md`.
- Related policy considered and kept: see [ADR-0006](./0006-keep-changelog-md-always-not-opt-in.md) — the file remains Always-written, not opt-in.
