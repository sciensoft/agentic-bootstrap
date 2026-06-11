# Add a lint check that validates the Template Index stays in sync with `### Template:` positions

**Area**: tooling / drift detection

**Refs**:
- [`.docs/adrs/0008-offset-read-template-index.md`](../adrs/0008-offset-read-template-index.md) — the decision this lint protects.
- [`scripts/lint_bootstrap.py`](../../scripts/lint_bootstrap.py) — the four-check lint that runs in CI; this would become check #5.
- [`AGENTIC-BOOTSTRAP.md`](../../AGENTIC-BOOTSTRAP.md) Part 4 — Template Index subsection.

## Context

ADR-0008 added a Template Index to the start of Part 4 mapping ~80 templates to `start → end` line offsets. The offsets are accurate at the time of writing, but every future edit to the file — adding a new template, expanding a section by even a few lines, renumbering Q-questions — risks drifting the index out of sync. Drift is silent: smart agents read at the wrong offsets and may read partial / mismatched template content. The drift safeguard inside the index ("if the offset doesn't land on `### Template:`, re-grep") is a band-aid; the real fix is to enforce sync in CI.

Add a fifth check to [`scripts/lint_bootstrap.py`](../../scripts/lint_bootstrap.py):

1. Grep `AGENTIC-BOOTSTRAP.md` for every `^### Template: ` heading position.
2. For each, compute the next template's `start - 1` as that template's `end` (or use Part 5's start - 1 for the last one).
3. Parse the Template Index table from the file.
4. Compare each row's `start → end` against the derived value.
5. Fail with a precise diff showing which rows are stale and what the correct values are.

A nice-to-have addition: emit the corrected table as `stderr` output so a maintainer can `sed`-replace it into the file as a one-line fix. Drift becomes a 30-second resolution instead of a hunt-and-edit chore.

## Deferred because

The index is correct as-of the commit that introduced it (and lint passes today). The drift problem is forward-looking — it shows up the first time someone edits Part 4 without re-running the offsets. Building the check now is preemptive but valuable; deferring it lets us ship ADR-0008's benefit immediately without bundling tooling work.

## Revisit when

- The next PR that edits Part 4 — that's when drift first becomes a real risk.
- OR when a contributor adds a new template (the most likely source of drift).
- OR within two weeks of ADR-0008 landing, regardless. The check is small (~30 lines of Python) and ships discipline that compounds.
