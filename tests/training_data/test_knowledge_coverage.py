from __future__ import annotations

import json
import shutil
from pathlib import Path

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
