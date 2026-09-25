"""Tests de contracte per les etapes pures de curació."""

import json
from pathlib import Path

from cervell.model import Corpus, Doc, Font
from curacio.chunking import make_chunks, word_count
from curacio.inventory import inventory_rows, render_inventory
from curacio.metadata import (
    domain_for,
    entities_in,
    family_for,
    normalize_redistribution,
    volatility_for,
    years_in,
)
from curacio.model import Block, Chunk, CuratedDoc
from curacio.normalize import normalize_inline, normalize_prose, strip_work_sentences
from curacio.pipeline import (
    _speech_segments,
    _speech_word_count,
    apply_overrides,
    check_corpus,
    generate_corpus,
    load_overrides,
    load_review_statuses,
)
from curacio.privacy import contains_pii, load_whitelist
from curacio.segments import segment_document
from curacio.snapshot import build_manifest, doc_id_for, git_blob_sha, manifest_jsonl


def test_snapshot_uses_git_blob_hash_and_stable_manifest(tmp_path: Path) -> None:
    root = tmp_path / "docs"
    path = root / "temes" / "test.md"
    path.parent.mkdir(parents=True)
    path.write_bytes(b"---\ntype: article\n---\ntext\n")
    doc = Doc(path, {"type": "article"}, "text")
    corpus = Corpus(root, [doc], {}, [])

    records, digest = build_manifest(root, corpus)

    assert doc_id_for(root, doc) == "temes/test"
    assert records[0]["sha"] == git_blob_sha(path.read_bytes())
    assert manifest_jsonl(records, digest).endswith('"maia_sha":"' + digest + '"}\n')


def test_normalization_keeps_anchor_and_removes_work_sentence() -> None:
    assert normalize_inline("**El [Consell](./consell.md)**") == "El Consell"
    assert normalize_prose("Un *fet* amb\ncontinuació.") == "Un fet amb continuació."
    cleaned, empty, reason = strip_work_sentences(
        "El corpus ha conservat la fitxa. El fet és cert."
    )
    assert (cleaned, empty, reason) == ("El fet és cert.", False, "frase de treball eliminada")


def test_metadata_maps_closed_fields_without_losing_source_detail() -> None:
    assert normalize_redistribution("False") == ("no", "False")
    assert normalize_redistribution("sí, amb atribució") == ("pendent", "sí, amb atribució")
    assert family_for("font", {"font": "família"}) == "família"
    assert family_for("", {}) == "sense-font"
    assert domain_for("temes/historia/x") == "temes"
    assert years_in("1419 i 2024, repetit 1419") == [1419, 2024]
    assert entities_in("Consell General i Andorra") == ["Consell General"]
    assert volatility_for("Els consellers en exercici ho confirmen avui") == 0.4
    assert volatility_for("Llei 12, article 3; avui; 2024") == 1.0


def test_chunking_uses_maximum_volatility_and_300_word_boundary() -> None:
    first = Block("#b1", "cos", "Un", "", text="paraula " * 170, volatility=0.0)
    second = Block("#b2", "cos", "Dos", "", text="paraula " * 150, volatility=0.4)
    chunks = make_chunks([first, second], "doc")

    assert len(chunks) == 2
    assert word_count(chunks[0].text) == 170
    assert chunks[1].volatility == 0.4


def test_privacy_checks_direct_identifiers_and_whitelist() -> None:
    assert contains_pii("Contacte: persona@example.ad", set())
    assert contains_pii("Telèfon 123 456", set())
    assert contains_pii("NRT C-123456-Z", set())
    assert contains_pii("Carrer Major 12", set())
    assert not contains_pii("Antoni Pol", {"antoni pol"})


def test_inventory_includes_review_status_only_on_chunks() -> None:
    doc = CuratedDoc("doc", Path("doc.md"), {"title": "Títol"}, "abc", [], [], [])
    chunk = Chunk("doc#c1", "Secció", [], "text", 0.0, review_status="approved")
    doc.chunks.append(chunk)
    metadata = {"font": "f", "familia_font": "f", "llicencia": "pendent"}
    rows = inventory_rows(doc, metadata, [])

    assert rows[0][-1] == "approved"
    assert render_inventory([(doc, metadata, [])]).endswith("approved\n")


def test_review_loader_uses_only_unit_id_and_status(tmp_path: Path) -> None:
    decisions = tmp_path / "decisions.jsonl"
    decisions.write_text(
        json.dumps(
            {
                "unit_id": "maia-docs/temes/test.md",
                "status": "approved",
                "rationale": "must be ignored",
            }
        )
        + "\n"
        + json.dumps({"unit_id": "other/test.md", "status": "approved"})
        + "\n",
        encoding="utf-8",
    )

    assert load_review_statuses(decisions) == {"temes/test": "approved"}


def test_chunk_overrides_are_explicit_and_must_target_existing_chunks(tmp_path: Path) -> None:
    path = tmp_path / "overrides.tsv"
    path.write_text(
        "chunk_id\tdecision\tmotiu\ndoc#c1\tpendent\tvalidació humana\n", encoding="utf-8"
    )
    chunk = Chunk("doc#c1", "Secció", [], "text", 0.0)
    overrides = load_overrides(path)

    assert apply_overrides([chunk], overrides) == 1
    assert chunk.decision == "pendent"
    assert chunk.reason == "override manual: validació humana"


def test_speech_preserves_uncertainties_and_counts_words_without_timestamps() -> None:
    raw = "[00:00:01.000 --> 00:00:02.000] Bon dia [?senyor] Cerni.\n"

    segments, uncertain = _speech_segments(raw, "parla/test")

    assert "Bon dia senyor Cerni." in segments[0]
    assert uncertain == ["senyor"]
    assert _speech_word_count(raw) == 4


def test_segmentation_classifies_related_and_preserves_unknown_as_prose() -> None:
    blocks, gaps = segment_document(
        "## Dada\n\nText propi.\n\n## Related\n\n- [Altres](./altre.md)"
    )

    assert [(block.kind, block.section) for block in blocks] == [
        ("cos", "Dada"),
        ("related", "Related"),
    ]
    assert gaps == []


def test_font_is_available_type_is_used() -> None:
    font = Font(Path("fonts/test.md"), "test", {"redistribucio": "si"})
    assert font.redistribucio == "si"
    assert "antoni pol" in load_whitelist(
        Path("absent.tsv"), [], [Font(Path("x"), "x", {"autor": "Antoni Pol"})]
    )


def test_generation_is_deterministic_and_check_detects_manual_edits(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    source = docs / "temes" / "test.md"
    source.parent.mkdir(parents=True)
    source.write_text(
        "---\ntype: article\ntitle: Prova\ntema: temes/prova\n---\n\nText verificable.\n",
        encoding="utf-8",
    )
    output = tmp_path / "corpus"

    first = generate_corpus(docs, output)
    second = generate_corpus(docs, output)
    assert first == second
    assert check_corpus(docs, output) == []

    (output / "README.md").write_text("edita manual", encoding="utf-8")
    assert "different: README.md" in check_corpus(docs, output)
