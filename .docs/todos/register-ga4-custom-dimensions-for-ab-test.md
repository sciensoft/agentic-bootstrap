# Register `experiment_id` and `variant` as GA4 custom dimensions

- **Area:** Landing-page telemetry — [[reposition-as-engineering-memory-system-with-ab-test]] follow-up
- **Refs:** [ADR-0009](../adrs/0009-reposition-as-engineering-memory-system-with-ab-test.md), [`docs/index.html`](../../docs/index.html), GA4 property `G-B9N6RPX058`

## Context

ADR-0009 instruments the landing-page hero with an A/B/C test that pushes five events through `gtag.js` — `experiment_view`, `cta_get_bootstrap`, `cta_github`, `scroll_past_hero`, `engaged_30s` — each carrying `{ experiment_id, variant }` as event parameters. GA4 receives these parameters by default and stores them with the events, but the **Explore / Reports UI cannot segment, filter, or compare metrics by them** until each parameter is registered as a **custom event dimension** under *GA4 Admin → Custom definitions → Create custom dimensions*. Without that registration the experiment is collecting data correctly but is effectively unreadable in the dashboard; a per-variant funnel still requires raw BigQuery export or the GA4 Data API.

The registration is a one-time, no-code step in the GA4 web UI — but it has to be done by the property owner with admin access (`alexandre.higtrollers@gmail.com`), so the agent cannot do it. There is also a GA4-side data-quality consideration: dimensions only start aggregating from the moment they are registered, so registering early in the experiment maximises the usable sample. Both dimensions should be scoped to **Event** (not User), since a single visitor sees one variant per browser but each visit fires its own events.

## Deferred because

The registration lives outside the repository — it is a GA4 admin action against the live property, not a code change. The bootstrap repo has no access to GA4 credentials and no IaC for analytics dimensions. The instrumentation in `docs/index.html` is complete and forward-compatible: once the dimensions are registered, *historical* events still won't be segmentable (GA4 limitation), but all *future* events will be — so the cost of deferring is bounded but non-zero.

## Revisit when

Either of the following:

1. The owner finishes the GA4 admin step (register `experiment_id` and `variant` as Event-scoped custom dimensions). At that point this entry is satisfied — remove it and note the registration date in ADR-0009's Consequences section so the data-window-start is auditable.
2. The hero A/B/C test is retired before registration happens. In that case mark this entry obsolete in its closing commit message and `git rm` it; the test loses its segmentable history but the project loses nothing else.
