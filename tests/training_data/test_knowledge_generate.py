from __future__ import annotations

import json
import shutil
from pathlib import Path

from training_data.inventory import scan_tree
from training_data.knowledge import EvidenceUnit, extract_knowledge
from training_data.knowledge_generate import (
    ConversationCandidate,
    build_knowledge_candidates,
    classify_knowledge_candidates,
    write_knowledge_candidates,
)

FIXTURES = Path(__file__).parents[1] / "fixtures" / "training_data"


def _knowledge_tree(root: Path) -> Path:
    docs = root / "docs"
    for name in (
        "knowledge_article.md",
        "knowledge_child.md",
        "knowledge_index.md",
        "knowledge_missing_source.md",
    ):
        destination = docs / "temes/topic" / name.replace("knowledge_", "")
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(FIXTURES / name, destination)
    return docs


def test_candidates_are_traceable_and_export_only_public_messages(tmp_path: Path) -> None:
    ledger = extract_knowledge(scan_tree(_knowledge_tree(tmp_path)))

    candidates = build_knowledge_candidates(ledger)

    assert candidates
    evidence_ids = {unit.id for unit in ledger.units}
    assert all(candidate.evidence_ids for candidate in candidates)
    assert all(set(candidate.evidence_ids) <= evidence_ids for candidate in candidates)
    assert all(candidate.family_id == candidate.evidence_ids[0] for candidate in candidates)
    assert all(candidate.review_status == "needs_review" for candidate in candidates)
    assert any(candidate.assistant == "Primer element de prova." for candidate in candidates)
    assert all("| --- | --- |" not in candidate.assistant for candidate in candidates)
    assert all(
        candidate.assistant != candidate.user.split("«")[1].split("»")[0]
        for candidate in candidates
    )
    assert all(
        "sobre «Article de coneixement de prova»?" not in candidate.user for candidate in candidates
    )

    public = candidates[0].to_public_record()
    assert set(public) == {"messages"}
    assert public["messages"] == [
        {"role": "user", "content": candidates[0].user},
        {"role": "assistant", "content": candidates[0].assistant},
    ]
    assert all(set(message) == {"role", "content"} for message in public["messages"])


def test_generator_seam_and_candidate_files_are_jsonl(tmp_path: Path) -> None:
    ledger = extract_knowledge(scan_tree(_knowledge_tree(tmp_path)))
    evidence = ledger.units[0]

    class StubGenerator:
        def generate(self, unit: EvidenceUnit, title: str) -> ConversationCandidate | None:
            assert title
            return ConversationCandidate(
                family_id=evidence.id,
                evidence_ids=(evidence.id,),
                user="Pregunta de prova?",
                assistant=evidence.content,
                review_status="needs_review",
            )

    candidates = build_knowledge_candidates(ledger, StubGenerator())
    work = tmp_path / "work"
    internal_path = write_knowledge_candidates(candidates, work=work)

    internal = [json.loads(line) for line in internal_path.read_text().splitlines()]
    public = [
        json.loads(line) for line in (work / "candidate-messages.jsonl").read_text().splitlines()
    ]
    assert len(internal) == len(ledger.units)
    assert all("evidence_ids" in record for record in internal)
    assert all(set(record) == {"messages"} for record in public)


def test_unreviewed_template_questions_cannot_enter_public_candidate_messages(
    tmp_path: Path,
) -> None:
    ledger = extract_knowledge(scan_tree(_knowledge_tree(tmp_path)))
    candidates = build_knowledge_candidates(ledger)
    classification = classify_knowledge_candidates(candidates, ledger)

    assert candidates
    assert not classification.eligible_candidates
    assert all(
        item.status == "unresolved" and item.reason == "human_review_required"
        for item in classification.decisions
    )

    work = tmp_path / "work"
    write_knowledge_candidates(
        candidates,
        work=work,
        classification=classification,
        public_candidates=candidates,
    )

    public_path = work / "candidate-messages.jsonl"
    assert public_path.read_text(encoding="utf-8") == ""
