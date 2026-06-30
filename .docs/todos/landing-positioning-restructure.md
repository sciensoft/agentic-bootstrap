# Landing-page positioning restructure — full backlog

- **Area:** Landing-page positioning ([`docs/index.html`](../../docs/index.html)) — follow-up to [[reposition-as-engineering-memory-system-with-ab-test]]
- **Refs:** [ADR-0009](../adrs/0009-reposition-as-engineering-memory-system-with-ab-test.md), [`docs/index.html`](../../docs/index.html), [`docs/index.v1.html`](../../docs/index.v1.html) (rollback snapshot), [`README.md`](../../README.md), [`.docs/prompts/1782833006.reposition_memory_system_ab_test.md`](../prompts/1782833006.reposition_memory_system_ab_test.md)

## Context

Commits `7a247eb` and `9f5af86` repositioned the **hero** of the landing page to the engineering-memory framing and instrumented an A/B/C test (currently pinned to B while baseline data is collected). The README pivoted with it — new lede, aha-quote, three-paragraph problem→substrate→solution block, outcome-first `What lands` table. But two independent reviewers raised *structural* points that the hero-only edit does not address — the rest of the page still leads with mechanism, lists artifacts before justifying them, and reads as "an AI tool" rather than "an engineering practice." Continuing to add new content on top of the existing flow makes the page longer and less readable; the right move is **restructuring** (reorder, reframe, cut), not stacking.

This file is the working backlog for that restructuring — *one* tracked artifact for the whole initiative rather than 14 fragmented TODOs. Items get marked **Done** inline as they ship; the file `git rm`s when every item is closed. The form bends the usual "one-file-per-idea" convention because the initiative IS one idea with many sub-items; splitting would lose the dependency graph between them.

### Improvement inventory

Legend: ✅ done · 🟡 partial · ⬜ open · ❓ blocked / needs input.

| # | Item | Status | Notes |
| --- | --- | --- | --- |
| 1 | Hero aha-moment + A/B/C variant test, gtag-instrumented | ✅ | commits `7a247eb`, `9f5af86`; B forced via `FORCE_VARIANT` |
| 2 | README "What lands" table reframed to outcome-first | ✅ | commit `7a247eb` — header `Habit` → `What the repo gains` |
| 3 | Landing meta `<title>` / description / OG tags aligned to memory framing | ✅ | commit `7a247eb` (variant-B-aligned copy for crawlers) |
| 4 | **Problem section** after the hero on the landing page | ⬜ | ~150 words, body form, no artifact talk; sets up the substrate section |
| 5 | **Substrate section** — the five memory types mapped to artifacts | ⬜ | episodic (prompts) / semantic (ADRs) / working (TODOs) / procedural (rules + best-practices) / evaluative (security). This IS the gestalt shift made visible. |
| 6 | **Workflow vignette** — "the OAuth story" | ⬜ | Request → prompt file lands → ADR lands → TODO lands for the deferred refresh-token rotation → 6 months later a new agent reads the ADR and inherits the context for free. Both reviewers explicitly asked for a real-example section. |
| 7 | Reframe `A repo that knows its own rules` to outcome-first | ⬜ | Currently lists artifacts mechanically; same pattern as the README table reframe but on the landing page. |
| 8 | Reframe `Process, encoded` to memory-led | ⬜ | Currently mechanism-led; reads as feature list. Rewrite so each item is "the repo gains X" not "the bootstrap installs Y". |
| 9 | **Comparison section** vs Cursor Rules / Copilot instructions / Claude skills / AGENTS.md alone | ⬜ | Defends the *more than a brief* claim. Both reviewers flagged this is missing. Tabular form, 4–5 axes. |
| 10 | Cut / consolidate `Postures` section | ⬜ | Currently duplicates README content. Shrink to one paragraph + link, or fold into a "Trust on your terms" line in the new substrate section. |
| 11 | Cut / consolidate `Architectures supported` | ⬜ | Currently a full section listing nine architecture variants. Shrink to one sentence + click-through to the README's full table. |
| 12 | **Reorder** sections per the new outline (see below) | ⬜ | Current flow is mechanism-first throughout; proposed flow is value-first with mechanism entering only after the visitor has reason to care. |
| 13 | Re-instrument new CTAs with `data-ab-event` once items 4–9 add them | ⬜ | Follow-on for any new clickable surfaces (vignette CTA, comparison-section CTA, etc.) — same `gtag` event pattern as the hero buttons. |
| 14 | Resolve open second-reviewer carryovers | ❓ | (a) What did they want **removed entirely** from the page? (b) What does **"ADs"** stand for in their closing question? Both unresolved from the original PDF; needs user re-read or paste. |
| 15 | Final readability pass — total word-count delta, scroll depth, contrast on new sections | ⬜ | After 4–13 land; verify the net effect is *clearer*, not just *different*. |

### Proposed restructured outline

The order each section serves the visitor's 30-second journey:

1. **Hero** — aha-moment (current A/B/C test, currently pinned to B)
2. **Problem** — *AI sessions end. Engineering knowledge shouldn't.* — body prose, no artifact names
3. **Substrate** — what "memory" actually is (5 types ↔ artifacts), with the per-artifact reframes from the README table
4. **Workflow vignette** — the OAuth story; ideally a visual (3-step timeline or before/after) rather than prose
5. **How it works** — current `Three steps. One file. One commit.` — keep, but **move below** the vignette so mechanism comes after value
6. **Architectures + Postures** — collapsed into one ~2-paragraph sub-section with a click-through to the README
7. **Comparison** — vs Cursor Rules / Copilot instructions / Claude skills / AGENTS.md
8. **Examples / Adoption / Footer** — unchanged

The current flow (Hero → How it works → Features → Architectures → Postures → Adoption) is mechanism-first throughout. The proposed flow is value-first; mechanism enters only after the visitor has reason to care.

### Phasing plan

One commit per phase keeps each diff reviewable.

| Phase | Scope | Length impact | Items closed |
| --- | --- | --- | --- |
| **P1** | Write this file (the capture) + agree the shape | none | — |
| **P2** | Reorder existing sections per the new outline; **no new content** | length-neutral | 12 |
| **P3** | Add Problem + Substrate sections | additive (~250 words) | 4, 5 |
| **P4** | Add Workflow vignette (prose first, visual as P4.5 if budget allows) | additive (~200 words) | 6 |
| **P5** | Reframe `A repo that knows its own rules` + `Process, encoded` in-place | length-neutral or shorter | 7, 8 |
| **P6** | Add Comparison section | additive (~150 words, tabular) | 9, 13 |
| **P7** | Cut/consolidate Postures + Architectures | length-negative (recovers ~400 words) | 10, 11 |
| **P8** | Resolve carryovers (14) + final readability pass (15) | variable | 14, 15 |

**Net length impact P3–P7: roughly neutral.** The page gets clearer without growing meaningfully.

### Risks and open questions

- **Risk: each phase changes the page state the A/B/C test runs against.** As long as B is forced (current state), the test is single-arm and the data collected from P2 onwards reflects "B + restructure." If the force lifts mid-restructure, variant comparisons cross a structural change-point — flag the lift date in ADR-0009 so the analysis is honest.
- **Risk: the vignette (P4) is harder than the prose suggests.** A "real example" that doesn't ring fake takes care; a flat list of (prompt, ADR, TODO) bullets won't land. May need a small visual.
- **Open: item 14.** Without the second reviewer's two unresolved points, P8 is partly speculative. Worth re-reading the PDF or pasting the relevant page.
- **Open: should this file be `.docs/todos/` or somewhere else?** Bends "do-later" semantics. Decided to stay inside conventions rather than invent `.docs/planning/`. Revisit if a second multi-commit initiative needs the same shape.

## Deferred because

This isn't deferred in the usual "we'll get to it" sense — it's the **active workplan** for a multi-commit initiative. Tracking it as one file inside `.docs/todos/` rather than as fourteen separate entries keeps the dependency graph (P2 must come before P3, P5 depends on P2's reorder, etc.) visible at a glance. The cost of the format mis-fit is small; the value is staying inside existing conventions instead of inventing a parallel planning directory.

## Revisit when

Every item above is ✅ — at that point this file's purpose is fulfilled. `git rm` it; ADR-0009's Consequences section already cross-references the underlying decision, so the rationale doesn't need a permanent home here.

If the hero A/B/C test resolves to a clear winner **before** P8 ships (e.g., B converts so dominantly that A and C become irrelevant), revisit P6's comparison-section design — the comparison framing may need to lean on the winning variant's vocabulary.
