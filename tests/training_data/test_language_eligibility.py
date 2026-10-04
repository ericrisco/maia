from __future__ import annotations

from pathlib import Path

from training_data.inventory import scan_tree
from training_data.language import extract_language


def _tree(root: Path) -> Path:
    docs = root / "docs"
    speech = docs / "parla/oral"
    fonts = docs / "fonts"
    speech.mkdir(parents=True)
    fonts.mkdir()
    (fonts / "speech-source.md").write_text(
        "---\ntype: font\nid: speech-source\ntitle: Font de parla\n"
        "llicencia: Creative Commons\nredistribucio: pendent\n---\n\n# Font\n",
        encoding="utf-8",
    )
    (speech / "eligible.md").write_text(
        "---\ntype: parla\ntitle: Parla autèntica\nveu: originaria\n"
        "epoca: contemporania\napte_llengua: true\nfont: speech-source\n---\n\n"
        "# Parla autèntica\n\nDiu: «Això ho fèiem així [ ?forma ]»\n",
        encoding="utf-8",
    )
    (speech / "compiled.md").write_text(
        "---\ntype: parla\ntitle: Text compilat\nveu: compilada\n"
        "epoca: contemporania\napte_llengua: false\nfont: speech-source\n---\n\n"
        "Text escrit per l'equip.\n",
        encoding="utf-8",
    )
    (speech / "historic.md").write_text(
        "---\ntype: parla\ntitle: Testimoni antic\nveu: originaria\n"
        "epoca: historica\napte_llengua: true\nfont: speech-source\n---\n\n"
        "Testimoni fora de l'època contemporània.\n",
        encoding="utf-8",
    )
    (speech / "not-approved.md").write_text(
        "---\ntype: parla\ntitle: Peça no apte\nveu: originaria\n"
        "epoca: contemporania\napte_llengua: false\nfont: speech-source\n---\n\n"
        "Peça no declarada apta per a llengua.\n",
        encoding="utf-8",
    )
    (speech / "missing-source.md").write_text(
        "---\ntype: parla\ntitle: Parla sense font\nveu: originaria\n"
        "epoca: contemporania\napte_llengua: true\nfont: absent-source\n---\n\n"
        "Text que no pot entrar encara.\n",
        encoding="utf-8",
    )
    (speech / "index.md").write_text(
        "---\ntype: index\ntitle: Índex de parla\n---\n\n# Índex\n",
        encoding="utf-8",
    )
    (speech / "broken.md").write_text("---\ntype: [bad\n---\n", encoding="utf-8")
    return docs


def test_language_selection_requires_all_three_fields_and_records_sources(
    tmp_path: Path,
) -> None:
    ledger = extract_language(scan_tree(_tree(tmp_path)))

    eligible = next(piece for piece in ledger.pieces if piece.path.endswith("eligible.md"))
    assert eligible.eligibility == "eligible"
    assert eligible.provenance[0].source_id == "speech-source"
    assert eligible.provenance[0].redistribution == "pendent"
    assert eligible.text.endswith("Diu: «Això ho fèiem així [ ?forma ]»\n")
    assert len(eligible.uncertainty_spans) == 1

    compiled = next(piece for piece in ledger.pieces if piece.path.endswith("compiled.md"))
    assert compiled.eligibility == "excluded"
    assert compiled.reason == "voice_not_original"
    historic = next(piece for piece in ledger.pieces if piece.path.endswith("historic.md"))
    assert historic.eligibility == "excluded"
    assert historic.reason == "epoch_not_contemporary"
    not_approved = next(piece for piece in ledger.pieces if piece.path.endswith("not-approved.md"))
    assert not_approved.eligibility == "excluded"
    assert not_approved.reason == "not_marked_language_eligible"

    missing = next(piece for piece in ledger.pieces if piece.path.endswith("missing-source.md"))
    assert missing.eligibility == "unresolved"
    assert missing.provenance[0].status == "missing_source_card"

    index = next(piece for piece in ledger.pieces if piece.path.endswith("index.md"))
    assert index.eligibility == "excluded"
    assert index.reason == "not_speech_piece"

    broken = next(piece for piece in ledger.pieces if piece.path.endswith("broken.md"))
    assert broken.eligibility == "unresolved"
    assert broken.reason == "markdown_error"
    assert ledger.report.eligible_pieces == 1
    assert ledger.report.excluded_pieces == 4
    assert ledger.report.unresolved_pieces == 2
    assert ledger.report.source_redistribution == {"pendent": 4}
