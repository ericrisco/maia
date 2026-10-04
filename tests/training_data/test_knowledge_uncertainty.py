from __future__ import annotations

import json
from pathlib import Path

from training_data.inventory import scan_tree
from training_data.knowledge import extract_knowledge
from training_data.knowledge_generate import (
    build_knowledge_candidates,
    classify_knowledge_candidates,
    write_knowledge_candidates,
)


def _tree(root: Path) -> Path:
    docs = root / "docs"
    fonts = docs / "fonts"
    topic = docs / "temes/topic"
    fonts.mkdir(parents=True)
    topic.mkdir(parents=True)
    (fonts / "fixture-source.md").write_text(
        "---\ntype: font\nid: fixture-source\ntitle: Font de prova\n"
        "redistribucio: pendent\n---\n\n# Font de prova\n",
        encoding="utf-8",
    )
    (topic / "review.md").write_text(
        "---\ntype: article\ntitle: Fitxa revisable\nfont: fixture-source\n---\n\n"
        "# Fitxa revisable\n\n"
        "Les fonts discrepen: una situa la festa el 4 de juliol i l'altra el 6 de juliol.\n\n"
        "El corpus no permet determinar la data exacta.\n\n"
        "El càrrec continua en actiu actualment i s'allarga fins al 2030.\n\n"
        "La festa se celebra al poble.\n",
        encoding="utf-8",
    )
    (topic / "missing.md").write_text(
        "---\ntype: article\ntitle: Font absent\nfont: missing-source\n---\n\n"
        "Una dada sense procedència registrada.\n",
        encoding="utf-8",
    )
    return docs


def test_classification_preserves_conflicts_and_unknowns_and_blocks_unsafe_items(
    tmp_path: Path,
) -> None:
    ledger = extract_knowledge(scan_tree(_tree(tmp_path)))
    candidates = build_knowledge_candidates(ledger)

    classified = classify_knowledge_candidates(candidates, ledger)

    conflict = next(
        candidate
        for candidate in candidates
        if candidate.assistant.startswith("Les fonts discrepen")
    )
    conflict_decision = next(
        decision for decision in classified.decisions if decision.family_id == conflict.family_id
    )
    assert conflict_decision.status == "included"
    assert conflict_decision.reason == "explicit_conflict_preserved"
    assert conflict.assistant == (
        "Les fonts discrepen: una situa la festa el 4 de juliol i l'altra el 6 de juliol."
    )

    unknown = next(
        candidate
        for candidate in candidates
        if candidate.assistant.startswith("El corpus no permet determinar")
    )
    unknown_decision = next(
        decision for decision in classified.decisions if decision.family_id == unknown.family_id
    )
    assert unknown_decision.status == "included"
    assert unknown_decision.reason == "explicit_unknown_preserved"
    assert unknown.assistant == "El corpus no permet determinar la data exacta."

    volatile = next(
        candidate
        for candidate in candidates
        if candidate.assistant.startswith("El càrrec continua en actiu")
    )
    volatile_decision = next(
        decision for decision in classified.decisions if decision.family_id == volatile.family_id
    )
    assert volatile_decision.status == "excluded"
    assert volatile_decision.reason == "volatility_threshold"
    assert volatile not in classified.eligible_candidates

    unprovenanced = next(
        candidate
        for candidate in candidates
        if candidate.assistant == "Una dada sense procedència registrada."
    )
    missing_decision = next(
        decision
        for decision in classified.decisions
        if decision.family_id == unprovenanced.family_id
    )
    assert missing_decision.status == "unresolved"
    assert missing_decision.reason == "missing_or_invalid_provenance"
    assert unprovenanced not in classified.eligible_candidates
    assert classified.unresolved_count > 0
    assert classified.excluded_count > 0
    assert classified.explicit_conflict_count == 1
    assert classified.explicit_unknown_count == 1

    work = tmp_path / "work"
    write_knowledge_candidates(candidates, work=work, classification=classified)
    public_records = [
        json.loads(line)
        for line in (work / "candidate-messages.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    serialized_public = json.dumps(public_records, ensure_ascii=False)
    assert volatile.assistant not in serialized_public
    assert unprovenanced.assistant not in serialized_public
    decisions = [
        json.loads(line)
        for line in (work / "candidate-decisions.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert len(decisions) == len(candidates)
    summary = json.loads((work / "candidate-classification.json").read_text(encoding="utf-8"))
    assert summary["excluded"] == classified.excluded_count


def test_pending_redistribution_is_visible_but_not_an_automatic_exclusion(tmp_path: Path) -> None:
    ledger = extract_knowledge(scan_tree(_tree(tmp_path)))
    candidates = build_knowledge_candidates(ledger)

    classified = classify_knowledge_candidates(candidates, ledger)

    stable = next(
        candidate
        for candidate in candidates
        if candidate.assistant == "La festa se celebra al poble."
    )
    decision = next(
        decision for decision in classified.decisions if decision.family_id == stable.family_id
    )
    assert decision.status == "included"
    assert decision.reason == "source_redistribution_pending"
    assert stable in classified.eligible_candidates
