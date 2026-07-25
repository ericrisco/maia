"""Tests for the anti-contamination pool partition (the hard B1 → M2 dependency)."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from maia.schemas import CorpusDocument, License, Registre, Source
from maia.synth.pools import (
    ContaminationError,
    Partition,
    assert_train_only,
    load_partition,
    pool_digest,
    split_corpus,
    verify_partition,
)


def document(text: str, *, source: Source = Source.GOVERN) -> CorpusDocument:
    return CorpusDocument(
        text=text,
        source=source,
        url="https://www.govern.ad/x",  # type: ignore[arg-type]
        fetched_at=datetime(2026, 8, 1, tzinfo=UTC),
        lang="ca",
        license=License.PUBLIC_OFFICIAL,
        registre=Registre.ESTANDARD,
    )


def corpus(count: int, *, source: Source = Source.GOVERN) -> list[CorpusDocument]:
    return [
        document(f"Document {index} de {source.value}.", source=source) for index in range(count)
    ]


# ─────────────────────────────────────────────────────────────
# The digest
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_digest_is_order_independent() -> None:
    # Re-serialising the partition must not invalidate the freeze.
    assert pool_digest(["a", "b"], ["c"]) == pool_digest(["b", "a"], ["c"])


@pytest.mark.unit
def test_moving_one_id_between_pools_changes_the_digest() -> None:
    """The property that makes the freeze mean anything."""
    assert pool_digest(["a", "b"], ["c"]) != pool_digest(["a"], ["b", "c"])


@pytest.mark.unit
def test_the_pools_are_not_interchangeable() -> None:
    # A digest that ignored which side an id was on would not detect a swapped partition.
    assert pool_digest(["a"], ["b"]) != pool_digest(["b"], ["a"])


# ─────────────────────────────────────────────────────────────
# The partition
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_an_overlapping_partition_is_refused() -> None:
    """An id in both pools means the partition guarantees nothing at all."""
    with pytest.raises(ContaminationError, match="in both pool_train and pool_bench"):
        Partition(frozenset({"a", "b"}), frozenset({"b"}))


@pytest.mark.unit
def test_a_clean_partition_reports_its_pools() -> None:
    partition = Partition(frozenset({"a", "b"}), frozenset({"c"}))
    assert partition.total == 3
    assert partition.allows("a")
    assert not partition.allows("c")
    assert not partition.allows("unknown")


@pytest.mark.unit
def test_verify_accepts_the_matching_digest() -> None:
    partition = Partition(frozenset({"a"}), frozenset({"b"}))
    verify_partition(partition, partition.digest)  # does not raise


@pytest.mark.unit
def test_verify_refuses_a_changed_partition() -> None:
    partition = Partition(frozenset({"a"}), frozenset({"b"}))
    with pytest.raises(ContaminationError, match="after the B1 freeze"):
        verify_partition(partition, "0" * 64)


@pytest.mark.unit
def test_assert_train_only_names_the_leak() -> None:
    partition = Partition(frozenset({"a"}), frozenset({"b"}))
    assert_train_only(partition, ["a"])  # does not raise
    with pytest.raises(ContaminationError, match="not in pool_train"):
        assert_train_only(partition, ["a", "b"])


@pytest.mark.unit
def test_assert_train_only_catches_an_unknown_id() -> None:
    partition = Partition(frozenset({"a"}), frozenset({"b"}))
    with pytest.raises(ContaminationError):
        assert_train_only(partition, ["never-seen"])


# ─────────────────────────────────────────────────────────────
# Splitting a corpus
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_splitting_holds_back_roughly_the_requested_share() -> None:
    partition = split_corpus(corpus(100), bench_share=0.15, seed=7)
    assert partition.total == 100
    assert 10 <= len(partition.bench) <= 20


@pytest.mark.unit
def test_splitting_is_deterministic() -> None:
    documents = corpus(50)
    first = split_corpus(documents, seed=7)
    second = split_corpus(documents, seed=7)
    assert first.digest == second.digest


@pytest.mark.unit
def test_a_different_seed_splits_differently() -> None:
    documents = corpus(50)
    assert split_corpus(documents, seed=7).digest != split_corpus(documents, seed=8).digest


@pytest.mark.unit
def test_splitting_does_not_depend_on_input_order() -> None:
    documents = corpus(50)
    forwards = split_corpus(documents, seed=7)
    backwards = split_corpus(list(reversed(documents)), seed=7)
    assert forwards.digest == backwards.digest


@pytest.mark.unit
def test_splitting_is_stratified_by_source() -> None:
    """Same reason as M1.11's sampling: an unstratified hold-out leaves the benchmark unable to
    ask about anything but the largest source."""
    documents = [*corpus(200), *corpus(20, source=Source.JURIDIC)]
    partition = split_corpus(documents, bench_share=0.15, seed=7)
    bench_sources = {doc.source.value for doc in documents if doc.id in partition.bench}
    assert bench_sources == {"govern", "juridic"}


@pytest.mark.unit
def test_a_tiny_source_still_contributes_to_bench() -> None:
    documents = [*corpus(200), *corpus(2, source=Source.JURIDIC)]
    partition = split_corpus(documents, bench_share=0.15, seed=7)
    juridic = {doc.id for doc in documents if doc.source is Source.JURIDIC}
    assert juridic & partition.bench


@pytest.mark.unit
def test_no_document_is_lost_or_duplicated() -> None:
    documents = corpus(60)
    partition = split_corpus(documents, seed=7)
    assert partition.train | partition.bench == {doc.id for doc in documents}
    assert not partition.train & partition.bench


@pytest.mark.unit
@pytest.mark.parametrize("share", [0.0, 1.0, -0.1, 1.5])
def test_an_impossible_bench_share_is_refused(share: float) -> None:
    with pytest.raises(ValueError, match="between 0 and 1"):
        split_corpus(corpus(10), bench_share=share, seed=7)


@pytest.mark.unit
def test_splitting_an_empty_corpus_yields_empty_pools() -> None:
    partition = split_corpus([], seed=7)
    assert partition.total == 0


# ─────────────────────────────────────────────────────────────
# The file, and tamper-evidence
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_partition_round_trips_through_its_file(tmp_path: Path) -> None:
    partition = split_corpus(corpus(40), seed=7)
    path = tmp_path / "pools.json"
    path.write_text(partition.to_json(), encoding="utf-8")
    assert load_partition(path).digest == partition.digest


@pytest.mark.unit
def test_editing_a_pool_file_without_refreezing_is_detected(tmp_path: Path) -> None:
    """Why the digest is recomputed on load rather than trusted.

    A hash stored next to the data it describes proves nothing on its own — only recomputing it
    makes the file tamper-evident.
    """
    partition = split_corpus(corpus(40), seed=7)
    path = tmp_path / "pools.json"
    payload = json.loads(partition.to_json())
    moved = payload["pool_bench"].pop()
    payload["pool_train"].append(moved)  # digest left untouched
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ContaminationError, match="edited without re-freezing"):
        load_partition(path)


@pytest.mark.unit
def test_loading_can_pin_to_an_expected_digest(tmp_path: Path) -> None:
    partition = split_corpus(corpus(40), seed=7)
    path = tmp_path / "pools.json"
    path.write_text(partition.to_json(), encoding="utf-8")
    assert load_partition(path, expected_digest=partition.digest).digest == partition.digest
    with pytest.raises(ContaminationError, match="after the B1 freeze"):
        load_partition(path, expected_digest="0" * 64)


@pytest.mark.unit
def test_a_malformed_pool_file_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "pools.json"
    path.write_text(json.dumps(["not", "an", "object"]), encoding="utf-8")
    with pytest.raises(ValueError, match="expected a JSON object"):
        load_partition(path)


@pytest.mark.unit
def test_a_pool_file_missing_a_key_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "pools.json"
    path.write_text(json.dumps({"digest": "x", "pool_train": []}), encoding="utf-8")
    with pytest.raises(ValueError, match="missing key\\(s\\): pool_bench"):
        load_partition(path)


@pytest.mark.unit
def test_an_overlapping_pool_file_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "pools.json"
    path.write_text(
        json.dumps({"digest": "x", "pool_train": ["a"], "pool_bench": ["a"]}), encoding="utf-8"
    )
    with pytest.raises(ContaminationError, match="in both"):
        load_partition(path)
