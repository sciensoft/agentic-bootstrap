# Extend the Claude `.claude/settings.json` allow-list with Python commands

**Area**: developer experience / posture configuration

**Refs**:
- [`.claude/settings.json`](../../.claude/settings.json)
- [`AGENTIC-BOOTSTRAP.md`](../../AGENTIC-BOOTSTRAP.md) — Part 4 `.claude/settings.json TRUSTED_DEV` template, "Language-specific addenda" table
- [`scripts/lint_bootstrap.py`](../../scripts/lint_bootstrap.py)

## Context

`.claude/settings.json` was written with the TRUSTED_DEV base template — but Q4 `LANG` was answered as *Other / mixed* (this is a markdown-content project), so the bootstrap intentionally skipped the language-specific allow addendum. In practice the only executable code in the repo is the Python lint script (`scripts/lint_bootstrap.py`), which now prompts on every invocation under the current allow-list.

Append the Python addendum to `permissions.allow`:

```json
"Bash(python:*)",
"Bash(python3:*)",
"Bash(uv:*)",
"Bash(pytest:*)",
"Bash(ruff:*)"
```

The full Python addendum is documented in Part 4's `.claude/settings.json TRUSTED_DEV` "Language-specific addenda" table.

## Deferred because

The bootstrap's first-time write honored the `LANG=Other` answer literally; flipping the addendum at scaffold time would not have matched the schema. The right move is a deliberate post-bootstrap edit captured here so it doesn't get lost.

## Revisit when

Next session that runs the lint script and gets prompted. Five-minute fix; commit as its own small PR.
