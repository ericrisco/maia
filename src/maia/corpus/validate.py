"""Corpus validator (PLAN M1.01) — enforces the §3.1 contract at 100 %.

Reads a JSONL corpus file (one document per line) and validates every line against
:class:`maia.schemas.CorpusDocument`. Blocks all scrapers: nothing lands in the corpus
that does not conform. Also surfaces the licensing signal (count of `no-redistribute`
documents, which must never reach public artifacts).

CLI:  ``maia-validate-corpus path/to/corpus.jsonl``  (exit 1 if any line is invalid).
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from pydantic import ValidationError

from maia.schemas import CorpusDocument, License


@dataclass(frozen=True)
class LineError:
    """A single invalid line: its 1-based number and a human-readable reason."""

    line: int
    reason: str


@dataclass
class ValidationReport:
    """Outcome of validating a corpus file."""

    total: int = 0
    valid: int = 0
    errors: list[LineError] = field(default_factory=list)
    by_source: Counter[str] = field(default_factory=Counter)
    by_license: Counter[str] = field(default_factory=Counter)

    @property
    def ok(self) -> bool:
        """True iff every line conformed (0 errors) and the file was non-empty."""
        return not self.errors and self.total > 0

    @property
    def no_redistribute(self) -> int:
        """Documents that must never enter public artifacts (compliance signal)."""
        return self.by_license.get(License.NO_REDISTRIBUTE.value, 0)


def _format_validation_error(exc: ValidationError) -> str:
    parts = [f"{'.'.join(str(x) for x in e['loc']) or '<root>'}: {e['msg']}" for e in exc.errors()]
    return "; ".join(parts)


def validate_line(raw: str, line_no: int) -> tuple[CorpusDocument | None, LineError | None]:
    """Validate one JSONL line. Returns (document, None) or (None, error)."""
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        return None, LineError(line_no, f"invalid JSON: {exc.msg}")
    if not isinstance(data, dict):
        return None, LineError(line_no, f"expected a JSON object, got {type(data).__name__}")
    try:
        return CorpusDocument.model_validate(data), None
    except ValidationError as exc:
        return None, LineError(line_no, _format_validation_error(exc))


def validate_corpus_file(path: Path) -> ValidationReport:
    """Validate every non-blank line of a JSONL corpus file."""
    report = ValidationReport()
    with path.open(encoding="utf-8") as handle:
        for line_no, raw in enumerate(handle, start=1):
            if not raw.strip():
                continue
            report.total += 1
            doc, err = validate_line(raw, line_no)
            if err is not None:
                report.errors.append(err)
                continue
            assert doc is not None
            report.valid += 1
            report.by_source[doc.source.value] += 1
            report.by_license[doc.license.value] += 1
    return report


def _render(report: ValidationReport, path: Path) -> str:
    lines = [
        f"corpus: {path}",
        f"  documents: {report.total}  valid: {report.valid}  invalid: {len(report.errors)}",
    ]
    if report.by_source:
        by_src = ", ".join(f"{k}={v}" for k, v in sorted(report.by_source.items()))
        lines.append(f"  by source: {by_src}")
    if report.no_redistribute:
        lines.append(
            f"  ⚠ no-redistribute (grounding-only, never public): {report.no_redistribute}"
        )
    for err in report.errors[:50]:
        lines.append(f"  ✗ line {err.line}: {err.reason}")
    if len(report.errors) > 50:
        lines.append(f"  … and {len(report.errors) - 50} more")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    """CLI entry point. Exit 0 if the corpus fully conforms, 1 otherwise."""
    parser = argparse.ArgumentParser(description="Validate a JSONL corpus against the §3.1 schema.")
    parser.add_argument("path", type=Path, help="path to the JSONL corpus file")
    args = parser.parse_args(argv)

    if not args.path.is_file():
        print(f"error: no such file: {args.path}", file=sys.stderr)
        return 1

    report = validate_corpus_file(args.path)
    print(_render(report, args.path))
    return 0 if report.ok else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
