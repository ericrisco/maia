"""Iterating on the run, and knowing when to stop — PLAN M3.05-06.

*"Iterate: adjust lr/epochs/r. **Max 3 full runs** — if 3 don't beat base clearly, the problem is
the data → back to Phase 2, don't burn GPU."*

This is a budget rule with a diagnosis attached, and both halves need code, because both are the
kind of thing a team talks itself out of at 11pm with a GPU already rented.

**The ceiling is enforced, not remembered.** Three full runs is roughly the whole Phase 3 budget;
a fourth is spending money the plan did not allocate on the hypothesis the plan already rejected.
:func:`may_run_again` says no, and :func:`verdict` says why.

**"Clearly" is a margin, not a `>`.** A candidate scoring 0.001 above the base has not beaten it —
that is noise, and shipping on it would put a fine-tuned model into production on the strength of a
rounding difference. :data:`CLEAR_MARGIN` is what "clearly" means here, and it is stated rather than
assumed.

**Running out of runs is a finding about the *data*, not a failure to try hard enough.** The plan is
explicit: three honest attempts that do not beat the base mean the dataset is the problem, and the
answer is Phase 2, not a fourth learning rate. :func:`verdict` returns that conclusion in those
words, because the alternative — an open-ended search — is exactly how a GPU budget disappears.

:func:`propose` suggests the next configuration, deterministically and with a reason. It does not
promise an improvement: it moves one dimension at a time along the plan's own axes (lr, epochs, r)
so that a comparison between runs means something. Changing three things at once produces a run that
cannot be learned from.
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from maia.training.config import MAX_FULL_RUNS, TrainingConfig

#: How much a candidate must beat the base by for the plan's word "clearly" to apply. Below this the
#: difference is noise, and shipping on it would promote a model on a rounding difference.
CLEAR_MARGIN = 0.02

#: The ladder :func:`propose` walks, one dimension at a time. Ordered by what the plan lists first
#: and by what is cheapest to try: the learning rate costs nothing extra, more epochs cost time, a
#: larger rank costs both time and memory.
#:
#: Only **two** learning rates, deliberately. With three and a three-run ceiling the ladder would
#: spend the entire phase on one axis and never reach ``epochs`` or ``r`` — the plan says "adjust
#: lr/epochs/r", so the budget has to be able to reach all three.
LEARNING_RATES = (2e-4, 1e-4)
EPOCHS = (3, 2)
RANKS = (16, 32)


class BudgetExhaustedError(RuntimeError):
    """Raised when a fourth full run is attempted."""


@dataclass(frozen=True)
class Attempt:
    """One completed full run and what it produced."""

    config: TrainingConfig
    score: float
    checkpoint: str
    notes: str = ""

    def to_json(self) -> str:
        """One line of the run log."""
        return json.dumps(
            {
                "name": self.config.name,
                "score": self.score,
                "checkpoint": self.checkpoint,
                "notes": self.notes,
                "config": json.loads(self.config.model_dump_json()),
            },
            ensure_ascii=False,
        )

    @classmethod
    def from_json(cls, line: str) -> Attempt:
        """Read one line of the run log.

        Raises:
            ValueError: if the line is not an attempt. A log that cannot be read is a log that
                cannot enforce a ceiling, and guessing would let a fourth run through.
        """
        try:
            payload = json.loads(line)
            return cls(
                config=TrainingConfig.model_validate(payload["config"]),
                score=float(payload["score"]),
                checkpoint=str(payload["checkpoint"]),
                notes=str(payload.get("notes", "")),
            )
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            raise ValueError(f"not a run-log entry: {line[:120]!r} ({error})") from error


def read_log(path: Path) -> list[Attempt]:
    """Read the run log, or return nothing if there is none yet."""
    if not path.is_file():
        return []
    return [
        Attempt.from_json(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def append_log(path: Path, attempt: Attempt) -> None:
    """Record one completed run. Append-only: a rewritten log could hide a run."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as sink:
        sink.write(f"{attempt.to_json()}\n")


def beats(candidate: float, base: float, *, margin: float = CLEAR_MARGIN) -> bool:
    """Whether ``candidate`` beats ``base`` **clearly**.

    The plan's word is "clearly", and a bare ``>`` does not implement it: 0.001 above the base is
    noise, and a fine-tuned model shipped on that has not been shown to be better than the model it
    replaces.
    """
    return candidate - base >= margin


def may_run_again(attempts: Sequence[Attempt], *, maximum: int = MAX_FULL_RUNS) -> bool:
    """Whether another full run is inside the phase's budget."""
    return len(attempts) < maximum


def require_budget(attempts: Sequence[Attempt], *, maximum: int = MAX_FULL_RUNS) -> None:
    """Refuse a run beyond the ceiling.

    Raises:
        BudgetExhaustedError: naming what the plan says to do instead. A fourth run spends money the
            plan did not allocate on the hypothesis it already rejected.
    """
    if not may_run_again(attempts, maximum=maximum):
        raise BudgetExhaustedError(
            f"{len(attempts)} full run(s) already completed and the plan caps Phase 3 at "
            f"{maximum}. If none beat the base clearly, the problem is the data — go back to "
            "Phase 2 rather than burning GPU on a fourth hyperparameter guess"
        )


def propose(
    attempts: Sequence[Attempt], base: TrainingConfig, *, maximum: int = MAX_FULL_RUNS
) -> TrainingConfig | None:
    """The next configuration to try, or ``None`` when the budget is spent.

    **One dimension at a time**, along the plan's own axes and in cost order — the learning rate is
    free to change, more epochs cost time, a larger rank costs time and memory. Changing three
    things at once produces a run that cannot be compared with the others, which wastes the run
    twice: once on the GPU and once on the conclusion nobody can draw from it.

    This proposes; it does not predict. Nothing here claims the next point will be better.
    """
    if not may_run_again(attempts, maximum=maximum):
        return None
    tried = {(item.config.learning_rate, item.config.epochs, item.config.r) for item in attempts}

    for rate in LEARNING_RATES:
        candidate = base.model_copy(update={"learning_rate": rate})
        if (candidate.learning_rate, candidate.epochs, candidate.r) not in tried:
            return candidate
    for epochs in EPOCHS:
        candidate = base.model_copy(update={"epochs": epochs})
        if (candidate.learning_rate, candidate.epochs, candidate.r) not in tried:
            return candidate
    for rank in RANKS:
        candidate = base.model_copy(update={"r": rank, "lora_alpha": rank * 2})
        if (candidate.learning_rate, candidate.epochs, candidate.r) not in tried:
            return candidate
    return None


@dataclass
class Verdict:
    """Where Phase 3 stands after the runs completed so far."""

    attempts: list[Attempt] = field(default_factory=list)
    base_score: float = 0.0
    margin: float = CLEAR_MARGIN

    @property
    def best(self) -> Attempt | None:
        """The highest-scoring run so far."""
        return max(self.attempts, key=lambda item: item.score, default=None)

    @property
    def winners(self) -> list[Attempt]:
        """Runs that beat the base clearly."""
        return [
            item for item in self.attempts if beats(item.score, self.base_score, margin=self.margin)
        ]

    @property
    def passed(self) -> bool:
        """Whether DoD-F3's *"≥1 checkpoint beating base"* is satisfied."""
        return bool(self.winners)

    @property
    def exhausted(self) -> bool:
        """Whether the phase has spent its run budget."""
        return not may_run_again(self.attempts)

    @property
    def back_to_phase_2(self) -> bool:
        """Whether the plan's own conclusion applies: the problem is the data.

        Three honest attempts that did not beat the base is evidence about the **dataset**, not a
        signal to try a fourth learning rate.
        """
        return self.exhausted and not self.passed


def verdict(
    attempts: Iterable[Attempt], *, base_score: float, margin: float = CLEAR_MARGIN
) -> Verdict:
    """Assess the runs so far against DoD-F3 and the phase budget."""
    return Verdict(attempts=list(attempts), base_score=base_score, margin=margin)


def render(assessment: Verdict, base: TrainingConfig | None = None) -> str:
    """Human-readable state of Phase 3."""
    lines = [
        f"{len(assessment.attempts)}/{MAX_FULL_RUNS} full run(s) used, base scores "
        f"{assessment.base_score:.3f}, a clear win needs +{assessment.margin:.3f}"
    ]
    for index, attempt in enumerate(assessment.attempts, start=1):
        delta = attempt.score - assessment.base_score
        mark = "✓" if beats(attempt.score, assessment.base_score, margin=assessment.margin) else "✗"
        lines.append(
            f"  {mark} run {index} {attempt.config.name}: {attempt.score:.3f} "
            f"({delta:+.3f} vs base)"
        )
        if attempt.notes:
            lines.append(f"      {attempt.notes}")

    if assessment.passed:
        best = assessment.best
        assert best is not None  # a winner exists, so a best does
        lines.append(
            f"  ✓ DoD-F3 met: {best.config.name} beats the base clearly "
            f"({best.score - assessment.base_score:+.3f}); freeze it as the candidate (M3.07)"
        )
    elif assessment.back_to_phase_2:
        lines.append(
            f"  ✗ {MAX_FULL_RUNS} runs, none beating the base by {assessment.margin:.3f} — "
            "the plan's own conclusion applies: **the problem is the data**. Go back to Phase 2 "
            "rather than spending a fourth run on another hyperparameter guess"
        )
    else:
        remaining = MAX_FULL_RUNS - len(assessment.attempts)
        lines.append(f"  {remaining} run(s) left in the budget")
        if base is not None:
            suggestion = propose(assessment.attempts, base)
            if suggestion is not None:
                lines.append(
                    f"  next: {suggestion.name} — one dimension changed, so the comparison with "
                    "the previous runs still means something"
                )
            else:
                lines.append(
                    "  next: the ladder has no untried rung left, so the remaining run is a human "
                    "choice — and if the ladder is exhausted, that is itself evidence the "
                    "hyperparameters are not where the problem is"
                )
    return "\n".join(lines)
