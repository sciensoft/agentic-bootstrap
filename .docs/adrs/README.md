# Architecture Decision Records

This directory holds the [Architecture Decision Records (ADRs)](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) for the project. Each ADR is a short markdown file capturing one structural decision: the context that prompted it, what was decided, and the consequences. Read these before making structural changes.

## Index

| # | Title | Status | Date |
| --- | --- | --- | --- |
| [0000](./0000-template.md) | ADR Template (do not cite) | Template | — |
| [0001](./0001-develop-trunk-with-ruleset-protection.md) | `develop` as trunk with GitHub Ruleset protection | Accepted | 2026-06-11 |
| [0002](./0002-drop-paths-filter-from-required-lint-check.md) | Drop paths filter from the required lint workflow | Accepted | 2026-06-11 |
| [0003](./0003-standardize-on-changelog-md.md) | Standardize on `CHANGELOG.md` (drop the `BOOTSTRAP_` prefix) | Accepted | 2026-06-11 |
| [0004](./0004-single-file-agent-executable-delivery-model.md) | Single-file, agent-executable delivery model | Accepted | 2026-06-11 |
| [0005](./0005-custom-domain-agentic-bootstrap-md.md) | Custom domain `agentic-bootstrap.md` for the landing page | Accepted | 2026-06-11 |
| [0006](./0006-keep-changelog-md-always-not-opt-in.md) | Keep `CHANGELOG.md` always-written, not gated by `CONTRIB` | Accepted | 2026-06-11 |
| [0007](./0007-structured-contribution-intake.md) | Structured contribution intake — issue templates, PR template, CODEOWNERS, SECURITY.md | Accepted | 2026-06-11 |

(Append new ADRs as `NNNN-<kebab-slug>.md` and add a row here in the same commit. See `.agents/rules/workflow.md` for when an ADR is required.)
