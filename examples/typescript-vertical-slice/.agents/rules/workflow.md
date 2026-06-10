# Workflow

This rule defines the naming, contents, and ordering of the per-request artifacts so `git log`, `ls .docs/prompts/`, and `ls .docs/adrs/` together reconstruct the project's history — and the *why* behind it — from the repository alone.

Every user request that changes files in this repository produces, all bundled into a single commit and pushed:

- A **prompt file** under `.docs/prompts/` capturing what was asked and why.
- **The code, config, or docs** the request produced.
- When the change is architecturally significant — a new module, library, layer, or pattern, or a meaningful change to one — a **new or updated ADR** under `.docs/adrs/`.
- **Telemetry** kept current — new behaviour gets new logs, changed behaviour gets existing logs updated, deleted behaviour gets its logs removed, at log levels that match each event's signal (DEBUG / INFO / WARNING / ERROR / CRITICAL), with sensitive-data redaction discipline (credentials, PII, request bodies — anything that shouldn't ride a wire to a third-party log service).
- A **single git commit** bundling all of the above on the current branch.
- A **push** of that commit to the remote.

## When this rule applies

Apply it whenever the response generates or modifies a file in the repository. Typical triggers:

- Writing, editing, or deleting source code
- Adding or updating documentation, rules, configs, or scripts
- Creating data files, fixtures, or seed content
- Renaming or moving tracked files

## When this rule does NOT apply

Skip the prompt file and the commit for interactions that produce no artifact. Examples:

- Plain conversation, clarifying questions, or brainstorming with no file changes
- Read-only investigation ("what does this function do?", "show me where X is defined")
- Advice or recommendations the user has not yet asked you to implement
- Explicit user instruction to look without changing ("just explore, don't commit")

If a conversation starts as chitchat but later produces an artifact, the rule kicks in at that point — write the prompt file for the portion that generated work, not for the preceding discussion.

## 1. Create a prompt file

For each user request, write a file to `.docs/prompts/` using the pattern:
