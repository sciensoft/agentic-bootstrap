# Security Review — Methodology

This is the playbook for security reviews of this project. It defines the frameworks used, the order in which the codebase is walked, the severity rubric applied to findings, and the "best practice" checklist behind each check. It is intentionally evergreen: it should change only when the *approach* changes, not when a finding lands or gets fixed.

Each individual audit lives in its own dated sibling file (`.docs/security/<YYYY-MM-DD>-<slug>.md`). Audit files cite this document for definitions and rubric so the findings can stay tight. The companion rule `.agents/rules/workflow-security.md` says *when* to consult this doc — both per-request (rubric pass on security-sensitive commits) and on cadence (full audits).

---

## 1. Audience and reason

This document has two audiences:

- **A future reviewer (human or agent)** running the next audit — to repeat the same approach without reinventing the rubric or the scope.
- **Any contributor adding a feature** — to run their change against the same checklist before opening the PR. The rubric in §5 is meant to be a usable pre-commit aid, not just a post-hoc taxonomy.

Findings, recommendations, and "what's currently shipped" all belong in the dated audit files, not here. This document doesn't change when the codebase ships a fix.

---

## 2. Frameworks

### 2.1 OWASP Top 10 (2021)

The [OWASP Top 10](https://owasp.org/Top10/) is a community-consensus list of the ten categories that produce the majority of web-application breaches. Each category represents a *class* of bug, not a single vulnerability — e.g. "Broken Access Control" covers IDOR, missing authorisation, privilege escalation, JWT-confusion, path traversal, and forced browsing under one heading. The 2021 revision is the current published list at time of writing; categories from earlier revisions (XSS, deserialisation, etc.) were rolled into broader buckets.

Even for projects that aren't classical web apps (CLIs, libraries, data pipelines), several OWASP categories apply directly: A02 (Cryptographic Failures), A06 (Vulnerable & Outdated Components), A08 (Software & Data Integrity Failures), A09 (Security Logging & Monitoring Failures). Treat the list as a starter taxonomy and let the rubric in §5 select what's load-bearing for your project.

| Category | What it covers |
| --- | --- |
| A01 Broken Access Control | IDOR, missing authorisation, path traversal, privilege escalation, forced browsing. |
| A02 Cryptographic Failures | TLS, cookie flags, secret storage, weak hashing, insecure RNG. |
| A03 Injection | SQL, NoSQL, OS command, LDAP, template, expression-language injection. |
| A04 Insecure Design | Missing rate limits, missing quotas, missing trust boundaries, threat-model gaps. |
| A05 Security Misconfiguration | Missing security headers, default creds, verbose errors, unnecessary features enabled. |
| A06 Vulnerable & Outdated Components | Known-CVE deps, unpinned versions, end-of-life libraries. |
| A07 Identification & Authentication Failures | Weak login, session fixation, credential stuffing, missing MFA. |
| A08 Software & Data Integrity Failures | Unverified updates, missing SRI on CDN scripts, signed-artifact gaps. |
| A09 Security Logging & Monitoring Failures | Missing audit logs, secrets in logs, no alerting. |
| A10 Server-Side Request Forgery (SSRF) | Server fetches a URL the attacker controls. |


---

## 3. Review approach

The audit is a **static, read-only** review:

- All evidence comes from reading source files, configuration, dependency manifests, and ADRs.
- No live HTTP requests, no fuzzing, no exploitation, no port scan.
- No code modifications, no patches.

This bounds the audit's reach (we may miss runtime-only issues — race conditions, TLS misconfiguration on the deployed instance, etc.) but keeps the cost low and the result reproducible: anyone can re-read the same files and reach the same conclusion.

The order in which the codebase is walked is deliberate. **Auth and access control come first** because every other finding's severity depends on the trust boundary they establish — an "injection in a service" is severe if any user can reach the service, mild if only an admin can. After auth, walk inputs (uploads, query strings, form bodies), then persistence (SQL hygiene, owner-scoping enforcement), then output (templating, output encoding), then transport (headers, cookies, CORS), then dependency hygiene, then logging.{{IF_LLM}} **The LLM surface is reviewed last** because its threats only make sense once the rest of the trust model is mapped.

---

## 4. Severity scale

The five-level scale is explicit so that prioritisation isn't subjective:

| Level | Meaning |
| --- | --- |
| **Critical** | Exploitable now, leads to compromise / data loss / takeover. |
| **High** | Exploitable with a small precondition (specific user state, specific tier). |
| **Medium** | Defence-in-depth gap; combined with another bug, becomes exploitable. |
| **Low** | Hardening recommendation; no plausible exploit path today. |
| **Info** | Positive observation, context, or N/A. Included to make absences explicit. |

Every category produces *something* — at minimum an `[Info]` note saying "no findings — appears mitigated". Silence is ambiguous; an explicit `[Info]` lets the next audit see whether a check was performed and skipped vs. forgotten.

---

## 5. What "best practice" looks like — the rubric

This is the rubric the audit is *looking for*. A contributor adding a feature can run their change against the matching sub-section before opening a PR. Sub-section numbers are stable (aligned to OWASP categories); if a section doesn't apply to your project, leave the gap rather than renumbering.


### 5.3 Input validation

- Inputs are validated at the boundary (the route handler, CLI parser, or service public method), not deep inside.
- Validation rejects rather than coerces — explicit allow-lists over deny-lists.
- File uploads have a byte-size cap enforced *before* the body is read into memory.
- File uploads have a content-type / magic-byte check, not just an extension check.
- URLs from users are parsed and host-allow-listed before any outbound request.
- Free-form strings have a length cap that protects downstream tokenisers / parsers from quadratic blow-up.


### 5.7 Secrets and configuration

- Secrets come from environment variables, never from committed files.
- `.env.example` is committed; `.env` is gitignored.
- Default secrets in `.env.example` are clearly labelled "rotate before deploy".
- Secrets are not logged — not at INFO, not at DEBUG, not in exception traces.
- Boot-time configuration prints non-sensitive summaries (`backend=postgres pool_size=10`), not the connection string.

### 5.8 Logging and monitoring

- Structured logging via a per-module logger.
- Event names are static lowercase dotted paths (`subsystem.action.outcome`); variable data goes in the structured payload.
- Levels match the signal: DEBUG for diagnostics, INFO for routine ops, WARNING for recoverable anomalies, ERROR for "operator should investigate", CRITICAL for unrecoverable / wake-someone events.
- Sensitive fields (passwords, tokens, OAuth codes, full request bodies, full message content, IPs, full email addresses) never appear in structured payloads. When *presence* matters, log a boolean (`token_present`).
- For SDK exceptions whose messages may echo caller-supplied secrets (e.g. botocore on bad keys), log the canonical short error code, not `str(exc)`.

### 5.9 Rate limiting and resource caps

- Per-actor rate limits on expensive endpoints / commands, keyed on the authenticated identity.
- Per-IP rate limits on unauthenticated endpoints (login, signup, public APIs).
- A bounded concurrency cap per actor on long-running operations (e.g. one in-flight inference per user).
- Decode caps (audio duration, image pixel count, document size) enforced *before* the heavyweight library does the work.

### 5.10 Dependency hygiene

- Lockfile (`uv.lock`, `poetry.lock`, `package-lock.json`, `go.sum`, etc.) is committed.
- High-risk deps have lower-bound pins in the manifest (so an automated upgrade doesn't silently regress).
- A CVE scanner (`pip-audit`, `safety`, `npm audit`, GitHub Dependabot) runs in CI and fails the build on critical advisories.
- High-velocity deps are watched; "watch" means the team gets a signal when they ship a security release.


---

## 6. Glossary

Short definitions for the acronyms and jargon used in audits that follow this playbook.


| Term | Definition |
| --- | --- |
| **RNG** | Random Number Generator. "Cryptographically secure RNG" = `secrets` / `os.urandom`, not `random.random()`. |
| **Constant-time compare** | A comparison that takes the same time regardless of where the inputs differ, to defeat timing oracles (`secrets.compare_digest` in Python). |
| **Rate limit** | A cap on how many requests a single client (user / IP / session) may make per unit time. Defends against brute force and resource exhaustion. |
| **Defence in depth** | The principle that no single mitigation should be load-bearing. Output encoding doesn't replace input validation; rate limits don't replace auth — each is a layer. |


---

## 7. How to run a security review

1. Walk the categories in the order defined in §3.
2. For each category, grep / read the matching files and capture findings as `(severity, file:line, what, risk, recommendation)`.
3. Assign severity per the rubric in §4.
4. Capture an `[Info]` note for every category with no findings, so absences are explicit.
5. Save the audit as a sibling file under `.docs/security/<YYYY-MM-DD>-<slug>.md`. Each audit is a snapshot in time; previous audits stay where they were so the diff between them is the story.
6. The audit file itself should carry: scope + date, executive summary, per-category findings, prioritised recommendation list (highest risk reduction per hour, first), and an explicit "out of scope" section. It should *not* re-state the framework descriptions, the severity rubric, the rubric of best practices, or the glossary — those live here.
7. If a finding becomes load-bearing for the project's shape (e.g. introduces a new mitigation pattern future code is expected to follow), promote the consequence to an ADR under `.docs/adrs/`.

A re-run of the audit after the prioritised recommendations from the previous audit ship should produce a noticeably shorter `[High]` list — that's the signal the previous audit caught real risk, not just style. The re-run produces a new sibling file; the previous audit is left alone.
