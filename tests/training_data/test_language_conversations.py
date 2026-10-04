from __future__ import annotations

from training_data.language import (
    LanguageLedger,
    LanguageSelectionReport,
    SpeechPiece,
    SpeechProvenance,
)
from training_data.language_conversations import build_human_conversations


def _piece(path: str, text: str) -> SpeechPiece:
    return SpeechPiece(
        path=path,
        piece_id=path.removesuffix(".md"),
        title="Testimoni",
        document_type="parla",
        voice="originaria",
        epoch="contemporania",
        language_eligible=True,
        text=text,
        provenance=(SpeechProvenance("source", "fonts/source.md", "recorded", "pendent"),),
        uncertainty_spans=(),
        eligibility="eligible",
        reason="all_eligibility_fields_and_source_recorded",
    )


def test_only_explicit_human_interviewer_and_speaker_turns_become_chat() -> None:
    transcript = (
        "## La transcripció\n\n"
        "Entrevistador: I això com ho fèieu abans?\n"
        "Parlant: Ho fèiem així, de tota la vida.\n"
        "Entrevistador: I quan hi anàveu?\n"
        "Parlant: Hi anàvem cada dissabte.\n"
    )
    ledger = LanguageLedger((_piece("parla/oral/interview.md", transcript),), _report())

    conversations = build_human_conversations(ledger)

    assert len(conversations) == 2
    first = conversations[0]
    assert first.user == "I això com ho fèieu abans?"
    assert first.assistant == "Ho fèiem així, de tota la vida."
    assert first.source_path == "parla/oral/interview.md"
    assert first.user == transcript[first.user_start : first.user_end]
    assert first.assistant == transcript[first.assistant_start : first.assistant_end]
    assert first.to_public_record() == {
        "messages": [
            {"role": "user", "content": first.user},
            {"role": "assistant", "content": first.assistant},
        ]
    }


def test_monologue_rhetorical_questions_are_not_relabelled_as_user_turns() -> None:
    ledger = LanguageLedger(
        (_piece("parla/oral/monologue.md", "[00:00:01] I per què? Doncs perquè ho fèiem així.\n"),),
        _report(),
    )

    assert build_human_conversations(ledger) == ()


def _report() -> LanguageSelectionReport:
    return LanguageSelectionReport(1, 1, 0, 1, 0, 0, 0, {"pendent": 1})
