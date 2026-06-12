# Quarterly per-tool adapter refresh ritual

**Area**: maintenance / per-tool adapters

**Refs**:
- [`AGENTIC-BOOTSTRAP.md`](../../AGENTIC-BOOTSTRAP.md) — Part 4 adapter templates (one section per tool)
- [`doctor-mode-upstream-check.md`](./doctor-mode-upstream-check.md) — automated counterpart to this ritual
- [`community-driven-adapter-contributions.md`](./community-driven-adapter-contributions.md) — longer-term, this ritual is replaced by distributed maintainership
- [`.docs/adrs/0004-single-file-agent-executable-delivery-model.md`](../adrs/0004-single-file-agent-executable-delivery-model.md) — the consequences list flags adapter drift as a known cost

## Context

The bootstrap supports 8 agentic tools (Claude Code, Cursor, Codex CLI, Continue.dev, Windsurf, Copilot, Aider, OpenCode) via per-tool adapter files that translate the tool-agnostic spine (`AGENTS.md` + `.agents/rules/`) into each tool's native config + permission format. When a tool's upstream format shifts (deprecated key, renamed section, new required field), the adapter silently goes stale and a user re-running an older bootstrap version gets an adapter that's subtly wrong against the current tool best-practice.

Already-observed examples in 2024–2025: Cursor's `.cursorrules` → `.cursor/rules/*.mdc`; Claude Code's `.claude/settings.json` schema bumps (permissions, hooks); Aider's metadata pipeline (`num_ctx` propagation through LiteLLM); Copilot's still-preview instructions file. The lint script catches internal cross-reference drift but cannot detect upstream-format drift. The "Works with 8 tools" claim on the landing page has roughly a 12-month half-life without this ritual.

This TODO is the ritual half of the mitigation. Every quarter:

1. Walk each tool's release notes / changelog / docs for changes since the last pass.
2. Compare the bootstrap's adapter template (Part 4) against the tool's current best-practice example.
3. Update the template + bump `<!-- bootstrap-version: -->` + add a `CHANGELOG.md` entry.
4. Edit this file in place to log the pass date and which adapters were touched. *Do not delete* — the file is the ritual's audit trail.

Pairs with [`doctor-mode-upstream-check.md`](./doctor-mode-upstream-check.md) — that's the automated half (catches drift between passes).

### Per-tool release-notes checklist (refresh URLs each pass — they shift)

- [ ] **Claude Code** — release notes at docs.claude.com (settings.json schema, hooks, permissions)
- [ ] **Cursor** — changelog.cursor.com + docs.cursor.com (`.cursor/rules/*.mdc` shape, settings.json)
- [ ] **Codex CLI** — github.com/openai/codex releases (`.codex/config.toml`, AGENTS.md handling)
- [ ] **Continue.dev** — github.com/continuedev/continue releases (`.continue/config.json` rules + tools blocks)
- [ ] **Windsurf** — docs.windsurf.com + Codeium changelog (`.windsurfrules`, settings.json)
- [ ] **Copilot** — github.blog/changelog/label/copilot (`.github/copilot-instructions.md` direction)
- [ ] **Aider** — github.com/Aider-AI/aider releases (`.aider.conf.yml`, model-metadata pipeline)
- [ ] **OpenCode** — github.com/sst/opencode releases (AGENTS.md interpretation)

### Pass log

*Edit in place after each quarterly pass — the git log of this file is the audit trail.*

- 2026-09-01 (Q3 2026 planned): not yet completed
- 2026-12-01 (Q4 2026 planned): not yet completed
- 2027-03-01 (Q1 2027 planned): not yet completed
- 2027-06-01 (Q2 2027 planned): not yet completed

## Deferred because

Continuous monitoring across 8 tools is not realistic for a single maintainer; a scheduled cadence ritual is the realistic compromise. The ritual stays as a TODO (not an ADR) because it's a process commitment, not a structural decision.

## Revisit when

Every quarter on the first of the month — first scheduled pass: **2026-09-01** (Q3 2026). Stop revisiting only when [`community-driven-adapter-contributions.md`](./community-driven-adapter-contributions.md) has matured into per-tool maintainers covering most of the load (the distributed-maintainership model that replaces this ritual).
