"""Tests for merge, quantisation and the Modelfile (PLAN M5.05)."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pytest

from maia.serving.quantize import (
    DISCLAIMER,
    MERGE_PROMPTS,
    MIN_RETENTION,
    IncomparableError,
    LocalRun,
    MergeCheck,
    Quant,
    QuantReport,
    QuantScore,
    build_modelfile,
    check_merge,
    check_modelfile,
    check_retention,
    quantise,
    render,
)
from maia.training.chat import END_OF_TURN, START_OF_TURN

HARNESS = "andbench-1.0.0"
PROMPTS = [f"Pregunta {index} sobre Andorra?" for index in range(MERGE_PROMPTS)]


@dataclass
class Fixed:
    """Answers deterministically from the prompt, optionally diverging on some."""

    suffix: str = ""
    diverge_on: set[str] = field(default_factory=set)

    def generate(self, prompt: str) -> str:
        base = f"Resposta a {prompt}"
        return f"{base}{self.suffix}" if prompt in self.diverge_on else base


def score(
    value: float, *, quant: Quant | None = None, harness: str = HARNESS, items: int = 100
) -> QuantScore:
    return QuantScore(quant=quant, score=value, harness_version=harness, items=items)


# ─────────────────────────────────────────────────────────────
# Merging must be a no-op
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_an_identical_merge_passes() -> None:
    check = check_merge(Fixed(), Fixed(), PROMPTS)
    assert check.passed
    assert check.identical == MERGE_PROMPTS
    assert f"{MERGE_PROMPTS}/{MERGE_PROMPTS} identical" in render(QuantReport(merge=check))


@pytest.mark.unit
def test_a_divergence_names_the_prompt() -> None:
    """One in twenty is a precision problem; twenty in twenty is a broken merge."""
    check = check_merge(Fixed(), Fixed(suffix=" (!)", diverge_on={PROMPTS[3]}), PROMPTS)
    assert not check.passed
    assert len(check.divergent) == 1
    assert check.divergent[0][0] == PROMPTS[3]
    rendered = render(QuantReport(merge=check))
    assert "1/20 diverged" in rendered
    assert PROMPTS[3][:20] in rendered


@pytest.mark.unit
def test_too_few_prompts_does_not_pass_even_when_identical() -> None:
    """Every number M4 measured describes the model it measured."""
    check = check_merge(Fixed(), Fixed(), PROMPTS[:5])
    assert not check.divergent
    assert not check.passed
    assert f"the plan asks for {MERGE_PROMPTS}" in render(QuantReport(merge=check))


@pytest.mark.unit
def test_a_merge_check_over_nothing_is_refused() -> None:
    """Over no prompts it would pass trivially, which is what this module exists to avoid."""
    with pytest.raises(ValueError, match="pass trivially"):
        check_merge(Fixed(), Fixed(), [])


@pytest.mark.unit
def test_an_unchecked_merge_is_reported_as_such() -> None:
    rendered = render(QuantReport())
    assert "merge equality: NOT CHECKED" in rendered
    assert "different model than M4 evaluated" in rendered


# ─────────────────────────────────────────────────────────────
# Retention
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_q4_retaining_enough_passes() -> None:
    retention = check_retention(score(0.80), score(0.77, quant=Quant.Q4_K_M))
    assert retention.retained == pytest.approx(0.9625)
    assert retention.passed
    assert MIN_RETENTION == 0.95


@pytest.mark.unit
def test_q4_losing_too_much_fails() -> None:
    retention = check_retention(score(0.80), score(0.70, quant=Quant.Q4_K_M))
    assert not retention.passed
    report = QuantReport(retention={Quant.Q4_K_M: retention})
    assert "✗ Q4_K_M: retains 87.5%" in render(report)
    assert "gate ≥95%" in render(report)


@pytest.mark.unit
def test_only_q4_is_gated() -> None:
    assert Quant.Q4_K_M.gated
    assert not Quant.Q8_0.gated
    report = QuantReport(
        retention={Quant.Q8_0: check_retention(score(0.80), score(0.60, quant=Quant.Q8_0))}
    )
    assert "· Q8_0" in render(report)
    assert "not gated" in render(report)


@pytest.mark.unit
def test_scores_from_different_harness_runs_are_not_comparable() -> None:
    """A Q4 score from a newer AndBench is a different measurement, not a smaller number."""
    with pytest.raises(IncomparableError, match="a different measurement"):
        check_retention(score(0.80), score(0.77, harness="andbench-2.0.0"))


@pytest.mark.unit
def test_scores_over_different_item_counts_are_not_comparable() -> None:
    with pytest.raises(IncomparableError, match="re-run both"):
        check_retention(score(0.80), score(0.77, items=50))


@pytest.mark.unit
def test_a_merged_model_scoring_zero_leaves_nothing_to_retain() -> None:
    with pytest.raises(ValueError, match="nothing to retain"):
        check_retention(score(0.0), score(0.0))


@pytest.mark.unit
def test_a_score_without_a_harness_version_is_refused() -> None:
    with pytest.raises(ValueError, match="cannot be shown to be comparable"):
        score(0.8, harness="")


@pytest.mark.unit
@pytest.mark.parametrize("value", [-0.1, 1.5])
def test_a_score_outside_the_unit_range_is_refused(value: float) -> None:
    with pytest.raises(ValueError, match=r"outside 0\.0-1\.0"):
        score(value)


@pytest.mark.unit
def test_an_unmeasured_q4_is_reported_as_required() -> None:
    assert "Q4_K_M: NOT MEASURED — DoD-F5 requires it" in render(QuantReport())


# ─────────────────────────────────────────────────────────────
# The Modelfile carries the training template
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_modelfile_embeds_the_training_template() -> None:
    """Ollama applies its own otherwise, and the model is worse only when served there."""
    modelfile = build_modelfile(Path("maia.gguf"), system="Ets MAIA.")
    assert "TEMPLATE" in modelfile
    assert START_OF_TURN in modelfile
    assert END_OF_TURN in modelfile
    assert "model\n" in modelfile
    assert check_modelfile(modelfile) == []


@pytest.mark.unit
def test_the_modelfile_carries_the_legal_disclaimer() -> None:
    """Andorran law in the training data is exactly what invites the mistake."""
    modelfile = build_modelfile(Path("maia.gguf"), system="Ets MAIA.")
    assert DISCLAIMER in modelfile
    assert "assessorament jurídic" in modelfile


@pytest.mark.unit
def test_the_modelfile_stops_at_the_turn_marker() -> None:
    modelfile = build_modelfile(Path("maia.gguf"), system="Ets MAIA.")
    assert f'PARAMETER stop "{END_OF_TURN}"' in modelfile


@pytest.mark.unit
@pytest.mark.parametrize(
    ("removed", "expected"),
    [
        ("TEMPLATE", "TEMPLATE"),
        ("SYSTEM", "SYSTEM"),
        ("PARAMETER stop", "stop parameter"),
    ],
)
def test_a_modelfile_missing_a_required_directive_is_caught(removed: str, expected: str) -> None:
    """So an edit cannot quietly drop something that fails silently rather than loudly."""
    modelfile = build_modelfile(Path("maia.gguf"), system="Ets MAIA.")
    stripped = "\n".join(line for line in modelfile.splitlines() if removed not in line)
    problems = check_modelfile(stripped)
    assert any(expected in problem for problem in problems)


@pytest.mark.unit
def test_a_modelfile_without_the_disclaimer_is_caught() -> None:
    problems = check_modelfile(build_modelfile(Path("m.gguf"), system="x").replace(DISCLAIMER, ""))
    assert any("disclaimer" in problem for problem in problems)


@pytest.mark.unit
def test_a_modelfile_with_the_wrong_turn_markers_is_caught() -> None:
    modelfile = build_modelfile(Path("m.gguf"), system="x").replace(START_OF_TURN, "<|im_start|>")
    assert any("turn markers" in problem for problem in check_modelfile(modelfile))


@pytest.mark.unit
def test_the_modelfile_records_the_size_for_the_16gb_claim() -> None:
    modelfile = build_modelfile(Path("m.gguf"), system="x", quant=Quant.Q4_K_M)
    assert "16 GB machine" in modelfile
    assert Quant.Q4_K_M.approximate_gib < 16


# ─────────────────────────────────────────────────────────────
# The local run
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_run_inside_16gb_passes_with_room_for_an_os() -> None:
    run = LocalRun(quant=Quant.Q4_K_M, load_seconds=25.0, tokens_per_second=12.0, ram_gib=9.0)
    assert run.fits_16gb
    assert run.usable
    assert "9.0 GiB, 25s load, 12.0 tok/s" in render(QuantReport(local=run))


@pytest.mark.unit
def test_a_run_that_does_not_fit_fails() -> None:
    run = LocalRun(quant=Quant.Q8_0, load_seconds=40.0, tokens_per_second=8.0, ram_gib=15.5)
    assert not run.fits_16gb
    assert "✗ local" in render(QuantReport(local=run))


@pytest.mark.unit
def test_throughput_below_reading_speed_is_flagged() -> None:
    """A local demo feels broken below ~5 tok/s even when it is working."""
    run = LocalRun(quant=Quant.Q4_K_M, load_seconds=30.0, tokens_per_second=2.0, ram_gib=9.0)
    assert run.fits_16gb
    assert not run.usable
    assert "feels broken even when it works" in render(QuantReport(local=run))


@pytest.mark.unit
def test_an_untested_local_run_is_reported_as_required() -> None:
    assert "16 GB machine: NOT TESTED — DoD-F5 requires it" in render(QuantReport())


# ─────────────────────────────────────────────────────────────
# The gate
# ─────────────────────────────────────────────────────────────


def complete_report() -> QuantReport:
    return QuantReport(
        merge=check_merge(Fixed(), Fixed(), PROMPTS),
        retention={
            Quant.Q4_K_M: check_retention(score(0.80), score(0.78, quant=Quant.Q4_K_M)),
            Quant.Q8_0: check_retention(score(0.80), score(0.795, quant=Quant.Q8_0)),
        },
        local=LocalRun(quant=Quant.Q4_K_M, load_seconds=25.0, tokens_per_second=12.0, ram_gib=9.0),
    )


@pytest.mark.unit
def test_a_complete_gate_passes() -> None:
    report = complete_report()
    assert report.passed
    assert "✓ PASS — F5 quantisation" in render(report)


@pytest.mark.unit
def test_a_missing_check_is_a_failure_not_a_pass() -> None:
    """This is the last gate before a public artifact."""
    report = complete_report()
    report.merge = None
    assert not report.passed

    report = complete_report()
    report.local = None
    assert not report.passed

    report = complete_report()
    report.retention = {}
    assert not report.passed


@pytest.mark.unit
def test_a_modelfile_problem_fails_the_gate() -> None:
    report = complete_report()
    report.modelfile_problems = ["TEMPLATE — without it Ollama applies its own"]
    assert not report.passed
    assert "Modelfile is missing TEMPLATE" in render(report)


# ─────────────────────────────────────────────────────────────
# Producing the files
# ─────────────────────────────────────────────────────────────


@dataclass
class FakeQuantizer:
    calls: list[tuple[Path, Path, str]] = field(default_factory=list)

    def convert(self, model_dir: Path, out: Path, *, quant: str) -> Path:
        self.calls.append((model_dir, out, quant))
        return out


@pytest.mark.unit
def test_both_quantisations_are_produced(tmp_path: Path) -> None:
    quantizer = FakeQuantizer()
    produced = quantise(tmp_path / "merged", quantizer, tmp_path / "gguf")
    assert set(produced) == set(Quant)
    assert produced[Quant.Q4_K_M].name == "maia-12b-Q4_K_M.gguf"
    assert [call[2] for call in quantizer.calls] == ["Q4_K_M", "Q8_0"]


@pytest.mark.unit
def test_requesting_no_quantisation_is_refused(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="no quantisation requested"):
        quantise(tmp_path, FakeQuantizer(), tmp_path, quants=[])


@pytest.mark.unit
def test_a_single_quantisation_can_be_requested(tmp_path: Path) -> None:
    produced = quantise(tmp_path, FakeQuantizer(), tmp_path, quants=[Quant.Q8_0])
    assert set(produced) == {Quant.Q8_0}


@pytest.mark.unit
def test_an_empty_merge_check_reports_no_divergence() -> None:
    assert MergeCheck().identical == 0
    assert not MergeCheck().passed


@pytest.mark.unit
def test_the_committed_modelfile_is_complete() -> None:
    """`deploy/Modelfile` is what Ollama loads, so it must not drift from the generator."""
    committed = Path(__file__).resolve().parents[1] / "deploy" / "Modelfile"
    assert committed.is_file()
    assert check_modelfile(committed.read_text(encoding="utf-8")) == []
