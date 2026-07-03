# Quickstart — 60 seconds

```text
# 1. Drop the file
curl -O https://raw.githubusercontent.com/sciensoft/agentic-bootstrap/main/AGENTIC-BOOTSTRAP.md

# 2. Tell your agent
> follow AGENTIC-BOOTSTRAP.md to bootstrap this repo

# 3. Answer 17 questions
# 4. Get a disciplined, tool-agnostic scaffold + first commit
```

That's it. The agent interviews you, scaffolds [`AGENTS.md`](https://agents.md) + `.agents/rules/` + `.docs/{adrs,prompts,todos,security}/`, writes per-tool adapter files for whichever agentic assistants you use (Claude Code, Cursor, Aider, Codex CLI, OpenCode, Continue.dev, Windsurf, GitHub Copilot), and commits everything in one focused commit.

**If the interview shows up as plain text** when your host has picker UI (Claude Code VSCode extension, Continue.dev, Cursor), paste this nudge:

```text
> use your interactive prompts (pickers, multi-select) — one call per question
```

## What you'll be asked

The interview is 17 questions, grouped into six tiers. None are trick questions; sensible defaults exist for every one. Skim the highlights:

- **Q1 — Project name + one-line purpose.** The cold-start brief title.
- **Q2 — Which agentic assistants?** Multi-pick. Decides which adapter files get written.
- **Q3 — Agent autonomy posture?** Cautious / read-only / trusted-dev / bypass. The chosen intent fans out into every tool's native permission config (`.claude/settings.json`, `.cursor/settings.json`, `.aider.conf.yml` autonomy keys, `.codex/config.toml`, `.continue/config.json` tools block, `.windsurf/settings.json`).
- **Q4 — Primary language or content type.** Eleven named examples — Python, TypeScript, Go, Rust, C# / .NET, Java, Ruby, PHP, Kotlin, Swift, Markdown / docs-as-code — plus *something else*. First-class scaffolds today: Python, TypeScript, Go, Rust; everything else gets a generic fallback. Drives the manifest, linter configs, test scaffold, and `Makefile`.
- **Q5 — Architecture shape.** 9 options including 4-Layer DDD, Hexagonal, Microservice, Vertical Slice, Monorepo, Serverless. Drives the layered-architecture rule.
- **Q6–Q8 — Project shape.** Web app? LLM in the request path? Env vars / secrets?
- **Q9–Q13 — Feature gates.** Customer-visible surfaces? UI component vocabulary? Governed metrics? Testing discipline? Shared-frontend propagation? (All opt-in.)
- **Q14–Q15 — Repository metadata.** License + contributions.
- **Q16–Q17 — Run instructions + anything else load-bearing.**

The full interview reference is in [`AGENTIC-BOOTSTRAP.md` Part 2](./AGENTIC-BOOTSTRAP.md).

## What you'll get

```text
your-repo/
├── AGENTS.md                       # primary cross-tool brief — purpose, rules, run, architecture
├── README.md · LICENSE · SECURITY.md
│
├── .agents/                        # tool-agnostic spine
│   ├── rules/
│   │   ├── workflow.md             # prompt → ADR → telemetry → commit → push
│   │   ├── workflow-todos.md
│   │   ├── workflow-security.md
│   │   ├── workflow-testing.md     # (if TESTING)
│   │   ├── best-practices.md       # refined from current sources if your agent has web search
│   │   └── layered-architecture.md # variant per Q5
│   └── bootstrap.json              # interview answers — re-runnable
│
│   # Per-tool adapters — only the ones you picked get written:
├── CLAUDE.md                       # Claude Code adapter (if Claude)
├── .claude/settings.json           # Claude permission posture
├── .cursor/rules/agents.mdc        # Cursor adapter (if Cursor)
├── .aider.conf.yml                 # Aider adapter (if Aider)
├── .continue/config.json           # Continue.dev (if Continue.dev)
├── .windsurfrules                  # Windsurf (if Windsurf)
├── .github/copilot-instructions.md # Copilot (if Copilot)
│
└── .docs/
    ├── prompts/                    # timestamped, one per request
    ├── adrs/                       # slim Nygard format with Mermaid diagrams
    ├── todos/                      # deferred ideas, one file per entry
    └── security/methodology.md     # OWASP + LLM-specific rubric
```

Plus a `tests/` scaffold, language-specific manifest + lint configs + `Makefile`, and the workflow-rule files referenced from `AGENTS.md`.

## Why this, not Cookiecutter / copier / a hand-typed agent brief?

| | This bootstrap | Cookiecutter / copier | Hand-typed agent brief |
| --- | --- | --- | --- |
| Output | A disciplined working repo + first commit | A working repo | A brief file for one tool (`AGENTS.md` / `CLAUDE.md` / `.cursor/rules/` / `.aider.conf.yml` / …) |
| Tool support | 8 agentic assistants out of the box, all in sync | None (it's a templating tool) | One — whichever brief you wrote |
| Discipline encoded | Workflow + ADRs + tests + security + TODOs + telemetry | Whatever the template authored | Whatever you typed |
| Architectures | 9, with diagram picker, ports/adapters family, microservice + vertical slice | Whatever the template authored | None |
| Live best-practices | Refined from current web sources for your stack | Frozen at template-author time | Frozen at typing time |
| Permission posture | One intent fans out to per-tool autonomy config (Claude / Cursor / Aider / Codex / Continue.dev / Windsurf) | Not addressed | Not addressed |
| Onboarding cost | One file. One prompt. 60 seconds. | Install Cookiecutter, find a template, hope it's current. | Hours of typing, no proof. |
| Re-runnable | Yes — idempotent; existing projects pick up new conventions on re-run | Usually no | No |

Cookiecutter / copier solve a different problem (template engines for many use cases). This bootstrap is specifically about *making an AI-coding workflow a first-class artefact of the project* — and works across the eight major agentic tools, not just one. A hand-typed brief (whether you wrote it as `AGENTS.md`, `CLAUDE.md`, a `.cursor/rules/` file, an `.aider.conf.yml`, or anything else) is the closest comparison, but it doesn't bring the rules, the security rubric, the testing discipline, the ADR culture, the diagram picker, the cross-tool adapter generation, or the per-tool permission posture fan-out — you'd be reinventing all of that for each tool, in each tool's own dialect.

## Examples — see the output before running

Browse three fully-bootstrapped projects under [`examples/`](./examples/):

- [`examples/python-4layer-ddd/`](./examples/python-4layer-ddd/) — Python + 4-Layer DDD
- [`examples/typescript-vertical-slice/`](./examples/typescript-vertical-slice/) — TypeScript + Vertical Slice
- [`examples/go-microservice/`](./examples/go-microservice/) — Go + Microservice

Each example shows the actual file tree the bootstrap produced for that stack, with the key files (AGENTS.md, the rule files, a representative source file or two, a test).

## Re-running on an existing project

The bootstrap is **idempotent**. Run it again any time you want to pick up new rules, new architecture variants, or a new tool adapter from a newer version of the file:

```text
> follow AGENTIC-BOOTSTRAP.md to bootstrap this repo
```

The agent reads `.agents/bootstrap.json` to skip questions you've already answered. Only newly-added interview keys get re-asked. The version delta is named in the Step 8 report so you see what's changed since your last run — driven by [`CHANGELOG.md`](./CHANGELOG.md).

## Audit-only mode (doctor)

If you want to check an existing project's compliance with the rules without writing anything, ask:

```text
> run bootstrap-doctor against this repo
```

You get a structured report: missing rule files, stale `bootstrap.json` keys, security audits overdue, refinement marker still `stub`, ADR index out of sync. No writes. See [`AGENTIC-BOOTSTRAP.md` § Step 0 → doctor mode](./AGENTIC-BOOTSTRAP.md) for the full report shape.

## Contributing

See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for how to add new architecture variants, tool adapters, language scaffolds, or feature gates to the bootstrap itself.

## License

MIT — see [`LICENSE`](./LICENSE).
