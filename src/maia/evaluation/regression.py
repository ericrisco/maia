"""General-Catalan regression — PLAN M4.03.

*"Softcatalà `ai-eval-catalan` on base vs fine-tune. Criterion O3: drop ≤5 %."*

The whole of Phase 2 spent 15-20 % of the dataset on an anti-forgetting mix (M2.04) to protect
exactly what this measures: whether teaching the model Andorra cost it its general Catalan. So this
is the check that says whether that mix worked.

Two things make the number mean something, and both are easy to get wrong:

**A "5 % drop" is relative, not absolute.** A base scoring 0.80 falling to 0.76 has dropped 5 %;
the same 0.04 from 0.40 is a 10 % drop. Reading it as percentage *points* would silently let a weak
model regress twice as far as a strong one before failing. :func:`relative_drop` divides.

**Two scores are comparable only under the same conditions.** The same harness version, the same
question set, the same decoding. A fine-tune measured on a newer `ai-eval-catalan` than the base is
not being compared with the base — it is being compared with a different test, and the difference
will be read as regression or as improvement with equal confidence. :func:`compare` **refuses**
mismatched conditions rather than producing a number nobody should trust.

The harness is Softcatalà's and is **blocked-by-resource**; :class:`CatalanEval` is the seam. As in
M4.02, nothing here reimplements its scoring.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Protocol

#: Criterion O3: general Catalan may fall by at most this share of the base score.
MAX_RELATIVE_DROP = 0.05

#: Slack for binary floating point when comparing against the limit. ``(0.80 - 0.76) / 0.80`` is
#: ``0.05000000000000005``, so a case sitting exactly on the threshold would fail on a
#: representation artefact. The limit is a quality decision; 1e-17 must not decide a gate.
_TOLERANCE = 1e-9


class IncomparableError(RuntimeError):
    """Raised when two runs were not measured under the same conditions."""


@dataclass(frozen=True)
class EvalRun:
    """One `ai-eval-catalan` run, with the conditions that make it comparable."""

    model: str
    score: float
    harness_version: str
    questions: int
    tasks: Mapping[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not 0.0 <= self.score <= 1.0:
            raise ValueError(f"{self.model}: score {self.score} is outside 0.0-1.0")
        if self.questions <= 0:
            raise ValueError(
                f"{self.model}: a score over {self.questions} questions is not a score"
            )
        if not self.harness_version:
            raise ValueError(
                f"{self.model}: no harness version recorded, so this run cannot be shown to be "
                "comparable with any other"
            )

    @property
    def conditions(self) -> tuple[str, int, tuple[str, ...]]:
        """What has to match for two runs to be comparable."""
        return (self.harness_version, self.questions, tuple(sorted(self.tasks)))


class CatalanEval(Protocol):
    """Softcatalà's `ai-eval-catalan`. Blocked-by-resource: an external harness and a GPU."""

    def run(self, model: str, *, revision: str | None = None) -> EvalRun:
        """Evaluate one model and return its score with the run's conditions."""


def relative_drop(base: float, candidate: float) -> float:
    """How far ``candidate`` fell below ``base``, as a share of ``base``.

    Relative, because O3 says *"drop ≤5 %"*: 0.80 → 0.76 is 5 %, while the same 0.04 from 0.40 is
    10 %. Percentage points would let a weak model regress twice as far as a strong one before
    failing. Negative when the candidate improved.
    """
    if base <= 0:
        raise ValueError(f"base score {base} gives nothing to regress from")
    return (base - candidate) / base


@dataclass(frozen=True)
class Regression:
    """The base-vs-fine-tune comparison, and whether O3 holds."""

    base: EvalRun
    candidate: EvalRun
    limit: float = MAX_RELATIVE_DROP

    @property
    def drop(self) -> float:
        """Relative drop; negative if the fine-tune improved."""
        return relative_drop(self.base.score, self.candidate.score)

    @property
    def passed(self) -> bool:
        """Whether criterion O3 holds.

        Not a bare ``<=`` — see :data:`_TOLERANCE`.
        """
        return self.drop <= self.limit + _TOLERANCE

    @property
    def improved(self) -> bool:
        """Whether general Catalan got *better*, which the anti-forgetting mix makes possible."""
        return self.drop < 0

    @property
    def worst_tasks(self) -> list[tuple[str, float]]:
        """Per-task drops, largest first — where the forgetting actually happened.

        The aggregate can pass while one task collapses, and knowing *which* is what tells you
        whether the anti-forgetting mix was the wrong shape rather than the wrong size.
        """
        shared = set(self.base.tasks) & set(self.candidate.tasks)
        drops = [
            (task, relative_drop(self.base.tasks[task], self.candidate.tasks[task]))
            for task in sorted(shared)
            if self.base.tasks[task] > 0
        ]
        return sorted(drops, key=lambda item: -item[1])


def compare(base: EvalRun, candidate: EvalRun, *, limit: float = MAX_RELATIVE_DROP) -> Regression:
    """Compare two runs, refusing to compare incomparable ones.

    Raises:
        IncomparableError: naming what differs. A fine-tune measured on a newer harness, or over a
            different question set, is not being compared with the base — it is being compared with
            a different test, and the difference reads as regression or improvement with equal
            confidence.
    """
    if base.conditions != candidate.conditions:
        differences = []
        if base.harness_version != candidate.harness_version:
            differences.append(f"harness {base.harness_version} vs {candidate.harness_version}")
        if base.questions != candidate.questions:
            differences.append(f"{base.questions} vs {candidate.questions} questions")
        if sorted(base.tasks) != sorted(candidate.tasks):
            differences.append("different task sets")
        raise IncomparableError(
            f"{base.model} and {candidate.model} were not measured under the same conditions "
            f"({'; '.join(differences)}); re-run both on the same harness rather than comparing "
            "a model against a different test"
        )
    return Regression(base=base, candidate=candidate, limit=limit)


def measure(
    harness: CatalanEval,
    *,
    base_model: str,
    candidate_model: str,
    candidate_revision: str | None = None,
    limit: float = MAX_RELATIVE_DROP,
) -> Regression:
    """Run both models through the harness and compare them."""
    return compare(
        harness.run(base_model),
        harness.run(candidate_model, revision=candidate_revision),
        limit=limit,
    )


def render(regression: Regression) -> str:
    """Human-readable verdict on criterion O3."""
    mark = "✓" if regression.passed else "✗"
    direction = "improved" if regression.improved else "dropped"
    lines = [
        f"{mark} general Catalan {direction} {abs(regression.drop):.1%} "
        f"(O3 allows a {regression.limit:.0%} drop)",
        f"  base      {regression.base.model}: {regression.base.score:.3f}",
        f"  candidate {regression.candidate.model}: {regression.candidate.score:.3f}",
        f"  both on {regression.base.harness_version} over {regression.base.questions} question(s)",
    ]
    worst = regression.worst_tasks
    if worst:
        lines.append("  per task, largest drop first:")
        lines += [f"    {task}: {drop:+.1%}" for task, drop in worst[:5]]
        if regression.passed and worst[0][1] > regression.limit:
            lines.append(
                f"  ⚠ the aggregate passes but {worst[0][0]} fell {worst[0][1]:.1%} — the "
                "anti-forgetting mix (M2.04) may be the wrong shape rather than the wrong size"
            )
    if regression.improved:
        lines.append(
            "  general Catalan got better, which the anti-forgetting mix makes possible; it is not "
            "evidence the Andorran training worked"
        )
    return "\n".join(lines)


def tasks_in_common(runs: Sequence[EvalRun]) -> list[str]:
    """Tasks every run reports — the only ones a comparison across all of them can use."""
    if not runs:
        return []
    shared = set(runs[0].tasks)
    for run in runs[1:]:
        shared &= set(run.tasks)
    return sorted(shared)
