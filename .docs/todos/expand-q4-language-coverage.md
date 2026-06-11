# Expand Q4 language coverage beyond Python / TypeScript / Go / Rust

**Area**: bootstrap design / inclusivity

**Refs**:
- [`AGENTIC-BOOTSTRAP.md`](../../AGENTIC-BOOTSTRAP.md) Q4 (line 280) and the multi-variant dispatch for `.gitignore` / manifest / linter / `Makefile` / `TRUSTED_DEV` allow addendum
- [`.docs/todos/markdown-content-best-practices-variant.md`](./markdown-content-best-practices-variant.md) — the paired follow-up for the Markdown variant

## Context

Q4 currently asks: *"Python / TypeScript / Go / Rust / something else / mixed?"* — those four languages have first-class scaffolds (gitignore variant, manifest stub, linter config, Makefile family, TRUSTED_DEV `Bash(...)` allow addendum); everything else falls through to a generic *Fallback* variant. The phrasing makes Python / TS / Go / Rust feel like *the* answers and other languages feel like second-class citizens.

Other languages with real agentic-coding adoption that deserve first-class treatment:

| Language | What a first-class scaffold needs |
| --- | --- |
| **C# / .NET** | `dotnet:*` allow entries, MSBuild targets, `.editorconfig` already supports most of it, `dotnet test`, large enterprise audience |
| **Java** | `mvn:*` / `gradle:*`, JaCoCo / SpotBugs / Checkstyle, JUnit |
| **Ruby** | `bundle:*`, `rake:*`, RuboCop, RSpec, Brakeman |
| **PHP** | `composer:*`, PHPUnit, PHP-CS-Fixer, PHPStan |
| **Kotlin** | Overlaps with Java but has its own idioms and the Gradle Kotlin DSL |
| **Swift** | `swift build / test`, SwiftFormat, SwiftLint |
| **Markdown / content-only** | markdownlint, lychee, Vale, cspell — see paired TODO `markdown-content-best-practices-variant.md` |

Adding a language is a **multi-template addition**: gitignore lines, manifest stub (or "no manifest" note), linter config, Makefile targets, TRUSTED_DEV allow addendum entries. Each adds ~50–150 lines to `AGENTIC-BOOTSTRAP.md` Part 4 — meaningful surface to maintain.

The smaller, decoupled fix is **reframing the Q4 question itself** so it doesn't lead with four named languages: ask *"What's the project's primary language or content type?"* with an open answer, then dispatch to the matching variant if one exists (Fallback otherwise). That refresh is a single-PR change to Q4's text + a note in Part 4 that explicitly invites variants.

## Deferred because

Each new first-class variant is a real chunk of work; best contributed by someone who lives in that language daily. The Q4 reframing is smaller and can ship independently — but doesn't itself add coverage, just removes the Python-centric framing.

## Revisit when

- A contribution from a C# / Java / Ruby / Kotlin / Swift / Markdown user lands — that PR brings the templates.
- OR the maintainer can sit down for a focused PR on one of them (probably C# / .NET first — largest underserved audience).
- OR the next issue or Discussion that explicitly asks why a specific language was skipped — use that as the signal to act.
