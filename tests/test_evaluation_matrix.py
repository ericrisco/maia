"""Tests for the 4-config matrix and the DoD-F4 gate (PLAN M4.05-M4.06)."""

from __future__ import annotations

import pytest

from maia.evaluation.andbench import Track, TrackResult
from maia.evaluation.matrix import (
    MIN_CONTRIBUTION,
    MIN_OBERT_WITH_RAG,
    MIN_OBERT_WITHOUT_RAG,
    Config,
    Matrix,
    Threshold,
    contributions,
    diagnosis,
    from_results,
    gate,
    render_gate,
    render_matrix,
    thresholds,
)


def result(score: float, track: Track = Track.OBERT) -> TrackResult:
    return TrackResult(track=track, score=score, items=100)


def matrix(
    base: float | None = 0.50,
    base_rag: float | None = 0.70,
    tuned: float | None = 0.72,
    tuned_rag: float | None = 0.92,
) -> Matrix:
    cells: dict[Config, list[TrackResult]] = {}
    for config, score in (
        (Config.BASE, base),
        (Config.BASE_RAG, base_rag),
        (Config.TUNED, tuned),
        (Config.TUNED_RAG, tuned_rag),
    ):
        if score is not None:
            cells[config] = [result(score)]
    return from_results(cells)


def named(items: list[object]) -> dict[str, object]:
    return {item.name: item for item in items}  # type: ignore[attr-defined]


# ─────────────────────────────────────────────────────────────
# The four cells
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_four_configurations_are_the_plans() -> None:
    assert {config.value for config in Config} == {
        "base-norag",
        "base-rag",
        "tuned-norag",
        "tuned-rag",
    }
    assert Config.TUNED_RAG.tuned and Config.TUNED_RAG.rag
    assert not Config.BASE.tuned and not Config.BASE.rag
    assert Config.TUNED_RAG.label == "fine-tune +RAG"


@pytest.mark.unit
def test_a_complete_matrix_reports_every_cell() -> None:
    full = matrix()
    assert full.complete
    assert full.missing == []
    assert full.score(Config.TUNED_RAG) == 0.92


@pytest.mark.unit
def test_three_cells_are_not_a_smaller_matrix() -> None:
    """They make the question unanswerable, which is the only reason the matrix exists."""
    partial = matrix(base_rag=None)
    assert not partial.complete
    assert partial.missing == [Config.BASE_RAG]
    assert contributions(partial) is None
    assert "cannot say which piece is doing the work" in diagnosis(partial)[0]


@pytest.mark.unit
def test_an_unmeasured_track_reports_none() -> None:
    assert matrix().score(Config.BASE, Track.CONEIX) is None


# ─────────────────────────────────────────────────────────────
# Which piece is doing the work
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_each_contribution_holds_the_other_piece_constant() -> None:
    computed = contributions(matrix())
    assert computed is not None
    by_name = named(list(computed))
    assert by_name["fine-tune (-RAG)"].delta == pytest.approx(0.22)  # type: ignore[attr-defined]
    assert by_name["RAG (base)"].delta == pytest.approx(0.20)  # type: ignore[attr-defined]
    assert by_name["RAG (fine-tune)"].delta == pytest.approx(0.20)  # type: ignore[attr-defined]


@pytest.mark.unit
def test_a_healthy_matrix_says_both_pieces_contribute() -> None:
    notes = diagnosis(matrix())
    assert notes == ["both pieces contribute, and they do not fight"]


@pytest.mark.unit
def test_a_fine_tune_that_only_helps_with_rag_is_diagnosed_as_a_data_problem() -> None:
    """RAG is answering and the fine-tune is along for the ride."""
    notes = diagnosis(matrix(base=0.50, tuned=0.51, base_rag=0.70, tuned_rag=0.90))
    assert any("along for the ride" in note for note in notes)
    assert any("(F2)" in note for note in notes)


@pytest.mark.unit
def test_a_fine_tune_that_adds_nothing_once_rag_answers_is_teaching_facts() -> None:
    notes = diagnosis(matrix(base=0.50, tuned=0.70, base_rag=0.90, tuned_rag=0.91))
    assert any("teaching facts rather than register" in note for note in notes)


@pytest.mark.unit
def test_a_fine_tune_that_never_beats_the_base_points_at_m3_05() -> None:
    notes = diagnosis(matrix(base=0.50, tuned=0.505, base_rag=0.70, tuned_rag=0.705))
    assert any("three runs like this mean the problem is the data" in note for note in notes)


@pytest.mark.unit
def test_rag_adding_nothing_names_both_possible_causes() -> None:
    notes = diagnosis(matrix(base=0.50, base_rag=0.51, tuned=0.72, tuned_rag=0.73))
    assert any(
        "not finding the right passages" in note and "ignoring them" in note for note in notes
    )


@pytest.mark.unit
def test_a_negative_interaction_is_flagged() -> None:
    """The fine-tuned model may be answering from its weights instead of the retrieved context."""
    notes = diagnosis(matrix(base=0.50, base_rag=0.70, tuned=0.72, tuned_rag=0.80))
    assert any("answering from its weights" in note for note in notes)


@pytest.mark.unit
def test_a_contribution_below_the_noise_floor_does_not_count() -> None:
    computed = contributions(matrix(base=0.50, tuned=0.51))
    assert computed is not None
    assert not named(list(computed))["fine-tune (-RAG)"].contributed  # type: ignore[attr-defined]
    assert MIN_CONTRIBUTION == 0.02


@pytest.mark.unit
def test_the_published_table_shows_cells_contributions_and_the_diagnosis() -> None:
    rendered = render_matrix(matrix())
    assert "| fine-tune +RAG | 0.920 |" in rendered
    assert "| base -RAG | 0.500 |" in rendered
    assert "| fine-tune (-RAG) | +0.220 ✓ |" in rendered
    assert "both pieces contribute" in rendered


@pytest.mark.unit
def test_an_incomplete_table_shows_a_dash_and_no_contributions() -> None:
    rendered = render_matrix(matrix(tuned=None))
    assert "| fine-tune -RAG | — |" in rendered
    assert "| contribution |" not in rendered


# ─────────────────────────────────────────────────────────────
# The thresholds
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_and_obert_has_two_thresholds_because_serving_has_rag() -> None:
    assert MIN_OBERT_WITH_RAG == 0.90
    assert MIN_OBERT_WITHOUT_RAG == 0.70
    checks = {check.name: check for check in thresholds(matrix())}
    assert checks["And-Obert +RAG"].measured == 0.92
    assert checks["And-Obert -RAG"].measured == 0.72
    assert all(check.passed for check in checks.values() if not check.unmeasured)


@pytest.mark.unit
def test_a_drop_is_inverted_into_headroom_so_every_threshold_reads_as_at_least() -> None:
    passing = {c.name: c for c in thresholds(matrix(), catalan_drop=0.03)}
    failing = {c.name: c for c in thresholds(matrix(), catalan_drop=0.08)}
    assert passing["general-Catalan headroom"].passed
    assert not failing["general-Catalan headroom"].passed


@pytest.mark.unit
def test_an_unmeasured_threshold_does_not_pass() -> None:
    """ "All thresholds green and documented" cannot be satisfied by one nobody measured."""
    check = Threshold("something", None, 0.5, "F2")
    assert check.unmeasured
    assert not check.passed


@pytest.mark.unit
def test_every_plan_threshold_is_present() -> None:
    names = {check.name for check in thresholds(matrix())}
    assert names == {
        "And-Obert +RAG",
        "And-Obert -RAG",
        "general-Catalan headroom",
        "retrieval hit-rate@5",
        "human linguistic correctness",
    }


@pytest.mark.unit
def test_each_threshold_carries_the_phase_to_return_to() -> None:
    """A bare "FAIL" leaves that to guesswork at the moment someone decides what to redo."""
    checks = {check.name: check for check in thresholds(matrix())}
    assert checks["And-Obert -RAG"].phase == "F3"
    assert checks["retrieval hit-rate@5"].phase == "F4"
    assert checks["general-Catalan headroom"].phase == "F2"


# ─────────────────────────────────────────────────────────────
# The gate
# ─────────────────────────────────────────────────────────────


MEASURED = {"catalan_drop": 0.03, "retrieval_hit_rate": 0.90, "human_correctness": 4.2}


@pytest.mark.unit
def test_everything_green_and_complete_lets_phase_5_proceed() -> None:
    verdict = gate(matrix(), **MEASURED)
    assert verdict.passed
    rendered = render_gate(verdict)
    assert "✓ PASS" in rendered
    assert "F5 may proceed (PO validates)" in rendered


@pytest.mark.unit
def test_one_failing_threshold_blocks_phase_5_and_names_the_phase() -> None:
    verdict = gate(matrix(), **{**MEASURED, "retrieval_hit_rate": 0.60})
    assert not verdict.passed
    assert verdict.phases == ["F4"]
    rendered = render_gate(verdict)
    assert "do **not** advance to F5" in rendered
    assert "iterate F4" in rendered


@pytest.mark.unit
def test_an_incomplete_matrix_blocks_the_gate_even_with_green_thresholds() -> None:
    """DoD-F4 asks for the matrix to be published, and three cells cannot be published as four."""
    verdict = gate(matrix(base_rag=None), **MEASURED)
    assert not verdict.passed
    assert "matrix incomplete: base +RAG not measured" in render_gate(verdict)


@pytest.mark.unit
def test_unmeasured_thresholds_block_the_gate_and_are_named_as_such() -> None:
    verdict = gate(matrix())
    assert not verdict.passed
    assert len(verdict.unmeasured) == 3
    rendered = render_gate(verdict)
    assert "NOT MEASURED" in rendered
    assert "an unmeasured threshold does not pass" in rendered


@pytest.mark.unit
def test_several_failures_list_every_phase_to_return_to() -> None:
    verdict = gate(
        matrix(tuned=0.40, tuned_rag=0.50),
        **{**MEASURED, "catalan_drop": 0.10, "retrieval_hit_rate": 0.5},
    )
    assert set(verdict.phases) >= {"F2", "F3", "F4"}
    # And-Obert +RAG is attributed to F2/F5, since the served path is both data and serving.
    assert "iterate F2 and F2/F5 and F3 and F4" in render_gate(verdict)


@pytest.mark.unit
def test_the_gate_lists_every_threshold_with_its_note() -> None:
    rendered = render_gate(gate(matrix(), **MEASURED))
    assert "how the model is actually served" in rendered
    assert "fix chunking or embeddings here, not in F5" in rendered
    assert "scored 1-5 by Andorran speakers" in rendered


@pytest.mark.unit
def test_the_gate_derives_its_thresholds_from_its_own_matrix() -> None:
    """Taking them as an argument allowed a verdict that reported one matrix's cells against
    another's thresholds, which would look entirely normal."""
    poor = gate(matrix(tuned=0.40, tuned_rag=0.50), **MEASURED)
    checks = {check.name: check for check in poor.checks}
    assert checks["And-Obert +RAG"].measured == 0.50
    assert checks["And-Obert -RAG"].measured == 0.40
    assert not poor.passed
