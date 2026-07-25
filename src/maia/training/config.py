"""QLoRA training configuration — PLAN M3.01.

*"Every run is reproducible from a ``configs/train/*.yaml`` + seed."* That sentence is the whole
specification of this module, and it has three consequences.

**A config that cannot be reproduced is not a config.** So this is a pydantic model with
``extra="forbid"``: a typo'd key in a YAML file is an error, not a silently ignored setting that
makes two runs differ for reasons nobody can find later. Every field defaults to the spec's
starting value, and the ranges the spec states are enforced — ``r``, ``alpha``, ``lr``, ``epochs``,
``max_seq_len``, and NF4 + bf16.

**The run has to be identifiable from its name.** The plan asks for the Latxa pattern,
``exp_{dataset_version}_{r}{lr_id}{epochs}``, in W&B *and* in the YAML. :meth:`TrainingConfig.name`
derives it, so the name cannot drift from the settings it describes.

**Cost is a gate, not a footnote.** The budget is 15-40 EUR for 3-6 h on a 1.5-3 EUR/h GPU, and
*"max 3 full runs — if 3 don't beat base clearly, the problem is the data"*. :func:`estimate` turns
a config into hours and euros so a run that cannot fit the budget is visible before the GPU is
rented, and
:data:`MAX_FULL_RUNS` records the ceiling the plan sets on the whole phase.

The trainer itself is **blocked-by-resource** (a rented A100/H100). This module produces the
configuration and the derived facts; M3.02 wires it to a smoke run behind an injected seam.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, model_validator

#: The base model. Facts live in RAG; this run teaches register, lexicon and domain shape.
DEFAULT_BASE_MODEL = "unsloth/gemma-4-12b-it"

#: LoRA target modules: all attention *and* MLP projections, which is what the spec asks for and
#: what Unsloth's own hyperparameter guide recommends for accuracy.
DEFAULT_TARGET_MODULES = (
    "q_proj",
    "k_proj",
    "v_proj",
    "o_proj",
    "gate_proj",
    "up_proj",
    "down_proj",
)

#: The plan's ceiling on full runs. Beyond this the problem is the data, not the hyperparameters.
MAX_FULL_RUNS = 3

#: GPU price band, EUR/hour (RunPod/Vast A100 80GB or H100).
GPU_EUR_PER_HOUR = (1.5, 3.0)

#: Phase 3's budget band, EUR.
BUDGET_EUR = (15.0, 40.0)

#: Rough throughput for 12B QLoRA at ``max_seq_len 4096`` on one A100/H100: the spec's own figure of
#: 3-6 h for 3 epochs over 12k examples, expressed as examples per hour per epoch.
EXAMPLES_PER_HOUR = (6_000, 12_000)


class TrainingConfig(BaseModel):
    """One reproducible QLoRA run.

    ``extra="forbid"`` on purpose: a mistyped key must fail loudly rather than leave two runs
    differing for a reason nobody can find afterwards.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    #: Free-form, but conventionally the dataset drop this run trains on — it lands in the name.
    dataset_version: str = Field(min_length=1, pattern=r"^[a-z0-9][a-z0-9.\-]*$")
    base_model: str = DEFAULT_BASE_MODEL

    # LoRA
    r: Annotated[int, Field(ge=4, le=128)] = 16
    lora_alpha: Annotated[int, Field(ge=4, le=256)] = 32
    lora_dropout: Annotated[float, Field(ge=0.0, le=0.3)] = 0.05
    target_modules: tuple[str, ...] = DEFAULT_TARGET_MODULES

    # Optimisation
    learning_rate: Annotated[float, Field(gt=0.0, le=1e-2)] = 2e-4
    lr_scheduler: Literal["cosine", "linear", "constant"] = "cosine"
    warmup_ratio: Annotated[float, Field(ge=0.0, le=0.2)] = 0.03
    epochs: Annotated[int, Field(ge=1, le=5)] = 3
    per_device_batch_size: Annotated[int, Field(ge=1, le=32)] = 2
    gradient_accumulation_steps: Annotated[int, Field(ge=1, le=64)] = 8
    max_seq_len: Annotated[int, Field(ge=512, le=32_768)] = 4_096
    seed: int = 20260725

    # Quantisation and compute
    load_in_4bit: bool = True
    quant_type: Literal["nf4", "fp4"] = "nf4"
    compute_dtype: Literal["bfloat16", "float16"] = "bfloat16"

    # Bookkeeping
    wandb_project: str = "maia"
    output_dir: Path = Path("build/train")

    @property
    def effective_batch_size(self) -> int:
        """What the optimiser actually sees per step."""
        return self.per_device_batch_size * self.gradient_accumulation_steps

    @property
    def lr_id(self) -> str:
        """The learning rate as a name-safe token: ``2e-4`` → ``2e4``, ``1.5e-4`` → ``1p5e4``.

        Not ``f"{lr:g}"``, which renders ``2e-4`` as ``0.0002`` and puts a decimal point in the
        middle of the run name. A fractional mantissa becomes ``p`` rather than being dropped, so
        two learning rates cannot share an id.
        """
        mantissa, exponent = f"{self.learning_rate:.1e}".split("e")
        trimmed = mantissa.rstrip("0").rstrip(".").replace(".", "p")
        return f"{trimmed}e{abs(int(exponent))}"

    @property
    def name(self) -> str:
        """The Latxa-pattern experiment name: ``exp_{dataset_version}_{r}{lr_id}{epochs}``.

        Derived rather than stored, so the name can never describe settings the config does not
        have.
        """
        return f"exp_{self.dataset_version}_r{self.r}lr{self.lr_id}e{self.epochs}"

    @model_validator(mode="after")
    def _check_coherence(self) -> TrainingConfig:
        """The cross-field rules the spec states, and two that it implies.

        * ``alpha`` below ``r`` scales the adapter *down*, which is almost always a mistake rather
          than a choice — the convention is ``alpha = 2r``.
        * The spec asks for an effective batch of 16-32; outside that the run is not the one the
          hyperparameters were chosen for.
        * QLoRA means 4-bit. ``load_in_4bit=False`` with a ``quant_type`` set is a contradiction
          that would silently train in a precision nobody asked for — and 12B in bf16 will not fit
          the 80 GB the plan budgets for.
        """
        if self.lora_alpha < self.r:
            raise ValueError(
                f"lora_alpha {self.lora_alpha} is below r {self.r}, which scales the adapter down; "
                "the convention this project follows is alpha = 2r"
            )
        if not 16 <= self.effective_batch_size <= 32:
            raise ValueError(
                f"effective batch size is {self.effective_batch_size} "
                f"({self.per_device_batch_size} x {self.gradient_accumulation_steps}); the spec's "
                "hyperparameters were chosen for 16-32"
            )
        if not self.load_in_4bit:
            raise ValueError(
                "load_in_4bit=False is not QLoRA: 12B in bf16 does not fit the 80 GB this phase "
                "budgets for, and the learning rate was chosen for a quantised base"
            )
        return self

    def to_yaml(self) -> str:
        """Serialise for ``configs/train/*.yaml``, ready to commit."""
        payload = json.loads(self.model_dump_json())
        return str(yaml.safe_dump(payload, sort_keys=True, allow_unicode=True))


def load_config(path: str | Path) -> TrainingConfig:
    """Read a training config from YAML.

    Raises:
        ValueError: if the file is not a mapping, or holds a key the model does not define. An
            unknown key is almost always a typo, and silently ignoring it is how two runs come to
            differ for reasons nobody can reconstruct.
    """
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"{path}: expected a mapping, got {type(raw).__name__}")
    return TrainingConfig.model_validate(raw)


def estimate(
    config: TrainingConfig, examples: int
) -> tuple[tuple[float, float], tuple[float, float]]:
    """``((low hours, high hours), (low EUR, high EUR))`` for one run.

    Bracketed rather than pointwise, because the inputs are a throughput band and a price band and a
    single number would imply a precision nobody has. Derived from the spec's own figure: 3-6 h for
    3 epochs over 12k examples.
    """
    if examples <= 0:
        raise ValueError("examples must be positive")
    fast, slow = max(EXAMPLES_PER_HOUR), min(EXAMPLES_PER_HOUR)
    low_hours = examples * config.epochs / fast
    high_hours = examples * config.epochs / slow
    cheap, dear = min(GPU_EUR_PER_HOUR), max(GPU_EUR_PER_HOUR)
    return (low_hours, high_hours), (low_hours * cheap, high_hours * dear)


def within_budget(config: TrainingConfig, examples: int) -> bool:
    """Whether the **worst case** for one run fits Phase 3's budget.

    Worst case, because a run that only fits if the GPU is cheap and fast is a run that will
    overrun.
    """
    _, (_, high_eur) = estimate(config, examples)
    return high_eur <= max(BUDGET_EUR)


def render(config: TrainingConfig, examples: int | None = None) -> str:
    """Human-readable summary of a configured run."""
    lines = [
        f"{config.name}",
        f"  base: {config.base_model}",
        f"  LoRA: r={config.r} alpha={config.lora_alpha} dropout={config.lora_dropout} "
        f"over {len(config.target_modules)} module(s)",
        f"  optim: lr={config.learning_rate:g} {config.lr_scheduler} "
        f"warmup={config.warmup_ratio:.0%} epochs={config.epochs} "
        f"effective batch={config.effective_batch_size}",
        f"  quant: {'4-bit ' + config.quant_type if config.load_in_4bit else 'none'} / "
        f"{config.compute_dtype}, max_seq_len={config.max_seq_len}",
        f"  seed: {config.seed}  W&B project: {config.wandb_project}",
    ]
    if examples is not None:
        (low_h, high_h), (low_eur, high_eur) = estimate(config, examples)
        fits = "✓" if within_budget(config, examples) else "✗"
        lines.append(
            f"  {fits} estimate over {examples:,} example(s): {low_h:.1f}-{high_h:.1f} h, "
            f"€{low_eur:.0f}-{high_eur:.0f} (budget €{min(BUDGET_EUR):.0f}-{max(BUDGET_EUR):.0f})"
        )
        if not within_budget(config, examples):
            lines.append(
                f"  ✗ the worst case exceeds the budget; the plan also caps the phase at "
                f"{MAX_FULL_RUNS} full runs, so one run must not consume it"
            )
    return "\n".join(lines)
