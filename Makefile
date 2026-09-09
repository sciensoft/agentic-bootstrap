.PHONY: help test lint format check run clean

help:
	@echo "Targets:"
	@echo "  lint   — run the bootstrap cross-reference linter (python scripts/lint_bootstrap.py)"
	@echo "  check  — alias for lint (no separate test step yet)"
	@echo "  run    — open the docs/index.html landing-page preview (open it manually in your browser)"
	@echo "  clean  — remove Python caches left by the lint script"
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
