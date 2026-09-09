# Agentic Bootstrap

Single-file scaffold that hands AI coding agents a disciplined workflow.

## Purpose

Agentic Bootstrap is a one-file artifact (`AGENTIC-BOOTSTRAP.md`) an engineer pastes into a fresh repo so an AI coding agent (Claude Code, Cursor, Aider, Codex CLI, Continue, Windsurf, Copilot, OpenCode) can scaffold the project with a consistent posture: a tool-agnostic spine in `AGENTS.md` + `.agents/rules/`, per-tool adapters that point back at it, ADRs under `.docs/adrs/`, a security methodology under `.docs/security/`, and conventional repo files (`README`, `LICENSE`, `SECURITY.md`, `CHANGELOG.md`, `.gitignore`, `.editorconfig`, etc.) sized to the answers from a short interview. The project is *self-applied*: this very repo is bootstrapped from its own `AGENTIC-BOOTSTRAP.md`.

## Rules

### Always

Five things, on every turn, whichever agent is reading this.

- **Confirm the reading before building.** When a request is short and admits more than one reading, say in one line which reading you are acting on, then act. Before the work, not after it. A wrong reading is cheap to correct at one line and expensive to correct at one commit.
- **Answer the request that was made.** Not the adjacent one you can answer more impressively. If a rule below would have you produce an artifact the request did not ask for, the request wins and the artifact waits to be offered.
- **Declare the task boundary.** State in one line at the top of each turn whether it continues the current task or opens a new one — e.g. *"Task: continuing 'add password reset' — refinement to the previous turn"* or *"Task: new — 'wire up SES'. Previous task committed at abc1234, closed"*. A commit closes the current task by default; the next turn is presumed new unless it is a fix-up on the just-committed work. Explicit user signals (*"now let's..."*, *"moving on..."*, *"unrelated:"*, *"different topic:"*) always open a new task. When the signal is ambiguous, **continue** — the cost of a mis-continuation is a longer prompt file; the cost of a mis-new-task is directory spam.
- **One prompt file per task**, under `.docs/prompts/`, amended as the task continues (not one per turn); the work itself; a commit (granularity to judgement — often one per task, sometimes two when refinements deserve separation); a push. Stage by explicit path, never `git add -A`.
- **Capture deferrals** as one file per idea under `.docs/todos/`, and remove an entry in the commit that satisfies its trigger. This especially applies to **proactive-discipline rules** (testing, metrics, telemetry — see below): when the user says *"skip this for now"*, don't drop it silently — capture a todo with a revisit trigger like *"next commit that touches this subsystem"* so the discipline gets picked up when the deferral's premise no longer holds.

### Read before you act

The files under `.agents/rules/` are **reference, and are deliberately not preloaded**. Read the file when its trigger fires, and read it *before* acting rather than after: each exists to stop a specific mistake that is expensive to undo, and reaching for one after the code is written is the failure it was meant to prevent. If a trigger is ambiguous, read the file.

Rules come in two flavors. **Reactive** rules (security, changes, UI, layered architecture, frontend) fire only when their specific surface is being touched — read them then, follow them then. **Proactive-discipline** rules (testing, metrics, telemetry) fire on *every* relevant work unit when opted in — read them once per session and apply the discipline on every code change, not only when the discipline's artifact is already being touched. If a project opted into metrics and you're building a new subsystem, ship events for it in the same commit; don't wait to be asked.

| When | Read |
| --- | --- |
| the full per-task loop, once per session before the first commit | [`workflow.md`](.agents/rules/workflow.md) |
| a new dependency, module, layer or pattern | [`workflow.md`](.agents/rules/workflow.md) §2 (ADR) |
| a new, changed or deleted code path, or a new failure branch | [`workflow.md`](.agents/rules/workflow.md) §3 (telemetry) |
| writing Python or Markdown content (this project's two authoring modes) | [`best-practices.md`](.agents/rules/best-practices.md) |
| auth, input, SQL, output encoding, headers, secrets, logging, rate limits, deps | [`workflow-security.md`](.agents/rules/workflow-security.md) |
| writing or removing a deferred-idea entry | [`workflow-todos.md`](.agents/rules/workflow-todos.md) |
| anything a user can see (README, QUICKSTART, `docs/index.html`, `AGENTIC-BOOTSTRAP.md` prose) | [`workflow-changes.md`](.agents/rules/workflow-changes.md) |

Each row states the *condition* and the *file*, not what the file is about. If two rows fit, read both.

### Measurement habit

The rules budget is small (a few kilobytes of always-loaded material) but three larger line items compete for the same window: the conversation itself (grows every turn), MCP tool schemas (varies by connected servers), and per-host system prompts. Check `/context` occasionally when a session starts feeling forgetful; the culprit is usually one of those three, not this file.

Architecture decisions and their trade-offs live in [`.docs/adrs/`](.docs/adrs/) — read these before making structural changes.

## Run

`python scripts/lint_bootstrap.py`; open `docs/index.html` for the landing-page preview

## Architecture map

[Short pointer to where the main pieces live. Add an `ARCHITECTURE.md` at the repo root if the project grows enough to need its own tree + diagram.]

## Conventions (summary)

See [`.agents/rules/best-practices.md`](.agents/rules/best-practices.md) for full detail.

## Maintenance notes

The bootstrap file IS the artifact; modify only via deliberate PRs that bump the `<!-- bootstrap-version: -->` header. The lint script at `scripts/lint_bootstrap.py` validates four cross-reference invariants and runs in CI on every PR.
