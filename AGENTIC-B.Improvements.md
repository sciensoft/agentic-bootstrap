# agentic-bootstrap — improvements, applied and ready to port

Assessment written 2026-08-31 from a generated repository (Sciensoft
Technologies: Go, `LAYOUT=agents`, `AGENTS_USED=[CLAUDE]`). The measurements are
this project's; the ratio they expose is a property of the emitted rule set, not
of the project, so it should reproduce anywhere the bootstrap has run with a
similar answer set.

Sections 1 to 5 are the assessment, section 1 including **how to reproduce the
measurement without repeating the mistake made the first time**. **Section 6 is
the implementation**, applied by hand to the source repository on 2026-08-31 and
written so it can be lifted into the generator: generated repositories should
then take it by re-running the bootstrap rather than by hand editing. Section 7
is the part of the context budget the generator does not control, which turns out
to be most of it. Section 9 records what the second application of this document
(`mcp-connectors`, 2026-09-02) added on top: mechanical enforcement of the
trigger index, and §6.4's checks as a make target — both ready to lift into the
generator alongside section 6.

Token figures were corrected on 2026-09-01 against a real measurement. The first
pass estimated them and was wrong by 28% in the direction that understated the
problem. Section 1 explains how, because any agent redoing this will reach for
the same wrong shortcut.

---

## 1. What was measured

`CLAUDE.md` `@`-imports `AGENTS.md` and every file under `.agents/rules/`. All of
it is in the context window before the user types anything.

| File | Bytes | What it mostly is |
| --- | ---: | --- |
| `ui-components.md` | 30,896 | **87% is the catalog**, a lookup table of affordances |
| `workflow.md` | 30,147 | **49% is the ADR section**, of which 12,751 bytes is the Mermaid diagram-type picker |
| `best-practices.md` | 13,041 | Language idioms, consulted when writing code |
| `AGENTS.md` | 12,278 | Identity, run instructions, hard constraints |
| `workflow-frontend.md` | 10,930 | Consumer-sweep procedure |
| `workflow-todos.md` | 7,750 | Entry shape for deferred ideas |
| `layered-architecture.md` | 7,670 | Layer definitions and dependency arrows |
| `frontend-visibility.md` | 6,951 | Mostly a per-agent tooling table; one row applies |
| `workflow-security.md` | 5,785 | Surface triggers pointing at `methodology.md` |
| `workflow-changes.md` | 4,671 | Surface map |
| `workflow-metrics.md` | 4,167 | The project has no metering at all |
| **Total** | **135,049** | **≈47,000 tokens** (measured, see below) |

Roughly **100KB of the 135KB is reference rather than behaviour**: material to
consult when a specific condition holds, not instructions that change what the
agent does on an arbitrary turn.

### How to reproduce this

The always-loaded set is defined by what the per-agent file imports, so take the
list from the file rather than assuming it:

```bash
# 1. what is actually loaded
grep '^@' CLAUDE.md | sed 's/^@//' > /tmp/imports.txt

# 2. bytes per file, and the total
while read -r f; do printf '%-46s %7d\n' "$f" "$(wc -c < "$f")"; done < /tmp/imports.txt
awk '{s+=$1} END {print s}' < <(while read -r f; do wc -c < "$f"; done < /tmp/imports.txt)

# 3. where the bulk sits inside the two biggest files
awk '/^## /{if(h)printf "  %-52s %6d\n",h,b; h=$0; b=0} {b+=length($0)+1}
     END{if(h)printf "  %-52s %6d\n",h,b}' .agents/rules/workflow.md
```

Step 3 is the one that matters. A file being large is not an argument; a file
being 87% lookup table is. Both of the headline findings came from sectioning the
two biggest files, not from their totals.

### The calibration trap, and how to avoid it

**Do not convert bytes to tokens with a guess.** The first pass here used the
usual bytes ÷ 4 rule of thumb for English prose and reported ~34,000 tokens.

`/context` in Claude Code reports the real per-file figures. After the change it
gave `AGENTS.md` 4,300 tokens and `CLAUDE.md` 217, so **4,517 tokens for 12,987
bytes: 2.88 bytes per token, not 4.00.**

Rule sets tokenize denser than prose. Markdown tables, backticked paths, code
fences, kebab-case filenames and heading punctuation all split into more tokens
per byte than running text. Applying the measured 2.88 to the original 135,049
bytes gives **~47,000 tokens**, not ~34,000.

The percentage cut survives a wrong ratio, because the error appears in both the
numerator and the denominator. **The absolute does not, and the absolute is what
makes the case.** So: measure one known file with `/context`, derive the ratio,
then apply it. Or quote bytes only and say so.

## 2. The problem is not only token cost

The always-loaded set is overwhelmingly procedural. Write a prompt file, consider
an ADR, update the catalog, sweep the consumers, check telemetry levels, commit,
push. When a short request arrives, a large share of attention goes to satisfying
that procedure rather than to reading the request.

The observed failure mode is output that is well-formed, correctly
cross-referenced, compliant with every rule, and answers a question the user did
not ask.

Two instances from the session that produced this document:

- *"The boxes are taking too much space which could fit more keywords"* was read
  as a request for capacity rather than for less visual weight. It produced a
  compliant prompt file, a commit body and two comparison tables, and had to be
  redone the next turn.
- *"Let's plan some improvements"* produced an ADR, an index row, a todo entry, a
  prompt file, a commit and a push, when the user had asked to assess.

This matters for how the fix is framed. Treated purely as a cost-saving exercise,
a smaller rule set would keep the same ratio of procedure to comprehension and
reproduce the same failure more cheaply.

## 3. Proposal: two tiers

Let the generator decide which tier a rule belongs to, rather than emitting
everything into `CLAUDE.md`.

**Tier 1, always loaded. Target under 10KB.** Only what changes behaviour on an
arbitrary turn:

- project identity and the hard constraints that make a wrong move expensive
- the per-turn loop: prompt file, commit, push, sweep todos
- the trigger index (below)

**Tier 2, loaded when a trigger fires.** Everything reference-shaped, no longer
`@`-imported.

Skills are one mechanism for this, and they are the wrong one to reach for first.
They add directories, frontmatter and a discovery step, and whether a skill fires
depends on its `description` matching the request. **The simpler mechanism needs
no new infrastructure: leave every rule file where it is, stop importing it, and
put a trigger index in the always-loaded file naming the path and the condition.**
The agent reads the file when the trigger fires. The trigger lines are then
*guaranteed* to be in context rather than dependent on a match, which is the
weaker link in the skills version.

Reach for skills only when a rule needs to be shared across repositories, or when
its body is large enough that even the trigger line wants a summary.

| Read | When |
| --- | --- |
| `ui-components.md` | touching any UI affordance |
| `workflow.md` §2 | a new dependency, module or pattern |
| `workflow.md` §3 | a new or changed code path, or a new failure branch |
| `best-practices.md` | writing code in the project language |
| `layered-architecture.md` | adding a module, moving code between layers |
| `workflow-security.md` | auth, input, SQL, secrets, headers, rate limits, deps |
| `workflow-frontend.md` | shared component, partial or styling token |
| `workflow-changes.md` | a change a user can see |
| `frontend-visibility.md` | diagnosing a visual bug |
| `workflow-todos.md` | writing or removing a deferred-idea entry |

### The trigger index is the load-bearing part

A skill that is never invoked is a rule that silently stopped applying, which is
worse than a rule that costs tokens. The triggers therefore stay in Tier 1 as
imperatives, so the pointer is always seen even though the body is not:

> Touching any UI affordance? Load `ui-catalog` first. Never invent a variant.
> Adding a dependency, module or pattern? Load `adr-authoring` before committing.

Roughly fifteen lines. This is the part to review hardest, and the part to test:
the honest measure of the split is whether the right skill fires unprompted on a
request that should trigger it.

### Where the index lives: the agnostic brief, not the per-agent file

The trigger index is not Claude-specific, so it does not belong in `CLAUDE.md`.
It goes in `AGENTS.md`, which every agent reads, alongside the always-on rules.
Per-agent files stay stubs whose only job is to pull the brief in using whatever
mechanism that host provides.

That is the general principle the generator should follow: **anything true for
every agent lives in the agnostic brief; a per-agent file carries only what is
genuinely specific to that host**, such as a tool or a permission it alone has.
Emitting the same guidance into `CLAUDE.md`, `AGENTS.md` and a Cursor rules file
is how they drift.

It also replaces rather than adds. `AGENTS.md` already carried a `## Rules`
section listing every rule with a descriptive summary, written as though all of
them applied at once. Rewriting that section as the trigger index made the brief
*smaller* while making it operational.

## 4. Three changes independent of tiering

1. **Per-task artefacts, not per-turn.** `workflow.md` requires a prompt file and
   a commit for every turn that touches a file. One piece of work spread over
   fifteen refinement turns produces fifteen prompt files and fifteen commits.
   That is a large amount of generated prose per unit of change, and it crowds
   out the work. Require the prompt file per *task*, amended as the task
   continues, with commit granularity left to judgement.

2. **Confirm the reading before building.** Add to Tier 1: when a request is
   short and admits more than one reading, state the chosen reading in one line
   before doing the work, not after. Cheap, and it catches the dominant failure.

3. **Emit only what the project uses.** `workflow-metrics.md` is present because
   the interview answered `METRICS: true`, but the project has never had
   metering. Treat such answers as provisional and drop a rule whose subject has
   not materialised, or re-ask on a later bootstrap run.

## 5. Expected effect

- Fixed load drops from ~47,000 tokens to 4,517 measured. The user's request
  becomes the loudest thing in the window rather than the twelfth.
- Reference material gets better rather than worse: freed from the always-on
  budget, the catalog and the practices can grow without a per-session cost.
- The failure mode inverts. Today a rule is always present and often irrelevant;
  afterwards a rule is always relevant and occasionally missed. That trade is
  worth taking only with the trigger index in place.
- Migration is mechanical and reversible. No file moves and none is rewritten:
  each `@`-import becomes a row in the trigger index. Restoring the old
  behaviour is putting the imports back.

## 6. What was changed

Applied by hand to the source repository. Two files changed, no rule file moved,
edited or deleted, and the change is reversible by restoring the imports.

| | bytes | tokens | how the tokens were got |
| --- | ---: | ---: | --- |
| Before: `AGENTS.md` + 10 `@`-imported rules | 135,049 | ~47,000 | 135,049 ÷ 2.88, the measured ratio |
| After: `AGENTS.md` 12,432 + `CLAUDE.md` 555 | **12,987** | **4,517** | `/context`, directly: 4,300 + 217 |
| Cut | 90.4% | **90.4%** | |

The after-figure is measured, not derived. The before-figure is derived from it,
because the imports were already gone by the time `/context` was run: 2.88 bytes
per token is the ratio the measured pair implies, and it is applied to the
original byte count. Anyone repeating this on an untouched repository should run
`/context` **before** changing anything and get both figures directly.

### 6.1 The per-agent file becomes a stub

Every `@`-import except the brief is removed. This is the whole per-agent file
now, and the closing paragraph is deliberate: it is what stops the file
re-accumulating guidance that belongs in the brief.

```markdown
# <AGENT> adapter

The brief is [`AGENTS.md`](./AGENTS.md), and it is agent-agnostic: purpose, run
instructions, architecture map, the always-on rules, the trigger index for
`.agents/rules/`, and the hard constraints. It is imported below.

@AGENTS.md

Nothing else belongs in this file. It exists because <AGENT> reads
`<AGENT_FILE>`, not because <AGENT> needs different instructions. Anything true
for every agent goes in `AGENTS.md`; put something here only when it is genuinely
specific to this host, such as a tool or a permission it alone has.
```

Where the host has no import mechanism, emit a one-line instruction to read
`AGENTS.md` first instead. Nothing else about the design changes.

### 6.2 The brief gains an `Always` block and a trigger index

These **replace** the existing `## Rules` section, which listed every rule with a
descriptive summary phrased as though all of them applied at once. Replacing
rather than appending is why the brief got smaller.

The `Always` block is emitted verbatim for every project:

```markdown
### Always

Four things, on every turn, whichever agent is reading this.

- **Confirm the reading before building.** When a request is short and admits
  more than one reading, say in one line which reading you are acting on, then
  act. Before the work, not after it. A wrong reading is cheap to correct at one
  line and expensive to correct at one commit.
- **Answer the request that was made.** Not the adjacent one you can answer more
  impressively. If a rule below would have you produce an artifact the request
  did not ask for, the request wins and the artifact waits to be offered.
- **Every artifact-producing task** gets a prompt file under `.docs/prompts/`,
  the work itself, a single commit, and a push. **One prompt file per task**,
  amended as the task continues, not one per turn. Stage by explicit path, never
  `git add -A`.
- **Capture deferrals** as one file per idea under `.docs/todos/`, and remove an
  entry in the commit that satisfies its trigger.
```

The index header is emitted verbatim, and its rows are emitted per rule the
interview turned on:

```markdown
### Read before you act

The files under `.agents/rules/` are **reference, and are deliberately not
preloaded**. Read the file when its trigger fires, and read it *before* acting
rather than after: each exists to stop a specific mistake that is expensive to
undo, and reaching for one after the code is written is the failure it was meant
to prevent. If a trigger is ambiguous, read the file.
```

| Emitted when | When (row) | Read |
| --- | --- | --- |
| `UI_COMPONENTS` | adding or changing any UI affordance | `ui-components.md` |
| always | a new dependency, module, layer or pattern | `workflow.md` §2, the ADR section |
| always | a new, changed or deleted code path, or a new failure branch | `workflow.md` §3, telemetry |
| always | the full per-task loop, once per session before the first commit | `workflow.md` |
| always | writing `<LANG>` | `best-practices.md` |
| `ARCH` set | adding a module, or moving code between layers | `layered-architecture.md` |
| `POSTURE` | auth, input, SQL, output encoding, headers, secrets, logging, rate limits, deps | `workflow-security.md` |
| `FRONTEND` | shared component, partial or styling token | `workflow-frontend.md` |
| `CHANGES` | anything a user can see | `workflow-changes.md` |
| `FRONTEND` | diagnosing or reporting a visual bug | `frontend-visibility.md` |
| always | writing or removing a deferred-idea entry | `workflow-todos.md` |
| `METRICS` | adding, changing or removing a metered event | `workflow-metrics.md` |

Each row states the condition and what the file stops, not what the file is
about. "Clone the canonical shape, never invent a variant" earns its place;
"catalog of canonical UI affordances" does not, because it does not tell the
reader when they need it.

### 6.3 Rules whose subject never materialised

`workflow-metrics.md` stays on disk but is left out of the index, with one line
saying why: the interview answered `METRICS: true` and the project has never had
metering. Better than deleting, which the next bootstrap run would undo.

The generator should either re-ask such answers on a later run, or emit the rule
unindexed with that note, so a false positive in the interview costs a line
rather than a section.

### 6.4 Checks worth running after the change

```bash
# nothing orphaned: every rule file is indexed, or deliberately noted as not
for f in .agents/rules/*.md; do
  grep -q "$(basename "$f")" AGENTS.md || echo "ORPHANED  $f"
done

# every path the brief links actually resolves
grep -o '(\.agents/rules/[a-z-]*\.md)' AGENTS.md | tr -d '()' | sort -u |
  while read -r p; do [ -f "$p" ] || echo "BROKEN  $p"; done

# the budget, in bytes and in calibrated tokens
b=$(( $(wc -c < AGENTS.md) + $(wc -c < CLAUDE.md) ))
echo "$b bytes  ~$(( b * 100 / 288 )) tokens at the measured 2.88 bytes/token"
```

The first two catch the failure this design introduces: a rule that stopped
applying because nothing points at it any more. The third keeps the budget a
measured number rather than a remembered one, since rule files grow. Worth
emitting as a `make` target so it is run rather than recalled.

### 6.5 The real test

Not the token count. **Whether the right file gets read unprompted when its
trigger fires.** If an agent starts editing a component without opening the UI
rule first, the index is too quiet and that row needs sharpening. That is the
failure this design trades for, and it is the thing to watch in the first week.

## 7. The budget the generator does not control

`/context` on the session that produced this document, taken **after** the change:

| Category | Tokens | Share of window |
| --- | ---: | ---: |
| Messages, the conversation itself | 539.5k | 53.9% |
| MCP tool definitions | 65.9k | 6.6% |
| System tools | 33.6k | 3.4% |
| Memory files, including this repo's brief | 5.2k | 0.5% |
| System prompt | 4k | 0.4% |
| Skills | 2.9k | 0.3% |

Of those 5.2k memory-file tokens, the repository's own instructions are **4,517**:
`AGENTS.md` 4,300 and `CLAUDE.md` 217. The remainder is an unrelated memory index.

Two conclusions, and both belong here because they change what "fix the context"
means for anyone applying this upstream.

**After the change, the generator's slice is small.** 4,517 tokens is about 4% of
the non-conversation overhead and 0.8% of the window. Trimming `AGENTS.md`
further has sharply diminishing returns. The 90% cut was the win, and there is no
second cut of that size available inside the generator's output.

**The two large line items belong to the user, not the generator.** The
conversation is roughly 120× the rules, and length is the main reason a long
session stops honouring constraints stated early in it. MCP tool definitions are
roughly 15× the rules, and in the measured session several came from servers that
never successfully connected. Shorter sessions per topic, and disconnecting MCP
servers a repository does not use, both beat any further rule trimming by an
order of magnitude.

The generator should say this rather than leave it implied. A bootstrap that
trims its own output to 4k tokens and stays silent about a 66k MCP payload has
optimised only the part it can see, and a user reading a "90% context reduction"
claim will reasonably expect the session to feel different. It will not, unless
the other two are addressed as well.

A sensible thing for the bootstrap to emit is a short note in the brief telling
the reader to check `/context` occasionally and naming these three line items, so
the measurement habit outlives this document.

### 7.1 The MCP payload, itemised

The 65.9k is not one thing, and only part of it is reachable from the repository.
Measured in the same session, per server:

| Server | Tools | Tokens | Declared in |
| --- | ---: | ---: | --- |
| `claude_ai_Microsoft_365` | 41 | 33,298 | claude.ai connector, account-level |
| `claude_ai_Gmail` | 29 | 20,590 | claude.ai connector, account-level |
| `playwright` | 45 | 9,305 | the repository's `.mcp.json` |
| `claude_ai_Hugging_Face` | 4 | 2,525 | claude.ai connector, account-level |
| `chrome-devtools` | — | 0 | `.mcp.json`, failed to connect all session |

**86% of it is account-level connectors, not project configuration.** Only the
9,305 tokens of `playwright` were declared by anything in the repository, and it
was not used once in the session that measured it: the browser work went through
`chromium` and the DevTools Protocol directly.

### 7.2 The levers, with their exact shapes

Taken from the settings schema at
`https://json.schemastore.org/claude-code-settings.json`, not from memory. The
two families have different shapes and different reach, and confusing them wastes
an afternoon.

**Project servers, from `.mcp.json`.** Flat arrays of names, where a name is the
key under `mcpServers`:

```jsonc
// .claude/settings.json — governs .mcp.json only
{
  "disabledMcpjsonServers": ["playwright", "chrome-devtools"],
  "enabledMcpjsonServers":  ["some-server-you-do-want"],
  "enableAllProjectMcpServers": false
}
```

`enableAllProjectMcpServers` is the odd one of the three and deserves its own
note, because it is **an approval switch, not a load switch**. A server declared
in `.mcp.json` is not trusted just because the file names it: `.mcp.json` is
checked into the repository, so trusting it means running somebody else's process
on your machine. Until it is approved the server sits in `⏸ Pending approval` and
contributes nothing, tokens included. That is why a repository can declare two
servers and show neither in `/context`.

The three keys are one decision at three grains:

| Key | Grain | Effect |
| --- | --- | --- |
| `enableAllProjectMcpServers: true` | blanket | every server in `.mcp.json` is approved, now and in future |
| `enabledMcpjsonServers: [...]` | per server | only the named ones are approved |
| `disabledMcpjsonServers: [...]` | per server | the named ones are rejected outright |

**Prefer the named allowlist over the blanket switch.** With `true`, a server a
teammate adds to `.mcp.json` in some later commit is approved before anyone has
looked at it: the branch is pulled, the session restarts, the process runs. With
`enabledMcpjsonServers` the approval is by name, so a new entry still stops and
asks. The cost of the safer form is one line per server, once.

This matters more than it looks, because these entries are commands. A real one
from the repository measured here reads
`npx chrome-devtools-mcp@latest`: unpinned, so it fetches and executes whatever
was published most recently, every session. Its neighbour pins
`@playwright/mcp@0.0.77` and does not. **A generator emitting `.mcp.json` should
pin versions and should not emit `enableAllProjectMcpServers: true`**, for the
same reason the security rule it already ships treats a new dependency as a
reviewable event.

**Every scope, including account connectors.** Arrays of *objects*, one of three
forms, matched by name, exact stdio command, or URL pattern:

```jsonc
// .claude/settings.local.json — personal, gitignored
{
  "deniedMcpServers": [
    { "serverName": "claude_ai_Microsoft_365" },
    { "serverCommand": ["npx", "chrome-devtools-mcp@latest"] },
    { "serverUrl": "https://*.example.com/*" }
  ]
}
```

`serverName` is constrained to `^[a-zA-Z0-9_-]+$`, so it takes the normalised
name (`claude_ai_Gmail`) rather than the display name ("claude.ai Gmail"), whose
dots and spaces would not match. Verify against `claude mcp list` before relying
on it; that mapping is the one thing here not confirmed by measurement.

Two properties make the denylist the useful lever rather than the allowlist: its
description says it blocks *across all scopes*, and **denylist beats allowlist**
where a server appears on both.

**On whether this needs enterprise settings:** the schema marks
`allowManagedMcpServersOnly` and `allowAllClaudeAiMcps` as *"(Managed settings
only)"*. It does **not** mark `allowedMcpServers` or `deniedMcpServers`, and
`allowManagedMcpServersOnly`'s own description says *"deniedMcpServers still
merges from all sources"*. So the denylist should be honoured from ordinary
project or local settings. There is no plain "load only what `.mcp.json`
declares" switch; `allowManagedMcpServersOnly` is the nearest thing and it is
managed-only.

### 7.3 What the generator should do with this

It cannot turn off somebody's account connectors, and it should not try. What it
can do:

- **Emit a `.mcp.json` containing only servers the project actually needs**, with
  a comment beside each saying roughly what it costs. A browser MCP is ~9k tokens
  for 45 tools; a project that drives a browser through CDP directly, as this one
  does, should not be paying it. An unused entry is not free, and an entry that
  fails to connect is worse because it looks configured.
- **Emit the denylist as a commented example** in `settings.local.json`, or name
  it in the brief, so a reader who has connectors they never use in this
  repository knows the lever exists. Most will not.
- **Pin every version in `.mcp.json`, and approve by name rather than in bulk.**
  `enabledMcpjsonServers` listing the servers explicitly costs one line each and
  keeps a later addition to the file from being trusted unseen;
  `enableAllProjectMcpServers: true` trades that away for nothing the project
  needs.
- **Put MCP in the same measurement habit as the rules.** The `make` target in
  §6.4 counts the brief's bytes; the number that matters is the whole window, and
  `/context` is where it is.
- **Say the proportion out loud.** A bootstrap that trims its output from 47k to
  4.5k and stays silent about 66k of tool schemas has been honest about its own
  work and misleading about the outcome. The improvement is real; on its own it
  will not make a session feel different.

## 8. What this does not explain

This addresses what is measurable inside a generated repository. It does not
account for quality problems in projects that carry no such rule set. If the
same regression appears there, it is not this.

## 9. Hardening the trigger index: additions from the second application

Applied to `mcp-connectors` on 2026-09-02, after porting sections 6 and 7.2
there. Both additions aim at §6.5's watch item — whether the right rule file
gets read unprompted when its trigger fires — and both cost context only in the
turn a trigger actually fires, so they serve the same brief as the split
itself: rules that support the work without standing in its window.

### 9.1 Path-matched hooks make the path-shaped rows mechanical

The trigger index depends on the model noticing the trigger. For rows whose
condition is a file path, that dependence can be removed: a `PreToolUse` hook
on `Edit|Write` reads the tool payload, matches the file path against the
index's path-shaped rows, and injects a one-line
`hookSpecificOutput.additionalContext` naming the rule file(s) to read first.
Silent on non-matching paths; a session-keyed sentinel dir under `$TMPDIR`
dedupes so each rule reminds at most once per session — a long UI sweep costs
one line, not one per edit.

Concretely, in `mcp-connectors`: `.claude/hooks/rule-reminder.sh` (a `case`
ladder over relative paths, ~50 lines, `jq` for payload parsing) plus one
`hooks.PreToolUse` block in the committed `.claude/settings.json` invoking it
via `bash "${CLAUDE_PROJECT_DIR:-.}/..."`. Rows enforced there: shared
components → the UI catalog + consumer-sweep rules, `desktop/**` → the
privilege rule, migrations → security, the URL-contract package and
`.env.example` → surface-sync, the events file → metering, todos → the todo
shape, and non-test `*_service.go` / `*_repository.go` / `*_handler.go` →
testing.

Placement is the part that generalises. Hooks are host machinery, not
guidance, so they belong in the per-agent layer — which is exactly what
§6.1's closing paragraph permits: the agnostic *contract* stays in
`AGENTS.md`; the hook merely enforces it on hosts that have hooks. The
generator should emit the script and settings block from the same interview
answers that emit the index rows, giving a `case` arm only to rows a path can
prove. Rows that are not path-shaped (writing the language at all, the
ADR/library questions, the per-task loop) stay attentional by design — do not
force them.

Verification shape, worth emitting into the generator's own checks: pipe-test
the script with synthesized payloads (a matching path, the same path again for
the dedupe, a deliberately excluded path such as `*_test.go`, a no-match), then
prove the wired hook fires once in the live harness with a temporary sentinel
prefix on the command. Limits to state honestly: the script is bash, so
Linux/macOS/WSL — a Windows-native host needs Git Bash or a PowerShell port —
and it converts only the path-shaped rows; §6.5's watch item stays open for
the rest.

### 9.2 §6.4 as an emitted make target

The three checks in §6.4 were run by hand there and recalled from this
document. That is the failure §6.4 itself warns about, so they became a
`rules-check` target in the repository Makefile: orphaned-rule scan,
broken-link scan, and the measured byte/token budget, exiting non-zero when
either scan finds anything. Tested red against a planted orphan file, not just
green. The generator should emit this target (creating a minimal Makefile
where none exists) so the index is checked by habit — and by CI, eventually —
rather than by memory.

### 9.3 A deviation from §7.3 worth recording

`mcp-connectors` put the `deniedMcpServers` list in the committed project
`.claude/settings.json`, not the gitignored `settings.local.json` §7.3
suggests — the user wanted every clone to get the trim — and kept the
product's own connector URLs off the list, because in that repository they are
the thing under development. Both halves generalise: the local-settings
commented example remains the right *default* emission (account connectors
are personal), a team can deliberately promote it to project scope since the
denylist merges from all sources either way, and a repository must never deny
the servers it exists to build.
