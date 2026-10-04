from __future__ import annotations

from pathlib import Path

import pytest

from training_data.inventory import scan_tree
from training_data.language import (
    AuthenticSpeechSegment,
    LanguageLedger,
    build_authentic_speech_segments,
    extract_language,
    validate_authentic_speech_segments,
)


def _ledger(root: Path) -> LanguageLedger:
    docs = root / "docs"
    speech = docs / "parla/oral"
    fonts = docs / "fonts"
    speech.mkdir(parents=True)
    fonts.mkdir()
    (fonts / "source.md").write_text(
        "---\ntype: font\nid: source\ntitle: Font\n---\n\n# Font\n", encoding="utf-8"
    )
    (speech / "piece.md").write_text(
        "---\ntype: parla\ntitle: Testimoni\nveu: originaria\n"
        "epoca: contemporania\napte_llengua: true\nfont: source\n---\n\n"
        "## Conversa\n\n— Ho fèiem així, de tota la vida.\n",
        encoding="utf-8",
    )
    return extract_language(scan_tree(docs))


def test_segments_are_verbatim_spans_from_eligible_source_pieces(tmp_path: Path) -> None:
    ledger = _ledger(tmp_path)

    segments = build_authentic_speech_segments(ledger)

    assert len(segments) == 1
    segment = segments[0]
    piece = next(piece for piece in ledger.pieces if piece.path == segment.source_path)
    assert piece.eligibility == "eligible"
    assert segment.text == piece.text[segment.source_start : segment.source_end]
    assert "Ho fèiem així" in segment.text
    assert "assistant" not in segment.text
    validate_authentic_speech_segments(ledger, segments)


def test_validator_rejects_generated_or_rewritten_speech(tmp_path: Path) -> None:
    ledger = _ledger(tmp_path)
    original = build_authentic_speech_segments(ledger)[0]
    generated = AuthenticSpeechSegment(
        segment_id=original.segment_id,
        source_path=original.source_path,
        piece_id=original.piece_id,
        source_start=original.source_start,
        source_end=original.source_end,
        text="Una resposta inventada i parafrasejada.",
    )

    with pytest.raises(ValueError, match="does not match source span"):
        validate_authentic_speech_segments(ledger, (generated,))
