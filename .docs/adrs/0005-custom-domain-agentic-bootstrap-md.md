# 5. Custom domain `agentic-bootstrap.md` for the landing page

- **Status**: Accepted
- **Date**: 2026-06-11

## Context

The project's GitHub Pages landing page lived at `sciensoft.github.io/agentic-bootstrap` until the LinkedIn launch push. The `.md` TLD (Moldova's ccTLD) reads naturally as "Markdown" — a brand opportunity unique to this project because the artifact IS a Markdown file the user hands to their agent. The URL becomes the punchline: *"I'm presenting AGENTIC-BOOTSTRAP.md"* at `https://agentic-bootstrap.md` — title and product are the same string.

## Decision

Register `agentic-bootstrap.md` via register.domains; point the apex at GitHub Pages via four A records (`185.199.108–111.153`) and four AAAA records (`2606:50c0:8000–8003::153`); CNAME `www` → `sciensoft.github.io`; enforce HTTPS via Let's Encrypt (provisioned automatically by GitHub Pages after DNS verification). Commit a [`docs/CNAME`](../../docs/CNAME) file containing `agentic-bootstrap.md` so GitHub knows which host to serve.

## Consequences

- Brand reinforcement: every share leads with the punchline. LinkedIn launch post (2026-06-11) used the domain itself as the title.
- Annual registrar fee — small, scoped cost.
- TLS auto-renews via Let's Encrypt; nothing to monitor under normal operation.
- Vendor concentration: register.domains is the single registrar dependency. Mitigated by the fact that DNS resolution itself runs through GitHub Pages once the records resolve; the registrar's role is limited to record management.
- The GitHub ruleset's **Require deployments to succeed** knob cannot currently be enabled — GitHub Pages auto-deploys *after* the merge, creating a chicken-and-egg deadlock. A PR-preview workflow would unlock it; deferred ([TODO](../todos/landing-page-pr-preview-workflow.md)).
- The `.md` TLD prices and policies are set by Moldova's registrar (ICANN-delegated). If the TLD's terms change adversely, the domain can be moved to a more conventional `.dev` or `.io` host without losing the discoverability already accumulated via redirects.

Related: [ADR-0004](./0004-single-file-agent-executable-delivery-model.md) (the brand is downstream of the delivery model — *the markdown file IS the product*).
