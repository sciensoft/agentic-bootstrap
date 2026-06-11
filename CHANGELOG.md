<!-- markdownlint-disable MD024 -->
<!-- MD024 disabled: Keep-a-Changelog nests Added/Changed/Removed under every version section — duplicates are the format. -->

# Bootstrap changelog

The bootstrap's own change log. Each entry covers one notable version of [`AGENTIC-BOOTSTRAP.md`](./AGENTIC-BOOTSTRAP.md). On re-run, the Step 8 report names the version delta and surfaces the relevant bullets so the user sees what changed.

Format: Keep a Changelog, dated by ISO date. The version marker at the top of `AGENTIC-BOOTSTRAP.md` (`<!-- bootstrap-version: <YYYY-MM-DD> -->`) is what the bootstrap reads to detect upgrades — bump it whenever you publish a notable change.

## [Unreleased]

### Added

- **Bootstrap-hardening prose against step-skipping agents.** Five focused additions to make a weaker / less-careful model's failure mode more visible and harder to fall into, triggered by a real Aider + `deepseek-r1:14b` debug session where the agent skipped Steps 0–3 and wrote files containing literal `{{PROJECT_NAME}}` etc. unsubstituted:
  - **`STOP` callout** above Part 1 — high-visibility block reading *"this is a multi-step playbook, not a list of files to create"* with the ordered step list inline. Sits between the *Before you start* sub-section and the Part 1 heading.
  - **`Before you start` sub-section** under *How to use* — names the failure modes explicitly (literal `{{PLACEHOLDER}}` tokens in output, Step 2 skipped, all 17 questions dumped at once) so the agent has the pattern to refuse if it's tempted.
  - **Model-capability note** inside *Before you start* — names the model classes that handle the playbook reliably (Claude Sonnet / Opus, GPT-4 class, Gemini 1.5 / 2.x, full DeepSeek-V3, Qwen 2.5 Coder 32B+) and the failure mode of smaller distilled reasoning models. Same copy as the landing-page advisory shipped in `feat/landing-bootstrap-tips`.
  - **Step 0 imperative opener** — *"Your first action: read this entire file. Do not write anything yet."* leads the section instead of being buried mid-paragraph.
  - **Step 4 gate check** — before the existing performance tip, an explicit *"do not start Step 4 unless Steps 0–3 are complete"* with the `{{PLACEHOLDER}} + {{IF_FLAG}}` reasoning attached. Makes the dependency between Step 2 and Step 4 visible at the entry point an offset-read-capable agent might hit directly.

### Changed

- **Category B editorial passes (Step 0 + Doctor mode + Q14).** Three independent tightening passes shipped together:
  - **Step 0 legacy-layout megabullet** broken into three sub-bullets (Migrate / Leave / Either way) under one parent bullet. The original was ~280 words of nested conditionals in a single bullet; the new shape preserves all three branches but is half the length and skim-able.
  - **Doctor mode 10-item checklist** converted from a numbered prose list to a `# / Check / What to flag` table. Each row is now one line instead of three-to-five; the *Critical / Stale / Drift / Informational* severity grouping under "Report shape" still maps cleanly to the rows.
  - **Q14 LICENSE** compressed into the same question + sub-table pattern as Q2 / Q3 / Q5. The four options stay inline as a compact one-line picker for chat-only renderers; a new **License options** sub-table adds a *Fits when* column with concrete guidance (hobby projects · larger OSS with corporate contributors · internal codebases · undecided experiments) that the original prose didn't surface.
  - All three passes preserve behaviour — same flag values, same Step 8 narrative, same Doctor failure modes. Template Index offsets refreshed by 78 rows to absorb the line shifts.

### Added

- **Landing page: two small reminders in the "Three steps" section.** (1) A six-word note under the Tell-the-agent code block — *"Re-run is safe — it's idempotent."* with a small refresh-arrow glyph — handles the case where an agent stalls mid-bootstrap, matched real `deepseek-r1:14b` + Aider behaviour observed in a debug session. (2) A single-sentence advisory below the three cards naming the model classes that handle the playbook reliably (Claude Sonnet / Opus, GPT-4 class, Gemini 1.5 / 2.x, full DeepSeek-V3, Qwen 2.5 Coder 32B+) and the failure mode of smaller distilled reasoners (skipping steps in an 80-template multi-step orchestration). Phrased as guidance, not gatekeeping — *"may skip steps; use a bigger model for this one-time scaffold."*
- **Landing page: copy buttons on the two "Three steps" code blocks.** The `Drop the file` curl command and the `Tell the agent` prompt now carry a small icon button (top-right corner of each code block) that copies the clean command — no `$` shell prompt, no `›` chevron — to the clipboard with one click. Visual feedback: icon swaps from a copy glyph to a violet checkmark for 1.5s after a successful write. Uses the modern `navigator.clipboard.writeText` API with a silent no-op fallback if the host browser doesn't support it. The actual text to copy lives in a `data-copy` attribute on each `.codeblock`, decoupled from the syntax-highlighted display markup. Accessibility: each button has an `aria-label` that updates to "Copied!" during the feedback window and restores afterwards.
- **5th lint check: Template Index offsets ↔ actual `### Template:` positions.** [`scripts/lint_bootstrap.py`](./scripts/lint_bootstrap.py) now parses the Part 4 Template Index table and compares each row's `start → end` offsets against the actual heading positions in the file. Drift is caught in CI before it ships; the failure message names the first few mismatching rows and tells the maintainer to re-grep `^### Template:` to refresh. Concurrent with this PR, the existing offsets — stale by +16 lines from #12 — were refreshed (78 rows updated). Closes the follow-up tracked at `.docs/todos/lint-template-index-offsets.md` (now `git rm`'d per the workflow-todos rule). The success message bumps from *"4 checks passed"* to *"5 checks passed"*.

### Changed

- **Interview Step 2: hard rule that questions are asked one at a time.** Bug surfaced in a real Aider session — the previous Step 2 instruction (*"otherwise ask one question at a time in chat"* buried at the tail of a paragraph) was too quiet for chat-only agents to follow. Aider dumped all 17 questions in one wall-of-text message, then dumped them again after Q1, until the user manually typed *"ask one question at a time please!"*. Step 2 now leads with the rule as a bolded directive, names the failure mode it prevents, lists the concrete 5-step protocol (ask one · wait · disambiguate within turn · record · move on), and explicitly distinguishes structured-picker hosts (Claude Code, Cursor) from chat-only hosts (Aider, Codex CLI, OpenCode). A defensive callout at the start of Part 2 reminds any agent that lands directly on the interview to honour the rule. Same questions, same flag set — only the agent-facing protocol changes.
- **Q2 and Q3 compressed into question + sub-table pairs.** Same pattern as the Q5 compression in #12. Q2 (AGENTS_USED) was a 945-char inline list of 8 tools with adapter descriptions; now a short question + a **Supported tools** sub-table with a `AGENTS.md natively?` column that surfaces a previously-buried fact (Codex CLI and OpenCode read AGENTS.md natively — two of eight need no adapter file). Q3 (POSTURE) was a 1,537-char paragraph of four posture descriptions glued together; now a short question + a **Posture options** sub-table (`Slot · Pre-allowed · Still prompts · Fits when`) with the `TRUSTED_DEV` language-toolchain cross-reference moved into a one-line footnote. Same flag values, same dispatch logic, same per-tool permission fan-out — only the user-facing text changes. Chat-only agents that paste verbatim render the question + the table together; smart picker hosts (Claude Code, Cursor) use the table rows as picker options.
- **Q5 compressed into a question + Architecture options table.** The old Q5 row was a 700-word single-cell paragraph describing seven shapes inline — genuinely hard for a user to skim during the interview. Now: a 50-word question (single-pick from the table that follows; disambiguation path named for system-topology / vocabulary-alias answers) plus a small **Architecture options** sub-table with one row per shape (Slot · Shape · Fits when). Same seven canonical options (`4_LAYER_DDD`, `HEXAGONAL`, `MICROSERVICE`, `VERTICAL_SLICE`, `3_TIER`, `SPA`, `FLAT`), same `ARCH` flag values, same disambiguation subsection unchanged. The agent now has a structured source it can render as a picker, a table, or a flow — instead of reflowing a 700-word paragraph.

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
