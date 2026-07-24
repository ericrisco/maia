"""Tests for the corpus file validator (PLAN M1.01)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from maia.corpus.validate import main, validate_corpus_file, validate_line


def _doc(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "text": "Andorra és un microestat als Pirineus.",
        "source": "viquipedia",
        "url": "https://ca.wikipedia.org/wiki/Andorra",
        "fetched_at": "2026-08-01T10:00:00Z",
        "license": "cc-by-sa-3.0",
        "registre": "estandard",
    }
    base.update(overrides)
    return base


def _write_jsonl(path: Path, rows: list[Any]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(row if isinstance(row, str) else json.dumps(row, ensure_ascii=False))
            handle.write("\n")


@pytest.mark.unit
def test_valid_line() -> None:
    doc, err = validate_line(json.dumps(_doc()), 1)
    assert err is None
    assert doc is not None and doc.source.value == "viquipedia"


@pytest.mark.unit
def test_invalid_json_line_reports_error() -> None:
    doc, err = validate_line("{not json", 7)
    assert doc is None
    assert err is not None and err.line == 7 and "invalid JSON" in err.reason


@pytest.mark.unit
def test_non_object_line_reports_error() -> None:
    doc, err = validate_line("[1, 2, 3]", 3)
    assert doc is None
    assert err is not None and "expected a JSON object" in err.reason


@pytest.mark.unit
def test_all_valid_file(tmp_path: Path) -> None:
    path = tmp_path / "corpus.jsonl"
    _write_jsonl(
        path,
        [
            _doc(text="doc u"),
            _doc(text="doc dos", source="govern", license="public-official"),
            "",  # blank lines are skipped
            _doc(text="doc tres", source="cultura", license="public-domain"),
        ],
    )
    report = validate_corpus_file(path)
    assert report.total == 3
    assert report.valid == 3
    assert report.ok
    assert report.by_source["govern"] == 1
    assert report.no_redistribute == 0


@pytest.mark.unit
def test_mixed_file_collects_errors_and_line_numbers(tmp_path: Path) -> None:
    path = tmp_path / "corpus.jsonl"
    _write_jsonl(
        path,
        [
            _doc(text="ok"),
            _doc(text="bad", source="INVALID"),
            _doc(text="", source="govern"),  # empty text
        ],
    )
    report = validate_corpus_file(path)
    assert report.total == 3
    assert report.valid == 1
    assert not report.ok
    assert {e.line for e in report.errors} == {2, 3}


@pytest.mark.unit
def test_no_redistribute_is_counted(tmp_path: Path) -> None:
    path = tmp_path / "corpus.jsonl"
    _write_jsonl(
        path,
        [
            _doc(text="public", license="public-official", source="govern"),
            _doc(text="private", license="no-redistribute", source="bopa"),
        ],
    )
    report = validate_corpus_file(path)
    assert report.ok
    assert report.no_redistribute == 1


@pytest.mark.unit
def test_empty_file_is_not_ok(tmp_path: Path) -> None:
    path = tmp_path / "empty.jsonl"
    path.write_text("\n\n", encoding="utf-8")
    report = validate_corpus_file(path)
    assert report.total == 0
    assert not report.ok


@pytest.mark.unit
def test_cli_returns_zero_on_valid(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "corpus.jsonl"
    _write_jsonl(path, [_doc(text="ok")])
    assert main([str(path)]) == 0
    assert "valid: 1" in capsys.readouterr().out


@pytest.mark.unit
def test_cli_returns_one_on_invalid(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "corpus.jsonl"
    _write_jsonl(path, [_doc(text="bad", source="INVALID")])
    assert main([str(path)]) == 1
    assert "invalid: 1" in capsys.readouterr().out


@pytest.mark.unit
def test_cli_missing_file_returns_one(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main([str(tmp_path / "nope.jsonl")]) == 1
    assert "no such file" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_warns_on_no_redistribute(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "corpus.jsonl"
    _write_jsonl(path, [_doc(text="private", license="no-redistribute", source="bopa")])
    assert main([str(path)]) == 0
    assert "no-redistribute" in capsys.readouterr().out


@pytest.mark.unit
def test_cli_truncates_long_error_list(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "corpus.jsonl"
    _write_jsonl(path, [_doc(text=f"bad {i}", source="INVALID") for i in range(55)])
    assert main([str(path)]) == 1
    out = capsys.readouterr().out
    assert "and 5 more" in out
