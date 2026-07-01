# 9. Reposition as engineering-memory system; validate via gtag-based A/B/C hero test

- **Status**: Superseded by [ADR-0010](./0010-reposition-as-engineering-operating-model.md)
- **Date**: 2026-06-30

> **Superseded.** [ADR-0010](./0010-reposition-as-engineering-operating-model.md) re-frames the positioning around the *category shift* (agentic AI made engineering knowledge abundant; the bootstrap makes it durable) rather than the *memory-system consequence* this ADR settled on. The A/B/C experiment **infrastructure** introduced here — `data-hero-variant-block` markup, `localStorage` stickiness, `FORCE_VARIANT`, `gtag`-based events, bot pinning — survives intact under ADR-0010; only the variant set in `<body>` and the strategic copy changed. The body below is preserved verbatim for history.

---

## Context

Two independent reviewers (one external, one in a separate LLM session) converged on the same diagnosis: the project's surfaces lead with **mechanism** — *"one markdown file, any agentic coding assistant, one prompt"* — rather than the **problem** it solves. A first-time visitor reads "another bootstrapper" and bounces before reaching the substance. Both reviewers reached the same reframe by independent paths: the artifacts the bootstrap installs (`AGENTS.md`, `.agents/rules/`, `.docs/adrs/`, `.docs/prompts/`, `.docs/todos/`, `.docs/security/methodology.md`) collectively form an **engineering memory substrate** — episodic memory (prompts), semantic memory (ADRs), working memory (TODOs), procedural memory (rules + best practices), evaluative memory (security rubric). Agents become *consumers* of that substrate; the repo itself is the memory.

Two strategic risks complicate a single bet on the new framing:

1. **"Engineering memory" is unproven copy at scale.** It might land — or it might read as too abstract for a developer audience that wants to see the diff. Picking one positioning blind throws away the chance to learn from real visitor behaviour.
2. **The provocation/recognition/reframe variants test different psychological gestures**, not just different words. A provocation ("We've been versioning the wrong thing") risks reading as overclaim if the rest of the page doesn't earn it; a recognition ("AI sessions end. Engineering knowledge shouldn't.") is the safest "true statement"; a reframe ("Your repo remembers the engineering") is descriptive but produces no gestalt shift. We genuinely don't know which one converts.

Solution: pivot the **static** surfaces (README, meta tags, OG description) toward the engineering-memory thesis using a hybrid of the two strongest variants, and **A/B/C-test** the landing page hero across all three psychological gestures so the data picks the winner.

## Decision

**Positioning.** Adopt **engineering-memory system** / **persistent operating model for AI-assisted software engineering** as the project's primary noun phrases on every public surface. Lead every surface with the problem (AI sessions evaporate engineering context), name the substrate, then describe the mechanism. Reframe the README's `What lands in your repo` table from artifact-first to outcome-first.

**A/B/C hero test on the landing page** (`docs/index.html`). Three variants:

- **Variant A — Provocation-led.** Eyebrow: *"We've been versioning the wrong thing."* H1: *"Your repo can remember the engineering, not just the code."*
- **Variant B — Recognition-led** (favored). Eyebrow: *"An engineering memory system for AI-coded repos."* H1: *"AI sessions end. Engineering knowledge shouldn't."*
- **Variant C — Reframe-led.** Eyebrow: *"A persistent operating model for AI-assisted software engineering."* H1: *"Your repo remembers the engineering."*

The eyebrow, H1, and lede paragraph vary by variant; the CTAs, project-feature checkmarks, and Works-with strip stay shared.

**Mechanism.** A synchronous inline script in `<head>` picks a variant before `<body>` renders, sets `data-hero-variant="A|B|C"` on `<html>`, and writes it to `localStorage` for visitor stickiness. CSS attribute selectors hide non-matching variant blocks, so there is no flash of wrong content. Weights are **50% B / 25% A / 25% C** — B-favored because it is the most honest variant (every word is a true statement about the world), so bouncing on B carries the smallest copy-credibility cost. Known bot user agents are pinned to B and excluded from the `experiment_view` event to keep the funnel clean.

**Telemetry.** Variant is reported to GA4 via `gtag('event', ...)` calls — there is no Google Tag Manager container; we push events through the existing `gtag.js` snippet:

- `experiment_view` — fired on initial load with `experiment_id` and `variant`.
- `cta_get_bootstrap` — primary CTA click ("Get AGENTIC-BOOTSTRAP.md").
- `cta_github` — secondary CTA click ("View on GitHub").
- `scroll_past_hero` — fired once when the post-hero section reaches ≥50% in view (IntersectionObserver).
- `engaged_30s` — fired if the tab is still focused after 30 seconds.

Every event carries `{ experiment_id: "hero_2026_q3", variant: "A|B|C" }` for downstream attribution.

**Snapshot.** The previous landing page is preserved verbatim as `docs/index.v1.html` so the diff and rollback path stay obvious. It is not linked from any served page.

```mermaid
sequenceDiagram
  participant V as Visitor (browser)
  participant LS as localStorage
  participant H as &lt;head&gt; inline script
  participant CSS as CSS attribute selectors
  participant GA as gtag.js → GA4
  V->>H: HTML parse, &lt;head&gt; executes
  H->>LS: read ab_hero_variant_v1
  alt no stored variant (first visit)
    H->>H: weighted random (50% B, 25% A, 25% C)
    H->>LS: write ab_hero_variant_v1
  end
  alt known bot UA
    H->>H: pin to B, skip experiment_view
  end
  H->>V: html[data-hero-variant="X"]
  CSS->>V: hide non-matching variant blocks
  H->>GA: experiment_view { experiment_id, variant }
  Note over V: Visitor reads the hero
  V->>GA: cta_get_bootstrap / cta_github on click
  V->>GA: scroll_past_hero (≥50% next section in view)
  V->>GA: engaged_30s (30s dwell, tab visible)
```

## Consequences

- **GA4 admin step required.** `experiment_id` and `variant` must be registered as custom event parameters (and optionally custom dimensions) in GA4 Admin → Custom definitions before the dashboard can segment by variant. Without this step the events fire but the UI can't filter by them. Tracked as a follow-up TODO.
- **Test power vs traffic.** Three arms converge slower than two. At the current traffic level (single-digit-thousands of uniques per month) a confident winner could take months. Acceptable because the experiment also functions as instrumented telemetry while it runs; if velocity matters more than nuance later, drop A or C to convert to a two-arm test.
- **Pattern reusable.** The `data-hero-variant-block` attribute + CSS hide rules + `gtag('event', ...)` instrumentation generalise. Future content tests (e.g., on the Quick start section or the Works-with strip) can extend the same scaffolding with a new experiment ID and new `data-*-variant` attribute family. Each new experiment should ship in its own ADR (or as an addendum here) to keep the positioning rationale auditable.
- **Visitor stickiness via localStorage.** Returning visitors see the same variant they were assigned. Clearing site data or switching browsers re-rolls. Private-window visits silently fail the write and re-roll each session — acceptable because private-window traffic is rare and the cost is double-counting, not corruption.
- **Bot pinning to B.** Crawlers — including OG-card previewers (Slack, Twitter, LinkedIn, Discord) — see variant B's copy, which is what the meta description and OG tags also encode. Static SEO and social shares therefore align with the "true statement" variant regardless of the test outcome.
- **Snapshot rollback path.** Reverting to the pre-repositioning page is `mv docs/index.v1.html docs/index.html`. The snapshot will rot as Tailwind/CDN drift; treat it as a one-quarter rollback option, not an indefinite mirror.
- **Future ADRs frame the project as a memory system.** The shift is load-bearing — subsequent decisions (e.g., new artifact categories, new agent-tool adapters) should reason from "does this strengthen the substrate the repo carries across sessions?" rather than "does this add a feature?"
- **Currently pinned to B via `FORCE_VARIANT`.** The variant-selection script in `<head>` carries a `FORCE_VARIANT = 'B'` constant that overrides the random engine and bypasses the `localStorage` read **and** write paths. Reasons: ship the most-trusted variant as the canonical hero while baseline conversion data is being gathered for B in isolation; align direct, organic, and social traffic on identical copy during the initial post-repositioning window so signal can be compared to the pre-positioning history without a multi-arm split confounding it. The force is non-destructive — the random engine, the bot-pinning branch, and the localStorage stickiness branch all remain intact; previously-assigned visitors keep their stored variant when the override is lifted (because the force path doesn't touch storage), and new visitors get a fresh weighted roll. *Revisit when:* B has enough sessions to read a baseline conversion rate (target ~500+ `experiment_view` events with `cta_*` events attributed), or sooner if visitor traffic clearly invalidates the experiment design. Lift by setting `FORCE_VARIANT = null;` — random engine resumes the same turn.

Cross-references: ADR-0004 (single-file delivery model — the substrate this ADR repositions); ADR-0005 (custom domain — the surface this ADR now reshapes).
