# Examples

Three sample projects, each fully bootstrapped against a different stack + architecture combination. Browse them to see what the bootstrap actually produces before you run it.

| Example | Stack | Architecture | What it demonstrates |
| --- | --- | --- | --- |
| [`python-4layer-ddd/`](./python-4layer-ddd/) | Python | 4-Layer DDD | Named-layer split: presentation / application / domain / infrastructure. Repositories behind protocols. Constructor DI. |
| [`typescript-vertical-slice/`](./typescript-vertical-slice/) | TypeScript | Vertical Slice | Feature-first folders. Each slice owns its handler / service / model / test. Features import only from `shared/`. |
| [`go-microservice/`](./go-microservice/) | Go | Microservice | 4-Layer DDD internals plus the cross-service surface: health/readiness, retries, distributed tracing, consumer-driven contracts. |

These are **trimmed to the essentials** — each example is ~5–8 files showing the shape, not a full production scaffold. A real bootstrap run produces 25–35 files (rules, ADR templates, security methodology, language manifests, linter configs, every per-tool adapter you picked). The examples here demonstrate the architecture pattern + the brief + a representative slice; the rest is in [`AGENTIC-BOOTSTRAP.md`](../AGENTIC-BOOTSTRAP.md) Part 4 if you want to see all the templates.

The same bootstrap file produced all three. Different `Q4 LANG` + `Q5 ARCH` answers; same disciplined output.
