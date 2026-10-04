from __future__ import annotations

import json
from pathlib import Path

from training_data.language import (
    LanguageLedger,
    LanguageSelectionReport,
    SpeechPiece,
    SpeechProvenance,
    UncertaintySpan,
)
from training_data.language_conversations import build_human_conversations
from training_data.language_uncertainty import (
    filter_uncertain_conversations,
    write_language_uncertainty_result,
)


def test_uncertain_turns_are_removed_and_clean_turns_remain_verbatim(tmp_path: Path) -> None:
    text = (
        "Entrevistador: I això com ho fèieu?\n"
        "Parlant: Ho fèiem [?així] abans.\n"
        "Entrevistador: I quan hi anàveu?\n"
        "Parlant: Cada dissabte.\n"
    )
    marker_start = text.index("[?així]")
    piece = SpeechPiece(
        path="parla/oral/interview.md",
        piece_id="parla/oral/interview",
        title="Entrevista",
        document_type="parla",
        voice="originaria",
        epoch="contemporania",
        language_eligible=True,
        text=text,
        provenance=(SpeechProvenance("source", "fonts/source.md", "recorded", "pendent"),),
        uncertainty_spans=(UncertaintySpan(marker_start, marker_start + 7, "[?així]"),),
        eligibility="eligible",
        reason="all_eligibility_fields_and_source_recorded",
    )
    ledger = LanguageLedger((piece,), LanguageSelectionReport(1, 1, 0, 1, 0, 0, 1, {"pendent": 1}))
    candidates = build_human_conversations(ledger)

    result = filter_uncertain_conversations(ledger, candidates)

    assert len(candidates) == 2
    assert len(result.accepted) == 1
    assert result.accepted[0].user == "I quan hi anàveu?"
    assert result.accepted[0].assistant == "Cada dissabte."
    assert len(result.excluded) == 1
    assert result.excluded[0].reason == "uncertain_span_in_turn"
    assert result.report.input_candidates == 2
    assert result.report.accepted_candidates == 1
    assert result.report.excluded_candidates == 1
    assert result.report.uncertainty_spans_discarded == 1
    assert all("[?" not in candidate.user + candidate.assistant for candidate in result.accepted)

    write_language_uncertainty_result(
        ledger,
        result,
        work=tmp_path / "work",
        reports=tmp_path / "reports",
    )
    public = [
        json.loads(line)
        for line in (tmp_path / "work/accepted-messages.jsonl").read_text().splitlines()
    ]
    assert len(public) == 1
    assert "[?" not in json.dumps(public, ensure_ascii=False)
    assert public[0]["messages"][1]["content"] == "Cada dissabte."


def test_uncertainty_outside_selected_dialogue_does_not_contaminate_turns() -> None:
    text = "Nota: [?font]\nEntrevistador: Com ho fèieu?\nParlant: Així mateix.\n"
    marker_start = text.index("[?font]")
    piece = SpeechPiece(
        path="parla/oral/interview.md",
        piece_id="parla/oral/interview",
        title="Entrevista",
        document_type="parla",
        voice="originaria",
        epoch="contemporania",
        language_eligible=True,
        text=text,
        provenance=(SpeechProvenance("source", "fonts/source.md", "recorded", "pendent"),),
        uncertainty_spans=(UncertaintySpan(marker_start, marker_start + 7, "[?font]"),),
        eligibility="eligible",
        reason="all_eligibility_fields_and_source_recorded",
    )
    ledger = LanguageLedger((piece,), LanguageSelectionReport(1, 1, 0, 1, 0, 0, 1, {"pendent": 1}))
    candidates = build_human_conversations(ledger)

    result = filter_uncertain_conversations(ledger, candidates)

    assert len(result.accepted) == 1
    assert result.excluded == ()
    assert result.report.uncertainty_spans_discarded == 0
