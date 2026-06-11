<!-- best-practices: custom · authored for a markdown-content / single-file scaffold project · accessed: 2026-06-11 -->

# Best Practices — Markdown-content discipline for `agentic-bootstrap`

This project is a **markdown-content scaffold**: the artifact is [`AGENTIC-BOOTSTRAP.md`](../../AGENTIC-BOOTSTRAP.md), the supporting docs are [`README.md`](../../README.md) / [`QUICKSTART.md`](../../QUICKSTART.md) / [`CONTRIBUTING.md`](../../CONTRIBUTING.md) / [`CHANGELOG.md`](../../CHANGELOG.md) / the landing page at [`docs/index.html`](../../docs/index.html), and the only executable code is [`scripts/lint_bootstrap.py`](../../scripts/lint_bootstrap.py) — a Python helper that validates four cross-reference invariants inside the bootstrap file.

Best practices here are about **content discipline** — how to keep the markdown trustworthy, readable, and amenable to both agent and human consumption — not application-development idioms. The bootstrap's shipped `best-practices.md` template options are *refined* (web-driven, for Python / TypeScript / Go / Rust) or *stub* (generic skeleton). Neither fit; this file was hand-written. A future Markdown-content variant for the bootstrap itself is tracked at [`.docs/todos/markdown-content-best-practices-variant.md`](../../.docs/todos/markdown-content-best-practices-variant.md).

## 1. Cross-reference discipline

The bootstrap's value depends on its internal links resolving cleanly. [`scripts/lint_bootstrap.py`](../../scripts/lint_bootstrap.py) enforces four invariants on `AGENTIC-BOOTSTRAP.md`:

1. Q-numbers in Part 2 are sequential `1..N` with no gaps.
2. Every `{{IF_<FLAG>}}` reference in Part 4 templates matches a key in `bootstrap.json`'s `answers` schema (or is a documented derived flag).
3. Every row in the Part 3 decision matrix points to a Part 4 template that exists.
4. The `<!-- bootstrap-version: ... -->` header matches the most recent dated entry in [`CHANGELOG.md`](../../CHANGELOG.md).

Run `python scripts/lint_bootstrap.py` (or `make lint`) before pushing — CI runs the same script and is a required status check on `develop` (see [ADR-0001](../../.docs/adrs/0001-develop-trunk-with-ruleset-protection.md)).

For Markdown links anywhere in the repo:

- Prefer **repo-relative paths** (`./CONTRIBUTING.md`, `../adrs/0004-...`) over absolute URLs that 404 in forks.
- Anchor links use the GitHub-rendered slug — change a heading, you change the slug; grep for any links pointing at it and update in the same commit.
- External links cite the access date for time-sensitive sources (release notes, doc pages that may revise).

## 2. Heading hierarchy

- **H1 (`#`) appears at most once per file**, at the very top. It IS the document title.
- **H2 (`##`) starts every section.** Don't skip from H1 to H3.
- Heading text should be **stable** — GitHub auto-generates anchors from heading text; renaming a heading silently breaks every deep link to it.
- For long files (`AGENTIC-BOOTSTRAP.md`, `workflow.md`), the H2 set IS the table of contents — keep it skimmable.

## 3. Code fences

- **Every fenced block carries a language tag** — `bash`, `json`, `yaml`, `mermaid`, `text` for plain output. Syntax highlighting helps human readers; agents use the tag as a signal too.
- For shell examples that mix input and output, prefix only the lines the reader is expected to type with `$` and a space, or split into separate blocks — input first, expected output second.
- For JSON, validate the snippet before paste: `python3 -m json.tool < snippet.json`.
- For YAML, **watch out for plain scalars containing a colon followed by a space** — that two-character sequence is parsed as a key separator and silently breaks the document. Wrap in single quotes when in doubt. This rule exists because we shipped [`.github/ISSUE_TEMPLATE/bug.yml`](../../.github/ISSUE_TEMPLATE/bug.yml) with exactly that bug and it took a missing-template screenshot to catch it (see [`1781155000.fix_bug_yml_yaml_parse.md`](../../.docs/prompts/1781155000.fix_bug_yml_yaml_parse.md)).

## 4. Mermaid diagrams

- **Caption every kept diagram** with one sentence explaining what the reader should take away. Without a caption the diagram is decoration, not communication.
- **Validate the syntax** — broken Mermaid renders as plain text inside a code block on GitHub, not as an error. Test non-trivial diagrams at the [Mermaid Live Editor](https://mermaid.live).
- Prefer the **structural types** (flowchart, sequence, state, ER, C4Context, quadrantChart) over the **decorative types** (pie, journey, mindmap) — structural diagrams compose well into ADRs; decorative ones rarely add information.
- Keep diagrams under ~30 nodes. Past that, split into two simpler diagrams.

## 5. Prose style

- **Concise > thorough.** A clear sentence beats a clear paragraph.
- **Em-dash for asides.** Avoid Oxford-comma-laden parentheticals when an em-dash carries the same meaning with less noise.
- **No prose-bloat headings.** *"Things to consider when you want to do X"* → just *"X."*
- **Active voice for instructions.** *"Run `make lint`"* not *"The lint command should be run."*
- **Name the constraint, not the wish.** *"GitHub blocks force-push to develop"* beats *"force-pushing to develop is discouraged."*

## 6. Linking discipline

- When fact `F` lives in `N` files, **name one as the source-of-truth** and treat the others as derivatives. Example: the bootstrap-version is canonical in `AGENTIC-BOOTSTRAP.md`'s header; `CHANGELOG.md` derives from it; `README.md` references both.
- When facts collide between source-of-truth and derivatives, the source-of-truth wins. The lint script enforces this for the four invariants above.
- Cite ADRs by number — `[ADR-0004](../../.docs/adrs/0004-single-file-agent-executable-delivery-model.md)` — so the link survives heading renames.

## 7. File location discipline

| Location | Role |
| --- | --- |
| Repo root | Maintainer-authored content: `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `LICENSE`, `SECURITY.md`, `QUICKSTART.md`, `AGENTIC-BOOTSTRAP.md`, `CLAUDE.md`, `AGENTS.md`, `CODE_OF_CONDUCT.md`, `Makefile` |
| `docs/` | Landing-page source: `index.html`, `CNAME`, `favicon.svg`. GitHub Pages publishes from here. |
| `.docs/` | Agent-authored project history: ADRs, prompts, todos, security audits. Hidden from casual browsing but committed. |
| `.agents/rules/` | The discipline files that govern agent behaviour. Canon under the re-run policy — the bootstrap may overwrite them. |
| `examples/` | Fully-bootstrapped sample projects. Don't drift content here; regenerate when conventions change. |
| `scripts/` | Executable helpers (currently just `lint_bootstrap.py`). |

## 8. PR hygiene

- **Bump `CHANGELOG.md`'s `[Unreleased]` section** in the same PR as any `AGENTIC-BOOTSTRAP.md` change. The lint validates the `bootstrap-version` header matches the latest dated entry — a stale changelog will fail.
- **Run the lint locally** before pushing: `python scripts/lint_bootstrap.py` or `make lint`.
- **One PR = one logical change.** Squash-merge is the repo policy; your branch history can be messy, but the merged commit should read as one focused unit.
- **For YAML / JSON files**, validate locally before push: `python3 -c "import yaml; yaml.safe_load(open('<file>'))"` or `python3 -m json.tool <file>`.
- **Direct push to `develop` is blocked** by the ruleset — open a feature branch + PR + self-merge once `lint` is green (see [ADR-0001](../../.docs/adrs/0001-develop-trunk-with-ruleset-protection.md)).

## 9. ADR + prompt + TODO discipline

The full discipline lives in [`workflow.md`](./workflow.md), [`workflow-todos.md`](./workflow-todos.md), and the supporting rules. Short version for this project:

- **Every artifact-producing request** gets a `.docs/prompts/<unix-ts>.<snake_slug>.md` file recording what was asked, why, and what landed.
- **Architectural decisions** (rename a load-bearing file; flip a re-run policy; add a tool adapter; change the deployment model; restructure intake) get an ADR under `.docs/adrs/`.
- **Deferred ideas** get a `.docs/todos/<kebab-slug>.md` file with `Area`, `Refs`, `Context`, `Deferred because`, `Revisit when`.

## 10. What this file is NOT

This is **not a coding style guide.** There is (almost) no application code here. Any future addition to `scripts/` should pull in a language-specific best-practices addition; until then, keep the discussion at the Markdown-content level.

---

## Enabling refinement (future maintainers)

If a future maintainer wants this file replaced by the bootstrap's refined template (synthesized live from web sources), see the **"Enable refinement"** section in the stub variant inside Part 4 of `AGENTIC-BOOTSTRAP.md` — set the agent's host to allow web search, then ask *"re-run the bootstrap's Step 4b best-practices refinement."* For a markdown-content project, refinement targeted at a programming language won't add much value; the long-term path is the **Markdown-content variant** tracked at [`.docs/todos/markdown-content-best-practices-variant.md`](../../.docs/todos/markdown-content-best-practices-variant.md), paired with Q4 inclusivity ([`.docs/todos/expand-q4-language-coverage.md`](../../.docs/todos/expand-q4-language-coverage.md)).
