<!-- best-practices: stub · refinement deferred · reason: agent host had no web access at bootstrap time -->
# Best Practices

> **This file is the generic baseline.** It contains language-agnostic patterns that apply across most projects. For *much* more value, refine it from current web sources for your specific your stack + framework stack — see [§ Enable refinement](#enable-refinement) at the bottom of this file.

Patterns and conventions established in this project. Apply them when adding new features or refactoring. Expand this file with language- or framework-specific idioms as the project matures — the sections below are the language-agnostic core.

## Architecture

### Layered architecture

Follow [`.agents/rules/layered-architecture.md`](./layered-architecture.md) for the project's layer names and dependency direction. Whatever the chosen shape (4-Layer DDD, 3-Tier, SPA, …), dependencies flow in one direction only; reverse imports break the layering. The architecture rule names the layers, the responsibilities of each, and the import arrows; this best-practices file just enforces *that you follow the rule*.


### Repository pattern

Every external data source is hidden behind a repository class.

- Repositories expose intent-revealing methods (`load_projects`, `load_commits`), not raw paths or URLs.
- Separation of concerns inside the class: private helpers handle discovery/parsing; public methods compose them.
- Always sort results deterministically (by date ascending unless otherwise specified).

### Service pattern

Business logic lives in services (classes, or module-level functions for genuinely stateless services).

- Services receive collaborators via `__init__` (never instantiate them internally).
- Services own data-loading orchestration — presentation handlers must not call repositories directly for computed data.
- Expose small focused methods and a high-level aggregator for UI consumption.
- Keep pure helpers as private members.

### Dependency Injection & Inversion

- **Constructor injection**: dependencies are passed to `__init__`, never instantiated inside methods.
- **Central wiring**: a single composition root (often `application/container.py` or equivalent) composes the graph. It exposes factory functions returning singletons.
- **Testability**: the container exposes a `reset()` (or equivalent) that clears cached instances so tests can swap fakes without touching production code paths.
- **Fail fast**: constructors validate required deps (e.g. `raise ValueError("XService requires a YRepository")`).

## Code style

- **Imports**: absolute across layers; relative imports only within the same package.
- **Async**: use the runtime's async primitives (`async`/`await` in Python or JS/TS, goroutines in Go, …) and run independent I/O concurrently where it helps. Don't mix sync and async carelessly inside a single call path.
- **Privacy**: prefer language-idiomatic privacy markers (`_underscore` for module-private in Python; `private` in TS; lowercase for unexported in Go). Reserve aggressive privacy mechanisms (double-underscore name mangling, sealed classes, etc.) for actual collision avoidance — don't reach for them as "more private".
- **Dates**: timezone-aware end-to-end. Never rely on system locale or naive datetimes for boundary work.
- **Avoid mutation**: prefer non-mutating operations where the language has them (`sorted(xs)` over `xs.sort()` in Python, spread/`map` over in-place updates in JS, immutable structs where the language supports them).
- **Type hints**: required for public function signatures and class attributes wherever the language supports them.
- **Validation**: validate at boundaries (UI input, external APIs, file parsing). Trust internal data shapes once they cross the boundary.
- **Errors**: raise specific exceptions in infrastructure; the application layer catches and converts to user-facing strings.

## File & Naming Conventions

- Module files: lowercase with the language's idiomatic separator (`snake_case.py`, `kebab-case.ts`, `lowercase.go`). One class per file for service/repository classes; small related helpers may co-locate.
- Services: `<feature>_service.<ext>` exporting a `<Feature>Service` class.
- Repositories: `<entity>_repository.<ext>` exporting a `<Entity>Repository` class.
- Domain protocols / interfaces live under a `domain/interfaces/` (or `domain/protocols/`, or your language's equivalent) directory.
- Infrastructure adapters: `<provider>_client.<ext>` (e.g. `s3_client.ts`, `youtube_client.py`).
- Constants: `UPPER_SNAKE_CASE` at module level.
- Private members: `_single_underscore` (Python) or the equivalent for your language.
- Package directories use lowercase, no separators.

## Data & Formatting

- Always sort returned collections — dates ascending by default, stats descending by value.
- Format numbers and dates via a locale-aware library (Babel for Python, Intl for JS, `golang.org/x/text` for Go) where the audience matters.
- Section copy should be **generic** and explain what the stats represent — never hard-code narrative from a specific dataset.

## What NOT to do

- Don't instantiate repositories in presentation handlers or services — get them from the container.
- Don't compute logic inside route handlers — delegate to application services.
- Don't add comments that restate the code; only document non-obvious *why*.
- Don't reach for a custom decorator/metaclass when a plain function or class fits.
- Don't mix layers — see [`.agents/rules/layered-architecture.md`](./layered-architecture.md) for the project's dependency direction. Reverse imports break the layering.
- Don't track build artifacts or virtual envs in git — gitignore them.
- Don't bundle multiple unrelated changes in one commit; one prompt + one commit per request (see `.agents/rules/workflow.md`).

## Enable refinement

The bootstrap tried to refine this file from current your stack + framework sources but couldn't reach the web from your agent host. Once you fix that, ask any agent to *"re-run the bootstrap's Step 4b best-practices refinement"* and a stack-specific version will replace this stub. **How to enable web access per host:**

| Agent host | What to enable |
| --- | --- |
| **Claude Code** | The `WebSearch` and `WebFetch` tools ship with the CLI. If calls prompt for permission, add `"WebSearch"` and `"WebFetch(domain:*)"` (or specific allowed domains) to the `permissions.allow` array in `.claude/settings.json`. For headless / cron runs, also pre-allow the domains you expect to fetch. |
| **Cursor** | Web search is built in (the `@web` symbol). If the agent doesn't pick it up automatically, prompt it explicitly: *"Use @web to research your stack best practices, then refine .agents/rules/best-practices.md."* |
| **OpenAI Codex CLI** | The `--web` flag / web-tool capability must be enabled in your Codex config. See `codex --help` for the current flag name; web access is opt-in per session. |
| **Aider** | Aider doesn't ship native web search. Either pipe sources in via `aider --read <url-or-path>` after fetching them yourself (`curl`), or use the `/web` slash command if your Aider build supports it (newer versions). |
| **OpenCode** | Web search is available via the platform's tool config. Enable it in your OpenCode settings before re-running the refinement prompt. |
| **Continue.dev** | The `@web` context provider is opt-in — add `"web"` to your `.continue/config.json`'s `contextProviders` array. |
| **Windsurf** | Web search is available via the platform's tool palette. Confirm it's enabled in your Windsurf workspace settings. |
| **GitHub Copilot** | Copilot Chat in supported IDEs has the `@web` participant (Copilot Workspace + recent VS Code Insiders). If your host is older / web-less, fetch sources manually and paste excerpts into the chat, then ask Copilot to refine the file. |

**Can the agent self-configure?** Sometimes. If your host's gap is *permissions* (the tool exists but is gated), an agent with write access to the host's config file can add the right entry — Claude Code can edit `.claude/settings.json`, Continue.dev can edit `.continue/config.json`. Ask the agent to enable web search by editing its own config, then re-run the refinement. If your host's gap is *capability* (the tool doesn't exist), no agent can give itself a new tool — switch hosts or fetch sources manually.

When refinement runs successfully, the marker comment at the top of this file flips from `stub` to `refined` and `bootstrap.json`'s `BEST_PRACTICES_REFINED` flag becomes `true`. Re-running the bootstrap after that point leaves this file alone (it becomes user-owned).
