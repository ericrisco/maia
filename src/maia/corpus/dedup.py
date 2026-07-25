"""Near-duplicate detection — PLAN M1.08, step 2 ("MinHash dedup").

Scraped corpora are full of near-duplicates that an exact hash cannot see: a page and its
print view, an article republished under two URLs, a law quoted inside a press release, the
same institutional notice on two comuns' sites. Left in, they skew the RAG index (the same
passage retrieved three times, crowding out other evidence) and over-weight whatever they
say when the synthetic dataset is grounded on the corpus.

The standard pipeline, implemented here with no third-party dependency:

1. **Shingle** — a document becomes the set of its overlapping word *n*-grams, so word order
   matters but position does not.
2. **MinHash** — each shingle set is reduced to a fixed-length signature whose per-position
   agreement rate estimates the Jaccard similarity of the underlying sets.
3. **LSH** — signatures are cut into bands; two documents sharing any band become a
   *candidate* pair. This is what avoids comparing every document to every other.
4. **Confirm exactly** — every candidate pair is checked against the true Jaccard of its
   shingle sets. LSH is only a recall device here, so its own threshold can be loose without
   ever admitting a false duplicate.
5. **Group** — confirmed pairs are merged transitively (union-find) into clusters, and one
   representative per cluster survives.

Everything is deterministic: the permutations come from a fixed seed, and ties are broken on
the document key, so the same corpus always yields the same survivors.

**Cost.** Pure Python, roughly ``num_perm x shingles`` integer operations per document —
minutes for a corpus of tens of thousands of documents, which is fine for a batch step run
once per consolidation. ``num_perm`` is the dial if that ever stops being true.
"""

from __future__ import annotations

import hashlib
import re
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from random import Random
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover — typing-only, no runtime import
    from _typeshed import SupportsRichComparison

#: Mersenne prime 2**61 - 1 — the modulus for the permutation family.
_MERSENNE = (1 << 61) - 1

_WORD = re.compile(r"\w+", re.UNICODE)

#: Documents are keyed by their §3.1 id everywhere in the pipeline.
Key = str
#: An LSH bucket: the band index plus that band's slice of the signature.
Bucket = tuple[int, tuple[int, ...]]


@dataclass(frozen=True)
class MinHashConfig:
    """Parameters of the sketch.

    Attributes:
        num_perm: signature length. More is more accurate and proportionally slower.
        bands: how many LSH bands to cut the signature into; must divide ``num_perm``. Fewer,
            wider bands means fewer candidates and lower recall. Since candidates are
            confirmed exactly, this trades speed against recall only — never precision.
        shingle_size: words per shingle. 5 is the usual choice for prose: long enough that
            an incidental phrase match is unlikely, short enough to survive light editing.
        seed: fixes the permutation family, so runs are reproducible.
    """

    num_perm: int = 64
    bands: int = 8
    shingle_size: int = 5
    seed: int = 20260725

    def __post_init__(self) -> None:
        if self.num_perm % self.bands:
            raise ValueError(f"bands ({self.bands}) must divide num_perm ({self.num_perm}) exactly")
        if self.shingle_size < 1:
            raise ValueError("shingle_size must be at least 1")

    @property
    def rows(self) -> int:
        """Signature values per band."""
        return self.num_perm // self.bands

    @property
    def candidate_threshold(self) -> float:
        """Similarity at which a pair has ~50 % chance of becoming a candidate.

        The classic ``(1/b)^(1/r)`` estimate. Informational: it documents the recall floor,
        and should sit comfortably *below* the confirmation threshold in use.
        """
        return float((1.0 / self.bands) ** (1.0 / self.rows))

    def permutations(self) -> tuple[tuple[int, int], ...]:
        """The ``(a, b)`` coefficient pairs of ``h(x) = (a·x + b) mod p``."""
        rng = Random(self.seed)
        return tuple(
            (rng.randrange(1, _MERSENNE), rng.randrange(0, _MERSENNE)) for _ in range(self.num_perm)
        )


DEFAULT_CONFIG = MinHashConfig()


def shingles(text: str, size: int = 5) -> frozenset[int]:
    """Hash ``text`` into the set of its word *n*-gram fingerprints.

    Words are lowercased and punctuation dropped, so formatting differences do not hide a
    duplicate. A document with fewer than ``size`` words yields one shingle for the whole of
    it, so short documents are still comparable.
    """
    words = _WORD.findall(text.lower())
    if not words:
        return frozenset()
    if len(words) < size:
        grams = [" ".join(words)]
    else:
        grams = [" ".join(words[i : i + size]) for i in range(len(words) - size + 1)]
    return frozenset(
        int.from_bytes(hashlib.blake2b(gram.encode("utf-8"), digest_size=8).digest(), "big")
        % _MERSENNE
        for gram in grams
    )


def signature(
    shingle_set: frozenset[int], config: MinHashConfig = DEFAULT_CONFIG
) -> tuple[int, ...]:
    """Reduce a shingle set to its MinHash signature."""
    if not shingle_set:
        return ()
    values = list(shingle_set)
    return tuple(
        min((a * value + b) % _MERSENNE for value in values) for a, b in config.permutations()
    )


def jaccard(left: frozenset[int], right: frozenset[int]) -> float:
    """Exact Jaccard similarity of two shingle sets."""
    if not left and not right:
        return 1.0
    union = len(left | right)
    return len(left & right) / union if union else 0.0


class UnionFind:
    """Disjoint-set forest with path compression — merges confirmed duplicate pairs.

    Public because near-duplicate detection is not only a MinHash concern: the semantic dedup in
    :mod:`maia.synth.semdedup` groups embedding neighbours with the same transitive closure.
    """

    def __init__(self) -> None:
        self._parent: dict[Key, Key] = {}

    def find(self, item: Key) -> Key:
        self._parent.setdefault(item, item)
        root = item
        while self._parent[root] != root:
            root = self._parent[root]
        while self._parent[item] != root:
            self._parent[item], item = root, self._parent[item]
        return root

    def union(self, left: Key, right: Key) -> None:
        left_root, right_root = self.find(left), self.find(right)
        if left_root != right_root:
            self._parent[right_root] = left_root

    def groups(self) -> dict[Key, list[Key]]:
        clusters: dict[Key, list[Key]] = {}
        for item in self._parent:
            clusters.setdefault(self.find(item), []).append(item)
        return clusters


@dataclass
class NearDuplicateIndex:
    """Accumulates documents and reports transitive clusters of near-duplicates.

    Usage is add-then-read: :meth:`add` every document, then :meth:`clusters` once.
    """

    config: MinHashConfig = DEFAULT_CONFIG
    threshold: float = 0.85
    _shingles: dict[Key, frozenset[int]] = field(default_factory=dict, repr=False)
    _buckets: dict[Bucket, list[Key]] = field(default_factory=dict, repr=False)
    _order: list[Key] = field(default_factory=list, repr=False)

    def add(self, key: Key, text: str) -> None:
        """Index one document under ``key``.

        Raises:
            ValueError: if ``key`` was already added — a duplicate key would silently lose a
                document, and callers dedupe exact matches by id before reaching here.
        """
        if key in self._shingles:
            raise ValueError(f"key already indexed: {key!r}")
        shingle_set = shingles(text, self.config.shingle_size)
        self._shingles[key] = shingle_set
        self._order.append(key)
        if not shingle_set:
            return
        sig = signature(shingle_set, self.config)
        rows = self.config.rows
        for band in range(self.config.bands):
            chunk = sig[band * rows : (band + 1) * rows]
            self._buckets.setdefault((band, chunk), []).append(key)

    def candidate_pairs(self) -> set[tuple[Key, Key]]:
        """Pairs sharing at least one LSH band, ordered by insertion for determinism."""
        rank = {key: index for index, key in enumerate(self._order)}
        pairs: set[tuple[Key, Key]] = set()
        for members in self._buckets.values():
            if len(members) < 2:
                continue
            ordered = sorted(set(members), key=lambda key: rank[key])
            for i, left in enumerate(ordered):
                for right in ordered[i + 1 :]:
                    pairs.add((left, right))
        return pairs

    def clusters(self) -> list[list[Key]]:
        """Groups of two or more documents confirmed similar at or above ``threshold``.

        Each group is ordered by insertion, and the groups themselves by their first member,
        so the result is stable across runs. Candidate pairs are also *merged* in insertion
        order: a union-find partition does not depend on merge order, but iterating the
        candidate set directly would vary with the hash seed, and reproducible internals are
        worth more than the microseconds the sort costs.
        """
        rank = {key: index for index, key in enumerate(self._order)}
        forest = UnionFind()
        for left, right in sorted(
            self.candidate_pairs(), key=lambda pair: (rank[pair[0]], rank[pair[1]])
        ):
            if jaccard(self._shingles[left], self._shingles[right]) >= self.threshold:
                forest.union(left, right)
        found = [
            sorted(members, key=lambda key: rank[key])
            for members in forest.groups().values()
            if len(members) > 1
        ]
        return sorted(found, key=lambda members: rank[members[0]])


def find_near_duplicates(
    documents: Iterable[tuple[Key, str]],
    *,
    config: MinHashConfig = DEFAULT_CONFIG,
    threshold: float = 0.85,
) -> list[list[Key]]:
    """Convenience wrapper: index ``(key, text)`` pairs and return the duplicate clusters."""
    index = NearDuplicateIndex(config=config, threshold=threshold)
    for key, text in documents:
        index.add(key, text)
    return index.clusters()


def choose_survivors(
    clusters: Iterable[Iterable[Key]],
    prefer: Callable[[Key], SupportsRichComparison],
) -> tuple[set[Key], set[Key]]:
    """Pick one member per cluster to keep. Returns ``(kept, dropped)``.

    ``prefer`` maps a key to any sort key; the **greatest** wins, so put the most desirable
    property first. See :func:`maia.corpus.consolidate.survivor_rank` for the ordering the corpus
    pipeline uses and why licence comes before length, and
    :func:`maia.synth.semdedup.survivor_rank` for why the dataset ranks the *split* first.
    """
    kept: set[Key] = set()
    dropped: set[Key] = set()
    for cluster in clusters:
        members = list(cluster)
        winner = max(members, key=prefer)
        kept.add(winner)
        dropped.update(member for member in members if member != winner)
    return kept, dropped
