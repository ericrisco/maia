"""Tests for the §3.3 RAG chunk and chunking (PLAN M5.01)."""

from __future__ import annotations

from itertools import pairwise

import pytest
from pydantic import ValidationError

from maia.rag.chunks import (
    CHARS_PER_TOKEN,
    DEFAULT_EMBEDDING_MODEL,
    OVERLAP_TOKENS,
    TARGET_TOKENS,
    CharacterEstimate,
    RagChunk,
    chunk_corpus,
    chunk_document,
    chunk_id,
    citable,
    render,
    restricted_share,
    split_text,
)
from maia.schemas import CorpusDocument, License, Rang, Registre, Source, compute_id

COUNTER = CharacterEstimate()


def document(
    text: str,
    *,
    licence: License = License.PUBLIC_OFFICIAL,
    legal: bool = False,
    source: Source = Source.VIQUIPEDIA,
) -> CorpusDocument:
    payload: dict[str, object] = {
        "id": compute_id(text),
        "text": text,
        "source": (Source.JURIDIC if legal else source).value,
        "url": "https://www.portaljuridicandorra.ad/llei/exemple",
        "fetched_at": "2026-07-26T10:00:00+00:00",
        "license": licence.value,
        "registre": Registre.ESTANDARD.value,
        "lang": "ca",
    }
    if legal:
        payload["legal"] = {
            "rang": Rang.ORDINARIA.value,
            "article": "5",
            "consolidacio_data": "2024-03-01",
            "llei": "Llei 9/2003 del patrimoni cultural",
        }
    return CorpusDocument.model_validate(payload)


LONG = " ".join(f"Frase número {index} del text andorrà." for index in range(400))
SHORT = "El Consell General es compon de vint-i-vuit consellers generals."


# ─────────────────────────────────────────────────────────────
# A legal article is one chunk
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_legal_document_is_never_split() -> None:
    """Splitting one would cut a citation in half."""
    chunks = chunk_document(document(LONG, legal=True))
    assert len(chunks) == 1
    assert chunks[0].text == LONG
    assert chunks[0].legal is not None
    assert chunks[0].legal.article == "5"


@pytest.mark.unit
def test_a_long_non_legal_document_is_split() -> None:
    chunks = chunk_document(document(LONG))
    assert len(chunks) > 1
    assert all(chunk.legal is None for chunk in chunks)


@pytest.mark.unit
def test_an_oversized_article_is_reported_not_mangled() -> None:
    _, report = chunk_corpus([document(LONG, legal=True)])
    assert report.legal_whole == 1
    assert len(report.oversized_legal) == 1
    rendered = render(report)
    assert "kept whole anyway" in rendered
    assert "may be truncated by the embedding model" in rendered


@pytest.mark.unit
def test_a_short_article_is_not_reported_as_oversized() -> None:
    _, report = chunk_corpus([document(SHORT, legal=True)])
    assert report.oversized_legal == []
    assert "kept whole anyway" not in render(report)


# ─────────────────────────────────────────────────────────────
# Overlapping, contiguous windows
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_short_text_is_one_chunk() -> None:
    assert split_text(SHORT, COUNTER) == [SHORT]


@pytest.mark.unit
def test_blank_text_produces_nothing() -> None:
    assert split_text("   \n ", COUNTER) == []


@pytest.mark.unit
def test_windows_are_contiguous_so_nothing_falls_between_them() -> None:
    """Overlap exists so a sentence spanning a boundary is retrievable from either side."""
    pieces = split_text(LONG, COUNTER, target=100, overlap=20)
    assert len(pieces) > 2
    for first, second in pairwise(pieces):
        # The end of one window reappears at the start of the next.
        assert first[-10:] in second or second.startswith(first[-10:])


@pytest.mark.unit
def test_every_character_of_the_source_appears_in_some_chunk() -> None:
    pieces = split_text(LONG, COUNTER, target=100, overlap=20)
    assert LONG.startswith(pieces[0][:50])
    assert pieces[-1][-50:] in LONG
    assert sum(len(piece) for piece in pieces) >= len(LONG)


@pytest.mark.unit
@pytest.mark.parametrize(("target", "overlap"), [(100, 100), (100, 200), (50, 50)])
def test_an_overlap_at_or_above_the_target_is_refused(target: int, overlap: int) -> None:
    """Equal makes no progress; larger drops the text between windows."""
    with pytest.raises(ValueError, match="not smaller than target"):
        split_text(LONG, COUNTER, target=target, overlap=overlap)


@pytest.mark.unit
def test_a_non_positive_target_is_refused() -> None:
    with pytest.raises(ValueError, match="target must be positive"):
        split_text(LONG, COUNTER, target=0)


@pytest.mark.unit
def test_a_negative_overlap_is_refused() -> None:
    with pytest.raises(ValueError, match="cannot be negative"):
        split_text(LONG, COUNTER, overlap=-1)


@pytest.mark.unit
def test_zero_overlap_is_allowed() -> None:
    assert len(split_text(LONG, COUNTER, target=100, overlap=0)) > 1


@pytest.mark.unit
def test_a_real_tokenizer_changes_the_boundaries() -> None:
    """Rather than being accepted and ignored."""

    class Verbose:
        def count(self, text: str) -> int:
            return len(text)  # one token per character

    default = split_text(LONG, COUNTER, target=100, overlap=20)
    verbose = split_text(LONG, Verbose(), target=100, overlap=20)
    assert len(verbose) > len(default)


@pytest.mark.unit
def test_the_plans_defaults_are_used() -> None:
    assert TARGET_TOKENS == 512
    assert OVERLAP_TOKENS == 64
    assert DEFAULT_EMBEDDING_MODEL == "intfloat/multilingual-e5-large"
    assert CHARS_PER_TOKEN == 4


# ─────────────────────────────────────────────────────────────
# The licence travels with the chunk
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_chunk_inherits_its_documents_licence() -> None:
    """Losing it here would make the serving decision impossible and nothing would notice."""
    chunk = chunk_document(document(SHORT, licence=License.NO_REDISTRIBUTE))[0]
    assert chunk.license is License.NO_REDISTRIBUTE
    assert chunk.restricted


@pytest.mark.unit
def test_restricted_text_may_be_quoted_privately_but_not_publicly() -> None:
    restricted = chunk_document(document(SHORT, licence=License.NO_REDISTRIBUTE))[0]
    assert citable(restricted, public=False)
    assert not citable(restricted, public=True)


@pytest.mark.unit
def test_public_text_may_be_quoted_anywhere() -> None:
    public = chunk_document(document(SHORT))[0]
    assert citable(public, public=True)
    assert citable(public, public=False)


@pytest.mark.unit
def test_a_restricted_chunk_is_still_citable_as_a_reference() -> None:
    """Withholding the reference would make answers unverifiable; quoting the text breaks D-0011."""
    restricted = chunk_document(document(SHORT, licence=License.NO_REDISTRIBUTE, legal=True))[0]
    citation = restricted.citation
    assert citation["url"].startswith("https://")
    assert citation["article"] == "5"
    assert restricted.text not in citation.values()


@pytest.mark.unit
def test_a_legal_citation_carries_the_consolidation_date() -> None:
    chunk = chunk_document(document(SHORT, legal=True))[0]
    assert chunk.citation["consolidacio_data"] == "2024-03-01"
    assert chunk.citation["llei"].startswith("Llei 9/2003")


@pytest.mark.unit
def test_a_non_legal_citation_is_just_the_url() -> None:
    assert set(chunk_document(document(SHORT))[0].citation) == {"url"}


@pytest.mark.unit
def test_the_restricted_share_of_an_index_is_reported() -> None:
    chunks = [
        *chunk_document(document(SHORT)),
        *chunk_document(document(SHORT + " Un altre.", licence=License.NO_REDISTRIBUTE)),
    ]
    assert restricted_share(chunks) == 0.5
    assert restricted_share([]) == 0.0


# ─────────────────────────────────────────────────────────────
# The schema
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_chunk_ids_are_content_addressed_and_stable() -> None:
    """So a re-index reproduces the same ids and does not duplicate the collection."""
    first = chunk_document(document(LONG))
    again = chunk_document(document(LONG))
    assert [chunk.id for chunk in first] == [chunk.id for chunk in again]
    assert len({chunk.id for chunk in first}) == len(first)


@pytest.mark.unit
def test_the_same_text_at_a_different_ordinal_is_a_different_chunk() -> None:
    assert chunk_id("a" * 64, 0, "text") != chunk_id("a" * 64, 1, "text")


@pytest.mark.unit
def test_a_chunk_records_its_position_in_the_document() -> None:
    chunks = chunk_document(document(LONG))
    assert [chunk.ordinal for chunk in chunks] == list(range(len(chunks)))


@pytest.mark.unit
def test_every_chunk_points_back_at_its_document() -> None:
    source = document(LONG)
    assert all(chunk.doc_id == source.id for chunk in chunk_document(source))


@pytest.mark.unit
def test_an_undeclared_field_is_refused() -> None:
    """A field nobody declared is a field nobody validates, and the index grounds served answers."""
    chunk = chunk_document(document(SHORT))[0]
    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        RagChunk.model_validate({**chunk.model_dump(), "score": 0.9})


@pytest.mark.unit
def test_a_chunk_is_frozen() -> None:
    chunk = chunk_document(document(SHORT))[0]
    with pytest.raises(ValidationError, match="frozen"):
        chunk.text = "edited"


@pytest.mark.unit
def test_an_empty_chunk_is_refused() -> None:
    chunk = chunk_document(document(SHORT))[0]
    with pytest.raises(ValidationError):
        RagChunk.model_validate({**chunk.model_dump(), "text": ""})


# ─────────────────────────────────────────────────────────────
# The corpus run
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_corpus_is_chunked_and_summarised() -> None:
    chunks, report = chunk_corpus(
        [document(LONG), document(SHORT, legal=True), document(SHORT + " Més.")]
    )
    assert report.documents == 3
    assert report.chunks == len(chunks)
    assert report.legal_whole == 1
    assert report.mean_chunks > 1
    assert "legal document(s) kept whole" in render(report)


@pytest.mark.unit
def test_the_report_says_the_token_counts_are_estimated() -> None:
    _, report = chunk_corpus([document(SHORT)])
    assert "ESTIMATED from characters" in render(report)


@pytest.mark.unit
def test_an_empty_corpus_produces_nothing() -> None:
    chunks, report = chunk_corpus([])
    assert chunks == []
    assert report.mean_chunks == 0.0


@pytest.mark.unit
def test_an_article_without_a_law_name_omits_it_from_the_citation() -> None:
    """Some consolidated text carries an article and rank but no title."""
    payload = document(SHORT, legal=True).model_dump()
    payload["legal"]["llei"] = None
    chunk = chunk_document(CorpusDocument.model_validate(payload))[0]
    assert "llei" not in chunk.citation
    assert chunk.citation["article"] == "5"


@pytest.mark.unit
def test_a_window_of_pure_whitespace_produces_no_chunk() -> None:
    """A document with a large blank run should not yield an empty chunk to embed."""
    text = "Text inicial. " + " " * 2_000 + "Text final."
    pieces = split_text(text, COUNTER, target=50, overlap=5)
    assert pieces
    assert all(piece.strip() for piece in pieces)


@pytest.mark.unit
def test_a_document_of_only_whitespace_is_counted_and_skipped() -> None:
    """§3.1 requires a non-empty string, which " " satisfies while holding no text."""
    blank = CorpusDocument.model_validate(
        {**document(SHORT).model_dump(), "text": "   ", "id": compute_id("   ")}
    )
    chunks, report = chunk_corpus([blank, document(SHORT)])
    assert len(chunks) == 1
    assert report.empty == [blank.id]
    assert "had no text and produced no chunk" in render(report)


@pytest.mark.unit
def test_the_loop_ends_on_the_final_window_without_overrunning() -> None:
    """The last window reaches the end of the text and stops there."""
    text = "".join(f"Frase {index}. " for index in range(60))
    pieces = split_text(text, COUNTER, target=40, overlap=10)
    assert pieces[-1].endswith(text[-5:])
