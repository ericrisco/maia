"""Semantic near-duplicate detection over the dataset — PLAN M2.05, filter 1 of 3.

M1.05 already dedupes the *corpus* by MinHash, which catches shared wording. It cannot catch what
a generator does: asked for 20 pairs about the Consell General from overlapping passages, it
produces *Quantes persones formen el Consell General?* and *De quants consellers es compon el
Consell General?* — no shingle overlap worth speaking of, the same training signal twice.
Redundancy inflates the example count without adding information, and over-weights whatever the
generator finds easy to say.

So this filter works on **embeddings**, and the same three-step shape as M1.05: bucket to get
candidates, confirm each candidate exactly, then take the transitive closure with the union-find
from :mod:`maia.corpus.dedup`. The bucketing is random-hyperplane LSH (SimHash): project each
vector onto ``bits`` fixed random planes, keep the sign bits, and require two vectors to agree on
a whole band of them. Without it this is O(n²) cosines — 112 million pairs at 15,000 examples.

**The survivor rule is the part that matters.** A near-duplicate pair that straddles ``train`` and
``test`` is not redundancy, it is **benchmark contamination**: the model would be evaluated on
something it was trained on, and the resulting number would be a lie. So the split is ranked
first, and ``test`` beats ``val`` beats ``train`` — the copy that dies is always the trainable one,
never the evidence. :attr:`SemanticDedupReport.cross_split` counts those separately because they
are a DoD finding, not a routine drop.

Embedding is **blocked-by-resource** (a model, or an API key). :class:`Embedder` is the seam; the
tests drive a deterministic fake.
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from random import Random
from typing import Protocol

from maia.corpus.dedup import UnionFind, choose_survivors
from maia.schemas import DatasetExample, ExampleType, Split

#: Cosine similarity at or above which two examples are the same training signal. Deliberately
#: high: at 0.90 distinct questions about one institution collide, and dropping a *distinct*
#: example is a worse error than keeping a redundant one. Calibrated against the M2.06 pilot.
DEFAULT_THRESHOLD = 0.95

#: How desirable each split is as the survivor of a cross-split near-duplicate — see the module
#: docstring. Greatest wins.
_SPLIT_RANK = {Split.TEST: 2, Split.VAL: 1, Split.TRAIN: 0}

Vector = Sequence[float]


class Embedder(Protocol):
    """Turns texts into vectors. Blocked-by-resource: a local model or a hosted API."""

    def embed(self, texts: Sequence[str]) -> list[Vector]:
        """Embed every text, in order. Must return exactly ``len(texts)`` vectors."""


@dataclass(frozen=True)
class SimHashConfig:
    """Random-hyperplane LSH parameters.

    ``bands * rows`` sign bits are drawn once from ``seed``, and two vectors are candidates when
    they agree on all ``rows`` bits of any band. More rows means fewer, better candidates; more
    bands means more chances to catch a true pair. 16x4 keeps recall high at the 0.95 threshold
    while leaving the candidate set small enough to confirm exactly.
    """

    bands: int = 16
    rows: int = 4
    seed: int = 20260725

    @property
    def bits(self) -> int:
        """Total number of hyperplanes."""
        return self.bands * self.rows


DEFAULT_SIMHASH = SimHashConfig()


def random_planes(dimensions: int, config: SimHashConfig = DEFAULT_SIMHASH) -> list[list[float]]:
    """``config.bits`` random hyperplanes, reproducible from ``config.seed``.

    Gaussian coordinates make the normals uniform over directions, which is what makes the
    probability of two vectors sharing a sign bit a function of the angle between them — the
    property the whole scheme rests on.
    """
    if dimensions <= 0:
        raise ValueError("dimensions must be positive")
    rng = Random(config.seed)
    return [[rng.gauss(0.0, 1.0) for _ in range(dimensions)] for _ in range(config.bits)]


def dot(left: Vector, right: Vector) -> float:
    """Dot product. ``left`` and ``right`` must be the same length."""
    if len(left) != len(right):
        raise ValueError(f"dimension mismatch: {len(left)} vs {len(right)}")
    return math.fsum(a * b for a, b in zip(left, right, strict=True))


def cosine(left: Vector, right: Vector) -> float:
    """Cosine similarity, or ``0.0`` if either vector has no length.

    A zero vector has no direction, so it is similar to nothing — treating it as similar to
    everything would collapse the whole dataset into one cluster.
    """
    scale = math.sqrt(dot(left, left)) * math.sqrt(dot(right, right))
    return dot(left, right) / scale if scale else 0.0


def sign_bits(vector: Vector, planes: Sequence[Vector]) -> tuple[bool, ...]:
    """Which side of each hyperplane ``vector`` falls on."""
    return tuple(dot(vector, plane) >= 0 for plane in planes)


def text_of(example: DatasetExample) -> str:
    """The text a dataset example is deduped on — every message, both roles.

    Not the prompt alone: two identical prompts with genuinely different answers are two
    different training signals, and dropping one loses information. Not the answer alone either,
    for the mirror reason.
    """
    return "\n".join(message.content for message in example.messages)


@dataclass
class SemanticIndex:
    """Accumulates embedded examples and reports transitive near-duplicate clusters.

    Add-then-read, like :class:`maia.corpus.dedup.NearDuplicateIndex`.
    """

    threshold: float = DEFAULT_THRESHOLD
    config: SimHashConfig = DEFAULT_SIMHASH
    _vectors: dict[str, Vector] = field(default_factory=dict, repr=False)
    _buckets: dict[tuple[int, tuple[bool, ...]], list[str]] = field(
        default_factory=dict, repr=False
    )
    _order: list[str] = field(default_factory=list, repr=False)
    _planes: list[list[float]] | None = field(default=None, repr=False)

    def add(self, key: str, vector: Vector) -> None:
        """Index one example's embedding.

        Raises:
            ValueError: if ``key`` was already added, if ``vector`` is empty, or if its dimension
                differs from the first vector seen — a silent mismatch would make every
                similarity meaningless.
        """
        if key in self._vectors:
            raise ValueError(f"key already indexed: {key!r}")
        if not vector:
            raise ValueError(f"{key!r}: empty embedding")
        if self._planes is None:
            self._planes = random_planes(len(vector), self.config)
        elif len(vector) != len(self._planes[0]):
            raise ValueError(
                f"{key!r}: embedding has {len(vector)} dimensions, expected {len(self._planes[0])}"
            )
        self._vectors[key] = vector
        self._order.append(key)
        bits = sign_bits(vector, self._planes)
        for band in range(self.config.bands):
            chunk = bits[band * self.config.rows : (band + 1) * self.config.rows]
            self._buckets.setdefault((band, chunk), []).append(key)

    def candidate_pairs(self) -> list[tuple[str, str]]:
        """Pairs agreeing on a whole band, in insertion order so runs are reproducible."""
        rank = {key: index for index, key in enumerate(self._order)}
        seen: set[tuple[str, str]] = set()
        pairs: list[tuple[str, str]] = []
        for members in self._buckets.values():
            if len(members) < 2:
                continue
            ordered = sorted(set(members), key=lambda key: rank[key])
            for index, left in enumerate(ordered):
                for right in ordered[index + 1 :]:
                    if (left, right) not in seen:
                        seen.add((left, right))
                        pairs.append((left, right))
        return sorted(pairs, key=lambda pair: (rank[pair[0]], rank[pair[1]]))

    def clusters(self) -> list[list[str]]:
        """Groups of two or more examples whose cosine similarity reaches ``threshold``."""
        rank = {key: index for index, key in enumerate(self._order)}
        forest = UnionFind()
        for left, right in self.candidate_pairs():
            if cosine(self._vectors[left], self._vectors[right]) >= self.threshold:
                forest.union(left, right)
        found = [
            sorted(members, key=lambda key: rank[key])
            for members in forest.groups().values()
            if len(members) > 1
        ]
        return sorted(found, key=lambda members: rank[members[0]])


def survivor_rank(example: DatasetExample) -> tuple[int, float, int, str]:
    """Sort key for choosing which near-duplicate to keep. Greatest wins.

    ``(split, judge_score, length, id)``, and **split comes first** deliberately: a pair spanning
    ``train`` and ``test`` is benchmark contamination, so the held-out copy must always be the one
    that survives, whatever its score or length. Within one split the better-judged example wins,
    then the longer one (more of the passage's content), then the id, to break ties reproducibly.
    """
    return (
        _SPLIT_RANK[example.split],
        example.judge_score,
        len(text_of(example)),
        str(example.id),
    )


@dataclass
class SemanticDedupReport:
    """What the semantic dedup examined and removed."""

    examined: int = 0
    embedded: int = 0
    clusters: int = 0
    dropped: int = 0
    cross_split: int = 0
    cross_split_examples: list[tuple[str, str]] = field(default_factory=list)

    @property
    def kept(self) -> int:
        """How many examples survive."""
        return self.examined - self.dropped


def deduplicate(
    examples: Sequence[DatasetExample],
    embedder: Embedder,
    *,
    threshold: float = DEFAULT_THRESHOLD,
    config: SimHashConfig = DEFAULT_SIMHASH,
    batch_size: int = 64,
) -> tuple[list[DatasetExample], SemanticDedupReport]:
    """Drop semantic near-duplicates, keeping the best member of each cluster.

    Raises:
        ValueError: if ``embedder`` returns a different number of vectors than it was given —
            that would silently pair every example with the wrong embedding.
    """
    report = SemanticDedupReport(examined=len(examples))
    if not examples:
        return [], report

    index = SemanticIndex(threshold=threshold, config=config)
    by_id = {str(example.id): example for example in examples}
    for batch in _batched(examples, batch_size):
        texts = [text_of(example) for example in batch]
        vectors = embedder.embed(texts)
        if len(vectors) != len(texts):
            raise ValueError(
                f"embedder returned {len(vectors)} vectors for {len(texts)} texts — refusing to "
                "pair examples with embeddings that may not be theirs"
            )
        for example, vector in zip(batch, vectors, strict=True):
            index.add(str(example.id), vector)
            report.embedded += 1

    clusters = index.clusters()
    report.clusters = len(clusters)
    for cluster in clusters:
        splits = {by_id[key].split for key in cluster}
        if len(splits) > 1:
            report.cross_split += 1
            report.cross_split_examples.append((cluster[0], cluster[1]))
    _, dropped_ids = choose_survivors(clusters, lambda key: survivor_rank(by_id[key]))
    report.dropped = len(dropped_ids)
    return [example for example in examples if str(example.id) not in dropped_ids], report


def _batched(examples: Sequence[DatasetExample], size: int) -> Iterable[Sequence[DatasetExample]]:
    """Fixed-size batches, because embedding APIs are priced and rate-limited per call."""
    if size <= 0:
        raise ValueError("batch_size must be positive")
    for start in range(0, len(examples), size):
        yield examples[start : start + size]


def render(report: SemanticDedupReport) -> str:
    """Human-readable summary."""
    lines = [
        f"semantic dedup: {report.kept}/{report.examined} kept "
        f"({report.dropped} dropped from {report.clusters} cluster(s))"
    ]
    if report.cross_split:
        lines.append(
            f"  ⚠ {report.cross_split} cluster(s) span more than one split — that is BENCHMARK "
            "CONTAMINATION, not redundancy; the held-out copy was kept and the trainable one "
            "dropped, but the generator produced near-identical items either side of the wall"
        )
        for left, right in report.cross_split_examples[:5]:
            lines.append(f"    {left} ~ {right}")
    return "\n".join(lines)


def share_by_type(examples: Iterable[DatasetExample]) -> dict[ExampleType, float]:
    """Share of the dataset held by each type — how filtering moved §3.2's distribution."""
    counts: dict[ExampleType, int] = {}
    total = 0
    for example in examples:
        counts[example.type] = counts.get(example.type, 0) + 1
        total += 1
    return {kind: count / total for kind, count in counts.items()} if total else {}


def ollama_embedder(
    url: str = "http://localhost:11434/api/embed",
    *,
    model: str = "jina/jina-embeddings-v2-base-es",
    timeout: float = 120.0,
) -> Embedder:
    """A live embedder over an Ollama-compatible ``/api/embed`` endpoint.

    Blocked-by-resource: needs the service reachable and the model pulled. ``requests`` is
    imported locally so this module and its tests need no network. Any endpoint answering with
    ``{"embeddings": [[...], ...]}`` works, which is also what TEI and vLLM's OpenAI-compatible
    embeddings route return under that key.
    """
    import requests

    @dataclass(frozen=True)
    class _HttpEmbedder:
        endpoint: str
        model: str

        def embed(self, texts: Sequence[str]) -> list[Vector]:
            response = requests.post(
                self.endpoint, json={"model": self.model, "input": list(texts)}, timeout=timeout
            )
            response.raise_for_status()
            return parse_embeddings(response.json(), len(texts))

    return _HttpEmbedder(url, model)


def parse_embeddings(payload: object, expected: int) -> list[Vector]:
    """Read an ``{"embeddings": [[...]]}`` response.

    Raises:
        ValueError: if the payload is not that shape, or holds the wrong number of vectors. An
            error body returned as HTTP 200 would otherwise read as a batch of embeddings and
            pair every example with the wrong vector.
    """
    if not isinstance(payload, dict) or not isinstance(payload.get("embeddings"), list):
        raise ValueError(
            "not an embeddings response: expected an 'embeddings' list, got "
            f"{sorted(payload) if isinstance(payload, dict) else type(payload).__name__}"
        )
    vectors = payload["embeddings"]
    if len(vectors) != expected:
        raise ValueError(f"got {len(vectors)} embeddings for {expected} texts")
    parsed: list[Vector] = []
    for index, vector in enumerate(vectors):
        if not isinstance(vector, list) or not all(
            isinstance(value, int | float) and not isinstance(value, bool) for value in vector
        ):
            raise ValueError(f"embedding {index} is not a list of numbers")
        parsed.append([float(value) for value in vector])
    return parsed
