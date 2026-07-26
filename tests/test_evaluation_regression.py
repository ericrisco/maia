"""Tests for the general-Catalan regression check (PLAN M4.03)."""

from __future__ import annotations

from dataclasses import dataclass, field

import pytest

from maia.evaluation.regression import (
    MAX_RELATIVE_DROP,
    EvalRun,
    IncomparableError,
    compare,
    measure,
    relative_drop,
    render,
    tasks_in_common,
)

HARNESS = "ai-eval-catalan-1.4.0"


def run(
    model: str,
    score: float,
    *,
    harness: str = HARNESS,
    questions: int = 500,
    tasks: dict[str, float] | None = None,
) -> EvalRun:
    return EvalRun(
        model=model,
        score=score,
        harness_version=harness,
        questions=questions,
        tasks=tasks or {},
    )


@dataclass
class FakeHarness:
    scores: dict[str, EvalRun] = field(default_factory=dict)
    calls: list[tuple[str, str | None]] = field(default_factory=list)

    def run(self, model: str, *, revision: str | None = None) -> EvalRun:
        self.calls.append((model, revision))
        return self.scores[model]


# ─────────────────────────────────────────────────────────────
# The drop is relative
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_same_absolute_fall_is_a_different_relative_drop() -> None:
    """Percentage points would let a weak model regress twice as far before failing."""
    assert relative_drop(0.80, 0.76) == pytest.approx(0.05)
    assert relative_drop(0.40, 0.36) == pytest.approx(0.10)


@pytest.mark.unit
def test_an_improvement_is_a_negative_drop() -> None:
    assert relative_drop(0.70, 0.77) == pytest.approx(-0.10)


@pytest.mark.unit
def test_there_is_nothing_to_regress_from_at_zero() -> None:
    with pytest.raises(ValueError, match="nothing to regress from"):
        relative_drop(0.0, 0.0)


# ─────────────────────────────────────────────────────────────
# Criterion O3
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_drop_within_five_percent_passes() -> None:
    regression = compare(run("base", 0.80), run("cand1", 0.77))
    assert regression.passed
    assert MAX_RELATIVE_DROP == 0.05
    assert "✓ general Catalan dropped 3.8%" in render(regression)


@pytest.mark.unit
def test_exactly_five_percent_passes() -> None:
    assert compare(run("base", 0.80), run("cand1", 0.76)).passed


@pytest.mark.unit
def test_a_larger_drop_fails() -> None:
    regression = compare(run("base", 0.80), run("cand1", 0.70))
    assert not regression.passed
    assert "✗ general Catalan dropped 12.5%" in render(regression)


@pytest.mark.unit
def test_an_improvement_passes_and_is_not_mistaken_for_success_elsewhere() -> None:
    """The anti-forgetting mix makes it possible; it says nothing about the Andorran training."""
    regression = compare(run("base", 0.70), run("cand1", 0.75))
    assert regression.passed
    assert regression.improved
    rendered = render(regression)
    assert "improved 7.1%" in rendered
    assert "not evidence the Andorran training worked" in rendered


@pytest.mark.unit
def test_the_limit_is_configurable() -> None:
    assert compare(run("base", 0.80), run("cand1", 0.70), limit=0.20).passed


# ─────────────────────────────────────────────────────────────
# Comparability
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_different_harness_version_is_not_a_comparison() -> None:
    """A model measured on a different test, read as regression with equal confidence."""
    with pytest.raises(IncomparableError, match=r"harness ai-eval-catalan-1\.4\.0 vs"):
        compare(run("base", 0.80), run("cand1", 0.76, harness="ai-eval-catalan-2.0.0"))


@pytest.mark.unit
def test_a_different_question_count_is_not_a_comparison() -> None:
    with pytest.raises(IncomparableError, match="500 vs 400 questions"):
        compare(run("base", 0.80), run("cand1", 0.76, questions=400))


@pytest.mark.unit
def test_a_different_task_set_is_not_a_comparison() -> None:
    with pytest.raises(IncomparableError, match="different task sets"):
        compare(run("base", 0.80, tasks={"a": 0.8}), run("cand1", 0.76, tasks={"b": 0.7}))


@pytest.mark.unit
def test_the_refusal_says_to_re_run_both() -> None:
    with pytest.raises(IncomparableError, match="re-run both on the same harness"):
        compare(run("base", 0.80), run("cand1", 0.76, harness="other"))


@pytest.mark.unit
def test_a_run_without_a_harness_version_cannot_be_compared_with_anything() -> None:
    with pytest.raises(ValueError, match="no harness version recorded"):
        run("base", 0.8, harness="")


@pytest.mark.unit
@pytest.mark.parametrize("score", [-0.1, 1.2])
def test_a_score_outside_the_unit_range_is_refused(score: float) -> None:
    with pytest.raises(ValueError, match=r"outside 0\.0-1\.0"):
        run("base", score)


@pytest.mark.unit
@pytest.mark.parametrize("questions", [0, -10])
def test_a_score_over_no_questions_is_refused(questions: int) -> None:
    with pytest.raises(ValueError, match="is not a score"):
        run("base", 0.8, questions=questions)


# ─────────────────────────────────────────────────────────────
# Per-task detail — where the forgetting happened
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_task_drops_are_reported_largest_first() -> None:
    regression = compare(
        run("base", 0.80, tasks={"spelling": 0.90, "syntax": 0.80, "lexicon": 0.70}),
        run("cand1", 0.78, tasks={"spelling": 0.88, "syntax": 0.40, "lexicon": 0.70}),
    )
    worst = regression.worst_tasks
    assert worst[0][0] == "syntax"
    assert worst[0][1] == pytest.approx(0.5)
    assert worst[-1][0] == "lexicon"


@pytest.mark.unit
def test_an_aggregate_that_passes_while_one_task_collapses_is_flagged() -> None:
    """Which tells you the anti-forgetting mix was the wrong shape, not the wrong size."""
    regression = compare(
        run("base", 0.80, tasks={"spelling": 0.90, "syntax": 0.80}),
        run("cand1", 0.78, tasks={"spelling": 0.95, "syntax": 0.40}),
    )
    assert regression.passed
    rendered = render(regression)
    assert "the aggregate passes but syntax fell 50.0%" in rendered
    assert "wrong shape rather than the wrong size" in rendered


@pytest.mark.unit
def test_a_run_without_task_detail_reports_none() -> None:
    assert compare(run("base", 0.80), run("cand1", 0.79)).worst_tasks == []


@pytest.mark.unit
def test_tasks_in_common_is_the_intersection() -> None:
    assert tasks_in_common(
        [run("a", 0.8, tasks={"x": 0.1, "y": 0.2}), run("b", 0.8, tasks={"y": 0.3, "z": 0.4})]
    ) == ["y"]
    assert tasks_in_common([]) == []


# ─────────────────────────────────────────────────────────────
# Driving the harness
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_both_models_are_measured_and_compared() -> None:
    harness = FakeHarness(
        scores={"gemma-4-12b-it": run("gemma-4-12b-it", 0.80), "maia-12b": run("maia-12b", 0.78)}
    )
    regression = measure(
        harness,
        base_model="gemma-4-12b-it",
        candidate_model="maia-12b",
        candidate_revision="cand1",
    )
    assert regression.passed
    assert harness.calls == [("gemma-4-12b-it", None), ("maia-12b", "cand1")]


@pytest.mark.unit
def test_a_threshold_case_is_not_decided_by_floating_point() -> None:
    """(0.80 - 0.76) / 0.80 is 0.05000000000000005 in binary; the gate must not turn on that."""
    regression = compare(run("base", 0.80), run("cand1", 0.76))
    assert regression.drop > MAX_RELATIVE_DROP  # the artefact is real
    assert regression.passed  # and does not decide the gate


@pytest.mark.unit
def test_a_failing_aggregate_is_not_also_flagged_as_a_shape_problem() -> None:
    """The shape warning is for the case where the aggregate *passes* and hides a collapse."""
    regression = compare(
        run("base", 0.80, tasks={"syntax": 0.80}),
        run("cand1", 0.50, tasks={"syntax": 0.30}),
    )
    assert not regression.passed
    rendered = render(regression)
    assert "wrong shape" not in rendered
    assert "syntax: +62.5%" in rendered
