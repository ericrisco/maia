from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path

import pytest

from training_data.inventory import scan_tree
from training_data.knowledge import extract_knowledge
from training_data.knowledge_coverage import (
    build_knowledge_coverage,
    write_knowledge_coverage,
)
from training_data.knowledge_generate import (
    build_knowledge_candidates,
    classify_knowledge_candidates,
)

FIXTURES = Path(__file__).parents[1] / "fixtures" / "training_data"
INVENTORY_SCRIPT = (
    Path(__file__).resolve().parents[2]
    / "training-data/knowledge/scripts/build_inventory.py"
)


def _inventory_script():
    spec = importlib.util.spec_from_file_location("build_knowledge_inventory", INVENTORY_SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _fixture_tree(root: Path) -> Path:
    docs = root / "docs"
    topic = docs / "temes/topic"
    fonts = docs / "fonts"
    topic.mkdir(parents=True)
    fonts.mkdir()
    for fixture, destination in (
        ("knowledge_article.md", topic / "article.md"),
        ("knowledge_child.md", topic / "child.md"),
        ("knowledge_index.md", topic / "index.md"),
        ("knowledge_missing_source.md", topic / "missing.md"),
        ("source_card.md", fonts / "fixture-source.md"),
    ):
        shutil.copyfile(FIXTURES / fixture, destination)
    return docs


def test_coverage_classifies_every_evidence_unit_and_reports_each_document(
    tmp_path: Path,
) -> None:
    ledger = extract_knowledge(scan_tree(_fixture_tree(tmp_path)))
    candidates = build_knowledge_candidates(ledger)
    classified = classify_knowledge_candidates(candidates, ledger)

    report = build_knowledge_coverage(ledger, classified)

    assert len(report.units) == ledger.report.units_detected
    assert report.represented_units + report.excluded_units + report.unresolved_units == len(
        report.units
    )
    assert report.total_coverage == 1.0
    assert report.trainable_units >= report.trainable_represented_units
    assert report.trainable_coverage == report.trainable_represented_units / report.trainable_units
    assert {entry.path for entry in report.documents} >= {
        "temes/topic/article.md",
        "temes/topic/missing.md",
    }
    assert all(
        item.detected_units == item.represented_units + item.excluded_units + item.unresolved_units
        for item in report.documents
    )
    assert any(unit.status == "unresolved" for unit in report.units)
    assert any(unit.status == "excluded" for unit in report.units)

    output = tmp_path / "reports"
    path = write_knowledge_coverage(report, reports=output)
    serialized = json.loads(path.read_text(encoding="utf-8"))
    assert serialized["total_coverage"] == 1.0
    assert len(serialized["units"]) == len(ledger.units)
    assert len(serialized["documents"]) == len(ledger.documents)


def test_inventory_excludes_table_headers_but_keeps_table_facts() -> None:
    from training_data.knowledge import EvidenceUnit

    inventory_script = _inventory_script()
    header = EvidenceUnit(
        id="topic.md#header",
        document_path="topic.md",
        location="",
        block_index=0,
        block_kind="table_row",
        heading_path=(),
        content="| Any | President |\n",
        provenance=(),
        volatility_score=0.0,
        volatility_status="unreviewed",
        representation_status="unrepresented",
    )
    separator = EvidenceUnit(
        id="topic.md#separator",
        document_path="topic.md",
        location="",
        block_index=1,
        block_kind="table_row",
        heading_path=(),
        content="| --- | --- |\n",
        provenance=(),
        volatility_score=0.0,
        volatility_status="unreviewed",
        representation_status="unrepresented",
    )
    fact = EvidenceUnit(
        id="topic.md#fact",
        document_path="topic.md",
        location="",
        block_index=2,
        block_kind="table_row",
        heading_path=(),
        content="| 2021 | Ada |\n",
        provenance=(),
        volatility_score=0.0,
        volatility_status="unreviewed",
        representation_status="unrepresented",
    )
    headers = inventory_script.table_header_ids([header, separator, fact])

    assert headers == {"topic.md#header"}
    assert (
        inventory_script.exclusion_reason(header, table_headers=headers)
        == "table_header_context_not_standalone_knowledge"
    )
    assert inventory_script.exclusion_reason(separator) == "table_separator_not_knowledge"
    assert inventory_script.exclusion_reason(fact) is None


def test_manual_inventory_exclusions_require_known_ids_and_reasons(tmp_path: Path) -> None:
    inventory_script = _inventory_script()
    path = tmp_path / "manual-unit-exclusions.jsonl"
    path.write_text(
        json.dumps({"evidence_id": "topic.md#note", "reason": "editorial note"}) + "\n",
        encoding="utf-8",
    )

    assert inventory_script.load_manual_exclusions(path, {"topic.md#note"}) == {
        "topic.md#note": "editorial note"
    }
    with pytest.raises(ValueError, match="Unknown manual exclusion"):
        inventory_script.load_manual_exclusions(path, set())
