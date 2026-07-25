"""Tests for the semantic near-duplicate filter (PLAN M2.05, filter 1)."""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass, field
from uuid import uuid4

import pytest

from maia.schemas import DatasetExample, ExampleType, Split, compute_id
from maia.synth.semdedup import (
    DEFAULT_SIMHASH,
    SemanticDedupReport,
    SemanticIndex,
    SimHashConfig,
    Vector,
    cosine,
    deduplicate,
    dot,
    ollama_embedder,
    parse_embeddings,
    random_planes,
    render,
    share_by_type,
    sign_bits,
    survivor_rank,
    text_of,
)

GROUNDING = compute_id("El Consell General es compon de 28 consellers generals.")


def example(
    prompt: str,
    response: str = "Vint-i-vuit consellers generals.",
    *,
    split: Split = Split.TRAIN,
    kind: ExampleType = ExampleType.QA,
    score: float = 0.9,
) -> DatasetExample:
    return DatasetExample.model_validate(
        {
            "id": str(uuid4()),
            "messages": [
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": response},
            ],
            "type": kind.value,
            "topic": "institucions/consell-general",
            "grounding_ids": [] if kind is ExampleType.GENERAL_CA else [GROUNDING],
            "generator": "claude-opus-5",
            "judge_score": score,
            "split": split.value,
        }
    )


@dataclass
class WordEmbedder:
    """A deterministic bag-of-words embedder — the injected seam, no network.

    Near-identical questions land at a near-zero angle because they share almost every word, which
    is exactly the geometry the real embedder produces and the LSH scheme depends on.
    """

    vocabulary: dict[str, int] = field(default_factory=dict)
    dimensions: int = 32
    calls: int = 0
    batches: list[int] = field(default_factory=list)

    def embed(self, texts: Sequence[str]) -> list[Vector]:
        self.calls += 1
        self.batches.append(len(texts))
        vectors: list[Vector] = []
        for text in texts:
            vector = [0.0] * self.dimensions
            for word in text.lower().split():
                slot = self.vocabulary.setdefault(word, len(self.vocabulary) % self.dimensions)
                vector[slot] += 1.0
            vectors.append(vector)
        return vectors


# ─────────────────────────────────────────────────────────────
# Geometry
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_cosine_of_identical_and_orthogonal_vectors() -> None:
    assert cosine([1.0, 0.0], [2.0, 0.0]) == pytest.approx(1.0)
    assert cosine([1.0, 0.0], [0.0, 1.0]) == pytest.approx(0.0)
    assert cosine([1.0, 0.0], [-1.0, 0.0]) == pytest.approx(-1.0)


@pytest.mark.unit
def test_a_zero_vector_is_similar_to_nothing() -> None:
    """Not to everything — that would collapse the dataset into one cluster."""
    assert cosine([0.0, 0.0], [1.0, 1.0]) == 0.0
    assert cosine([0.0, 0.0], [0.0, 0.0]) == 0.0


@pytest.mark.unit
def test_mismatched_dimensions_are_refused() -> None:
    with pytest.raises(ValueError, match="dimension mismatch: 2 vs 3"):
        dot([1.0, 2.0], [1.0, 2.0, 3.0])


@pytest.mark.unit
def test_planes_are_reproducible_from_the_seed_and_differ_between_seeds() -> None:
    config = SimHashConfig(bands=2, rows=2, seed=7)
    assert random_planes(4, config) == random_planes(4, config)
    assert random_planes(4, config) != random_planes(4, SimHashConfig(bands=2, rows=2, seed=8))


@pytest.mark.unit
def test_the_number_of_planes_is_bands_times_rows() -> None:
    config = SimHashConfig(bands=3, rows=5)
    assert config.bits == 15
    assert len(random_planes(8, config)) == 15


@pytest.mark.unit
@pytest.mark.parametrize("dimensions", [0, -1])
def test_planes_need_a_positive_dimension(dimensions: int) -> None:
    with pytest.raises(ValueError, match="dimensions must be positive"):
        random_planes(dimensions)


@pytest.mark.unit
def test_similar_vectors_agree_on_more_sign_bits_than_dissimilar_ones() -> None:
    """The property the whole scheme rests on: bit agreement tracks the angle."""
    planes = random_planes(16, DEFAULT_SIMHASH)
    base = [math.sin(index) for index in range(16)]
    near = [value + 0.01 for value in base]
    far = [math.cos(index * 3) for index in range(16)]
    agree_near = sum(
        a == b for a, b in zip(sign_bits(base, planes), sign_bits(near, planes), strict=True)
    )
    agree_far = sum(
        a == b for a, b in zip(sign_bits(base, planes), sign_bits(far, planes), strict=True)
    )
    assert agree_near > agree_far


# ─────────────────────────────────────────────────────────────
# The index
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_near_identical_vectors_cluster_and_distant_ones_do_not() -> None:
    index = SemanticIndex(threshold=0.99)
    base = [1.0, 2.0, 3.0, 4.0]
    index.add("a", base)
    index.add("b", [1.01, 2.0, 3.0, 4.0])
    index.add("c", [-4.0, 3.0, -2.0, 1.0])
    assert index.clusters() == [["a", "b"]]


@pytest.mark.unit
def test_clusters_are_transitive() -> None:
    index = SemanticIndex(threshold=0.999)
    index.add("a", [1.0, 0.0, 0.0])
    index.add("b", [1.0, 0.01, 0.0])
    index.add("c", [1.0, 0.02, 0.0])
    assert index.clusters() == [["a", "b", "c"]]


@pytest.mark.unit
def test_a_repeated_key_is_refused() -> None:
    index = SemanticIndex()
    index.add("a", [1.0])
    with pytest.raises(ValueError, match="key already indexed"):
        index.add("a", [1.0])


@pytest.mark.unit
def test_an_empty_embedding_is_refused() -> None:
    with pytest.raises(ValueError, match="empty embedding"):
        SemanticIndex().add("a", [])


@pytest.mark.unit
def test_a_dimension_change_mid_run_is_refused() -> None:
    """A silent mismatch would make every similarity meaningless."""
    index = SemanticIndex()
    index.add("a", [1.0, 2.0])
    with pytest.raises(ValueError, match="has 3 dimensions, expected 2"):
        index.add("b", [1.0, 2.0, 3.0])


@pytest.mark.unit
def test_candidate_pairs_are_unique_and_ordered_by_insertion() -> None:
    index = SemanticIndex(threshold=0.99)
    for key in ("a", "b", "c"):
        index.add(key, [1.0, 1.0, 1.0, 1.0])
    pairs = index.candidate_pairs()
    assert pairs == [("a", "b"), ("a", "c"), ("b", "c")]
    assert len(pairs) == len(set(pairs))


@pytest.mark.unit
def test_nothing_indexed_means_no_clusters() -> None:
    assert SemanticIndex().clusters() == []


@pytest.mark.unit
def test_lsh_bucketing_is_a_filter_not_the_verdict() -> None:
    """Sharing a band makes a pair a candidate; only cosine decides.

    With one band of one bit, half the vectors collide by construction. If bucketing decided, this
    would cluster unrelated examples.
    """
    index = SemanticIndex(threshold=0.99, config=SimHashConfig(bands=1, rows=1, seed=3))
    index.add("a", [1.0, 0.0])
    index.add("b", [0.0, 1.0])
    assert index.candidate_pairs() in ([("a", "b")], [])
    assert index.clusters() == []


# ─────────────────────────────────────────────────────────────
# Which copy survives — the anti-contamination rule
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_test_split_outranks_val_and_train() -> None:
    ranks = [
        survivor_rank(example("Q", split=split))[0]
        for split in (Split.TRAIN, Split.VAL, Split.TEST)
    ]
    assert ranks == sorted(ranks)
    assert ranks[2] > ranks[1] > ranks[0]


@pytest.mark.unit
def test_the_held_out_copy_survives_a_cross_split_duplicate() -> None:
    """A near-duplicate across splits is benchmark contamination, not redundancy.

    Keeping the train copy would leave the model evaluated on something it trained on, so the
    trainable copy is the one that dies — even though here it has the better score and more text.
    """
    train = example("Quants consellers té el Consell General?", score=1.0)
    held = example("Quants consellers te el Consell General?", response="28.", score=0.1)
    held = held.model_copy(update={"split": Split.TEST})
    survivors, report = deduplicate([train, held], WordEmbedder(), threshold=0.5)
    assert [item.id for item in survivors] == [held.id]
    assert report.cross_split == 1
    assert "BENCHMARK CONTAMINATION" in render(report)


@pytest.mark.unit
def test_within_one_split_the_better_judged_example_survives() -> None:
    weak = example("Quants consellers hi ha al Consell General?", score=0.5)
    strong = example("Quants consellers hi ha al Consell General?", score=0.95)
    survivors, report = deduplicate([weak, strong], WordEmbedder(), threshold=0.9)
    assert [item.id for item in survivors] == [strong.id]
    assert report.cross_split == 0


@pytest.mark.unit
def test_at_equal_score_the_longer_example_survives() -> None:
    short = example("Quants consellers hi ha?", response="28.")
    long = example("Quants consellers hi ha?", response="Vint-i-vuit consellers generals, elegits.")
    survivors, _ = deduplicate([short, long], WordEmbedder(), threshold=0.5)
    assert [item.id for item in survivors] == [long.id]


@pytest.mark.unit
def test_the_rank_is_split_then_score_then_length_then_id() -> None:
    ranked = survivor_rank(example("Q", split=Split.VAL, score=0.5))
    assert ranked[0] == 1
    assert ranked[1] == 0.5
    assert ranked[2] == len(text_of(example("Q", split=Split.VAL, score=0.5)))
    assert isinstance(ranked[3], str)


# ─────────────────────────────────────────────────────────────
# The pipeline stage
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_distinct_examples_all_survive() -> None:
    examples = [
        example("Quantes parròquies té Andorra?", "Set."),
        example("Qui és el síndic general?", "Presideix el Consell General."),
        example("Què és la Batllia?", "El tribunal de primera instància."),
    ]
    survivors, report = deduplicate(examples, WordEmbedder())
    assert len(survivors) == 3
    assert report.dropped == 0
    assert report.clusters == 0
    assert report.kept == 3
    assert "3/3 kept" in render(report)


@pytest.mark.unit
def test_an_empty_dataset_needs_no_embedder_call() -> None:
    embedder = WordEmbedder()
    survivors, report = deduplicate([], embedder)
    assert survivors == []
    assert report.examined == 0
    assert embedder.calls == 0


@pytest.mark.unit
def test_embedding_happens_in_batches() -> None:
    """Embedding APIs are priced and rate-limited per call."""
    embedder = WordEmbedder()
    deduplicate([example(f"Pregunta {index}") for index in range(10)], embedder, batch_size=4)
    assert embedder.batches == [4, 4, 2]


@pytest.mark.unit
def test_an_embedder_returning_the_wrong_count_is_refused() -> None:
    """Silently zipping short would pair examples with embeddings that are not theirs."""

    @dataclass
    class Truncating:
        def embed(self, texts: Sequence[str]) -> list[Vector]:
            return [[1.0, 2.0]] * (len(texts) - 1)

    with pytest.raises(ValueError, match="returned 1 vectors for 2 texts"):
        deduplicate([example("A"), example("B")], Truncating())


@pytest.mark.unit
@pytest.mark.parametrize("size", [0, -3])
def test_a_non_positive_batch_size_is_refused(size: int) -> None:
    with pytest.raises(ValueError, match="batch_size must be positive"):
        deduplicate([example("A")], WordEmbedder(), batch_size=size)


@pytest.mark.unit
def test_the_report_counts_every_embedded_example() -> None:
    _, report = deduplicate([example(f"Q{index}") for index in range(5)], WordEmbedder())
    assert report.embedded == 5
    assert report.examined == 5


@pytest.mark.unit
def test_deduped_text_covers_both_roles() -> None:
    text = text_of(example("La pregunta", "La resposta"))
    assert "La pregunta" in text and "La resposta" in text


# ─────────────────────────────────────────────────────────────
# Reporting
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_type_shares_sum_to_one() -> None:
    shares = share_by_type(
        [
            example("A", kind=ExampleType.QA),
            example("B", kind=ExampleType.QA),
            example("C", kind=ExampleType.GENERAL_CA),
        ]
    )
    assert shares[ExampleType.QA] == pytest.approx(2 / 3)
    assert shares[ExampleType.GENERAL_CA] == pytest.approx(1 / 3)
    assert sum(shares.values()) == pytest.approx(1.0)


@pytest.mark.unit
def test_type_shares_of_nothing_are_empty() -> None:
    assert share_by_type([]) == {}


@pytest.mark.unit
def test_a_clean_report_says_nothing_about_contamination() -> None:
    assert "CONTAMINATION" not in render(SemanticDedupReport(examined=3))


@pytest.mark.unit
def test_the_report_lists_at_most_five_contaminated_pairs() -> None:
    report = SemanticDedupReport(
        examined=20, cross_split=7, cross_split_examples=[(f"a{i}", f"b{i}") for i in range(7)]
    )
    assert render(report).count(" ~ ") == 5


# ─────────────────────────────────────────────────────────────
# The live embedder's response shape
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_an_embeddings_response_is_parsed() -> None:
    assert parse_embeddings({"embeddings": [[1.0, 2], [3, 4.5]]}, 2) == [[1.0, 2.0], [3.0, 4.5]]


@pytest.mark.unit
@pytest.mark.parametrize(
    ("payload", "expected", "message"),
    [
        ({"error": "model not found"}, 1, "expected an 'embeddings' list"),
        ("not json", 1, "expected an 'embeddings' list"),
        ({"embeddings": [[1.0]]}, 2, "got 1 embeddings for 2 texts"),
        ({"embeddings": ["nope"]}, 1, "embedding 0 is not a list of numbers"),
        ({"embeddings": [[True]]}, 1, "embedding 0 is not a list of numbers"),
    ],
)
def test_a_bad_embeddings_response_is_refused(payload: object, expected: int, message: str) -> None:
    """An error body returned as HTTP 200 must not read as a batch of embeddings."""
    with pytest.raises(ValueError, match=message):
        parse_embeddings(payload, expected)


# ─────────────────────────────────────────────────────────────
# The live wiring — blocked-by-resource, so the transport is faked, not the logic
# ─────────────────────────────────────────────────────────────


@dataclass
class FakeResponse:
    """Enough of a ``requests.Response`` for the embedder."""

    payload: object
    status: int = 200

    def raise_for_status(self) -> None:
        if self.status >= 400:
            raise RuntimeError(f"HTTP {self.status}")

    def json(self) -> object:
        return self.payload


@pytest.mark.unit
def test_the_live_embedder_posts_the_batch_and_parses_the_reply(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sent: dict[str, object] = {}

    def fake_post(url: str, **kwargs: object) -> FakeResponse:
        sent["url"] = url
        sent.update(kwargs)
        return FakeResponse({"embeddings": [[1.0, 0.0], [0.0, 1.0]]})

    monkeypatch.setattr("requests.post", fake_post)
    embedder = ollama_embedder("http://localhost:11434/api/embed", model="jina/test")
    assert embedder.embed(["un", "dos"]) == [[1.0, 0.0], [0.0, 1.0]]
    assert sent["url"] == "http://localhost:11434/api/embed"
    assert sent["json"] == {"model": "jina/test", "input": ["un", "dos"]}


@pytest.mark.unit
def test_the_live_embedder_raises_on_an_http_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("requests.post", lambda url, **kwargs: FakeResponse({}, status=503))
    with pytest.raises(RuntimeError, match="HTTP 503"):
        ollama_embedder().embed(["un"])


@pytest.mark.unit
def test_the_live_embedder_refuses_a_short_reply(monkeypatch: pytest.MonkeyPatch) -> None:
    """The count check lives in the transport too, where the mismatch first becomes visible."""
    monkeypatch.setattr(
        "requests.post", lambda url, **kwargs: FakeResponse({"embeddings": [[1.0]]})
    )
    with pytest.raises(ValueError, match="got 1 embeddings for 2 texts"):
        ollama_embedder().embed(["un", "dos"])
