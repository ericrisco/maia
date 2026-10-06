from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import pytest

from training_data.inventory import scan_tree
from training_data.knowledge import extract_knowledge
from training_data.knowledge_generate import (
    build_knowledge_candidates,
    load_review_conversations,
    review_candidate,
)

FIXTURES = Path(__file__).parents[1] / "fixtures" / "training_data"


def test_manual_review_keeps_evidence_and_improves_direct_answer(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    topic = docs / "temes/topic"
    topic.mkdir(parents=True)
    (docs / "fonts").mkdir()
    shutil.copyfile(FIXTURES / "knowledge_article.md", topic / "article.md")
    shutil.copyfile(FIXTURES / "source_card.md", docs / "fonts/fixture-source.md")
    ledger = extract_knowledge(scan_tree(docs))
    candidate = next(
        item for item in build_knowledge_candidates(ledger) if "s'aplica el 2030" in item.assistant
    )
    evidence_by_id = {unit.id: unit for unit in ledger.units}

    reviewed = review_candidate(
        candidate,
        evidence_by_id=evidence_by_id,
        user="Quan s'aplica aquesta dada?",
        assistant="La dada és activa actualment i s'aplica el 2030.",
    )

    assert reviewed.family_id == candidate.family_id
    assert reviewed.evidence_ids == candidate.evidence_ids
    assert reviewed.review_status == "human_reviewed"
    assert reviewed.user == "Quan s'aplica aquesta dada?"
    assert reviewed.assistant.startswith("La dada")
    assert "2030" in reviewed.assistant
    assert "parcial" not in reviewed.assistant


def test_manual_review_preserves_multiturn_followups(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    topic = docs / "temes/topic"
    topic.mkdir(parents=True)
    shutil.copyfile(FIXTURES / "knowledge_article.md", topic / "article.md")
    (docs / "fonts").mkdir()
    shutil.copyfile(FIXTURES / "source_card.md", docs / "fonts/fixture-source.md")
    ledger = extract_knowledge(scan_tree(docs))
    candidate = next(
        item for item in build_knowledge_candidates(ledger) if "s'aplica el 2030" in item.assistant
    )
    reviewed = review_candidate(
        candidate,
        evidence_by_id={unit.id: unit for unit in ledger.units},
        user="Aquesta norma ja s'aplica?",
        assistant="Sí, és activa actualment i s'aplica el 2030.",
        follow_ups=(("I què canvia aquell any?", "La regla entra en vigor el 2030."),),
    )

    assert [message["role"] for message in reviewed.to_public_record()["messages"]] == [
        "user",
        "assistant",
        "user",
        "assistant",
    ]


def test_review_loader_preserves_turns_and_checks_trace(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    topic = docs / "temes/topic"
    topic.mkdir(parents=True)
    shutil.copyfile(FIXTURES / "knowledge_article.md", topic / "article.md")
    (docs / "fonts").mkdir()
    shutil.copyfile(FIXTURES / "source_card.md", docs / "fonts/fixture-source.md")
    ledger = extract_knowledge(scan_tree(docs))
    messages = [
        {"role": "user", "content": "Com s'aplica la norma?"},
        {"role": "assistant", "content": "La norma és activa actualment."},
        {"role": "user", "content": "I quan entra en vigor?"},
        {"role": "assistant", "content": "Entra en vigor el 2030."},
    ]
    public_record = {"messages": messages}
    digest = hashlib.sha256(
        json.dumps(public_record, ensure_ascii=False, separators=(",", ":")).encode()
    ).hexdigest()
    trace = {
        "example_line": 1,
        "evidence_ids": [ledger.units[0].id],
        "messages_sha256": digest,
        "review_status": "approved",
    }
    conversations_path = tmp_path / "conversations.jsonl"
    provenance_path = tmp_path / "provenance.jsonl"
    conversations_path.write_text(json.dumps(public_record, ensure_ascii=False) + "\n")
    provenance_path.write_text(json.dumps(trace, ensure_ascii=False) + "\n")

    candidate = load_review_conversations(conversations_path, provenance_path, ledger)[0]

    assert candidate.review_status == "human_reviewed"
    assert candidate.to_public_record() == public_record
    trace["messages_sha256"] = "stale"
    provenance_path.write_text(json.dumps(trace, ensure_ascii=False) + "\n")
    with pytest.raises(ValueError, match="hash mismatch"):
        load_review_conversations(conversations_path, provenance_path, ledger)


def test_review_rejects_unknown_evidence_and_empty_wording(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    topic = docs / "temes/topic"
    topic.mkdir(parents=True)
    shutil.copyfile(FIXTURES / "knowledge_article.md", topic / "article.md")
    ledger = extract_knowledge(scan_tree(docs))
    candidate = build_knowledge_candidates(ledger)[0]

    with pytest.raises(ValueError, match="evidence"):
        review_candidate(
            candidate,
            evidence_by_id={},
            user="Pregunta?",
            assistant="Resposta.",
        )

    with pytest.raises(ValueError, match="non-empty"):
        review_candidate(
            candidate,
            evidence_by_id={unit.id: unit for unit in ledger.units},
            user=" ",
            assistant="Resposta.",
        )
