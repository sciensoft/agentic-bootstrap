# Open a case-study PR or issue against the AGENTS.md repo

**Area**: distribution / AAIF visibility

**Refs**:
- [`.docs/adrs/0004-single-file-agent-executable-delivery-model.md`](../adrs/0004-single-file-agent-executable-delivery-model.md)
- [AGENTS.md GitHub repo (OpenAI-donated, AAIF-stewarded)](https://github.com/openai/agents.md)
- [Linux Foundation announcement of AAIF](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation)
- [aaif.io](https://aaif.io/) — community channels and proposal process

## Context

The Agentic AI Foundation (AAIF) is a Linux Foundation project anchored by AGENTS.md (donated by OpenAI), MCP (Anthropic), and goose (Block). Platinum members include AWS, Anthropic, Block, Bloomberg, Cloudflare, Google, Microsoft, OpenAI. **Contributions go via the AGENTS.md GitHub repo — no paid membership required.** Two angles worth pursuing:

- **Case study**: *"Real-world AGENTS.md consumer: agentic-bootstrap.md uses AGENTS.md as the spine with thin per-tool adapters for 8 assistants. Here's how the pattern works."* If accepted, agentic-bootstrap becomes a canonical reference example.
- **Spec gap**: as an 8-adapter implementer, document one concrete gap (e.g. *how AGENTS.md should signal posture/autonomy intent across tools that each model permissions differently*) as a discussion or proposal.

Either gets the project onto the maintainers' Rolodex.

## Deferred because

Awesome-list submissions come first (warmer distribution, faster signal). The AAIF case-study play takes longer to land but unlocks much wider reach — best run after the public framing has been validated by at least one awesome-list acceptance.

## Revisit when

After at least two of the four awesome-list submissions land — then within the same week, propose the case study first. Fall back to the spec gap if the maintainers prefer a structural contribution.
