# Agentic Bootstrap — Claude Code adapter

The brief is [`AGENTS.md`](./AGENTS.md), and it is agent-agnostic: purpose, run instructions, architecture map, the always-on rules, the trigger index for `.agents/rules/`, and the hard constraints. It is imported below.

@AGENTS.md

Nothing else belongs in this file. It exists because Claude Code reads `CLAUDE.md`, not because Claude needs different instructions. Anything true for every agent goes in `AGENTS.md`; put something here only when it is genuinely specific to this host, such as a tool or a permission it alone has.
