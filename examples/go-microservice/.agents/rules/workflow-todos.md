# Workflow — Do-Later Ideas

This rule governs how the project tracks ideas explicitly deferred — features the agent (or the user) suggested but didn't ship in the moment, follow-ups noted in commit messages or ADR consequence sections, scope cuts surfaced during implementation. Managed per the rules in `workflow.md`: the agent adds entries proactively when an idea is deferred, sweeps entries during implementation that the change satisfies, and removes (rather than archives) on completion. Cross-link the ADR or prompt where the idea originated so the *why* is reconstructible.

## Where entries live

Entries live as **one file per idea** under `.docs/todos/`, not inline in this rule. A directory listing is the index; each file is a self-contained, individually-addressable artifact. The companion `.docs/todos/README.md` explains what lives in the directory; this rule explains *how to manage entries there*.

The split is deliberate: this rule is stable (the discipline doesn't churn); the entries churn constantly (added, edited, removed every few commits). Keeping the rule small and the entries individually-addressable makes both halves easier to read, link, and `git mv` without dragging surrounding noise.

## Filename pattern

Each entry is a single markdown file named:
