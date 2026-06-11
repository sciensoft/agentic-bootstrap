# Restructure tool adapters as the community contribution surface

**Area**: maintenance / sustainability

**Refs**:
- [`.docs/adrs/0004-single-file-agent-executable-delivery-model.md`](../adrs/0004-single-file-agent-executable-delivery-model.md)
- [`AGENTIC-BOOTSTRAP.md`](../../AGENTIC-BOOTSTRAP.md) — Part 4 holds every per-tool template inline
- [`.docs/todos/version-watch-cron-action.md`](./version-watch-cron-action.md)

## Context

Each of the eight supported tools (Claude Code, Cursor, Aider, Codex CLI, OpenCode, Continue.dev, Windsurf, GitHub Copilot) can change its settings / permissions schema independently. Maintaining all 8 adapter templates as a solo maintainer is a treadmill (see [ADR-0004 consequences](../adrs/0004-single-file-agent-executable-delivery-model.md)). The mitigation: make the adapter templates the *contribution surface* — when Cursor 0.7 changes its config, a Cursor power user should be able to PR the fix without needing to understand the whole bootstrap.

Two structural options:

1. **Section-per-tool inside `AGENTIC-BOOTSTRAP.md`** — each tool's posture template gets its own clearly-named section so contributors can find the block by `grep`. CONTRIBUTING.md documents the contribution path: *"Cursor changed its settings format? Edit this section. PR it. Doctor mode tests it."*
2. **`tools/<tool>.md` partials** referenced from the main file (longer-term, only when the monolith becomes painful).

Doctor mode is already the drift-detection feedback loop. Add an explicit "tool-churn" CONTRIBUTING path so contributors know exactly what to PR.

## Deferred because

Single-file model still works at current size (~321 KB). Premature splitting introduces complexity without payoff. Wait for the first community PR that exposes friction, then refactor.

## Revisit when

After the first external tool-churn issue or PR — the pain that surfaces dictates the refactor shape (section reorder vs file split).
