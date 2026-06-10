# Bootstrap changelog

The bootstrap's own change log. Each entry covers one notable version of [`AGENTIC_BOOTSTRAP.md`](./AGENTIC_BOOTSTRAP.md). On re-run, the Step 8 report names the version delta and surfaces the relevant bullets so the user sees what changed.

Format: Keep a Changelog, dated by ISO date. The version marker at the top of `AGENTIC_BOOTSTRAP.md` (`<!-- bootstrap-version: <YYYY-MM-DD> -->`) is what the bootstrap reads to detect upgrades — bump it whenever you publish a notable change.

## [Unreleased]

### Added

- Bootstrap version header + `BOOTSTRAP_CHANGELOG.md` + Step 8 upgrade narrative — re-runs now name the version delta and surface relevant changes.
- Bootstrap-doctor mode — audit-only invocation that produces a structured drift report against an existing project (no writes).
- `CONTRIBUTING.md` for this repo — how to add ARCH templates, tool adapters, feature gates, and language scaffolds.
- `QUICKSTART.md` — 60-second human-readable quickstart, separate from the operational prompt.
- 3 example projects under `examples/` — `python-4layer-ddd`, `typescript-vertical-slice`, `go-microservice`. Browseable proof of what the bootstrap produces.

### Changed

- Architecture variants extracted from the monolithic file into `templates/architectures/` — lazy-loaded based on Q5 `ARCH`. Cuts per-bootstrap token cost ~30% on top of the existing 16-question interview cost.

## [2026-06-10] — Multi-tool refactor + testing rule + Mermaid picker + Hexagonal/Microservice/Vertical Slice

### Added

- Interview question Q2 `AGENTS_USED` — multi-select of agentic coding assistants the project supports. Bootstrap now writes per-tool adapters for whichever assistants are picked.
- Per-tool adapter templates: Cursor (`.cursor/rules/agents.mdc`), Aider (`.aider.conf.yml`), Continue.dev (`.continue/config.json`), Windsurf (`.windsurfrules`), GitHub Copilot (`.github/copilot-instructions.md`). Codex CLI and OpenCode read `AGENTS.md` natively.
- Interview question Q12 `TESTING` — opt-in testing discipline. Installs `workflow-testing.md` (pyramid shape, mock-at-boundaries, regression-first for bug fixes, TDD encouraged not mandated, coverage tracked without a hard floor, tests bundled into the same commit as code).
- Step 4b — best-practices.md refinement. When the running agent has web search, the bootstrap probes current sources for the user's stack and synthesises a refined `best-practices.md` with inline citations. Falls back to a stub with per-agent enablement guidance when web access isn't available. Never blocks.
- Q5 disambiguation table — routes topology answers (microservice, monorepo, modular monolith, serverless), vocabulary aliases (hexagonal, ports-and-adapters, clean, onion), and bare *DDD* to the right ARCH slot.
- Two new ARCH slots: `HEXAGONAL` (Ports and Adapters family — covers Hexagonal / Clean / Onion in one template) and `MONOREPO` / `SERVERLESS` (added earlier).
- Two more ARCH slots: `MICROSERVICE` (one service in a larger ecosystem with cross-service conventions) and `VERTICAL_SLICE` (feature-first layout with per-feature thin layers).
- Mermaid diagram-type picker in `workflow.md` — 22+ diagram types catalogued (flowchart, sequenceDiagram, stateDiagram-v2, erDiagram, classDiagram, C4Context/Container/Component/Deployment/Dynamic, gitGraph, gantt, timeline, journey, mindmap, pie, sankey-beta, xychart-beta, quadrantChart, radar, requirementDiagram, block-beta, architecture-beta, kanban, packet-beta, treemap) with worked examples, readability conventions, and a context-driven framing ("the choice depends on the request, situation, problem, and solution — not on a lookup table").

### Changed

- **Spine inverted**: `AGENTS.md` is now the primary brief; `CLAUDE.md` becomes a Claude-specific adapter pointing at `AGENTS.md`. The cross-tool convention now leads.
- Rules moved from `.claude/rules/` to `.agents/rules/`. Answer cache moved from `.claude/bootstrap.json` to `.agents/bootstrap.json`. `.claude/settings.json` stays Claude-specific.
- Q3 `POSTURE` is now conditional on `CLAUDE ∈ AGENTS_USED`; skipped (and `.claude/settings.json` skipped) otherwise.
- `best-practices.md` template split into refined-variant (generation contract for the web-search path) and stub-variant (literal template with per-agent enablement matrix).

### Migration

- Projects bootstrapped under the pre-multi-tool layout (rules under `.claude/rules/`, answer cache at `.claude/bootstrap.json`) are detected at Step 0 and offered a migration prompt — accept to move into `.agents/rules/` + `.agents/bootstrap.json` so other assistants can be added, or decline to keep the legacy paths for this re-run.

---

## Format

When updating this file: add to `[Unreleased]` as you go; when the change is meaningful enough to bump the bootstrap version, rename `[Unreleased]` to `[<YYYY-MM-DD>] — <short summary>`, bump the `<!-- bootstrap-version: ... -->` header in `AGENTIC_BOOTSTRAP.md` to the same date, and start a new empty `[Unreleased]` block above. Existing projects re-running the bootstrap will see the new version's bullets in their Step 8 report.
