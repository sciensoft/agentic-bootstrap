<!-- markdownlint-disable MD024 -->
<!-- MD024 disabled: Keep-a-Changelog nests Added/Changed/Removed under every version section — duplicates are the format. -->

# Bootstrap changelog

The bootstrap's own change log. Each entry covers one notable version of [`AGENTIC-BOOTSTRAP.md`](./AGENTIC-BOOTSTRAP.md). On re-run, the Step 8 report names the version delta and surfaces the relevant bullets so the user sees what changed.

Format: Keep a Changelog, dated by ISO date. The version marker at the top of `AGENTIC-BOOTSTRAP.md` (`<!-- bootstrap-version: <YYYY-MM-DD> -->`) is what the bootstrap reads to detect upgrades — bump it whenever you publish a notable change.

## [Unreleased]

### Added

- **Part 4 Template Index for offset-read selective loading.** A line-range table at the start of Part 4 mapping each of the ~80 templates to its trigger flag and `start → end` line offsets. Paired with a performance tip in Part 1 Step 4 instructing agents with `offset`-capable Read tools (Claude Code, Cursor, Aider, Codex CLI) to load *only* the templates the captured answers require — skipping the irrelevant ~65 templates a typical bootstrap doesn't touch. Cuts scaffold-time token cost from ~75k → ~25k for smart agents (~60–70% reduction); naive readers fall through to top-to-bottom reading with no regression. Landing page Runtime footprint section updated to reflect the three-number story (smart scaffold · naive fallback · runtime).

### Changed

- **Q4 reframed for language inclusivity.** Renamed *"Language / runtime"* → *"Primary language or content type"*. Question text now lists eleven named examples (Python, TypeScript, Go, Rust, C# / .NET, Java, Ruby, PHP, Kotlin, Swift, Markdown / docs-as-code) plus *"something else"* instead of leading with four named languages. Names the first-class-scaffold coverage gap explicitly and points contributors at `CONTRIBUTING.md` for the one-PR pattern to add a new variant. No template changes — Python / TypeScript / Go / Rust remain the only languages with full scaffolds; everything else continues to land on the existing fallback variant. `QUICKSTART.md` Q4 description updated to match.

## [2026-06-12] — Shared-frontend propagation rule + landing-page contribute section

### Added

- **Q13 `FRONTEND` feature gate.** New opt-in interview question installing **two complementary rule files**:
  - `.agents/rules/workflow-frontend.md` — the *touch-source-sweep-consumers* propagation discipline for shared frontend code. When a request says *"fix component X on page Y"*, the rule forces the agent to find the canonical source via `grep`, edit there (not the consumer), list every importer in the prompt file, sweep each consumer for regressions and opportunities, and fold the consumer updates into the same commit. Anti-patterns called out: inline "quick fix" copies, forking shared components into `v2` variants, leaving stale consumers after a prop rename, hard-coding values where a design token exists.
  - `.agents/rules/frontend-visibility.md` — the *closing-the-loop* companion. Markdown rules can't fix the bigger friction in agentic frontend work: the engineer *sees* a rendered UI, the agent has no eyes. This file documents the per-agent browser-tooling setup (Playwright MCP for Claude, `@web` for Cursor, screenshot-piping for Aider, etc.), the Storybook / Histoire convention for the visual catalog, the engineer-side reporting convention (*screenshot + route + component + symptom + desired outcome*), and the agent-side response convention (open via MCP if available; ask for a screenshot otherwise; `grep` for the source; cross-reference `ui-components.md`).
- Landing-page **Contribute / feedback section** before the CTA — three linked cards (Bug report → Issues, Discussion → Discussions, Pull request → Compare) with copy that names what to include in each.

### Changed

- Interview count bumped from 16 to 17. Previous Q13–Q16 (LICENSE / CONTRIB / RUN_INSTRUCTIONS / ADDITIONAL) renumbered to Q14–Q17. `bootstrap.json` schema gains the `FRONTEND` boolean key. AGENTS.md template + Claude / Cursor / Aider / Windsurf / Copilot adapters all carry a new `{{IF_FRONTEND}}` reference so the rule is loaded automatically when the gate is on.
- `workflow.md` commit checklist gains a `{{IF_FRONTEND}}` line: *"For shared frontend changes: every consumer update that follows from the change."*

### Migration

- Existing projects pick up the new question on next re-run. If the project has a UI surface, answer `yes` to install the rule; otherwise `no` and re-run is idempotent.

## [2026-06-11] — Per-tool permission posture fan-out + adoption scaffolding

### Added

- Bootstrap version header + `CHANGELOG.md` + Step 8 upgrade narrative — re-runs now name the version delta and surface relevant changes.
- Bootstrap-doctor mode — audit-only invocation that produces a structured drift report against an existing project (no writes).
- `CONTRIBUTING.md` for this repo — how to add ARCH templates, tool adapters, feature gates, and language scaffolds.
- `QUICKSTART.md` — 60-second human-readable quickstart, separate from the operational prompt.
- 3 example projects under `examples/` — `python-4layer-ddd`, `typescript-vertical-slice`, `go-microservice`. Browseable proof of what the bootstrap produces.
- `scripts/lint_bootstrap.py` + `.github/workflows/lint-bootstrap.yml` — consistency lint for `AGENTIC-BOOTSTRAP.md` with four checks (Q-numbers sequential, `{{IF_FLAG}}` references match `bootstrap.json` schema, decision-matrix rows point to existing Part 4 templates, version header matches latest dated changelog entry). Runs on every PR.
- Per-tool permission-posture templates — Q3 `POSTURE` is now a single tool-agnostic intent that fans out into every tool's native permission config: `.claude/settings.json`, `.cursor/settings.json`, `.codex/config.toml`, `.windsurf/settings.json` (each in 4 variants), plus `IF_POSTURE_*` blocks in the existing `.aider.conf.yml` and `.continue/config.json` adapters. OpenCode and GitHub Copilot don't have file-based permission models; their adapters carry a posture-intent note for the user to apply manually.
- SVG favicon + theme-color meta on the landing page matching the brand mark.
- Landing-page "Adoption" section with linked cards (examples, quickstart, doctor mode), positioning table vs Cookiecutter / copier / hand-typed agent brief, trust signals (Star button, version badge linking to changelog, Contribute button, CI status badge).

### Changed

- **Q3 POSTURE is now unconditional and tool-agnostic.** Previously asked only if `CLAUDE ∈ AGENTS_USED` and the `N_A` value skipped `.claude/settings.json`. Now always asked, value drives a per-tool autonomy config for every assistant in `AGENTS_USED`. `POSTURE=N_A` is no longer a valid value.
- `AGENTS.md` is now the primary cross-tool brief; `CLAUDE.md` is a thin Claude-specific adapter pointing at it.
- Landing-page Postures section reframed agent-agnostic (no longer "For Claude Code, ...").
- Landing-page + QUICKSTART positioning table renamed "Hand-typed CLAUDE.md" column to "Hand-typed agent brief" and added a row for the per-tool permission posture capability.
- Landing-page prose `todo` / `todos` capitalized to `TODO` / `TODOs` (file paths kept lowercase).

### Migration

- Projects bootstrapped under the previous version where `CLAUDE ∉ AGENTS_USED` and `POSTURE=N_A`: on re-run, the agent re-asks Q3 to capture a real posture, then writes per-tool configs for the rest of the assistants in `AGENTS_USED`.

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

When updating this file: add to `[Unreleased]` as you go; when the change is meaningful enough to bump the bootstrap version, rename `[Unreleased]` to `[<YYYY-MM-DD>] — <short summary>`, bump the `<!-- bootstrap-version: ... -->` header in `AGENTIC-BOOTSTRAP.md` to the same date, and start a new empty `[Unreleased]` block above. Existing projects re-running the bootstrap will see the new version's bullets in their Step 8 report.
