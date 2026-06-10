# Do-Later Ideas

This directory holds the project's deferred ideas — features the agent (or the user) suggested but didn't ship in the moment, follow-ups noted in commit messages or ADR consequence sections, scope cuts surfaced during implementation.

The discipline for managing this directory is documented in `.agents/rules/workflow-todos.md`. The short version:

- **One file per idea**, named `<kebab-case-slug>.md`. Flat — no subdirectories.
- **Shape**: title + Area + Refs + Context (3–5+ sentences) + Deferred because + Revisit when.
- **Add proactively** when the user defers something.
- **Sweep on every commit** for entries the change satisfies; `git rm` to remove (no archive — git log is canonical).

`ls .docs/todos/` is the index — files are individually-addressable artifacts.
