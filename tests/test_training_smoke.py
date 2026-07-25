"""Tests for the smoke run (PLAN M3.02)."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from pathlib import Path
from uuid import UUID, uuid5

import pytest

from maia.schemas import DatasetExample, ExampleType, compute_id
from maia.training.chat import RESPONSE_PART, render
from maia.training.config import TrainingConfig
from maia.training.smoke import (
    MAX_HOURS,
    MIN_LOSS_DROP,
    SMOKE_EXAMPLES,
    Check,
    SmokeReport,
    TrainingOutcome,
    check_duration,
    check_generation,
    check_loss,
    check_parity,
    check_stop,
    render_report,
    run_smoke,
)

_NAMESPACE = UUID("6ba7b819-9dad-11d1-80b4-00c04fd430c8")
GROUNDING = compute_id("El Consell General es compon de 28 consellers generals.")

CATALAN = (
    "El Consell General es compon de vint-i-vuit consellers generals, la meitat elegits per "
    "circumscripció parroquial i l'altra meitat per circumscripció nacional del Principat."
)
SPANISH = (
    "El Consejo General se compone de veintiocho consejeros generales, la mitad elegidos por "
    "circunscripción parroquial y la otra mitad por circunscripción nacional del Principado."
)


def example(tag: str = "a") -> DatasetExample:
    return DatasetExample.model_validate(
        {
            "id": str(uuid5(_NAMESPACE, tag)),
            "messages": [
                {"role": "user", "content": f"Quants consellers hi ha? ({tag})"},
                {"role": "assistant", "content": CATALAN},
            ],
            "type": ExampleType.QA.value,
            "topic": "institucions/consell-general",
            "grounding_ids": [GROUNDING],
            "generator": "claude-opus-5",
            "judge_score": 0.9,
            "split": "train",
        }
    )


def config(**overrides: object) -> TrainingConfig:
    return TrainingConfig.model_validate({"dataset_version": "v1", "epochs": 1, **overrides})


def outcome(
    losses: tuple[float, ...] = (2.0, 1.8, 1.5, 1.2, 1.0), hours: float = 0.5
) -> TrainingOutcome:
    return TrainingOutcome(losses=losses, checkpoint=Path("build/ckpt"), hours=hours)


@dataclass
class FakeTrainer:
    """The injected trainer — no GPU."""

    result: TrainingOutcome = field(default_factory=outcome)
    rows: list[dict[str, str]] = field(default_factory=list)
    configs: list[TrainingConfig] = field(default_factory=list)

    def train(self, config_: TrainingConfig, rows: object) -> TrainingOutcome:
        self.configs.append(config_)
        assert isinstance(rows, list)
        self.rows = rows
        return self.result


@dataclass
class FakeEngine:
    """An injected inference backend."""

    name: str = "unsloth"
    answer: str = CATALAN
    prompts: list[str] = field(default_factory=list)

    def generate(self, checkpoint: Path, prompt: str, *, max_new_tokens: int = 128) -> str:
        self.prompts.append(prompt)
        return self.answer


# ─────────────────────────────────────────────────────────────
# Loss
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_falling_loss_passes() -> None:
    check = check_loss(outcome())
    assert check.passed
    # Windowed: the five-step history averages to 1.9 at the start and 1.1 at the end.
    assert "1.9000 → 1.1000" in check.detail
    assert "42.1% drop" in check.detail


@pytest.mark.unit
def test_a_flat_loss_fails() -> None:
    """Frozen adapters or a zero learning rate: the run finished, cost money, taught nothing."""
    check = check_loss(outcome(losses=(1.5,) * 10))
    assert not check.passed
    assert "0.0% drop" in check.detail


@pytest.mark.unit
def test_a_loss_that_is_zero_everywhere_fails_loudly() -> None:
    """Not a miracle — the response mask matched nothing."""
    check = check_loss(outcome(losses=(0.0,) * 10))
    assert not check.passed
    assert "mask matched nothing" in check.detail
    assert "INSTRUCTION_PART" in check.detail


@pytest.mark.unit
@pytest.mark.parametrize("bad", [math.nan, math.inf, -math.inf])
def test_a_non_finite_loss_fails_whatever_it_ended_on(bad: float) -> None:
    """A diverged run can end on a small-looking value after a NaN."""
    check = check_loss(outcome(losses=(2.0, bad, 0.1, 0.1, 0.1)))
    assert not check.passed
    assert "diverged" in check.detail


@pytest.mark.unit
def test_no_loss_history_fails() -> None:
    assert not check_loss(outcome(losses=())).passed


@pytest.mark.unit
def test_a_rising_loss_fails() -> None:
    assert not check_loss(outcome(losses=(1.0, 1.2, 1.5, 1.8, 2.0))).passed


@pytest.mark.unit
def test_the_drop_threshold_is_configurable() -> None:
    small = outcome(losses=(1.0, 0.98, 0.96, 0.95, 0.95))
    assert not check_loss(small).passed
    assert check_loss(small, min_drop=0.01).passed
    assert MIN_LOSS_DROP == 0.10


@pytest.mark.unit
def test_the_window_averages_rather_than_trusting_one_step() -> None:
    """A single noisy final step must not decide the verdict."""
    noisy = outcome(losses=(2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 5.0))
    assert check_loss(noisy, window=3).passed is False  # the spike is inside the window
    assert check_loss(noisy, window=2).passed is False


@pytest.mark.unit
def test_a_two_step_run_still_compares() -> None:
    check = check_loss(outcome(losses=(2.0, 1.0)))
    assert check.passed
    assert "2 step(s)" in check.detail


@pytest.mark.unit
def test_a_negative_initial_loss_is_refused() -> None:
    check = check_loss(outcome(losses=(-1.0, -2.0)))
    assert not check.passed
    assert "nothing to fall from" in check.detail


# ─────────────────────────────────────────────────────────────
# Duration
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_run_inside_the_hour_passes() -> None:
    assert check_duration(outcome(hours=0.8)).passed
    assert MAX_HOURS == 1.0


@pytest.mark.unit
def test_a_run_that_is_not_a_smoke_run_any_more_fails() -> None:
    """One that takes four hours cannot be used to iterate, which is why it exists."""
    check = check_duration(outcome(hours=4.0))
    assert not check.passed
    assert "4.00 h" in check.detail


# ─────────────────────────────────────────────────────────────
# Generation
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_coherent_catalan_passes() -> None:
    check = check_generation(FakeEngine(), Path("ckpt"), [example()])
    assert check.passed
    assert "coherent Catalan" in check.detail


@pytest.mark.unit
def test_a_checkpoint_answering_in_spanish_fails() -> None:
    """The same judgement the corpus was built with, not a second opinion."""
    check = check_generation(FakeEngine(answer=SPANISH), Path("ckpt"), [example()])
    assert not check.passed
    assert "not Catalan" in check.detail


@pytest.mark.unit
def test_an_empty_generation_fails() -> None:
    check = check_generation(FakeEngine(answer="   "), Path("ckpt"), [example()])
    assert not check.passed
    assert "empty generation" in check.detail


@pytest.mark.unit
def test_a_generation_too_short_to_judge_fails() -> None:
    """Below the floor, language detection is guessing and a pass would mean nothing."""
    check = check_generation(FakeEngine(answer="Sí."), Path("ckpt"), [example()])
    assert not check.passed
    assert "too short to judge" in check.detail


@pytest.mark.unit
def test_the_generation_prompt_is_chat_templated() -> None:
    engine = FakeEngine()
    check_generation(engine, Path("ckpt"), [example()])
    assert engine.prompts[0] == render(example(), add_generation_prompt=True)
    assert engine.prompts[0].endswith(RESPONSE_PART)


@pytest.mark.unit
def test_generation_without_an_engine_does_not_run() -> None:
    check = check_generation(None, Path("ckpt"), [example()])
    assert not check.ran
    assert not check.passed
    assert "NOT RUN" in check.detail


@pytest.mark.unit
def test_generation_without_prompts_fails() -> None:
    assert not check_generation(FakeEngine(), Path("ckpt"), []).passed


# ─────────────────────────────────────────────────────────────
# Stopping
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_checkpoint_that_stops_passes() -> None:
    assert check_stop(FakeEngine(), Path("ckpt"), [example()]).passed


@pytest.mark.unit
def test_a_checkpoint_that_starts_a_new_turn_fails() -> None:
    """A failure that looks like verbosity and survives every quality eval as "it rambles"."""
    runaway = FakeEngine(answer=f"{CATALAN}<end_of_turn>\n{RESPONSE_PART}I encara més...")
    check = check_stop(runaway, Path("ckpt"), [example()])
    assert not check.passed
    assert "did not learn" in check.detail


@pytest.mark.unit
def test_stopping_without_an_engine_does_not_run() -> None:
    assert not check_stop(None, Path("ckpt"), [example()]).ran


# ─────────────────────────────────────────────────────────────
# Engine parity — the check the spec singles out
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_two_agreeing_engines_pass() -> None:
    engines = [FakeEngine(name="unsloth"), FakeEngine(name="transformers")]
    check = check_parity(engines, Path("ckpt"), [example()])
    assert check.passed
    assert "unsloth, transformers agree" in check.detail


@pytest.mark.unit
def test_two_disagreeing_engines_fail_and_show_both() -> None:
    """A template or EOS mismatch is invisible in either backend alone."""
    engines = [
        FakeEngine(name="unsloth", answer=CATALAN),
        FakeEngine(name="transformers", answer=CATALAN + " I una cosa més."),
    ]
    check = check_parity(engines, Path("ckpt"), [example()])
    assert not check.passed
    assert "disagree on the same prompt" in check.detail
    assert "transformers:" in check.detail
    assert "unsloth:" in check.detail


@pytest.mark.unit
def test_one_engine_cannot_check_parity() -> None:
    """Which is the whole point: a mismatch looks fine from inside one backend."""
    check = check_parity([FakeEngine()], Path("ckpt"), [example()])
    assert not check.ran
    assert "needs two engines" in check.detail


@pytest.mark.unit
def test_no_engines_cannot_check_parity() -> None:
    assert not check_parity([], Path("ckpt"), [example()]).ran


@pytest.mark.unit
def test_parity_is_checked_on_every_prompt() -> None:
    engines = [FakeEngine(name="a"), FakeEngine(name="b")]
    check_parity(engines, Path("ckpt"), [example("1"), example("2"), example("3")])
    assert len(engines[0].prompts) == 3


# ─────────────────────────────────────────────────────────────
# The whole run
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_healthy_smoke_run_passes_every_check() -> None:
    trainer = FakeTrainer()
    engines = [FakeEngine(name="unsloth"), FakeEngine(name="transformers")]
    report = run_smoke(config(), [example(str(i)) for i in range(5)], trainer, engines=engines)
    assert report.passed
    assert report.skipped == []
    assert len(report.checks) == 5
    rendered = render_report(report)
    assert "✓ PASS" in rendered
    assert "the full run (M3.03) may proceed" in rendered


@pytest.mark.unit
def test_the_trainer_receives_chat_templated_rows() -> None:
    trainer = FakeTrainer()
    run_smoke(config(), [example()], trainer)
    assert trainer.rows == [{"text": render(example())}]
    assert trainer.configs[0].epochs == 1


@pytest.mark.unit
def test_a_run_with_no_engines_fails_because_nothing_was_verified() -> None:
    """A smoke run that verified nothing is an unrun smoke run, not a green one."""
    report = run_smoke(config(), [example()], FakeTrainer())
    assert not report.passed
    assert set(report.skipped) == {"generation", "stop", "engine parity"}
    rendered = render_report(report)
    assert "✗ FAIL" in rendered
    assert "is not a passing smoke run" in rendered


@pytest.mark.unit
def test_one_engine_verifies_generation_but_not_parity() -> None:
    report = run_smoke(config(), [example()], FakeTrainer(), engines=[FakeEngine()])
    assert report.skipped == ["engine parity"]
    assert not report.passed


@pytest.mark.unit
def test_a_failing_loss_fails_the_run() -> None:
    trainer = FakeTrainer(result=outcome(losses=(1.0,) * 10))
    engines = [FakeEngine(name="a"), FakeEngine(name="b")]
    report = run_smoke(config(), [example()], trainer, engines=engines)
    assert not report.passed
    assert "✗ loss" in render_report(report)


@pytest.mark.unit
def test_a_multi_epoch_config_is_not_a_smoke_run() -> None:
    with pytest.raises(ValueError, match="a smoke run is one epoch"):
        run_smoke(config(epochs=3), [example()], FakeTrainer())


@pytest.mark.unit
def test_a_smoke_run_needs_examples() -> None:
    with pytest.raises(ValueError, match="needs examples"):
        run_smoke(config(), [], FakeTrainer())


@pytest.mark.unit
def test_probes_default_to_the_first_three_examples() -> None:
    engine = FakeEngine()
    run_smoke(config(), [example(str(i)) for i in range(10)], FakeTrainer(), engines=[engine])
    # generation and stop each generate once per probe.
    assert len(engine.prompts) == 6


@pytest.mark.unit
def test_probes_can_be_supplied_explicitly() -> None:
    engine = FakeEngine()
    run_smoke(
        config(),
        [example(str(i)) for i in range(10)],
        FakeTrainer(),
        engines=[engine],
        probes=[example("probe")],
    )
    assert len(engine.prompts) == 2
    assert "probe" in engine.prompts[0]


@pytest.mark.unit
def test_the_report_links_the_wandb_run() -> None:
    trainer = FakeTrainer(
        result=TrainingOutcome(
            losses=(2.0, 1.0), checkpoint=Path("ckpt"), hours=0.4, run_url="https://wandb.ai/x/y/z"
        )
    )
    report = run_smoke(config(), [example()], trainer, engines=[FakeEngine()])
    assert "https://wandb.ai/x/y/z" in render_report(report)


@pytest.mark.unit
def test_an_empty_report_does_not_pass() -> None:
    assert not SmokeReport(config_name="x", examples=0).passed


@pytest.mark.unit
def test_a_not_run_check_is_never_a_pass() -> None:
    check = Check.not_run("something", "no backend")
    assert not check.passed
    assert not check.ran


@pytest.mark.unit
def test_the_smoke_size_is_the_plans() -> None:
    assert SMOKE_EXAMPLES == 500
