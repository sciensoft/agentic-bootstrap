# Prompt files

This directory holds the per-request prompt files — one file per user request that produced an artifact, capturing what was asked, why, and what was actually done in response.

The discipline for writing and naming these files lives in `.agents/rules/workflow.md`. The short version:

- **One file per request**, named `<unix-timestamp>.<snake_case_slug>.md`. Flat — no subdirectories.
- **Shape**: `# Request` (what was asked) + `## Reasoning` (why) + `## Output` (what was done).
- **Write before or alongside** the change, not after; the prompt file is the commit's companion note.
- **One prompt → one commit.** Reading the prompts in timestamp order tells the story of how the project evolved.

`ls .docs/prompts/` is the index — files are individually-addressable artifacts and sort chronologically by their timestamp prefix.
