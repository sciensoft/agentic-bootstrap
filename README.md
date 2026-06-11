# Agentic Bootstrap

**One markdown file. Any agentic coding assistant. One prompt. Your repo grows the discipline a Senior Engineer would have set up on day one — tool-agnostic, cross-stack, idempotent.**

[**🌐 agentic-bootstrap.md →**](https://agentic-bootstrap.md) · [Quickstart](./QUICKSTART.md) · [Examples](./examples/) · [Changelog](./CHANGELOG.md) · [Contribute](./CONTRIBUTING.md)

*By [Alexandre Souza](https://github.com/AlexzSouz) · [MIT licensed](./LICENSE) · [github.com/sciensoft/agentic-bootstrap](https://github.com/sciensoft/agentic-bootstrap)*

---

Every project grows good engineering habits eventually — usually after the third *"why did we do it that way?"*, the first security scare, the fifth time the agent re-derives the same context. **The bootstrap installs them on day one.**

Hand [`AGENTIC-BOOTSTRAP.md`](./AGENTIC-BOOTSTRAP.md) to your coding agent, say *"follow this bootstrap"*, and walk away with the discipline most projects don't get for months: an `AGENTS.md` brief every assistant reads, workflow rules under `.agents/rules/`, ADRs for load-bearing decisions, a prompt history that captures the *why*, a security rubric you actually walk, a testing pyramid (opt-in), permissions matched to risk, and a thin adapter file for each of the eight agentic tools the project supports.

No templates to clone. No CLI to install. No external fetches. Just one file your agent reads end-to-end.

## Quick start

```text
# 1. Drop the file
curl -O https://raw.githubusercontent.com/sciensoft/agentic-bootstrap/main/AGENTIC-BOOTSTRAP.md

# 2. Tell your agent
> follow AGENTIC-BOOTSTRAP.md to bootstrap this repo

# 3. Answer 17 questions
# 4. Get a disciplined, tool-agnostic scaffold + first commit
```

> **Before you run — two things to verify.**
>
> 1. **Capable model.** Best results with Claude Sonnet / Opus, GPT-4 class, Gemini 1.5 / 2.x, full DeepSeek-V3, or Qwen 2.5 Coder 32B+. Smaller distilled reasoning models may skip steps in this multi-step playbook; use a bigger model for this one-time scaffold.
> 2. **Context window fits ~80k tokens.** The bootstrap reads at ~80k tokens. Verify your model + runtime + tool can carry that much in one window. Common failure modes: model architecturally capped below 128k (most Qwen 2.5 builds, Codestral, Phi-4); runtime serving a smaller context than the model supports (Ollama, vLLM, llama.cpp all have separate caps); agent re-sending the file every turn vs chunked tool reads. When the math doesn't fit, use a hosted API for this one-time scaffold — the cost is rounding error against a single dev day.

Full quickstart with the question breakdown, the produced tree, and the positioning table: [`QUICKSTART.md`](./QUICKSTART.md).

## What lands in your repo

| Habit | What lands |
| --- | --- |
| **Cross-tool brief every assistant reads.** | `AGENTS.md` at the root — purpose, rules, run, architecture map. The eight major agentic tools either read it natively (Codex CLI, OpenCode) or read a thin adapter that points back to it (Claude Code, Cursor, Aider, Continue.dev, Windsurf, Copilot). |
| **Decisions don't fade into commit messages.** | `.docs/adrs/` with a Nygard-format template. Every load-bearing decision gets its own file — with a Mermaid diagram picked from 22+ types based on the decision's shape. |
| **The *why* lives next to the *what*.** | `.docs/prompts/<ts>.<slug>.md` — every artifact-producing request leaves a prompt file. `git log` + prompts reconstruct the whole story. |
| **Tests ship with the code (opt-in).** | `.agents/rules/workflow-testing.md` — pyramid-shaped, mock at boundaries not internals, bug fixes start with a failing regression test. Tests + code land in the same commit, always. |
| **Security gets a checklist, not a vibe.** | `.docs/security/methodology.md` — OWASP Top 10 + OWASP LLM Top 10 rubric you walk before merging anything risky. |
| **Best practices, refined for your stack.** | When your agent has web search, the bootstrap probes current sources for your language + framework and synthesises a `best-practices.md` with inline citations. Falls back to a stub with per-agent enablement guidance when search isn't available. Never blocked. |
| **Deferred ideas don't drown in a ticket backlog.** | `.docs/todos/` — one file per idea, each with a *Revisit when* trigger. Sweep when a commit satisfies it; `git rm` to retire. |
| **Permissions match risk (Claude Code).** | Four `.claude/settings.json` postures with explicit deny-patterns for `git push --force`, `rm -rf`, `git reset --hard`. |
| **Boring conventional files exist from day one.** | `.gitignore`, `.editorconfig`, `Makefile`, linter configs, `SECURITY.md`, `CHANGELOG.md` — language-aware where it matters. |
| **Re-runs never break what you own.** | The Canon / Mixed / Sacred [ownership model](#the-ownership-model-why-re-runs-are-safe) — the bootstrap evolves; your edits stay safe. |

## Examples — see the output before running

Three fully-bootstrapped projects browseable under [`examples/`](./examples/):

- [`examples/python-4layer-ddd/`](./examples/python-4layer-ddd/) — Python + 4-Layer DDD
- [`examples/typescript-vertical-slice/`](./examples/typescript-vertical-slice/) — TypeScript + Vertical Slice
- [`examples/go-microservice/`](./examples/go-microservice/) — Go + Microservice

Each example shows the actual file tree the bootstrap produces for that stack, with the key files filled in.

## Why one file, not a template or CLI

You've seen the alternatives. None of them stick:

| You don't want | Because |
| --- | --- |
| A git template you copy and then drift from | Templates rot the second you fork them. |
| A CLI tool with its own version, plugins, and breaking changes | Another dependency to track for something you do once per project. |
| A 12-step blog post you skim and half-apply | You'll skip the parts you don't understand and regret it later. |
| A static dump where you delete the irrelevant 60% | Wasted effort; opinionated noise. |

The bootstrap is **a single file your agent reads and follows**. It interviews you, picks only the parts that match your project, and writes them. To evolve it, you edit the file. That's the whole tool.

A side-by-side comparison vs Cookiecutter / copier / a hand-typed agent brief lives in [`QUICKSTART.md` § Why this, not Cookiecutter](./QUICKSTART.md).

## Works with

| Tool | Adapter |
| --- | --- |
| **Claude Code** | `CLAUDE.md` adapter + `.claude/settings.json` (permission posture) |
| **Cursor** | `.cursor/rules/agents.mdc` |
| **Aider** | `.aider.conf.yml` (with `read:` list) |
| **OpenAI Codex CLI** | reads `AGENTS.md` natively — no adapter file |
| **OpenCode** | reads `AGENTS.md` natively — no adapter file |
| **Continue.dev** | `.continue/config.json` rules entry |
| **Windsurf** | `.windsurfrules` |
| **GitHub Copilot** | `.github/copilot-instructions.md` |

The tool-agnostic spine (`AGENTS.md` + `.agents/rules/`) is written every time; adapter files are written only for the tools you pick during the interview.

## The interview

Seventeen questions, six tiers. The full list is in [`AGENTIC-BOOTSTRAP.md` Part 2](./AGENTIC-BOOTSTRAP.md); the highlights:

| Tier | Questions | What it controls |
| --- | --- | --- |
| **Bootstrap behaviour** | Q1 name, Q2 `AGENTS_USED`, Q3 autonomy posture | `AGENTS.md` title; which per-tool adapters get written; per-tool permission-posture configs |
| **Project identity** | Q4 language, Q5 architecture | `.gitignore` / manifest / linter / `Makefile` family; `layered-architecture.md` variant (one of 9) |
| **Project shape** | Q6 web surface, Q7 LLM in request path, Q8 env vars | Security rubric sub-sections; `.env.example` |
| **Feature gates** | Q9 customer-visible surfaces, Q10 UI components, Q11 governed metrics, Q12 testing, Q13 shared-frontend propagation | Opt-in workflow rules |
| **Repository metadata** | Q14 license, Q15 contributions | `LICENSE` variant; `CONTRIBUTING.md` + `CODE_OF_CONDUCT.md` |
| **Free-form** | Q16 run instructions, Q17 anything else | `AGENTS.md` extra sections |

## Architectures supported

Nine, with a Q5 disambiguation that routes topology answers (microservice, monorepo, modular monolith, serverless) and vocabulary aliases (hexagonal, ports-and-adapters, clean, onion, bare *DDD*) to the right slot.

| Slot | Shape |
| --- | --- |
| `4_LAYER_DDD` | presentation → application → domain ← infrastructure + shared |
| `HEXAGONAL` | domain at the centre with `ports/` + symmetric `adapters/primary/` + `adapters/secondary/` (covers Hexagonal / Clean / Onion family) |
| `MICROSERVICE` | 4-Layer DDD internals + cross-service conventions (health/readiness, retries, circuit breakers, tracing, contract tests, deploy manifest) |
| `VERTICAL_SLICE` | features at the top level; each owns its own thin layers; features may only import from `shared/` |
| `3_TIER` | presentation / business / data |
| `SPA` | components / pages / hooks / services / types |
| `FLAT` | no layering; modules organised by topic |
| `MONOREPO` | top-level workspace; sub-projects pick their own internal architecture |
| `SERVERLESS` | handlers/{http,events,scheduled}/ + thin `lib/` core |

## The ownership model (why re-runs are safe)

Every file the bootstrap writes is classified in [Part 3's decision matrix](./AGENTIC-BOOTSTRAP.md). This is the contract that makes the bootstrap re-runnable forever.

| Category | What it means | Re-run behaviour | Examples |
| --- | --- | --- | --- |
| **Canon** | The bootstrap is the source of truth. | Silently overwrites if different. | Rules, ADR template, security methodology. |
| **Mixed** | You layer project-specific additions on top of the baseline. | Diff and ask: *overwrite / keep / merge*. | `settings.json`, `.gitignore`, `Makefile`, linter configs. |
| **Sacred** | You own it after the first write. | Never touched on re-run. | `AGENTS.md`, `CLAUDE.md`, `README.md`, code, real ADRs, todos. |
| **New each run** | Fresh file every time. | No overwrite question. | Timestamped prompt files. |

> **The contract:** *"Feel free to re-run the bootstrap whenever the file is updated. Nothing you own will be touched."*

Cached interview answers live in `.agents/bootstrap.json` (committed, shared with the team). On re-run the agent only asks you about *new* questions added to a newer version of the bootstrap, and surfaces the version delta in the Step 8 report so you see what changed — driven by [`CHANGELOG.md`](./CHANGELOG.md).

## Audit-only mode (doctor)

If you want to check an existing project's compliance with the rules without writing anything:

```text
> run bootstrap-doctor against this repo
```

You get a structured report: missing rule files, stale `bootstrap.json` keys, security audits overdue, refinement marker still `stub`, ADR index out of sync. No writes. Full report shape in [`AGENTIC-BOOTSTRAP.md` § Step 0 → doctor mode](./AGENTIC-BOOTSTRAP.md).

## Design principles

These shape every decision in the artifact:

1. **Single file, self-contained.** No `curl`, no `WebFetch` for the bootstrap itself. The agent that runs it might not have network tools.
2. **Tool-agnostic spine.** `AGENTS.md` + `.agents/rules/` is the source of truth; per-tool adapters are thin pointers.
3. **Project-agnostic.** No domain-specific bleed.
4. **Interactive interview, not static dump.** Opt-in files appear only when the matching flag is yes.
5. **Agent-executable.** The file is itself a playbook. Part 1 reads top-to-bottom and tells the agent what to do.
6. **Easy to update.** Edit the file in place; the next bootstrap reflects the change. The change log lives in `CHANGELOG.md`.
7. **Idempotent re-runs.** State lives in `.agents/bootstrap.json`; ownership is encoded in the matrix.
8. **Failure-safe refinement.** Web-search-driven best-practices refinement falls back to a sensible stub when search isn't available — the bootstrap never blocks.
9. **Conventions over preferences.** The bootstrap is opinionated. That's the point.

## How it's structured

[`AGENTIC-BOOTSTRAP.md`](./AGENTIC-BOOTSTRAP.md) is one file in six parts:

| Part | What it contains |
| --- | --- |
| **1. Operator playbook** | Steps 0–8 the agent follows: detect run mode → sanity check → interview → decide → write → refine best practices → prompt + persist → commit → push → report. |
| **2. Interview** | 17 questions across 6 tiers, plus a Q5 disambiguation table. |
| **3. Decision matrix** | 40+ files with Type / Trigger / Re-run policy. |
| **4. File templates** | Embedded templates for every file, including 9 architecture variants, 5 language variants × 4 template families, 4 permission posture variants, 3 license variants, 5 per-tool adapter variants. |
| **5. Post-bootstrap checklist** | User-facing next steps. |
| **6. How to extend** | Maintainer's manual. The dedicated `CONTRIBUTING.md` at the repo root covers contribution patterns in more depth. |

## Files in this repo

- [`AGENTIC-BOOTSTRAP.md`](./AGENTIC-BOOTSTRAP.md) — **the artifact.** What you hand to your agent.
- [`QUICKSTART.md`](./QUICKSTART.md) — 60-second quickstart for human readers.
- [`CHANGELOG.md`](./CHANGELOG.md) — version history.
- [`CONTRIBUTING.md`](./CONTRIBUTING.md) — how to extend the bootstrap.
- [`examples/`](./examples/) — three fully-bootstrapped sample projects.
- [`docs/`](./docs/) — the landing-page source.
- [`README.md`](./README.md) — this file.
- [`LICENSE`](./LICENSE) — MIT.

## Prior art

The bootstrap doesn't invent the conventions it encodes — it synthesises them. **The novel contribution is the single paste-and-go file with idempotent re-runs, eight-tool adapter generation, and live best-practices refinement.** The components stand on the shoulders of:

- **Architecture Decision Records** — Michael Nygard's original ADR pattern (2011) and the [MADR](https://adr.github.io/madr/) format.
- **[AGENTS.md](https://agents.md)** — the emerging cross-tool agent-brief convention.
- **OWASP Top 10** and **OWASP LLM Top 10** — the security methodology's rubric framing.
- **[Keep a Changelog](https://keepachangelog.com)** — the `CHANGELOG.md` format.
- **Hexagonal / Ports and Adapters** (Alistair Cockburn), **Clean Architecture** (Robert Martin), **Onion Architecture** (Jeffrey Palermo), **Vertical Slice Architecture** (Jimmy Bogard).
- **[Mermaid](https://mermaid.js.org)** — the diagram-as-code system that powers the ADR diagram picker.
- **[EditorConfig](https://editorconfig.org)**, **[pre-commit](https://pre-commit.com)**, **[gitleaks](https://github.com/gitleaks/gitleaks)** — universal tooling baked into the scaffold.

If you've been doing this manually on every project, the bootstrap is the file that ends that.

---

> **Try it now.** `cd` into any repo, hand [`AGENTIC-BOOTSTRAP.md`](./AGENTIC-BOOTSTRAP.md) to your agent, and say *"follow this bootstrap."* Sixty seconds to the day-one discipline you'd otherwise grow over six months — one painful lesson at a time.
