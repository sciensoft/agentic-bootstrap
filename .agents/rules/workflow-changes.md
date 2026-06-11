# Workflow: keeping product surfaces in sync

This rule supplements `workflow.md` for the subset of changes that affect the **product** rather than just the codebase. When you change something a user can see, the surfaces that describe that thing move with it — in the same commit, before the work is "done." The user shouldn't have to send a follow-up request to remember the docs.

## When this rule applies

Any change that alters something a user (free, paid, or trial) can experience or read. Typical triggers:

- A new capability — feature, command, public API endpoint, response field
- A change in behaviour the user can perceive (tier behaviour, defaults, included features)
- A new input source (file format, integration, platform)
- A new display surface (panel, page, tab, view)
- A change to the visible app shell (navigation, header, footer, key partials)
- A change to hero copy, brand positioning, or product framing
- A licence or policy change

The decision test, when in doubt: *would a customer reading the public-facing surfaces be misled if I skip the update?* If yes → apply the rule.

## When this rule does NOT apply

Changes a user can't experience:

- Internal refactors with no behavioral change
- Bug fixes that restore intended behaviour — the docs already describe what should happen
- Performance / observability / logging tweaks
- Test additions
- Config & env-var changes that don't shift user-visible defaults
- Workflow / rule file edits, ADR-only additions, prompt files
- Internal tooling (build scripts, CI, dependency bumps that don't surface as a feature)

## Surface map

Fill this table in as you discover surfaces. The starter set:

| Surface | What lives there, when to update |
| --- | --- |
| `README.md` | Project intro, tagline, models in the stack, contributing terms, licence framing. |
| `AGENTS.md` | Architecture map, conventions, response policy, copy guard-rails. |
| `LICENSE` | Actual licence text changes (rare). |
| Public docs / guide page | New capability documentation, examples, tier matrices. |
| Pricing / tiers page | Tier behaviour change, comparison-table cell, new tier feature. |
| App shell partials | Visible navigation, header, footer, key UI fragments. |
| Static assets | New visible CSS / JS that introduces behavior the change relies on. |

When the surface map needs a new row, add it in the same commit that introduces the surface.

## Same-commit rule

The doc updates ride in the **same commit** that lands the product change. Not "in a follow-up", not "after the PR ships." Two reasons:

1. Public surfaces never drift past one commit's lifetime.
2. Reviewers reading the diff can verify the docs match the code, in one place.

When a feature is gated behind a flag or rolled out internally only, hold the doc update until the flag flips for users — *publicly visible* is what triggers the update. Until then, the feature lives only in the relevant ADR and prompt file.

## Completeness expectation

Finishing a product-related change means walking the surface map (and any other user-readable files the change touches) before declaring the work done. The user shouldn't have to remind you that a public surface exists.

If a surface's ownership is unclear — multiple files describe it, or the change cuts across several — sweep all of them rather than guessing which is canonical.

## When you're not sure where the change should surface

Sometimes a change is genuinely new in shape — there's no existing carousel card, no matrix row, no hero line that maps. **Ask before inventing a new section, page, or surface category.** A new section on a public page (or worse, a new page) is an architectural decision that warrants an ADR, not a quiet addition. The right move is to surface the question:

> "This new feature doesn't fit any existing surface — should I propose a new section on `<page>` / a new page / extend the existing X category?"

Then proceed once the user picks. Inventing silently makes the surface map drift away from the team's mental model.

## Why this rule exists

Documentation drift is slow and silent. A feature shipped without its surfaces updated leaves the public guides subtly wrong: a user reading the guide and not seeing the feature assumes it doesn't exist; a user comparing tiers on the pricing page makes the wrong call from stale info; a partner reading the README forms a wrong picture of what the product currently is. Coupling the doc updates to the commit that introduces the change — and treating those updates as a non-optional part of "done" — keeps the public surfaces honest without requiring a separate follow-up step.
