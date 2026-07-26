"""Tests for the retrieval evaluation gate (PLAN M4.04)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import pytest

from maia.evaluation.retrieval import (
    DEFAULT_K,
    EXPECTED_QUESTIONS,
    MIN_HIT_RATE,
    Question,
    RetrievalReport,
    Retrieved,
    coverage,
    evaluate,
    read_questions,
    render,
    worst_ranked,
)


def question(index: int, source: str | None = None) -> Question:
    return Question(question=f"Pregunta {index}?", source_id=source or f"doc-{index}")


@dataclass
class FakeRetriever:
    """Returns the source at a configured rank, or misses it entirely."""

    rank: int = 1
    miss: set[str] = field(default_factory=set)
    requested_k: list[int] = field(default_factory=list)
    duplicate: bool = False

    def search(self, question: str, *, k: int) -> list[str]:
        self.requested_k.append(k)
        index = question.split()[1].rstrip("?")
        source = f"doc-{index}"
        if self.duplicate:
            return ["noise", "noise"]
        filler = [f"noise-{position}" for position in range(k)]
        if source in self.miss:
            return filler[:k]
        placed = [*filler[: self.rank - 1], source, *filler[self.rank - 1 :]]
        return placed[:k]


def report(
    *, total: int = 10, missing: int = 0, rank: int = 1, k: int = DEFAULT_K
) -> RetrievalReport:
    questions = [question(index) for index in range(total)]
    retriever = FakeRetriever(rank=rank, miss={f"doc-{index}" for index in range(missing)})
    return evaluate(questions, retriever, k=k)


# ─────────────────────────────────────────────────────────────
# The gate
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_perfect_retrieval_passes() -> None:
    measured = report()
    assert measured.hit_rate == 1.0
    assert measured.passed
    assert "✓ hit-rate@5: 10/10" in render(measured)
    assert MIN_HIT_RATE == 0.85
    assert DEFAULT_K == 5


@pytest.mark.unit
def test_exactly_the_gate_passes() -> None:
    """17 of 20 is 85 %."""
    measured = report(total=20, missing=3)
    assert measured.hit_rate == pytest.approx(0.85)
    assert measured.passed


@pytest.mark.unit
def test_below_the_gate_fails_and_points_at_phase_4() -> None:
    measured = report(total=20, missing=4)
    assert not measured.passed
    rendered = render(measured)
    assert "✗ hit-rate@5" in rendered
    assert "fix chunking or embeddings **here**, not in F5" in rendered
    assert "looks exactly like a model that answers badly" in rendered


@pytest.mark.unit
def test_an_empty_evaluation_is_refused() -> None:
    with pytest.raises(ValueError, match="no questions to evaluate"):
        evaluate([], FakeRetriever())


@pytest.mark.unit
def test_a_report_over_nothing_does_not_pass() -> None:
    empty = RetrievalReport()
    assert not empty.passed
    assert empty.hit_rate == 0.0
    assert empty.mean_reciprocal_rank == 0.0
    assert empty.hit_rate_at(3) == 0.0


# ─────────────────────────────────────────────────────────────
# Rank, not just presence
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_source_at_rank_five_is_a_hit_but_a_worse_one() -> None:
    """hit-rate@5 counts rank 5 like rank 1, and the model reads the window in order."""
    first = report(rank=1)
    fifth = report(rank=5)
    assert first.hit_rate == fifth.hit_rate == 1.0
    assert first.mean_reciprocal_rank > fifth.mean_reciprocal_rank
    assert fifth.mean_reciprocal_rank == pytest.approx(0.2)


@pytest.mark.unit
def test_the_curve_is_reported_not_one_point() -> None:
    measured = report(rank=4)
    assert measured.hit_rate_at(1) == 0.0
    assert measured.hit_rate_at(3) == 0.0
    assert measured.hit_rate_at(5) == 1.0
    assert "curve: @1=0%, @3=0%, @5=100%" in render(measured)


@pytest.mark.unit
def test_a_miss_has_no_rank_and_no_reciprocal() -> None:
    result = Retrieved(question=question(1), ranked=("other", "another"))
    assert result.rank is None
    assert result.reciprocal_rank == 0.0
    assert not result.hit(5)


@pytest.mark.unit
def test_only_k_results_are_requested() -> None:
    """Measuring against a deeper search reports a number the served system will not reproduce."""
    retriever = FakeRetriever()
    evaluate([question(1)], retriever, k=3)
    assert retriever.requested_k == [3]


# ─────────────────────────────────────────────────────────────
# Diagnosing the failure: chunking or embeddings
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_misses_clustered_on_one_document_read_as_a_chunking_problem() -> None:
    """A location to fix, rather than a general retriever quality problem."""
    questions = [question(index, source="doc-shared") for index in range(4)]
    questions += [question(100 + index) for index in range(6)]
    measured = evaluate(questions, FakeRetriever(miss={"doc-shared"}))
    assert measured.misses_by_source == {"doc-shared": 4}
    assert measured.clustered
    assert "a chunking problem with a location" in render(measured)


@pytest.mark.unit
def test_misses_scattered_across_documents_read_as_an_embedding_problem() -> None:
    questions = [question(index) for index in range(12)]
    measured = evaluate(questions, FakeRetriever(miss={f"doc-{index}" for index in range(6)}))
    assert len(measured.misses_by_source) == 6
    assert not measured.clustered
    assert "an embedding problem, not a chunking one" in render(measured)


@pytest.mark.unit
def test_a_single_miss_is_not_called_clustered() -> None:
    """One data point is not a pattern."""
    measured = report(total=10, missing=1)
    assert len(measured.misses) == 1
    assert not measured.clustered


@pytest.mark.unit
def test_a_clean_run_reports_no_misses() -> None:
    measured = report()
    assert measured.misses == []
    assert measured.misses_by_source == {}
    assert not measured.clustered
    assert "miss(es)" not in render(measured)


@pytest.mark.unit
def test_the_worst_ranked_questions_put_misses_first() -> None:
    """Then the deepest hits: a rank-5 source is where the next chunking change shows up first."""
    questions = [question(0), question(1), question(2)]
    measured = evaluate(questions, FakeRetriever(rank=4, miss={"doc-1"}))
    worst = worst_ranked(measured, limit=2)
    assert worst[0][1] is None
    assert worst[1][1] == 4


# ─────────────────────────────────────────────────────────────
# Honest denominators
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_small_question_set_is_flagged_as_coarse() -> None:
    """At 20 questions one miss is 5 points, and the plan asks for 100."""
    rendered = render(report(total=20))
    assert f"the plan asks for {EXPECTED_QUESTIONS}" in rendered
    assert "one miss moves it 5.0%" in rendered


@pytest.mark.unit
def test_a_full_question_set_is_not_flagged() -> None:
    assert "the plan asks for" not in render(report(total=EXPECTED_QUESTIONS))


@pytest.mark.unit
def test_a_source_absent_from_the_corpus_can_never_be_a_hit() -> None:
    """It measures nothing and silently lowers the ceiling of the gate."""
    questions = [question(1, source="indexed"), question(2, source="never-indexed")]
    assert coverage(questions, {"indexed": object()}) == ["never-indexed"]
    assert coverage(questions, {"indexed": 1, "never-indexed": 1}) == []


@pytest.mark.unit
def test_duplicate_results_make_rank_meaningless_and_are_refused() -> None:
    with pytest.raises(ValueError, match="duplicate ids"):
        evaluate([question(1)], FakeRetriever(duplicate=True))


# ─────────────────────────────────────────────────────────────
# The question set
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_question_needs_text_and_a_known_source() -> None:
    with pytest.raises(ValueError, match="no text"):
        Question(question="  ", source_id="doc")
    with pytest.raises(ValueError, match="a hit-rate needs something to hit"):
        Question(question="Q?", source_id="")


@pytest.mark.unit
def test_the_question_set_round_trips(tmp_path: Path) -> None:
    path = tmp_path / "questions.jsonl"
    path.write_text(
        "\n".join(
            json.dumps({"question": f"Pregunta {index}?", "source_id": f"doc-{index}"})
            for index in range(3)
        )
        + "\n\n",
        encoding="utf-8",
    )
    loaded = read_questions(path)
    assert [item.source_id for item in loaded] == ["doc-0", "doc-1", "doc-2"]


@pytest.mark.unit
def test_a_malformed_question_names_its_line(tmp_path: Path) -> None:
    """A dropped question changes the denominator of the gate."""
    path = tmp_path / "questions.jsonl"
    path.write_text('{"question": "Q?"}\n', encoding="utf-8")
    with pytest.raises(ValueError, match=r"questions\.jsonl:1: not a retrieval question"):
        read_questions(path)
