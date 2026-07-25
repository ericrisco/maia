"""Anti-contamination pool partition — the hard ``B1 → M2`` dependency.

AndBench is MAIA's sibling benchmark, and every MAIA success metric is measured on it. That
only means anything if the benchmark items were never trained on. So the corpus is split in
two **before** Phase 2 generation begins:

* ``pool_train`` — the only passages the generator may sample.
* ``pool_bench`` — reserved for benchmark items, and off-limits to generation.

The generator **validates the partition digest before it starts** (:func:`verify_partition`).
That check is the whole point of this module: a contaminated benchmark does not fail loudly, it
quietly reports better numbers than the model deserves, and by the time anyone suspects it the
training run and the evaluation are both done. Cheap to check, ruinous to skip.

Two properties make the check meaningful rather than decorative:

* The digest is **recomputed from the id lists on load** and compared to the one stored in the
  file. Editing a pool file without updating its digest is therefore detected — a stored hash
  that is merely *copied* alongside the data proves nothing.
* The digest is **order-independent**, so re-serialising the partition does not invalidate it,
  while moving a single id from one pool to the other does.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path
from random import Random

from maia.schemas import CorpusDocument

#: Share of the corpus held back for benchmark items by :func:`split_corpus`.
DEFAULT_BENCH_SHARE = 0.15


class ContaminationError(RuntimeError):
    """Raised when generation would touch ``pool_bench``, or the partition cannot be trusted."""


def pool_digest(train: Iterable[str], bench: Iterable[str]) -> str:
    """A digest of the partition itself.

    Order-independent (both pools are sorted first) so re-serialising is safe, and sensitive to
    which pool an id is in, so moving one id changes it.
    """
    hasher = hashlib.sha256()
    for label, ids in (("train", train), ("bench", bench)):
        hasher.update(label.encode("utf-8"))
        for corpus_id in sorted(ids):
            hasher.update(b"\n")
            hasher.update(corpus_id.encode("utf-8"))
        hasher.update(b"\n\n")
    return hasher.hexdigest()


@dataclass(frozen=True)
class Partition:
    """The frozen ``pool_train`` / ``pool_bench`` split."""

    train: frozenset[str]
    bench: frozenset[str]

    def __post_init__(self) -> None:
        overlap = self.train & self.bench
        if overlap:
            raise ContaminationError(
                f"{len(overlap)} document(s) are in both pool_train and pool_bench, so the "
                f"partition guarantees nothing (e.g. {sorted(overlap)[0]})"
            )

    @property
    def digest(self) -> str:
        """This partition's digest — what the generator is pinned to."""
        return pool_digest(self.train, self.bench)

    @property
    def total(self) -> int:
        """Documents across both pools."""
        return len(self.train) + len(self.bench)

    def allows(self, corpus_id: str) -> bool:
        """Whether the generator may ground on ``corpus_id``."""
        return corpus_id in self.train

    def to_json(self) -> str:
        """Serialise with the digest alongside, for committing."""
        return json.dumps(
            {
                "digest": self.digest,
                "pool_train": sorted(self.train),
                "pool_bench": sorted(self.bench),
            },
            indent=2,
        )


def split_corpus(
    documents: Iterable[CorpusDocument],
    *,
    bench_share: float = DEFAULT_BENCH_SHARE,
    seed: int,
) -> Partition:
    """Split a corpus deterministically, stratified by source.

    Stratifying matters for the same reason it does in M1.11's sampling: an unstratified
    hold-out over a corpus that is mostly one source leaves the benchmark unable to ask about
    anything else. Deterministic from ``seed``, so the partition can be reproduced from the
    corpus rather than only from the file.

    Each source keeps **at least one** document in ``pool_train``: a source is never held back
    in its entirety, because that would remove it from generation without any signal.
    """
    if not 0.0 < bench_share < 1.0:
        raise ValueError(f"bench_share must be between 0 and 1, got {bench_share}")

    by_source: dict[str, list[str]] = {}
    for document in documents:
        by_source.setdefault(document.source.value, []).append(document.id)

    rng = Random(seed)
    bench: set[str] = set()
    train: set[str] = set()
    for source in sorted(by_source):
        ids = sorted(set(by_source[source]))
        # Every source contributes at least one benchmark item, but never its whole stock: with
        # `max(1, …)` alone, a source holding a single document had 100 % of it held back and
        # nothing left to train on — which for a small but important source (the legal
        # subcorpus early on, a one-programme radio sample) silently removes it from generation
        # altogether.
        held = min(max(1, round(len(ids) * bench_share)), len(ids) - 1) if len(ids) > 1 else 0
        chosen = set(rng.sample(ids, held))
        bench |= chosen
        train |= set(ids) - chosen
    return Partition(frozenset(train), frozenset(bench))


def load_partition(path: str | Path, *, expected_digest: str | None = None) -> Partition:
    """Read a partition file, verifying its stored digest.

    Raises:
        ContaminationError: if the file's stored digest does not match the id lists it
            contains, or does not match ``expected_digest``. Recomputing rather than trusting
            the stored value is what makes the file tamper-evident: a hash sitting next to the
            data it describes proves nothing on its own.
        ValueError: if the file is not the expected shape.
    """
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"{path}: expected a JSON object, got {type(raw).__name__}")
    missing = {"digest", "pool_train", "pool_bench"} - set(raw)
    if missing:
        raise ValueError(f"{path}: missing key(s): {', '.join(sorted(missing))}")

    partition = Partition(frozenset(raw["pool_train"]), frozenset(raw["pool_bench"]))
    if partition.digest != raw["digest"]:
        raise ContaminationError(
            f"{path}: stored digest {raw['digest']} does not match the pools it contains "
            f"({partition.digest}) — the file was edited without re-freezing it"
        )
    if expected_digest is not None:
        verify_partition(partition, expected_digest)
    return partition


def verify_partition(partition: Partition, expected_digest: str) -> None:
    """Pin the generator to one specific frozen partition.

    Raises:
        ContaminationError: on any mismatch. A benchmark trained on does not fail loudly — it
            quietly reports better numbers than the model earned.
    """
    if partition.digest != expected_digest:
        raise ContaminationError(
            f"partition digest {partition.digest} does not match the frozen "
            f"{expected_digest}: pool_train/pool_bench changed after the B1 freeze, so "
            "generation would risk contaminating the benchmark"
        )


def assert_train_only(partition: Partition, corpus_ids: Sequence[str]) -> None:
    """Assert every id is in ``pool_train``.

    Raises:
        ContaminationError: naming the offending ids. Called on the passages actually sampled,
            so the guarantee holds even if a sampler is changed later.
    """
    leaked = sorted(set(corpus_ids) - partition.train)
    if leaked:
        raise ContaminationError(
            f"{len(leaked)} sampled passage(s) are not in pool_train "
            f"(e.g. {leaked[0]}) — generation must never touch pool_bench"
        )
