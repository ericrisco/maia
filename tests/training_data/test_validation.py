from __future__ import annotations

import json
from pathlib import Path

from training_data.inventory import scan_tree
from training_data.knowledge import extract_knowledge
from training_data.knowledge_coverage import build_knowledge_coverage
from training_data.knowledge_deduplicate import deduplicate_knowledge_candidates
from training_data.knowledge_generate import (
    build_knowledge_candidates,
    classify_knowledge_candidates,
    review_candidate,
)
from training_data.knowledge_split import split_knowledge_candidates, write_knowledge_splits
from training_data.language import (
    LanguageLedger,
    LanguageSelectionReport,
    SpeechPiece,
    SpeechProvenance,
    UncertaintySpan,
)
from training_data.language_conversations import build_human_conversations
from training_data.language_split import split_language_conversations, write_language_splits
from training_data.language_uncertainty import filter_uncertain_conversations
from training_data.validation import (
    validate_knowledge_dataset,
    validate_language_dataset,
    validate_public_splits,
)


def _paths(root: Path) -> dict[str, Path]:
    return {name: root / f"{name}.jsonl" for name in ("train", "validation", "test")}


def test_public_validator_rejects_markdown_metadata_and_exact_duplicates(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    valid = {
        "messages": [
            {"role": "user", "content": "Què és això?"},
            {"role": "assistant", "content": "Una resposta."},
        ]
    }
    paths["train"].write_text(json.dumps(valid) + "\n", encoding="utf-8")
    paths["validation"].write_text(json.dumps(valid) + "\n", encoding="utf-8")
    invalid = {
        "messages": [
            {"role": "user", "content": "Què és això?"},
            {"role": "assistant", "content": "**Una resposta.**"},
        ],
        "evidence_ids": ["internal"],
    }
    paths["test"].write_text(json.dumps(invalid) + "\n", encoding="utf-8")

    report = validate_public_splits(paths, dataset="fixture")

    assert not report.valid
    codes = {issue.code for issue in report.issues}
    assert "exact_duplicate" in codes
    assert "public_schema" in codes
    assert report.exact_duplicates == 1


def test_public_validator_accepts_complete_multiturn_conversation(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    record = {
        "messages": [
            {"role": "user", "content": "La Passa és un ball?"},
            {"role": "assistant", "content": "No, és una cercavila."},
            {"role": "user", "content": "Qui va al davant?"},
            {"role": "assistant", "content": "Les parelles que es casaran aquell any."},
        ]
    }
    paths["train"].write_text(json.dumps(record) + "\n", encoding="utf-8")
    paths["validation"].write_text("", encoding="utf-8")
    paths["test"].write_text("", encoding="utf-8")

    report = validate_public_splits(paths, dataset="fixture")

    assert report.valid, report.issues
    assert report.record_counts == {"train": 1, "validation": 0, "test": 0}


def test_knowledge_validator_accepts_grounded_clean_splits(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    (docs / "temes/topic").mkdir(parents=True)
    (docs / "fonts").mkdir()
    (docs / "fonts/source.md").write_text(
        "---\ntype: font\nid: source\ntitle: Font\nredistribucio: si\n---\n",
        encoding="utf-8",
    )
    (docs / "temes/topic/article.md").write_text(
        "---\ntype: article\ntitle: Festa local\nfont: source\n---\n\n"
        "# Festa local\n\nLa festa local se celebra cada hivern.\n",
        encoding="utf-8",
    )
    ledger = extract_knowledge(scan_tree(docs))
    draft_candidates = build_knowledge_candidates(ledger)
    evidence_by_id = {unit.id: unit for unit in ledger.units}
    candidates = tuple(
        review_candidate(
            item,
            evidence_by_id=evidence_by_id,
            user="Quan se celebra la festa local?",
            assistant="La festa local se celebra cada hivern.",
        )
        for item in draft_candidates
        if "La festa local se celebra cada hivern." in item.assistant
    )
    assert candidates
    classification = classify_knowledge_candidates(candidates, ledger)
    deduplicated = deduplicate_knowledge_candidates(classification.eligible_candidates)
    split = split_knowledge_candidates(deduplicated.candidates)
    output = tmp_path / "output"
    paths = write_knowledge_splits(split, output=output, work=tmp_path / "work")
    coverage = build_knowledge_coverage(ledger, classification)

    report = validate_knowledge_dataset(paths, split, ledger, coverage)

    assert report.valid, report.issues
    assert report.record_counts == split.manifest.actual_counts


def _language_ledger(text: str, *, uncertain: bool = False) -> LanguageLedger:
    source_start = text.find("[?dubte]") if uncertain else -1
    piece = SpeechPiece(
        path="parla/oral/sample.md",
        piece_id="parla/oral/sample",
        title="Testimoni",
        document_type="parla",
        voice="originaria",
        epoch="contemporania",
        language_eligible=True,
        text=text,
        provenance=(SpeechProvenance("source", "fonts/source.md", "recorded", "pendent"),),
        uncertainty_spans=(
            (UncertaintySpan(source_start, source_start + len("[?dubte]"), "[?dubte]"),)
            if uncertain
            else ()
        ),
        eligibility="eligible",
        reason="all_eligibility_fields_and_source_recorded",
    )
    return LanguageLedger(
        (piece,), LanguageSelectionReport(1, 1, 0, 1, 0, 0, int(uncertain), {"pendent": 1})
    )


def test_language_validator_accepts_only_source_exact_eligible_clean_turns(tmp_path: Path) -> None:
    ledger = _language_ledger("Entrevistador: I això com ho fèieu?\nParlant: Ho fèiem així.\n")
    candidates = build_human_conversations(ledger)
    filtered = filter_uncertain_conversations(ledger, candidates)
    split = split_language_conversations(filtered.accepted)
    paths = write_language_splits(split, output=tmp_path / "output", work=tmp_path / "work")

    report = validate_language_dataset(paths, split, ledger)

    assert report.valid, report.issues


def test_language_validator_rejects_uncertain_spans_even_if_bypassing_filter(
    tmp_path: Path,
) -> None:
    ledger = _language_ledger(
        "Entrevistador: I això com ho fèieu?\nParlant: Ho fèiem [?dubte] així.\n",
        uncertain=True,
    )
    candidates = build_human_conversations(ledger)
    split = split_language_conversations(candidates)
    paths = write_language_splits(split, output=tmp_path / "output", work=tmp_path / "work")

    report = validate_language_dataset(paths, split, ledger)

    assert not report.valid
    assert "uncertain_language_turn" in {issue.code for issue in report.issues}
