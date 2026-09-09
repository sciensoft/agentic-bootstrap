.PHONY: help test lint format check run clean rules-check

help:
	@echo "Targets:"
	@echo "  lint         — run the bootstrap cross-reference linter (python scripts/lint_bootstrap.py)"
	@echo "  rules-check  — audit AGENTS.md trigger index (orphans, broken links, budget)"
	@echo "  check        — alias for lint (no separate test step yet)"
	@echo "  run          — open the docs/index.html landing-page preview (open it manually in your browser)"
	@echo "  clean        — remove Python caches left by the lint script"
	@echo ""
	@echo "Targets to fill in as the project grows: test, format"

test:
	@echo "TODO: no test runner yet — wire one up when behaviour code lands"

lint:
	python scripts/lint_bootstrap.py

format:
	@echo "TODO: wire up a markdown / prose formatter if desired (mdformat, prettier, etc.)"

check: lint

run:
	@echo "Open docs/index.html in a browser to preview the landing page."

clean:
	rm -rf __pycache__ .ruff_cache
	find . -type d -name __pycache__ -prune -exec rm -rf {} +

rules-check:
	@echo "== orphaned rules (present on disk but no trigger-index row in AGENTS.md) =="
	@for f in .agents/rules/*.md; do \
	  grep -q "$$(basename $$f)" AGENTS.md || echo "  ORPHANED  $$f"; \
	done
	@echo "== broken links from AGENTS.md into .agents/rules/ =="
	@grep -o '(\.agents/rules/[a-z-]*\.md)' AGENTS.md | tr -d '()' | sort -u | \
	  while read -r p; do [ -f "$$p" ] || echo "  BROKEN  $$p"; done
	@echo "== rules budget (measured 2.88 bytes/token) =="
	@b=$$(( $$(wc -c < AGENTS.md) + $$(wc -c < CLAUDE.md 2>/dev/null || echo 0) )); \
	  echo "  AGENTS.md + CLAUDE.md = $$b bytes  ~$$(( b * 100 / 288 )) tokens"
