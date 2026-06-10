# Workflow: keeping the metrics surface honest

This rule supplements `workflow.md` for changes that touch the metering system — anywhere a metering counter is updated, a usage event is written, or a metrics-driven display reads from. The discipline exists because metrics drift silently: an event that no longer fires, a counter renamed but never updated downstream, a label growing in cardinality, a display that hasn't been told a new metric exists.

## Top-level rule

> **Adding, modifying, or removing a metered event means moving the four surfaces in lockstep — write site, durable read side, observability labels, display — plus updating a catalog at `.docs/metrics/README.md` AND a per-metric deep-dive at `.docs/metrics/<kebab-kind>.md`. All in the same commit. The cardinality discipline (no PII, no high-cardinality identifiers in labels) is non-negotiable and applies on every emit, not just new ones.**

## The four surfaces

Every metered event sits at the intersection of four surfaces. A change that touches any of them must consider the other three:

1. **Constant** — the canonical `kind` name (a string constant defined in one place in code so consumers import it instead of typing it).
2. **Call site** — where the meter is emitted. Always through a centralised meter helper (never a raw counter call) so the dual-write to ledger + observability is preserved.
3. **Catalog row + deep-dive** — `.docs/metrics/README.md` is the index; `.docs/metrics/<kebab-kind>.md` is the per-metric record of decisions (what counts as one event, what the bounded labels are *for*, what the metric does NOT measure, where it surfaces, caveats).
4. **Display** — wherever the metric is read (analytics endpoint, user-facing usage page, dashboard chart). Removing a metric without removing the display crashes the page; adding a metric without wiring the display means it's invisible.

## Cardinality discipline

Bounded labels only. Strip user identifiers from observability labels (the durable ledger row can keep `user_id` because it stores rows, not aggregates).

**Forbidden as bounded labels** (always — no exceptions):

- `user_id`, `chat_id`, `message_id`, any per-record UUID.
- `email`, `name`, `display_name`, `picture_url`, `phone`, IP addresses.
- User-supplied text content, filenames, prompts.
- Free-form upstream-system text (provider error strings, raw URLs, exception messages).
- Trace IDs, span IDs, request IDs, session tokens.

**Allowed as bounded labels** (small enumerable sets):

- Tier names, tool names, model names, source kinds, instrument modes, provider names.
- Booleans (`ok`, `cancelled`, `is_signup`).
- Discrete enum values you can list on a single line.

When in doubt, ask: *does this value have a bounded enumerable set?* If yes, allow. If it grows with users / time / events, forbid.

## Don't speculate

Three guardrails:

1. **Concrete signal first.** Add a metric when there's a question someone wants to answer. Empty dashboards are clutter.
2. **One axis at a time.** A single concept usually has one ledger axis. Don't double-emit two counters when one is unused.
3. **Per-user attribution earns its keep.** If a counter doesn't need per-user attribution, your observability auto-instrumentation already handles it. Reserve the dual-write path for things that will eventually feed quotas or per-user displays.

## Why this rule exists

The metering system has four surfaces that move independently — write side, durable read side, observability, display. Each is touched by different commits, often weeks apart. Without a rule that ties them together, drift is inevitable: a counter renamed at the write site keeps showing the old name on dashboards because the chart still reads the old `kind`; a new metric lands but the catalog doesn't, so the next contributor adds a duplicate counter for the same concept under a slightly different name; a label key sneaks in carrying user IDs because nobody re-read the cardinality rule.

Coupling the surfaces to one commit, locking the catalog as the canonical source, and treating the rule as load-bearing (not optional) keeps the metering surface honest.
