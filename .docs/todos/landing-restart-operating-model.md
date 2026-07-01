# Landing-page restart — engineering operating model positioning

- **Area:** Landing-page positioning ([`docs/index.html`](../../docs/index.html)) and downstream README pivot
- **Refs:** [ADR-0010](../adrs/0010-reposition-as-engineering-operating-model.md), [ADR-0009 (superseded)](../adrs/0009-reposition-as-engineering-memory-system-with-ab-test.md), [`docs/index.html`](../../docs/index.html), [`docs/index.v1.html`](../../docs/index.v1.html) (rollback snapshot from ADR-0009 era), [`README.md`](../../README.md), [`.docs/prompts/1782851069.full_restart_operating_model_positioning.md`](../prompts/1782851069.full_restart_operating_model_positioning.md)

## Context

[ADR-0010](../adrs/0010-reposition-as-engineering-operating-model.md) restarts the landing-page positioning around the brief's category-creation thesis: *agentic AI has made engineering knowledge abundant; AGENTIC_BOOTSTRAP makes it durable.* The hero in R1 (this commit) collapses to a single curiosity-led variant, and the rest of the page — currently leading with mechanism (3-step quickstart, file-tree visual, *Process encoded* features grid, Architectures, Postures, etc.) — is restructured over the following commits. The substrate's substance doesn't change; only the story changes.

This file replaces [`landing-positioning-restructure.md`](./landing-positioning-restructure.md) (now `git rm`-d in the same commit). That earlier 8-phase backlog framed the Substrate section as *"5 memory types ↔ artifacts"* — clever but still mechanism dressed in metaphor. The new plan reorders to lead with the **category shift** first, then introduces the substrate as evidence in service of the philosophy, and explicitly carries a *Why now* beat (IaC / GitOps / containerization parallel) that the old plan didn't.

The form bends the usual "one-file-per-deferred-idea" TODO convention because this initiative IS one idea with many sequenced sub-items; splitting would lose the inter-phase dependencies. Same self-acknowledgment as the file it replaces.

### Phase plan

Legend: ✅ done · ⬜ open · 🟡 partial.

| Phase | Status | Commit scope | Length impact | Sections touched |
| --- | --- | --- | --- | --- |
| **R1** | ✅ | Hero rewrite (single curiosity-led variant) + ADR-0010 + supersede ADR-0009 + TODO swap | length-negative (drops right-column codeblock) | §1 Hero |
| **R2** | ✅ | Prose-hierarchy Aha section between hero and 60-second demo. Anchor is a two-sentence H2 slogan (*"The best engineering now happens in conversation. It shouldn't disappear with it."*) — user-flagged as load-bearing category-defining copy comparable in shape to *Infrastructure as Code* / *Build once. Run anywhere.*, protected verbatim through future iterations per [[feedback-tagline-preservation]]. Body follows the *conversation produces engineering knowledge → AGENTIC_BOOTSTRAP makes it lasting → opinionated but flexible → grows with your engineering* arc, with a styled blockquote breaking the middle. The earlier chip-row shape (Architectural decisions · Trade-offs · Future ideas · Conventions + *Things worth keeping / Most of it disappears / AGENTIC_BOOTSTRAP keeps it*) is retired — the substance survives as prose inside the second paragraph. Section: `py-20` with `max-w-2xl` centered container, left-aligned prose. | additive (~110 words, prose-hierarchy shape) | §2 (merged §3) |
| **R3** | ⬜ | Add *Why now* — IaC / GitOps / containerization parallel; align OG/meta tags with the new framing once R2 body settles | additive (~150 words) + meta sweep | §4, meta |
| **R4** | ⬜ | Add *What "durable engineering knowledge" actually looks like* — categories of knowledge, no file names yet | additive (~180 words) | §5 |
| **R5** | ⬜ | Reframe *What you get* into *The substrate* (existing file-tree reused with new framing) + add *vignette* (a single human–AI session, before-and-after) | additive (~250 words) + reuse | §6, §7 |
| **R6** | ⬜ | Reframe *Three steps* (mechanism after value); reframe *Runtime footprint* to lead with **durability without per-session tax**; cut/consolidate *Architectures*; cut/consolidate *Postures*; re-add *Works-with* strip as standalone band; move checkmarks into Adoption | length-negative (recovers ~500 words) | §8, §9, §11, §12 |
| **R7** | ⬜ | Add *What this is vs what it isn't* (comparison vs Cursor Rules / Copilot / Claude skills / bare AGENTS.md); pivot README to mirror the new framing | additive (~200 words) + README rewrite | §10, README |
| **R8** | ⬜ | Final readability + scroll-depth + contrast pass; verify A/B engine still fires `experiment_view` cleanly with `variant: "A"`; confirm any new CTAs carry `data-ab-event` | minimal | polish |

### New section order (anchors for R2–R7)

1. **Hero** — curiosity-led, single variant *(R1 ✅)*
2. **Why this matters?** — Aha beat: chip-row with the four knowledge types + three-line resolution ending on *AGENTIC_BOOTSTRAP keeps it*. Compressed delivery of what was planned as separate §2 *What just changed* + §3 *The new bottleneck* prose. *(R2 ✅)*
3. **Why now** — IaC / GitOps / containerization parallel *(R3)*
4. **What "durable engineering knowledge" actually looks like** — categories of knowledge, no file names *(R4)*
5. **The substrate** — first introduction of the artifact list, framed as evidence *(R5)*
6. **A single human–AI session, before and after** — vignette *(R5)*
7. **How it works** — existing 3-step, reframed (mechanism after value) *(R6)*
8. **Runtime footprint** — kept, reframed to lead with *durability without per-session tax* *(R6)*
9. **What this is — vs what it isn't** — comparison vs Cursor Rules / Copilot instructions / Claude skills / bare AGENTS.md *(R7)*
10. **Tool-agnostic** — 8-tool list (moved out of hero into its own band) *(R6)*
11. **Architectures · postures** — collapsed to one paragraph + README link *(R6)*
12. **Adoption · footer** — unchanged

### Open items

- **R3's *Why now* needs a short, punchy parallel framing.** The brief sketches the IaC / GitOps / containerization analogy but doesn't supply prose; this needs careful drafting to avoid sounding like "another category created by the AI hype cycle."
- **R5's vignette is the hardest write.** A "real example" risks reading fake unless it names specifics. Carryover from the old plan; still open.
- **R6's Runtime-footprint reframe must keep the three numeric anchors** (~25k smart-agent scaffold · ~80k naive-fallback · ~10k every session). The reframe is a copy edit on the eyebrow, H2, and closing line, not a restructure of the cards.
- **R7's README pivot may warrant its own ADR.** If the structural changes go beyond a copy refresh — e.g., reordering top-level sections — the new structure is itself an architectural decision worth capturing.
- **A/B/C engine is dormant under R1.** Returning visitors with `localStorage`-stored B or C see A via `FORCE_VARIANT = 'A'`. Stored values are not overwritten (the force path doesn't touch `localStorage.setItem`), so a future multi-arm test launched against new variants re-rolls cleanly. No data corruption.

## Deferred because

Not "deferred" in the conventional sense — this is the active workplan for a 7-commit (R2–R8) positioning restart following R1. Tracking as one file inside `.docs/todos/` keeps the inter-phase dependencies (R2's prose sets up R5's substrate framing; R5's vignette needs the *Why now* established in R3; etc.) visible at a glance. Cost of the form mis-fit is small; value is staying inside existing conventions instead of inventing a parallel planning directory.

## Revisit when

Every R-phase row in the plan above is marked ✅ — at that point this file's purpose is fulfilled. `git rm` it; ADR-0010's Consequences section already cross-references the underlying decision, so the rationale doesn't need a permanent home here.

If a strategic pivot supersedes ADR-0010 mid-restart (analogous to how this ADR supersedes ADR-0009), rewrite or replace this file in the same commit as the new ADR.
