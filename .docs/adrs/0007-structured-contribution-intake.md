# 7. Structured contribution intake — issue templates, PR template, CODEOWNERS, SECURITY.md

- **Status**: Accepted
- **Date**: 2026-06-11

## Context

The repo went public on 2026-06-11 (LinkedIn launch). Up to that point, `.github/` held only the lint workflow — no PR template, no issue templates, no SECURITY.md, no CODEOWNERS. External PRs and issues would have landed without structure, triage path, or clear conventions. With a solo maintainer ([ADR-0001](./0001-develop-trunk-with-ruleset-protection.md)) the time cost of unstructured intake compounds quickly.

Two specific constraints shaped the design:

1. **The maintenance-treadmill risk** (see [ADR-0004](./0004-single-file-agent-executable-delivery-model.md) consequences) means tool-schema churn is the dominant source of future fixes. A vague *"my Cursor adapter is broken"* issue creates a question-asking round trip; a structured field-by-field churn report does not.
2. **The solo-maintainer / 0-approvals workflow** makes triage *signal quality* more important than volume. Filtering noise before it lands on the issue tracker reduces context-switch cost.

## Decision

Adopt the structure below. All paths under `.github/` unless noted.

| File | Role |
| --- | --- |
| `PULL_REQUEST_TEMPLATE.md` | Checklist tying PRs back to the lint script and the `CHANGELOG.md [Unreleased]` bump documented in `CONTRIBUTING.md`. Keeps the PR body short. |
| `ISSUE_TEMPLATE/bug.yml` | Structured bug report: bootstrap version, which agentic tool was running, expected vs actual, repro from a clean directory. |
| `ISSUE_TEMPLATE/tool-churn.yml` | **Novel** template dedicated to "tool X changed its config schema." Fields mirror what a fix PR needs: which tool, version where the change appeared, current vs new schema snippet, source URL. Directly mitigates ADR-0004's maintenance treadmill. |
| `ISSUE_TEMPLATE/feature.yml` | Scope-typed feature requests (architecture / adapter / workflow rule / language / question / doctor check). |
| `ISSUE_TEMPLATE/config.yml` | Disables blank issues; routes "general questions / I bootstrapped my project, here's what happened" to GitHub Discussions. |
| `CODEOWNERS` | `* @AlexzSouz` — auto-tags the maintainer on every PR. Narrows by path when a co-maintainer joins. |
| `../SECURITY.md` (repo root) | Points to GitHub's [private vulnerability reporting](https://github.com/sciensoft/agentic-bootstrap/security/advisories/new) — no email exposed to scrapers. Names the realistic security surface (the bootstrap file itself; the lint script; the scaffolded permission-posture configs; the scaffolded security methodology). |

Discussion categories on the Discussions tab (set up via the GitHub onboarding wizard):

- **Announcements** (maintainer-only)
- **Show & tell** — the most important category; trip reports become social proof feeding the AAIF / awesome-list strategy
- **Q&A** — with marked-best-answer
- **Ideas** — pre-issue brainstorming
- **Tool churn watch** — early signals before a formal `tool-churn` issue

## Consequences

- Triage cost drops: the structured `tool-churn.yml` turns a vague *"Cursor is broken"* report into PR-ready input.
- Issue noise drops: `blank_issues_enabled: false` plus the Discussions redirect channels "how do I…?" away from the issue tracker.
- The `tool-churn` template's existence signals to contributors that *we expect and welcome* churn fixes — making the maintenance-treadmill mitigation visible to anyone who lands on the repo.
- Trade-off: the YAML issue-form format is finicky. A misplaced `: ` (colon + space) in a plain scalar silently breaks the whole template — caught once during initial scaffold (see [`1781155000.fix_bug_yml_yaml_parse.md`](../prompts/1781155000.fix_bug_yml_yaml_parse.md)). Mitigation: validate locally with `python3 -c "import yaml; yaml.safe_load(open('...'))"` before push, per [`.agents/rules/best-practices.md`](../../.agents/rules/best-practices.md) §3.
- The "Discussions tab as social-proof surface" framing depends on people actually using Show & tell. If it sits empty after 60 days, revisit the prompt copy in the welcome post.

Related: [ADR-0001](./0001-develop-trunk-with-ruleset-protection.md) (protection that makes self-merge the bottleneck), [ADR-0004](./0004-single-file-agent-executable-delivery-model.md) (the treadmill the tool-churn template addresses).
