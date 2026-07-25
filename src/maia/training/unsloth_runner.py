"""The Unsloth trainer — PLAN M3.03, the full run.

M3.02 defined :class:`~maia.training.smoke.Trainer` as a seam and left it empty. This is the
implementation: the real Unsloth wiring, plus the bookkeeping DoD-F3 asks for (*"reproducible YAML,
linked W&B run, cost recorded"*).

The GPU is **blocked-by-resource**, so ``unsloth``, ``trl`` and ``datasets`` are imported inside
:func:`unsloth_trainer` and nowhere else. Everything above that line — how a :class:`TrainingConfig`
becomes Unsloth's arguments, what a checkpoint is called, how loss history is collected, how cost is
computed — is ordinary code and is tested against a fake library.

Four things this does that a transcription of the tutorial would not:

* **``train_on_responses_only`` is applied, not optional.** The plan decides to train on the visible
  response only; skipping that call trains on the prompts too, and the *symptom* is a model that
  parrots questions. :meth:`FakeableTrainer.build` always applies it with M3.01's constants, and
  :class:`UnslothUnavailableError` is raised if the helper is missing rather than proceeding.
* **A checkpoint per epoch, named after the epoch.** M3.04 selects between epochs and *"the best is
  not always the last"*, so a run that only keeps the final weights makes that selection impossible.
* **Cost is recorded from the wall clock**, not estimated — M3.01's estimate is what you use before
  renting a GPU, and this is what you compare it against afterwards.
* **The loss history comes from the trainer's own log**, so `check_loss` sees what W&B saw rather
  than a number this module chose to keep.
"""

from __future__ import annotations

import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

from maia.training.chat import INSTRUCTION_PART, RESPONSE_PART
from maia.training.config import TrainingConfig
from maia.training.smoke import TrainingOutcome

#: Unsloth's gradient-checkpointing mode. ``"unsloth"`` is its own long-context implementation,
#: which the docs recommend for lower VRAM at 12B.
GRADIENT_CHECKPOINTING = "unsloth"

#: 8-bit AdamW: the optimiser state is what runs a 12B QLoRA run out of memory, not the weights.
OPTIMIZER = "adamw_8bit"

#: How often the trainer logs. Every step, because `check_loss` needs a curve and not a summary.
LOGGING_STEPS = 1


class UnslothUnavailableError(RuntimeError):
    """Raised when the installed Unsloth is missing something this module depends on."""


class ModelLoader(Protocol):
    """``unsloth.FastLanguageModel``, narrowed to what is used here."""

    def from_pretrained(
        self, *, model_name: str, max_seq_length: int, load_in_4bit: bool, full_finetuning: bool
    ) -> tuple[Any, Any]:
        """Load a base model and its tokenizer."""

    def get_peft_model(self, model: Any, **kwargs: Any) -> Any:
        """Attach LoRA adapters."""


@dataclass(frozen=True)
class PeftArgs:
    """The LoRA arguments derived from a config, as a plain value so they can be asserted on."""

    r: int
    lora_alpha: int
    lora_dropout: float
    target_modules: tuple[str, ...]
    use_gradient_checkpointing: str
    random_state: int
    max_seq_length: int

    def as_kwargs(self) -> dict[str, Any]:
        """Unsloth's keyword names."""
        return {
            "r": self.r,
            "lora_alpha": self.lora_alpha,
            "lora_dropout": self.lora_dropout,
            "target_modules": list(self.target_modules),
            "use_gradient_checkpointing": self.use_gradient_checkpointing,
            "random_state": self.random_state,
            "max_seq_length": self.max_seq_length,
        }


def peft_args(config: TrainingConfig) -> PeftArgs:
    """Translate a config into Unsloth's LoRA arguments.

    ``random_state`` is the config's ``seed``: LoRA initialisation is part of what makes a run
    reproducible, and leaving it at Unsloth's default would make two runs from the same YAML differ.
    """
    return PeftArgs(
        r=config.r,
        lora_alpha=config.lora_alpha,
        lora_dropout=config.lora_dropout,
        target_modules=config.target_modules,
        use_gradient_checkpointing=GRADIENT_CHECKPOINTING,
        random_state=config.seed,
        max_seq_length=config.max_seq_len,
    )


def sft_kwargs(config: TrainingConfig, *, run_name: str | None = None) -> dict[str, Any]:
    """Translate a config into ``SFTConfig`` arguments.

    ``save_strategy="epoch"`` is the one that matters: M3.04 chooses between epochs, and *"the best
    is not always the last"*, so a run keeping only its final weights makes that selection
    impossible. ``bf16`` follows the config rather than being hardcoded, because a GPU without
    bf16 support has to fall back and the config is where that is recorded.
    """
    return {
        "max_seq_length": config.max_seq_len,
        "per_device_train_batch_size": config.per_device_batch_size,
        "gradient_accumulation_steps": config.gradient_accumulation_steps,
        "num_train_epochs": config.epochs,
        "learning_rate": config.learning_rate,
        "lr_scheduler_type": config.lr_scheduler,
        "warmup_ratio": config.warmup_ratio,
        "logging_steps": LOGGING_STEPS,
        "save_strategy": "epoch",
        "save_total_limit": config.epochs,
        "output_dir": str(config.output_dir / config.name),
        "optim": OPTIMIZER,
        "seed": config.seed,
        "bf16": config.compute_dtype == "bfloat16",
        "fp16": config.compute_dtype == "float16",
        "run_name": run_name or config.name,
        "report_to": "wandb",
    }


def losses_from_log(history: Sequence[dict[str, Any]]) -> tuple[float, ...]:
    """Pull the loss curve out of a trainer's log history.

    Takes what the trainer recorded rather than a number this module kept, so ``check_loss`` sees
    the same curve W&B did. Entries without a ``loss`` (evaluation rows, the final summary) are
    skipped; a numeric ``loss`` that is not a number is an error rather than a silent gap, because a
    missing step would make a diverged run look shorter and healthier than it was.
    """
    curve: list[float] = []
    for index, entry in enumerate(history):
        if "loss" not in entry:
            continue
        value = entry["loss"]
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise UnslothUnavailableError(
                f"log entry {index} has a non-numeric loss {value!r}; refusing to drop it, because "
                "a missing step makes a diverged run look shorter and healthier than it was"
            )
        curve.append(float(value))
    return tuple(curve)


def epoch_checkpoints(config: TrainingConfig) -> list[Path]:
    """Where each epoch's checkpoint is expected, in order.

    Derived from the config rather than discovered, so M3.04 can be handed the list before the run
    finishes and a missing one is visibly missing.
    """
    root = config.output_dir / config.name
    return [root / f"checkpoint-epoch-{epoch}" for epoch in range(1, config.epochs + 1)]


@dataclass
class RunRecord:
    """What a full run produced — the DoD-F3 evidence."""

    config: TrainingConfig
    outcome: TrainingOutcome
    checkpoints: list[Path] = field(default_factory=list)
    eur_per_hour: float = 0.0

    @property
    def cost_eur(self) -> float:
        """Recorded, not estimated: the wall clock times the rate actually paid."""
        return self.outcome.hours * self.eur_per_hour

    @property
    def complete(self) -> bool:
        """Whether every epoch left a checkpoint behind."""
        return len(self.checkpoints) == self.config.epochs


@dataclass
class FakeableTrainer:
    """A trainer built from injected library entry points, so the wiring is testable without a GPU.

    :func:`unsloth_trainer` supplies the real ones.
    """

    loader: ModelLoader
    sft_trainer: Callable[..., Any]
    sft_config: Callable[..., Any]
    responses_only: Callable[..., Any] | None
    eur_per_hour: float = 0.0
    clock: Callable[[], float] = time.monotonic

    def train(self, config: TrainingConfig, rows: Sequence[dict[str, str]]) -> TrainingOutcome:
        """Run one training job and return its loss curve, checkpoint and wall clock."""
        trainer = self.build(config, rows)
        started = self.clock()
        trainer.train()
        hours = (self.clock() - started) / 3_600
        history = getattr(trainer.state, "log_history", [])
        checkpoints = epoch_checkpoints(config)
        return TrainingOutcome(
            losses=losses_from_log(history),
            checkpoint=checkpoints[-1],
            hours=hours,
            run_url=getattr(trainer, "run_url", ""),
        )

    def build(self, config: TrainingConfig, rows: Sequence[dict[str, str]]) -> Any:
        """Assemble model, adapters and trainer — every step derived from ``config``."""
        model, tokenizer = self.loader.from_pretrained(
            model_name=config.base_model,
            max_seq_length=config.max_seq_len,
            load_in_4bit=config.load_in_4bit,
            full_finetuning=False,
        )
        model = self.loader.get_peft_model(model, **peft_args(config).as_kwargs())
        trainer = self.sft_trainer(
            model=model,
            tokenizer=tokenizer,
            train_dataset=list(rows),
            args=self.sft_config(**sft_kwargs(config)),
        )
        if self.responses_only is None:
            raise UnslothUnavailableError(
                "train_on_responses_only is not available in the installed Unsloth; without it the "
                "run trains on the prompts too, and the symptom is a model that parrots questions "
                "rather than answering them"
            )
        return self.responses_only(
            trainer, instruction_part=INSTRUCTION_PART, response_part=RESPONSE_PART
        )


def unsloth_trainer(*, eur_per_hour: float = 0.0) -> FakeableTrainer:
    """The real trainer (blocked-by-resource: needs a GPU, ``unsloth``, ``trl``).

    Imported here and nowhere else, so the module and all of its tests need none of them.
    """
    from trl import SFTConfig, SFTTrainer
    from unsloth import FastLanguageModel
    from unsloth.chat_templates import train_on_responses_only

    return FakeableTrainer(
        loader=FastLanguageModel,
        sft_trainer=SFTTrainer,
        sft_config=SFTConfig,
        responses_only=train_on_responses_only,
        eur_per_hour=eur_per_hour,
    )


def render(record: RunRecord) -> str:
    """Human-readable summary of a full run — the shape DoD-F3 asks to see."""
    lines = [
        f"{record.config.name}: {record.outcome.steps} step(s) in {record.outcome.hours:.2f} h",
        f"  checkpoints: {len(record.checkpoints)}/{record.config.epochs} epoch(s)",
    ]
    for path in record.checkpoints:
        lines.append(f"    {path}")
    if record.eur_per_hour:
        lines.append(
            f"  cost: €{record.cost_eur:.2f} recorded at €{record.eur_per_hour:.2f}/h "
            "(measured, not estimated)"
        )
    else:
        lines.append("  cost: NOT RECORDED — DoD-F3 requires it; pass eur_per_hour")
    if record.outcome.run_url:
        lines.append(f"  W&B: {record.outcome.run_url}")
    else:
        lines.append("  W&B: NOT LINKED — DoD-F3 requires a linked run")
    if not record.complete:
        lines.append(
            "  ✗ an epoch left no checkpoint, so M3.04 cannot choose between epochs — and the best "
            "is not always the last"
        )
    return "\n".join(lines)
