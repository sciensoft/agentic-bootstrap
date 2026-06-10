# Example — TypeScript + Vertical Slice

A trimmed sample of what the bootstrap produces for `LANG=TypeScript/Node` + `ARCH=VERTICAL_SLICE`.

## Interview answers (relevant subset)

- `Q1 PROJECT_NAME` = `helix`
- `Q1 ONE_LINE_PURPOSE` = `Issue and verify ephemeral access tokens for a mesh of internal services.`
- `Q2 AGENTS_USED` = `[CURSOR, AIDER]`
- `Q4 LANG` = `TypeScript/Node`
- `Q5 ARCH` = `VERTICAL_SLICE`
- `Q12 TESTING` = `true`

## What's shown here

| File | What it demonstrates |
| --- | --- |
| `AGENTS.md` | Primary brief. Cursor reads it via `.cursor/rules/agents.mdc`; Aider reads it via `.aider.conf.yml`'s `read:`. |
| `src/features/issue-token/handler.ts` | Inbound entry — HTTP route. Validates input, calls service, formats response. |
| `src/features/issue-token/service.ts` | The feature's business logic. Imports only its own slice's types + `shared/`. |
| `src/features/issue-token/model.ts` | Feature-internal types — request, response, errors. |
| `src/features/issue-token/issue-token.test.ts` | All tests for the slice, co-located. |
| `src/shared/auth/signing-key.ts` | Cross-feature primitive every slice needs. The only legitimate cross-slice import target. |

## The one rule

**Features may only import from `shared/`. Features may NEVER import from each other.** This is the discipline that makes Vertical Slice *Vertical Slice*. The bootstrap installs `import-linter` (Python) / `eslint-plugin-boundaries` (TypeScript) / equivalent for your stack so the rule is enforced mechanically, not just by review.

## What's NOT shown here

A real bootstrap run also produces: `.agents/rules/{workflow,workflow-todos,workflow-security,workflow-testing,best-practices,layered-architecture}.md`, `.docs/{adrs,prompts,todos,security}/`, `.cursor/rules/agents.mdc`, `.aider.conf.yml`, `package.json`, `tsconfig.json`, `eslint.config.js`, `.prettierrc.json`, `vitest.config.ts`, `Makefile`, `.gitignore`, `.env.example`, plus conventional repo files.

Browse the full template set in [`AGENTIC_BOOTSTRAP.md` Part 4](../../AGENTIC_BOOTSTRAP.md).
