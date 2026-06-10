# Workflow: testing discipline

This rule is a companion to [`workflow.md`](./workflow.md). It defines **when** tests are required, **what** they should cover, **where** in the layering they should live, and **what** the agent must include in the commit that introduces or changes code.

The discipline is opinionated but not religious. The headline rule is short: **every artifact-producing change ships with the tests that prove the behaviour, in the same commit as the behaviour**. The rest of the file says what "the tests that prove the behaviour" actually means.

## When this rule applies

- Any new feature, public function, route, command, message handler, scheduled task, or worker.
- Any bug fix.
- Any refactor that changes observable behaviour at a layer boundary.
- Any change to a rule-encoded invariant (auth check, permission scope, cardinality limit, retry policy).

## When this rule does NOT apply

- Pure typo / wording fixes in docs, comments, or non-behavioural strings.
- Rename-only refactors with no behavioural change (function rename, file move, import reorder).
- Configuration edits with no logic change (linter config, editor config, gitignore, CI tweaks unrelated to test execution).
- Bootstrap / scaffolding commits that introduce empty placeholder modules with no real behaviour yet.

When unsure: write the test. The cost of an extra test is low; the cost of an untested regression is real.

## The pyramid (default shape, not a quota)

| Layer | Volume | What it covers | What it mocks |
| --- | --- | --- | --- |
| **Unit** | The bulk | Pure functions, single classes, domain logic, individual service methods, helpers. | Nothing internal. Mock only at the *boundary* of the unit (a clock, an HTTP client, a clock-like time source). |
| **Integration** | A meaningful minority | Real wiring across a meaningful boundary — a route handler calling a service calling a real (or test-double) repository against a real DB; a queue consumer end-to-end against a real broker; a CLI command exercised through its actual entrypoint. | External third-party APIs (HTTP, queues, model endpoints) via canned responses. The database, in-process side-effects, and your own modules are real. |
| **End-to-end** | A thin top | The happy-path of a user-facing flow: login → checkout, sign-up → first action, a CLI invocation that touches every layer. | The fewest mocks possible — usually none, or only third-party APIs the test environment can't reach. |

The pyramid is the default shape; particular projects (data pipelines, ML training code, infrastructure modules) have their own ratios. The rule is: bias towards the cheapest layer that meaningfully exercises the behaviour. **A unit test that mocks the database is exercising the mock, not the behaviour.** When you find yourself piling on mocks, move the test up the pyramid.

## Bug fixes: regression test first

For any bug fix:

1. **Write the failing test first.** Reproduce the bug at the lowest layer that surfaces it.
2. Confirm the test fails for the right reason (not a typo, not a missing import).
3. Apply the fix.
4. Confirm the test now passes and no other tests broke.
5. Commit the test and the fix together in the same commit.

A bug fix without a regression test is half a fix — the same bug will return the moment someone refactors that area. The test is the bug's tombstone.

## Mocking discipline: mock at boundaries, not internals

- **Mock at the system boundary.** External HTTP APIs, third-party SDKs, the model endpoint, the wall clock, randomness, the filesystem when it's incidental. These are non-deterministic, slow, or out of your control.
- **Don't mock your own code.** Mocking a service to test the route that calls it tests the mock, not the wiring. Use the real service against a test database, an in-memory adapter, or a fake that implements the protocol fully.
- **Don't mock to make a test easier.** If a unit needs five mocks to be testable, the unit is doing too much. Split it before you write the test.
- **Prefer fakes to mocks.** A fake repository that holds state in a dict is more readable, more reusable, and catches more real bugs than a mock that records calls.
- **Avoid snapshot tests for behavioural code.** Snapshots are useful for UI rendering and CLI output where the shape is the contract; they're a trap for business logic where they ossify the *current* output without asserting the *intended* one.

## Naming, structure, and signal

- Name tests by **behaviour, not implementation**: `returns_403_when_viewer_is_not_owner`, not `test_check_owner`. The name should read as a sentence describing the contract.
- One assertion *concept* per test. A test can make multiple `assert` calls if they prove the same concept; if they prove two unrelated things, split them.
- Arrange / act / assert sections are visually separated (blank line, comment, or whitespace).
- Tests are independent and order-independent. No shared mutable state between tests. If two tests share setup, lift it to a fixture, not to a class attribute.
- Test files live alongside the code they cover unless the language ecosystem dictates otherwise — `tests/` directory for Python/Rust (per `pytest` / `cargo test` conventions), `*.test.ts` co-located for TypeScript, `*_test.go` co-located for Go.

## TDD: encouraged, not mandated

Test-Driven Development — *red, green, refactor* — is the recommended default for non-trivial behaviour. It forces the contract to be designed before the implementation, catches over-engineering early, and produces tests that genuinely cover the behaviour because they were written before the code that satisfies them existed.

That said, TDD is a *practice*, not a rule. Some changes (small bug fixes, mechanical refactors, exploratory spikes) don't benefit from it; some teams aren't on board with it; some moments don't allow the discipline. **The hard rule is: every change ships with its tests in the same commit.** Whether you wrote the test first or second is your call — but the commit must contain both.

When TDD genuinely helps: new public API design, new use-case orchestration, anything where you're not sure what the contract should look like yet, anything where the implementation is non-trivial and you want to confirm the contract before locking yourself in.

When TDD genuinely doesn't: trivial helpers, configuration plumbing, generated code, exploratory spikes you'll throw away.

## Coverage: track, don't gate

- Run coverage tooling locally and in CI. **Report it; don't gate on a percentage.** Hard percentage gates incentivise the wrong behaviour — gaming the metric with assertion-free tests, or skipping a useful test because it doesn't move the number.
- The right question is "does this commit's diff have tests for its behaviour?" — answered by reading the diff, not by reading a percentage. A change that adds 200 lines of behaviour and 0 tests fails the review regardless of project-level coverage.
- Coverage **drops** in a PR are a useful signal. If overall coverage went down because new code lacks tests, that's a question worth asking in review. If it went down because dead code was deleted, that's progress.
- For long-lived projects, watching the *trend* of coverage matters more than the absolute number. Sustained downward trend means the discipline is slipping; sustained upward trend means the project is hardening.

## Flaky tests

A flaky test is a broken test — it just hasn't decided which failure mode it prefers yet. Treat them as P1:

- **First flake**: investigate the same day. Time / order / race / network non-determinism. Fix the underlying cause.
- **Can't fix immediately**: quarantine (skip with a clear `Flaky: <reason>` annotation) and file a `.docs/todos/<ts>.<slug>.md` entry per `workflow-todos.md` so the quarantine is visible and dated.
- **Never** disable a flaky test silently. A skipped flake with no entry is technical debt that compounds.

## Test data and fixtures

- **Builders / factories over fixtures of fixed data.** A `make_user(role="admin")` helper that takes overrides is more readable and more maintainable than dozens of fixture files.
- **No real PII or secrets in test data.** Use obviously fake values (`user@example.com`, `password-for-test`). Never copy production data into a test file.
- **Time and randomness pinned.** Inject a clock and a seeded RNG so tests are deterministic. If a test depends on the real clock or `random`, it will fail on Tuesdays at 3am six months from now.

## What goes in the commit

Per `workflow.md`, every artifact-producing request bundles its prompt, ADR (if applicable), telemetry, security pass, and code into one commit. With this rule installed, the same commit also bundles:

- **The new / updated tests** that cover the change.
- **Any test infrastructure** needed by those tests (a new fixture, a new factory, a new fake adapter).
- **Any test-data updates** for cases the change touches.

If the agent commits code without tests when this rule applies, the commit is incomplete — push back and fix it before moving on.

## Cross-references

- **Security findings** (per `workflow-security.md`): every finding's fix must include a regression test that proves the vulnerability is closed and won't return. That test is part of the same commit as the fix.
- **Bug fixes** triggered by a `.docs/todos/` entry: the regression test lives in the commit that closes the entry.
- **Metering changes** (per `workflow-metrics.md`, if installed): tests cover the catalog entry, the emit site, and the read side — at integration level where they actually exercise the wiring.
- **Product-surface changes** (per `workflow-changes.md`, if installed): the test layer that matches the surface — UI components → component tests, public API → contract tests, docs → link / build checks.

## Why this rule exists

Tests are a memory aid for the project's intended behaviour. Without them, every refactor is a roll of the dice and every bug fix is a hope. With them, the contract is enforced by code that runs on every commit; future agents and humans can change the implementation without breaking the behaviour, because the tests catch them when they do.

The cost of writing the test now is small. The cost of *not* writing it — the production incident, the customer impact, the cold-debug at midnight — is large and lumpy. This rule trades a known small cost for an unknown but eventually large one.
