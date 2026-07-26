"""Retrieval evaluation — PLAN M4.04.

*"Retrieval hit-rate@5 over 100 questions with known source doc (≥85 %). **If it fails, fix
chunking/embeddings here, not in F5.**"*

That last clause is why this is a Phase 4 gate and not a Phase 5 concern. A model that answers badly
because retrieval never handed it the right passage looks exactly like a model that answers badly,
and the fix is in the index rather than in the weights. Measuring retrieval **separately** is what
lets those two be told apart — and doing it before F5 is what stops a chunking bug from being
diagnosed as a training failure.

Two things this measures that a single hit-rate does not:

**Where in the ranking the hit landed.** Hit-rate@5 counts a document found at rank 5 exactly like
one found at rank 1, and a retriever that is technically passing while burying every answer at the
bottom of the window will behave badly in practice — the model sees four irrelevant passages first.
:attr:`RetrievalReport.mean_reciprocal_rank` is reported alongside, and
:attr:`hit_rate_at` gives the curve rather than one point on it.

**Which questions fail, and whether they share a source.** If the misses cluster on one document,
that is a chunking problem with a location; if they scatter, it is an embedding problem. The report
groups them, because *"85 % hit-rate"* alone tells you nothing about which of the two to fix.

The retriever is **blocked-by-resource** (Qdrant plus an embedding model); :class:`Retriever` is the
seam.
"""

from __future__ import annotations

import json
import statistics
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

#: The plan's gate: at least this share of questions must find their source in the top ``k``.
MIN_HIT_RATE = 0.85

#: The plan's window.
DEFAULT_K = 5

#: The plan's question count. Fewer makes the rate coarse: at 20 questions one miss is 5 points.
EXPECTED_QUESTIONS = 100


class Retriever(Protocol):
    """A retrieval index. Blocked-by-resource: Qdrant and an embedding model."""

    def search(self, question: str, *, k: int) -> list[str]:
        """Return up to ``k`` corpus document ids, best first."""


@dataclass(frozen=True)
class Question:
    """One evaluation question with the document that should answer it."""

    question: str
    source_id: str
    note: str = ""

    def __post_init__(self) -> None:
        if not self.question.strip():
            raise ValueError("a question with no text cannot be retrieved for")
        if not self.source_id.strip():
            raise ValueError(
                f"{self.question[:40]!r} has no known source; a hit-rate needs something to hit"
            )


@dataclass(frozen=True)
class Retrieved:
    """What retrieval returned for one question."""

    question: Question
    ranked: tuple[str, ...]

    @property
    def rank(self) -> int | None:
        """1-based rank of the source document, or ``None`` if it was not returned."""
        try:
            return self.ranked.index(self.question.source_id) + 1
        except ValueError:
            return None

    def hit(self, k: int) -> bool:
        """Whether the source appears in the top ``k``."""
        rank = self.rank
        return rank is not None and rank <= k

    @property
    def reciprocal_rank(self) -> float:
        """``1/rank``, or ``0.0`` for a miss."""
        rank = self.rank
        return 1.0 / rank if rank is not None else 0.0


@dataclass
class RetrievalReport:
    """How well retrieval found the documents it was supposed to."""

    results: list[Retrieved] = field(default_factory=list)
    k: int = DEFAULT_K
    minimum: float = MIN_HIT_RATE

    @property
    def total(self) -> int:
        """Questions evaluated."""
        return len(self.results)

    @property
    def hits(self) -> int:
        """Questions whose source was in the top ``k``."""
        return sum(1 for result in self.results if result.hit(self.k))

    @property
    def hit_rate(self) -> float:
        """Share of questions whose source was retrieved in the top ``k``."""
        return self.hits / self.total if self.total else 0.0

    @property
    def passed(self) -> bool:
        """Whether the plan's gate is met."""
        return self.total > 0 and self.hit_rate >= self.minimum

    @property
    def mean_reciprocal_rank(self) -> float:
        """MRR over every question.

        Reported because hit-rate@5 counts rank 5 exactly like rank 1, and a retriever that buries
        every answer at the bottom of the window hands the model four irrelevant passages first.
        """
        return (
            statistics.fmean(result.reciprocal_rank for result in self.results)
            if self.results
            else 0.0
        )

    def hit_rate_at(self, k: int) -> float:
        """Hit-rate at an arbitrary ``k`` — the curve, rather than one point on it."""
        return (
            sum(1 for result in self.results if result.hit(k)) / self.total if self.total else 0.0
        )

    @property
    def misses(self) -> list[Retrieved]:
        """Questions whose source was not in the top ``k``."""
        return [result for result in self.results if not result.hit(self.k)]

    @property
    def misses_by_source(self) -> dict[str, int]:
        """Missed questions grouped by the document that should have answered them.

        The distinction the gate needs: misses clustered on one document are a **chunking** problem
        with a location, misses scattered across many are an **embedding** problem. *"85 %"* alone
        does not say which.
        """
        grouped: dict[str, int] = {}
        for result in self.misses:
            grouped[result.question.source_id] = grouped.get(result.question.source_id, 0) + 1
        return dict(sorted(grouped.items(), key=lambda item: (-item[1], item[0])))

    @property
    def clustered(self) -> bool:
        """Whether the misses concentrate on few documents rather than scattering.

        True when the worst document accounts for at least a third of the misses and there is more
        than one miss — the shape that says "fix this chunk", not "fix the embeddings".
        """
        grouped = self.misses_by_source
        if len(self.misses) < 2 or not grouped:
            return False
        return max(grouped.values()) / len(self.misses) >= 1 / 3


def evaluate(
    questions: Sequence[Question],
    retriever: Retriever,
    *,
    k: int = DEFAULT_K,
    minimum: float = MIN_HIT_RATE,
) -> RetrievalReport:
    """Retrieve for every question and measure.

    Retrieves ``k`` results, not more: measuring hit-rate@5 against a deeper search would report a
    number the served system will not reproduce.

    Raises:
        ValueError: if there are no questions, or if the retriever returns duplicate ids for one
            question. A duplicate would make rank meaningless and could turn one hit into two.
    """
    if not questions:
        raise ValueError("no questions to evaluate retrieval with")
    results: list[Retrieved] = []
    for question in questions:
        ranked = tuple(retriever.search(question.question, k=k))
        if len(set(ranked)) != len(ranked):
            raise ValueError(
                f"{question.question[:40]!r}: the retriever returned duplicate ids, which makes "
                "rank meaningless"
            )
        results.append(Retrieved(question=question, ranked=ranked))
    return RetrievalReport(results=results, k=k, minimum=minimum)


def read_questions(path: Path) -> list[Question]:
    """Read the evaluation set from JSONL.

    Raises:
        ValueError: naming the line. A dropped question changes the denominator of the gate.
    """
    questions: list[Question] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
            questions.append(
                Question(
                    question=str(payload["question"]),
                    source_id=str(payload["source_id"]),
                    note=str(payload.get("note", "")),
                )
            )
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            raise ValueError(f"{path}:{number}: not a retrieval question ({error})") from error
    return questions


def render(report: RetrievalReport) -> str:
    """Human-readable verdict on the retrieval gate."""
    mark = "✓" if report.passed else "✗"
    lines = [
        f"{mark} hit-rate@{report.k}: {report.hits}/{report.total} "
        f"({report.hit_rate:.1%}, gate ≥{report.minimum:.0%})",
        f"  MRR {report.mean_reciprocal_rank:.3f} — hit-rate@{report.k} counts rank {report.k} "
        "like rank 1, and the model reads the window in order",
    ]
    curve = [f"@{k}={report.hit_rate_at(k):.0%}" for k in (1, 3, report.k, report.k * 2)]
    lines.append("  curve: " + ", ".join(curve))

    if report.total < EXPECTED_QUESTIONS:
        lines.append(
            f"  ⚠ {report.total} question(s); the plan asks for {EXPECTED_QUESTIONS}, and a "
            f"smaller set makes the rate coarse (one miss moves it {1 / report.total:.1%})"
        )
    if report.misses:
        lines.append(f"  {len(report.misses)} miss(es), by source document:")
        for source, count in list(report.misses_by_source.items())[:5]:
            lines.append(f"    {source[:16]}…: {count}")
        lines.append(
            "  → misses cluster on few documents: a chunking problem with a location"
            if report.clustered
            else "  → misses scatter across documents: an embedding problem, not a chunking one"
        )
    if not report.passed:
        lines.append(
            "  the plan is explicit: fix chunking or embeddings **here**, not in F5 — a model that "
            "never received the right passage looks exactly like a model that answers badly"
        )
    return "\n".join(lines)


def worst_ranked(report: RetrievalReport, limit: int = 5) -> list[tuple[str, int | None]]:
    """The questions whose source ranked worst, for a human to look at.

    Misses first (rank ``None``), then the deepest hits: a source found at rank 5 is a near-miss and
    is where the next chunking change will show up first.
    """
    # Misses sort first (``False`` < ``True``), then hits by descending rank via the negation.
    ordered = sorted(
        report.results, key=lambda result: (result.rank is not None, -(result.rank or 0))
    )
    return [(result.question.question, result.rank) for result in ordered[:limit]]


def coverage(questions: Sequence[Question], corpus_ids: Mapping[str, object]) -> list[str]:
    """Question sources that are not in the corpus.

    A question whose source document is not indexed can never be a hit, so it measures nothing and
    silently lowers the ceiling of the gate.
    """
    return sorted({q.source_id for q in questions if q.source_id not in corpus_ids})
