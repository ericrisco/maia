from __future__ import annotations

import shutil
from pathlib import Path

from training_data.inventory import scan_tree
from training_data.knowledge import extract_knowledge
from training_data.knowledge_generate import build_relation_candidates

FIXTURES = Path(__file__).parents[1] / "fixtures" / "training_data"


def test_linked_documents_produce_candidate_with_both_evidence_records(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    topic = docs / "temes/topic"
    topic.mkdir(parents=True)
    for fixture, name in (
        ("knowledge_article.md", "article.md"),
        ("knowledge_child.md", "child.md"),
        ("knowledge_index.md", "index.md"),
    ):
        shutil.copyfile(FIXTURES / fixture, topic / name)
    ledger = extract_knowledge(scan_tree(docs))

    candidates = build_relation_candidates(ledger)

    candidate = next(
        item
        for item in candidates
        if "temes/topic/article.md" in item.family_id and "temes/topic/child.md" in item.family_id
    )
    units = {unit.id: unit for unit in ledger.units}
    assert len(candidate.evidence_ids) >= 2
    assert all(evidence_id in units for evidence_id in candidate.evidence_ids)
    assert {units[evidence_id].document_path for evidence_id in candidate.evidence_ids} == {
        "temes/topic/article.md",
        "temes/topic/child.md",
    }
    assert "enllaça" in candidate.assistant
    assert "Contingut que completa" in candidate.assistant
    assert set(candidate.to_public_record()) == {"messages"}


def test_relation_candidates_skip_unresolved_and_external_links(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    topic = docs / "temes/topic"
    topic.mkdir(parents=True)
    shutil.copyfile(FIXTURES / "knowledge_article.md", topic / "article.md")
    ledger = extract_knowledge(scan_tree(docs))

    candidates = build_relation_candidates(ledger)

    assert candidates == ()
