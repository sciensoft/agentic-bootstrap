# Security Policy

## Reporting a vulnerability

If you find a security issue in the bootstrap or any file it scaffolds for downstream projects, **please don't open a public issue**. Use GitHub's [private vulnerability reporting](https://github.com/sciensoft/agentic-bootstrap/security/advisories/new) instead.

Include:

- A short description of the issue.
- The bootstrap version affected (the `<!-- bootstrap-version: YYYY-MM-DD -->` header at the top of [`AGENTIC-BOOTSTRAP.md`](./AGENTIC-BOOTSTRAP.md)).
- A proof of concept, if you have one.

Expect acknowledgement within 72 hours. Fixes ship as a dated entry in [`CHANGELOG.md`](./CHANGELOG.md) and a credited security advisory.

## Scope

This repo is a single-file scaffold that hands its output to a coding agent. The realistic security surface is:

- **[`AGENTIC-BOOTSTRAP.md`](./AGENTIC-BOOTSTRAP.md) itself** — a malicious change would affect every downstream project that runs it.
- **[`scripts/lint_bootstrap.py`](./scripts/lint_bootstrap.py)** — runs in CI on every PR.
- **The scaffolded permission-posture configs** — `.claude/settings.json`, `.codex/config.toml`, `.cursor/settings.json`, `.windsurf/settings.json`, `.continue/config.json`, `.aider.conf.yml` autonomy keys. A bad template could grant more autonomy than the user intended.
- **The scaffolded security methodology** at `.docs/security/methodology.md` — outdated or wrong rubric guidance is itself a security issue.

Out of scope: vulnerabilities in the agentic tools themselves (Claude Code, Cursor, Aider, Codex CLI, OpenCode, Continue.dev, Windsurf, GitHub Copilot) — please report those to their respective maintainers.
