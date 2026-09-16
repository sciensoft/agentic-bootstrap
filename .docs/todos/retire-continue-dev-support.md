# Retire Continue.dev support

- **Area:** Per-tool adapters (Q2 `AGENTS_USED` set, Continue.dev variant)
- **Refs:** [`AGENTIC-BOOTSTRAP.md`](../../AGENTIC-BOOTSTRAP.md) Q2 answer space + Part 3 matrix + Part 4 `.continue/config.json` template; [`README.md`](../../README.md); [`QUICKSTART.md`](../../QUICKSTART.md); [`SECURITY.md`](../../SECURITY.md); [`examples/`](../../examples/) three `best-practices.md` sample files. Landing page (`docs/index.html`) already had Continue.dev removed in the 2026-09-16 rebuild.

## Context

Continue.dev the product was discontinued in mid-2026 — its team joined Cursor. The landing page dropped mentions of Continue.dev during the context-management-overhaul rebuild, but the bootstrap generator, the human-facing README/QUICKSTART/SECURITY, three example projects' `best-practices.md`, and the `AGENTS_USED` interview enum still fully support the adapter. If a user picks Continue.dev on the interview today, `.continue/config.json` still gets emitted for a product that no longer exists.

Retirement scope, when picked up:

- Drop `CONTINUE` from Q2's `AGENTS_USED` value set + its Part 1 dispatch entry.
- Remove the `.continue/config.json` Part 4 template + Part 3 matrix row + Template Index row.
- Trim the AGENTS.md template intro that names Continue.dev among the supported hosts.
- Remove Continue.dev references from best-practices refinement guidance (§ *Enable refinement*) and its per-agent enablement matrix.
- README/QUICKSTART/SECURITY: strip Continue.dev from the supported-agents lists.
- Three `examples/*/.agents/rules/best-practices.md` sample files: same.
- `.agents/bootstrap.json` template's answers schema: drop `CONTINUE` from the `AGENTS_USED` enum.
- CHANGELOG entry naming the retirement + a bootstrap-version bump (removing a supported agent is a real interview-shape change, worth its own dated release).

## Deferred because

Landing-page-side removal was in scope for the context-management overhaul (Continue.dev on a landing page implied active support the product no longer offers). The wider generator + docs sweep is a separate concern — it changes the Q2 answer space and removes a Part 4 template, and would muddle the context-management merge if bundled in. Also low-urgency: existing projects that already have `.continue/config.json` keep working; the only harm is new projects picking a discontinued adapter, and the emitted file itself is inert without a Continue.dev install to consume it.

## Revisit when

Any of:

- The next full bootstrap re-run cycle when a Q2 answer-space change is otherwise justified (e.g. adding a new agent) — bundle the retirement in the same commit so the Q2 sub-table is only touched once.
- A concrete report from a user who picked Continue.dev on a fresh bootstrap and hit friction.
- **2026-12-01** onward, regardless of user reports — even without friction, the "supported hosts" list ages badly with a defunct product on it, and six months from discontinuation is a reasonable retirement floor.
