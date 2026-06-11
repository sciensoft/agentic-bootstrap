# Workflow — Do-Later Ideas

This rule governs how the project tracks ideas explicitly deferred — features the agent (or the user) suggested but didn't ship in the moment, follow-ups noted in commit messages or ADR consequence sections, scope cuts surfaced during implementation. Managed per the rules in `workflow.md`: the agent adds entries proactively when an idea is deferred, sweeps entries during implementation that the change satisfies, and removes (rather than archives) on completion. Cross-link the ADR or prompt where the idea originated so the *why* is reconstructible.

## Where entries live

Entries live as **one file per idea** under `.docs/todos/`, not inline in this rule. A directory listing is the index; each file is a self-contained, individually-addressable artifact. The companion `.docs/todos/README.md` explains what lives in the directory; this rule explains *how to manage entries there*.

The split is deliberate: this rule is stable (the discipline doesn't churn); the entries churn constantly (added, edited, removed every few commits). Keeping the rule small and the entries individually-addressable makes both halves easier to read, link, and `git mv` without dragging surrounding noise.

## Filename pattern

Each entry is a single markdown file named:

```
.docs/todos/<kebab-case-slug>.md
```

- **`<kebab-case-slug>`**: short, descriptive, scoped enough to avoid colliding with neighbours. Read at a glance from `ls`.
- Files sit **flat** in `.docs/todos/`. The topical grouping lives inside each file's **Area** field — `ls` is the index, no subdirectories.
- Slug derives from the entry's title. If the slug ever collides with an existing file, disambiguate by prefixing with the area (e.g. `auth-`, `ingest-`) — don't suffix with a number.

## File content structure

Every file follows the same shape — title, two header lines, three prose sections. The shape is the contract; if a draft idea doesn't fit it, the idea is probably not yet a TODO (it's a brainstorm, a feature request, an ADR candidate — surface it directly).

```markdown
# <One-line title>

- **Area:** <Topic / feature area — e.g. "Auth (ADR-0007)", "Ingest pipeline">
- **Refs:** <Comma-separated cross-links: ADR(s), prompt file(s), code paths, commit SHAs>

## Context

A paragraph (3–5+ sentences) capturing the back-story — what feature /
area we were discussing, what problem or opportunity surfaced, what
alternatives we considered, why this particular idea is worth saving.
Write enough that a future contributor (or future-you) understands the
*why* without needing to dig up the original conversation.

## Deferred because

2–4 sentences on the trade-off, blocker, scope cut, or constraint that
pushed this to later. Be specific — cite the actual constraint, not just
"out of scope".

## Revisit when

Concrete trigger — a metric crossed, a model released, an ADR landed,
a feature shipped, a usage threshold hit. Short is fine here; the test
should be unambiguous.
```

The 3–5+-sentence minimum on **Context** is load-bearing. *AI agents satisfice on minimums* — "1-2 sentences" gets read as "two words" and produces uselessly-thin entries that nobody else has the back-conversation to interpret. Don't compress it; if an entry feels long, the entry probably *should* be long.

**Cross-references** in `Refs` and `Context` use repo-relative paths from `.docs/todos/`:

- ADRs: `../adrs/<NNNN>-<slug>.md`
- Prompts: `../../.docs/prompts/<ts>.<slug>.md`
- Code: `../../<layer>/<path>.<ext>`
- Sibling docs: `../<dir>/<file>.md`

## When to add an entry (proactively, without being asked)

- The user defers an idea explicitly: *"for now"*, *"later"*, *"hold this"*, *"save it for later"*, *"add to TODOs"*, *"we'll revisit"*.
- You suggest something the user accepts but explicitly scopes out of the current change ("yes, but not this commit").
- An ADR's *Consequences* names a deferred follow-up that wouldn't otherwise be tracked anywhere actionable.
- Implementation reveals an out-of-scope sub-task worth remembering — a refactor opportunity, a known limitation that needs revisiting once a constraint changes, a "we should also do X" that the user agrees to defer.

When you spot one of these, surface the draft entry inline in your response — *"I'll capture this in `.docs/todos/<slug>.md` as: …"* — so the user sees what lands without having to open the file. Create it in the same commit as the related work unless the deferral is the only thing the turn produced (then it's its own commit per the prompt-file + commit + push rule in `workflow.md`).

## Consistency sweep on every commit

Before staging files for a commit, scan `.docs/todos/` for entries this change satisfies. If an entry's *Revisit when* trigger has fired — either because this commit closes it, or because the underlying state has changed since the entry was written — **remove the file** (`git rm`) in the same commit. There is no archive directory; git log is canonical history.

When the same commit also touches an ADR a file references, check that file's framing against current reality: a blocker that has since been resolved should be reframed or removed even if the underlying idea is still deferred for other reasons.

## Removing entries safely

Three layers of safeguard, in order:

1. **Scope test.** Only consider removing files whose `Refs:` cross-link to ADRs, prompts, or topics the current commit *actually touches*. If the commit changes one module but the candidate-for-removal lives in an unrelated area with no shared refs, leave it. This catches the "the agent thought it was done but it's something else entirely" failure mode.

2. **Cite the closing change.** To remove an entry, you must point at the specific commit / file / lines that satisfy the entry's *Revisit when* trigger. If you can't articulate that link in one sentence, the file stays. **When in doubt, leave it** — cost of an extra stale file is small; cost of dropping in-progress work is high.

3. **Announce inline before pushing.** Same pattern as the inline-draft-then-add for new entries: your response always names what was removed and why, with the citation. *"Removing **<entry title>** (`.docs/todos/<slug>.md`): <commit/ADR/feature> satisfies the *Revisit when* trigger because <one sentence>. Refs cross-checked."* The user sees it before push and can override same-turn.

These combine into: automation stays (no per-removal approval gate), paper trail exists (the announcement + cite is reviewable), failure mode is conservative (when scope or citation isn't clean, the entry stays).

## Updating entries

When reality drifts under an entry — a blocker resolves but other reasons keep the idea deferred, a trigger sharpens, a ref needs adding — edit the file in place. The file's `git log` is the audit trail; no need for "Updated YYYY-MM-DD" notes inside the body unless the change is large enough that a future reader would benefit from the timeline.

## Why this rule exists

The do-later list is a working memory across contributors and across time. If entries are scattered (in commit messages only, in chat history only, in ADR consequences only), the team forgets ideas and ships duplicates of work that was already considered and rejected. Pinning entries to individual files under `.docs/todos/` — and pinning the discipline of *when to add / sweep / remove* to this rule — keeps the list honest without requiring a separate review step.

The shape is the contract: every entry shows its back-story, its blocker, its trigger, and its refs, so the next contributor (often future-you, often a different agent session) can read a single file and decide whether the idea has aged into action.
