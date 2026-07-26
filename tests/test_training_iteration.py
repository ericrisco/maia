"""Tests for run iteration and the phase budget (PLAN M3.05-06)."""

from __future__ import annotations

from pathlib import Path

import pytest

from maia.training.config import MAX_FULL_RUNS, TrainingConfig
from maia.training.iteration import (
    CLEAR_MARGIN,
    Attempt,
    BudgetExhaustedError,
    append_log,
    beats,
    may_run_again,
    propose,
    read_log,
    render,
    require_budget,
    verdict,
)

BASE_SCORE = 0.500


def config(**overrides: object) -> TrainingConfig:
    return TrainingConfig.model_validate({"dataset_version": "v1", **overrides})


def attempt(score: float, **overrides: object) -> Attempt:
    return Attempt(config=config(**overrides), score=score, checkpoint="build/ckpt")


# ─────────────────────────────────────────────────────────────
# "Clearly" is a margin, not a >
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_rounding_difference_does_not_beat_the_base() -> None:
    """Shipping on 0.001 would promote a model on noise."""
    assert not beats(BASE_SCORE + 0.001, BASE_SCORE)
    assert not beats(BASE_SCORE, BASE_SCORE)
    assert not beats(BASE_SCORE - 0.1, BASE_SCORE)


@pytest.mark.unit
def test_a_clear_win_beats_the_base() -> None:
    assert beats(BASE_SCORE + CLEAR_MARGIN, BASE_SCORE)
    assert beats(BASE_SCORE + 0.1, BASE_SCORE)
    assert CLEAR_MARGIN == 0.02


@pytest.mark.unit
def test_the_margin_is_configurable() -> None:
    assert beats(BASE_SCORE + 0.005, BASE_SCORE, margin=0.001)
    assert not beats(BASE_SCORE + 0.005, BASE_SCORE, margin=0.5)


# ─────────────────────────────────────────────────────────────
# The ceiling
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_three_runs_are_allowed_and_a_fourth_is_not() -> None:
    runs = [attempt(0.5) for _ in range(MAX_FULL_RUNS)]
    assert may_run_again(runs[:2])
    assert not may_run_again(runs)
    assert MAX_FULL_RUNS == 3


@pytest.mark.unit
def test_a_fourth_run_is_refused_with_the_plans_own_advice() -> None:
    with pytest.raises(BudgetExhaustedError, match="the problem is the data"):
        require_budget([attempt(0.5) for _ in range(MAX_FULL_RUNS)])


@pytest.mark.unit
def test_a_run_inside_the_budget_is_allowed() -> None:
    require_budget([attempt(0.5)])


# ─────────────────────────────────────────────────────────────
# The verdict
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_one_clear_winner_satisfies_dod_f3() -> None:
    assessment = verdict([attempt(0.51), attempt(0.55)], base_score=BASE_SCORE)
    assert assessment.passed
    assert [item.score for item in assessment.winners] == [0.55]
    assert not assessment.back_to_phase_2
    assert "DoD-F3 met" in render(assessment)
    assert "freeze it as the candidate (M3.07)" in render(assessment)


@pytest.mark.unit
def test_three_runs_with_no_clear_winner_send_the_work_back_to_phase_2() -> None:
    """The plan's own conclusion: the problem is the data, not the hyperparameters."""
    assessment = verdict([attempt(0.50), attempt(0.505), attempt(0.51)], base_score=BASE_SCORE)
    assert not assessment.passed
    assert assessment.exhausted
    assert assessment.back_to_phase_2
    rendered = render(assessment)
    assert "the problem is the data" in rendered
    assert "Go back to Phase 2" in rendered
    assert "another hyperparameter guess" in rendered


@pytest.mark.unit
def test_runs_remaining_are_reported_rather_than_a_verdict() -> None:
    assessment = verdict([attempt(0.50)], base_score=BASE_SCORE)
    assert not assessment.passed
    assert not assessment.exhausted
    assert not assessment.back_to_phase_2
    assert "2 run(s) left in the budget" in render(assessment)


@pytest.mark.unit
def test_a_win_before_the_budget_is_spent_still_passes() -> None:
    assessment = verdict([attempt(0.60)], base_score=BASE_SCORE)
    assert assessment.passed
    assert not assessment.exhausted


@pytest.mark.unit
def test_the_best_run_is_reported() -> None:
    assessment = verdict([attempt(0.52), attempt(0.60), attempt(0.55)], base_score=BASE_SCORE)
    assert assessment.best is not None
    assert assessment.best.score == 0.60


@pytest.mark.unit
def test_no_runs_yet_has_no_best_and_no_verdict() -> None:
    assessment = verdict([], base_score=BASE_SCORE)
    assert assessment.best is None
    assert not assessment.passed
    assert not assessment.back_to_phase_2


@pytest.mark.unit
def test_each_run_is_shown_against_the_base() -> None:
    rendered = render(verdict([attempt(0.55), attempt(0.49)], base_score=BASE_SCORE))
    assert "+0.050 vs base" in rendered
    assert "-0.010 vs base" in rendered
    assert "✓ run 1" in rendered
    assert "✗ run 2" in rendered


@pytest.mark.unit
def test_notes_are_surfaced() -> None:
    noted = Attempt(config=config(), score=0.4, checkpoint="c", notes="OOM at epoch 2")
    assert "OOM at epoch 2" in render(verdict([noted], base_score=BASE_SCORE))


# ─────────────────────────────────────────────────────────────
# Proposing the next run
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_first_proposal_is_the_specs_starting_point() -> None:
    suggestion = propose([], config())
    assert suggestion is not None
    assert suggestion.learning_rate == 2e-4


@pytest.mark.unit
def test_each_proposal_changes_exactly_one_dimension() -> None:
    """Changing three things at once produces a run nobody can learn from."""
    base = config()
    tried: list[Attempt] = []
    seen: list[TrainingConfig] = []
    while (suggestion := propose(tried, base)) is not None:
        seen.append(suggestion)
        differences = sum(
            1
            for field in ("learning_rate", "epochs", "r")
            if getattr(suggestion, field) != getattr(base, field)
        )
        assert differences <= 1, suggestion.name
        tried.append(Attempt(config=suggestion, score=0.5, checkpoint="c"))
    assert len(seen) == MAX_FULL_RUNS


@pytest.mark.unit
def test_a_configuration_already_tried_is_not_proposed_again() -> None:
    base = config()
    first = propose([], base)
    assert first is not None
    second = propose([Attempt(config=first, score=0.5, checkpoint="c")], base)
    assert second is not None
    assert (second.learning_rate, second.epochs, second.r) != (
        first.learning_rate,
        first.epochs,
        first.r,
    )


@pytest.mark.unit
def test_the_learning_rate_is_explored_before_the_rank() -> None:
    """It is the cheapest dimension to change; a larger rank costs time and memory."""
    base = config()
    first = propose([], base)
    assert first is not None
    second = propose([Attempt(config=first, score=0.5, checkpoint="c")], base)
    assert second is not None
    assert second.r == base.r
    assert second.learning_rate != first.learning_rate


@pytest.mark.unit
def test_nothing_is_proposed_once_the_budget_is_spent() -> None:
    spent = [attempt(0.5, learning_rate=rate) for rate in (2e-4, 1e-4, 3e-4)]
    assert propose(spent, config()) is None


@pytest.mark.unit
def test_a_proposal_keeps_alpha_at_twice_the_rank() -> None:
    """Otherwise the config's own coherence rule would reject it."""
    base = config()
    tried = [
        Attempt(config=base.model_copy(update={"learning_rate": rate}), score=0.5, checkpoint="c")
        for rate in (2e-4, 1e-4)
    ]
    # Exhaust the learning rates and the epochs so a rank change is next.
    while (suggestion := propose(tried, base)) is not None and suggestion.r == base.r:
        tried.append(Attempt(config=suggestion, score=0.5, checkpoint="c"))
        if len(tried) >= MAX_FULL_RUNS:
            break
    if suggestion is not None and suggestion.r != base.r:
        assert suggestion.lora_alpha == suggestion.r * 2


@pytest.mark.unit
def test_the_report_names_the_next_run_when_one_is_available() -> None:
    rendered = render(verdict([attempt(0.50)], base_score=BASE_SCORE), base=config())
    assert "next: exp_v1" in rendered
    assert "one dimension changed" in rendered


@pytest.mark.unit
def test_the_report_omits_a_suggestion_when_no_base_is_given() -> None:
    assert "next:" not in render(verdict([attempt(0.50)], base_score=BASE_SCORE))


# ─────────────────────────────────────────────────────────────
# The run log
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_an_attempt_round_trips() -> None:
    original = Attempt(config=config(r=32, lora_alpha=64), score=0.55, checkpoint="c", notes="n")
    assert Attempt.from_json(original.to_json()) == original


@pytest.mark.unit
@pytest.mark.parametrize("line", ["not json", "{}", '{"score": 1}', "[]"])
def test_an_unreadable_log_line_is_refused(line: str) -> None:
    """A log that cannot be read cannot enforce a ceiling."""
    with pytest.raises(ValueError, match="not a run-log entry"):
        Attempt.from_json(line)


@pytest.mark.unit
def test_the_log_is_append_only(tmp_path: Path) -> None:
    """A rewritten log could hide a run, and the ceiling depends on the count."""
    path = tmp_path / "runs" / "log.jsonl"
    append_log(path, attempt(0.51))
    append_log(path, attempt(0.55, epochs=2))
    entries = read_log(path)
    assert [item.score for item in entries] == [0.51, 0.55]
    assert not may_run_again([*entries, attempt(0.6)])


@pytest.mark.unit
def test_reading_a_log_that_does_not_exist_yet(tmp_path: Path) -> None:
    assert read_log(tmp_path / "absent.jsonl") == []


@pytest.mark.unit
def test_the_ceiling_survives_a_restart(tmp_path: Path) -> None:
    """The count comes from the log on disk, not from memory."""
    path = tmp_path / "log.jsonl"
    for rate in (2e-4, 1e-4, 3e-4):
        append_log(path, attempt(0.50, learning_rate=rate))
    with pytest.raises(BudgetExhaustedError):
        require_budget(read_log(path))


@pytest.mark.unit
def test_the_ladder_reaches_epochs_within_the_three_run_budget() -> None:
    """The plan says "adjust lr/epochs/r"; a ladder that spends all three runs on the learning
    rate would never touch the other two axes."""
    base = config()
    tried: list[Attempt] = []
    axes: set[str] = set()
    while (suggestion := propose(tried, base)) is not None:
        if suggestion.learning_rate != base.learning_rate:
            axes.add("learning_rate")
        if suggestion.epochs != base.epochs:
            axes.add("epochs")
        if suggestion.r != base.r:
            axes.add("r")
        tried.append(Attempt(config=suggestion, score=0.5, checkpoint="c"))
    assert axes == {"learning_rate", "epochs"}


@pytest.mark.unit
def test_the_rank_axis_is_reached_when_the_budget_allows() -> None:
    base = config()
    tried: list[Attempt] = []
    ranks: set[int] = set()
    while (suggestion := propose(tried, base, maximum=10)) is not None:
        ranks.add(suggestion.r)
        tried.append(Attempt(config=suggestion, score=0.5, checkpoint="c"))
    assert ranks == {16, 32}
    # Every proposal is a valid config: alpha stayed at twice the rank.
    assert all(item.config.lora_alpha == item.config.r * 2 for item in tried)


@pytest.mark.unit
def test_the_ladder_terminates_when_every_rung_is_tried() -> None:
    base = config()
    tried: list[Attempt] = []
    while (suggestion := propose(tried, base, maximum=100)) is not None:
        tried.append(Attempt(config=suggestion, score=0.5, checkpoint="c"))
    assert 0 < len(tried) < 100
    assert propose(tried, base, maximum=100) is None


@pytest.mark.unit
def test_an_exhausted_ladder_with_budget_left_says_so(monkeypatch: pytest.MonkeyPatch) -> None:
    """Unreachable with the current constants — four rungs against a three-run ceiling — but the
    state is real if the ladder is ever shortened, and silence would read as "no advice"."""
    monkeypatch.setattr("maia.training.iteration.propose", lambda attempts, base: None)
    rendered = render(verdict([attempt(0.50)], base_score=BASE_SCORE), base=config())
    assert "no untried rung left" in rendered
    assert "not where the problem is" in rendered
