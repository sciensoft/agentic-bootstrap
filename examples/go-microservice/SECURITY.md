# Security Policy

## Reporting a vulnerability

If you've found a security issue in quill, please **do not file a public issue**. Public disclosure before a fix is shipped exposes other users to the same risk.

Instead, contact the maintainers privately:

- **Email**: <security@{{PROJECT_DOMAIN_OR_PLACEHOLDER}}> (replace with the project's real address before publishing)
- Or open a private security advisory on the repository host (e.g. GitHub's "Report a vulnerability" button under the *Security* tab) if available

Please include:

- A description of the issue and its impact.
- Steps to reproduce.
- The affected version (commit SHA or release tag).
- Any proof-of-concept you have — code, request payloads, screenshots.

You'll get an acknowledgement within **5 business days**. We'll keep you posted on the fix timeline; coordinated disclosure happens once a fix is available and users have had a reasonable upgrade window.

## Scope

In scope:

- The code in this repository.
- Default configuration and recommended deployment instructions.
- Dependencies pinned by this project (we'll triage and forward upstream as appropriate).

Out of scope:

- Vulnerabilities in third-party services we don't control (cloud providers, CDNs, …).
- Social-engineering attacks.
- Self-XSS / requires-physical-access scenarios with no plausible attack path.

## Security posture

The project's overall security methodology, rubric, and the dated audit history live under [`.docs/security/`](./.docs/security/). See [`.docs/security/methodology.md`](./.docs/security/methodology.md) for the playbook reviewers follow.

The companion workflow rule at [`.agents/rules/workflow-security.md`](./.agents/rules/workflow-security.md) describes how security-sensitive changes are reviewed during day-to-day development.
