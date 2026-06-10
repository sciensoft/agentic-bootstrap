# Contributing to Agentic Bootstrap

Thanks for considering a contribution. This file covers how to evolve the bootstrap itself — adding new ARCH templates, tool adapters, feature gates, language scaffolds, and rule files. The bootstrap is a single self-contained markdown file plus a thin set of helper docs, so contributions are usually small, surgical, and easy to review.

If you're a user of the bootstrap (i.e. you ran it on your own project), the [project-internal `CONTRIBUTING.md`](./AGENTIC_BOOTSTRAP.md) that the bootstrap *writes* to your repo covers your project's contribution rules. This file covers contributions to **this** repo — the bootstrap source.

## How the bootstrap works (briefly)

[`AGENTIC_BOOTSTRAP.md`](./AGENTIC_BOOTSTRAP.md) is structured as six parts:

1. **Operator playbook** — Steps 0–8 the agent follows when running the bootstrap.
2. **Interview** — the 16 questions.
3. **Decision matrix** — which files get written under which conditions, with re-run policies.
4. **File templates** — the literal content of every file the bootstrap writes.
5. **Post-bootstrap checklist** — what the user should do after the first commit.
6. **How to extend** — recipes for the common contribution patterns (this file links into Part 6).

When you contribute, you're almost always editing one of: Part 2 (a new interview question), Part 3 (a new matrix row), Part 4 (a new template), or [`docs/index.html`](./docs/index.html) (the landing page).

## Before you start

- **Read [`AGENTIC_BOOTSTRAP.md` Part 6 — How to extend this bootstrap](./AGENTIC_BOOTSTRAP.md)** before writing the change. Part 6 has battle-tested recipes for the common contribution patterns; following the recipe keeps your PR small and the review fast.
- **Open an issue or discussion first** for anything substantial — a new ARCH slot, a new tool adapter, a new feature gate that asks a new question. Lightweight changes (typo, clarification, a new diagram example) can go straight to a PR.
- **Bump [`BOOTSTRAP_CHANGELOG.md`](./BOOTSTRAP_CHANGELOG.md)** in the same PR. Add a bullet to `[Unreleased]` describing what changed. The version marker at the top of `AGENTIC_BOOTSTRAP.md` (`<!-- bootstrap-version: <YYYY-MM-DD> -->`) gets bumped when the maintainer cuts a release; you don't need to bump it in your PR.

## Common contribution patterns

### Adding a new architecture variant (`ARCH` slot)

The bootstrap currently supports 9 architecture slots. To add a tenth:

1. **Part 2 / Q5** — extend the question prose to mention the new option and add the value to the `ARCH` enum.
2. **Part 1 multi-value dispatch** — extend the `ARCH` dispatch description to name the new variant.
3. **Part 3 decision matrix** — update the `layered-architecture.md` row to list the new variant.
4. **Part 2 Q5 disambiguation table** — add a row if the new variant has vocabulary aliases or topology-shaped answers that should route to it.
5. **Part 4** — write the new `### Template: `.agents/rules/layered-architecture.md` — variant for `ARCH=<NEW>`` section. Mirror the structure of an existing variant (project tree, layer responsibilities, dependency direction, "when to pick this over X" callout if it sits close to another slot).
6. **Landing page** — add a card to the Architectures section.
7. **Examples** (optional but recommended) — add a minimal example under `examples/` showing what the new architecture produces.

Keep the template focused on the *folder shape* and the *dependency rule*. Conventions that apply across architectures (DI patterns, repository discipline) belong in `best-practices.md`, not the per-architecture template.

### Adding a new tool adapter (`AGENTS_USED` value)

The bootstrap currently supports 8 agentic tools. To add a ninth:

1. **Part 2 / Q2** — extend the `AGENTS_USED` enum and the per-tool explanation in the question prose.
2. **Part 1 multi-value dispatch** — extend the `AGENTS_USED` dispatch list with the new tool's adapter file path.
3. **Part 3 decision matrix** — add a conditional row for the new adapter file with the `<TOOL> ∈ AGENTS_USED` trigger.
4. **Part 4** — write the adapter template. Decide whether the tool *follows file references* (then the adapter is a thin pointer to `AGENTS.md` and `.agents/rules/*`, like Cursor / Claude / Aider) or *inlines its rules* (then the adapter summarises the workflow + best-practices + security headlines directly, like Copilot). Mirror the closest existing adapter.
5. **Step 6 staging line** — add the adapter path to the `git add` list in Step 6 of Part 1.
6. **Landing page Hero "Works with" strip** — add the tool name.
7. **`best-practices.md` stub variant § Enable refinement matrix** — add a row showing how to enable web search on this tool.

If the new tool reads `AGENTS.md` natively (like Codex CLI and OpenCode), no adapter file is needed — just mark it in the multi-value dispatch as "reads `AGENTS.md` natively — no extra file."

### Adding a new feature gate (a new yes/no question)

Used for opt-in workflow rules (currently: `CHANGES`, `UI_COMPONENTS`, `METRICS`, `TESTING`). To add a new one:

1. **Part 2** — add the question to the **Feature gates** tier; pick the next available Q-number. If the new question slots between existing ones, follow the renumbering procedure (`sed` high-to-low; see how `TESTING` was inserted in `BOOTSTRAP_CHANGELOG.md`'s 2026-06-10 entry for the worked example).
2. **Part 3 decision matrix** — add an opt-in row for the new rule file, gated on the new flag.
3. **Part 4** — write the new `### Template: `.agents/rules/<your-rule>.md` *(opt-in, write only if `<FLAG>`)*` section.
4. **`AGENTS.md` template** — add a `{{IF_<FLAG>}}- [...](your-rule.md) — <one-line>` line to the Rules list.
5. **Every per-tool adapter template** — add the matching `{{IF_<FLAG>}}` line so adapters stay in sync.
6. **`workflow.md` template § Commit checklist** — add a `{{IF_<FLAG>}}` line if your rule changes what goes in the commit.
7. **`bootstrap.json` template** — add the new key to the `answers` object so existing projects re-ask it on next re-run.
8. **Landing page Features grid** — consider whether the new gate warrants a feature card or fits inside an existing one (the grid is currently 6 cards — keep it tight).

### Adding a new language scaffold (`LANG` value)

Used when the bootstrap should ship language-specific `.gitignore`, manifest, test scaffold, linter configs, and `Makefile` for a new language. To add a new one (e.g. Elixir, Zig, Kotlin):

1. **Part 2 / Q4** — extend the question prose to include the new language as an explicit pick.
2. **Part 1 multi-value dispatch** — note the new value in the `LANG` description.
3. **Part 4** — write all five template variants under their existing template headers: `.gitignore`, manifest + test scaffold, linter / formatter config, `Makefile`. Mirror the structure of the closest existing language.
4. **Part 4 / `.claude/settings.json` — variant for `POSTURE=TRUSTED_DEV`** — add a language-specific allow addendum so the `TRUSTED_DEV` posture pre-allows the new language's safe build/test commands.

The five template families (`.gitignore`, manifest, linter, `Makefile`, `TRUSTED_DEV` addendum) ship together — they're dispatched as a set by Q4 `LANG`. If you can only contribute three of the five, that's still useful; mark the missing two clearly in your PR and a maintainer will fill them in.

## Style

- **Prose**: opinionated, concrete, honest about trade-offs. Avoid hedging weasel words ("might want to consider", "if you feel like it"). The bootstrap exists because indecision costs time.
- **Markdown**: standard CommonMark. Tables for picker / dispatch tables. Fenced code blocks (with language tag) for everything else. Mermaid for diagrams.
- **No emojis**: the bootstrap content stays emoji-free unless an existing pattern uses them.
- **Cite when relevant**: if a recommendation is grounded in an external source (OWASP guidance, a language style guide, a framework's own docs), cite it inline.

## Testing your change

Before opening the PR, run a smoke check:

1. **Manual bootstrap.** Spin up a fresh empty directory; ask an agent (Claude Code is easiest if you have it) to follow the modified `AGENTIC_BOOTSTRAP.md` against it; confirm the bootstrap produces the expected files for a stack that exercises your change. For an ARCH-template contribution: pick that ARCH, confirm the template renders correctly; for a feature-gate contribution: answer yes to the new question, confirm the rule file lands.
2. **Re-run check.** Run the bootstrap a second time against the same directory; confirm re-run mode picks up the already-bootstrapped project and only asks for any newly-added interview keys.
3. **Doctor check** (when bootstrap-doctor mode ships): invoke `doctor` mode, confirm the report surfaces nothing unexpected.
4. **Lint**: the bootstrap file is one large markdown document. Run your editor's markdown linter or `markdownlint AGENTIC_BOOTSTRAP.md` and fix anything it flags that isn't a known false positive (the file's header disables MD010 for the Makefile tab requirement; everything else should be clean).

## PR conventions

- **Branch from `main`**. Open the PR against `main`.
- **One PR per change**. Don't bundle a new ARCH slot with a new tool adapter — review them separately.
- **Reference the issue or discussion** if there was one.
- **Update [`BOOTSTRAP_CHANGELOG.md`'s `[Unreleased]` section](./BOOTSTRAP_CHANGELOG.md)** in the same PR.
- **Tag a maintainer** for review if you don't get one within ~5 business days.

## Code of conduct

Be kind. Disagree about substance, not people. The bootstrap is an opinionated project; lots of legitimate decisions could have gone the other way. Maintainers will explain why a decision was made when it's not obvious from the file; contributors don't have to agree, but the project's opinions stand unless argued away with concrete reasons.

## Maintainership

The bootstrap is currently single-maintainer. If that bothers you (it should — bus factor is a real concern), help reduce it: triage issues, review PRs, write the architecture template you wished existed. Earned co-maintainer status follows sustained contribution.
