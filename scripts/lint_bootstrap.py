#!/usr/bin/env python3
"""Consistency lint for AGENTIC-BOOTSTRAP.md.

Checks (each one independent; all run every invocation):

1. **Q-numbers** in the interview table are sequential 1..N with no gaps and
   start at Q1. Renumbering mistakes (e.g. inserting Q12 without renumbering
   Q12+ to Q13+) get caught here.

2. **`{{IF_FLAG}}` references** in templates all match a flag in the
   `bootstrap.json` `answers` schema. Adding `{{IF_NEWFLAG}}` to a template
   without extending the schema is a silent miss until a user re-runs and
   the new question never gets persisted.

3. **Decision-matrix rows** in Part 3 all point to a Part 4 template that
   actually exists. Removing a template without removing its matrix row
   (or vice versa) leaves an unwritten file the bootstrap thinks it wrote.

4. **Version header ↔ changelog** — the `<!-- bootstrap-version: ... -->`
   header in AGENTIC-BOOTSTRAP.md matches the most recent dated entry in
   `CHANGELOG.md`. Bumping one without the other means re-run
   Step 8's upgrade narrative says the wrong thing.

5. **Template Index offsets ↔ actual `### Template:` positions** — the
   Index table at the start of Part 4 lets capable agents skip irrelevant
   templates via offset reads. Stale offsets degrade gracefully (the
   drift safeguard re-greps when a read doesn't land on a heading), but
   silently waste tokens. Catching drift in CI is cheaper than letting
   it accumulate.

Exit code 0 on clean, 1 on any finding. Findings to stderr, one per line,
prefixed with the check name.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP_PATH = REPO_ROOT / "AGENTIC-BOOTSTRAP.md"
CHANGELOG_PATH = REPO_ROOT / "CHANGELOG.md"


def main() -> int:
    if not BOOTSTRAP_PATH.exists():
        print(f"ERROR: missing {BOOTSTRAP_PATH}", file=sys.stderr)
        return 1
    if not CHANGELOG_PATH.exists():
        print(f"ERROR: missing {CHANGELOG_PATH}", file=sys.stderr)
        return 1

    bootstrap = BOOTSTRAP_PATH.read_text()
    changelog = CHANGELOG_PATH.read_text()

    findings: list[str] = []
    findings += check_q_numbers(bootstrap)
    findings += check_if_flags(bootstrap)
    findings += check_decision_matrix(bootstrap)
    findings += check_version(bootstrap, changelog)
    findings += check_template_index(bootstrap)

    if not findings:
        print("lint_bootstrap: OK (5 checks passed)")
        return 0

    print(f"lint_bootstrap: FAIL ({len(findings)} finding(s))", file=sys.stderr)
    for f in findings:
        print(f"  - {f}", file=sys.stderr)
    return 1


# ---------- checks ----------------------------------------------------------


def check_q_numbers(bootstrap: str) -> list[str]:
    """Interview rows must be Q1..QN with no gaps."""
    qs = re.findall(r"^\| Q(\d+) \|", bootstrap, re.MULTILINE)
    nums = sorted({int(n) for n in qs})
    if not nums:
        return ["q_numbers: no interview rows found"]
    findings: list[str] = []
    if nums[0] != 1:
        findings.append(f"q_numbers: first question is Q{nums[0]}, expected Q1")
    expected = set(range(1, max(nums) + 1))
    missing = sorted(expected - set(nums))
    if missing:
        findings.append(
            "q_numbers: gaps in interview sequence (missing "
            + ", ".join(f"Q{n}" for n in missing)
            + ")"
        )
    return findings


# Derived flags — computed from other answers, not persisted in bootstrap.json.
# Document each one when adding it (see Part 1 "Derived flags").
DERIVED_FLAGS = {"LAYERED"}


def check_if_flags(bootstrap: str) -> list[str]:
    """Every {{IF_<FLAG>}} inside Part 4 must resolve to a real flag.

    Valid forms:
      {{IF_KEY}}            where KEY is in bootstrap.json answers
      {{IF_KEY}}            where KEY is a derived flag (see DERIVED_FLAGS above)
      {{IF_KEY_VALUE}}      value-equality conditional; KEY must be in answers
                            and treated as a string-typed key (LICENSE, POSTURE, ARCH, LANG)

    Scope: only checked inside Part 4 (templates). Part 6 ("How to extend")
    uses {{IF_FLAG}} / {{IF_NEWFLAG}} as illustrative placeholders — not real flags.
    """
    answer_keys, string_keys = _bootstrap_json_schema(bootstrap)
    if not answer_keys:
        return ["if_flags: could not parse bootstrap.json answers schema"]

    part4 = _extract_section(bootstrap, "## Part 4 — File templates", "## Part 5 ")
    if not part4:
        return ["if_flags: could not locate Part 4 section"]

    used = set(re.findall(r"\{\{IF_([A-Z][A-Z0-9_]*)\}\}", part4))
    unresolved: set[str] = set()
    for name in used:
        if name in answer_keys or name in DERIVED_FLAGS:
            continue
        # Value-equality form: KEY_VALUE where KEY is a string-typed schema key.
        # Find the longest matching prefix; the rest is the value label.
        matched = False
        for key in sorted(string_keys, key=len, reverse=True):
            if name == key:
                matched = True
                break
            if name.startswith(key + "_"):
                matched = True
                break
        if not matched:
            unresolved.add(name)

    findings: list[str] = []
    if unresolved:
        findings.append(
            "if_flags: Part 4 templates reference flags not in bootstrap.json answers: "
            + ", ".join(sorted(unresolved))
        )
    return findings


def _bootstrap_json_schema(bootstrap: str) -> tuple[set[str], set[str]]:
    """Return (all answer keys, keys whose value is a string literal in the template).

    String-typed keys are the ones that can carry value-equality conditionals
    (e.g. {{IF_LICENSE_MIT}}). Boolean-typed keys (`{{KEY}}` with no quotes around
    the placeholder) can only be used in plain {{IF_KEY}} form.
    """
    template_match = re.search(
        r"### Template: `\.agents/bootstrap\.json`.*?```json(.*?)```",
        bootstrap,
        re.DOTALL,
    )
    if not template_match:
        return set(), set()
    json_block = template_match.group(1)

    answers_match = re.search(r'"answers"\s*:\s*\{(.*?)\n\s*\}', json_block, re.DOTALL)
    if not answers_match:
        return set(), set()
    body = answers_match.group(1)

    keys = set(re.findall(r'"([A-Z][A-Z0-9_]*)"\s*:', body))
    # String-typed: value is "{{KEY}}" wrapped in quotes; boolean-typed: value is {{KEY}}.
    string_keys = set(
        re.findall(r'"([A-Z][A-Z0-9_]*)"\s*:\s*"\{\{[^}]+\}\}"', body)
    )
    return keys, string_keys


def _extract_section(text: str, start_marker: str, end_marker: str) -> str:
    start = text.find(start_marker)
    if start < 0:
        return ""
    end = text.find(end_marker, start + len(start_marker))
    if end < 0:
        return text[start:]
    return text[start:end]


def check_decision_matrix(bootstrap: str) -> list[str]:
    """Every matrix row must point to a Part 4 template that exists."""
    # Carve out Part 3 — the matrix lives between Part 3's heading and Part 4's.
    part3_start = bootstrap.find("## Part 3 — Decision matrix")
    part4_start = bootstrap.find("## Part 4 — File templates")
    if part3_start < 0 or part4_start < 0 or part4_start <= part3_start:
        return ["matrix: could not locate Part 3 / Part 4 section boundaries"]
    part3 = bootstrap[part3_start:part4_start]
    part4 = bootstrap[part4_start:]

    # Matrix rows look like:  | `<path>` | <Type> | <Trigger> | <Re-run> |
    # The first column is a backtick-wrapped path (may include placeholders like <...>).
    paths = re.findall(r"^\| `([^`]+)` \|", part3, re.MULTILINE)

    # Part 4 templates are headed by:  ### Template: `<path>` (optionally with variant suffix)
    template_paths = set(re.findall(r"^### Template: `([^`]+)`", part4, re.MULTILINE))

    findings: list[str] = []
    for path in paths:
        # Skip dynamic placeholders — the row describes a class of files, not one path.
        if "<" in path:
            continue
        # Allow loose match: a row like `.docs/prompts/<ts>.bootstrap_project.md` is
        # filtered by the `<` check above; everything else should match a template.
        if path in template_paths:
            continue
        findings.append(f"matrix: row for `{path}` has no matching Part 4 template")
    return findings


def check_version(bootstrap: str, changelog: str) -> list[str]:
    """Bootstrap version header must match the most recent dated changelog entry."""
    header_match = re.search(
        r"<!--\s*bootstrap-version:\s*(\d{4}-\d{2}-\d{2})\s*-->", bootstrap
    )
    if not header_match:
        return ["version: no <!-- bootstrap-version: --> header found"]
    bootstrap_version = header_match.group(1)

    # Most recent dated entry. Keep-a-Changelog convention: dated entries are
    # listed reverse-chronologically; [Unreleased] sits above them and is skipped.
    dated = re.findall(r"^##\s*\[(\d{4}-\d{2}-\d{2})\]", changelog, re.MULTILINE)
    if not dated:
        return ["version: no dated entries (## [YYYY-MM-DD]) in changelog"]
    most_recent = dated[0]

    if bootstrap_version != most_recent:
        return [
            f"version: bootstrap-version header is {bootstrap_version} but most "
            f"recent dated changelog entry is {most_recent} — bump one to match the other"
        ]
    return []


def check_template_index(bootstrap: str) -> list[str]:
    """Template Index in Part 4 must stay in sync with actual `### Template:` positions.

    The Index lets capable agents skip irrelevant templates via offset reads
    (Read(offset=START, limit=END-START+1)). Stale offsets don't break
    correctness (the drift safeguard re-greps), but waste tokens silently.
    """
    actual_ranges, err = _actual_template_ranges(bootstrap)
    if err is not None:
        return [err]

    index_ranges, err = _parse_template_index_rows(bootstrap)
    if err is not None:
        return [err]

    return _diff_template_ranges(bootstrap, actual_ranges, index_ranges)


def _actual_template_ranges(bootstrap: str) -> tuple[list[tuple[int, int]], str | None]:
    """Return (start, end) tuples for every `### Template:` heading in Part 4."""
    template_lines = [
        i
        for i, line in enumerate(bootstrap.splitlines(), start=1)
        if line.startswith("### Template:")
    ]
    if not template_lines:
        return [], "template_index: no `### Template:` headings found in file"

    part5_match = re.search(r"^## Part 5 ", bootstrap, re.MULTILINE)
    if not part5_match:
        return [], (
            "template_index: could not locate `## Part 5` heading "
            "(needed to compute the last template's end line)"
        )
    part5_line = bootstrap[: part5_match.start()].count("\n") + 1

    ranges = [
        (start, (template_lines[i + 1] - 1) if i + 1 < len(template_lines) else part5_line - 1)
        for i, start in enumerate(template_lines)
    ]
    return ranges, None


def _parse_template_index_rows(
    bootstrap: str,
) -> tuple[list[tuple[int, int]], str | None]:
    """Parse the Part 4 Template Index table into a list of (start, end) tuples."""
    index_header = "### Template Index"
    idx_start = bootstrap.find(index_header)
    if idx_start < 0:
        return [], (
            "template_index: no `### Template Index` heading found in Part 4 "
            "— the offset-read optimisation requires one"
        )
    next_section = re.search(
        r"^### ", bootstrap[idx_start + len(index_header) :], re.MULTILINE
    )
    idx_end = (
        idx_start + len(index_header) + next_section.start()
        if next_section
        else len(bootstrap)
    )
    row_pattern = re.compile(r"^\|.*?\|.*?\|\s*(\d+)\s*→\s*(\d+)\s*\|", re.MULTILINE)
    ranges = [
        (int(m.group(1)), int(m.group(2)))
        for m in row_pattern.finditer(bootstrap[idx_start:idx_end])
    ]
    if not ranges:
        return [], (
            "template_index: no rows matching `| ... | ... | START → END |` "
            "parsed from the Index table"
        )
    return ranges, None


def _diff_template_ranges(
    bootstrap: str,
    actual: list[tuple[int, int]],
    index: list[tuple[int, int]],
) -> list[str]:
    """Compare Index rows against actual template positions, summarise mismatches."""
    findings: list[str] = []
    if len(index) != len(actual):
        findings.append(
            f"template_index: row count mismatch — Index table has {len(index)} "
            f"rows, file has {len(actual)} `### Template:` headings"
        )

    lines = bootstrap.splitlines()
    mismatches = [
        _format_template_mismatch(i, lines, actual[i], index[i])
        for i in range(min(len(index), len(actual)))
        if actual[i] != index[i]
    ]
    if not mismatches:
        return findings

    findings.append(
        f"template_index: {len(mismatches)} offset mismatch(es) "
        f"— re-grep `^### Template:` in AGENTIC-BOOTSTRAP.md to refresh the table"
    )
    findings.extend(f"template_index: {m}" for m in mismatches[:3])
    if len(mismatches) > 3:
        findings.append(
            f"template_index: ...and {len(mismatches) - 3} more mismatches "
            f"(showing first 3)"
        )
    return findings


def _format_template_mismatch(
    i: int,
    lines: list[str],
    actual: tuple[int, int],
    index: tuple[int, int],
) -> str:
    """Format one row mismatch with the template path for context."""
    path_match = re.search(r"### Template: `([^`]+)`", lines[actual[0] - 1])
    path = path_match.group(1) if path_match else f"line {actual[0]}"
    return (
        f"row {i + 1} (`{path}`): "
        f"index says {index[0]} → {index[1]}, "
        f"actual is {actual[0]} → {actual[1]}"
    )


if __name__ == "__main__":
    sys.exit(main())
