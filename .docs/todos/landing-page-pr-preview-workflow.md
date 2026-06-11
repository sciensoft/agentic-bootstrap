# GitHub Actions PR-preview workflow for the landing page

**Area**: CI / developer experience

**Refs**:
- [`.docs/adrs/0005-custom-domain-agentic-bootstrap-md.md`](../adrs/0005-custom-domain-agentic-bootstrap-md.md)
- [`docs/index.html`](../../docs/index.html)

## Context

The landing page lives in `docs/index.html` and deploys to `agentic-bootstrap.md` via GitHub Pages on push to `develop`. There's no PR-level preview today, which means:

1. Contributors can't preview their changes before merge.
2. The GitHub ruleset's **Require deployments to succeed** knob remains unusable — it would deadlock against the current "Pages auto-deploys after merge" model (see [ADR-0005 consequences](../adrs/0005-custom-domain-agentic-bootstrap-md.md)).
3. Broken HTML / dead links can land silently.

Build a GitHub Actions workflow that:

- Triggers on PRs touching `docs/**`.
- Validates HTML (linter, broken-link check).
- Deploys to a temporary preview environment — Cloudflare Pages preview, Netlify drop, or a stash branch GitHub Pages serves separately.
- Posts the preview URL as a PR comment.

Once it exists, **Require deployments to succeed** can be enabled for `docs/**`-touching PRs.

## Deferred because

Solo maintainer hasn't needed it yet; landing-page changes are still maintainer-driven. The need will show up the first time a contributor proposes a landing-page PR.

## Revisit when

A contributor's PR touches `docs/**`, OR maintainer-side changes to the landing page become frequent enough that local preview friction is felt.
