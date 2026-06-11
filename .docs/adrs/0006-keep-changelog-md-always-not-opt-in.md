# 6. Keep `CHANGELOG.md` always-written, not gated by `CONTRIB`

- **Status**: Accepted (after considering an opt-in alternative)
- **Date**: 2026-06-11

## Context

During a review of the Part 3 decision matrix, the question came up: should `CHANGELOG.md` be demoted from `Always | Sacred` to `Opt-in (CONTRIB)`? The argument for opt-in is real — internal/personal projects rarely cut formal releases, the file rots into "Initial commit" forever, and the existing `CONTRIB` flag (Q15) is a strong signal (`yes` = open-source norms expected, `no` = internal). Symmetry with how `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` are already gated would be elegant.

## Decision

Keep the current matrix entry: `CHANGELOG.md | Always | universal; Keep a Changelog format | Sacred`. The bootstrap writes a stub on first run; the Sacred re-run policy means the file is never re-created if the user deletes it. Cost is one ~10-line stub on first run; benefit is that every bootstrapped project has the convention available without having to answer a question about it.

## Consequences

- The bootstrap stays aligned with design principle 9 ([`README.md` "Design principles"](../../README.md)) — *"Conventions over preferences."* CHANGELOG is a convention.
- Symmetry with `.gitignore`, `.editorconfig`, `SECURITY.md` — all "boring conventional files that exist from day one."
- Doctor mode flagging a missing CHANGELOG as drift is correct behaviour. The Sacred policy stops the bootstrap from re-creating a file the user has explicitly deleted, which means a `CONTRIB=no` user who never wants the file pays the cost exactly once.
- Trade-off accepted: a `CONTRIB=no` project that *does* eventually want a changelog will need to recreate it manually (or re-run with Sacred behavior bypassed). Rare enough not to justify a second interview question.
- Alternative considered and rejected: a derived flag `CHANGELOG = CONTRIB` that gates the file without a new question. Cleverness without payoff — the always-on cost is one stub.

Related: [ADR-0003](./0003-standardize-on-changelog-md.md) (the rename), [ADR-0004](./0004-single-file-agent-executable-delivery-model.md) (the conventions-over-preferences principle in context).
