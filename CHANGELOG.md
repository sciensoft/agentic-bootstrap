<!-- markdownlint-disable MD024 -->
<!-- MD024 disabled: Keep-a-Changelog nests Added/Changed/Removed under every version section — duplicates are the format. -->

# Bootstrap changelog

The bootstrap's own change log. Each entry covers one notable version of [`AGENTIC-BOOTSTRAP.md`](./AGENTIC-BOOTSTRAP.md). On re-run, the Step 8 report names the version delta and surfaces the relevant bullets so the user sees what changed.

Format: Keep a Changelog, dated by ISO date. The version marker at the top of `AGENTIC-BOOTSTRAP.md` (`<!-- bootstrap-version: <YYYY-MM-DD> -->`) is what the bootstrap reads to detect upgrades — bump it whenever you publish a notable change.

## [Unreleased]

## [2026-09-09] — Context-management overhaul (trigger index, enforcement, proactive rules, MCP, migration) + interview + UX polish

### Added

- **Opt-in brief-shape migration for existing projects** (Part 1 Step 0 gains a new bullet). Existing projects bootstrapped before the trigger-index refactor still carry the pre-Cut-1 `AGENTS.md` shape (a `## Rules` bullet list of every rule, treated as always-loaded reference) and a `CLAUDE.md` with `@.agents/rules/*` imports. Sacred re-run policy protects those files, so a normal re-run doesn't move them — the user gets Cut 1's 90% context cut only on newly-bootstrapped projects. This migration path plugs the gap: on re-run, Step 0 content-detects the old shape (not version-based — a bump is optional and users may hand-edit before upgrading) and asks the user *migrate / show diff first / skip*. On *migrate*, Step 4 treats `AGENTS.md` (targeted `## Rules`-section rewrite, all user-authored sections preserved byte-for-byte) and `CLAUDE.md` (whole-file replace with the stub — the old shape carried no project-specific content beyond `@`-imports) as write-through rather than Sacred. Outcome recorded in `.agents/bootstrap.json`'s new top-level `brief_shape_migration` key (`"applied"` / `"declined"` / `"not-needed"`) so future re-runs don't re-ask. Step 8's report gains a matching outcome bullet; the Update-mode quick reference gains a one-narrow-exception caveat on Sacred's contract. Delivered as playbook prose inside `AGENTIC-BOOTSTRAP.md` — no external script (the whole delivery model is one downloadable file).

- **`.mcp.example.json` starter template + MCP measurement guidance in the brief** (MCP-handling cut of the context-management improvement series; §7 of [`AGENTIC-B.Improvements.md`](./AGENTIC-B.Improvements.md)). New Part 4 template at repo root: a pinned Playwright-MCP example wrapped in a template body that documents the safety pattern — pin every version (never `@latest`), approve servers by name via `enabledMcpjsonServers` (never blanket `enableAllProjectMcpServers: true`), deny account-level connectors this project doesn't need via `.claude/settings.local.json`'s `deniedMcpServers` array, and check `/context` after adopting a server (a browser MCP typically costs ~9k tokens, account-level connectors 20k+ each). Emitted as `.example` so file presence doesn't accidentally activate MCP on projects that don't need it — users copy to `.mcp.json` when adopting. `AGENTS.md` template's `Measurement habit` section (and Copilot's inlined copy — which also gained the section itself, missing since Cut 1) enriched with the MCP levers so a reader chasing a slow session knows where to look. Part 3 matrix + Template Index refreshed.
- **Self-application to this repo**: `AGENTS.md` measurement habit note updated; `.mcp.example.json` emitted at repo root to dogfood the pattern.

### Intentionally scoped out

- **No new interview question for MCP.** Most projects don't use MCP, and the current `.claude/settings.json` variants already omit `enableAllProjectMcpServers: true`, which is the load-bearing safe default. A user who wants named allowlist entries adds them post-bootstrap. Adopting an interview Q now would cost interview length for a small opt-in benefit; can be revisited if MCP configuration becomes a common pattern.
- **No changes to `.claude/settings.json` variants beyond the existing safe defaults.** The absence of `enableAllProjectMcpServers: true` is already what §7.3 recommends; adding an empty `enabledMcpjsonServers: []` explicitly is decorative rather than load-bearing.

### Changed

- **Trigger index rules split into two flavors: reactive and proactive-discipline** (Cut 3 of the context-management improvement series). *Reactive* rules (security, changes, UI, layered arch, frontend) fire only when their specific surface is being touched. *Proactive-discipline* rules (testing, metrics, telemetry) apply on every relevant work unit when opted in — the trigger fires on any code change matching the discipline's scope, not just when the discipline's artifact is already being touched. `AGENTS.md`'s `Read before you act` intro gains a paragraph naming the two flavors so future rules land in the right camp.

- **`workflow-metrics.md` trigger reframed proactive-first.** Previously fired only on *"adding, changing or removing a metered event"* — a reactive-only trigger, meaning new features never got instrumented because the trigger required metering to already be there. Now fires on *"a new user-facing flow, business operation, external integration, or a change to an existing metered event"*, so the agent instruments new subsystems as part of building them. The rule body gains a new `## When to add metrics (proactive discipline)` section listing the four proactive triggers (user-facing flow, business operation, external integration, aggregate-worthy failure mode) and naming the deferral path through `.docs/todos/`.

- **`AGENTS.md`'s `Always`-block deferral bullet gains a sub-clause about proactive-rule deferrals.** When the user says *"skip this for now"* on a proactive-discipline rule, the agent captures a todo with a revisit trigger like *"next commit that touches this subsystem"* rather than silently dropping the discipline. Same edit in the Copilot adapter (which inlines the block verbatim since Copilot cannot chase file references).

- **Section 6.3 of `AGENTIC-B.Improvements.md` marked superseded.** The "provisional rules pattern" idea (drop opted-in rules that aren't yet used) was written before Cut 1's trigger-index math settled. Unused rules now cost one index line, not a preloaded body — the false-negative correctness debt of dropping opted-in rules the project will eventually grow into would swamp the false-positive line cost of keeping them. Interview answers capture *intent*, not *usage*.

- **Self-application to this repo**: `AGENTS.md` picks up the deferral extension and the reactive/proactive intro paragraph. Metrics changes not applicable — METRICS is off in this repo.

### Added

- **Agent-agnostic mechanical enforcement for the trigger index** — the design in [`AGENTIC-B.Improvements.md`](./AGENTIC-B.Improvements.md) §9, ported into the generator (Cut 2 of the context-management improvement series). Three enforcement paths, agent-agnostic by default and per-host opt-in:
  - **`scripts/check_consulted_rules.sh` + `.pre-commit-config.yaml` `local` hook** — post-facto enforcement, agent-agnostic. Every commit's staged paths are matched against a case ladder of path → rule mappings (case-ladder arms gated by `IF_UI_COMPONENTS` / `IF_FRONTEND` / `IF_CHANGES` / `IF_METRICS`); the committed prompt file's new `## Consulted rules` section must name every rule a staged path fired, or waive it explicitly with `<rule> (n/a — <reason>)`. Soft-skips when no prompt file is staged or when the section is absent, so existing repos add zero friction.
  - **`.claude/hooks/rule-reminder.sh` + `hooks.PreToolUse` in all four `.claude/settings.json` variants** — pre-facto enforcement, Claude-only (opt-in on `CLAUDE ∈ AGENTS_USED`). Before every Edit / Write, injects a one-line reminder naming the rule to open when the target path fires a trigger. Session-keyed sentinel dir dedupes so a long UI sweep costs one reminder per rule, not one per edit.
  - **`.cursor/rules/trigger-index.mdc`** — pre-facto reinforcement, Cursor-only (opt-in on `CURSOR ∈ AGENTS_USED`). A second Cursor rule beyond `agents.mdc`, `alwaysApply: true`, inlines the path-shaped trigger-index rows so Cursor's rule loader injects them on every message. Path-shaped rows only; attentional rows stay in `AGENTS.md`.
- **`## Consulted rules` section in the prompt-file schema** — new section in `.agents/rules/workflow.md`'s Section 1 file-contents block, sitting between `## Reasoning` and `## Output`. Names the rules a task fired (path-shaped or attentional), one per line. The pre-commit hook cross-checks this section against staged paths; missing entries either name the rule or waive it with `<rule> (n/a — <reason>)`.
- **`## Task boundaries` and the five-item `Always` block** already shipped in Cut 1; Cut 2 is what makes those rules mechanically visible to hosts that support hooks.

### Changed

- **`workflow.md`** template picks up the `## Consulted rules` section in the prompt-file schema. Existing prompt files without the section still commit fine (the hook soft-skips); new tasks starting under the updated schema will populate it.
- **`.claude/settings.json`** — all four posture variants (CAUTIOUS / READONLY / TRUSTED_DEV / BYPASS) now include a `hooks.PreToolUse` block invoking `.claude/hooks/rule-reminder.sh`. Same block in each; the posture setting doesn't gate the reminder, only what needs permission.
- **`.pre-commit-config.yaml`** template gains a `local` hook stanza calling `bash scripts/check_consulted_rules.sh`. Comment above the block explains the mechanism.
- **Part 3 decision matrix** gets rows for the three new templates (`scripts/check_consulted_rules.sh`, `.claude/hooks/rule-reminder.sh`, `.cursor/rules/trigger-index.mdc`); **Template Index** rebuilt to 81 rows after the insertions and shifts.
- **Self-application to this repo.** `.agents/rules/workflow.md` picks up the `## Consulted rules` schema. Other pieces skipped intentionally — this repo has no UI/FRONTEND/METRICS paths (empty case ladder would be dead code), no `.pre-commit-config.yaml` yet (separate concern), no Cursor adapter to reinforce.

- **Rule files under `.agents/rules/` are reference, not preloaded** — the trigger-index split catalogued in the new [`AGENTIC-B.Improvements.md`](./AGENTIC-B.Improvements.md). Every per-agent adapter template (`CLAUDE.md`, `.cursor/rules/agents.mdc`, `.aider.conf.yml`, `.continue/config.json`, `.windsurfrules`) now points at `AGENTS.md` with a "nothing else belongs here" closing paragraph and no `@`-import list for the rule files. `.github/copilot-instructions.md` is the exception — since Copilot cannot chase file references, it inlines the `Always` block + trigger index verbatim from `AGENTS.md`. Fixed always-loaded context in a typical generated project drops from ~47k tokens (measured before, per the doc's §1) to ~4.5k (measured after) — the user's request becomes the loudest thing in the window rather than the twelfth. Every rule file stays where it is; the change is reversible by restoring the imports.

- **`AGENTS.md` template gains an `Always` block + `Read before you act` trigger index**, replacing the previous `## Rules` bullet list that read as though every rule applied every turn. `Always` carries the five things that DO apply every turn (confirm the reading before building; answer the request that was made; declare the task boundary; one prompt file per task; capture deferrals). The trigger index names each reference file's *condition* and asks the agent to open the file *when* the condition fires — not before. Index rows are conditional on the same `{{IF_*}}` flags that gate rule emission. A short `Measurement habit` note points readers at `/context` and names the three large line items outside the generator's control (conversation length, MCP tool schemas, per-host system prompt).

- **`workflow.md` template rewritten from per-request to per-task.** New `## Task boundaries` section defines a task as one coherent piece of user intent, and puts the boundary decision on the agent (declared, not inferred): a commit closes the current task by default; explicit user signals (*"now let's..."*, *"moving on..."*, *"unrelated:"*) force a new one; when the signal is ambiguous, **continue** — the cost of a mis-continuation is a longer prompt file, the cost of a mis-new-task is directory spam. Prompt files are amended across turns of the same task via a `## Refinements` sub-section rather than a new file per turn. `## 1. Create a prompt file` renamed to `## 1. Create (or amend) a prompt file`; `## 4. Commit the result` opens with commit-granularity-is-a-judgement-call. Fixes the observed failure of directories spraying with fifteen prompt files for one piece of work across fifteen refinement turns.

- **Template Index refreshed** (78 rows) after the line-range shifts from the three template rewrites above.

- **Self-application to this repo.** `CLAUDE.md`, `AGENTS.md`, and `.agents/rules/workflow.md` in this repo updated to match the new shape — the bootstrap is self-applied and shipping a generator change while leaving the reference implementation on the old shape would be preaching without practicing. Sacred re-run policy on `AGENTS.md` / `CLAUDE.md` is preserved for user-generated projects; a Sacred-file migration helper for existing projects is a follow-up, not part of this PR.

### Added

- **`AGENTIC-B.Improvements.md`** — the design record for the context-management improvement series (Cut 1 here; Cut 2 + Cut 3 in follow-up PRs). Sections 1–5 are the assessment (including the calibration-trap warning that had the first pass off by 28%); section 6 is what Cut 1 implements; section 7 (the MCP payload the generator does not control) and section 9 (mechanical enforcement via `make rules-check`, `pre-commit`, per-host hooks) belong to Cuts 2 and 2b.

### Changed

- **Step 2's rich-picker directive strengthened from *"use it"* to *"you MUST use it"*.** In practice, some UI-capable hosts (Claude Code VSCode extension, Continue.dev, IDE extensions with prompt primitives) still fall back to plain-text prompting on the first read of the bootstrap — the softer *"use it"* wording wasn't landing consistently. Line 160 in [`AGENTIC-BOOTSTRAP.md`](./AGENTIC-BOOTSTRAP.md) now names the failure mode explicitly (*"falling back to plain text when picker UI is available is a UX regression, not a valid default"*), acknowledges the common first-turn miss, and pre-registers the user-facing nudge — *"use your interactive prompts (pickers, multi-select) — one call per question"* — as the signal to switch mid-interview. The landing page and QUICKSTART also gain a companion nudge card the user can paste when the picker UI doesn't show up on first try. Continue.dev added to the picker-primitive example list (previously only Claude Code and Cursor were named).

### Added

- **Interview checkpoint via `interview_status` field on `.agents/bootstrap.json`.** Session-interruption recovery — real incident that triggered this: a user was near the end of Q17, opened another project window in VSCode which took over the session, and lost every answer because the interview only persisted at the end. New protocol writes `.agents/bootstrap.json` after **every** answered question in Step 2 with `interview_status: "in_progress"` and the accumulated answers dict; on the final answer, flips to `interview_status: "done"`. Step 0's re-run detection now branches on the field: **`"in_progress"`** offers *"Resume from Q{N+1}, or start fresh?"* — resume picks up mid-interview with captured answers preserved, start fresh wipes and re-runs from Q1; **`"done"`** (or field missing on legacy bootstrap.json files) is normal re-run mode. User-requested answer changes (*"re-ask Q12"*) temporarily flip to `"in_progress"` for the duration of the change. Single file, single field — no separate WIP file. Bootstrap.json template updated with the new field + field-note explaining semantics + legacy-file handling (missing = treat as `"done"`). Template Index offsets refreshed accordingly.

- **Context-window advisory in two visitor-facing surfaces (landing page + README).** A new info-callout below the existing model-capability advisory in the landing page's *Three steps* section, plus a *Before you run* blockquote under the Quick start in [`README.md`](./README.md). Surfaces three failure modes the bootstrap hits in practice: (1) model architecturally capped below 128k (most Qwen 2.5 builds, Codestral, Phi-4), (2) runtime serving a smaller context than the model supports (Ollama, vLLM, llama.cpp all have separate caps), (3) agent re-sending the file every turn vs chunked tool reads. Closes with the same "use a hosted API for this one-time scaffold" escape hatch. Triggered by a real debug session — 2× RTX 3090 (48 GB VRAM), Qwen 2.5 Coder 32B with Modelfile `num_ctx 131072`, still served at 32k because the GGUF metadata caps at 32k regardless. Aider sent 81k, Ollama silently truncated the file out, the model accurately reported *"please provide the contents."* The README's *Before you run* block bundles both this context note and the model-capability note (which the README didn't previously carry) under one heading so first-time visitors see both constraints together. No bootstrap-internal warning ships — by design: a model that hits the warning has already passed the test; a model that fails never reads the warning at all.

- **Bootstrap-hardening prose against step-skipping agents.** Five focused additions to make a weaker / less-careful model's failure mode more visible and harder to fall into, triggered by a real Aider + `deepseek-r1:14b` debug session where the agent skipped Steps 0–3 and wrote files containing literal `{{PROJECT_NAME}}` etc. unsubstituted:
  - **`STOP` callout** above Part 1 — high-visibility block reading *"this is a multi-step playbook, not a list of files to create"* with the ordered step list inline. Sits between the *Before you start* sub-section and the Part 1 heading.
  - **`Before you start` sub-section** under *How to use* — names the failure modes explicitly (literal `{{PLACEHOLDER}}` tokens in output, Step 2 skipped, all 17 questions dumped at once) so the agent has the pattern to refuse if it's tempted.
  - **Model-capability note** inside *Before you start* — names the model classes that handle the playbook reliably (Claude Sonnet / Opus, GPT-4 class, Gemini 1.5 / 2.x, full DeepSeek-V3, Qwen 2.5 Coder 32B+) and the failure mode of smaller distilled reasoning models. Same copy as the landing-page advisory shipped in `feat/landing-bootstrap-tips`.
  - **Step 0 imperative opener** — *"Your first action: read this entire file. Do not write anything yet."* leads the section instead of being buried mid-paragraph.
  - **Step 4 gate check** — before the existing performance tip, an explicit *"do not start Step 4 unless Steps 0–3 are complete"* with the `{{PLACEHOLDER}} + {{IF_FLAG}}` reasoning attached. Makes the dependency between Step 2 and Step 4 visible at the entry point an offset-read-capable agent might hit directly.

### Changed

- **Q2 rebalanced from Claude-centric preset bundles toward true multi-pick of individual tools.** Real bootstrap-run screenshot: Claude Code's picker rendered Q2 as four preset bundles (*"Claude Code only"*, *"Claude Code + Cursor"*, *"Claude Code + GitHub Copilot"*, *"All eight tools"*, *"Other"*) — three of the four presets centered Claude, and *"All eight tools"* is an edge case not a sensible default. The Q2 row in [`AGENTIC-BOOTSTRAP.md`](./AGENTIC-BOOTSTRAP.md) now explicitly forbids preset-bundle picker rendering (naming the specific bad shapes so the agent has the pattern to refuse), tells the agent this is a multi-select of individual tools where the user picks any subset from 1 to all 8, names the four most-adopted tools (**Claude Code · Cursor · GitHub Copilot · Windsurf**) as primary picker options, and puts the remaining four (**Aider · Codex CLI · OpenCode · Continue.dev**) under an *Other* / *More* group. The *Supported tools — for Q2* sub-table splits accordingly, with a preamble explaining the grouping. Ordering is alphabetical within the top four; the earlier concern was three-of-four presets centering Claude Code, not Claude Code appearing at all in the primary group. Template Index offsets refreshed by +7 lines to absorb the additions.

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
