# Doctor mode: upstream-tool-format check

**Area**: Doctor mode / per-tool adapters

**Refs**:
- [`AGENTIC-BOOTSTRAP.md`](../../AGENTIC-BOOTSTRAP.md) — Part 1 §Doctor mode (10-row check table)
- [`quarterly-adapter-refresh.md`](./quarterly-adapter-refresh.md) — ritual counterpart to this automated check
- [`community-driven-adapter-contributions.md`](./community-driven-adapter-contributions.md) — once per-tool maintainers exist, they're also signal-providers for this check

## Context

Doctor mode currently audits internal consistency (layout, sentinel files, `bootstrap.json` freshness, architecture rule freshness, refinement marker, audit cadence, adapter coverage, ADR index, TODOs hygiene, prompt-file presence — 10 rows in the check table). It does NOT audit whether the *adapter files themselves* are still correct against the tool's current upstream format.

Failure mode: a user re-runs an older bootstrap version, gets a `.cursor/rules/agents.mdc` that's syntactically valid but uses a since-deprecated key. Doctor mode reports "all green" because the file is present and parses. The user has no signal anything is wrong until the tool surfaces a warning (which not all tools do).

A new Doctor sub-check (becomes row 11) would, for each tool in `AGENTS_USED`:

1. Fetch the tool's current config-schema docs / changelog / settings example (via WebFetch when host supports it; if no fetch capability, skip with an Informational note — same fall-through pattern Step 4b uses for the best-practices refinement).
2. Diff the adapter the *current* bootstrap version would write against the adapter currently on disk.
3. Flag delta with severity. Critical: tool deprecated this key entirely. Stale: better key available. Informational: unchanged.

This catches upstream-tool drift between [`quarterly-adapter-refresh.md`](./quarterly-adapter-refresh.md) passes — the automated half of the per-tool adapter treadmill. Each catches what the other misses: the ritual catches *known* changes you read in changelogs; the Doctor check catches changes you missed or that happened mid-quarter.

## Deferred because

Real engineering pass — needs:
- A per-tool "where to fetch" mapping (URLs, sections to extract).
- WebFetch wiring in the Doctor mode section of `AGENTIC-BOOTSTRAP.md`.
- A diff/report shape (probably a small new severity tier in the existing report-shape block).
- Test coverage for the no-WebFetch fallback.

Out of scope for the post-launch community phase that's the current focus. The quarterly refresh is a sufficient first-line defence; this enhancement is the second-line defence to ship once the project has more maintenance bandwidth or once a real reported case justifies the work.

## Revisit when

Whichever comes first:
- A user reports a real broken adapter from upstream drift between two quarterly refreshes (proves the gap exists in practice); or
- The project reaches 50+ stars / first 5 outside contributors (signal that maintenance volume justifies automation); or
- **2026-12-01** — fallback calendar date so it doesn't drift forever.
