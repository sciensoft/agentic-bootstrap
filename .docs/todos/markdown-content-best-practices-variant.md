# Add a Markdown / content-only variant of `best-practices.md`

**Area**: bootstrap design / coverage

**Refs**:
- [`AGENTIC-BOOTSTRAP.md`](../../AGENTIC-BOOTSTRAP.md) `best-practices.md` templates in Part 4
- [`.docs/todos/expand-q4-language-coverage.md`](./expand-q4-language-coverage.md) — pairs with this
- [`.agents/rules/best-practices.md`](../../.agents/rules/best-practices.md) — this repo's own hand-written Markdown-content best-practices, suitable as the seed for the variant template

## Context

The current `best-practices.md` template ships in two variants — **refined** (synthesized from web sources for a single language stack: Python / TypeScript-Node / Go / Rust) or **stub** (generic skeleton awaiting refinement). Neither fits Markdown / content-only projects (documentation sites, docs-as-code workflows, single-file scaffolds, knowledge bases, design-doc repos, the bootstrap itself).

A Markdown variant would cover:

- **Cross-reference discipline** — every link uses repo-relative paths; broken links fail CI; the `: ` YAML trap that breaks GitHub issue forms
- **Code-fence language tagging** — every fenced block carries a language tag; agents use it as a parsing signal too
- **Heading hierarchy + anchor stability** — H1 once at top; renamed headings silently break all deep links to them
- **Mermaid diagrams** — captioned, valid, structural over decorative, capped at ~30 nodes
- **Lint tooling**: `markdownlint` for structural rules, `lychee` or `markdown-link-check` for link integrity, `cspell` for terminology, `Vale` for prose style
- **External link curation** — name the access date for citations; prefer first-party docs over blog posts
- **Cross-file consistency** — name the source-of-truth and treat the rest as derivatives

This repo already has a working draft at [`.agents/rules/best-practices.md`](../../.agents/rules/best-practices.md) — refactor that into the variant template (strip the project-specific paragraphs; keep the universal rules).

## Deferred because

The Q4 question phrasing makes Markdown an awkward fit today — it's currently captured under *"Other / mixed."* The Markdown variant only really pays off once Q4 explicitly offers Markdown as an option (see [`expand-q4-language-coverage.md`](./expand-q4-language-coverage.md)).

## Revisit when

Pair with the Q4 expansion. When that PR lands, harvest this repo's `best-practices.md` as the variant template and mark `BEST_PRACTICES_REFINED=true` in `bootstrap.json` for projects choosing the Markdown variant.
