"""Tests for the Unsloth wiring (PLAN M3.03)."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pytest

from maia.training.chat import INSTRUCTION_PART, RESPONSE_PART
from maia.training.config import TrainingConfig
from maia.training.smoke import TrainingOutcome, check_loss
from maia.training.unsloth_runner import (
    GRADIENT_CHECKPOINTING,
    LOGGING_STEPS,
    OPTIMIZER,
    FakeableTrainer,
    RunRecord,
    UnslothUnavailableError,
    epoch_checkpoints,
    losses_from_log,
    peft_args,
    render,
    sft_kwargs,
)


def config(**overrides: object) -> TrainingConfig:
    return TrainingConfig.model_validate({"dataset_version": "v1", **overrides})


@dataclass
class FakeState:
    log_history: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class FakeTrainerObject:
    """What SFTTrainer stands in for."""

    state: FakeState = field(default_factory=FakeState)
    trained: int = 0
    run_url: str = "https://wandb.ai/maia/run/abc"
    masked: dict[str, str] = field(default_factory=dict)

    def train(self) -> None:
        self.trained += 1
        if not self.state.log_history:
            self.state.log_history = [
                {"loss": 2.0, "step": 1},
                {"loss": 1.5, "step": 2},
                {"epoch": 1.0},  # a summary row with no loss
                {"loss": 1.0, "step": 3},
            ]


@dataclass
class FakeLoader:
    """What unsloth.FastLanguageModel stands in for."""

    loaded: dict[str, Any] = field(default_factory=dict)
    peft: dict[str, Any] = field(default_factory=dict)

    def from_pretrained(
        self, *, model_name: str, max_seq_length: int, load_in_4bit: bool, full_finetuning: bool
    ) -> tuple[str, str]:
        self.loaded = {
            "model_name": model_name,
            "max_seq_length": max_seq_length,
            "load_in_4bit": load_in_4bit,
            "full_finetuning": full_finetuning,
        }
        return "model", "tokenizer"

    def get_peft_model(self, model: Any, **kwargs: Any) -> str:
        self.peft = {"model": model, **kwargs}
        return "peft-model"


@dataclass
class Library:
    """The three injected entry points, plus what they were called with."""

    loader: FakeLoader = field(default_factory=FakeLoader)
    trainer_object: FakeTrainerObject = field(default_factory=FakeTrainerObject)
    sft_calls: list[dict[str, Any]] = field(default_factory=list)
    config_calls: list[dict[str, Any]] = field(default_factory=list)
    masking: list[dict[str, str]] = field(default_factory=list)
    with_masking: bool = True

    def sft_trainer(self, **kwargs: Any) -> FakeTrainerObject:
        self.sft_calls.append(kwargs)
        return self.trainer_object

    def sft_config(self, **kwargs: Any) -> dict[str, Any]:
        self.config_calls.append(kwargs)
        return kwargs

    def responses_only(
        self, trainer: FakeTrainerObject, *, instruction_part: str, response_part: str
    ) -> FakeTrainerObject:
        self.masking.append({"instruction": instruction_part, "response": response_part})
        return trainer

    def build(self, *, eur_per_hour: float = 0.0, clock: Any = None) -> FakeableTrainer:
        return FakeableTrainer(
            loader=self.loader,
            sft_trainer=self.sft_trainer,
            sft_config=self.sft_config,
            responses_only=self.responses_only if self.with_masking else None,
            eur_per_hour=eur_per_hour,
            clock=clock or (lambda: 0.0),
        )


ROWS = [{"text": "<start_of_turn>user\nQ<end_of_turn>\n<start_of_turn>model\nA<end_of_turn>\n"}]


# ─────────────────────────────────────────────────────────────
# Config → Unsloth arguments
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_lora_arguments_come_from_the_config() -> None:
    args = peft_args(config(r=32, lora_alpha=64, lora_dropout=0.1))
    assert (args.r, args.lora_alpha, args.lora_dropout) == (32, 64, 0.1)
    assert args.max_seq_length == 4_096
    assert args.use_gradient_checkpointing == GRADIENT_CHECKPOINTING


@pytest.mark.unit
def test_the_lora_seed_is_the_configs_seed() -> None:
    """LoRA initialisation is part of reproducibility; Unsloth's default would break it."""
    assert peft_args(config(seed=1234)).random_state == 1234


@pytest.mark.unit
def test_every_target_module_is_passed_through() -> None:
    kwargs = peft_args(config()).as_kwargs()
    assert kwargs["target_modules"] == [
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
        "gate_proj",
        "up_proj",
        "down_proj",
    ]


@pytest.mark.unit
def test_a_checkpoint_is_saved_every_epoch() -> None:
    """M3.04 chooses between epochs, and the best is not always the last."""
    kwargs = sft_kwargs(config(epochs=3))
    assert kwargs["save_strategy"] == "epoch"
    assert kwargs["save_total_limit"] == 3


@pytest.mark.unit
def test_the_optimiser_arguments_come_from_the_config() -> None:
    kwargs = sft_kwargs(config(learning_rate=1e-4, epochs=2, lr_scheduler="linear"))
    assert kwargs["learning_rate"] == 1e-4
    assert kwargs["num_train_epochs"] == 2
    assert kwargs["lr_scheduler_type"] == "linear"
    assert kwargs["warmup_ratio"] == 0.03
    assert kwargs["optim"] == OPTIMIZER
    assert kwargs["logging_steps"] == LOGGING_STEPS


@pytest.mark.unit
def test_the_precision_flags_follow_the_config_rather_than_being_hardcoded() -> None:
    """A GPU without bf16 support has to fall back, and the config is where that is recorded."""
    bf16 = sft_kwargs(config(compute_dtype="bfloat16"))
    assert bf16["bf16"] and not bf16["fp16"]
    fp16 = sft_kwargs(config(compute_dtype="float16"))
    assert fp16["fp16"] and not fp16["bf16"]


@pytest.mark.unit
def test_the_run_name_defaults_to_the_experiment_name() -> None:
    assert sft_kwargs(config())["run_name"] == config().name
    assert sft_kwargs(config(), run_name="override")["run_name"] == "override"


@pytest.mark.unit
def test_wandb_is_the_reporting_target() -> None:
    """DoD-F3 requires a linked W&B run."""
    assert sft_kwargs(config())["report_to"] == "wandb"


@pytest.mark.unit
def test_the_output_directory_is_namespaced_by_experiment() -> None:
    kwargs = sft_kwargs(config())
    assert kwargs["output_dir"].endswith(config().name)


# ─────────────────────────────────────────────────────────────
# Checkpoints
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_one_checkpoint_path_per_epoch_in_order() -> None:
    paths = epoch_checkpoints(config(epochs=3))
    assert len(paths) == 3
    assert [path.name for path in paths] == [
        "checkpoint-epoch-1",
        "checkpoint-epoch-2",
        "checkpoint-epoch-3",
    ]
    assert all(config().name in str(path) for path in paths)


# ─────────────────────────────────────────────────────────────
# The loss curve
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_curve_is_taken_from_the_trainers_own_log() -> None:
    """So check_loss sees what W&B saw, not a number this module kept."""
    history: list[dict[str, Any]] = [
        {"loss": 2.0},
        {"epoch": 1.0},
        {"loss": 1.0},
        {"train_runtime": 42},
    ]
    assert losses_from_log(history) == (2.0, 1.0)


@pytest.mark.unit
def test_an_empty_log_yields_an_empty_curve() -> None:
    assert losses_from_log([]) == ()
    assert not check_loss(TrainingOutcome(losses=(), checkpoint=Path("x"), hours=1)).passed


@pytest.mark.unit
def test_integers_are_accepted_as_losses() -> None:
    assert losses_from_log([{"loss": 2}, {"loss": 1}]) == (2.0, 1.0)


@pytest.mark.unit
@pytest.mark.parametrize("bad", ["2.0", None, True, [1.0]])
def test_a_non_numeric_loss_is_an_error_not_a_silent_gap(bad: object) -> None:
    """A missing step makes a diverged run look shorter and healthier than it was."""
    with pytest.raises(UnslothUnavailableError, match="non-numeric loss"):
        losses_from_log([{"loss": 2.0}, {"loss": bad}])


# ─────────────────────────────────────────────────────────────
# The assembled trainer
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_model_is_loaded_from_the_config() -> None:
    library = Library()
    library.build().build(config(), ROWS)
    assert library.loader.loaded == {
        "model_name": "unsloth/gemma-4-12b-it",
        "max_seq_length": 4_096,
        "load_in_4bit": True,
        "full_finetuning": False,
    }


@pytest.mark.unit
def test_adapters_are_attached_to_the_loaded_model() -> None:
    library = Library()
    library.build().build(config(), ROWS)
    assert library.loader.peft["model"] == "model"
    assert library.loader.peft["r"] == 16


@pytest.mark.unit
def test_the_trainer_receives_the_adapted_model_and_the_rows() -> None:
    library = Library()
    library.build().build(config(), ROWS)
    call = library.sft_calls[0]
    assert call["model"] == "peft-model"
    assert call["tokenizer"] == "tokenizer"
    assert call["train_dataset"] == ROWS


@pytest.mark.unit
def test_response_only_masking_is_always_applied() -> None:
    """Skipping it trains on the prompts too, and the symptom is a model that parrots questions."""
    library = Library()
    library.build().build(config(), ROWS)
    assert library.masking == [{"instruction": INSTRUCTION_PART, "response": RESPONSE_PART}]


@pytest.mark.unit
def test_a_build_without_the_masking_helper_is_refused() -> None:
    """Rather than quietly proceeding to train on everything."""
    library = Library(with_masking=False)
    with pytest.raises(UnslothUnavailableError, match="parrots questions"):
        library.build().build(config(), ROWS)


# ─────────────────────────────────────────────────────────────
# Running
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_run_returns_the_curve_the_final_checkpoint_and_the_clock() -> None:
    library = Library()
    ticks = iter([0.0, 3_600.0])
    outcome = library.build(clock=lambda: next(ticks)).train(config(epochs=2), ROWS)
    assert outcome.losses == (2.0, 1.5, 1.0)
    assert outcome.hours == pytest.approx(1.0)
    assert outcome.checkpoint == epoch_checkpoints(config(epochs=2))[-1]
    assert outcome.run_url == "https://wandb.ai/maia/run/abc"
    assert library.trainer_object.trained == 1


@pytest.mark.unit
def test_the_outcome_feeds_the_smoke_checks_unchanged() -> None:
    """The two modules meet here: M3.03 produces what M3.02 inspects."""
    library = Library()
    ticks = iter([0.0, 1_800.0])
    outcome = library.build(clock=lambda: next(ticks)).train(config(epochs=1), ROWS)
    assert check_loss(outcome).passed


@pytest.mark.unit
def test_a_trainer_without_a_run_url_reports_none() -> None:
    library = Library(trainer_object=FakeTrainerObject(run_url=""))
    ticks = iter([0.0, 60.0])
    assert library.build(clock=lambda: next(ticks)).train(config(), ROWS).run_url == ""


# ─────────────────────────────────────────────────────────────
# The run record — DoD-F3 evidence
# ─────────────────────────────────────────────────────────────


def record(**overrides: object) -> RunRecord:
    settings = config(epochs=2)
    base = {
        "config": settings,
        "outcome": TrainingOutcome(
            losses=(2.0, 1.0),
            checkpoint=epoch_checkpoints(settings)[-1],
            hours=2.5,
            run_url="https://wandb.ai/maia/run/abc",
        ),
        "checkpoints": epoch_checkpoints(settings),
        "eur_per_hour": 2.0,
    }
    return RunRecord(**{**base, **overrides})  # type: ignore[arg-type]


@pytest.mark.unit
def test_cost_is_recorded_from_the_wall_clock() -> None:
    """M3.01's estimate is what you use before renting; this is what you compare it against."""
    assert record().cost_eur == pytest.approx(5.0)
    assert "€5.00 recorded at €2.00/h" in render(record())
    assert "measured, not estimated" in render(record())


@pytest.mark.unit
def test_an_unrecorded_cost_is_called_out() -> None:
    """DoD-F3 requires it."""
    assert "cost: NOT RECORDED" in render(record(eur_per_hour=0.0))


@pytest.mark.unit
def test_an_unlinked_wandb_run_is_called_out() -> None:
    settings = config(epochs=2)
    unlinked = record(
        outcome=TrainingOutcome(losses=(2.0, 1.0), checkpoint=Path("x"), hours=1.0, run_url="")
    )
    assert "W&B: NOT LINKED" in render(unlinked)
    assert settings.epochs == 2


@pytest.mark.unit
def test_a_run_with_every_epoch_checkpointed_is_complete() -> None:
    assert record().complete
    assert "checkpoints: 2/2 epoch(s)" in render(record())


@pytest.mark.unit
def test_a_missing_epoch_checkpoint_is_a_finding() -> None:
    """M3.04 cannot choose between epochs it does not have."""
    partial = record(checkpoints=epoch_checkpoints(config(epochs=2))[:1])
    assert not partial.complete
    rendered = render(partial)
    assert "✗ an epoch left no checkpoint" in rendered
    assert "the best is not always the last" in rendered


@pytest.mark.unit
def test_the_real_trainer_is_wired_through_the_seam(monkeypatch: pytest.MonkeyPatch) -> None:
    """unsloth and trl are blocked-by-resource, so only the wiring is exercised."""
    import sys
    import types

    unsloth = types.ModuleType("unsloth")
    unsloth.FastLanguageModel = FakeLoader()  # type: ignore[attr-defined]
    templates = types.ModuleType("unsloth.chat_templates")
    templates.train_on_responses_only = lambda trainer, **kwargs: trainer  # type: ignore[attr-defined]
    trl = types.ModuleType("trl")
    trl.SFTTrainer = lambda **kwargs: FakeTrainerObject()  # type: ignore[attr-defined]
    trl.SFTConfig = dict  # type: ignore[attr-defined]
    for name, module in (
        ("unsloth", unsloth),
        ("unsloth.chat_templates", templates),
        ("trl", trl),
    ):
        monkeypatch.setitem(sys.modules, name, module)

    from maia.training.unsloth_runner import unsloth_trainer

    trainer = unsloth_trainer(eur_per_hour=2.5)
    assert trainer.eur_per_hour == 2.5
    assert trainer.responses_only is not None
