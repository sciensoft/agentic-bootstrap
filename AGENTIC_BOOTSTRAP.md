<!-- markdownlint-disable MD010 -->
<!-- MD010 disabled: Makefile fenced blocks legitimately require hard tabs (POSIX make spec). -->

# Agentic Bootstrap

> One file. Project-agnostic. Tool-agnostic. Hand it to any agentic coding assistant in a fresh (or existing) repo and say *"follow this bootstrap"*; the agent interviews you and lays down a cross-tool workflow scaffold — `AGENTS.md` (the primary brief), `.agents/rules/` (workflow + best-practices + architecture), `.docs/prompts/`, `.docs/adrs/`, `.docs/todos/` — plus a thin adapter file for each agentic tool the project supports (Claude Code, Cursor, Aider, Codex CLI, OpenCode, Continue.dev, Windsurf, GitHub Copilot), plus the first commit that records the bootstrap itself.
>
> The discipline encoded here: every artifact-producing request gets a timestamped prompt file under `.docs/prompts/`, an ADR under `.docs/adrs/` when architecturally significant, deferred ideas as one-file-per-entry under `.docs/todos/`, telemetry kept current, security-sensitive changes run through the rubric in `.docs/security/methodology.md` before commit (dated audits as sibling files on a cadence), and a single commit + push wrapping all of the above.
>
> The file is self-contained. The agent does not need to fetch anything. To evolve the bootstrap, edit this file in place — your next bootstrap reflects the change.

---

## How to use

1. `cd` into your target project (a clean `mkdir foo && cd foo`, or an existing repo).
2. Open an agent session there (Claude Code, Cursor, Codex CLI, Aider — anything that can read this file and run shell commands + edit files).
3. Paste this file's contents into the session, then write: **"Follow this bootstrap."**

The agent will interview you, write the scaffold, create the first commit, and (if a remote exists) push.

---

## Part 1 — Operator playbook

**You are the agent.** Read this entire file once, top to bottom, before acting. Then execute the steps below in order. Do not skip steps. If a step needs clarification, ask the user — do not guess silently.

### Step 0. Detect run mode

The bootstrap is **idempotent**: it's safe to re-run on a project that's already been bootstrapped (e.g. to pick up new rules / templates from a newer version of this file). Decide the mode first.

- Check for the sentinel: `.agents/rules/workflow.md`. If it exists, the bootstrap has already run here → **re-run mode** (also called *update mode*).
- Also check for `.agents/bootstrap.json` — if it exists, read it; the file holds the answers captured during the previous bootstrap (see Part 4 template). On re-run, reuse those answers and skip those questions; only ask for any keys *missing* from the file (new interview questions added in newer bootstrap versions).
- **Legacy-layout migration**: if `.agents/rules/workflow.md` does *not* exist but `.claude/rules/workflow.md` does, this is a project bootstrapped under the **pre-multi-tool layout** (rules under `.claude/rules/`, answer cache at `.claude/bootstrap.json`). Treat it as re-run mode and **ask the user**: *"This project uses the legacy `.claude/rules/` layout. Migrate to `.agents/rules/` so other agentic assistants can be added (recommended)? Or leave the files in place?"* If they pick **migrate**, `git mv .claude/rules .agents/rules` and `git mv .claude/bootstrap.json .agents/bootstrap.json` before proceeding; update any `@.claude/rules/…` references in `CLAUDE.md` to `@.agents/rules/…` in the same step. If they pick **leave**, keep treating the legacy paths as the live ones for this re-run (skip the rename, keep writing to `.claude/rules/` and `.claude/bootstrap.json`); flag in the Step 8 report that adapter generation for non-Claude tools will be limited until they migrate. Either way, write the chosen layout into `bootstrap.json` so future re-runs don't re-ask.
- If no sentinel exists at either path → **first-time mode**. Standard flow (Steps 1–8 as written).

Both modes share the same playbook from this point on, with these behavioural differences:

| | First-time mode | Re-run / update mode |
| --- | --- | --- |
| Step 1 collision check | Stop on any of `AGENTS.md`, `CLAUDE.md`, `.agents/rules/`, `.claude/rules/` (legacy), `.docs/adrs/`, `.docs/todos/` | Expected to exist; no abort |
| Step 2 interview | Ask all 16 questions | Ask only questions whose flag is **missing** from `.agents/bootstrap.json` |
| Step 4 file writes | Write every applicable file from scratch | Apply the per-file **re-run policy** (Canon / Mixed / Sacred — see Part 3 matrix) |
| Step 6 commit message | `Bootstrap project with agentic workflow conventions` | `Re-bootstrap: <one-line summary of what changed>` (e.g. *"refresh rules to `<date>` bootstrap version"*) |

If the user explicitly wants a clean wipe-and-recreate, they can tell you to *"treat this as first-time mode"*; in that case, ask them to confirm the destructive intent, then back up the existing `.agents/`, `.claude/`, `.docs/`, and root config files (rename to `.agents.backup-<ts>/` etc.) before running first-time mode.

### Step 1. Sanity-check the working directory

- Run `pwd` to confirm where you are; run `ls -la` to see what's already here.
- **First-time mode**: if **any** of these already exist — `AGENTS.md`, `CLAUDE.md`, `.agents/rules/`, `.claude/rules/` (legacy), `.docs/adrs/`, `.docs/todos/`, `AGENTIC_BOOTSTRAP.md` itself — **stop and ask the user** how to proceed (overwrite? merge? skip the conflicting files? switch to re-run mode?). Never silently overwrite their work.
- **Re-run mode**: these files are expected to exist; no abort. Still sanity-check for unexpected state — if `.agents/rules/` (or the legacy `.agents/rules/` if migration was deferred) is missing files the matrix knows about, or `.docs/security/methodology.md` was deleted, or anything else seems wrong, surface it before proceeding.
- If `.git/` doesn't exist, ask whether to `git init` as part of the bootstrap (default: yes). Re-run mode in a non-git directory is unusual; mention it.

### Step 2. Run the interview (Part 2)

Ask the interview questions. Capture answers. If your host supports a structured interactive question tool (e.g. `AskUserQuestion` in Claude Code), use it; otherwise ask one question at a time in chat. Record the answers compactly — you'll reference them when filling templates.

**Re-run mode**: load `.agents/bootstrap.json` (read in Step 0). Treat its keys as already-answered. Ask the user **only** for keys whose flag is missing from the file — these are new interview questions added in newer bootstrap versions, or fields the previous bootstrap didn't capture. When done, write the updated `.agents/bootstrap.json` with the merged set (old + new keys) in Step 4's bootstrap.json template.

If the user wants to change a previously-captured answer (e.g. switch `POSTURE` from `CAUTIOUS` to `TRUSTED_DEV`), they can tell you explicitly — *"re-ask about posture"*; in that case, ask the relevant question even though the key is present, and update `.agents/bootstrap.json` with the new value. Make sure the user understands which files will be re-written under the new answer (the re-run policy still applies — Sacred files stay sacred even on a changed answer).

### Step 3. Decide which files to write (Part 3 decision matrix)

Always-included files are written every time. Opt-in files are written only when the matching interview answer is *yes*.

### Step 4. Write the files (Part 4 templates)

For each file you decided to write in Step 3:

- Create parent directories as needed (`mkdir -p`).
- Write the file's contents from the template verbatim, with these substitutions:
  - `{{PLACEHOLDER}}` tokens → the user's interview answer.
  - `{{IF_FLAG}}<line content>` → keep the line (after stripping the `{{IF_FLAG}}` prefix) when `FLAG` is true; remove the line entirely when false.
- **Derived flags** (computed from interview answers, not asked directly):
  - `LAYERED` = `(ARCH != FLAT)`. True when Q5 picked any non-Flat shape; controls the architecture-rule ref lines in `AGENTS.md`, the `CLAUDE.md` adapter (if Claude in `AGENTS_USED`), each other per-tool adapter, and `best-practices.md`.
- **Multi-value flag dispatch**: pick the template variant whose label matches the user's interview answer.
  - **`AGENTS_USED`** (Q2): a set of one or more values from `{CLAUDE, CURSOR, AIDER, CODEX, OPENCODE, CONTINUE, WINDSURF, COPILOT}`. Drives the per-tool adapter files — each adapter is written **only if** its tool is in the set. Always-written tool-agnostic files (`AGENTS.md`, `.agents/rules/*`, `.agents/bootstrap.json`) are independent of this flag. Adapter mapping:
    - `CLAUDE` → `CLAUDE.md` (thin adapter pointing at `AGENTS.md`) + `.claude/settings.json` (gated additionally by Q3 `POSTURE ≠ N_A`).
    - `CURSOR` → `.cursor/rules/agents.mdc`.
    - `AIDER` → `.aider.conf.yml`.
    - `CODEX` and `OPENCODE` → no adapter; both read `AGENTS.md` natively.
    - `CONTINUE` → `.continue/config.json`.
    - `WINDSURF` → `.windsurfrules`.
    - `COPILOT` → `.github/copilot-instructions.md`.
  - **`POSTURE`** (Q3): variants `CAUTIOUS`, `READONLY`, `TRUSTED_DEV`, `BYPASS` each have their own `.claude/settings.json` template. **Only asked / applied if `CLAUDE ∈ AGENTS_USED`**; otherwise set `POSTURE=N_A` and skip both the question and the settings file. `TRUSTED_DEV` is composed: write the base template, then append the language-specific allow entries from the table that follows the base, picking by Q4 `LANG`. For `LANG=Other / mixed` under `TRUSTED_DEV`, skip the language addendum and tell the user post-bootstrap to extend their `allow` list with their toolchain's commands. **Write `.claude/settings.json` first** (after creating directories, before any other file) so the chosen posture takes effect for the rest of the bootstrap's file writes.
  - **`LANG`** (Q4): controls four template families — the `.gitignore` variant, the manifest + test-scaffold variant, the linter / formatter config variant, and the `Makefile` variant. Each family has Python / TypeScript-Node / Go / Rust / Fallback variants. Pick the variant matching the user's primary language across all four; they ship together. If mixed (e.g. fullstack monorepo), pick the dominant backend language and tell the user the frontend equivalents need adding separately.
  - **`ARCH`** (Q5): variants `4_LAYER_DDD`, `3_TIER`, `SPA`, `MONOREPO`, `SERVERLESS` each have their own `layered-architecture.md` template. `MONOREPO` documents the top-level workspace layout (sub-projects pick their own internal architecture on add); `SERVERLESS` documents a handlers-first layout for FaaS codebases. If `ARCH=OTHER`, ask the user for a one-paragraph description and write a minimal stub capturing it. If `ARCH=FLAT`, don't write the file. If Q5 elicited a system-topology answer, run the disambiguation in Part 2 before settling on `ARCH`.
  - **`LICENSE`** (Q13): variants `MIT`, `APACHE_2_0`, `PROPRIETARY` each have their own `LICENSE` template. If `LICENSE=SKIP`, don't write the file. All non-SKIP variants need `{{COPYRIGHT_HOLDER}}` (captured during Q13's follow-up prompt) and `{{CURRENT_YEAR}}` (from `date +%Y`). If you reach the LICENSE write step without `COPYRIGHT_HOLDER`, ask the user before writing — don't substitute a placeholder.
- **Conditional file writes**: `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` are written only if Q14 `CONTRIB=yes`. `LICENSE` is written only if Q13 `LICENSE != SKIP`. `.env.example` is written only if Q8 `ENV_VARS=yes` (skipped for purely static frontends, libraries, and other projects with no runtime config).
- **Re-run policy** (re-run mode only): every file in the Part 3 decision matrix has a **Re-run** category — `Canon`, `Mixed`, or `Sacred`. For each file you would write in first-time mode, on re-run apply the category's behaviour:
  - **`Canon`** — versioned discipline; the bootstrap is the source of truth. Diff the would-write content against what's on disk. If different, **overwrite silently** (announce the change in the Step 8 report). If identical, no-op.
  - **`Mixed`** — user is expected to layer project-specific additions on top of the bootstrap baseline. Diff the would-write content against what's on disk. If different, **show the user a unified diff and ask**: *overwrite* (use the new bootstrap version, discarding their additions), *keep* (preserve the user's version unchanged), or *merge* (the agent attempts to add new entries from the bootstrap baseline without removing user additions — only viable for additive-only changes like new gitignore lines or new allow-list entries; ask the user to review the merged file before continuing). If identical, no-op.
  - **`Sacred`** — user-owned; the bootstrap never touches it on re-run. Skip silently. If the file is missing entirely (the user deleted it), ask the user whether to re-scaffold from the bootstrap template before proceeding — don't recreate without consent.

  After applying the policy file-by-file, summarise the touched / skipped / asked counts in the Step 8 report.

### Step 4b. Refine `best-practices.md` from current web sources (capability-gated, failure-safe)

`best-practices.md` is the one rule file whose value depends sharply on the *current* state of the user's chosen language + framework ecosystem. A generic stub is fine; a stack-specific synthesis of current idioms is far better. This step tries to produce the better version *when the running agent host has web search / web fetch*, and falls back to the generic stub otherwise.

**The hard rule for this step:** `best-practices.md` MUST end the bootstrap as a written, committed file. Web search failures, capability gaps, timeout errors, parse problems — none of them block the bootstrap. The stub is the safety net.

Decide which path to take by **probing your own capability**, not by asking the user:

1. **Capability probe.** Attempt a small, low-cost web action — a single `WebSearch` query for `"<LANG> best practices <CURRENT_YEAR>"`, or a `WebFetch` of a known stable URL (e.g. the chosen language's official docs root). If the call returns content within ~10 seconds, treat web access as **available**. If the call errors, prompts for permission you can't satisfy, times out, or returns empty, treat web access as **unavailable**.
2. **Self-configure if the gap is just permissions, not capability.** If the probe failed because your host's permission model gated the call (Claude Code with a missing `WebFetch` / `WebSearch` allow-entry; an MCP web-tool the user hasn't enabled), and you have write access to the host's settings file (e.g. `.claude/settings.json` you're about to write anyway), add the minimum entry needed to unblock the search, then re-probe once. **Do not** invent capabilities your host doesn't ship — adding a permission only works if the underlying tool exists.

Then act:

- **If web access is available**, run a small fan-out of targeted queries in parallel with the rest of Step 4's file writes — don't block other writes on this. Search for:
  - `"<LANG> best practices <CURRENT_YEAR>"` (general)
  - `"<LANG> <primary framework from Q14/Q15> idioms"` (framework-specific — extract framework names from the user's run instructions, dependencies, or free-form notes)
  - `"<LANG> testing patterns"` (if `TESTING=yes`, to feed the file's testing-discipline cross-refs)
  - `"<LANG> <ARCH lowercase, e.g. ddd / 3-tier / spa>"` (architecture-specific)
  - One or two follow-up fetches against authoritative sources surfaced by the searches (official framework docs, well-regarded style guides — prefer first-party sources over blog posts).

  Then synthesise the results into `best-practices.md` following the structural skeleton in the **refined-variant** template (Part 4). Each significant claim cites its source inline (URL + accessed date). Drop the top-of-file marker `<!-- best-practices: refined · sources: [...] · accessed: <YYYY-MM-DD> -->` so re-runs can detect refinement status without re-running web searches.

- **If web access is unavailable** (probe failed and self-configure didn't unstick it, or fan-out searches errored, or synthesis produced an empty / malformed result), write the **stub-variant** template (Part 4) verbatim. The stub carries the top-of-file marker `<!-- best-practices: stub · refinement deferred · reason: <one-line> -->` and a prominent **"How to enable refinement"** section that names the host-specific knobs (see the stub template for the per-agent matrix). Set `BEST_PRACTICES_REFINED=false` in `bootstrap.json`.

**Re-run behaviour.** On re-run, read the marker line at the top of the existing `best-practices.md`:

- Marker says `refined` → leave the file untouched (it's user-owned now even though it sits in the Canon category). Note in the Step 8 report.
- Marker says `stub` → attempt the refinement again from scratch (capability may have changed since the last run — a permission was added, an MCP server got enabled, the user switched hosts). If still unavailable, overwrite with a fresh stub carrying an updated reason line.
- Marker is missing entirely (pre-refinement bootstrap) → treat as stub and attempt refinement.

**Failure handling.** Any error during refinement — HTTP failure on every search, model confusion synthesising, JSON parse error, anything — falls back silently to the stub. Log the failure cause in the stub's marker reason line so the user can see why refinement didn't happen. The bootstrap continues. Never block on this step.

### Step 5. Write the bootstrap prompt file and persist the answers

Two writes here, in order:

1. **Prompt file**. Per the `workflow.md` rule you just installed, every artifact-producing request gets a prompt file. The bootstrap is an artifact-producing request. Create:

   ```text
   .docs/prompts/<unix-timestamp>.bootstrap_project.md
   ```

   Use `date +%s` for the timestamp. Use the standard prompt-file shape (described in `workflow.md`): three sections — `# Request`, `## Reasoning`, `## Output`. Be specific about what was written and which interview answers shaped the output. On re-run, the prompt file documents what *changed* in this re-bootstrap (which Canon files were refreshed, which Mixed files were merged/kept/overwritten, which new flags landed).

2. **Persisted answers**. Write `.agents/bootstrap.json` with the captured interview answers (see Part 4 template). On first-time mode this is the initial write; on re-run mode it merges new answers with existing ones. This file is committed (project-shared) so future re-runs and other agent sessions can reuse it.

### Step 6. First commit

- Stage explicitly: `git add AGENTS.md .agents/ .docs/` plus any per-tool adapters written based on `AGENTS_USED` — `CLAUDE.md` and `.claude/` (if `CLAUDE`), `.cursor/` (if `CURSOR`), `.aider.conf.yml` (if `AIDER`), `.continue/` (if `CONTINUE`), `.windsurfrules` (if `WINDSURF`), `.github/copilot-instructions.md` (if `COPILOT`), and any root-level config files written this run (`.gitignore`, `.editorconfig`, `Makefile`, manifest, linter configs, etc.). Never `git add -A` or `git add .`.
- Commit message:

  ```text
  Bootstrap project with agentic workflow conventions
  ```

- Include a co-author trailer for your agent host (e.g. `Co-Authored-By: Claude <noreply@anthropic.com>`). The discipline is to *include one*; the exact string depends on which agent is running this.

### Step 7. Push (if a remote exists)

- Run `git remote -v`. If a remote is configured: `git push -u origin <branch>`.
- If no remote: tell the user the commit is local and that they can push once they add one (no need to error out).

### Step 8. Report back

In one short paragraph:

- **First-time mode**: what was written (paths), which opt-in rules landed (and which were skipped, by interview answer), which per-tool adapters were written (from `AGENTS_USED`), the natural next step — usually: open `AGENTS.md` and expand the *Purpose* / *Architecture map* sections; if the project starts with a load-bearing decision, write the first real ADR (`.docs/adrs/0001-<slug>.md`).
- **Re-run mode**: which Canon files were refreshed, which Mixed files were merged / kept / overwritten / skipped (with per-file user decisions), which Sacred files were preserved untouched, which new interview keys landed in `.agents/bootstrap.json`. Also flag any Sacred files that were missing on disk (the user may want to re-scaffold from the template manually).
- **Best-practices refinement status** (always — call this out explicitly so the user notices). Two outcomes:
  - *Refined*: name the sources cited (one-line summary), the accessed date, and that the file is now user-owned (re-runs won't touch it).
  - *Stubbed*: name the one-line failure reason (probe error / permission gated / no capability), point at `§ Enable refinement` in `best-practices.md` for the per-agent remediation matrix, and offer: *"Want me to try self-configuring your host's web access now?"* if the host gap appears to be permissions (not capability).

### Update-mode quick reference

What to remember about idempotent re-runs in practice:

1. **Re-runs are safe to ask for.** Tell the user *"feel free to re-run this bootstrap whenever the file is updated — nothing user-owned will be touched."* That's the contract.
2. **`.agents/bootstrap.json` is the answer cache.** Adding a new interview question in a future bootstrap version means existing projects will be asked *only* that new question on their next re-run.
3. **Canon vs Mixed vs Sacred is the contract on user-edits**:
   - Edited a Canon file (a rule, an ADR template, the security methodology)? Your edit is at risk of being silently overwritten on re-run. If the edit is load-bearing, **upstream the change into this bootstrap** instead of locally diverging — see Part 6.
   - Edited a Mixed file (settings.json, gitignore, Makefile, linter config)? The re-run will diff and ask. Your edit is safe unless you actively pick "overwrite".
   - Edited a Sacred file (AGENTS.md, CLAUDE.md, README, code, real ADRs, todos)? Never touched on re-run, ever.
4. **Wipe-and-recreate is a separate flow.** The user can say *"treat this as first-time mode"* to force a clean rebuild — the agent backs up the existing config dirs before doing it. Don't assume re-run mode handles this case silently.
5. **The persisted answers file is committed.** Team members re-running on a shared checkout reuse the same answers — they only get re-asked for newly-added interview keys. If a team member wants different per-machine settings, they layer them in `.claude/settings.local.json` (gitignored), not by changing `.agents/bootstrap.json`.

---

## Part 2 — Interview

Ask these. Use the defaults only if the user gives no preference — never silently.

Questions are grouped into six tiers reflecting how they're used: **bootstrap behaviour** affects how the rest of the interview/scaffolding runs; **project identity** is the minimum-viable description; **project shape properties** describe what the project IS; **feature gates** decide which optional rules / templates get installed; **repository metadata** covers license / contributions; **free-form details** capture run instructions and anything else.

### Bootstrap behaviour

| # | Question | Affects |
| --- | --- | --- |
| Q1 | **Project name + one-line purpose.** "What's the project called, and what does it do in one sentence?" | `AGENTS.md` title + purpose stub. `{{PROJECT_NAME}}` also flows into every per-tool adapter that names the project. |
| Q2 | **Which agentic coding assistants will work in this repo?** "Multi-pick. The bootstrap writes one tool-agnostic spine (`AGENTS.md` + `.agents/rules/`) plus thin per-tool adapter files for whichever assistants you pick. Pick at least one. **Claude Code** (`CLAUDE.md` adapter + `.claude/settings.json`); **Cursor** (`.cursor/rules/agents.mdc` adapter); **Aider** (`.aider.conf.yml` with `read:` list); **OpenAI Codex CLI** (reads `AGENTS.md` natively — no extra file); **OpenCode** (reads `AGENTS.md` natively — no extra file); **Continue.dev** (`.continue/config.json` rules entry); **Windsurf** (`.windsurfrules` adapter); **GitHub Copilot** (`.github/copilot-instructions.md` adapter)." Asked early — it gates Q3 and decides which adapters get written. | `AGENTS_USED` set — any subset of `{CLAUDE, CURSOR, AIDER, CODEX, OPENCODE, CONTINUE, WINDSURF, COPILOT}`. Drives the conditional dispatch for every per-tool adapter file. |
| Q3 | **Claude Code permission posture?** *(asked only if `CLAUDE ∈ AGENTS_USED`; otherwise skip — set `POSTURE=N_A` and don't write `.claude/settings.json`).* "Single-pick controlling `.claude/settings.json` content. **Cautious** (`{}`): every action prompts; safest for shared / team / open-source projects. **Read-only autonomy**: pre-allow read-only Bash (ls, cat, grep, find, git status/log/diff/show); investigation friction-free, writes still prompt. **Trusted dev**: read-only + safe git workflow + language-specific build/test commands picked from Q4 `LANG` (`uv:*` / `npm:*` / `go:*` / `cargo:*`); daily dev no prompts; force-push / hard-reset / clean -f still require approval via `deny` patterns. **Full bypass**: `defaultMode: bypassPermissions`, no prompts ever; only safe in dedicated dev VMs / containers / trusted personal workspaces." Asked early so the chosen posture takes effect for the rest of the bootstrap's file writes. | `POSTURE` value in `{CAUTIOUS, READONLY, TRUSTED_DEV, BYPASS, N_A}`. Picks the `.claude/settings.json` template variant. `N_A` skips the file. All non-`N_A` variants pin `model: claude-opus-4-7`. |

### Project identity

| # | Question | Affects |
| --- | --- | --- |
| Q4 | **Language / runtime.** "Python / TypeScript / Go / Rust / something else / mixed?" | `AGENTS.md` run section, `best-practices.md` idioms. Drives the multi-variant dispatch for `.gitignore`, manifest + test scaffold, linter configs, `Makefile`, and the `POSTURE=TRUSTED_DEV` language-specific allow addendum. |
| Q5 | **Architecture shape?** "What's the primary *internal* code organisation of this codebase? Single-pick from: **4-Layer DDD** (presentation → application → domain ← infrastructure + shared — non-trivial backends with multiple I/O surfaces); **Classical 3-Tier** (presentation / business / data — simpler CRUD apps, Rails/Django/.NET-style); **SPA frontend** (components / pages / hooks / services / types — React/Vue/Svelte conventional layout); **Flat** (no layering, modules organised by topic — CLIs, libraries, small scripts). If none fits, say so — the agent will write a minimal stub capturing the user's own description for them to expand post-bootstrap. **If the user answers with a system-topology word instead** (microservices, serverless / FaaS, monorepo, modular monolith, distributed, SOA), drop into the disambiguation below before settling on `ARCH`." | `ARCH` flag — value in `{4_LAYER_DDD, 3_TIER, SPA, FLAT, MONOREPO, SERVERLESS, OTHER}`. Derived `LAYERED` = (ARCH ≠ FLAT). Controls which `layered-architecture.md` template gets written and the `AGENTS.md` / `best-practices.md` rule-ref lines. |

#### Q5 disambiguation — when the user answers with system topology

Q5 asks how code is organised *inside* this codebase. Topology answers — **microservices**, **serverless / FaaS**, **monorepo**, **modular monolith**, **distributed**, **SOA** — answer a different question. Don't silently coerce them into one of Q5's options; ask one follow-up to pick the scenario that actually fits, then route:

| User's clarification | Route to |
| --- | --- |
| "This repo is one service among many (poly-repo, or a single microservice in a larger ecosystem)." | Re-ask Q5's normal options for **this service's** internal layering. From the bootstrap's POV the repo is just a single codebase; the surrounding ecosystem doesn't change what we write here. |
| "This repo is a monorepo containing multiple sub-projects / services / apps." | `ARCH=MONOREPO`. Top-level `layered-architecture.md` documents the monorepo layout and the discipline for adding sub-projects; each sub-project picks its own internal architecture when added (re-run the bootstrap inside the sub-project, or capture the choice in an ADR). |
| "Modular monolith — single deployable now, designed to be split into services later." | `ARCH=4_LAYER_DDD` (the layering that maps cleanest to bounded contexts). Note in the Step 5 prompt file that bounded-context boundaries are intentional and should be preserved when adding new code. |
| "Serverless / functions / FaaS — handlers per route / event / schedule, no long-running service." | `ARCH=SERVERLESS`. A handlers-first template gets written. |
| "I want microservices but haven't picked services yet" / "I just want clean separation of concerns." | Re-ask Q5's normal options. The likely fit is `4_LAYER_DDD` — a well-organised monolith with clear seams the user can split later. |
| "None of the above — I want to describe it myself." | `ARCH=OTHER`. Capture the user's one-paragraph description as a minimal stub. |

The disambiguation is one shot, not a tree. If the clarification still doesn't fit a row above, fall through to `OTHER` and capture the user's own description.

### Project shape properties

| # | Question | Affects |
| --- | --- | --- |
| Q6 | **Web app?** "Does the project expose an HTTP surface (web app, REST/GraphQL API, OAuth, sessions, browser-rendered HTML)? Used to gate web-specific rubric sub-sections in the security methodology (auth, CSP, CSRF, output encoding, SQL parameterisation)." | `WEB` flag — gates `methodology.md` web sub-sections |
| Q7 | **LLM in the request path?** "Does the project run an LLM, agent, or AI tool as part of serving requests (chat, RAG, agentic workflows, in-process model inference)? Used to gate LLM-specific rubric sub-sections (prompt injection, tool agency, model supply chain, unbounded consumption)." | `LLM` flag — gates `methodology.md` LLM sub-sections |
| Q8 | **Uses env vars / runtime secrets?** "Does the project read configuration from environment variables, manage runtime secrets, or hold credentials (database URLs, API keys, OAuth credentials, session secrets)? **Yes** for most web apps / APIs / LLM-bearing projects / CLI tools calling external services. **No** for purely static frontends (plain HTML/CSS/JS), libraries that don't ship a runtime, or scripts with no external dependencies." | `ENV_VARS` flag — gates `.env.example` |

### Feature gates

| # | Question | Affects |
| --- | --- | --- |
| Q9 | **Customer-visible surfaces?** "Does the project have public surfaces that describe the product (UI, marketing pages, public docs, public API reference)? If yes, a workflow rule will require keeping them in sync with code changes in the same commit." | `CHANGES` flag — controls `workflow-changes.md` |
| Q10 | **UI component vocabulary?** "Does the project have a UI with reusable components worth cataloguing (buttons, cards, modals, dropdowns)?" | `UI_COMPONENTS` flag — controls `ui-components.md` |
| Q11 | **Governed metrics?** "Does the project emit metering / observability events where names and labels matter (user analytics, billing-tied counters, cardinality-sensitive dashboards)?" | `METRICS` flag — controls `workflow-metrics.md` |
| Q12 | **Testing discipline?** "Should every artifact-producing change ship with the tests that prove its behaviour? **Yes** (recommended for anything that will live longer than a weekend) installs `workflow-testing.md` — the pyramid (unit-heavy / integration-light / e2e-thin), mock at boundaries not internals, regression-first for bug fixes, TDD encouraged but not mandated, coverage tracked without a hard floor, tests bundled into the same commit as the change they cover. **No** skips the rule (sensible for throwaway scripts, one-off prototypes, repos where you'll add tests later)." | `TESTING` flag — controls `workflow-testing.md` |

### Repository metadata

| # | Question | Affects |
| --- | --- | --- |
| Q13 | **License?** "Single-pick: **MIT** (permissive, most popular OSS), **Apache 2.0** (permissive + explicit patent grant — preferred for larger projects), **Proprietary** (all rights reserved, internal use only), **Skip** (no LICENSE file)." **If LICENSE ≠ SKIP**, also ask: *"Who is the copyright holder? (person name or organisation — used in the LICENSE file's copyright line.)"* | `LICENSE` value in `{MIT, APACHE_2_0, PROPRIETARY, SKIP}`. Picks the LICENSE template variant. `COPYRIGHT_HOLDER` captured as a free-form string used in the LICENSE body. |
| Q14 | **Accepting external contributions?** "yes / no. If yes, scaffold `CONTRIBUTING.md` with a stub covering dev setup, branch / PR conventions, code style pointer, and how to file issues. If no (internal / personal project), skip the file." | `CONTRIB` flag — controls `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` |

### Free-form details

| # | Question | Affects |
| --- | --- | --- |
| Q15 | **Run instructions.** "What's the command(s) to run locally? Any major system prerequisites (ffmpeg, postgres, GPU, …)?" | `AGENTS.md` run section |
| Q16 | **Anything else load-bearing for the brief?** Persistence story, security notes, deployment, dependencies, model swap-points — anything top-of-mind the agent should re-read on every cold start. | `AGENTS.md` extra sections |

---

## Part 3 — Decision matrix

The **Re-run** column codes how each file is handled when the bootstrap runs against an already-bootstrapped project (see Step 0):

- **C** = *Canon* — bootstrap is source of truth; silently rewrite if different.
- **M** = *Mixed* — user may have layered project-specific additions; diff and ask before changing.
- **S** = *Sacred* — user-owned after first write; never touch on re-run.
- **N** = *New each run* — write a fresh file every run (e.g. dated prompt files); no overwrite question.

| File | Type | Trigger | Re-run |
| --- | --- | --- | --- |
| `AGENTS.md` | Always | the primary cross-tool project brief — title, purpose, run, architecture map, rule pointers | S |
| `.agents/rules/workflow.md` | Always | — | C |
| `.agents/rules/workflow-todos.md` | Always | — | C |
| `.agents/rules/workflow-security.md` | Always | — | C |
| `.agents/rules/best-practices.md` | Always | — | C |
| `.agents/bootstrap.json` | Always | persisted interview answers; written in Step 5 | C |
| `CLAUDE.md` | Conditional | written if `CLAUDE ∈ AGENTS_USED`. Thin adapter pointing at `AGENTS.md` + `.agents/rules/`. | S |
| `.claude/settings.json` | Conditional | written if `CLAUDE ∈ AGENTS_USED` **and** Q3 `POSTURE ≠ N_A`. Content variant picked by `POSTURE`. All non-`N_A` variants pin `model: claude-opus-4-7`. `TRUSTED_DEV` also dispatches on Q4 `LANG` for the language-specific allow addendum. | M |
| `.cursor/rules/agents.mdc` | Conditional | written if `CURSOR ∈ AGENTS_USED`. Thin adapter (always-include glob) pointing at `AGENTS.md` + `.agents/rules/*`. | C |
| `.aider.conf.yml` | Conditional | written if `AIDER ∈ AGENTS_USED`. Sets `read:` list to always include `AGENTS.md` + `.agents/rules/*.md`. | M |
| `.continue/config.json` | Conditional | written if `CONTINUE ∈ AGENTS_USED`. Minimal config with a `rules` entry pointing at `AGENTS.md` + `.agents/rules/`. | M |
| `.windsurfrules` | Conditional | written if `WINDSURF ∈ AGENTS_USED`. Thin adapter pointing at `AGENTS.md` + `.agents/rules/`. | C |
| `.github/copilot-instructions.md` | Conditional | written if `COPILOT ∈ AGENTS_USED`. Thin adapter inlining the AGENTS.md pointer + rules summary (Copilot does not follow file refs). | C |
| `.docs/adrs/README.md` | Always | — | M |
| `.docs/adrs/0000-adr-template.md` | Always | — | C |
| `.docs/todos/README.md` | Always | — | C |
| `.docs/security/methodology.md` | Always | sub-sections gated by `WEB` and `LLM` flags | C |
| `.gitignore` | Always | content variant picked by Q4 `LANG`; OS / editor sweep is universal | M |
| `.env.example` | Opt-in | Q8 = yes (`ENV_VARS`). Skipped for purely static frontends, libraries, and scripts with no runtime config. | S |
| `.editorconfig` | Always | universal | C |
| `README.md` | Always | public-facing project intro; minimal stub | S |
| `LICENSE` | Conditional | written if Q13 `LICENSE != SKIP`. Content variant picked by `LICENSE` value (MIT / APACHE_2_0 / PROPRIETARY). | S |
| `<manifest>` + `tests/` scaffold | Always | manifest filename + test layout dispatched by Q4 `LANG` | S |
| `<linter configs>` | Always | content variants picked by Q4 `LANG` (`ruff.toml` / `eslint.config.js` + `.prettierrc.json` / `.golangci.yml` / `rustfmt.toml` / skip) | M |
| `Makefile` | Always | content variant picked by Q4 `LANG` | M |
| `.pre-commit-config.yaml` | Always | universal (whitespace + YAML/JSON/TOML syntax + gitleaks); user layers language-specific hooks later | M |
| `SECURITY.md` | Always | universal; private vulnerability disclosure | S |
| `.gitattributes` | Always | universal; line-ending normalisation + binary detection + linguist hints | C |
| `CHANGELOG.md` | Always | universal; Keep a Changelog format | S |
| `CODE_OF_CONDUCT.md` | Opt-in | Q14 = yes (`CONTRIB`) — same gate as CONTRIBUTING | S |
| `CONTRIBUTING.md` | Opt-in | Q14 = yes (`CONTRIB`) | S |
| `.docs/prompts/<ts>.bootstrap_project.md` | Always | written in Step 5 | N |
| `.agents/rules/layered-architecture.md` | Opt-in | Q5 ≠ FLAT (`LAYERED` derived). Template variant picked by `ARCH` value — `4_LAYER_DDD`, `3_TIER`, `SPA`, `MONOREPO`, `SERVERLESS`, or `OTHER` stub. | C |
| `.agents/rules/workflow-changes.md` | Opt-in | Q9 = yes (`CHANGES`) | C |
| `.agents/rules/ui-components.md` | Opt-in | Q10 = yes (`UI_COMPONENTS`) | C |
| `.agents/rules/workflow-metrics.md` | Opt-in | Q11 = yes (`METRICS`) | C |
| `.agents/rules/workflow-testing.md` | Opt-in | Q12 = yes (`TESTING`) | C |

---

## Part 4 — File templates

Each template below is wrapped in a **four-backtick fence** so that three-backtick code blocks inside the file content survive intact. When you write the file, write only the content between the fences — not the fence itself.

---

### Template: `CLAUDE.md` *(written only if `CLAUDE ∈ AGENTS_USED`)*

A thin Claude-specific adapter. The full brief — purpose, rules, run, architecture map — lives in `AGENTS.md`. Claude Code follows `@`-prefixed file references natively, so the rules under `.agents/rules/` get auto-loaded via the include below.

````markdown
# {{PROJECT_NAME}} — Claude Code adapter

This project's primary agent brief lives in [`AGENTS.md`](./AGENTS.md). Treat that file as the source of truth — title, purpose, run instructions, architecture map, rule pointers.

Always follow the rules under `.agents/rules/`:

@AGENTS.md
@.agents/rules/workflow.md
@.agents/rules/workflow-todos.md
@.agents/rules/workflow-security.md
@.agents/rules/best-practices.md
{{IF_LAYERED}}@.agents/rules/layered-architecture.md
{{IF_CHANGES}}@.agents/rules/workflow-changes.md
{{IF_UI_COMPONENTS}}@.agents/rules/ui-components.md
{{IF_METRICS}}@.agents/rules/workflow-metrics.md
{{IF_TESTING}}@.agents/rules/workflow-testing.md

When `AGENTS.md` and this file disagree, `AGENTS.md` wins — keep this file as a thin pointer rather than a parallel brief.
````

---

### Template: `.agents/rules/workflow.md`

````markdown
# Workflow

This rule defines the naming, contents, and ordering of the per-request artifacts so `git log`, `ls .docs/prompts/`, and `ls .docs/adrs/` together reconstruct the project's history — and the *why* behind it — from the repository alone.

Every user request that changes files in this repository produces, all bundled into a single commit and pushed:

- A **prompt file** under `.docs/prompts/` capturing what was asked and why.
- **The code, config, or docs** the request produced.
- When the change is architecturally significant — a new module, library, layer, or pattern, or a meaningful change to one — a **new or updated ADR** under `.docs/adrs/`.
- **Telemetry** kept current — new behaviour gets new logs, changed behaviour gets existing logs updated, deleted behaviour gets its logs removed, at log levels that match each event's signal (DEBUG / INFO / WARNING / ERROR / CRITICAL), with sensitive-data redaction discipline (credentials, PII, request bodies — anything that shouldn't ride a wire to a third-party log service).
- A **single git commit** bundling all of the above on the current branch.
- A **push** of that commit to the remote.

## When this rule applies

Apply it whenever the response generates or modifies a file in the repository. Typical triggers:

- Writing, editing, or deleting source code
- Adding or updating documentation, rules, configs, or scripts
- Creating data files, fixtures, or seed content
- Renaming or moving tracked files

## When this rule does NOT apply

Skip the prompt file and the commit for interactions that produce no artifact. Examples:

- Plain conversation, clarifying questions, or brainstorming with no file changes
- Read-only investigation ("what does this function do?", "show me where X is defined")
- Advice or recommendations the user has not yet asked you to implement
- Explicit user instruction to look without changing ("just explore, don't commit")

If a conversation starts as chitchat but later produces an artifact, the rule kicks in at that point — write the prompt file for the portion that generated work, not for the preceding discussion.

## 1. Create a prompt file

For each user request, write a file to `.docs/prompts/` using the pattern:

```
<unix-timestamp>.<snake_case_slug>.md
```

- **`<unix-timestamp>`**: seconds-since-epoch at the time of the request (e.g. `date +%s`). Keeps files chronologically sortable by filename.
- **`<snake_case_slug>`**: 2–5 words summarizing the intent (e.g. `fix_navmenu_client`, `home_page_structure_ideas`).

### File contents

```markdown
# Request

<Verbatim or lightly-cleaned restatement of what the user asked for. Preserve intent — do not editorialize.>

## Reasoning

<Why the user asked for this: the motivation, the constraint, the trade-off being made. One short paragraph is usually enough.>

## Output

<What was actually done in response: files created/modified, decisions taken, follow-ups noted. Bullet list or short paragraph. Keep it factual.>
```

Write the prompt file **before** or **alongside** making the changes, not after. Treat it as the commit's companion note.

## 2. Create or update an ADR

ADRs (Architecture Decision Records) live under `.docs/adrs/` and capture the **why** behind structural choices: which framework, which layer pattern, which library, which interaction model. Each is a single file in slim Nygard format and is indexed by `.docs/adrs/README.md`.

The prompt file records *what happened in this request*; the ADR records *what shape the project now has and why*. Many requests produce a prompt without touching an ADR — that's expected. The ADR question is only "did the architectural picture change?"

### When to create a new ADR

A request introduces a new ADR when it adds something the existing ADRs don't already cover:

- A new external dependency that shapes the architecture (a new framework, a new library, a database, an auth provider).
- A new module, layer, or pattern that future code is expected to follow.
- A decision with trade-offs worth recording — alternatives considered, constraints, deferred follow-ups.

Filename pattern: `.docs/adrs/<NNNN>-<kebab-case-slug>.md`. `NNNN` is the next free four-digit number; numbers never get reused. Append the new ADR's row to the table in `.docs/adrs/README.md` so the index stays current.

### When to update an existing ADR

A request updates an existing ADR when it modifies something the ADR already tracks:

- The chosen library is upgraded, swapped, or its configuration changes meaningfully.
- A deferred follow-up listed under **Consequences** is now done — move it out of follow-ups, mention it in the **Decision** body.
- A new constraint or trade-off surfaces that the original **Context** didn't anticipate.

If the decision is replaced rather than extended, mark the old ADR's **Status** as `Superseded by ADR-NNNN`, link forward in its body, and create a new ADR for the replacement.

### When to skip the ADR

The architecture stays the same for many changes; don't ADR them:

- Bug fixes, styling tweaks, copy edits.
- A new route handler, template, or service that fits a pattern an existing ADR already captures.
- Refactors internal to a single module that don't change its public contract.
- Renames, file moves, gitignore adjustments.

A useful test: if a future contributor reading only the ADRs would miss this change and end up confused about the project's shape, write or update one. Otherwise the prompt file alone carries the context.

### When to include a Mermaid diagram

If the change introduces or reshapes a system of components (a new layer, a multi-step flow, a per-tier policy graph, …), include a [Mermaid](https://mermaid.js.org) diagram inside the ADR. A picture of how the pieces fit together is often the fastest way for an engineer to grasp the change before reading the prose. Whether to include one depends on complexity — not every ADR needs one.

Reach for Mermaid when:

- The change involves more than two collaborators with non-trivial relationships (calls, ownership, data flow).
- The decision concerns a sequence of steps (request → service → tool → result) and the order matters.
- The decision establishes a dependency graph, class hierarchy, or state machine.

Skip Mermaid when:

- The change is a single isolated tweak (a copy edit, a config flag, a renaming).
- The prose alone makes the picture obvious in a sentence.

### Diagram-type picker

Don't default to `flowchart` for everything. **Mermaid supports many diagram types — the table below is a guide, not a closed list.** If the decision's shape fits a type not listed here (e.g. a `gantt` for a release schedule, a `quadrantChart` for a 2×2 strategic positioning, a `sankey-beta` for flow volumes), use it. The full type reference is at <https://mermaid.js.org/intro/> — consult it whenever the listed types don't quite fit. The agent should scan this table before drawing and choose deliberately, but the *underlying rule* is "pick whatever Mermaid type makes the shape easiest to grasp" — including types not enumerated below.

| Decision shape | Mermaid type | Why |
| --- | --- | --- |
| Layered architecture / dependency direction / module boundaries | `flowchart LR` (or `TB` for vertical hierarchy) with `subgraph` grouping | Shows the import arrows; subgraphs visually group layers / bounded contexts. |
| Request flow / call sequence / inter-service interaction over time | `sequenceDiagram` | Captures *order* and *participant* explicitly; activation bars show synchronous spans. |
| Entity lifecycle / process states / retry / circuit-breaker logic | `stateDiagram-v2` | Names states and transitions; supports nested composite states for sub-machines. |
| Data model / schema / relations between entities | `erDiagram` | Captures cardinality (`1:N`, `N:M`) and attribute lists; reads as a soft schema. |
| Class / type hierarchy / interface implementation | `classDiagram` | Shows inheritance + composition + interface satisfaction in one view. |
| System context — which services / users / externals touch this codebase | `C4Context` (or `C4Container` for one level deeper) | The C4 model's top levels make boundaries obvious without zooming into code. |
| Component breakdown inside a service | `C4Component` | Bridges between a `C4Container` and the actual codebase modules. |
| Deployment topology / nodes + their hosted containers | `C4Deployment` | Names physical / cloud nodes and what runs on each — the right level for infra ADRs. |
| Runtime collaboration that needs sequence + context together | `C4Dynamic` | Numbered sequence overlaid on the container/component view — useful when *where* and *when* matter equally. |
| Branching strategy / release model / git workflow | `gitGraph` | The only Mermaid type that natively models commits, branches, and merges. |
| Project plan / multi-track timeline with dependencies and durations | `gantt` | Tasks-with-bars + dependencies; right level for migration plans, multi-team rollouts. |
| Time-anchored milestones without dependency arrows | `timeline` | A horizontal time axis with grouped milestones; simpler than `gantt` when durations don't matter. |
| User journey / cross-functional workflow with subjective scoring | `journey` | Stages × actors × satisfaction; useful for UX-shaped decisions. |
| Concept map / brainstorm of related ideas | `mindmap` | Hub-and-spoke; good for early-stage decisions where the structure isn't a graph yet. |
| Categorical share / breakdown by percentage | `pie` | When the decision hinges on proportion (capacity allocation, traffic split). |
| Volume flow between sources, intermediaries, and sinks | `sankey-beta` | Widths encode magnitude; the right type for "where does our throughput go?" ADRs. |
| Quantitative chart embedded in an ADR (latency over time, cost projection) | `xychart-beta` | Line / bar charts inline; sufficient for the small charts that belong in an ADR. |
| 2×2 strategic positioning (effort vs. impact, build vs. buy) | `quadrantChart` | Forces the trade-off conversation onto two axes; good for option-comparison ADRs. |
| Multi-attribute comparison across options (radar / spider) | `radar` | When 5+ attributes matter and you want shape-at-a-glance comparison. |
| Requirement graph — requirement → satisfied-by → verified-by | `requirementDiagram` | The only built-in type for requirement traceability in safety / compliance contexts. |
| Block layout — boxes-and-connections without flowchart auto-layout | `block-beta` | When you want explicit grid control over a system diagram (rare; use sparingly). |
| Cloud / infra topology — hosts, networks, services | `architecture-beta` | Newer type aimed at infra diagrams; sometimes clearer than `C4Deployment` for cloud-native shapes. |
| Process / work board with columns and cards | `kanban` | When the ADR documents a workflow-board structure (release pipeline, intake queue). |
| Network packet structure / on-the-wire byte layout | `packet-beta` | Protocol design ADRs — header field sizes and offsets. |
| Hierarchical proportional breakdown (cost-by-service, capacity-by-tier) | `treemap` | When the shape is "what's the share of each child within each parent?" |

If the decision needs *two* views (e.g., a context diagram for boundaries + a sequence diagram for the request flow), put both diagrams in the ADR — one shouldn't crowd out the other. A single ADR with one too-busy diagram is worse than the same ADR with two focused ones.

> **Beta / experimental diagrams.** Mermaid marks several types `-beta` (e.g. `block-beta`, `sankey-beta`, `xychart-beta`, `packet-beta`, `architecture-beta`) and C4 support is still flagged experimental. They render on GitHub and on `mermaid.js.org`; some IDE Markdown previews fall back to showing the source. Use them when the audience views ADRs on a Mermaid-aware viewer; for hostile environments fall back to a labelled `flowchart` with `subgraph` boundaries.

### Worked examples

Use these as starting points to riff on — copy, adjust labels, add nodes.

**Layered architecture** (`flowchart LR` with subgraphs):

```mermaid
flowchart LR
  subgraph Presentation
    routes[routes/]
    templates[templates/]
  end
  subgraph Application
    services[services/]
  end
  subgraph Domain
    models[models/]
    protocols[interfaces/]
  end
  subgraph Infrastructure
    repos[repositories/]
    clients[external clients/]
  end
  routes --> services
  services --> protocols
  models -.-> services
  repos -.implements.-> protocols
  clients -.-> repos
```

**Request flow** (`sequenceDiagram`):

```mermaid
sequenceDiagram
  participant U as User
  participant API as API route
  participant S as Order service
  participant R as Order repository
  participant DB as Postgres
  U->>API: POST /orders
  API->>S: create(order_payload)
  S->>R: insert(order)
  R->>DB: BEGIN; INSERT; COMMIT
  DB-->>R: order_id
  R-->>S: Order
  S-->>API: Order
  API-->>U: 201 Created
```

**Entity lifecycle** (`stateDiagram-v2`):

```mermaid
stateDiagram-v2
  [*] --> Draft
  Draft --> PendingReview: submit
  PendingReview --> Approved: approve
  PendingReview --> Draft: reject
  Approved --> Published: publish
  Published --> Archived: archive (after 90d)
  Archived --> [*]
```

**Data model** (`erDiagram`):

```mermaid
erDiagram
  USER ||--o{ ORDER : places
  ORDER ||--|{ ORDER_ITEM : contains
  PRODUCT ||--o{ ORDER_ITEM : "appears in"
  USER {
    uuid id PK
    string email UK
    timestamp created_at
  }
  ORDER {
    uuid id PK
    uuid user_id FK
    string status
    timestamp placed_at
  }
  ORDER_ITEM {
    uuid order_id FK
    uuid product_id FK
    int qty
  }
```

**System context** (`C4Context`):

```mermaid
C4Context
  Person(customer, "Customer", "Places orders via web or mobile")
  System(api, "Order Service", "Accepts and fulfils orders")
  System_Ext(stripe, "Stripe", "Payment processor")
  System_Ext(warehouse, "Warehouse API", "Inventory + fulfilment")
  SystemDb_Ext(postgres, "Postgres", "Primary store")
  Rel(customer, api, "Places orders", "HTTPS / JSON")
  Rel(api, stripe, "Authorises charges", "HTTPS")
  Rel(api, warehouse, "Reserves stock", "HTTPS")
  Rel(api, postgres, "Reads / writes", "TCP")
```

**Branching strategy** (`gitGraph`):

```mermaid
gitGraph
  commit id: "main"
  branch develop
  commit
  branch feature/checkout
  commit
  commit
  checkout develop
  merge feature/checkout
  checkout main
  merge develop tag: "v0.2.0"
```

**Migration timeline** (`timeline`):

```mermaid
timeline
  title Postgres → cluster migration
  2026-Q1 : Shadow writes to new cluster
          : Read-side dual-checks
  2026-Q2 : Cutover for non-critical reads
          : Stress-test on 10% traffic
  2026-Q3 : Full cutover for writes
          : Legacy decommissioning
```

### Readability conventions

A diagram earns its place by being *faster to grasp than the prose*. The following keep that bar:

- **Direction matches mental model.** `LR` for flow (left-to-right reads as "from input to output"); `TB` for hierarchy (top-down reads as "from broad to specific"). Don't mix.
- **Cap soft size at ~12 nodes per diagram.** Beyond that, the diagram becomes a wall of text. Split into two focused diagrams instead — one zoomed-out, one zoomed-in.
- **Group by `subgraph`** when the diagram has 2+ clear regions (layers, bounded contexts, deployment tiers). The visual grouping does work the labels can't.
- **Name nodes by *role*, not by class name.** `Order service` beats `OrderServiceImpl`. Diagrams capture intent; class names belong in code.
- **Label edges when the relationship isn't obvious.** `A -->|publishes events| B` is worth typing; `A --> B` is fine when both sides are the same kind of thing.
- **Use solid arrows for required edges, dotted for "uses by composition / sometimes touches".** `A --> B` is "A always calls B"; `A -.-> B` is "A may consult B; the dependency exists but isn't load-bearing in every path."
- **Caption every diagram with one sentence above or below.** The sentence states what the reader should take away — "Reads flow through the cache; writes go straight to the primary." A diagram without a caption is a puzzle.
- **Stay monochrome by default.** Mermaid's auto-styling is fine; reach for `classDef` colours only when you need to distinguish two genuinely-different *kinds* of node (e.g., internal vs external systems) and a label wouldn't be enough.

GitHub renders Mermaid blocks inline; some IDE Markdown previews fall back to showing the source. Both are readable — write Mermaid as if the rendered version *and* the raw text both need to be intelligible.

### File contents

```markdown
# N. Title

- **Status**: Accepted | Proposed | Superseded by ADR-NNNN | Deprecated
- **Date**: YYYY-MM-DD

## Context
What's the situation prompting this decision?

## Decision
What did we decide?

## Consequences
What follows from this — both positive and negative. Cross-link to related ADRs by number.
```

Each ADR is short — **Context** and **Decision** usually a paragraph each, **Consequences** a bulleted list. The point is that someone can read the file in under a minute and understand both the choice and what it cost.

## 3. Ensure telemetry is in place

Code changes that don't update the project's logs are dark code: they run in production with nothing to grep for when they misbehave. Every code change must leave the observability surface coherent — new behaviour gets new log lines (at the level that matches each event's signal, not always INFO), changed behaviour gets existing logs updated, deleted behaviour gets its logs deleted.

### When telemetry must move

Add or update logs on any of these triggers:

- **New code path** — a new service method, route handler, repository, tool, middleware, or background task starts producing or transforming meaningful state. Pick the level for each event deliberately (see below). At minimum: one log for the success outcome at the level that matches the signal (DEBUG / INFO) and one at WARNING / ERROR / CRITICAL for every failure path that wasn't expected to happen.
- **Changed code path** — a method's contract, side effects, error handling, or branching changed. Walk the existing log statements and update their event names, fields, and levels to match. A log line that used to mean one thing and now means something different is worse than no log at all.
- **Deleted code path** — remove the logs that referenced it. Stale event names accumulate noise that grep eventually has to wade through.
- **New failure mode** — anywhere a `try/except` is added, the `except` branch needs at least one log call before re-raising or returning. Silent catches are observability bugs.
- **A field's meaning shifts** — if a `user_id` becomes a `session_id`, all log payloads using the old name follow. Same for renames and type changes.

If telemetry is genuinely needed but truly out of scope for the current change, capture the gap as a new file under `.docs/todos/` so it's not forgotten (rules in `workflow-todos.md`).

### Conventions

- **Module logger.** Use a module-scoped logger named after the dotted module path (e.g. `logging.getLogger(__name__)` in Python). Don't share loggers across modules — the module name is the routing key.
- **Event names** are lowercase dotted paths describing *subsystem.action* or *subsystem.action.outcome* — `chat.send.start`, `chat.send.end`, `blob.s3.put`, `auth.login.invalid_state`. Read existing log calls in the codebase before inventing a new shape; convention should be consistent.
- **Structured payloads** via the structured-fields mechanism your runtime provides (e.g. Python's `extra={...}`), never string interpolation into the message. Search, alerting, and log routing all rely on the structured fields. Keep the message string the bare event name; everything variable goes in the structured payload.
- **Levels** map roughly to:
  - **DEBUG** — fine-grained internal state useful only when actively debugging.
  - **INFO** — meaningful operations a future operator would want to see in normal traffic, INCLUDING lifecycle events (model-load milestones, warmup completions, normal start/end events). Lifecycle events live here because they're *normal* operations, not failures.
  - **WARNING** — recoverable anomalies the user noticed or the system handled but worth flagging (`auth.login.invalid_state`, `source.attach.file.too_long`).
  - **ERROR** — failures the caller has to handle, things the operator should investigate.
  - **CRITICAL** — failures or unrecoverable conditions that should wake an operator. NOT for routine boot or model-load milestones — those are INFO. The discriminator is "did something go *wrong*?", not "is this a significant moment?"
- **Timing.** For operations that can be slow, time them and include `elapsed_ms` in the payload.

### What NEVER goes in logs (sensitive data)

Treat the log stream as if it lands unencrypted on someone else's disk. *Sensitive data* is broader than *credentials* — anything that shouldn't ride a wire to a third-party log service stays out, even when it isn't a token:

- **Authentication credentials** in any form: passwords, API keys, cloud-provider access-key IDs and secret keys, OAuth client secrets, OAuth `code` grants, access tokens, refresh tokens, ID tokens, session secrets, signed cookies, Basic-auth headers.
- **Database connection passwords.** Mask the password component of a DSN before logging.
- **Encryption keys**, private keys, certificate material.
- **Verbatim exception strings on auth failures.** Some SDKs echo the access key ID on `InvalidAccessKeyId` / `SignatureDoesNotMatch`-style errors; log the canonical short error code instead.
- **PII unless it's load-bearing.** Real names, profile pictures, addresses, phone numbers, IPs, and personal preferences stay out. Email is borderline — log as a boolean (`email_present: true`) unless the value itself is the affordance being debugged. Internal UUIDs (user IDs, chat IDs) are fine — they're identifiers, not personal data.
- **Billing / financial state.** Payment-method identifiers, subscription transaction IDs from third-party processors, invoice line items. Tier names (`free`, `pro`) are fine.
- **Request bodies** — audio bytes, uploaded file contents, free-form prompt text, message content, chat titles. Log lengths, hashes, or short fingerprints if you need a needle.
- **Internal infrastructure topology** that exceeds what your `.env.example` exposes — internal IPs, hostnames not already documented, full database connection strings (even without password).

When a sensitive value's *presence* matters but the value itself doesn't, log a boolean (`token_present`, `email_present`) or a short fingerprint (first 6 chars of a hash, never the raw value).

### Audit pass on review

Before declaring a commit done, grep the diff for the logger calls and the structured payloads. For each:

- Does the level match the signal? Diagnostic-only → DEBUG; normal-traffic operation (including lifecycle / boot / model-load milestones) → INFO; recoverable anomaly the system handled → WARNING; failure the operator should investigate → ERROR; unrecoverable failure that should wake someone → CRITICAL. CRITICAL is for things going *wrong*, not for significant moments. Don't default everything to INFO either — diagnostic events still belong at DEBUG.
- Could any field carry sensitive data — a credential, token, password, unmasked DSN, PII, billing identifier, or raw user-supplied content? If yes, redact at the source.
- Is the message string a static event name (no interpolation)?
- For new failure paths: is there a corresponding log at WARNING or ERROR?

In auth, billing, admin, or any flow handling personal data, do the redaction check **twice** — once on the field as it is today, once by considering what the underlying value could become if upstream code changes.

### Security checks

Security has its own companion rule: `workflow-security.md`. The short version: changes that touch a security-sensitive surface (auth, input validation, SQL, output encoding, transport headers, secrets, logging, rate limits, dependency adds/upgrades, LLM context) walk the rubric in `.docs/security/methodology.md` *before commit*, the same way telemetry coherence is checked. The rubric is grouped by surface — read only the sub-sections that match what your change touched. Full audits remain dated sibling files under `.docs/security/<YYYY-MM-DD>-<slug>.md` on a cadence.

## 4. Commit the result

Once the work is done, create a git commit that includes:

- The prompt file (`.docs/prompts/<ts>.<slug>.md`).
- Any new or updated ADR file under `.docs/adrs/` (and the README index entry, if a new ADR was added).
{{IF_TESTING}}- The tests that cover the change (per [`workflow-testing.md`](./workflow-testing.md) — same commit as the behaviour they prove; bug fixes start with a failing regression test).
- Every other file produced or modified while handling the request.

Commit message conventions:

- Imperative subject line under 70 characters, reflecting the prompt's intent.
- Optional body paragraph for non-obvious *why*.
- Include the co-author trailer your agent host uses (`Co-Authored-By: Claude <noreply@anthropic.com>` or the equivalent for the model running the task).

Stage files by explicit path (`git add <paths>`). Never `git add -A` or `git add .` — the prompt file, ADR, and outputs are a curated set, not everything dirty in the tree.

## 5. Capture do-later ideas under `.docs/todos/`

Deferred ideas — features the agent (or the user) suggested but didn't ship in the moment, follow-ups noted in commit messages or ADR consequence sections, scope cuts surfaced during implementation — live as **one file per idea** under `.docs/todos/`. The dedicated rule `workflow-todos.md` owns the full discipline (filename pattern, file content structure, when-to-add triggers, sweep-and-remove safeguards); this section names the per-commit obligation so the rest of `workflow.md` doesn't have to duplicate it.

Manage the directory as part of every workflow turn:

- **Add** when a deferral happens. A new file at `.docs/todos/<kebab-slug>.md` with the title + Area + Refs + Context + Deferred because + Revisit when shape from `workflow-todos.md`. Surface the draft inline in your response — *"I'll capture this in `.docs/todos/<slug>.md` as: …"* — so the user sees what lands. Add in the same commit as the related work unless the deferral is the only thing the turn produced (then it's its own commit).
- **Sweep** before staging files. Scan `.docs/todos/` for entries this change satisfies. If an entry's *Revisit when* trigger has fired, `git rm` the file in the same commit. There is no archive directory; git log is canonical.
- **Remove safely** using the three-layer safeguard from `workflow-todos.md` — scope test, cite the closing change, announce inline before pushing. When in doubt, leave the entry; cost of a stale file is small, cost of dropping in-progress work is high.
- **Update** when reality drifts — edit the file in place; its `git log` is the audit trail.

Read `workflow-todos.md` end-to-end the first time you write or remove a TODO this session — the entry shape is load-bearing.

## 6. Push the commit

Immediately after the commit lands, push it to the remote:

```
git push
```

If the branch has no upstream yet, use `git push -u origin <branch>` the first time. Push without waiting for confirmation — a commit that isn't pushed doesn't exist for anyone else, and the prompt/ADR/commit/remote chain is what makes the history trustworthy.

Exception: if the push is destructive (force-push to a shared branch, rewriting already-pushed history), stop and confirm with the user first. Same for pushes to a branch with no remote configured — tell the user and let them set the remote.

## Why this rule exists

The `.docs/prompts/` history doubles as a per-request decision log and a reconstruction aid: reading the prompts in timestamp order tells the story of how the project evolved, and each prompt maps to exactly one commit so `git log` and `ls .docs/prompts/` stay aligned.

The ADRs in `.docs/adrs/` distill the architecturally significant subset — the decisions worth re-reading at scale, with their alternatives and trade-offs preserved. Reading the ADRs answers *"what is this project shaped like, and why?"*; reading the prompts answers *"what happened on day N?"*.

Breaking any of the pairings — prompt without commit, ADR-worthy change without ADR, commit without push — erodes that guarantee.

## Amending vs. new commit

Default to new commits. Amending is acceptable only when fixing a commit that has not yet been pushed **and** the user has explicitly authorized it.
````

---

### Template: `.agents/rules/workflow-todos.md`

````markdown
# Workflow — Do-Later Ideas

This rule governs how the project tracks ideas explicitly deferred — features the agent (or the user) suggested but didn't ship in the moment, follow-ups noted in commit messages or ADR consequence sections, scope cuts surfaced during implementation. Managed per the rules in `workflow.md`: the agent adds entries proactively when an idea is deferred, sweeps entries during implementation that the change satisfies, and removes (rather than archives) on completion. Cross-link the ADR or prompt where the idea originated so the *why* is reconstructible.

## Where entries live

Entries live as **one file per idea** under `.docs/todos/`, not inline in this rule. A directory listing is the index; each file is a self-contained, individually-addressable artifact. The companion `.docs/todos/README.md` explains what lives in the directory; this rule explains *how to manage entries there*.

The split is deliberate: this rule is stable (the discipline doesn't churn); the entries churn constantly (added, edited, removed every few commits). Keeping the rule small and the entries individually-addressable makes both halves easier to read, link, and `git mv` without dragging surrounding noise.

## Filename pattern

Each entry is a single markdown file named:

```
.docs/todos/<kebab-case-slug>.md
```

- **`<kebab-case-slug>`**: short, descriptive, scoped enough to avoid colliding with neighbours. Read at a glance from `ls`.
- Files sit **flat** in `.docs/todos/`. The topical grouping lives inside each file's **Area** field — `ls` is the index, no subdirectories.
- Slug derives from the entry's title. If the slug ever collides with an existing file, disambiguate by prefixing with the area (e.g. `auth-`, `ingest-`) — don't suffix with a number.

## File content structure

Every file follows the same shape — title, two header lines, three prose sections. The shape is the contract; if a draft idea doesn't fit it, the idea is probably not yet a TODO (it's a brainstorm, a feature request, an ADR candidate — surface it directly).

```markdown
# <One-line title>

- **Area:** <Topic / feature area — e.g. "Auth (ADR-0007)", "Ingest pipeline">
- **Refs:** <Comma-separated cross-links: ADR(s), prompt file(s), code paths, commit SHAs>

## Context

A paragraph (3–5+ sentences) capturing the back-story — what feature /
area we were discussing, what problem or opportunity surfaced, what
alternatives we considered, why this particular idea is worth saving.
Write enough that a future contributor (or future-you) understands the
*why* without needing to dig up the original conversation.

## Deferred because

2–4 sentences on the trade-off, blocker, scope cut, or constraint that
pushed this to later. Be specific — cite the actual constraint, not just
"out of scope".

## Revisit when

Concrete trigger — a metric crossed, a model released, an ADR landed,
a feature shipped, a usage threshold hit. Short is fine here; the test
should be unambiguous.
```

The 3–5+-sentence minimum on **Context** is load-bearing. *AI agents satisfice on minimums* — "1-2 sentences" gets read as "two words" and produces uselessly-thin entries that nobody else has the back-conversation to interpret. Don't compress it; if an entry feels long, the entry probably *should* be long.

**Cross-references** in `Refs` and `Context` use repo-relative paths from `.docs/todos/`:

- ADRs: `../adrs/<NNNN>-<slug>.md`
- Prompts: `../../.docs/prompts/<ts>.<slug>.md`
- Code: `../../<layer>/<path>.<ext>`
- Sibling docs: `../<dir>/<file>.md`

## When to add an entry (proactively, without being asked)

- The user defers an idea explicitly: *"for now"*, *"later"*, *"hold this"*, *"save it for later"*, *"add to TODOs"*, *"we'll revisit"*.
- You suggest something the user accepts but explicitly scopes out of the current change ("yes, but not this commit").
- An ADR's *Consequences* names a deferred follow-up that wouldn't otherwise be tracked anywhere actionable.
- Implementation reveals an out-of-scope sub-task worth remembering — a refactor opportunity, a known limitation that needs revisiting once a constraint changes, a "we should also do X" that the user agrees to defer.

When you spot one of these, surface the draft entry inline in your response — *"I'll capture this in `.docs/todos/<slug>.md` as: …"* — so the user sees what lands without having to open the file. Create it in the same commit as the related work unless the deferral is the only thing the turn produced (then it's its own commit per the prompt-file + commit + push rule in `workflow.md`).

## Consistency sweep on every commit

Before staging files for a commit, scan `.docs/todos/` for entries this change satisfies. If an entry's *Revisit when* trigger has fired — either because this commit closes it, or because the underlying state has changed since the entry was written — **remove the file** (`git rm`) in the same commit. There is no archive directory; git log is canonical history.

When the same commit also touches an ADR a file references, check that file's framing against current reality: a blocker that has since been resolved should be reframed or removed even if the underlying idea is still deferred for other reasons.

## Removing entries safely

Three layers of safeguard, in order:

1. **Scope test.** Only consider removing files whose `Refs:` cross-link to ADRs, prompts, or topics the current commit *actually touches*. If the commit changes one module but the candidate-for-removal lives in an unrelated area with no shared refs, leave it. This catches the "the agent thought it was done but it's something else entirely" failure mode.

2. **Cite the closing change.** To remove an entry, you must point at the specific commit / file / lines that satisfy the entry's *Revisit when* trigger. If you can't articulate that link in one sentence, the file stays. **When in doubt, leave it** — cost of an extra stale file is small; cost of dropping in-progress work is high.

3. **Announce inline before pushing.** Same pattern as the inline-draft-then-add for new entries: your response always names what was removed and why, with the citation. *"Removing **<entry title>** (`.docs/todos/<slug>.md`): <commit/ADR/feature> satisfies the *Revisit when* trigger because <one sentence>. Refs cross-checked."* The user sees it before push and can override same-turn.

These combine into: automation stays (no per-removal approval gate), paper trail exists (the announcement + cite is reviewable), failure mode is conservative (when scope or citation isn't clean, the entry stays).

## Updating entries

When reality drifts under an entry — a blocker resolves but other reasons keep the idea deferred, a trigger sharpens, a ref needs adding — edit the file in place. The file's `git log` is the audit trail; no need for "Updated YYYY-MM-DD" notes inside the body unless the change is large enough that a future reader would benefit from the timeline.

## Why this rule exists

The do-later list is a working memory across contributors and across time. If entries are scattered (in commit messages only, in chat history only, in ADR consequences only), the team forgets ideas and ships duplicates of work that was already considered and rejected. Pinning entries to individual files under `.docs/todos/` — and pinning the discipline of *when to add / sweep / remove* to this rule — keeps the list honest without requiring a separate review step.

The shape is the contract: every entry shows its back-story, its blocker, its trigger, and its refs, so the next contributor (often future-you, often a different agent session) can read a single file and decide whether the idea has aged into action.
````

---

### Template: `.agents/rules/workflow-security.md`

````markdown
# Workflow: keeping security checks honest

This rule supplements `workflow.md` for changes that touch a security-sensitive surface. The discipline: a lightweight per-request rubric pass before commit, full audits as dated sibling files re-run on cadence, findings that introduce a new mitigation pattern promoted to an ADR. The rubric, severity scale, and framework references all live in [`.docs/security/methodology.md`](../../.docs/security/methodology.md) — this rule says *when and how* to use it, not *what* it contains.

## When this rule applies

If your change touches any of these surfaces, walk the matching `§5.X` block of `methodology.md` before commit:

- **Authentication / sessions** — login, signup, OAuth, session storage, cookie flags (web).
- **Authorisation / access control** — owner-scoping, permission checks, multi-tenant boundaries (web).
- **Input validation** — request bodies, file uploads, URLs, free-form strings, CLI args, env vars (always).
- **SQL / data layer** — query construction, migrations, connection pool tuning (web / persistence).
- **Output encoding / templating** — HTML / Markdown rendering, sanitiser config, autoescape settings (web).
- **HTTP transport / browser-side** — security headers, CORS, CSRF, SRI, TrustedHost (web).
- **Secrets and configuration** — env vars, `.env.example` defaults, credential storage, boot-time logging of config (always).
- **Logging** — structured payload contents, levels, redaction discipline (always).
- **Rate limiting / resource caps** — per-actor limits, decode caps, generation budgets, agent-loop iteration caps (always — generalised to per-process / per-actor when not HTTP).
- **Dependency hygiene** — adding / upgrading deps, lockfile churn, CVE-scanner output (always).
- **LLM context** — system prompts, tool definitions, tool outputs reaching the model, agent loops, model supply chain (only when an LLM sits in the request path).

## When this rule does NOT apply

- Pure docs / copy edits, refactors with no behaviour change.
- Test additions that don't change production code paths.
- ADR or workflow-rule edits.
- Bug fixes that restore intended behaviour without changing the security model.

## Per-request: how the rubric pass works

The rubric in `methodology.md §5` is grouped by surface. For each surface your change touches:

1. Locate the matching `§5.X` block.
2. Walk each bullet and ask: *"does my change still satisfy this?"*. If yes, fine. If no, the change either fixes the regression *before* commit or includes a same-commit `.docs/todos/` entry citing the gap with a severity assessed per `§4` of `methodology.md`.
3. The pass is a self-review — no separate artefact is produced. The discipline is the act of walking the rubric, not a file you generate.

If your change introduces a *new* security-sensitive surface not yet covered (a new dependency layer, a new untrusted input source, a new tool the LLM can call), update `methodology.md §5` in the same commit so the next change has something to grep against. Treat that update like any other rule edit.

## Cadenced full audits

A full audit is a dated sibling file:

```text
.docs/security/<YYYY-MM-DD>-<slug>.md
```

The audit:

- Cites this rule + `methodology.md` for framework, severity, and rubric definitions (don't re-state them).
- Walks every `§5` surface in the order defined by `methodology.md §3`.
- Captures findings as `(severity, file:line, what, risk, recommendation)`.
- Captures an `[Info]` note for surfaces with no findings — so absences are explicit, not implicit.
- Closes with a prioritised recommendation list (highest risk reduction per hour first).
- Has an explicit "out of scope" section.

Cadence triggers:

- **Calendar** — every N months (3 / 6 / 12, depending on project risk profile).
- **Significant surface change** — a new auth provider, the first user-uploaded content endpoint, the first LLM tool call, a new external integration that broadens the trust boundary.
- **Pre-release** — before the first public deploy; before tier expansions that materially change exposure.
- **Reactive** — after a CVE drops on a high-velocity dep the project uses, after a security-relevant incident anywhere in the stack.

Previous audits stay where they are; the new audit is a sibling. The diff between audits is the project's security trend over time. A re-run after the prioritised recommendations from the previous audit ship should produce a noticeably shorter `[High]` list — that's the signal the previous audit caught real risk, not just style.

## Findings → ADRs

When a finding's fix introduces a *pattern future code is expected to follow* — a new middleware, a new repository-layer check, a new sanitiser, a new dependency convention — promote the decision to an ADR under `.docs/adrs/`. The ADR captures the pattern; the audit file captures the finding that motivated it. Cross-link both ways.

When a finding is fixed *without* introducing a load-bearing pattern (a one-off config tweak, a one-off bug fix), the audit file plus the regular workflow.md commit are enough — no ADR needed.

## Why this rule exists

Security regressions are slow and silent — a missing `Secure` flag on a cookie, a forgotten owner-scope on a new endpoint, a `trust_remote_code=True` snuck in by a careless model swap, a SQL query that grew an f-string when it was refactored. None of these crash the test suite; all of them produce real incidents.

Coupling the rubric to every security-relevant commit (lightweight, surface-scoped) and to scheduled audits (deep, whole-surface) keeps the security posture from drifting while staying proportional to project shape — small projects don't pay an OAuth-review cost if they have no auth.
````

---

### Template: `.agents/rules/best-practices.md` — two variants, picked by the Step 4b capability probe

`best-practices.md` is the one rule file whose value depends sharply on the *current* state of the chosen language + framework ecosystem. Step 4b in Part 1 decides which variant to write based on whether the running agent host has web access.

- **Refined variant** (write when web access is available) — a generation contract the agent follows. The agent fan-outs searches against current sources, then produces a stack-specific file that mirrors the structural skeleton below, with inline citations and a `refined` marker.
- **Stub variant** (write when web access is unavailable) — a static, language-agnostic baseline with a `stub` marker and a *How to enable refinement* matrix so the user knows what knobs to flip per agent host.

Both variants ALWAYS end with the same set of sections so downstream rule cross-references (from `workflow.md`, `workflow-testing.md`, `layered-architecture.md`) keep working regardless of which variant landed.

---

#### Variant A: Refined (generation contract, used when Step 4b's probe succeeds)

This is not a verbatim template — it's the contract the agent follows when producing the refined file. The output is markdown the agent writes from research; the structure below names the required sections, their goals, and the source-citation expectations.

**Top-of-file marker (mandatory, literal):**

```markdown
<!-- best-practices: refined · sources: [<comma-separated source labels>] · accessed: <YYYY-MM-DD> · lang: <LANG> · arch: <ARCH> -->
```

**Required sections** (in this order; expand each from current research for the user's specific stack):

1. `# Best Practices` — H1 title plus a one-paragraph orientation that names the stack ({{LANG}} + main framework(s) detected from Q14/Q15) and the date of the research pass.
2. `## Architecture` — language- and framework-specific notes on the chosen `ARCH`. If `LAYERED`, cross-reference [`layered-architecture.md`](./layered-architecture.md) and keep the architecture-rule as the source of truth on layer names / arrows; this file adds *language-idiomatic* layering notes (e.g. for Python+FastAPI: dependency-injection via `Depends`; for Go: interface segregation at package boundaries; for TS+Next.js: server vs client component split).
3. `## Repository pattern` — current idioms for the chosen language's ORM / data layer. Cite the ORM's own docs.
4. `## Service pattern` — orchestration conventions, with the chosen framework's lifecycle / DI primitives named.
5. `## Dependency Injection & Inversion` — the language's idiomatic DI primitives, container libraries (if any), constructor injection patterns. Avoid recommending a heavy DI framework if the language's primitives are sufficient.
6. `## Code style` — idiomatic style for the specific language + framework. Cover: import organisation, async / concurrency primitives, privacy markers, date / timezone handling, immutability where idiomatic, type system usage, validation at boundaries, error model. Cite the official style guide where one exists (PEP 8 + ruff defaults for Python, Effective Go, TS handbook, official Rust style guide, framework-specific conventions).
7. `## File & Naming Conventions` — language-idiomatic naming (module casing, class casing, file layout). Cite the language's convention doc.
8. `## Data & Formatting` — locale-aware formatting libraries the language ecosystem provides, current best practice for serialisation (orjson vs json, Jackson vs serde_json, etc.).
9. `## Testing notes` *(include only if `TESTING=yes`)* — the language's current test runner conventions (pytest fixtures vs unittest; vitest vs jest; `go test` vs testify; cargo test conventions). Defer the *discipline* itself to [`workflow-testing.md`](./workflow-testing.md); this section adds the *idiomatic mechanics* (how to structure fixtures, how to parametrise, how to use the language's mocking library).
10. `## What NOT to do` — known anti-patterns in this specific stack, sourced from current community discussion (e.g. "don't use `requirements.txt` for new Python projects in 2026" if that's the consensus at the time of research). Be concrete; abstract anti-patterns belong in `workflow.md`.
11. `## References` — bullet list of all sources cited inline, in the form `- <Title> — <URL> (accessed <YYYY-MM-DD>)`. First-party sources first (official docs, language style guides), then well-regarded secondary sources (popular framework guides, widely-cited blog posts from recognised authors). Skip random blog posts.

**Inline citations.** Every significant claim ("FastAPI dependency injection via `Depends`", "use `orjson` for high-throughput JSON in Python") carries an inline citation like `([FastAPI docs](https://fastapi.tiangolo.com/tutorial/dependencies/))`. Don't pile up citations on uncontentious statements — cite where the recommendation matters and where the user might want to verify.

**Quality bar.** Refined content is concrete, opinionated, and dated. If the research surfaces conflicting recommendations (a 2023 blog post vs the 2026 official docs), prefer the more recent first-party source and note the divergence. If a section can't be filled with stack-specific guidance from current sources, write the generic baseline for that section only (don't fail the whole refinement) and note the gap inline.

**Cross-references to preserve verbatim:**

- `[layered-architecture.md](./layered-architecture.md)` — gated on `{{IF_LAYERED}}`.
- `[workflow.md](./workflow.md)` — for the one-prompt-one-commit rule.
- `[workflow-testing.md](./workflow-testing.md)` — gated on `{{IF_TESTING}}`.

---

#### Variant B: Stub (literal template, used when Step 4b's probe fails or self-configure doesn't unstick it)

````markdown
<!-- best-practices: stub · refinement deferred · reason: {{REFINEMENT_FAILURE_REASON}} -->
# Best Practices

> **This file is the generic baseline.** It contains language-agnostic patterns that apply across most projects. For *much* more value, refine it from current web sources for your specific {{LANG}} + framework stack — see [§ Enable refinement](#enable-refinement) at the bottom of this file.

Patterns and conventions established in this project. Apply them when adding new features or refactoring. Expand this file with language- or framework-specific idioms as the project matures — the sections below are the language-agnostic core.

## Architecture

{{IF_LAYERED}}### Layered architecture
{{IF_LAYERED}}
{{IF_LAYERED}}Follow [`.agents/rules/layered-architecture.md`](./layered-architecture.md) for the project's layer names and dependency direction. Whatever the chosen shape (4-Layer DDD, 3-Tier, SPA, …), dependencies flow in one direction only; reverse imports break the layering. The architecture rule names the layers, the responsibilities of each, and the import arrows; this best-practices file just enforces *that you follow the rule*.
{{IF_LAYERED}}

### Repository pattern

Every external data source is hidden behind a repository class.

- Repositories expose intent-revealing methods (`load_projects`, `load_commits`), not raw paths or URLs.
- Separation of concerns inside the class: private helpers handle discovery/parsing; public methods compose them.
- Always sort results deterministically (by date ascending unless otherwise specified).

### Service pattern

Business logic lives in services (classes, or module-level functions for genuinely stateless services).

- Services receive collaborators via `__init__` (never instantiate them internally).
- Services own data-loading orchestration — presentation handlers must not call repositories directly for computed data.
- Expose small focused methods and a high-level aggregator for UI consumption.
- Keep pure helpers as private members.

### Dependency Injection & Inversion

- **Constructor injection**: dependencies are passed to `__init__`, never instantiated inside methods.
- **Central wiring**: a single composition root (often `application/container.py` or equivalent) composes the graph. It exposes factory functions returning singletons.
- **Testability**: the container exposes a `reset()` (or equivalent) that clears cached instances so tests can swap fakes without touching production code paths.
- **Fail fast**: constructors validate required deps (e.g. `raise ValueError("XService requires a YRepository")`).

## Code style

- **Imports**: absolute across layers; relative imports only within the same package.
- **Async**: use the runtime's async primitives (`async`/`await` in Python or JS/TS, goroutines in Go, …) and run independent I/O concurrently where it helps. Don't mix sync and async carelessly inside a single call path.
- **Privacy**: prefer language-idiomatic privacy markers (`_underscore` for module-private in Python; `private` in TS; lowercase for unexported in Go). Reserve aggressive privacy mechanisms (double-underscore name mangling, sealed classes, etc.) for actual collision avoidance — don't reach for them as "more private".
- **Dates**: timezone-aware end-to-end. Never rely on system locale or naive datetimes for boundary work.
- **Avoid mutation**: prefer non-mutating operations where the language has them (`sorted(xs)` over `xs.sort()` in Python, spread/`map` over in-place updates in JS, immutable structs where the language supports them).
- **Type hints**: required for public function signatures and class attributes wherever the language supports them.
- **Validation**: validate at boundaries (UI input, external APIs, file parsing). Trust internal data shapes once they cross the boundary.
- **Errors**: raise specific exceptions in infrastructure; the application layer catches and converts to user-facing strings.

## File & Naming Conventions

- Module files: lowercase with the language's idiomatic separator (`snake_case.py`, `kebab-case.ts`, `lowercase.go`). One class per file for service/repository classes; small related helpers may co-locate.
- Services: `<feature>_service.<ext>` exporting a `<Feature>Service` class.
- Repositories: `<entity>_repository.<ext>` exporting a `<Entity>Repository` class.
- Domain protocols / interfaces live under a `domain/interfaces/` (or `domain/protocols/`, or your language's equivalent) directory.
- Infrastructure adapters: `<provider>_client.<ext>` (e.g. `s3_client.ts`, `youtube_client.py`).
- Constants: `UPPER_SNAKE_CASE` at module level.
- Private members: `_single_underscore` (Python) or the equivalent for your language.
- Package directories use lowercase, no separators.

## Data & Formatting

- Always sort returned collections — dates ascending by default, stats descending by value.
- Format numbers and dates via a locale-aware library (Babel for Python, Intl for JS, `golang.org/x/text` for Go) where the audience matters.
- Section copy should be **generic** and explain what the stats represent — never hard-code narrative from a specific dataset.

## What NOT to do

- Don't instantiate repositories in presentation handlers or services — get them from the container.
- Don't compute logic inside route handlers — delegate to application services.
- Don't add comments that restate the code; only document non-obvious *why*.
- Don't reach for a custom decorator/metaclass when a plain function or class fits.
{{IF_LAYERED}}- Don't mix layers — see [`.agents/rules/layered-architecture.md`](./layered-architecture.md) for the project's dependency direction. Reverse imports break the layering.
- Don't track build artifacts or virtual envs in git — gitignore them.
- Don't bundle multiple unrelated changes in one commit; one prompt + one commit per request (see `.agents/rules/workflow.md`).

## Enable refinement

The bootstrap tried to refine this file from current {{LANG}} + framework sources but couldn't reach the web from your agent host. Once you fix that, ask any agent to *"re-run the bootstrap's Step 4b best-practices refinement"* and a stack-specific version will replace this stub. **How to enable web access per host:**

| Agent host | What to enable |
| --- | --- |
| **Claude Code** | The `WebSearch` and `WebFetch` tools ship with the CLI. If calls prompt for permission, add `"WebSearch"` and `"WebFetch(domain:*)"` (or specific allowed domains) to the `permissions.allow` array in `.claude/settings.json`. For headless / cron runs, also pre-allow the domains you expect to fetch. |
| **Cursor** | Web search is built in (the `@web` symbol). If the agent doesn't pick it up automatically, prompt it explicitly: *"Use @web to research {{LANG}} best practices, then refine .agents/rules/best-practices.md."* |
| **OpenAI Codex CLI** | The `--web` flag / web-tool capability must be enabled in your Codex config. See `codex --help` for the current flag name; web access is opt-in per session. |
| **Aider** | Aider doesn't ship native web search. Either pipe sources in via `aider --read <url-or-path>` after fetching them yourself (`curl`), or use the `/web` slash command if your Aider build supports it (newer versions). |
| **OpenCode** | Web search is available via the platform's tool config. Enable it in your OpenCode settings before re-running the refinement prompt. |
| **Continue.dev** | The `@web` context provider is opt-in — add `"web"` to your `.continue/config.json`'s `contextProviders` array. |
| **Windsurf** | Web search is available via the platform's tool palette. Confirm it's enabled in your Windsurf workspace settings. |
| **GitHub Copilot** | Copilot Chat in supported IDEs has the `@web` participant (Copilot Workspace + recent VS Code Insiders). If your host is older / web-less, fetch sources manually and paste excerpts into the chat, then ask Copilot to refine the file. |

**Can the agent self-configure?** Sometimes. If your host's gap is *permissions* (the tool exists but is gated), an agent with write access to the host's config file can add the right entry — Claude Code can edit `.claude/settings.json`, Continue.dev can edit `.continue/config.json`. Ask the agent to enable web search by editing its own config, then re-run the refinement. If your host's gap is *capability* (the tool doesn't exist), no agent can give itself a new tool — switch hosts or fetch sources manually.

When refinement runs successfully, the marker comment at the top of this file flips from `stub` to `refined` and `bootstrap.json`'s `BEST_PRACTICES_REFINED` flag becomes `true`. Re-running the bootstrap after that point leaves this file alone (it becomes user-owned).
````

---

### Template: `.agents/rules/layered-architecture.md` — variant for `ARCH=4_LAYER_DDD`

````markdown
# Layered Architecture (4-Layer DDD)

This document describes the layered architecture of this project — `presentation/` (UI surface), `application/` (business logic), `domain/` (pure models), `infrastructure/` (I/O) — plus `shared/` for cross-cutting utilities. Dependencies flow inward only: a new module goes in the layer matching its responsibility, and must not import from a layer further out.

## Project Structure (Sample)

Concrete entries are placeholders; rename / extend as the project takes shape.

```txt
{project-folder}/
├── .agents/                            # Tool-agnostic agent config: rules/, bootstrap.json
├── .claude/                            # Claude Code: settings.json (if Claude in AGENTS_USED)
├── .docs/                              # ADRs, todos, project docs
├── .python-version / .nvmrc / etc.     # Language/runtime version pin
├── .gitignore
├── <pkg manifest>                      # pyproject.toml / package.json / go.mod / …
│
├── <entrypoint>                        # Process entrypoint (bootstrap + launch; no business logic)
│
├── presentation/                       # UI surface — routes, templates, components
│   ├── routes/                         # HTTP route handlers (one module per resource)
│   ├── templates/                      # If templated UI
│   ├── components/                     # UI helpers (parsers, formatters)
│   └── static/                         # Static assets
│
├── application/                        # Business logic — no I/O, no UI framework imports
│   ├── container.py / di.ts / …        # DI composition root
│   ├── services/                       # Stateless orchestrators over repositories
│   │   └── <feature>_service.<ext>
│   └── use_cases/                      # Multi-service workflows (optional)
│       └── <verb_noun>.<ext>
│
├── domain/                             # Pure models & contracts — zero deps on other layers
│   ├── models/
│   │   └── <entity>.<ext>              # Data classes / value objects
│   ├── interfaces/
│   │   └── <entity>_repository.<ext>   # Protocol / interface contracts
│   └── errors/
│       └── <domain_error>.<ext>        # Domain-specific exception classes
│
├── infrastructure/                     # All I/O lives here — the only layer that touches the outside world
│   ├── network/
│   ├── http/
│   ├── auth/
│   ├── db/
│   ├── logging/
│   ├── repositories/                   # Persistence adapters implementing domain protocols
│   │   └── <entity>_repository.<ext>
│   └── telemetry/
│
└── shared/                             # Cross-cutting utilities & types (no business logic)
    └── utils/
```

## Layer responsibilities

- **Entrypoint** — process entrypoint. Bootstraps the DI container, builds the app, launches the server / CLI / worker. Contains no business logic.
- **`presentation/`** — the UI surface. Route handlers **orchestrate** (resolve the viewer, call a service, render a template). Never fetch from a repository directly, never contain business rules, never instantiate dependencies — those come from the DI container.
- **`application/`** — use-case and service classes. Services receive collaborators through **constructor injection** and expose intent-revealing methods. No direct instantiation of infrastructure inside service bodies; no I/O (that lives in `infrastructure/`); no UI framework imports.
- **`domain/`** — plain types, value objects, domain errors, and the **protocols** repositories must satisfy. Zero imports from other layers. Swapping a database or HTTP client never touches this folder.
- **`infrastructure/`** — the only layer that talks to the outside world: DBs, HTTP APIs, filesystem, ML model weights, clocks, sockets. Concrete repositories implement the protocols declared in `domain/`. Each adapter is small, testable, and replaceable.
- **`shared/`** — pure utilities, constants, and shared types that cross feature boundaries. No business logic; no repository or service imports.

## The Dependency-Injection container

The container is the **composition root**: the single module that knows how to build every service and repository, and the single place `presentation/` modules go to obtain them.

- **Singletons vs. scoped factories**. Stateless collaborators are singletons. Anything parameterised by a runtime value — per-user, per-tenant, per-request — is produced by a **scoped factory** keyed on that value so the same request reuses the same instance.
- **Constructor injection everywhere**. Services declare their dependencies in `__init__`; the container wires them. A service never reaches back into the container; a `presentation/` module never instantiates a repository directly.
- **Fail fast**. Constructors validate required collaborators so missing wiring surfaces at boot, not on the first call.
- **Testability**. The container exposes a `reset()` (or equivalent) that clears cached instances so tests can swap in fakes without touching production code paths.
- **Active identity resolution**. Where requests are scoped to a signed-in user, the container exposes a single helper that reads the verified session and returns the scoping key. Every scoped repository is instantiated from that key, so one session can only read its own data.

## Dependency direction (the only rule that never bends)

```
presentation ──▶ application ──▶ domain ◀── infrastructure
       │                              ▲
       └──────────── shared ──────────┘
```

- `presentation/` depends on `application/` (and `shared/`) — never on `infrastructure/` directly.
- `application/` depends on `domain/` — never on `infrastructure/` concretes, only on the protocols declared in `domain/`.
- `infrastructure/` depends on `domain/` (to implement its protocols) — never on `application/` or `presentation/`.
- `domain/` depends on nothing.
- `shared/` depends on nothing business-specific — only on the standard library and framework primitives.

If an import would break the arrows above, the layering is wrong — fix the dependency before merging.
````

---

### Template: `.agents/rules/layered-architecture.md` — variant for `ARCH=3_TIER`

````markdown
# Layered Architecture (Classical 3-Tier)

This document describes the classical 3-tier architecture of this project — `presentation/` (UI surface), `business/` (rules and orchestration), `data/` (persistence + external I/O). Dependencies flow inward only: presentation calls business, business calls data, and nothing calls back upward.

## Project Structure (Sample)

Concrete entries are placeholders; rename / extend as the project takes shape.

```txt
{project-folder}/
├── .agents/                            # Tool-agnostic agent config: rules/, bootstrap.json
├── .claude/                            # Claude Code: settings.json (if Claude in AGENTS_USED)
├── .docs/                              # ADRs, todos, project docs
├── .gitignore
├── <pkg manifest>                      # pyproject.toml / package.json / go.mod / …
│
├── <entrypoint>                        # Process entrypoint (bootstrap + launch; no business logic)
│
├── presentation/                       # UI surface — routes, templates, components
│   ├── routes/                         # HTTP route handlers (one module per resource)
│   ├── templates/                      # If templated UI
│   └── static/                         # Static assets
│
├── business/                           # Business logic — rules, orchestration, validation
│   ├── services/                       # Stateless orchestrators over data-access objects
│   │   └── <feature>_service.<ext>
│   ├── models/                         # Domain types (data classes / value objects)
│   │   └── <entity>.<ext>
│   └── validation/                     # Cross-field validators, business invariants
│
├── data/                               # Persistence + external I/O
│   ├── repositories/                   # CRUD access to DB tables / collections
│   │   └── <entity>_repository.<ext>
│   ├── clients/                        # External API / SDK wrappers
│   └── migrations/                     # DB schema migrations
│
└── shared/                             # Cross-cutting utilities (no business logic)
    └── utils/
```

## Layer responsibilities

- **Entrypoint** — bootstraps the app, wires dependencies, launches the server / CLI / worker. Contains no business logic.
- **`presentation/`** — the UI surface. Route handlers **orchestrate** (validate request shape, call a service, render a response). No SQL, no DB access, no business rules in handlers.
- **`business/`** — services that compose data-access calls into use cases, plus the domain types they pass around. Services hold the *rules* (e.g. "a paid user can do X but a free user cannot"). The models in `business/models/` are plain data; serialisation lives at the boundary, not inside them.
- **`data/`** — the only layer that talks to the outside world: DB, external APIs, filesystem. Repositories expose intent-revealing methods (`find_active_users`, `save_invoice`) and hide the SQL / query DSL behind that interface. Each repository is small, testable, and replaceable.
- **`shared/`** — pure utilities, constants, and shared types that cross feature boundaries. No business logic.

## The Dependency-Injection container

The container is the **composition root**: the single module that knows how to build every service and repository, and the single place `presentation/` modules go to obtain them.

- **Constructor injection everywhere**. Services declare their dependencies in `__init__`; the container wires them. A service never reaches back into the container; a route handler never instantiates a repository directly.
- **Singletons vs. scoped factories**. Stateless collaborators are singletons. Anything parameterised by a runtime value (per-user, per-tenant, per-request) is produced by a scoped factory.
- **Testability**. The container exposes a `reset()` so tests can swap in fakes.

## Dependency direction (the only rule that never bends)

```
presentation ──▶ business ──▶ data
       │           │           │
       └─── shared ┴─── shared ┘
```

- `presentation/` depends on `business/` (and `shared/`) — never on `data/` directly.
- `business/` depends on `data/` for I/O and on `shared/` for utilities — never on `presentation/`.
- `data/` depends on `shared/` only — never on `business/` or `presentation/`.

If an import would break the arrows above, the layering is wrong — fix the dependency before merging. The most common drift is route handlers reaching into `data/` to "save one quick thing"; that's where rules get lost. Route the call through a `business/` service instead, even if the service is one line today.

## When to consider promoting to 4-Layer DDD

3-Tier collapses the *domain* (pure types + protocols) into `business/`. That works fine until the project grows enough that:

- Multiple business services share the same domain types and the import graph between them gets tangled.
- The data layer's concrete shape leaks into business logic (e.g. raw `Row` objects flowing back into services).
- Swapping a persistence backend would touch many business files.

When that happens, the project is outgrowing 3-Tier. The migration is mechanical: extract `domain/` from `business/` (types + protocols), rename `data/` to `infrastructure/` (which then implements the protocols `domain/` declares), and the rule becomes 4-Layer DDD. Capture the migration as an ADR; the discipline is otherwise the same.
````

---

### Template: `.agents/rules/layered-architecture.md` — variant for `ARCH=SPA`

````markdown
# Frontend Architecture (SPA)

This document describes the file organisation of this single-page application. SPAs don't have the same inward-only data-flow rule as backend layered architectures — but they *do* have a clear dependency direction between file kinds (pages → components → primitives; pages → hooks → services; everything → types / utils), and following it keeps the codebase navigable.

## Project Structure (Sample)

Concrete entries are placeholders; rename / extend as the project takes shape.

```txt
{project-folder}/
├── .agents/                            # Tool-agnostic agent config: rules/, bootstrap.json
├── .claude/                            # Claude Code: settings.json (if Claude in AGENTS_USED)
├── .docs/                              # ADRs, todos, project docs
├── .gitignore
├── package.json
├── tsconfig.json (or jsconfig.json)
├── vite.config.ts (or webpack/rollup/etc.)
├── index.html                          # SPA entry HTML
│
├── src/
│   ├── main.<tsx|jsx>                  # App entry — mounts the root component
│   ├── App.<tsx|jsx>                   # Root component (router, providers, layout)
│   │
│   ├── pages/                          # Route-level composites; one file per route
│   │   ├── HomePage.<tsx|jsx>
│   │   └── <Feature>Page.<tsx|jsx>
│   │
│   ├── components/                     # Reusable presentational components
│   │   ├── ui/                         # Primitives (Button, Card, Modal, …)
│   │   └── <feature>/                  # Feature-scoped components
│   │
│   ├── hooks/                          # Custom hooks — stateful logic, no JSX
│   │   └── use<Thing>.<ts|js>
│   │
│   ├── services/                       # API clients, data fetching, side-effectful glue
│   │   └── <resource>_service.<ts|js>
│   │
│   ├── stores/                         # Global state (Zustand / Redux / Pinia / …) — optional
│   │   └── <slice>_store.<ts|js>
│   │
│   ├── types/                          # Shared TypeScript types / interfaces
│   │   └── <domain>.<ts>
│   │
│   ├── utils/                          # Pure helpers (formatters, parsers, predicates)
│   │   └── <topic>.<ts|js>
│   │
│   ├── styles/                         # Global CSS / Tailwind config / theme tokens
│   │
│   └── assets/                         # Static assets bundled with the app (svg, png, fonts)
│
├── public/                             # Static files served as-is (favicon, robots.txt)
│
└── tests/                              # Unit / integration tests (or co-located *.test.<ext>)
```

## File-kind responsibilities

- **`pages/`** — route-level composites. Each file maps to one route. Pages compose components + call hooks; pages do *not* contain inline business logic or fetch calls (delegate to hooks / services).
- **`components/`** — presentational, reusable. `components/ui/` is the design-system primitives (Button, Card, Modal, Form fields); `components/<feature>/` is feature-scoped composites. Components receive props, render JSX, raise events. No data fetching inside a component — call a hook.
- **`hooks/`** — stateful logic without JSX. `useUser()`, `useDebounce()`, `useChat()`. Hooks call services for I/O and return state + handlers to the caller.
- **`services/`** — the only layer that talks to the outside world. API clients (REST / GraphQL / WebSocket), browser APIs (geolocation, storage), third-party SDKs. Services return promises / observables; the consumer (usually a hook) decides how to surface state.
- **`stores/`** (if used) — global state. Each slice owns a coherent piece of the app's state machine. Stores read from services; UI components read from stores via selectors.
- **`types/`** — shared TypeScript types / interfaces. Pure type files, no runtime code.
- **`utils/`** — pure functions only. Formatters, parsers, predicates. No imports of components / hooks / services.
- **`styles/`** — global CSS, Tailwind config, theme tokens. Project-specific CSS that Tailwind utilities can't express cleanly.
- **`assets/`** — static media that ships with the bundle.

## Dependency direction

```
pages ──▶ components ──▶ types / utils
  │           │
  │           └─▶ hooks ──▶ services ──▶ types
  │                  │
  │                  └──▶ stores ◀── services
  │
  └─▶ hooks ──▶ services
```

- **`pages/`** can import from anywhere downstream (components, hooks, services, stores, types, utils).
- **`components/`** can import other components, types, utils. Components should *not* import services directly — go through a hook so the side-effect is testable.
- **`hooks/`** can import services, stores, other hooks, types, utils. No JSX.
- **`services/`** can import types and utils. **Never** import components, hooks, pages, or stores — services are the leaves.
- **`stores/`** can import services, types, utils. Don't have stores import components.
- **`types/`** and **`utils/`** import nothing project-internal (only stdlib + npm deps).

If an import would break the arrows above, the organization is wrong — refactor before merging. The most common drift is a component fetching data inline; route the fetch through a hook so the component stays pure and the side-effect can be mocked in tests.

## What this rule does NOT cover

- **Component shape and styling conventions** — those live in [`ui-components.md`](./ui-components.md) (if installed) or grow as a project-specific catalog.
- **State management choice** (Zustand / Redux / Context-only / Pinia / Svelte stores) — that's an ADR-level decision; record the choice and its trade-offs in `.docs/adrs/`.
- **Routing library choice** — same as above.
- **Backend communication shape** (REST / GraphQL / tRPC / RPC) — same. The `services/` layer hides whichever choice you make from the rest of the app.
````

---

### Template: `.agents/rules/layered-architecture.md` — variant for `ARCH=MONOREPO`

````markdown
# Repository Architecture (Monorepo)

This document describes the *top-level* layout of this monorepo and the discipline for adding sub-projects. **Internal** code organisation of each sub-project (4-Layer DDD, 3-Tier, SPA, Flat, Serverless, …) is **not** decided here — it's picked when the sub-project is added, captured in an ADR, and ideally has its own bootstrap re-run inside the sub-project directory.

## Project Structure (Sample)

Concrete entries are placeholders; rename / extend as the project takes shape.

```txt
{project-folder}/
├── .agents/                            # Tool-agnostic agent config: rules/, bootstrap.json (shared across sub-projects)
├── .claude/                            # Claude Code: settings.json (if Claude in AGENTS_USED, shared across sub-projects)
├── .docs/                              # ADRs, prompts, todos, project docs (cross-cutting)
├── .gitignore
├── README.md
├── <workspace manifest>                # pnpm-workspace.yaml / package.json (workspaces) / Cargo.toml / go.work / turbo.json / nx.json
│
├── apps/                               # End-user-facing deployables (web apps, CLIs, mobile)
│   └── <app-name>/
│       ├── .agents/                    # Sub-project agent config (optional override of top-level)
│       ├── <pkg manifest>
│       └── …                           # Internal architecture decided per sub-project
│
├── services/                           # Backend / API / worker services (long-running deployables)
│   └── <service-name>/
│       ├── <pkg manifest>
│       └── …                           # Internal architecture decided per sub-project
│
├── packages/ (or libs/)                # Shared libraries consumed by apps/ and services/
│   └── <package-name>/
│       ├── <pkg manifest>
│       └── …
│
└── tools/                              # Build, deploy, codegen, CI helpers — not shipped to users
```

## Top-level rules

- **Each sub-project owns its internal architecture.** When adding a new `apps/<name>` or `services/<name>`, re-run the bootstrap *inside* that directory, or capture the chosen layering (4-Layer DDD / 3-Tier / SPA / Flat / Serverless / Other) in an ADR under `.docs/adrs/`. Sub-projects do **not** silently inherit a top-level layering — the decision is explicit per sub-project.
- **Dependency direction across the monorepo**: `apps/` and `services/` depend on `packages/`; `packages/` depend on each other in a DAG (no cycles); `tools/` may depend on anything (but is not depended on by anything that ships).
- **Cross-cutting code lives in `packages/`**, never copy-pasted between sub-projects. If two sub-projects need the same helper, lift it to a package before the third user shows up.
- **Per-sub-project deployability**. Each `apps/<name>` and `services/<name>` should be runnable and deployable on its own. Shared CI sequences sub-project pipelines but doesn't merge them.
- **One ADR per significant cross-cutting decision** — workspace tool (npm / pnpm / yarn workspaces / nx / turborepo / cargo / go workspaces), shared linting strategy, release/versioning model (fixed vs independent), CI orchestration, cross-sub-project import boundaries. Capture in `.docs/adrs/` so the next sub-project's author understands the constraints they inherit.

## When to consider promoting a sub-project out of the monorepo

- Its release cadence diverges so much that monorepo CI becomes a bottleneck.
- Its dependency graph isolates cleanly with zero `packages/` imports unique to it.
- It needs different access control (open-source carve-out, tenant isolation, regulated workload).

Capture the split as an ADR; the rest of the monorepo layout otherwise stays put.
````

---

### Template: `.agents/rules/layered-architecture.md` — variant for `ARCH=SERVERLESS`

````markdown
# Serverless Architecture (Functions / FaaS)

This document describes the file organisation of a serverless / function-per-handler codebase. There's no long-running server process: each handler is a leaf invoked by an HTTP route, event, queue message, or schedule. The discipline is to keep handlers **thin** (parse the platform event → call exactly one `lib/` service → format the response) and push all business and infrastructure logic into `lib/` so it's testable without standing up the platform runtime.

## Project Structure (Sample)

Concrete entries are placeholders; rename / extend as the project takes shape.

```txt
{project-folder}/
├── .agents/                            # Tool-agnostic agent config: rules/, bootstrap.json
├── .claude/                            # Claude Code: settings.json (if Claude in AGENTS_USED)
├── .docs/                              # ADRs, todos, project docs
├── .gitignore
├── <pkg manifest>                      # pyproject.toml / package.json / go.mod / …
├── <deploy manifest>                   # serverless.yml / template.yaml (SAM) / main.tf / wrangler.toml / vercel.json
│
├── handlers/                           # Function entrypoints — one file per handler
│   ├── http/                           # HTTP-triggered handlers (REST / GraphQL routes)
│   │   └── <verb>_<resource>.<ext>
│   ├── events/                         # Queue / topic / stream consumers
│   │   └── <event_name>.<ext>
│   └── scheduled/                      # Cron / timer triggers
│       └── <task_name>.<ext>
│
├── lib/                                # The testable core — business + infra logic
│   ├── services/                       # Use-case orchestrators called from handlers
│   ├── domain/                         # Pure types / models (no I/O)
│   ├── repositories/                   # Persistence adapters (DynamoDB / Firestore / SQL clients)
│   └── clients/                        # External API wrappers
│
├── shared/                             # Cross-cutting utilities (logging, validation, errors)
│
└── tests/                              # Unit + integration tests against `lib/` (handlers stay thin enough to cover via lib)
```

## Handler responsibilities

- **Parse + validate the platform event** (API Gateway request, SQS message, EventBridge payload, scheduled trigger). The handler unwraps the platform-specific shape; `lib/` services never see raw platform types.
- **Call exactly one `lib/` service.** A handler that orchestrates multiple services is doing the service's job — push the orchestration down.
- **Format the platform response.** Status codes, headers, error envelopes. Logging and tracing wrap the call.
- **No business rules in the handler.** If a sentence like "users on the free tier can do X" appears in a handler, it belongs in a `lib/` service.

## Why this matters

Serverless platforms make handlers easy to add and *hard* to test directly (cold starts, runtime mocks, IAM). Keeping handlers thin means business logic stays in plain functions you can unit-test in milliseconds; integration tests against the platform are reserved for the handler ↔ platform boundary.

## Dependency direction

```
handlers ──▶ lib/services ──▶ lib/domain
                │                ▲
                ├──▶ lib/repositories ──▶ (DB)
                └──▶ lib/clients ──▶ (external APIs)

shared ◀── (everyone — but no business logic in shared/)
```

- `handlers/` depend on `lib/` and `shared/`. Handlers do **not** import other handlers.
- `lib/services/` depend on `lib/domain`, `lib/repositories`, `lib/clients`, `shared/`. Services do **not** import handlers.
- `lib/domain` depends on nothing project-internal.
- `lib/repositories` and `lib/clients` depend on `lib/domain` (to implement protocols / return domain types) and `shared/`.

## The deploy manifest is part of the architecture

The deploy manifest (`serverless.yml` / SAM template / Terraform / `wrangler.toml` / `vercel.json`) is **as load-bearing as the code**. Treat changes to it as architectural — they belong in ADRs when the change introduces a new trigger type, IAM scope, runtime version, network topology, or cold-start-sensitive setting.

## What this rule does NOT cover

- **Platform choice** (AWS Lambda / GCP Cloud Functions / Cloudflare Workers / Vercel / Netlify / Azure Functions) — that's an ADR-level decision; capture in `.docs/adrs/`.
- **Local development story** (sam-local, serverless-offline, wrangler dev, miniflare) — document in `AGENTS.md` Run section.
- **State storage backend** (DynamoDB / Firestore / RDS / Postgres / KV) — ADR if it's load-bearing.
````

---

### Template: `.agents/rules/workflow-changes.md` *(opt-in, write only if `CHANGES`)*

````markdown
# Workflow: keeping product surfaces in sync

This rule supplements `workflow.md` for the subset of changes that affect the **product** rather than just the codebase. When you change something a user can see, the surfaces that describe that thing move with it — in the same commit, before the work is "done." The user shouldn't have to send a follow-up request to remember the docs.

## When this rule applies

Any change that alters something a user (free, paid, or trial) can experience or read. Typical triggers:

- A new capability — feature, command, public API endpoint, response field
- A change in behaviour the user can perceive (tier behaviour, defaults, included features)
- A new input source (file format, integration, platform)
- A new display surface (panel, page, tab, view)
- A change to the visible app shell (navigation, header, footer, key partials)
- A change to hero copy, brand positioning, or product framing
- A licence or policy change

The decision test, when in doubt: *would a customer reading the public-facing surfaces be misled if I skip the update?* If yes → apply the rule.

## When this rule does NOT apply

Changes a user can't experience:

- Internal refactors with no behavioral change
- Bug fixes that restore intended behaviour — the docs already describe what should happen
- Performance / observability / logging tweaks
- Test additions
- Config & env-var changes that don't shift user-visible defaults
- Workflow / rule file edits, ADR-only additions, prompt files
- Internal tooling (build scripts, CI, dependency bumps that don't surface as a feature)

## Surface map

Fill this table in as you discover surfaces. The starter set:

| Surface | What lives there, when to update |
| --- | --- |
| `README.md` | Project intro, tagline, models in the stack, contributing terms, licence framing. |
| `AGENTS.md` | Architecture map, conventions, response policy, copy guard-rails. |
| `LICENSE` | Actual licence text changes (rare). |
| Public docs / guide page | New capability documentation, examples, tier matrices. |
| Pricing / tiers page | Tier behaviour change, comparison-table cell, new tier feature. |
| App shell partials | Visible navigation, header, footer, key UI fragments. |
| Static assets | New visible CSS / JS that introduces behavior the change relies on. |

When the surface map needs a new row, add it in the same commit that introduces the surface.

## Same-commit rule

The doc updates ride in the **same commit** that lands the product change. Not "in a follow-up", not "after the PR ships." Two reasons:

1. Public surfaces never drift past one commit's lifetime.
2. Reviewers reading the diff can verify the docs match the code, in one place.

When a feature is gated behind a flag or rolled out internally only, hold the doc update until the flag flips for users — *publicly visible* is what triggers the update. Until then, the feature lives only in the relevant ADR and prompt file.

## Completeness expectation

Finishing a product-related change means walking the surface map (and any other user-readable files the change touches) before declaring the work done. The user shouldn't have to remind you that a public surface exists.

If a surface's ownership is unclear — multiple files describe it, or the change cuts across several — sweep all of them rather than guessing which is canonical.

## When you're not sure where the change should surface

Sometimes a change is genuinely new in shape — there's no existing carousel card, no matrix row, no hero line that maps. **Ask before inventing a new section, page, or surface category.** A new section on a public page (or worse, a new page) is an architectural decision that warrants an ADR, not a quiet addition. The right move is to surface the question:

> "This new feature doesn't fit any existing surface — should I propose a new section on `<page>` / a new page / extend the existing X category?"

Then proceed once the user picks. Inventing silently makes the surface map drift away from the team's mental model.

## Why this rule exists

Documentation drift is slow and silent. A feature shipped without its surfaces updated leaves the public guides subtly wrong: a user reading the guide and not seeing the feature assumes it doesn't exist; a user comparing tiers on the pricing page makes the wrong call from stale info; a partner reading the README forms a wrong picture of what the product currently is. Coupling the doc updates to the commit that introduces the change — and treating those updates as a non-optional part of "done" — keeps the public surfaces honest without requiring a separate follow-up step.
````

---

### Template: `.agents/rules/workflow-metrics.md` *(opt-in, write only if `METRICS`)*

````markdown
# Workflow: keeping the metrics surface honest

This rule supplements `workflow.md` for changes that touch the metering system — anywhere a metering counter is updated, a usage event is written, or a metrics-driven display reads from. The discipline exists because metrics drift silently: an event that no longer fires, a counter renamed but never updated downstream, a label growing in cardinality, a display that hasn't been told a new metric exists.

## Top-level rule

> **Adding, modifying, or removing a metered event means moving the four surfaces in lockstep — write site, durable read side, observability labels, display — plus updating a catalog at `.docs/metrics/README.md` AND a per-metric deep-dive at `.docs/metrics/<kebab-kind>.md`. All in the same commit. The cardinality discipline (no PII, no high-cardinality identifiers in labels) is non-negotiable and applies on every emit, not just new ones.**

## The four surfaces

Every metered event sits at the intersection of four surfaces. A change that touches any of them must consider the other three:

1. **Constant** — the canonical `kind` name (a string constant defined in one place in code so consumers import it instead of typing it).
2. **Call site** — where the meter is emitted. Always through a centralised meter helper (never a raw counter call) so the dual-write to ledger + observability is preserved.
3. **Catalog row + deep-dive** — `.docs/metrics/README.md` is the index; `.docs/metrics/<kebab-kind>.md` is the per-metric record of decisions (what counts as one event, what the bounded labels are *for*, what the metric does NOT measure, where it surfaces, caveats).
4. **Display** — wherever the metric is read (analytics endpoint, user-facing usage page, dashboard chart). Removing a metric without removing the display crashes the page; adding a metric without wiring the display means it's invisible.

## Cardinality discipline

Bounded labels only. Strip user identifiers from observability labels (the durable ledger row can keep `user_id` because it stores rows, not aggregates).

**Forbidden as bounded labels** (always — no exceptions):

- `user_id`, `chat_id`, `message_id`, any per-record UUID.
- `email`, `name`, `display_name`, `picture_url`, `phone`, IP addresses.
- User-supplied text content, filenames, prompts.
- Free-form upstream-system text (provider error strings, raw URLs, exception messages).
- Trace IDs, span IDs, request IDs, session tokens.

**Allowed as bounded labels** (small enumerable sets):

- Tier names, tool names, model names, source kinds, instrument modes, provider names.
- Booleans (`ok`, `cancelled`, `is_signup`).
- Discrete enum values you can list on a single line.

When in doubt, ask: *does this value have a bounded enumerable set?* If yes, allow. If it grows with users / time / events, forbid.

## Don't speculate

Three guardrails:

1. **Concrete signal first.** Add a metric when there's a question someone wants to answer. Empty dashboards are clutter.
2. **One axis at a time.** A single concept usually has one ledger axis. Don't double-emit two counters when one is unused.
3. **Per-user attribution earns its keep.** If a counter doesn't need per-user attribution, your observability auto-instrumentation already handles it. Reserve the dual-write path for things that will eventually feed quotas or per-user displays.

## Why this rule exists

The metering system has four surfaces that move independently — write side, durable read side, observability, display. Each is touched by different commits, often weeks apart. Without a rule that ties them together, drift is inevitable: a counter renamed at the write site keeps showing the old name on dashboards because the chart still reads the old `kind`; a new metric lands but the catalog doesn't, so the next contributor adds a duplicate counter for the same concept under a slightly different name; a label key sneaks in carrying user IDs because nobody re-read the cardinality rule.

Coupling the surfaces to one commit, locking the catalog as the canonical source, and treating the rule as load-bearing (not optional) keeps the metering surface honest.
````

---

### Template: `.agents/rules/workflow-testing.md` *(opt-in, write only if `TESTING`)*

````markdown
# Workflow: testing discipline

This rule is a companion to [`workflow.md`](./workflow.md). It defines **when** tests are required, **what** they should cover, **where** in the layering they should live, and **what** the agent must include in the commit that introduces or changes code.

The discipline is opinionated but not religious. The headline rule is short: **every artifact-producing change ships with the tests that prove the behaviour, in the same commit as the behaviour**. The rest of the file says what "the tests that prove the behaviour" actually means.

## When this rule applies

- Any new feature, public function, route, command, message handler, scheduled task, or worker.
- Any bug fix.
- Any refactor that changes observable behaviour at a layer boundary.
- Any change to a rule-encoded invariant (auth check, permission scope, cardinality limit, retry policy).

## When this rule does NOT apply

- Pure typo / wording fixes in docs, comments, or non-behavioural strings.
- Rename-only refactors with no behavioural change (function rename, file move, import reorder).
- Configuration edits with no logic change (linter config, editor config, gitignore, CI tweaks unrelated to test execution).
- Bootstrap / scaffolding commits that introduce empty placeholder modules with no real behaviour yet.

When unsure: write the test. The cost of an extra test is low; the cost of an untested regression is real.

## The pyramid (default shape, not a quota)

| Layer | Volume | What it covers | What it mocks |
| --- | --- | --- | --- |
| **Unit** | The bulk | Pure functions, single classes, domain logic, individual service methods, helpers. | Nothing internal. Mock only at the *boundary* of the unit (a clock, an HTTP client, a clock-like time source). |
| **Integration** | A meaningful minority | Real wiring across a meaningful boundary — a route handler calling a service calling a real (or test-double) repository against a real DB; a queue consumer end-to-end against a real broker; a CLI command exercised through its actual entrypoint. | External third-party APIs (HTTP, queues, model endpoints) via canned responses. The database, in-process side-effects, and your own modules are real. |
| **End-to-end** | A thin top | The happy-path of a user-facing flow: login → checkout, sign-up → first action, a CLI invocation that touches every layer. | The fewest mocks possible — usually none, or only third-party APIs the test environment can't reach. |

The pyramid is the default shape; particular projects (data pipelines, ML training code, infrastructure modules) have their own ratios. The rule is: bias towards the cheapest layer that meaningfully exercises the behaviour. **A unit test that mocks the database is exercising the mock, not the behaviour.** When you find yourself piling on mocks, move the test up the pyramid.

## Bug fixes: regression test first

For any bug fix:

1. **Write the failing test first.** Reproduce the bug at the lowest layer that surfaces it.
2. Confirm the test fails for the right reason (not a typo, not a missing import).
3. Apply the fix.
4. Confirm the test now passes and no other tests broke.
5. Commit the test and the fix together in the same commit.

A bug fix without a regression test is half a fix — the same bug will return the moment someone refactors that area. The test is the bug's tombstone.

## Mocking discipline: mock at boundaries, not internals

- **Mock at the system boundary.** External HTTP APIs, third-party SDKs, the model endpoint, the wall clock, randomness, the filesystem when it's incidental. These are non-deterministic, slow, or out of your control.
- **Don't mock your own code.** Mocking a service to test the route that calls it tests the mock, not the wiring. Use the real service against a test database, an in-memory adapter, or a fake that implements the protocol fully.
- **Don't mock to make a test easier.** If a unit needs five mocks to be testable, the unit is doing too much. Split it before you write the test.
- **Prefer fakes to mocks.** A fake repository that holds state in a dict is more readable, more reusable, and catches more real bugs than a mock that records calls.
- **Avoid snapshot tests for behavioural code.** Snapshots are useful for UI rendering and CLI output where the shape is the contract; they're a trap for business logic where they ossify the *current* output without asserting the *intended* one.

## Naming, structure, and signal

- Name tests by **behaviour, not implementation**: `returns_403_when_viewer_is_not_owner`, not `test_check_owner`. The name should read as a sentence describing the contract.
- One assertion *concept* per test. A test can make multiple `assert` calls if they prove the same concept; if they prove two unrelated things, split them.
- Arrange / act / assert sections are visually separated (blank line, comment, or whitespace).
- Tests are independent and order-independent. No shared mutable state between tests. If two tests share setup, lift it to a fixture, not to a class attribute.
- Test files live alongside the code they cover unless the language ecosystem dictates otherwise — `tests/` directory for Python/Rust (per `pytest` / `cargo test` conventions), `*.test.ts` co-located for TypeScript, `*_test.go` co-located for Go.

## TDD: encouraged, not mandated

Test-Driven Development — *red, green, refactor* — is the recommended default for non-trivial behaviour. It forces the contract to be designed before the implementation, catches over-engineering early, and produces tests that genuinely cover the behaviour because they were written before the code that satisfies them existed.

That said, TDD is a *practice*, not a rule. Some changes (small bug fixes, mechanical refactors, exploratory spikes) don't benefit from it; some teams aren't on board with it; some moments don't allow the discipline. **The hard rule is: every change ships with its tests in the same commit.** Whether you wrote the test first or second is your call — but the commit must contain both.

When TDD genuinely helps: new public API design, new use-case orchestration, anything where you're not sure what the contract should look like yet, anything where the implementation is non-trivial and you want to confirm the contract before locking yourself in.

When TDD genuinely doesn't: trivial helpers, configuration plumbing, generated code, exploratory spikes you'll throw away.

## Coverage: track, don't gate

- Run coverage tooling locally and in CI. **Report it; don't gate on a percentage.** Hard percentage gates incentivise the wrong behaviour — gaming the metric with assertion-free tests, or skipping a useful test because it doesn't move the number.
- The right question is "does this commit's diff have tests for its behaviour?" — answered by reading the diff, not by reading a percentage. A change that adds 200 lines of behaviour and 0 tests fails the review regardless of project-level coverage.
- Coverage **drops** in a PR are a useful signal. If overall coverage went down because new code lacks tests, that's a question worth asking in review. If it went down because dead code was deleted, that's progress.
- For long-lived projects, watching the *trend* of coverage matters more than the absolute number. Sustained downward trend means the discipline is slipping; sustained upward trend means the project is hardening.

## Flaky tests

A flaky test is a broken test — it just hasn't decided which failure mode it prefers yet. Treat them as P1:

- **First flake**: investigate the same day. Time / order / race / network non-determinism. Fix the underlying cause.
- **Can't fix immediately**: quarantine (skip with a clear `Flaky: <reason>` annotation) and file a `.docs/todos/<ts>.<slug>.md` entry per `workflow-todos.md` so the quarantine is visible and dated.
- **Never** disable a flaky test silently. A skipped flake with no entry is technical debt that compounds.

## Test data and fixtures

- **Builders / factories over fixtures of fixed data.** A `make_user(role="admin")` helper that takes overrides is more readable and more maintainable than dozens of fixture files.
- **No real PII or secrets in test data.** Use obviously fake values (`user@example.com`, `password-for-test`). Never copy production data into a test file.
- **Time and randomness pinned.** Inject a clock and a seeded RNG so tests are deterministic. If a test depends on the real clock or `random`, it will fail on Tuesdays at 3am six months from now.

## What goes in the commit

Per `workflow.md`, every artifact-producing request bundles its prompt, ADR (if applicable), telemetry, security pass, and code into one commit. With this rule installed, the same commit also bundles:

- **The new / updated tests** that cover the change.
- **Any test infrastructure** needed by those tests (a new fixture, a new factory, a new fake adapter).
- **Any test-data updates** for cases the change touches.

If the agent commits code without tests when this rule applies, the commit is incomplete — push back and fix it before moving on.

## Cross-references

- **Security findings** (per `workflow-security.md`): every finding's fix must include a regression test that proves the vulnerability is closed and won't return. That test is part of the same commit as the fix.
- **Bug fixes** triggered by a `.docs/todos/` entry: the regression test lives in the commit that closes the entry.
- **Metering changes** (per `workflow-metrics.md`, if installed): tests cover the catalog entry, the emit site, and the read side — at integration level where they actually exercise the wiring.
- **Product-surface changes** (per `workflow-changes.md`, if installed): the test layer that matches the surface — UI components → component tests, public API → contract tests, docs → link / build checks.

## Why this rule exists

Tests are a memory aid for the project's intended behaviour. Without them, every refactor is a roll of the dice and every bug fix is a hope. With them, the contract is enforced by code that runs on every commit; future agents and humans can change the implementation without breaking the behaviour, because the tests catch them when they do.

The cost of writing the test now is small. The cost of *not* writing it — the production incident, the customer impact, the cold-debug at midnight — is large and lumpy. This rule trades a known small cost for an unknown but eventually large one.
````

---

### Template: `.agents/rules/ui-components.md` *(opt-in, write only if `UI_COMPONENTS`)*

````markdown
# UI Components

A catalog of canonical UI affordances in this codebase. Before adding a new button, dropdown, card, status badge, or any other reusable bit, check this list. If the affordance is here, **clone the shape from the canonical file**, don't invent a one-off variant inline. If it isn't here, propose adding a row explicitly so the catalog grows intentionally.

This rule exists because consistency drift is the kind of thing that gets flagged on every other UI commit ("please match the dropdown style", "please use the same card", …). The pattern map should answer those questions before the user asks them.

## Top-level rule

> **Before adding a UI affordance, check the catalog below. If a canonical shape exists, clone the implementation file referenced — same classes, same DOM structure, same colour treatment. If it doesn't exist yet, surface that explicitly ("there's no canonical X — proposing this shape, happy to adjust") and add a row to the catalog when the pattern lands.**

## The catalog

Each entry should name:

- **Canonical** — the file (or files) where the shape lives. Multiple canonical files is fine when the pattern has variants.
- **Shape** — the actual classes, DOM structure, colour treatment. Summarise inline; always read the canonical file for the exact set.
- **Anti-rules** — variants to avoid, common mistakes, parent caveats.

Grow the catalog organically. Start by adding rows for the affordances the project introduces in its first few weeks (buttons, dropdowns, cards, modals, toggles, form fields, status pills, banners). When you discover the project needs an affordance and you can't find it here, add it.

### Example entry shape

```
### Primary button

- **Canonical**: `<path/to/canonical/file>`.
- **Shape**: `<the full class string or component reference>`.
- **When to use**: the primary action on a surface — the one we want the user to click. At most one per visible surface.
- **Anti-rule**: don't use this for destructive actions; clone the destructive button entry instead.
```

## When to introduce a new pattern

Three triggers:

1. **The catalog doesn't fit.** A new affordance is genuinely different from anything listed. Surface it: *"There's no canonical pattern for X — proposing this shape, here's the file. Happy to adjust before I clone it elsewhere."* Then add the row.
2. **An existing pattern is being deliberately superseded.** A new component replaces an old one. Update the catalog row pointing at the new canonical file; mark the old file as deprecated in a code comment if it sticks around for backward-compat.
3. **A pattern's classes drift.** If the actual canonical file's classes have changed since the catalog was written, the catalog is wrong — fix the catalog rather than the file. Source of truth is the file; the catalog is a pointer.

Adding a row mid-commit is the right move when the work introduces the pattern. Don't defer it to "later" or the next reminder loop returns.
````

---

### Template: `.docs/adrs/README.md`

````markdown
# Architecture Decision Records

This directory holds the [Architecture Decision Records (ADRs)](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) for the project. Each ADR is a short markdown file capturing one structural decision: the context that prompted it, what was decided, and the consequences. Read these before making structural changes.

## Index

| # | Title | Status | Date |
| --- | --- | --- | --- |
| [0000](./0000-adr-template.md) | ADR Template (do not cite) | Template | — |

(Append new ADRs as `NNNN-<kebab-slug>.md` and add a row here in the same commit. See `.agents/rules/workflow.md` for when an ADR is required.)
````

---

### Template: `.docs/adrs/0000-adr-template.md`

````markdown
# 0. ADR Template

- **Status**: Template (not a real decision; do not cite)
- **Date**: —

## Context

What is the situation prompting this decision? What constraints, requirements, or trade-offs are in play? Keep this to a paragraph; cite related ADRs by number where they constrain or motivate this one.

## Decision

What did we decide? State it plainly. Include a Mermaid diagram if the change reshapes more than two collaborators or introduces a multi-step flow.

```mermaid
graph LR
  A --> B
  B --> C
```

## Consequences

What follows from this — both positive and negative. Bulleted list works well:

- Positive consequence one.
- Positive consequence two.
- Cost or trade-off accepted.
- Deferred follow-up (capture under `.docs/todos/` if actionable).

Cross-link to related ADRs by number.
````

---

### Template: `.docs/todos/README.md`

````markdown
# Do-Later Ideas

This directory holds the project's deferred ideas — features the agent (or the user) suggested but didn't ship in the moment, follow-ups noted in commit messages or ADR consequence sections, scope cuts surfaced during implementation.

The discipline for managing this directory is documented in `.agents/rules/workflow-todos.md`. The short version:

- **One file per idea**, named `<kebab-case-slug>.md`. Flat — no subdirectories.
- **Shape**: title + Area + Refs + Context (3–5+ sentences) + Deferred because + Revisit when.
- **Add proactively** when the user defers something.
- **Sweep on every commit** for entries the change satisfies; `git rm` to remove (no archive — git log is canonical).

`ls .docs/todos/` is the index — files are individually-addressable artifacts.
````

---

### Template: `.docs/security/methodology.md`

````markdown
# Security Review — Methodology

This is the playbook for security reviews of this project. It defines the frameworks used, the order in which the codebase is walked, the severity rubric applied to findings, and the "best practice" checklist behind each check. It is intentionally evergreen: it should change only when the *approach* changes, not when a finding lands or gets fixed.

Each individual audit lives in its own dated sibling file (`.docs/security/<YYYY-MM-DD>-<slug>.md`). Audit files cite this document for definitions and rubric so the findings can stay tight. The companion rule `.agents/rules/workflow-security.md` says *when* to consult this doc — both per-request (rubric pass on security-sensitive commits) and on cadence (full audits).

---

## 1. Audience and reason

This document has two audiences:

- **A future reviewer (human or agent)** running the next audit — to repeat the same approach without reinventing the rubric or the scope.
- **Any contributor adding a feature** — to run their change against the same checklist before opening the PR. The rubric in §5 is meant to be a usable pre-commit aid, not just a post-hoc taxonomy.

Findings, recommendations, and "what's currently shipped" all belong in the dated audit files, not here. This document doesn't change when the codebase ships a fix.

---

## 2. Frameworks

### 2.1 OWASP Top 10 (2021)

The [OWASP Top 10](https://owasp.org/Top10/) is a community-consensus list of the ten categories that produce the majority of web-application breaches. Each category represents a *class* of bug, not a single vulnerability — e.g. "Broken Access Control" covers IDOR, missing authorisation, privilege escalation, JWT-confusion, path traversal, and forced browsing under one heading. The 2021 revision is the current published list at time of writing; categories from earlier revisions (XSS, deserialisation, etc.) were rolled into broader buckets.

Even for projects that aren't classical web apps (CLIs, libraries, data pipelines), several OWASP categories apply directly: A02 (Cryptographic Failures), A06 (Vulnerable & Outdated Components), A08 (Software & Data Integrity Failures), A09 (Security Logging & Monitoring Failures). Treat the list as a starter taxonomy and let the rubric in §5 select what's load-bearing for your project.

| Category | What it covers |
| --- | --- |
| A01 Broken Access Control | IDOR, missing authorisation, path traversal, privilege escalation, forced browsing. |
| A02 Cryptographic Failures | TLS, cookie flags, secret storage, weak hashing, insecure RNG. |
| A03 Injection | SQL, NoSQL, OS command, LDAP, template, expression-language injection. |
| A04 Insecure Design | Missing rate limits, missing quotas, missing trust boundaries, threat-model gaps. |
| A05 Security Misconfiguration | Missing security headers, default creds, verbose errors, unnecessary features enabled. |
| A06 Vulnerable & Outdated Components | Known-CVE deps, unpinned versions, end-of-life libraries. |
| A07 Identification & Authentication Failures | Weak login, session fixation, credential stuffing, missing MFA. |
| A08 Software & Data Integrity Failures | Unverified updates, missing SRI on CDN scripts, signed-artifact gaps. |
| A09 Security Logging & Monitoring Failures | Missing audit logs, secrets in logs, no alerting. |
| A10 Server-Side Request Forgery (SSRF) | Server fetches a URL the attacker controls. |

{{IF_LLM}}### 2.2 OWASP Top 10 for LLM Applications (2025)
{{IF_LLM}}
{{IF_LLM}}The [OWASP LLM Top 10](https://genai.owasp.org/llm-top-10/) is the AI-specific complement, published by the OWASP Generative AI security project. It covers risks that don't surface in classical web-app reviews because they emerge only when an LLM is in the request path: the model has *its own* attack surface (prompt injection), *its own* output channel (improperly handled markdown / actions), and *its own* supply chain (model weights, model providers, model fine-tunes).
{{IF_LLM}}
{{IF_LLM}}| Category | What it covers |
{{IF_LLM}}| --- | --- |
{{IF_LLM}}| LLM01 Prompt Injection | Untrusted text in the prompt or tool outputs steering the model. |
{{IF_LLM}}| LLM02 Sensitive Info Disclosure | Model leaks secrets / training data / system prompt / cross-user data. |
{{IF_LLM}}| LLM03 Supply Chain | Compromised model weights, dataset poisoning, malicious adapters / `trust_remote_code`. |
{{IF_LLM}}| LLM04 Data & Model Poisoning | Training-time or feedback-loop attacks. |
{{IF_LLM}}| LLM05 Improper Output Handling | Model output rendered to HTML, executed as code, or interpolated into shell / SQL. |
{{IF_LLM}}| LLM06 Excessive Agency | Tools that can take destructive actions; agent loop with too much authority. |
{{IF_LLM}}| LLM07 System Prompt Leakage | System prompt contains secrets or sensitive guidance. |
{{IF_LLM}}| LLM08 Vector & Embedding Weaknesses | RAG cross-tenant leaks, embedding inversion, embedding-injection. |
{{IF_LLM}}| LLM09 Misinformation | Hallucination / over-reliance / unsupported assertions. |
{{IF_LLM}}| LLM10 Unbounded Consumption | Cost / GPU / memory exhaustion via large prompts, long generations, abusive loops. |
{{IF_LLM}}
{{IF_LLM}}### 2.3 Why both lists, not just one
{{IF_LLM}}
{{IF_LLM}}A web-app-only review of an AI product misses LLM01 (prompt injection of tool outputs) and LLM06 (agent agency) entirely — the actual *novel* risks. An LLM-only review of a web app misses A01 (owner-scoping), A05 (security headers), A07 (OAuth flow correctness) — the *boring-but-load-bearing* risks. The two lists overlap (LLM03 supply-chain ≈ A06, LLM05 improper output ≈ A03 injection / A09 logging) but each catches distinct things. Running both is the standard for an AI-bearing web app.

---

## 3. Review approach

The audit is a **static, read-only** review:

- All evidence comes from reading source files, configuration, dependency manifests, and ADRs.
- No live HTTP requests, no fuzzing, no exploitation, no port scan.
- No code modifications, no patches.

This bounds the audit's reach (we may miss runtime-only issues — race conditions, TLS misconfiguration on the deployed instance, etc.) but keeps the cost low and the result reproducible: anyone can re-read the same files and reach the same conclusion.

The order in which the codebase is walked is deliberate. **Auth and access control come first** because every other finding's severity depends on the trust boundary they establish — an "injection in a service" is severe if any user can reach the service, mild if only an admin can. After auth, walk inputs (uploads, query strings, form bodies), then persistence (SQL hygiene, owner-scoping enforcement), then output (templating, output encoding), then transport (headers, cookies, CORS), then dependency hygiene, then logging.{{IF_LLM}} **The LLM surface is reviewed last** because its threats only make sense once the rest of the trust model is mapped.

---

## 4. Severity scale

The five-level scale is explicit so that prioritisation isn't subjective:

| Level | Meaning |
| --- | --- |
| **Critical** | Exploitable now, leads to compromise / data loss / takeover. |
| **High** | Exploitable with a small precondition (specific user state, specific tier). |
| **Medium** | Defence-in-depth gap; combined with another bug, becomes exploitable. |
| **Low** | Hardening recommendation; no plausible exploit path today. |
| **Info** | Positive observation, context, or N/A. Included to make absences explicit. |

Every category produces *something* — at minimum an `[Info]` note saying "no findings — appears mitigated". Silence is ambiguous; an explicit `[Info]` lets the next audit see whether a check was performed and skipped vs. forgotten.

---

## 5. What "best practice" looks like — the rubric

This is the rubric the audit is *looking for*. A contributor adding a feature can run their change against the matching sub-section before opening a PR. Sub-section numbers are stable (aligned to OWASP categories); if a section doesn't apply to your project, leave the gap rather than renumbering.

{{IF_WEB}}### 5.1 Authentication & sessions
{{IF_WEB}}
{{IF_WEB}}- OAuth `state` parameter is generated with a cryptographically secure RNG.
{{IF_WEB}}- `state` comparison uses constant-time compare to defeat timing attacks.
{{IF_WEB}}- PKCE is used on the OAuth handshake when feasible (RFC 9700).
{{IF_WEB}}- Session secret comes from the environment, not a default; production fails-closed if missing.
{{IF_WEB}}- Session cookie carries `Secure`, `HttpOnly`, and `SameSite=Lax` (or stricter) flags.
{{IF_WEB}}- Cookie payload is signed (or encrypted), not just base64-encoded.
{{IF_WEB}}- Cookie payload contains the minimum (a user ID, not tokens, not email).
{{IF_WEB}}- Logout clears the session server-side.
{{IF_WEB}}- `email_verified` is checked on the IdP userinfo response before account-create / -merge.
{{IF_WEB}}- Identity protocol bugs: open redirect on `next=`, host-header injection on `redirect_uri`, replay on `state`.
{{IF_WEB}}
{{IF_WEB}}### 5.2 Access control / authorisation
{{IF_WEB}}
{{IF_WEB}}- Every request that reads or writes a resource filters by the requesting user's ID at the lowest possible layer (the repository).
{{IF_WEB}}- "Wrong owner" returns the same shape as "not found" (no oracle).
{{IF_WEB}}- Cross-user inputs (resource IDs, document IDs, message IDs) are looked up *with* the owner constraint, not validated *after* the lookup.
{{IF_WEB}}- Privilege escalations are gated behind a real authority check, not a self-service form.
{{IF_WEB}}- Path-traversal defences on storage keys: resolve, then assert the resolved path stays within the per-user prefix.

### 5.3 Input validation

- Inputs are validated at the boundary (the route handler, CLI parser, or service public method), not deep inside.
- Validation rejects rather than coerces — explicit allow-lists over deny-lists.
- File uploads have a byte-size cap enforced *before* the body is read into memory.
- File uploads have a content-type / magic-byte check, not just an extension check.
- URLs from users are parsed and host-allow-listed before any outbound request.
- Free-form strings have a length cap that protects downstream tokenisers / parsers from quadratic blow-up.

{{IF_WEB}}### 5.4 SQL and data layer
{{IF_WEB}}
{{IF_WEB}}- All SQL parameters use placeholders (`%s` for psycopg, `?` for sqlite, named binds for SQLAlchemy / ORMs). No `f"..."` or `%` of user input into SQL.
{{IF_WEB}}- Migrations don't take user input; if they ever do, they must use the same parameterisation discipline.
{{IF_WEB}}- Connection strings are not logged in full (passwords stripped via `urlparse`-then-rebuild).
{{IF_WEB}}- Connection pool has a sane `max_size` so a request burst can't open thousands of sockets.
{{IF_WEB}}
{{IF_WEB}}### 5.5 Output encoding / templating
{{IF_WEB}}
{{IF_WEB}}- Templating engine has autoescape on by default for HTML templates (Jinja `autoescape=True`, React JSX, etc.).
{{IF_WEB}}- Trust-escape escape hatches (`|safe`, `Markup(...)`, `dangerouslySetInnerHTML`) are audited — every use is justified.
{{IF_WEB}}- Markdown rendering is followed by an HTML sanitiser (DOMPurify, bleach) before insertion into the DOM.
{{IF_WEB}}- User content is never interpolated into `<script>` blocks, `javascript:` URLs, or `data:` URLs.
{{IF_LLM}}{{IF_WEB}}- Agent-generated output is treated like user content for the purposes of sanitisation.
{{IF_WEB}}
{{IF_WEB}}### 5.6 HTTP transport / browser-side
{{IF_WEB}}
{{IF_WEB}}- `Content-Security-Policy` is set, scoped tightly, and includes `script-src` with explicit origins.
{{IF_WEB}}- `Strict-Transport-Security` is set with at least `max-age=31536000`.
{{IF_WEB}}- `X-Content-Type-Options: nosniff` is set.
{{IF_WEB}}- `X-Frame-Options: DENY` (or CSP `frame-ancestors 'none'`) is set if no embedding is intended.
{{IF_WEB}}- `Referrer-Policy: strict-origin-when-cross-origin` (or stricter) is set.
{{IF_WEB}}- `TrustedHostMiddleware` (or framework equivalent) is configured with the production hostnames.
{{IF_WEB}}- CSRF is mitigated either by SameSite=Lax/Strict cookies + same-origin checks, or by explicit token.
{{IF_WEB}}- All third-party scripts loaded from CDNs carry an `integrity="sha384-..."` Subresource Integrity attribute and a pinned version.

### 5.7 Secrets and configuration

- Secrets come from environment variables, never from committed files.
- `.env.example` is committed; `.env` is gitignored.
- Default secrets in `.env.example` are clearly labelled "rotate before deploy".
- Secrets are not logged — not at INFO, not at DEBUG, not in exception traces.
- Boot-time configuration prints non-sensitive summaries (`backend=postgres pool_size=10`), not the connection string.

### 5.8 Logging and monitoring

- Structured logging via a per-module logger.
- Event names are static lowercase dotted paths (`subsystem.action.outcome`); variable data goes in the structured payload.
- Levels match the signal: DEBUG for diagnostics, INFO for routine ops, WARNING for recoverable anomalies, ERROR for "operator should investigate", CRITICAL for unrecoverable / wake-someone events.
- Sensitive fields (passwords, tokens, OAuth codes, full request bodies, full message content, IPs, full email addresses) never appear in structured payloads. When *presence* matters, log a boolean (`token_present`).
- For SDK exceptions whose messages may echo caller-supplied secrets (e.g. botocore on bad keys), log the canonical short error code, not `str(exc)`.

### 5.9 Rate limiting and resource caps

- Per-actor rate limits on expensive endpoints / commands, keyed on the authenticated identity.
- Per-IP rate limits on unauthenticated endpoints (login, signup, public APIs).
- A bounded concurrency cap per actor on long-running operations (e.g. one in-flight inference per user).
{{IF_LLM}}- Bounded `max_new_tokens` / generation budgets on every model call.
{{IF_LLM}}- Bounded loop iterations on agent loops; a hard cap so a misbehaving model can't spin forever.
- Decode caps (audio duration, image pixel count, document size) enforced *before* the heavyweight library does the work.

### 5.10 Dependency hygiene

- Lockfile (`uv.lock`, `poetry.lock`, `package-lock.json`, `go.sum`, etc.) is committed.
- High-risk deps have lower-bound pins in the manifest (so an automated upgrade doesn't silently regress).
- A CVE scanner (`pip-audit`, `safety`, `npm audit`, GitHub Dependabot) runs in CI and fails the build on critical advisories.
- High-velocity deps are watched; "watch" means the team gets a signal when they ship a security release.

{{IF_LLM}}### 5.11 LLM-specific practices
{{IF_LLM}}
{{IF_LLM}}- Tool outputs that flow into the model context are wrapped in delimiters and explicitly framed as untrusted in the system prompt.
{{IF_LLM}}- The system prompt contains no secrets, no per-user data, no DB rows, no internal endpoints.
{{IF_LLM}}- Tools have *narrow capabilities*: a tool that reads data cannot also write files or call the network; tools cannot mutate state outside their declared output channel.
{{IF_LLM}}- The agent loop has a hard iteration cap.
{{IF_LLM}}- Model loaders (`from_pretrained(..., revision="<sha>")` for HF Hub, equivalent for other registries) pin to a specific commit / version.
{{IF_LLM}}- `trust_remote_code=True` (or equivalent code-execution-on-load flags) is **never** set unless the model is owned by the team.
{{IF_LLM}}- Multi-turn history filters or sanitises previous assistant messages before re-feeding them, so a malicious "prior assistant" can't seed instructions.
{{IF_LLM}}- Cost / token budgets per actor, per-tier.

---

## 6. Glossary

Short definitions for the acronyms and jargon used in audits that follow this playbook.

{{IF_WEB}}| Term | Definition |
{{IF_WEB}}| --- | --- |
{{IF_WEB}}| **CSP** | Content-Security-Policy — HTTP header that whitelists the origins from which scripts / styles / media may load. The single most effective browser-side mitigation against XSS. |
{{IF_WEB}}| **HSTS** | HTTP Strict Transport Security — header instructing browsers to refuse HTTP for the host for `max-age` seconds. Closes downgrade attacks. |
{{IF_WEB}}| **SRI** | Subresource Integrity — `integrity="sha384-..."` on a `<script>` or `<link>` tag; the browser refuses to run the asset if its hash doesn't match. Defends against CDN compromise. |
{{IF_WEB}}| **CSRF** | Cross-Site Request Forgery — an attacker site induces the victim's browser to issue an authenticated request. Mitigated by SameSite cookies, origin checks, or anti-CSRF tokens. |
{{IF_WEB}}| **IDOR** | Insecure Direct Object Reference — server returns a record because the *ID* is valid, not because the *requester* is authorised. |
{{IF_WEB}}| **SSRF** | Server-Side Request Forgery — server makes an outbound HTTP request to a URL the attacker controls; used to exfiltrate cloud-metadata or pivot into internal networks. |
{{IF_WEB}}| **PKCE** | Proof Key for Code Exchange (RFC 7636) — extension to OAuth that binds a code-grant to a one-time client secret, defending against code-interception. |
{{IF_WEB}}| **JWT** | JSON Web Token — signed, base64-encoded JSON used as an opaque session token. Common confusion: claim verification ≠ signature verification. |
{{IF_WEB}}| **TLS** | Transport Layer Security — the protocol "underneath HTTPS". |
{{IF_WEB}}| **Owner-scoping** | The practice of filtering reads/writes by the requesting user's ID at the data layer, so a wrong owner gets the same response as a missing record. |

| Term | Definition |
| --- | --- |
| **RNG** | Random Number Generator. "Cryptographically secure RNG" = `secrets` / `os.urandom`, not `random.random()`. |
| **Constant-time compare** | A comparison that takes the same time regardless of where the inputs differ, to defeat timing oracles (`secrets.compare_digest` in Python). |
| **Rate limit** | A cap on how many requests a single client (user / IP / session) may make per unit time. Defends against brute force and resource exhaustion. |
| **Defence in depth** | The principle that no single mitigation should be load-bearing. Output encoding doesn't replace input validation; rate limits don't replace auth — each is a layer. |

{{IF_LLM}}| Term | Definition |
{{IF_LLM}}| --- | --- |
{{IF_LLM}}| **Prompt injection** | LLM-specific injection: untrusted text reaches the model's context and steers it (e.g. tool output telling the model to ignore the system prompt). |
{{IF_LLM}}| **Excessive agency** | An LLM agent that can take destructive or far-reaching actions (delete files, send emails, transfer money) without a human confirmation step. The risk grows with the breadth of the tools. |
{{IF_LLM}}| **System prompt leakage** | The LLM is induced to output its system prompt, exposing sensitive guidance or secrets that shouldn't have been there in the first place. |
{{IF_LLM}}| **Vector / embedding weakness** | RAG-specific: cross-tenant data leaks, embedding inversion, or embeddings that index attacker-poisoned content. |
{{IF_LLM}}| **Unbounded consumption** | LLM-specific cost / GPU / memory exhaustion via large prompts, long generations, or abusive loops. |

---

## 7. How to run a security review

1. Walk the categories in the order defined in §3.
2. For each category, grep / read the matching files and capture findings as `(severity, file:line, what, risk, recommendation)`.
3. Assign severity per the rubric in §4.
4. Capture an `[Info]` note for every category with no findings, so absences are explicit.
5. Save the audit as a sibling file under `.docs/security/<YYYY-MM-DD>-<slug>.md`. Each audit is a snapshot in time; previous audits stay where they were so the diff between them is the story.
6. The audit file itself should carry: scope + date, executive summary, per-category findings, prioritised recommendation list (highest risk reduction per hour, first), and an explicit "out of scope" section. It should *not* re-state the framework descriptions, the severity rubric, the rubric of best practices, or the glossary — those live here.
7. If a finding becomes load-bearing for the project's shape (e.g. introduces a new mitigation pattern future code is expected to follow), promote the consequence to an ADR under `.docs/adrs/`.

A re-run of the audit after the prioritised recommendations from the previous audit ship should produce a noticeably shorter `[High]` list — that's the signal the previous audit caught real risk, not just style. The re-run produces a new sibling file; the previous audit is left alone.
````

---

### Template: `.gitignore` — variant for `LANG=Python`

````gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class
*.so

# Distribution / packaging
build/
dist/
*.egg-info/
*.egg
wheels/
*.whl

# Virtual environments
.venv/
venv/
ENV/
env/

# Test / coverage
.pytest_cache/
.tox/
.coverage
.coverage.*
htmlcov/
coverage.xml
*.cover
.hypothesis/

# Type checkers
.mypy_cache/
.pyright/
.pytype/

# Linters
.ruff_cache/

# Jupyter
.ipynb_checkpoints/

# Environment / secrets
.env
.env.*
!.env.example

# Editor / IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Claude Code per-machine settings (personal allowlist / WebFetch domains / etc.)
.claude/settings.local.json

# OS
.DS_Store
Thumbs.db
````

---

### Template: `.gitignore` — variant for `LANG=TypeScript/Node`

````gitignore
# Dependencies
node_modules/
.pnpm-store/
.yarn/

# Build output
dist/
build/
out/
.next/
.nuxt/
.svelte-kit/
.vite/
.turbo/

# Tests / coverage
coverage/
.nyc_output/

# TypeScript
*.tsbuildinfo

# Environment / secrets
.env
.env.*
!.env.example

# Logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
*.log

# Editor / IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Claude Code per-machine settings (personal allowlist / WebFetch domains / etc.)
.claude/settings.local.json

# OS
.DS_Store
Thumbs.db
````

---

### Template: `.gitignore` — variant for `LANG=Go`

````gitignore
# Binaries
*.exe
*.exe~
*.dll
*.so
*.dylib
bin/

# Test binary, built with `go test -c`
*.test

# Output of `go test -coverprofile`
*.out
coverage.txt

# Dependency directory (vendor mode)
vendor/

# Environment / secrets
.env
.env.*
!.env.example

# Editor / IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Claude Code per-machine settings (personal allowlist / WebFetch domains / etc.)
.claude/settings.local.json

# OS
.DS_Store
Thumbs.db
````

---

### Template: `.gitignore` — variant for `LANG=Rust`

````gitignore
# Generated by Cargo
target/
**/*.rs.bk

# Lockfile is typically committed for binaries, not for libraries — adjust as needed
# Cargo.lock

# Coverage
*.profraw
*.profdata

# Environment / secrets
.env
.env.*
!.env.example

# Editor / IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Claude Code per-machine settings (personal allowlist / WebFetch domains / etc.)
.claude/settings.local.json

# OS
.DS_Store
Thumbs.db
````

---

### Template: `.gitignore` — fallback variant for any other `LANG`

````gitignore
# Environment / secrets
.env
.env.*
!.env.example

# Build / artifacts (extend per language)
build/
dist/
out/
target/

# Logs
*.log

# Editor / IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Claude Code per-machine settings (personal allowlist / WebFetch domains / etc.)
.claude/settings.local.json

# OS
.DS_Store
Thumbs.db
````

---

### Template: `.env.example` *(opt-in, write only if `ENV_VARS`)*

````sh
# Environment variables for {{PROJECT_NAME}}.
#
# Copy this file to `.env` (gitignored) and fill in real values before running.
# Default values here are placeholders — rotate before any non-local deploy.
#
# `methodology.md §5.7` documents the secrets discipline this file participates in.

# --- Application ---
# APP_ENV=development
# APP_PORT=8000

# --- Persistence ---
# DATABASE_URL=postgres://user:password@localhost:5432/{{PROJECT_NAME}}
# REDIS_URL=redis://localhost:6379/0

# --- Auth (if applicable) ---
# SESSION_SECRET=change-me-before-deploy
# OAUTH_CLIENT_ID=
# OAUTH_CLIENT_SECRET=

# --- External services (add as needed) ---
````

---

### Template: `.editorconfig`

````editorconfig
# editorconfig.org — consistent indentation, line endings, charset across editors.
root = true

[*]
charset = utf-8
end_of_line = lf
indent_style = space
indent_size = 4
insert_final_newline = true
trim_trailing_whitespace = true

[*.{js,jsx,ts,tsx,json,yml,yaml,html,css,scss,md}]
indent_size = 2

[*.{go,py,rs}]
indent_size = 4

[Makefile]
indent_style = tab

[*.md]
trim_trailing_whitespace = false
````

---

### Template: `README.md`

````markdown
# {{PROJECT_NAME}}

{{ONE_LINE_PURPOSE}}

## Quick start

{{RUN_INSTRUCTIONS}}

## Documentation

- **For contributors and agents**: read [`AGENTS.md`](./AGENTS.md) — the cold-start brief covering architecture, conventions, and the rules under [`.agents/rules/`](./.agents/rules/). Per-tool adapters (e.g. `CLAUDE.md`, `.cursor/rules/`, `.aider.conf.yml`) all point back to it.
- **Architecture decisions**: see [`.docs/adrs/`](./.docs/adrs/) for the trade-offs behind structural choices.
- **Security**: the rubric and methodology live at [`.docs/security/methodology.md`](./.docs/security/methodology.md). Dated audits are sibling files.

{{IF_CONTRIB}}## Contributing
{{IF_CONTRIB}}
{{IF_CONTRIB}}See [`CONTRIBUTING.md`](./CONTRIBUTING.md).

## License

{{IF_LICENSE_MIT}}MIT — see [`LICENSE`](./LICENSE).
{{IF_LICENSE_APACHE_2_0}}Apache 2.0 — see [`LICENSE`](./LICENSE).
{{IF_LICENSE_PROPRIETARY}}Proprietary. All rights reserved. See [`LICENSE`](./LICENSE).
{{IF_LICENSE_SKIP}}No license declared yet. Contact the maintainers before reusing this code.
````

---

### Template: `LICENSE` — variant for `LICENSE=MIT`

````text
MIT License

Copyright (c) {{CURRENT_YEAR}} {{COPYRIGHT_HOLDER}}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
````

The agent fills `{{CURRENT_YEAR}}` from `date +%Y` and asks the user for `{{COPYRIGHT_HOLDER}}` (name or organisation) before writing.

---

### Template: `LICENSE` — variant for `LICENSE=APACHE_2_0`

Write the file with the populated header (using `{{CURRENT_YEAR}}` from `date +%Y` and `{{COPYRIGHT_HOLDER}}` from the Q13 follow-up prompt) followed by the canonical Apache 2.0 license text verbatim. The full file:

````text
Copyright {{CURRENT_YEAR}} {{COPYRIGHT_HOLDER}}

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

----

                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted"
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is conspicuously marked or otherwise
      designated in writing by the copyright owner as "Not a Contribution."

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and

      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding those notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.

      You may add Your own copyright statement to Your modifications and
      may provide additional or different license terms and conditions
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.

   END OF TERMS AND CONDITIONS

   APPENDIX: How to apply the Apache License to your work.

      To apply the Apache License to your work, attach the following
      boilerplate notice, with the fields enclosed by brackets "[]"
      replaced with your own identifying information. (Don't include
      the brackets!)  The text should be enclosed in the appropriate
      comment syntax for the file format. We also recommend that a
      file or class name and description of purpose be included on the
      same "printed page" as the copyright notice for easier
      identification within third-party archives.

   Copyright [yyyy] [name of copyright owner]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
````

---

### Template: `LICENSE` — variant for `LICENSE=PROPRIETARY`

````text
Copyright (c) {{CURRENT_YEAR}} {{COPYRIGHT_HOLDER}}. All rights reserved.

This software and its accompanying documentation are the confidential and
proprietary property of {{COPYRIGHT_HOLDER}}. Unauthorized copying, distribution,
modification, public display, public performance, or use of any portion of this
software, in source or binary form, in whole or in part, is strictly prohibited
without the prior written permission of {{COPYRIGHT_HOLDER}}.

No license, express or implied, by estoppel or otherwise, to any intellectual
property rights is granted by this document or by the possession of this
software.

THIS SOFTWARE IS PROVIDED "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
````

---

### Template: `AGENTS.md`

The primary, tool-agnostic agent brief. Every supported assistant (Claude Code via the `CLAUDE.md` adapter, Cursor via `.cursor/rules/`, Aider via `.aider.conf.yml`, OpenAI Codex CLI and OpenCode natively, Continue.dev via `.continue/config.json`, Windsurf via `.windsurfrules`, GitHub Copilot via `.github/copilot-instructions.md`) reads or transitively loads this file. Keep the brief here; let adapters point at it.

````markdown
# {{PROJECT_NAME}}

{{ONE_LINE_PURPOSE}}

## Purpose

[Expand the one-line purpose into a paragraph the agent reads on every cold start — what this project IS, who it's for, the core concepts and vocabulary, the main external dependencies (libraries, models, services). Replace this stub during bootstrap or in a follow-up commit.]

## Rules

Always follow the rules in `.agents/rules/`:

- [`workflow.md`](.agents/rules/workflow.md) — every artifact-producing request gets a timestamped prompt file under `.docs/prompts/`, an optional new-or-updated ADR under `.docs/adrs/`, telemetry kept current (logs added/updated for new and changed code paths, at log levels that match each event's signal — DEBUG / INFO / WARNING / ERROR / CRITICAL — with sensitive-data redaction discipline covering credentials, PII, billing identifiers, and request bodies), a single git commit bundling the lot, and a push. Also defines how do-later ideas get captured proactively.
- [`workflow-todos.md`](.agents/rules/workflow-todos.md) — the discipline for managing deferred ideas. Entries live as one file per idea under [`.docs/todos/`](.docs/todos/). Capture entries proactively when the user defers something ("for now / later / hold this"), sweep entries when a commit satisfies their *Revisit when* trigger, `git rm` rather than archive (git log is canonical).
- [`workflow-security.md`](.agents/rules/workflow-security.md) — companion to `workflow.md` for security-sensitive changes. Before commit, walk the rubric in [`.docs/security/methodology.md`](.docs/security/methodology.md) for surfaces your change touches (auth, inputs, SQL, output, transport, secrets, logging, rate limits, deps, LLM context). Full audits live as dated sibling files under `.docs/security/<YYYY-MM-DD>-<slug>.md` and re-run on cadence.
- [`best-practices.md`](.agents/rules/best-practices.md) — naming, dependency injection, repository / service patterns, language idioms, do/don't lists.
{{IF_LAYERED}}- [`layered-architecture.md`](.agents/rules/layered-architecture.md) — `presentation → application → domain ← infrastructure`, plus `shared` available to all but depending on none. Inward dependencies only.
{{IF_CHANGES}}- [`workflow-changes.md`](.agents/rules/workflow-changes.md) — companion to `workflow.md` for *product-affecting* changes. When a change alters anything a user can see, the surfaces that describe it must move in the same commit.
{{IF_UI_COMPONENTS}}- [`ui-components.md`](.agents/rules/ui-components.md) — catalog of canonical UI affordances. Before adding a new affordance, check the catalog and clone the canonical file's shape; never invent a one-off variant inline.
{{IF_METRICS}}- [`workflow-metrics.md`](.agents/rules/workflow-metrics.md) — companion to `workflow.md` for *metering* changes. Adding / modifying / removing a metered event must move surfaces in lockstep — constant, call site, catalog row, display side — all in the same commit. Cardinality discipline (no PII, no high-cardinality identifiers in labels) is non-negotiable.
{{IF_TESTING}}- [`workflow-testing.md`](.agents/rules/workflow-testing.md) — companion to `workflow.md` for testing discipline. Every artifact-producing change ships with the tests that prove its behaviour, in the same commit. Pyramid-shaped (unit-heavy / integration-light / e2e-thin), mock at boundaries not internals, bug fixes start with a failing regression test, TDD encouraged but not mandated, coverage tracked without a hard floor.

Architecture decisions and their trade-offs live in [`.docs/adrs/`](.docs/adrs/) — read these before making structural changes.

## Run

{{RUN_INSTRUCTIONS}}

## Architecture map

[Short pointer to where the main pieces live. Add an `ARCHITECTURE.md` at the repo root if the project grows enough to need its own tree + diagram.]

## Conventions (summary)

See [`.agents/rules/best-practices.md`](.agents/rules/best-practices.md) for full detail.

{{ADDITIONAL_SECTIONS_FROM_INTERVIEW}}
````

---

### Template: `.cursor/rules/agents.mdc` *(written only if `CURSOR ∈ AGENTS_USED`)*

A thin Cursor adapter. The frontmatter sets `alwaysApply: true` and a broad glob so Cursor includes this rule in every conversation across the workspace; the body points at `AGENTS.md` and the rules under `.agents/rules/`.

````markdown
---
description: Cross-tool agent brief — see AGENTS.md
globs: ["**/*"]
alwaysApply: true
---

This project's primary agent brief lives in `AGENTS.md` at the repo root.

Read these files at the start of any non-trivial task; they define the project's purpose, run instructions, architecture, and the workflow / security / best-practices rules every change must follow:

- `AGENTS.md`
- `.agents/rules/workflow.md`
- `.agents/rules/workflow-todos.md`
- `.agents/rules/workflow-security.md`
- `.agents/rules/best-practices.md`
{{IF_LAYERED}}- `.agents/rules/layered-architecture.md`
{{IF_CHANGES}}- `.agents/rules/workflow-changes.md`
{{IF_UI_COMPONENTS}}- `.agents/rules/ui-components.md`
{{IF_METRICS}}- `.agents/rules/workflow-metrics.md`
{{IF_TESTING}}- `.agents/rules/workflow-testing.md`

ADRs (architecture decisions) live under `.docs/adrs/` — read these before making structural changes. Do-later ideas live under `.docs/todos/`. Per-request prompt files live under `.docs/prompts/`.

When this file and `AGENTS.md` disagree, `AGENTS.md` wins.
````

---

### Template: `.aider.conf.yml` *(written only if `AIDER ∈ AGENTS_USED`)*

A minimal Aider config that always reads the brief + rule files into context. Users can layer their own model, lint, and edit-format preferences on top.

````yaml
# Aider config — keeps the cross-tool brief and rule files in context for every session.
# See https://aider.chat/docs/config/aider_conf.html for the full option list.

read:
  - AGENTS.md
  - .agents/rules/workflow.md
  - .agents/rules/workflow-todos.md
  - .agents/rules/workflow-security.md
  - .agents/rules/best-practices.md
{{IF_LAYERED}}  - .agents/rules/layered-architecture.md
{{IF_CHANGES}}  - .agents/rules/workflow-changes.md
{{IF_UI_COMPONENTS}}  - .agents/rules/ui-components.md
{{IF_METRICS}}  - .agents/rules/workflow-metrics.md
{{IF_TESTING}}  - .agents/rules/workflow-testing.md

# Aider auto-commits by default; the workflow.md rule wants one commit per request
# bundling the prompt file + ADR + code + telemetry. Leave auto-commit on, and let
# the rule guide what goes into a single commit.
# auto-commits: true

# Add your preferred model + edit-format here, e.g.:
# model: anthropic/claude-opus-4-7
# edit-format: diff
````

---

### Template: `.continue/config.json` *(written only if `CONTINUE ∈ AGENTS_USED`)*

A minimal Continue.dev config with a `rules` block pointing at the canonical brief + rule files. Users layer their model providers and slash commands on top.

````json
{
  "name": "{{PROJECT_NAME}}",
  "rules": [
    {
      "name": "Agent brief",
      "description": "Cross-tool project brief and workflow / best-practice rules.",
      "globs": ["**/*"],
      "rule": "Always read AGENTS.md and the files under .agents/rules/ before starting work. They define this project's purpose, run instructions, architecture, and the workflow / security / best-practices discipline every change must follow. ADRs live under .docs/adrs/ — consult before structural changes. Per-request prompt files go under .docs/prompts/. Do-later ideas go under .docs/todos/ as one file per entry."
    }
  ],
  "context": [
    { "provider": "file" },
    { "provider": "code" },
    { "provider": "diff" }
  ],
  "models": []
}
````

---

### Template: `.windsurfrules` *(written only if `WINDSURF ∈ AGENTS_USED`)*

A thin Windsurf rules file. Windsurf reads `.windsurfrules` automatically; the body points at the canonical brief.

````markdown
# Windsurf rules — pointer to AGENTS.md

This project's primary agent brief lives in `AGENTS.md` at the repo root. Read it (and the rule files it links to) before starting any non-trivial task.

Always-loaded context:

- `AGENTS.md` — purpose, run, architecture map, rule pointers.
- `.agents/rules/workflow.md` — prompt file → ADR → telemetry → commit → push.
- `.agents/rules/workflow-todos.md` — deferred ideas as one file per entry under `.docs/todos/`.
- `.agents/rules/workflow-security.md` — security rubric pass before commit.
- `.agents/rules/best-practices.md` — naming, DI, patterns, idioms.
{{IF_LAYERED}}- `.agents/rules/layered-architecture.md` — layer responsibilities and dependency direction.
{{IF_CHANGES}}- `.agents/rules/workflow-changes.md` — product-surface sync rule.
{{IF_UI_COMPONENTS}}- `.agents/rules/ui-components.md` — canonical component vocabulary.
{{IF_METRICS}}- `.agents/rules/workflow-metrics.md` — metering / cardinality rules.
{{IF_TESTING}}- `.agents/rules/workflow-testing.md` — testing pyramid + regression-first + same-commit test gate.

ADRs: `.docs/adrs/`. Per-request prompts: `.docs/prompts/`. Deferred ideas: `.docs/todos/`. Security audits: `.docs/security/`.

When this file and `AGENTS.md` disagree, `AGENTS.md` wins.
````

---

### Template: `.github/copilot-instructions.md` *(written only if `COPILOT ∈ AGENTS_USED`)*

GitHub Copilot reads `.github/copilot-instructions.md` automatically in repos but does *not* follow file references — it only sees what's inlined. The adapter therefore summarises the workflow + best-practice headlines directly and points to the canonical files for the agent (or human) to read on demand.

````markdown
# Copilot instructions — {{PROJECT_NAME}}

This project follows the **agentic-bootstrap** workflow discipline. The canonical, full brief lives in [`AGENTS.md`](../AGENTS.md) and the rule files under [`.agents/rules/`](../.agents/rules/). Read those before any non-trivial change.

## Workflow (summary — full text in `.agents/rules/workflow.md`)

Every artifact-producing request bundles:

1. A **prompt file** at `.docs/prompts/<unix-timestamp>.<slug>.md` capturing the request, reasoning, and output.
2. A **new or updated ADR** under `.docs/adrs/` when the change is architecturally significant (new module / pattern / dependency / contract).
3. **Telemetry kept current** — logs added/updated for new and changed code paths, at log levels matching the event's signal (DEBUG / INFO / WARNING / ERROR / CRITICAL), with no credentials / PII / billing IDs / request bodies in log output.
4. A **single commit** bundling all of the above, with an explicit `git add` (never `git add -A`).
5. A **push** to the remote when the commit succeeds.

Deferred ideas go to `.docs/todos/` as one file per entry — never as inline TODO comments or undocumented promises.

## Best practices (summary — full text in `.agents/rules/best-practices.md`)

- Dependency injection at the composition root; never instantiate infrastructure inside business logic.
- Repositories own data access; services own use cases; presentation orchestrates.
- Names are intent-revealing; comments are reserved for non-obvious *why*, not *what*.
- Tests cover behaviour at the right layer; mock at boundaries, not internals.

## Security (summary — full text in `.agents/rules/workflow-security.md`)

Before any security-sensitive commit, walk the rubric in [`.docs/security/methodology.md`](../.docs/security/methodology.md) for the surfaces your change touches (auth, inputs, SQL, output, transport, secrets, logging, rate limits, deps, LLM context). Full dated audits live as sibling files under `.docs/security/`.

{{IF_TESTING}}## Testing (summary — full text in `.agents/rules/workflow-testing.md`)
{{IF_TESTING}}
{{IF_TESTING}}Every artifact-producing change ships with its tests in the same commit. Pyramid shape: unit-heavy, integration-light, e2e-thin. Mock at boundaries (HTTP, clock, randomness, third-party SDKs) — never internals. Bug fixes start with a failing regression test. TDD is encouraged but not mandated; the hard rule is *tests + code in the same commit*. Coverage is tracked, not gated by a percentage. Flaky tests are P1 — fix or quarantine with a dated entry under `.docs/todos/`.
{{IF_TESTING}}
When this file and `AGENTS.md` disagree, `AGENTS.md` wins.
````

---

### Template: `.claude/settings.json` — variant for `POSTURE=CAUTIOUS`

````json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "model": "claude-opus-4-7"
}
````

Every Bash command, every WebFetch, every tool call prompts for permission. Safest baseline. Suitable for shared / team / open-source projects where multiple contributors check out the repo with different trust assumptions.

---

### Template: `.claude/settings.json` — variant for `POSTURE=READONLY`

````json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "model": "claude-opus-4-7",
  "permissions": {
    "allow": [
      "Bash(ls:*)",
      "Bash(cat:*)",
      "Bash(grep:*)",
      "Bash(find:*)",
      "Bash(wc:*)",
      "Bash(head:*)",
      "Bash(tail:*)",
      "Bash(pwd)",
      "Bash(date:*)",
      "Bash(echo:*)",
      "Bash(file:*)",
      "Bash(stat:*)",
      "Bash(git status:*)",
      "Bash(git log:*)",
      "Bash(git diff:*)",
      "Bash(git show:*)",
      "Bash(git branch:*)",
      "Bash(git ls-files:*)",
      "Bash(git remote:*)"
    ]
  }
}
````

Investigation (listing files, reading content, grepping, walking git history) is friction-free. Any write — file edits, `git add`, `git commit`, `mkdir`, etc. — still prompts. Good middle ground when you want the agent to *explore* freely but not *act* without consent.

---

### Template: `.claude/settings.json` — variant for `POSTURE=TRUSTED_DEV`

Write the base template below; then append the language-specific allow entries (from the table that follows) matching Q4 `LANG` into the `permissions.allow` array before the closing bracket. If `LANG=Other / mixed`, skip the language addendum and tell the user post-bootstrap to add their toolchain's commands manually.

**Base template** (all `TRUSTED_DEV` variants share this):

````json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "model": "claude-opus-4-7",
  "permissions": {
    "allow": [
      "Bash(ls:*)",
      "Bash(cat:*)",
      "Bash(grep:*)",
      "Bash(find:*)",
      "Bash(wc:*)",
      "Bash(head:*)",
      "Bash(tail:*)",
      "Bash(pwd)",
      "Bash(date:*)",
      "Bash(echo:*)",
      "Bash(file:*)",
      "Bash(stat:*)",
      "Bash(mkdir:*)",
      "Bash(touch:*)",
      "Bash(cp:*)",
      "Bash(mv:*)",
      "Bash(git:*)",
      "Bash(make:*)"
    ],
    "deny": [
      "Bash(rm -rf:*)",
      "Bash(rm -fr:*)",
      "Bash(git push --force:*)",
      "Bash(git push -f:*)",
      "Bash(git reset --hard:*)",
      "Bash(git clean -f:*)",
      "Bash(git clean -fd:*)",
      "Bash(git branch -D:*)",
      "Bash(git checkout .:*)",
      "Bash(git restore .:*)"
    ]
  }
}
````

**Language-specific addenda** — append these strings to the `permissions.allow` array based on Q4 `LANG`:

| `LANG` | Allow entries to append |
| --- | --- |
| Python | `"Bash(uv:*)"`, `"Bash(python:*)"`, `"Bash(python3:*)"`, `"Bash(pytest:*)"`, `"Bash(ruff:*)"`, `"Bash(mypy:*)"`, `"Bash(pyright:*)"`, `"Bash(black:*)"` |
| TypeScript/Node | `"Bash(npm:*)"`, `"Bash(pnpm:*)"`, `"Bash(yarn:*)"`, `"Bash(bun:*)"`, `"Bash(node:*)"`, `"Bash(npx:*)"`, `"Bash(tsc:*)"`, `"Bash(eslint:*)"`, `"Bash(prettier:*)"`, `"Bash(vitest:*)"`, `"Bash(jest:*)"` |
| Go | `"Bash(go:*)"`, `"Bash(gofmt:*)"`, `"Bash(goimports:*)"`, `"Bash(golangci-lint:*)"` |
| Rust | `"Bash(cargo:*)"`, `"Bash(rustc:*)"`, `"Bash(rustfmt:*)"`, `"Bash(clippy:*)"` |
| Other / mixed | (none — leave base template as-is; user adds their toolchain manually) |

Daily development — install, lint, format, test, build, commit, push — runs without prompts. The `deny` block keeps the catastrophic git / filesystem operations gated even though `Bash(git:*)` is broadly allowed. `rm` without `-rf` still goes through the allow check (so individual file deletes prompt).

---

### Template: `.claude/settings.json` — variant for `POSTURE=BYPASS`

````json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "model": "claude-opus-4-7",
  "permissions": {
    "defaultMode": "bypassPermissions"
  }
}
````

No prompts. Ever. Every tool call auto-approved.

**Use only when**:

- This is a personal / sandboxed environment (dedicated dev VM, container, throwaway workspace).
- The agent cannot reach production data, customer secrets, or shared infrastructure from here.
- You're comfortable with the agent running any command the operating system permits.

**Do not use when**:

- The workspace has shared credentials in env vars or files the agent could read.
- The workspace can `ssh` / `kubectl` / `aws` / `gh` into production from its current shell.
- Other people will check out this repo and inherit the setting (since `.claude/settings.json` is committed). For team projects, prefer `TRUSTED_DEV` and let each contributor pick `BYPASS` themselves via their gitignored `.claude/settings.local.json`.

---

**Notes for all variants**:

- `.claude/settings.local.json` is a per-machine override file the user may layer on top (their personal WebFetch domains, additional command allowlists, etc.). It's gitignored by the bootstrap so personal additions don't leak into commits.
- Document any later additions to `settings.json` (new permissions, hooks, env vars) in an ADR under `.docs/adrs/`. Permission changes especially — they alter what future agent sessions can do without prompting.

---

### Template: `.agents/bootstrap.json`

Persisted interview answers. Committed (project-shared). Read on re-run (Step 0) so previously-answered questions aren't re-asked. Re-write at the end of every bootstrap (Step 5) with the merged set of old + newly-answered keys.

Shape:

````json
{
  "$schema": "https://json.schemastore.org/claude-code-bootstrap.json",
  "bootstrap_version": "{{BOOTSTRAP_TIMESTAMP_ISO}}",
  "last_run_at": "{{CURRENT_TIMESTAMP_ISO}}",
  "answers": {
    "PROJECT_NAME": "{{PROJECT_NAME}}",
    "ONE_LINE_PURPOSE": "{{ONE_LINE_PURPOSE}}",
    "AGENTS_USED": {{AGENTS_USED_JSON_ARRAY}},
    "LAYOUT": "{{LAYOUT}}",
    "POSTURE": "{{POSTURE}}",
    "LANG": "{{LANG}}",
    "ARCH": "{{ARCH}}",
    "WEB": {{WEB}},
    "LLM": {{LLM}},
    "ENV_VARS": {{ENV_VARS}},
    "CHANGES": {{CHANGES}},
    "UI_COMPONENTS": {{UI_COMPONENTS}},
    "METRICS": {{METRICS}},
    "TESTING": {{TESTING}},
    "BEST_PRACTICES_REFINED": {{BEST_PRACTICES_REFINED}},
    "LICENSE": "{{LICENSE}}",
    "COPYRIGHT_HOLDER": "{{COPYRIGHT_HOLDER}}",
    "CONTRIB": {{CONTRIB}},
    "RUN_INSTRUCTIONS": "{{RUN_INSTRUCTIONS}}",
    "ADDITIONAL_SECTIONS_FROM_INTERVIEW": "{{ADDITIONAL_SECTIONS_FROM_INTERVIEW}}"
  }
}
````

**Field notes for the agent**:

- `bootstrap_version` — the timestamp from this bootstrap file's header (or `date +%Y-%m-%d` at write time if no header timestamp is tracked). Lets a future re-run report "you're upgrading from `<old>` to `<new>`".
- `last_run_at` — `date -Iseconds` at the moment of write; updated every re-run.
- `answers` — every flag from the interview. **Yes/no flags** are JSON booleans (`true` / `false`, no quotes). **String flags** (POSTURE, LANG, ARCH, LICENSE, LAYOUT) are JSON strings. **Set flags** (`AGENTS_USED`) are JSON arrays of uppercase strings — e.g. `["CLAUDE", "CURSOR", "AIDER"]`. Free-form text (PROJECT_NAME, ONE_LINE_PURPOSE, RUN_INSTRUCTIONS, ADDITIONAL_SECTIONS_FROM_INTERVIEW, COPYRIGHT_HOLDER) are JSON strings; escape newlines as `\n`. If `LICENSE=SKIP`, `COPYRIGHT_HOLDER` stays as the empty string. `POSTURE=N_A` is reserved for projects where `CLAUDE ∉ AGENTS_USED` (no Claude settings file written). `LAYOUT` is `"agents"` (canonical, files under `.agents/rules/`) or `"legacy_claude"` (pre-multi-tool projects where the user picked "leave in place" during the Step 0 migration prompt — see the legacy-layout migration note in Part 1). `BEST_PRACTICES_REFINED` is set by Step 4b: `true` after a successful web-search-driven refinement of `.agents/rules/best-practices.md`, `false` when the stub variant was written. The same flag is independently verifiable by reading the marker comment at the top of the file (single source of truth); the bootstrap.json mirror exists so re-runs can decide cheaply without opening the file.
- Omit any key the current bootstrap version doesn't know about. On re-run, **missing keys** are exactly what the agent re-asks the user.
- **No secrets in this file**. Free-form fields capture user intent, not credentials. If the user accidentally includes a secret in `RUN_INSTRUCTIONS` or `ADDITIONAL_SECTIONS_FROM_INTERVIEW`, the agent should flag and ask before persisting.

**On re-run mode**:

- Read the existing file in Step 0.
- In Step 2, identify keys missing from `answers` (new questions since the last bootstrap version) and ask only those.
- In this step (Step 5), write the file with the merged answers and the current `bootstrap_version` / `last_run_at`.
- The file is itself **Canon** category (see Part 3): silently rewritten on every bootstrap so the persisted state stays in sync with the actual interview.

---

### Template: manifest + test scaffold — variant for `LANG=Python`

Write two files.

**`pyproject.toml`**:

````toml
[project]
name = "{{PROJECT_NAME}}"
version = "0.1.0"
description = "{{ONE_LINE_PURPOSE}}"
requires-python = ">=3.11"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=8",
    "ruff>=0.6",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra -q"

[tool.ruff]
line-length = 100
````

**`tests/test_smoke.py`**:

````python
def test_smoke() -> None:
    """Sanity check the test runner is wired up.

    Replace this with the first real test as the project takes shape.
    """
    assert 1 + 1 == 2
````

Mention to the user post-bootstrap: pick a real package manager (`uv` is the modern choice — `uv sync` + `uv lock`) and commit the resulting lockfile.

---

### Template: manifest + test scaffold — variant for `LANG=TypeScript/Node`

Write two files.

**`package.json`**:

````json
{
  "name": "{{PROJECT_NAME}}",
  "version": "0.1.0",
  "description": "{{ONE_LINE_PURPOSE}}",
  "type": "module",
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest"
  },
  "devDependencies": {
    "typescript": "^5",
    "vitest": "^2",
    "@types/node": "^22"
  }
}
````

**`tests/smoke.test.ts`**:

````typescript
import { describe, it, expect } from "vitest";

describe("smoke", () => {
  it("wires up the test runner", () => {
    expect(1 + 1).toBe(2);
  });
});
````

Mention to the user post-bootstrap: pick a package manager (npm / pnpm / yarn / bun) and commit the resulting lockfile. Add a `tsconfig.json` matching the project's runtime target.

---

### Template: manifest + test scaffold — variant for `LANG=Go`

Write two files.

**`go.mod`**:

````go
module {{PROJECT_MODULE_PATH}}

go 1.23
````

The agent asks the user for `{{PROJECT_MODULE_PATH}}` (e.g. `github.com/<org>/{{PROJECT_NAME}}` or a private path) before writing.

**`smoke_test.go`** (at the repo root):

````go
package main

import "testing"

func TestSmoke(t *testing.T) {
    if 1+1 != 2 {
        t.Fatal("arithmetic broken")
    }
}
````

Mention to the user post-bootstrap: run `go mod tidy` once real imports land.

---

### Template: manifest + test scaffold — variant for `LANG=Rust`

Write two files.

**`Cargo.toml`**:

````toml
[package]
name = "{{PROJECT_NAME}}"
version = "0.1.0"
edition = "2021"
description = "{{ONE_LINE_PURPOSE}}"

[dependencies]

[dev-dependencies]
````

**`tests/smoke.rs`**:

````rust
#[test]
fn smoke() {
    assert_eq!(1 + 1, 2);
}
````

Mention to the user post-bootstrap: run `cargo build` to generate `Cargo.lock`; decide whether to commit it (commit for binaries, optional for libraries).

---

### Template: manifest + test scaffold — fallback variant for any other `LANG`

No manifest written. Tell the user post-bootstrap:

> "The bootstrap doesn't ship a manifest stub for `{{LANG}}`. Add the canonical project file for your language (`<manifest>`), a tests directory with one placeholder test, and a lockfile discipline once tooling is picked. The security methodology's `§5.10 Dependency hygiene` rubric assumes a committed lockfile."

---

### Template: `CONTRIBUTING.md` *(opt-in, write only if `CONTRIB`)*

````markdown
# Contributing to {{PROJECT_NAME}}

Thanks for considering a contribution. This file covers the bare minimum to get a change landed; the deeper conventions live in [`AGENTS.md`](./AGENTS.md) and the rules under [`.agents/rules/`](./.agents/rules/).

## Development setup

{{RUN_INSTRUCTIONS}}

## Branch and PR conventions

- Work on a feature branch off `main`; one logical change per PR.
- PR title is imperative and under 70 characters (it becomes the squash-merge commit subject).
- PR description explains *why* — the *what* is in the diff.
- Link the originating issue or discussion if one exists.

## Code style

- Follow [`.agents/rules/best-practices.md`](./.agents/rules/best-practices.md) — naming, dependency injection, repository / service patterns, language idioms.
- Run the project's formatter and linter before opening the PR (`make lint`, `ruff check`, `eslint`, `gofmt`, `cargo fmt` — whichever applies).
- Tests for new behaviour live next to the existing tests; the smoke test is the entry point.

## Filing issues

- **Bug reports**: include the steps to reproduce, the expected behaviour, the actual behaviour, and the environment (OS, language version, relevant deps).
- **Feature requests**: explain the use case before the implementation. The decision-record style at [`.docs/adrs/0000-adr-template.md`](./.docs/adrs/0000-adr-template.md) is a good frame for "what shape is the change, and what are the trade-offs?".
- **Security**: do not file public issues for vulnerabilities. Contact the maintainers privately (see `SECURITY.md` if present, otherwise email the repository owner). See [`.docs/security/methodology.md`](./.docs/security/methodology.md) for the project's overall security posture.

## Architecture decisions

Significant structural changes (a new library, a new layer, a new pattern, a shift in tier or pricing behaviour) need a new ADR under [`.docs/adrs/`](./.docs/adrs/) in the same PR. The discipline is described in [`.agents/rules/workflow.md`](./.agents/rules/workflow.md).
````

---

### Template: `SECURITY.md`

````markdown
# Security Policy

## Reporting a vulnerability

If you've found a security issue in {{PROJECT_NAME}}, please **do not file a public issue**. Public disclosure before a fix is shipped exposes other users to the same risk.

Instead, contact the maintainers privately:

- **Email**: <security@{{PROJECT_DOMAIN_OR_PLACEHOLDER}}> (replace with the project's real address before publishing)
- Or open a private security advisory on the repository host (e.g. GitHub's "Report a vulnerability" button under the *Security* tab) if available

Please include:

- A description of the issue and its impact.
- Steps to reproduce.
- The affected version (commit SHA or release tag).
- Any proof-of-concept you have — code, request payloads, screenshots.

You'll get an acknowledgement within **5 business days**. We'll keep you posted on the fix timeline; coordinated disclosure happens once a fix is available and users have had a reasonable upgrade window.

## Scope

In scope:

- The code in this repository.
- Default configuration and recommended deployment instructions.
- Dependencies pinned by this project (we'll triage and forward upstream as appropriate).

Out of scope:

- Vulnerabilities in third-party services we don't control (cloud providers, CDNs, …).
- Social-engineering attacks.
- Self-XSS / requires-physical-access scenarios with no plausible attack path.

## Security posture

The project's overall security methodology, rubric, and the dated audit history live under [`.docs/security/`](./.docs/security/). See [`.docs/security/methodology.md`](./.docs/security/methodology.md) for the playbook reviewers follow.

The companion workflow rule at [`.agents/rules/workflow-security.md`](./.agents/rules/workflow-security.md) describes how security-sensitive changes are reviewed during day-to-day development.
````

---

### Template: `.gitattributes`

````gitattributes
# Normalise line endings — repository stores LF; checkouts convert per OS where needed.
* text=auto eol=lf

# Explicitly binary (do not normalise).
*.png       binary
*.jpg       binary
*.jpeg      binary
*.gif       binary
*.ico       binary
*.webp      binary
*.pdf       binary
*.zip       binary
*.gz        binary
*.tar       binary
*.woff      binary
*.woff2     binary
*.ttf       binary
*.otf       binary
*.eot       binary
*.mp3       binary
*.mp4       binary
*.wav       binary
*.flac      binary

# Lockfiles — generated, treat as text but linguist should not count toward language stats.
*.lock              linguist-generated=true
package-lock.json   linguist-generated=true
yarn.lock           linguist-generated=true
pnpm-lock.yaml      linguist-generated=true
poetry.lock         linguist-generated=true
uv.lock             linguist-generated=true
Cargo.lock          linguist-generated=true
go.sum              linguist-generated=true

# Markdown docs aren't "code" — keep them out of language stats too.
.docs/**           linguist-documentation=true
````

---

### Template: `CHANGELOG.md`

````markdown
# Changelog

All notable changes to this project will be documented in this file. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security

## [0.1.0] — {{CURRENT_DATE_ISO}}

### Added
- Initial project bootstrap. See `AGENTS.md` and `.agents/rules/` for conventions.
````

The agent fills `{{CURRENT_DATE_ISO}}` from `date +%Y-%m-%d`.

---

### Template: `CODE_OF_CONDUCT.md` *(opt-in, write only if `CONTRIB`)*

````markdown
# Code of Conduct

This project follows the [Contributor Covenant](https://www.contributor-covenant.org/), version 2.1.

## Our pledge

We pledge to make participation in {{PROJECT_NAME}} a harassment-free experience for everyone, regardless of age, body size, visible or invisible disability, ethnicity, sex characteristics, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual identity and orientation.

## Our standards

Examples of behaviour that contributes to a positive environment:

- Demonstrating empathy and kindness toward other people.
- Being respectful of differing opinions, viewpoints, and experiences.
- Giving and gracefully accepting constructive feedback.
- Accepting responsibility and apologising to those affected by our mistakes, and learning from the experience.
- Focusing on what is best not just for us as individuals, but for the overall community.

Examples of unacceptable behaviour:

- The use of sexualised language or imagery, and sexual attention or advances of any kind.
- Trolling, insulting or derogatory comments, and personal or political attacks.
- Public or private harassment.
- Publishing others' private information, such as a physical or email address, without their explicit permission.
- Other conduct which could reasonably be considered inappropriate in a professional setting.

## Enforcement

Instances of abusive, harassing, or otherwise unacceptable behaviour may be reported to the maintainers at <conduct@{{PROJECT_DOMAIN_OR_PLACEHOLDER}}>. All complaints will be reviewed and investigated promptly and fairly.

All maintainers are obligated to respect the privacy and security of the reporter of any incident.

## Attribution

This Code of Conduct is adapted from the [Contributor Covenant, version 2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct.html). For answers to common questions, see the [Contributor Covenant FAQ](https://www.contributor-covenant.org/faq).
````

---

### Template: linter / formatter configs — variant for `LANG=Python`

The Python manifest stub already carries a minimal `[tool.ruff]` block in `pyproject.toml`. If the project wants a standalone Ruff config (some teams prefer separating tool config from manifests), additionally write:

**`ruff.toml`**:

````toml
line-length = 100
target-version = "py311"

[lint]
# Conservative starter set. Expand as the project matures.
select = ["E", "F", "I", "B", "UP", "SIM"]
ignore = []

[format]
quote-style = "double"
indent-style = "space"
````

Don't write this file *and* keep `[tool.ruff]` in `pyproject.toml` — pick one place for Ruff config and stay consistent. Default for new projects: keep it inline in `pyproject.toml`; promote to `ruff.toml` only when the config grows past ~10 lines.

---

### Template: linter / formatter configs — variant for `LANG=TypeScript/Node`

Write two files (or skip if the project picks a different toolchain; eslint + prettier is the modern default).

**`eslint.config.js`** (flat config, ESLint 9+):

````javascript
import js from "@eslint/js";
import tseslint from "typescript-eslint";

export default [
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
    },
    rules: {
      "@typescript-eslint/no-unused-vars": ["warn", { argsIgnorePattern: "^_" }],
    },
  },
  {
    ignores: ["dist/", "build/", "node_modules/", "coverage/"],
  },
];
````

**`.prettierrc.json`**:

````json
{
  "printWidth": 100,
  "tabWidth": 2,
  "semi": true,
  "singleQuote": false,
  "trailingComma": "all",
  "arrowParens": "always",
  "endOfLine": "lf"
}
````

Add to `package.json` `devDependencies`:

```text
"@eslint/js", "typescript-eslint", "eslint", "prettier"
```

---

### Template: linter / formatter configs — variant for `LANG=Go`

Go's built-in `gofmt` covers formatting; for linting use [`golangci-lint`](https://golangci-lint.run/). Write:

**`.golangci.yml`**:

````yaml
run:
  timeout: 5m

linters:
  disable-all: true
  enable:
    - errcheck
    - gosimple
    - govet
    - ineffassign
    - staticcheck
    - unused
    - gofmt
    - goimports
    - revive

issues:
  exclude-use-default: false
````

The user installs `golangci-lint` separately (it's not a Go module dep). Run with `golangci-lint run`.

---

### Template: linter / formatter configs — variant for `LANG=Rust`

Rust's built-in `rustfmt` + `clippy` are the standard. Write:

**`rustfmt.toml`**:

````toml
edition = "2021"
max_width = 100
````

**`clippy.toml`** (optional — only needed when overriding defaults):

````toml
# Empty by default — clippy ships sensible defaults. Add overrides as the project matures.
````

The user runs `cargo fmt` and `cargo clippy -- -D warnings` (treat clippy warnings as errors in CI).

---

### Template: linter / formatter configs — fallback variant for any other `LANG`

No config files written. Tell the user post-bootstrap:

> "The bootstrap doesn't ship linter/formatter configs for `{{LANG}}`. Pick the canonical formatter + linter for your language, add their config files to the repo root, and wire the invocations into the `Makefile` (or your task runner) so `lint` / `format` targets are one command."

---

### Template: `Makefile` — variant for `LANG=Python`

````makefile
.PHONY: help install test lint format check run clean

help:
	@echo "Targets:"
	@echo "  install   Install dependencies (and dev deps)"
	@echo "  test      Run tests"
	@echo "  lint      Run linter"
	@echo "  format    Run formatter"
	@echo "  check     Lint + test (CI-style)"
	@echo "  run       Run the application (override per project)"
	@echo "  clean     Remove build / cache artefacts"

install:
	uv sync --extra dev

test:
	uv run pytest

lint:
	uv run ruff check .

format:
	uv run ruff format .

check: lint test

run:
	@echo "Override the 'run' target per project (e.g. 'uv run python -m {{PROJECT_NAME}}')"

clean:
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .ruff_cache/ .mypy_cache/ htmlcov/ .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
````

If the project uses `pip` / `poetry` instead of `uv`, swap the commands accordingly.

---

### Template: `Makefile` — variant for `LANG=TypeScript/Node`

````makefile
.PHONY: help install test lint format check run clean

# Replace `npm` with `pnpm`, `yarn`, or `bun` if the project uses a different package manager.
PM := npm

help:
	@echo "Targets:"
	@echo "  install   Install dependencies"
	@echo "  test      Run tests"
	@echo "  lint      Run linter"
	@echo "  format    Run formatter"
	@echo "  check     Lint + test (CI-style)"
	@echo "  run       Run the application (override per project)"
	@echo "  clean     Remove build / cache artefacts"

install:
	$(PM) install

test:
	$(PM) test

lint:
	$(PM) exec eslint .

format:
	$(PM) exec prettier --write .

check: lint test

run:
	@echo "Override the 'run' target per project (e.g. '$(PM) run dev')"

clean:
	rm -rf dist/ build/ coverage/ .turbo/ .next/ .vite/
````

---

### Template: `Makefile` — variant for `LANG=Go`

````makefile
.PHONY: help build test lint format check run clean

BIN_DIR ?= bin
BIN_NAME ?= {{PROJECT_NAME}}

help:
	@echo "Targets:"
	@echo "  build     Compile the binary into $(BIN_DIR)/"
	@echo "  test      Run tests"
	@echo "  lint      Run golangci-lint"
	@echo "  format    Run gofmt + goimports"
	@echo "  check     Lint + test (CI-style)"
	@echo "  run       Run the application"
	@echo "  clean     Remove build artefacts"

build:
	mkdir -p $(BIN_DIR)
	go build -o $(BIN_DIR)/$(BIN_NAME) ./...

test:
	go test ./...

lint:
	golangci-lint run

format:
	gofmt -w .
	goimports -w .

check: lint test

run:
	go run ./...

clean:
	rm -rf $(BIN_DIR)/
	go clean
````

---

### Template: `Makefile` — variant for `LANG=Rust`

````makefile
.PHONY: help build test lint format check run clean

help:
	@echo "Targets:"
	@echo "  build     Compile (debug)"
	@echo "  test      Run tests"
	@echo "  lint      Run clippy"
	@echo "  format    Run rustfmt"
	@echo "  check     Lint + test (CI-style)"
	@echo "  run       Run the application"
	@echo "  clean     Remove target/"

build:
	cargo build

test:
	cargo test

lint:
	cargo clippy --all-targets -- -D warnings

format:
	cargo fmt

check: lint test

run:
	cargo run

clean:
	cargo clean
````

---

### Template: `Makefile` — fallback variant for any other `LANG`

````makefile
.PHONY: help test lint format check run clean

# Replace each target's body with the canonical command for your language toolchain.
help:
	@echo "Targets to fill in: test, lint, format, check, run, clean"

test:
	@echo "TODO: wire up the test runner for {{LANG}}"

lint:
	@echo "TODO: wire up the linter for {{LANG}}"

format:
	@echo "TODO: wire up the formatter for {{LANG}}"

check: lint test

run:
	@echo "TODO: wire up the run command"

clean:
	@echo "TODO: wire up cache / artefact cleanup"
````

---

### Template: `.pre-commit-config.yaml`

````yaml
# https://pre-commit.com — install with: pip install pre-commit && pre-commit install
# Hook on every commit; mirrors what the Makefile `check` target does, faster feedback.

repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-toml
      - id: check-merge-conflict
      - id: check-added-large-files
        args: ["--maxkb=512"]
      - id: detect-private-key

  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.21.2
    hooks:
      - id: gitleaks
````

Per-language hooks the user adds as the project matures (don't write them at bootstrap — they require the toolchain to be installed):

- **Python**: `ruff` (lint + format), `mypy` / `pyright` (types).
- **TypeScript/Node**: `eslint`, `prettier`, `typescript`.
- **Go**: `golangci-lint`, `gofmt`, `goimports`.
- **Rust**: `cargo fmt`, `cargo clippy`.

The bootstrap ships the universal hooks (whitespace, YAML/JSON/TOML syntax, secret detection via gitleaks); each project layers its language-specific hooks on top.

---

## Part 5 — Post-bootstrap checklist (for the user)

After the agent finishes and pushes the first commit, here's what's worth doing next (not the agent — you):

- **Open `AGENTS.md`** and expand the *Purpose* paragraph. The interview gives the agent one sentence; the cold-start brief deserves a paragraph.
- **Read the rules** under `.agents/rules/` once, end-to-end. They're load-bearing for every future request; knowing what's in there means you can tell when the agent is drifting.
- **Verify each picked adapter actually loads the brief in its tool.** Open the project in each assistant in `AGENTS_USED` and confirm it picks up `AGENTS.md` + the rule files — Claude follows the `@`-refs in `CLAUDE.md`, Cursor applies the `alwaysApply: true` rule in `.cursor/rules/agents.mdc`, Aider reads files listed in `.aider.conf.yml`'s `read:`, etc. If an adapter is silently ignored, that's a load-bearing gap.
- **Refine `best-practices.md` from current web sources** if the Step 8 report flagged it as *stubbed*. Open the file's `§ Enable refinement` matrix, flip whichever knob your agent host needs (Claude Code permission entries, Cursor `@web` invocation, Codex `--web` flag, Continue.dev's `web` context provider, etc.), then ask any agent to *"re-run the bootstrap's Step 4b best-practices refinement"*. The stub variant becomes a stack-specific refined variant with inline citations — substantially more useful than the generic baseline. If your host can't reach the web at all, fetch the few canonical sources for your stack manually and paste excerpts into the chat to seed the refinement.
- **Write the first real ADR** (`0001-<slug>.md`) if the project starts with a load-bearing decision — framework choice, persistence story, deployment shape. Update the README index in the same commit.
- **Schedule the first security audit.** The methodology at [`.docs/security/methodology.md`](.docs/security/methodology.md) is the playbook; the first dated audit (`.docs/security/<YYYY-MM-DD>-baseline.md`) is a useful pre-release baseline even on a small codebase. The rubric is also a usable pre-commit aid once the project has shipped its first security-sensitive surface.
- **Grow `.claude/settings.json`** (if Claude is in `AGENTS_USED`) as the project's agent-host needs surface — hooks, permission allowlists, environment vars, model pin. The bootstrap leaves it as an empty `{}`; document each addition in an ADR.
- **Add CI** for your hosting platform of choice — GitHub Actions, GitLab CI, Bitbucket Pipelines, CircleCI, etc. The bootstrap intentionally skips CI (it's host-specific); the security methodology's "CVE scanner in CI" rubric stays aspirational until you wire one up.
- **Lock dependencies** — run the language's lockfile generator (`uv lock`, `npm install` / `pnpm install`, `cargo build`, `go mod tidy`) and commit the resulting lockfile per `methodology.md §5.10`.
- **Consider adding an `ARCHITECTURE.md`** at the repo root when the project grows enough to need a tree + diagram alongside `AGENTS.md`.
- **Update this file** (`AGENTIC_BOOTSTRAP.md`) whenever you discover a pattern worth standardising across future projects. The whole point is that the next `cd new-project && paste-this-file` reflects your latest thinking. See Part 6 for the maintenance checklist.

---

## Part 6 — How to extend this bootstrap

The bootstrap evolves. New patterns surface, new conventions emerge, new languages show up. This section is the checklist for editing the file safely — read it before adding an interview question, a new template, or a new rule.

### Coupled surfaces

Every meaningful edit touches **four or five places**, in lockstep:

1. **Part 2 (Interview)** — the question that captures the user's answer.
1. **Part 3 (Decision matrix)** — the row that says whether the file is always-written or conditional, what triggers it, and its **Re-run policy** (Canon / Mixed / Sacred / New each run — see the legend at the top of Part 3).
1. **Part 4 (Templates)** — the actual file content the agent writes.
1. **Part 1 Step 4 (Dispatch)** — *only when a flag is multi-valued* (like `LANG`, `ARCH`, `LICENSE`, `POSTURE`): the dispatch paragraph that tells the agent how to pick the variant.
1. **`.agents/bootstrap.json` template** (Part 4) — *only when a new flag / interview key is added*: extend the `answers` object so the new key gets persisted (and so existing projects know to re-ask it on next re-run, since the key is missing from their cached file).

Skipping any of these breaks the bootstrap: a template with no interview question is dead code; a question with no template is a dangling answer; a matrix row out of sync misleads the agent on whether to write the file; a missing Re-run policy means re-runs guess wrong about whether to overwrite or preserve user edits.

### Common edits — recipes

**Adding a new always-installed file** (e.g. another universal scaffold like `SECURITY.md`):

1. Add a row to **Part 3** marked `Always`, with a **Re-run policy** picked:
   - `C` (Canon) — versioned discipline, bootstrap is source of truth (rules, ADR template, security methodology, AGENTS.md, .gitattributes, .editorconfig).
   - `M` (Mixed) — user expected to layer additions on top (gitignore, settings.json, Makefile, linter configs).
   - `S` (Sacred) — written once, then user-owned (README, SECURITY.md, CHANGELOG, manifests).
2. Add the **Part 4** template (single block, no conditional wrappers).
3. If the file is referenced from the primary brief, add the reference line to the **`AGENTS.md` template** (and to each per-tool adapter template that mirrors the rule list — `CLAUDE.md`, `.cursor/rules/agents.mdc`, `.aider.conf.yml`, `.windsurfrules`, `.github/copilot-instructions.md`). Adapters that load files transitively only need the rule path in `AGENTS.md`; adapters that inline their rule list (Copilot) need it inlined.
4. No interview question needed.

**Adding a new opt-in file** (e.g. another conventional file gated on existing flags):

1. Pick or add the flag that gates it. If a new flag is needed, add an interview question (**Part 2**) AND extend the `.agents/bootstrap.json` `answers` object so existing projects re-ask it on next re-run.
2. Add a row to **Part 3** marked `Opt-in`, citing the trigger and the Re-run policy.
3. Add the **Part 4** template wrapped in `{{IF_FLAG}}` headers or labelled `*(opt-in, write only if FLAG)*`.
4. Update the **`AGENTS.md` template** rule-list block if the new file is a rule worth pointing at — and mirror the addition into every per-tool adapter template that lists rules explicitly.

**Adding a new multi-value flag variant** (e.g. another language for `LANG`):

1. Update **Part 2 Q4** options if the new value is user-pickable (or document under "Other → fallback").
2. Update **Part 1 Step 4** dispatch description to mention the new value.
3. Add **Part 4** template variants under the existing template (`### Template: X — variant for LANG=NewLang`).
4. Make sure both the `.gitignore` and `manifest + test scaffold` variants exist for the new language — they ship together.
5. The `LANG` key is already in `.agents/bootstrap.json`'s schema; the new value will be captured automatically.

**Adding a new opt-in rule under `.agents/rules/`**:

1. Add an interview question in **Part 2** to gate it, AND extend `.agents/bootstrap.json`'s `answers` object with the new flag.
2. Add a row to **Part 3** marked `Opt-in`, Re-run policy `C` (rules are always Canon).
3. Add the **Part 4** template.
4. Add a `{{IF_NEWFLAG}}` reference line to the **`AGENTS.md` template** rule-list block, plus the matching `{{IF_NEWFLAG}}` line to each per-tool adapter template that lists rules (`CLAUDE.md`, `.cursor/rules/agents.mdc`, `.aider.conf.yml`, `.windsurfrules`, `.github/copilot-instructions.md`).

**Editing an existing template**:

- Edit in place. The next bootstrap reflects the change. No version-tracking discipline here — the file's git log is the audit trail.
- If the edit reshapes the discipline (not just the wording), update the cross-references in other templates that point at it. `workflow.md` references `workflow-security.md`, `workflow-todos.md`, `workflow-changes.md`, `workflow-metrics.md`; `methodology.md` references `workflow-security.md`; etc. Drift between cross-references and reality is the easiest way to make the bootstrap subtly wrong.

### Conditional syntax — keep it simple

The bootstrap uses two conditional shapes; don't invent a third:

- **`{{PLACEHOLDER}}`** — direct substitution. The agent replaces with the interview answer (or a computed value like `{{CURRENT_YEAR}}` from `date +%Y`).
- **`{{IF_FLAG}}<line content>`** — keep the line (after stripping the prefix) when `FLAG` is true; remove the line entirely when false. Used for both pure-boolean flags (`CHANGES`, `METRICS`, `UI_COMPONENTS`, `CONTRIB`, `WEB`, `LLM`) and derived flags (`LAYERED` = `(ARCH != FLAT)`).

For multi-value flag variants (`LANG`, `ARCH`, `LICENSE`), use **separate labelled template sections** rather than inline conditionals. Each variant gets its own `### Template: X — variant for FLAG=VALUE` heading; the agent picks the matching one. This is easier to read, easier to add new variants to, and easier to delete obsolete ones from.

### Quality bar

Before saving an edit, sanity-check:

- **Cross-references resolve.** Internal links (`[`text`](path)`) actually point at files the bootstrap will write.
- **Templates are self-contained.** Don't reference content that lives in another template only as a side effect — if a template needs context from another file, restate the dependency.
- **Conditional content is removable.** Test mentally: if all opt-in flags are false, does the file still read coherently?
- **No project-specific bleed.** Search for project names ("musical", a company name, an LLM name) before saving. The bootstrap is project-agnostic; the templates it writes get filled in per project.

### What lives elsewhere

The bootstrap is *one file*. Things that don't belong inside it:

- **Lockfiles, dependencies, build artefacts.** The bootstrap describes how to scaffold these; it doesn't ship them.
- **Project-specific code.** The bootstrap writes templates; real code is written per project, after bootstrap.
- **Long-form rationale.** ADRs are the right home for "why this shape over that one"; the bootstrap is the *what*, not the *why*. Promote a debate to an ADR once it's load-bearing.
- **A changelog of bootstrap versions.** The file's git log is canonical history. If a behavioural change matters across projects, raise it in an out-of-band note when you update; don't build a version index inside the bootstrap.
