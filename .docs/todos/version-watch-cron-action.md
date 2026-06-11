# Version-watch GitHub Action for the 8 supported tools

**Area**: maintenance / sustainability

**Refs**:
- [`.docs/todos/community-driven-adapter-contributions.md`](./community-driven-adapter-contributions.md)
- [`.github/ISSUE_TEMPLATE/tool-churn.yml`](../../.github/ISSUE_TEMPLATE/tool-churn.yml)

## Context

Nightly cron workflow that hits each tool's GitHub Releases feed, detects new minor versions, and opens an issue against the bootstrap when one appears. Turns latent tool-schema churn into an early-warning signal. Cheap to implement (most tools publish releases programmatically); no scraping fragility.

Initial mapping (verify the actual repo/release-feed path before wiring):

| Tool | Likely release feed |
|---|---|
| Claude Code | `anthropics/claude-code` |
| Cursor | `getcursor/cursor` (or vendor changelog) |
| Aider | `paul-gauthier/aider` |
| Codex CLI | `openai/codex` |
| OpenCode | `opencode-ai/opencode` |
| Continue.dev | `continuedev/continue` |
| Windsurf | Codeium org — find the right repo |
| GitHub Copilot | No public release feed; skip the cron, rely on changelog scraping or manual notice |

## Deferred because

No tool-churn issues yet. Building the workflow before any real schema change happens is speculative engineering — and the first churn event will inform what the cron actually needs to check (just version number? release-notes keyword scan? diff of a specific config schema?).

## Revisit when

After the first tool-churn issue is filed (whether by the maintainer or a contributor). That validates demand; *then* build the cron to catch the next one earlier.
