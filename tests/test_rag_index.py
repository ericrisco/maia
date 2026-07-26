"""Tests for indexing and retrieval (PLAN M5.02-M5.03)."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field

import pytest

from maia.rag.chunks import chunk_document
from maia.rag.index import (
    DEFAULT_COLLECTION,
    DEFAULT_TOP_K,
    PASSAGE_PREFIX,
    QUERY_PREFIX,
    Hit,
    PrefixError,
    ReindexPlan,
    apply_reindex,
    check_prefixes,
    citable_hit,
    context_block,
    index_chunks,
    missing_obligations,
    passage_text,
    plan_reindex,
    query_text,
    render_index,
    render_reindex,
    retrieve,
    system_prompt,
    to_hit,
    to_point,
)
from maia.schemas import CorpusDocument, License, Rang, Registre, Source, compute_id

TEXT = "El comú de la parròquia gestiona el territori i els serveis de proximitat."
RESTRICTED_TEXT = "Transcripció de ràdio que no es pot redistribuir."


def document(
    text: str = TEXT, *, licence: License = License.PUBLIC_OFFICIAL, legal: bool = False
) -> CorpusDocument:
    payload: dict[str, object] = {
        "id": compute_id(text),
        "text": text,
        "source": (Source.JURIDIC if legal else Source.VIQUIPEDIA).value,
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
            "llei": "Llei 9/2003",
        }
    return CorpusDocument.model_validate(payload)


def chunk(text: str = TEXT, **kwargs: object) -> object:
    return chunk_document(document(text, **kwargs))[0]  # type: ignore[arg-type]


@dataclass
class FakeEmbedder:
    dimensions: int = 8
    seen: list[str] = field(default_factory=list)
    short: bool = False

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        self.seen.extend(texts)
        vectors = [[float(len(text) % 7), *([0.1] * (self.dimensions - 1))] for text in texts]
        return vectors[:-1] if self.short and vectors else vectors


@dataclass
class FakeStore:
    upserted: list[Mapping[str, object]] = field(default_factory=list)
    deleted: list[str] = field(default_factory=list)
    results: list[Mapping[str, object]] = field(default_factory=list)
    searches: list[tuple[str, int]] = field(default_factory=list)

    def upsert(self, collection: str, points: Sequence[Mapping[str, object]]) -> None:
        self.upserted.extend(points)

    def delete(self, collection: str, ids: Sequence[str]) -> None:
        self.deleted.extend(ids)

    def search(
        self, collection: str, vector: Sequence[float], *, limit: int
    ) -> list[Mapping[str, object]]:
        self.searches.append((collection, limit))
        return self.results[:limit]


def point(
    *, text: str = TEXT, licence: str = "public-official", legal: bool = False, score: float = 0.9
) -> dict[str, object]:
    payload: dict[str, object] = {
        "text": text,
        "url": "https://www.portaljuridicandorra.ad/llei/exemple",
        "license": licence,
    }
    if legal:
        payload["legal"] = {
            "article": "5",
            "consolidacio_data": "2024-03-01",
            "llei": "Llei 9/2003",
        }
    return {"id": "a" * 64, "score": score, "payload": payload}


# ─────────────────────────────────────────────────────────────
# E5 prefixes — the silent failure
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_question_is_prefixed_as_a_query() -> None:
    assert query_text("Què fa el comú?") == f"{QUERY_PREFIX}Què fa el comú?"


@pytest.mark.unit
def test_a_chunk_is_prefixed_as_a_passage() -> None:
    assert passage_text(chunk()).startswith(PASSAGE_PREFIX)  # type: ignore[arg-type]


@pytest.mark.unit
def test_the_wrong_prefix_is_caught_rather_than_producing_a_bad_index() -> None:
    """The failure it catches produces a working index that retrieves badly."""
    with pytest.raises(PrefixError, match="degrades retrieval with no error"):
        check_prefixes([query_text("Q?")], expect=PASSAGE_PREFIX)


@pytest.mark.unit
def test_the_right_prefix_passes() -> None:
    check_prefixes([passage_text(chunk())], expect=PASSAGE_PREFIX)  # type: ignore[arg-type]
    check_prefixes([query_text("Q?")], expect=QUERY_PREFIX)


@pytest.mark.unit
def test_indexing_embeds_passages_and_retrieval_embeds_a_query() -> None:
    embedder, store = FakeEmbedder(), FakeStore()
    index_chunks([chunk()], embedder, store)  # type: ignore[list-item]
    assert all(text.startswith(PASSAGE_PREFIX) for text in embedder.seen)

    embedder.seen.clear()
    store.results = [point()]
    retrieve("Què fa el comú?", embedder, store)
    assert embedder.seen == [f"{QUERY_PREFIX}Què fa el comú?"]


# ─────────────────────────────────────────────────────────────
# Indexing
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_point_carries_the_licence_into_the_payload() -> None:
    """So the serving layer decides what to quote without a second lookup."""
    written = to_point(chunk(RESTRICTED_TEXT, licence=License.NO_REDISTRIBUTE), [0.1, 0.2])  # type: ignore[arg-type]
    payload = written["payload"]
    assert isinstance(payload, dict)
    assert payload["license"] == "no-redistribute"
    assert payload["url"].startswith("https://")


@pytest.mark.unit
def test_a_legal_point_carries_its_article() -> None:
    written = to_point(chunk(legal=True), [0.1])  # type: ignore[arg-type]
    payload = written["payload"]
    assert isinstance(payload, dict)
    assert payload["legal"]["article"] == "5"


@pytest.mark.unit
def test_indexing_reports_what_it_wrote_and_how_much_is_restricted() -> None:
    store = FakeStore()
    report = index_chunks(
        [chunk(), chunk(RESTRICTED_TEXT, licence=License.NO_REDISTRIBUTE)],  # type: ignore[list-item]
        FakeEmbedder(),
        store,
    )
    assert report.chunks == 2
    assert report.restricted == 1
    assert report.restricted_share == 0.5
    assert len(store.upserted) == 2
    rendered = render_index(report)
    assert "retrievable and citable" in rendered
    assert "withheld from public answers" in rendered


@pytest.mark.unit
def test_a_clean_index_says_nothing_about_restrictions() -> None:
    assert "restricted" not in render_index(index_chunks([chunk()], FakeEmbedder(), FakeStore()))  # type: ignore[list-item]


@pytest.mark.unit
def test_a_chunk_built_for_another_model_is_refused() -> None:
    """A mixed-model collection returns neighbours from two incompatible spaces."""
    other = chunk_document(document(), embedding_model="other/model")[0]
    with pytest.raises(ValueError, match="incompatible spaces"):
        index_chunks([other], FakeEmbedder(), FakeStore())


@pytest.mark.unit
def test_an_embedder_returning_too_few_vectors_is_refused() -> None:
    with pytest.raises(ValueError, match="may not be theirs"):
        index_chunks(
            [chunk(), chunk(TEXT + " Més.")],  # type: ignore[list-item]
            FakeEmbedder(short=True),
            FakeStore(),
        )


@pytest.mark.unit
def test_indexing_happens_in_batches() -> None:
    store = FakeStore()
    chunks = [chunk(f"{TEXT} variant {index}.") for index in range(5)]
    report = index_chunks(chunks, FakeEmbedder(), store, batch_size=2)  # type: ignore[arg-type]
    assert report.batches == 3
    assert len(store.upserted) == 5


@pytest.mark.unit
@pytest.mark.parametrize("size", [0, -1])
def test_a_non_positive_batch_size_is_refused(size: int) -> None:
    with pytest.raises(ValueError, match="batch_size must be positive"):
        index_chunks([chunk()], FakeEmbedder(), FakeStore(), batch_size=size)  # type: ignore[list-item]


# ─────────────────────────────────────────────────────────────
# Retrieval
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_retrieval_returns_hits_with_their_citations() -> None:
    store = FakeStore(results=[point(legal=True)])
    hits = retrieve("Què diu l'article 5?", FakeEmbedder(), store)
    assert len(hits) == 1
    assert hits[0].citation == {
        "url": "https://www.portaljuridicandorra.ad/llei/exemple",
        "article": "5",
        "consolidacio_data": "2024-03-01",
        "llei": "Llei 9/2003",
    }
    assert store.searches == [(DEFAULT_COLLECTION, DEFAULT_TOP_K)]


@pytest.mark.unit
def test_a_hit_without_attribution_is_refused() -> None:
    """Silently dropping the attribution is how an unsourced answer gets served as a sourced one."""
    with pytest.raises(ValueError, match="cannot be served as a sourced answer"):
        to_hit({"id": "x", "payload": {"text": TEXT, "license": "public-official"}})


@pytest.mark.unit
def test_a_result_without_a_payload_is_refused() -> None:
    with pytest.raises(ValueError, match="has no payload"):
        to_hit({"id": "x"})


@pytest.mark.unit
def test_a_missing_score_reads_as_zero_rather_than_crashing() -> None:
    assert to_hit({"id": "x", "payload": point()["payload"]}).score == 0.0


@pytest.mark.unit
@pytest.mark.parametrize("question", ["", "   "])
def test_an_empty_question_is_refused(question: str) -> None:
    with pytest.raises(ValueError, match="retrieves nothing meaningful"):
        retrieve(question, FakeEmbedder(), FakeStore())


@pytest.mark.unit
@pytest.mark.parametrize("top_k", [0, -3])
def test_a_non_positive_top_k_is_refused(top_k: int) -> None:
    with pytest.raises(ValueError, match="top_k must be positive"):
        retrieve("Q?", FakeEmbedder(), FakeStore(), top_k=top_k)


@pytest.mark.unit
def test_an_embedder_returning_the_wrong_count_for_a_question_is_refused() -> None:
    with pytest.raises(ValueError, match="vectors for one question"):
        retrieve("Q?", FakeEmbedder(short=True), FakeStore())


# ─────────────────────────────────────────────────────────────
# The system prompt
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_prompt_states_all_three_obligations() -> None:
    assert missing_obligations(system_prompt()) == []


@pytest.mark.unit
def test_a_prompt_missing_the_no_ho_se_instruction_is_caught() -> None:
    """The obligation M2's whole no_ho_se type trained for."""
    assert "unknown" in missing_obligations("Ets MAIA. Cita les fonts.")


@pytest.mark.unit
def test_a_prompt_missing_identity_or_citation_is_caught() -> None:
    assert "identity" in missing_obligations("Cita les fonts. Si no ho saps, digues-ho.")
    assert "cite" in missing_obligations("Ets MAIA. Si no consta, digues-ho.")


@pytest.mark.unit
def test_extra_instructions_are_appended_not_substituted() -> None:
    prompt = system_prompt(extra="Respon sempre amb brevetat.")
    assert missing_obligations(prompt) == []
    assert "brevetat" in prompt


@pytest.mark.unit
def test_blank_extra_instructions_are_ignored() -> None:
    assert system_prompt(extra="   ") == system_prompt()


# ─────────────────────────────────────────────────────────────
# Restricted text in the served context
# ─────────────────────────────────────────────────────────────


def hit(*, licence: str = "public-official", text: str = TEXT) -> Hit:
    return to_hit(point(text=text, licence=licence, legal=True))


@pytest.mark.unit
def test_public_passages_are_quoted_in_full() -> None:
    block = context_block([hit()], public=True)
    assert TEXT in block
    assert "article=5" in block


@pytest.mark.unit
def test_a_restricted_passage_is_cited_without_its_text() -> None:
    """The model can say "segons l'article 5..." without the transcript holding restricted text."""
    block = context_block([hit(licence="no-redistribute", text=RESTRICTED_TEXT)], public=True)
    assert RESTRICTED_TEXT not in block
    assert "article=5" in block
    assert "llicència restringida" in block


@pytest.mark.unit
def test_a_restricted_passage_is_quoted_in_a_private_context() -> None:
    block = context_block([hit(licence="no-redistribute", text=RESTRICTED_TEXT)], public=False)
    assert RESTRICTED_TEXT in block


@pytest.mark.unit
def test_the_restricted_passage_is_kept_rather_than_dropped() -> None:
    """Dropping it would make the model answer "no ho sé" about something the corpus knows."""
    block = context_block(
        [hit(licence="no-redistribute", text=RESTRICTED_TEXT), hit()], public=True
    )
    assert "[1]" in block and "[2]" in block


@pytest.mark.unit
def test_no_passages_says_so_explicitly() -> None:
    assert context_block([]) == "(cap passatge recuperat)"


@pytest.mark.unit
def test_the_citable_rule_matches_the_chunk_level_one() -> None:
    assert citable_hit(hit(), public=True)
    assert not citable_hit(hit(licence="no-redistribute"), public=True)
    assert citable_hit(hit(licence="no-redistribute"), public=False)


# ─────────────────────────────────────────────────────────────
# The quarterly reindex
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_an_unchanged_corpus_needs_no_work() -> None:
    current = chunk_document(document())
    indexed = {current[0].id: current[0].doc_id}
    plan = plan_reindex(current, indexed)
    assert plan.touched == 0
    assert plan.unchanged == 1
    assert "already matches the corpus" in render_reindex(plan)


@pytest.mark.unit
def test_a_new_document_is_added() -> None:
    current = chunk_document(document("Un text completament nou del corpus andorrà."))
    plan = plan_reindex(current, {})
    assert plan.added == [current[0].id]
    assert plan.deleted == []


@pytest.mark.unit
def test_a_changed_article_supersedes_its_old_chunk() -> None:
    """Ids are content-addressed, so changed text is a new id and the old one has to go."""
    old = chunk_document(document("Article 5 en la seva redacció antiga i derogada."))[0]
    new = chunk_document(document("Article 5 en la seva redacció antiga i derogada, modificada."))[
        0
    ]
    plan = plan_reindex([new], {old.id: new.doc_id})
    assert plan.added == [new.id]
    assert plan.replaced == [old.id]
    assert "superseded articles answering as current law" in render_reindex(plan)


@pytest.mark.unit
def test_a_removed_document_is_deleted() -> None:
    current = chunk_document(document())
    plan = plan_reindex(current, {current[0].id: current[0].doc_id, "b" * 64: "c" * 64})
    assert plan.deleted == ["b" * 64]
    assert plan.replaced == []


@pytest.mark.unit
def test_an_add_only_refresh_would_leave_stale_law_and_the_plan_says_so() -> None:
    old = chunk_document(document("Redacció antiga de l'article cinquè de la llei."))[0]
    new = chunk_document(document("Redacció nova de l'article cinquè de la llei."))[0]
    plan = plan_reindex([new], {old.id: new.doc_id})
    assert plan.replaced, "the superseded chunk must be identified, not just the new one added"


@pytest.mark.unit
def test_applying_a_reindex_writes_before_it_deletes() -> None:
    """An interrupted reindex should leave both versions, not neither."""

    @dataclass
    class OrderedStore(FakeStore):
        order: list[str] = field(default_factory=list)

        def upsert(self, collection: str, points: Sequence[Mapping[str, object]]) -> None:
            self.order.append("upsert")
            super().upsert(collection, points)

        def delete(self, collection: str, ids: Sequence[str]) -> None:
            self.order.append("delete")
            super().delete(collection, ids)

    old = chunk_document(document("Redacció antiga de l'article cinquè."))[0]
    new = chunk_document(document("Redacció nova de l'article cinquè."))[0]
    plan = plan_reindex([new], {old.id: new.doc_id})
    store = OrderedStore()
    apply_reindex(plan, [new], FakeEmbedder(), store)
    assert store.order == ["upsert", "delete"]
    assert store.deleted == [old.id]


@pytest.mark.unit
def test_a_reindex_with_nothing_to_delete_touches_no_deletions() -> None:
    new = chunk_document(document("Un text nou per al corpus."))[0]
    store = FakeStore()
    apply_reindex(plan_reindex([new], {}), [new], FakeEmbedder(), store)
    assert store.deleted == []
    assert len(store.upserted) == 1


@pytest.mark.unit
def test_an_empty_plan_has_nothing_to_touch() -> None:
    assert ReindexPlan().touched == 0


@pytest.mark.unit
def test_a_legal_hit_missing_a_field_omits_it_from_the_citation() -> None:
    """Consolidated text without a law title still cites its article and date."""
    partial = to_hit(
        {
            "id": "a" * 64,
            "score": 0.5,
            "payload": {
                "text": TEXT,
                "url": "https://www.portaljuridicandorra.ad/x",
                "license": "public-official",
                "legal": {"article": "5", "consolidacio_data": "2024-03-01", "llei": None},
            },
        }
    )
    assert set(partial.citation) == {"url", "article", "consolidacio_data"}


@pytest.mark.unit
def test_a_non_legal_hit_cites_only_its_url() -> None:
    assert set(to_hit(point()).citation) == {"url"}
