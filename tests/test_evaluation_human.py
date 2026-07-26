"""Tests for the human eval and the blind baseline comparison (PLAN M4.07-M4.08)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from maia.evaluation.human import (
    BASELINE_QUESTIONS,
    CONVERSATIONS,
    MIN_CORRECTNESS,
    Axis,
    BaselineComparison,
    HumanEval,
    Preference,
    Score,
    Side,
    blind_pairs,
    read_scores,
    render,
    render_baseline,
    unblind,
)


def score(
    conversation: str,
    *,
    reviewer: str = "reviewer-1",
    correctness: int = 4,
    naturalness: int = 4,
    andorranitat: int = 4,
    note: str = "",
) -> Score:
    return Score(
        conversation_id=conversation,
        reviewer=reviewer,
        scores={
            Axis.CORRECTNESS: correctness,
            Axis.NATURALNESS: naturalness,
            Axis.ANDORRANITAT: andorranitat,
        },
        note=note,
    )


def evaluation(count: int = CONVERSATIONS, **overrides: int) -> HumanEval:
    return HumanEval(
        scores=[
            score(f"c{index}", reviewer=f"reviewer-{index % 2 + 1}", **overrides)  # type: ignore[arg-type]
            for index in range(count)
        ]
    )


# ─────────────────────────────────────────────────────────────
# Three axes, one gate
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_only_linguistic_correctness_is_gated() -> None:
    assert Axis.CORRECTNESS.gated
    assert not Axis.NATURALNESS.gated
    assert not Axis.ANDORRANITAT.gated
    assert MIN_CORRECTNESS == 4.0


@pytest.mark.unit
def test_strong_andorranitat_cannot_carry_weak_catalan_past_the_bar() -> None:
    """Averaging the axes would let it; the plan set the bar for Catalan alone."""
    lopsided = evaluation(correctness=2, naturalness=5, andorranitat=5)
    assert not lopsided.passed
    assert lopsided.mean(Axis.CORRECTNESS) == 2.0
    assert lopsided.mean(Axis.ANDORRANITAT) == 5.0


@pytest.mark.unit
def test_correct_catalan_passes_even_when_the_model_is_lifeless() -> None:
    """Not a gate — but the report says it, because it is still a finding."""
    lifeless = evaluation(correctness=5, naturalness=2, andorranitat=2)
    assert lifeless.passed
    rendered = render(lifeless)
    assert "naturalness: 2.00/5 (reported, not gated)" in rendered
    assert "correct and lifeless is still a finding" in rendered


@pytest.mark.unit
def test_a_missing_axis_is_refused() -> None:
    """The axes are kept apart precisely so one cannot stand in for another."""
    with pytest.raises(ValueError, match="no score for andorranitat"):
        Score(
            conversation_id="c1",
            reviewer="r",
            scores={Axis.CORRECTNESS: 4, Axis.NATURALNESS: 4},
        )


@pytest.mark.unit
@pytest.mark.parametrize("value", [0, 6, -1])
def test_a_score_outside_one_to_five_is_refused(value: int) -> None:
    with pytest.raises(ValueError, match="not 1-5"):
        score("c1", correctness=value)


@pytest.mark.unit
def test_an_unscored_evaluation_does_not_pass() -> None:
    empty = HumanEval()
    assert not empty.passed
    assert empty.mean(Axis.CORRECTNESS) is None
    assert "not scored" in render(empty)


@pytest.mark.unit
def test_exactly_four_passes() -> None:
    assert evaluation(correctness=4).passed


# ─────────────────────────────────────────────────────────────
# What is reported even when the gate passes
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_short_review_is_flagged() -> None:
    assert any(
        f"the plan asks for {CONVERSATIONS}" in note for note in evaluation(count=10).findings
    )


@pytest.mark.unit
def test_a_full_review_by_two_reviewers_has_no_findings() -> None:
    assert evaluation().findings == []


@pytest.mark.unit
def test_a_single_reviewer_is_flagged() -> None:
    """One reviewer's taste cannot be told from the model's quality."""
    solo = HumanEval(scores=[score(f"c{index}") for index in range(CONVERSATIONS)])
    assert solo.reviewers == ["reviewer-1"]
    assert any("external" in note for note in solo.findings)


@pytest.mark.unit
def test_the_worst_conversations_are_surfaced_with_their_notes() -> None:
    mixed = HumanEval(
        scores=[
            score("good", correctness=5),
            score("bad", correctness=2, note="castellanismes"),
        ]
    )
    assert mixed.worst[0][:2] == ("bad", 2)
    assert "castellanismes" in render(mixed)


@pytest.mark.unit
def test_the_review_round_trips(tmp_path: Path) -> None:
    path = tmp_path / "review.jsonl"
    path.write_text(
        json.dumps(
            {
                "conversation_id": "c1",
                "reviewer": "anna",
                "scores": {
                    "linguistic_correctness": 5,
                    "naturalness": 4,
                    "andorranitat": 4,
                },
                "note": "bé",
            }
        )
        + "\n\n",
        encoding="utf-8",
    )
    loaded = read_scores(path)
    assert loaded[0].of(Axis.CORRECTNESS) == 5
    assert loaded[0].reviewer == "anna"


@pytest.mark.unit
def test_a_malformed_score_names_its_line(tmp_path: Path) -> None:
    """A dropped score changes a mean that a gate reads."""
    path = tmp_path / "review.jsonl"
    path.write_text('{"conversation_id": "c1"}\n', encoding="utf-8")
    with pytest.raises(ValueError, match=r"review\.jsonl:1: not a review score"):
        read_scores(path)


# ─────────────────────────────────────────────────────────────
# M4.08 — the blind before/after
# ─────────────────────────────────────────────────────────────

QUESTIONS = [f"Pregunta {index}?" for index in range(BASELINE_QUESTIONS)]
BASE = [f"Resposta base {index}." for index in range(BASELINE_QUESTIONS)]
TUNED = [f"Resposta afinada {index}." for index in range(BASELINE_QUESTIONS)]


@pytest.mark.unit
def test_the_presentation_is_shuffled_so_the_reviewer_cannot_know() -> None:
    """Told which answer is the new model, a reviewer will prefer it — that is expectation, not
    quality."""
    pairs = blind_pairs(QUESTIONS, BASE, TUNED, seed=1)
    sides = {pair.tuned_side for pair in pairs}
    assert sides == {Side.A, Side.B}


@pytest.mark.unit
def test_each_pair_still_holds_both_answers_for_its_own_question() -> None:
    for index, pair in enumerate(blind_pairs(QUESTIONS, BASE, TUNED, seed=1)):
        assert {pair.a, pair.b} == {BASE[index], TUNED[index]}
        assert pair.answer_from(pair.tuned_side) == TUNED[index]


@pytest.mark.unit
def test_the_shuffle_is_reproducible_from_the_seed() -> None:
    """So the presentation can be reconstructed when someone questions the result."""
    first = [pair.tuned_side for pair in blind_pairs(QUESTIONS, BASE, TUNED, seed=7)]
    again = [pair.tuned_side for pair in blind_pairs(QUESTIONS, BASE, TUNED, seed=7)]
    other = [pair.tuned_side for pair in blind_pairs(QUESTIONS, BASE, TUNED, seed=8)]
    assert first == again
    assert first != other


@pytest.mark.unit
def test_misaligned_answer_lists_are_refused() -> None:
    """A misaligned pair compares one question's answer with another's, and looks like a
    normal row."""
    with pytest.raises(ValueError, match="misaligned pair"):
        blind_pairs(QUESTIONS, BASE[:5], TUNED, seed=1)


@pytest.mark.unit
def test_comparing_nothing_is_refused() -> None:
    with pytest.raises(ValueError, match="no questions to compare"):
        blind_pairs([], [], [], seed=1)


@pytest.mark.unit
def test_the_answer_key_is_kept_separately() -> None:
    pairs = blind_pairs(QUESTIONS, BASE, TUNED, seed=1)
    key = unblind(pairs)
    assert set(key) == set(QUESTIONS)
    assert all(side in {Side.A, Side.B} for side in key.values())


def comparison(
    *, prefer_tuned: int, total: int = BASELINE_QUESTIONS, seed: int = 1
) -> BaselineComparison:
    pairs = blind_pairs(QUESTIONS[:total], BASE[:total], TUNED[:total], seed=seed)
    preferences = []
    for index, pair in enumerate(pairs):
        if index < prefer_tuned:
            chose = pair.tuned_side
        else:
            chose = Side.B if pair.tuned_side is Side.A else Side.A
        preferences.append(Preference(question=pair.question, reviewer="anna", chose=chose))
    return BaselineComparison(pairs=pairs, preferences=preferences)


@pytest.mark.unit
def test_preferences_are_counted_once_unblinded() -> None:
    result = comparison(prefer_tuned=8)
    assert result.for_tuned == 8
    assert result.decided == BASELINE_QUESTIONS
    assert result.tuned_rate == pytest.approx(0.8)
    assert "8/10 decided comparison(s) (80%)" in render_baseline(result)


@pytest.mark.unit
def test_ties_are_excluded_from_the_rate() -> None:
    result = comparison(prefer_tuned=5)
    result.preferences.append(Preference(question=QUESTIONS[0], reviewer="marc", chose=Side.TIE))
    assert result.ties == 1
    assert result.decided == BASELINE_QUESTIONS
    assert "1 tie(s)" in render_baseline(result)


@pytest.mark.unit
def test_a_different_question_set_is_not_a_before_after() -> None:
    """M0.06 fixed ten questions; the comparison only holds over the same set."""
    rendered = render_baseline(comparison(prefer_tuned=3, total=5))
    assert f"M0.06 fixed {BASELINE_QUESTIONS} questions" in rendered
    assert "only a before/after over the same set" in rendered


@pytest.mark.unit
def test_one_reviewer_per_question_says_nothing_about_agreement() -> None:
    result = comparison(prefer_tuned=8)
    assert result.consistency is None
    assert "whether the preference is shared or personal" in render_baseline(result)


@pytest.mark.unit
def test_agreement_is_reported_when_questions_are_judged_twice() -> None:
    result = comparison(prefer_tuned=BASELINE_QUESTIONS)
    for pair in result.pairs:
        result.preferences.append(
            Preference(question=pair.question, reviewer="marc", chose=pair.tuned_side)
        )
    assert result.consistency == 1.0
    assert "reviewers agreed on 100% of contested questions" in render_baseline(result)


@pytest.mark.unit
def test_reviewers_who_disagree_make_the_aggregate_a_different_claim() -> None:
    """A 6-4 split says the models are hard to tell apart, not that the fine-tune is better."""
    result = comparison(prefer_tuned=BASELINE_QUESTIONS)
    for pair in result.pairs:
        opposite = Side.B if pair.tuned_side is Side.A else Side.A
        result.preferences.append(
            Preference(question=pair.question, reviewer="marc", chose=opposite)
        )
    assert result.consistency == pytest.approx(0.5)
    rendered = render_baseline(result)
    assert "reviewers largely disagree" in rendered
    assert "hard to tell apart" in rendered


@pytest.mark.unit
def test_an_empty_comparison_reports_no_rate() -> None:
    empty = BaselineComparison()
    assert empty.tuned_rate == 0.0
    assert empty.decided == 0
