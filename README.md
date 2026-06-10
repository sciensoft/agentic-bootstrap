# Agentic Bootstrap

**One markdown file. One agent. One command. Your repo grows the discipline a Senior Engineer would have set up on day one.**

*By [Alexandre Souza](https://github.com/AlexzSouz) · [MIT licensed](./LICENSE) · [github.com/sciensoft/agentic-bootstrap](https://github.com/sciensoft/agentic-bootstrap)*

Every project grows good engineering habits eventually — usually after the third *"why did we do it that way?"*, the first security scare, the fifth time the agent re-derives the same context. **The bootstrap installs them on day one.**

Hand [AGENTIC_BOOTSTRAP.md](./AGENTIC_BOOTSTRAP.md) to your coding agent, say *"follow this bootstrap"*, and walk away with the discipline most projects don't get for months: ADRs for load-bearing decisions, a prompt history that captures the *why*, a security rubric you actually walk, permissions matched to risk, a `CLAUDE.md` the agent re-reads on every cold start — all interactively tailored to your stack, your risk tolerance, and your project's shape.

No templates to clone. No CLI to install. No external fetches. Just one file your agent reads end-to-end.

---

## Engineering principles, on day one

Every project grows these habits eventually. The third *"why did we do it that way?"* triggers ADRs. The first security scare triggers a review rubric. The fifth time the agent re-derives the same context triggers a `CLAUDE.md`. The fourth `git push --force` prompt triggers permission discipline.

You'd get there in six months. The bootstrap gets you there in two minutes.

| Habit | What lands in your repo |
| --- | --- |
| **Decisions don't fade into commit messages.** | `.docs/adrs/` with a Nygard-format template. Every load-bearing decision gets its own file. |
| **The *why* lives next to the *what*.** | `.claude/prompts/<ts>.<slug>.md` — every artifact-producing request leaves a prompt file. `git log` + prompts reconstruct the whole story. |
| **Security gets a checklist, not a vibe.** | `.docs/security/methodology.md` — OWASP Top 10 + OWASP LLM Top 10 rubric you walk before merging anything risky. |
| **Deferred ideas don't drown in a ticket backlog.** | `.docs/todos/` — one file per idea, each with a *Revisit when* trigger. Sweep when a commit satisfies it; `git rm` to retire. |
| **Permissions match risk.** | Four `.claude/settings.json` postures with explicit deny-patterns for `git push --force`, `rm -rf`, `git reset --hard`. |
| **The agent re-reads the project, not your last twelve messages.** | `CLAUDE.md` — cold-start brief, refreshed every session. |
| **Boring conventional files exist from day one.** | `.gitignore`, `.editorconfig`, `Makefile`, linter configs, `SECURITY.md`, `CHANGELOG.md` — language-aware where it matters. |
| **Re-runs never break what you own.** | The Canon / Mixed / Sacred [ownership model](#the-ownership-model-why-re-runs-are-safe) — the bootstrap evolves; your edits stay safe. |

---

## Why one file, not a template or CLI

You've seen the alternatives. None of them stick:

| You don't want | Because |
| --- | --- |
| A git template you copy and then drift from | Templates rot the second you fork them. |
| A CLI tool with its own version, plugins, and breaking changes | Another dependency to track for something you do once per project. |
| A 12-step blog post you skim and half-apply | You'll skip the parts you don't understand and regret it later. |
| A static dump where you delete the irrelevant 60% | Wasted effort; opinionated noise. |

The bootstrap is **a single file your agent reads and follows**. It interviews you, picks only the parts that match your project, and writes them. To evolve it, you edit the file. That's the whole tool.

---

## Quick start

1. `cd` into your target project — a fresh `mkdir foo && cd foo`, or any existing repo.
2. Open your coding agent (Claude Code, Cursor, Codex CLI, Aider — anything that reads a file and runs shell + edits).
3. Paste the full contents of [AGENTIC_BOOTSTRAP.md](./AGENTIC_BOOTSTRAP.md) into the session, then say:

   > **Follow this bootstrap.**

The agent reads [Part 1](./AGENTIC_BOOTSTRAP.md), interviews you (14 questions, 6 tiers), writes only the files matching your answers, makes the first commit, and pushes if you have a remote.

Re-run any time the bootstrap is updated. Your edits stay safe — the [ownership model](#the-ownership-model-why-re-runs-are-safe) guarantees it.

---

## What your repo looks like after

```text
your-project/
├── CLAUDE.md                       # cold-start brief; the agent re-reads this every session
├── AGENTS.md                       # cross-tool pointer to CLAUDE.md
├── README.md                       # project intro stub for you to expand
├── LICENSE                         # MIT / Apache 2.0 / Proprietary / skipped
├── SECURITY.md                     # private vulnerability disclosure
├── CHANGELOG.md                    # Keep a Changelog format
├── Makefile                        # language-aware targets
├── .editorconfig
├── .gitignore                      # language-aware + OS / editor sweep
├── .gitattributes                  # line-ending + binary detection + linguist hints
├── .pre-commit-config.yaml         # whitespace + syntax + gitleaks
├── .env.example                    # only if your project uses env vars
├── pyproject.toml                  # or package.json / go.mod / Cargo.toml
├── tests/                          # smoke test scaffold for your language
│
├── .claude/
│   ├── settings.json               # permission posture: Cautious / Read-only / Trusted-dev / Bypass
│   ├── bootstrap.json              # cached interview answers; makes re-runs safe
│   ├── rules/
│   │   ├── workflow.md             # the core discipline (always)
│   │   ├── workflow-todos.md       # deferred ideas as files (always)
│   │   ├── workflow-security.md    # security review on risky changes (always)
│   │   ├── best-practices.md       # naming, DI, idioms (always)
│   │   ├── layered-architecture.md # 4-Layer DDD / 3-Tier / SPA / skipped if flat
│   │   ├── workflow-changes.md     # opt-in: customer-visible surfaces stay in sync
│   │   ├── workflow-metrics.md     # opt-in: cardinality + naming discipline
│   │   └── ui-components.md        # opt-in: catalog of canonical UI affordances
│   └── prompts/
│       └── 1737000000.bootstrap_project.md   # timestamped prompt history
│
└── .docs/
    ├── adrs/                       # Nygard-format Architecture Decision Records
    │   ├── README.md
    │   └── 0000-adr-template.md
    ├── todos/                      # one file per deferred idea
    │   └── README.md
    └── security/
        └── methodology.md          # OWASP Top 10 + OWASP LLM Top 10 review rubric
```

Nothing in this tree is mandatory. The interview decides what lands.

---

## The interview

Fourteen questions, grouped into six tiers. Each tier shapes a different layer of the scaffold.

| Tier | Questions | What it controls |
| --- | --- | --- |
| **Bootstrap behaviour** | Q1 name, Q2 permission posture | `CLAUDE.md` title; `.claude/settings.json` variant |
| **Project identity** | Q3 language, Q4 architecture | `.gitignore` / manifest / linter / `Makefile` family; `layered-architecture.md` variant |
| **Project shape** | Q5 web surface, Q6 LLM in request path, Q7 env vars | Security rubric sub-sections; `.env.example` |
| **Feature gates** | Q8 customer-visible surfaces, Q9 UI components, Q10 governed metrics | Opt-in workflow rules |
| **Repository metadata** | Q11 license, Q12 contributions | `LICENSE` variant; `CONTRIBUTING.md` + `CODE_OF_CONDUCT.md` |
| **Free-form** | Q13 run instructions, Q14 anything else | `CLAUDE.md` extra sections |

**Permission posture (Q2) is asked early on purpose** — the chosen posture takes effect for the rest of the bootstrap's file writes, so the agent stops prompting before it starts writing.

### Permission postures at a glance

| Posture | Default mode | When to pick it |
| --- | --- | --- |
| **Cautious** | Every action prompts | Shared, team, or open-source projects. |
| **Read-only autonomy** | Read-only Bash and git pre-allowed; writes prompt | Investigation-heavy work; you want friction-free reads. |
| **Trusted dev** | Read-only + safe git + language-specific build/test pre-allowed; force-push and hard-reset still deny | Daily dev on a project you own. |
| **Full bypass** | No prompts at all | Dedicated dev VMs, containers, or trusted personal workspaces only. |

All four variants pin `model: claude-opus-4-7`.

---

## The ownership model (why re-runs are safe)

Every file the bootstrap writes is classified in [Part 3's decision matrix](./AGENTIC_BOOTSTRAP.md). This is the contract that makes the bootstrap re-runnable forever.

| Category | What it means | Re-run behaviour | Examples |
| --- | --- | --- | --- |
| **Canon** | The bootstrap is the source of truth. | Silently overwrites if different. | Rules, ADR template, security methodology. |
| **Mixed** | You layer project-specific additions on top of the baseline. | Diff and ask: *overwrite / keep / merge*. | `settings.json`, `.gitignore`, `Makefile`, linter configs. |
| **Sacred** | You own it after the first write. | Never touched on re-run. | `CLAUDE.md`, `README.md`, code, real ADRs, todos. |
| **New each run** | Fresh file every time. | No overwrite question. | Timestamped prompt files. |

> **The contract:** *"Feel free to re-run the bootstrap whenever the file is updated. Nothing you own will be touched."*

Cached interview answers live in `.claude/bootstrap.json` (committed, shared with the team). On re-run the agent only asks you about *new* questions added to a newer version of the bootstrap. Switching machines, switching teammates, switching agents — the answers come with the repo.

---

## Design principles

These are load-bearing. They shape every decision in the artifact.

1. **Single file, self-contained.** No `curl`, no `WebFetch`, no template registry. The Apache 2.0 license text is embedded verbatim. The agent that runs it might not have network tools.
2. **Project-agnostic.** No domain-specific bleed. The patterns survive; the example project that birthed them does not appear.
3. **Interactive interview, not static dump.** Opt-in files appear only when the matching flag is yes.
4. **Agent-executable.** The file is itself a playbook. Part 1 reads top-to-bottom and tells the agent what to do.
5. **Easy to update.** Edit the file in place; the next bootstrap reflects the change. No version registry, no internal changelog — `git log` is canonical.
6. **Idempotent re-runs.** State lives in `.claude/bootstrap.json`; ownership is encoded in the matrix.
7. **Conventions over preferences.** The bootstrap is opinionated. That's the point.

---

## How it's structured

[AGENTIC_BOOTSTRAP.md](./AGENTIC_BOOTSTRAP.md) is one file in six parts, roughly 3,220 lines:

| Part | What it contains |
| --- | --- |
| **1. Operator playbook** | Steps 0–8 the agent follows: detect run mode → sanity check → interview → decide → write → prompt + persist → commit → push → report. |
| **2. Interview** | 14 questions across 6 tiers. |
| **3. Decision matrix** | 30+ files with Type / Trigger / Re-run policy. |
| **4. File templates** | Embedded templates for every file, including 4 architecture variants, 5 language variants across 4 template families, 4 permission posture variants, 3 license variants. |
| **5. Post-bootstrap checklist** | User-facing next steps. |
| **6. How to extend** | Maintainer's manual: coupled surfaces, recipes for adding rules / files / flags, conditional syntax, quality bar. |

### Template syntax

Only two conditional forms exist throughout the file:

- **`{{PLACEHOLDER}}`** — direct substitution from an interview answer or computed value (e.g. `{{CURRENT_YEAR}}`, `{{COPYRIGHT_HOLDER}}`).
- **`{{IF_FLAG}}<line content>`** — keep the line when `FLAG` is true; drop it when false.

Multi-value flags (`LANG`, `ARCH`, `LICENSE`, `POSTURE`) use **separate labelled template sections** — never nested conditionals. The syntax stays scannable on a 3,000-line file.

---

## Extending the bootstrap

[Part 6](./AGENTIC_BOOTSTRAP.md) is the maintainer's manual. The short version: every new file or rule touches up to five coupled surfaces — the interview, the matrix, the template section, the dispatch logic for multi-value flags, and the `bootstrap.json` schema. Keep them in lockstep.

Adding a new language means writing variants in all four `LANG`-driven template families — `.gitignore`, manifest + tests, linter configs, `Makefile` — plus the Trusted-dev posture allow-list addendum.

To evolve the bootstrap, you edit the file. Your next run reflects the change. Your previous projects pick it up on their next re-run.

---

## Status & scope

- **Verified on Claude Code.** The bootstrap mentions `AskUserQuestion` (Claude Code-specific) but says *"or plain prose questions"* as a fallback. Untested with Cursor / Codex CLI / Aider — refinement likely needed once those are exercised.
- **CI is intentionally out of scope.** GitHub Actions / GitLab CI / Bitbucket Pipelines are host-specific; the bootstrap stays portable. CI is a post-bootstrap step you own.
- **Pre-commit hooks are universal-only.** `.pre-commit-config.yaml` ships whitespace + syntax + secrets scanning; language-specific hooks are added when your toolchain stabilises.

---

## Prior art

The bootstrap doesn't invent the conventions it encodes — it synthesises them. **The novel contribution is the single paste-and-go file with idempotent re-runs.** The components stand on the shoulders of:

- **Architecture Decision Records** — Michael Nygard's original ADR pattern (2011) and the [MADR](https://adr.github.io/madr/) format.
- **OWASP Top 10** and **OWASP LLM Top 10** — the security methodology's rubric framing.
- **[Keep a Changelog](https://keepachangelog.com)** — the `CHANGELOG.md` format.
- **Prompt journaling** — the community pattern of capturing the prompt alongside the diff.
- **[EditorConfig](https://editorconfig.org)**, **[pre-commit](https://pre-commit.com)**, **[gitleaks](https://github.com/gitleaks/gitleaks)** — universal tooling baked into the scaffold.

If you've been doing this manually on every project, the bootstrap is the file that ends that.

---

## Files in this repo

- [AGENTIC_BOOTSTRAP.md](./AGENTIC_BOOTSTRAP.md) — **the artifact.** ~3,220 lines, six parts. This is what you hand to your agent.
- [README.md](./README.md) — this file.
- [LICENSE](./LICENSE) — MIT.

---

> **Try it now.** `cd` into any repo, paste [AGENTIC_BOOTSTRAP.md](./AGENTIC_BOOTSTRAP.md) into your agent, and say *"follow this bootstrap."* Two minutes to the day-one discipline you'd otherwise grow over six months — one painful lesson at a time.
