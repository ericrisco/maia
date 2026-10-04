from __future__ import annotations

import json
import shutil
from pathlib import Path

from training_data.inventory import scan_tree
from training_data.knowledge import extract_knowledge, write_knowledge_extraction

FIXTURES = Path(__file__).parents[1] / "fixtures" / "training_data"


def _copy_fixture(source: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(FIXTURES / source, destination)


def _knowledge_tree(root: Path) -> Path:
    docs = root / "docs"
    _copy_fixture("knowledge_article.md", docs / "temes/topic/article.md")
    _copy_fixture("knowledge_child.md", docs / "temes/topic/child.md")
    _copy_fixture("knowledge_index.md", docs / "temes/topic/index.md")
    _copy_fixture("knowledge_missing_source.md", docs / "temes/topic/missing-source.md")
    _copy_fixture("malformed_frontmatter.md", docs / "temes/topic/broken.md")
    _copy_fixture("source_card.md", docs / "fonts/fixture-source.md")
    return docs


def test_knowledge_extraction_preserves_units_provenance_and_relations(tmp_path: Path) -> None:
    docs = _knowledge_tree(tmp_path)

    ledger = extract_knowledge(scan_tree(docs))

    assert ledger.report.processed_documents == 5
    assert ledger.report.markdown_errors == 1
    assert ledger.report.sections_processed == 1
    assert ledger.report.tables_processed == 1
    assert ledger.report.table_rows_processed == 3
    assert ledger.report.units_detected == len(ledger.units)
    assert ledger.report.links_detected == 3
    assert ledger.report.internal_links_detected == 2

    documents = {document.path: document for document in ledger.documents}
    article = documents["temes/topic/article.md"]
    assert article.evidence_ids
    assert article.provenance[0].source_id == "fixture-source"
    assert article.provenance[0].status == "recorded"
    assert article.provenance[0].redistribution == "pendent"
    assert "parcial" in " ".join(
        unit.content for unit in ledger.units if unit.document_path == article.path
    )

    index = documents["temes/topic/index.md"]
    assert index.evidence_ids
    assert index.provenance[0].status == "missing_source_id"

    missing = documents["temes/topic/missing-source.md"]
    assert missing.provenance[0].status == "missing_source_card"
    assert "missing_source_card" in {issue.code for issue in ledger.unresolved}
    assert "markdown_error" in {issue.code for issue in ledger.unresolved}

    relation = next(
        relation
        for relation in ledger.relations
        if relation.source_path == article.path and relation.target == "child.md"
    )
    assert relation.internal is True
    assert relation.target_path == "temes/topic/child.md"
    assert relation.resolved is True

    volatile_candidates = [unit for unit in ledger.units if unit.volatility_score > 0]
    assert volatile_candidates
    assert all(unit.volatility_status == "unreviewed" for unit in ledger.units)
    assert article.path not in {issue.path for issue in ledger.exclusions}


def test_knowledge_report_and_work_ledgers_are_reproducible_json(tmp_path: Path) -> None:
    docs = _knowledge_tree(tmp_path)
    ledger = extract_knowledge(scan_tree(docs))
    work = tmp_path / "Maia Knowledge" / "work"
    reports = tmp_path / "Maia Knowledge" / "reports"

    report = write_knowledge_extraction(ledger, work=work, reports=reports)

    evidence_lines = (work / "evidence.jsonl").read_text(encoding="utf-8").splitlines()
    relation_lines = (work / "relations.jsonl").read_text(encoding="utf-8").splitlines()
    issue_lines = (work / "unresolved.jsonl").read_text(encoding="utf-8").splitlines()
    report_json = json.loads((reports / "inventory.json").read_text(encoding="utf-8"))
    assert len(evidence_lines) == report.units_detected
    assert all(isinstance(json.loads(line), dict) for line in evidence_lines)
    assert all(isinstance(json.loads(line), dict) for line in relation_lines)
    assert all(isinstance(json.loads(line), dict) for line in issue_lines)
    assert report_json["processed_documents"] == 5
    assert report_json["table_rows_processed"] == 3
