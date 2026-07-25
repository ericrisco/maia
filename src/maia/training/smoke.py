"""The smoke run — PLAN M3.02.

*"500 examples, verifies the whole pipeline (data→train→checkpoint→W&B) in <1 h. Done = loss drops,
checkpoint generates coherent Catalan, and an inference with the same chat template + EOS as
training gives identical output in Unsloth and transformers."*

The point of a smoke run is not quality, it is **finding out that the pipeline is wrong before
spending the real budget on it**. So this module is the three checks the spec lists, each written to
catch a specific failure that otherwise surfaces hours later as "the model is somehow worse":

1. **Loss dropped.** :func:`check_loss` refuses three shapes that all *look* like training happened:
   a loss that never moves, a ``NaN``/``inf`` (a diverged run whose final number can still be
   small), and a loss that is **exactly zero from the first step** — which is not a miracle, it is
   the mask matching nothing, and it is the failure Unsloth's own troubleshooting page warns about
   for chat models.
2. **The checkpoint speaks Catalan.** :func:`check_generation` reuses M1's language detector, so
   "coherent Catalan" is the same judgement the corpus was built with rather than a new opinion. A
   checkpoint that emits Spanish, or empty strings, or the prompt back, fails here.
3. **Two engines agree.** :func:`check_parity` runs the *same* prompt through two inference backends
   and compares. This is the check the spec singles out, and the reason is that a template or EOS
   mismatch is invisible in any single backend — both look fine on their own.

Every backend is **blocked-by-resource**: a GPU for the trainer, a loaded model for each engine.
:class:`Trainer` and :class:`Engine` are the seams. A check whose backend was not supplied reports
``NOT RUN`` and the gate **fails**, because a smoke run that verified nothing is not a passing smoke
run — it is an unrun one.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

from maia.corpus.language import is_catalan
from maia.schemas import DatasetExample
from maia.training.chat import (
    END_OF_TURN,
    RESPONSE_PART,
    format_dataset,
    render,
)
from maia.training.config import TrainingConfig

#: The plan's smoke size.
SMOKE_EXAMPLES = 500

#: The plan's wall-clock ceiling for a smoke run, in hours. Longer means it is not a smoke run.
MAX_HOURS = 1.0

#: Loss must fall by at least this fraction of its starting value. Not a quality bar — a run that
#: barely moves has usually failed to train at all (frozen adapters, zero learning rate).
MIN_LOSS_DROP = 0.10

#: How many steps at each end are averaged when comparing. A single step is noise.
WINDOW = 5

#: Minimum characters a generated sample must have to be judged. Below this, language detection is
#: guessing and a "pass" would mean nothing.
MIN_SAMPLE_CHARS = 40


@dataclass(frozen=True)
class TrainingOutcome:
    """What a training run reports back."""

    losses: tuple[float, ...]
    checkpoint: Path
    hours: float
    run_url: str = ""

    @property
    def steps(self) -> int:
        """How many optimiser steps were recorded."""
        return len(self.losses)


class Trainer(Protocol):
    """Runs one training job. Blocked-by-resource: needs a rented GPU."""

    def train(self, config: TrainingConfig, rows: Sequence[dict[str, str]]) -> TrainingOutcome:
        """Train on pre-formatted rows and return the loss history and checkpoint."""


class Engine(Protocol):
    """An inference backend — Unsloth or transformers. Blocked-by-resource: loads the model."""

    @property
    def name(self) -> str:
        """Which backend this is, for the report."""

    def generate(self, checkpoint: Path, prompt: str, *, max_new_tokens: int = 128) -> str:
        """Continue ``prompt``, which is already chat-templated."""


@dataclass(frozen=True)
class Check:
    """One smoke check."""

    name: str
    passed: bool
    detail: str
    ran: bool = True

    @classmethod
    def not_run(cls, name: str, reason: str) -> Check:
        """A check whose backend was not supplied. Never a pass."""
        return cls(name=name, passed=False, detail=f"NOT RUN — {reason}", ran=False)


def check_loss(
    outcome: TrainingOutcome, *, min_drop: float = MIN_LOSS_DROP, window: int = WINDOW
) -> Check:
    """Whether the loss actually fell.

    Three shapes are refused because each one *looks* like training happened:

    * **Not a number.** A diverged run can end on a small-looking value after a ``NaN``, so any
      non-finite loss anywhere fails rather than being averaged away.
    * **Exactly zero from the start.** Not a miracle — the response mask matched nothing, so there
      were no tokens to compute loss over. Unsloth's troubleshooting page names this for chat
      models, and it is silent otherwise.
    * **Barely moved.** Frozen adapters or a zero learning rate produce a flat curve; the run
      finished, cost money, and taught nothing.
    """
    if not outcome.losses:
        return Check("loss", False, "no loss history was recorded")
    if any(not math.isfinite(value) for value in outcome.losses):
        return Check(
            "loss", False, "loss contains NaN or inf — the run diverged, whatever it ended on"
        )
    if all(value == 0.0 for value in outcome.losses):
        return Check(
            "loss",
            False,
            "loss is exactly 0.0 at every step: the response mask matched nothing, so there were "
            "no tokens to train on (check INSTRUCTION_PART/RESPONSE_PART against the template)",
        )
    span = min(window, max(1, len(outcome.losses) // 2))
    first = sum(outcome.losses[:span]) / span
    last = sum(outcome.losses[-span:]) / span
    if first <= 0:
        return Check("loss", False, f"initial loss is {first:.4f}; nothing to fall from")
    drop = (first - last) / first
    passed = drop >= min_drop
    return Check(
        "loss",
        passed,
        f"{first:.4f} → {last:.4f} over {outcome.steps} step(s), a {drop:.1%} drop "
        f"(need ≥{min_drop:.0%})",
    )


def check_duration(outcome: TrainingOutcome, *, max_hours: float = MAX_HOURS) -> Check:
    """Whether the run stayed inside the smoke budget.

    Not a quality signal: it is the check that the *smoke* run is still a smoke run. One that takes
    four hours cannot be used to iterate, which is the only reason it exists.
    """
    passed = outcome.hours <= max_hours
    return Check(
        "duration",
        passed,
        f"{outcome.hours:.2f} h (ceiling {max_hours:g} h)",
    )


def check_generation(
    engine: Engine | None,
    checkpoint: Path,
    prompts: Sequence[DatasetExample],
) -> Check:
    """Whether the checkpoint produces coherent Catalan.

    Reuses M1's :func:`is_catalan`, so "coherent Catalan" is the same judgement the corpus was built
    with rather than a second opinion that could disagree with it. Catches the three ways a broken
    checkpoint answers: empty, too short to judge, or another language.
    """
    if engine is None:
        return Check.not_run("generation", "no inference engine supplied")
    if not prompts:
        return Check("generation", False, "no prompts to generate from")

    failures: list[str] = []
    for example in prompts:
        prompt = render(example, add_generation_prompt=True)
        answer = engine.generate(checkpoint, prompt).strip()
        if not answer:
            failures.append("empty generation")
        elif len(answer) < MIN_SAMPLE_CHARS:
            failures.append(f"only {len(answer)} char(s), too short to judge: {answer!r}")
        elif not is_catalan(answer):
            failures.append(f"not Catalan: {answer[:80]!r}")
    if failures:
        return Check(
            "generation",
            False,
            f"{len(failures)}/{len(prompts)} sample(s) failed — " + "; ".join(failures[:3]),
        )
    return Check("generation", True, f"{len(prompts)} sample(s) in coherent Catalan")


def check_stop(engine: Engine | None, checkpoint: Path, prompts: Sequence[DatasetExample]) -> Check:
    """Whether the checkpoint stops.

    A model trained with the terminator outside its loss mask keeps generating past the end of its
    answer — a failure that looks like verbosity rather than like a bug, and that survives every
    quality eval as "the model rambles".
    """
    if engine is None:
        return Check.not_run("stop", "no inference engine supplied")
    runaway = [
        example
        for example in prompts
        if RESPONSE_PART in engine.generate(checkpoint, render(example, add_generation_prompt=True))
    ]
    if runaway:
        return Check(
            "stop",
            False,
            f"{len(runaway)} sample(s) generated a new turn instead of stopping — the model did "
            f"not learn {END_OF_TURN}",
        )
    return Check("stop", True, f"{len(prompts)} sample(s) stopped at the end of their turn")


def check_parity(
    engines: Sequence[Engine], checkpoint: Path, prompts: Sequence[DatasetExample]
) -> Check:
    """Whether two inference backends produce identical output.

    The check the spec singles out, and the reason it needs two backends: a template or EOS mismatch
    is invisible in any single one — both look fine on their own, and the disagreement only appears
    when the same prompt is put through both.
    """
    if len(engines) < 2:
        return Check.not_run(
            "engine parity",
            f"needs two engines, got {len(engines)} — a mismatch is invisible in one backend",
        )
    for example in prompts:
        prompt = render(example, add_generation_prompt=True)
        answers = {engine.name: engine.generate(checkpoint, prompt) for engine in engines}
        distinct = set(answers.values())
        if len(distinct) > 1:
            first, second = sorted(answers)
            return Check(
                "engine parity",
                False,
                f"{first} and {second} disagree on the same prompt:\n"
                f"    {first}: {answers[first][:80]!r}\n"
                f"    {second}: {answers[second][:80]!r}\n"
                "    a chat-template or EOS mismatch is invisible in either backend alone",
            )
    return Check(
        "engine parity",
        True,
        f"{', '.join(engine.name for engine in engines)} agree on {len(prompts)} prompt(s)",
    )


@dataclass
class SmokeReport:
    """The outcome of a smoke run."""

    config_name: str
    examples: int
    checks: list[Check] = field(default_factory=list)
    outcome: TrainingOutcome | None = None

    @property
    def passed(self) -> bool:
        """Whether every check ran **and** passed.

        A check that did not run is not a pass: a smoke run that verified nothing is an unrun smoke
        run, and treating it as green is how a broken pipeline reaches the full run.
        """
        return bool(self.checks) and all(check.passed for check in self.checks)

    @property
    def skipped(self) -> list[str]:
        """Checks whose backend was not supplied."""
        return [check.name for check in self.checks if not check.ran]


def run_smoke(
    config: TrainingConfig,
    examples: Sequence[DatasetExample],
    trainer: Trainer,
    *,
    engines: Sequence[Engine] = (),
    probes: Sequence[DatasetExample] = (),
    max_hours: float = MAX_HOURS,
) -> SmokeReport:
    """Train on ``examples`` and run every check the spec lists.

    ``probes`` are the examples used to generate from — by default the first three of ``examples``,
    which is enough to catch a checkpoint that is broken and cheap enough not to matter.

    Raises:
        ValueError: if ``examples`` is empty, or if the config asks for more than one epoch. A
            multi-epoch smoke run is not a smoke run; it is a cheap full run that will not fit the
            hour the plan gives it.
    """
    if not examples:
        raise ValueError("a smoke run needs examples")
    if config.epochs != 1:
        raise ValueError(
            f"config {config.name} trains for {config.epochs} epochs; a smoke run is one epoch, or "
            f"it will not fit the {max_hours:g} h the plan gives it"
        )

    outcome = trainer.train(config, format_dataset(examples))
    sample = list(probes) or list(examples[:3])
    first_engine = engines[0] if engines else None

    report = SmokeReport(config_name=config.name, examples=len(examples), outcome=outcome)
    report.checks = [
        check_loss(outcome),
        check_duration(outcome, max_hours=max_hours),
        check_generation(first_engine, outcome.checkpoint, sample),
        check_stop(first_engine, outcome.checkpoint, sample),
        check_parity(engines, outcome.checkpoint, sample),
    ]
    return report


def render_report(report: SmokeReport) -> str:
    """Human-readable verdict on a smoke run."""
    status = "✓ PASS" if report.passed else "✗ FAIL"
    lines = [f"{status} — smoke run {report.config_name} over {report.examples} example(s)"]
    for check in report.checks:
        mark = "✓" if check.passed else ("·" if not check.ran else "✗")
        lines.append(f"  {mark} {check.name}: {check.detail}")
    if report.outcome and report.outcome.run_url:
        lines.append(f"  W&B: {report.outcome.run_url}")
    if report.skipped:
        lines.append(
            f"  {len(report.skipped)} check(s) did not run ({', '.join(report.skipped)}) — a smoke "
            "run that verified nothing is not a passing smoke run"
        )
    if report.passed:
        lines.append("  the pipeline is sound; the full run (M3.03) may proceed")
    return "\n".join(lines)
