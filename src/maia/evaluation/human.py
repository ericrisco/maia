"""Human evaluation and the baseline comparison — PLAN M4.07-M4.08.

*"Human eval: 30 free conversations scored 1-5 on naturalness, linguistic correctness and
andorranidad. Ideal: 1-2 external Andorran speakers."*
*"Comparison against the M0.06 baseline (same 10 questions) as the internal before/after."*

Two gates that both rest on a judgement no code can make, so what the code does is make that
judgement **answerable and hard to fudge**:

**Three axes, scored separately, and only one of them is a gate.** DoD-F4 asks for *"≥4/5 on
linguistic correctness"* and nothing numeric about the other two. Averaging the three into an
overall score would let good *andorranidad* carry poor Catalan past the bar — so the axes stay
apart, the gate reads only the one the plan names, and the other two are reported because a model
that is correct and lifeless is a finding even when it passes.

**A blind before/after, or it is not a before/after.** M0.06 recorded the base model's answers to
ten questions. A reviewer comparing them side by side, knowing which is which, will prefer the
fine-tune — that is what expectation does. :func:`blind_pairs` shuffles each pair from a seed and
keeps the key separately, so the preference is recorded before anyone knows what they preferred.
:attr:`BaselineComparison.consistency` then reports how often reviewers agreed, because a 6-4 split
is not a before/after either.

The reviewers are people; nothing here is blocked-by-resource, and nothing here can be automated
away.
"""

from __future__ import annotations

import json
import statistics
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from random import Random

#: The plan's conversation count for the free-form review.
CONVERSATIONS = 30

#: The plan's baseline question count, fixed by M0.06.
BASELINE_QUESTIONS = 10

#: DoD-F4's bar, on linguistic correctness only.
MIN_CORRECTNESS = 4.0

#: Below this many reviewers, an agreement rate is not a measurement.
MIN_REVIEWERS = 2


class Axis(StrEnum):
    """What each conversation is scored on. Only ``CORRECTNESS`` is a gate."""

    NATURALNESS = "naturalness"
    CORRECTNESS = "linguistic_correctness"
    ANDORRANITAT = "andorranitat"

    @property
    def gated(self) -> bool:
        """Whether DoD-F4 sets a numeric bar for this axis."""
        return self is Axis.CORRECTNESS


@dataclass(frozen=True)
class Score:
    """One reviewer's 1-5 scores for one conversation."""

    conversation_id: str
    reviewer: str
    scores: dict[Axis, int]
    note: str = ""

    def __post_init__(self) -> None:
        missing = [axis for axis in Axis if axis not in self.scores]
        if missing:
            raise ValueError(
                f"{self.conversation_id}: no score for {', '.join(a.value for a in missing)}; the "
                "axes are kept apart precisely so one cannot stand in for another"
            )
        for axis, value in self.scores.items():
            if not 1 <= value <= 5:
                raise ValueError(f"{self.conversation_id}: {axis.value} is {value}, not 1-5")

    def of(self, axis: Axis) -> int:
        """This reviewer's score on one axis."""
        return self.scores[axis]


@dataclass
class HumanEval:
    """The free-conversation review."""

    scores: list[Score] = field(default_factory=list)
    minimum: float = MIN_CORRECTNESS

    @property
    def conversations(self) -> int:
        """Distinct conversations reviewed."""
        return len({score.conversation_id for score in self.scores})

    @property
    def reviewers(self) -> list[str]:
        """Who reviewed."""
        return sorted({score.reviewer for score in self.scores})

    def mean(self, axis: Axis) -> float | None:
        """Mean score on one axis, or ``None`` if nothing was scored."""
        values = [score.of(axis) for score in self.scores]
        return statistics.fmean(values) if values else None

    @property
    def passed(self) -> bool:
        """Whether DoD-F4's bar is met.

        Reads **only** linguistic correctness. Averaging the three would let strong *andorranidad*
        carry weak Catalan past a bar the plan set for Catalan alone.
        """
        measured = self.mean(Axis.CORRECTNESS)
        return measured is not None and measured >= self.minimum

    @property
    def findings(self) -> list[str]:
        """What is worth saying even when the gate passes."""
        notes: list[str] = []
        if self.conversations < CONVERSATIONS:
            notes.append(
                f"{self.conversations} conversation(s) reviewed; the plan asks for {CONVERSATIONS}"
            )
        if len(self.reviewers) < MIN_REVIEWERS:
            notes.append(
                f"{len(self.reviewers)} reviewer(s); the plan wants 1-2 **external** Andorran "
                "speakers, and a single reviewer's taste cannot be told from the model's quality"
            )
        for axis in Axis:
            measured = self.mean(axis)
            if measured is not None and not axis.gated and measured < self.minimum:
                notes.append(
                    f"{axis.value} averages {measured:.2f}, below the correctness bar — not a "
                    "gate, but a model that is correct and lifeless is still a finding"
                )
        return notes

    @property
    def worst(self) -> list[tuple[str, int, str]]:
        """The lowest-scored conversations on the gated axis, with their notes."""
        ranked = sorted(self.scores, key=lambda score: score.of(Axis.CORRECTNESS))
        return [
            (score.conversation_id, score.of(Axis.CORRECTNESS), score.note) for score in ranked[:5]
        ]


def read_scores(path: Path) -> list[Score]:
    """Read a filled review sheet from JSONL.

    Raises:
        ValueError: naming the line. A dropped score changes a mean that a gate reads.
    """
    scores: list[Score] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
            scores.append(
                Score(
                    conversation_id=str(payload["conversation_id"]),
                    reviewer=str(payload["reviewer"]),
                    scores={Axis(key): int(value) for key, value in payload["scores"].items()},
                    note=str(payload.get("note", "")),
                )
            )
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            raise ValueError(f"{path}:{number}: not a review score ({error})") from error
    return scores


def render(evaluation: HumanEval) -> str:
    """Human-readable verdict on the human eval."""
    mark = "✓" if evaluation.passed else "✗"
    correctness = evaluation.mean(Axis.CORRECTNESS)
    lines = [
        f"{mark} linguistic correctness: "
        + ("not scored" if correctness is None else f"{correctness:.2f}/5")
        + f" (gate ≥{evaluation.minimum:.1f})",
        f"  {evaluation.conversations} conversation(s), "
        f"{len(evaluation.reviewers)} reviewer(s): {', '.join(evaluation.reviewers) or 'none'}",
    ]
    for axis in Axis:
        measured = evaluation.mean(axis)
        if axis.gated or measured is None:
            continue
        lines.append(f"  {axis.value}: {measured:.2f}/5 (reported, not gated)")
    lines += [f"  ⚠ {note}" for note in evaluation.findings]
    for conversation, score, note in evaluation.worst:
        if score < evaluation.minimum:
            lines.append(f"    {conversation}: {score}/5{f' — {note}' if note else ''}")
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────
# M4.08 — the blind before/after against M0.06
# ─────────────────────────────────────────────────────────────


class Side(StrEnum):
    """Which answer a reviewer preferred, in the shuffled presentation."""

    A = "a"
    B = "b"
    TIE = "tie"


@dataclass(frozen=True)
class Pair:
    """One baseline question with both answers, presented in a shuffled order."""

    question: str
    a: str
    b: str
    #: Which side holds the fine-tuned answer. Kept out of the presentation on purpose.
    tuned_side: Side

    def answer_from(self, side: Side) -> str:
        """The text shown on one side."""
        return self.a if side is Side.A else self.b


def blind_pairs(
    questions: Sequence[str],
    base_answers: Sequence[str],
    tuned_answers: Sequence[str],
    *,
    seed: int,
) -> list[Pair]:
    """Shuffle each before/after pair so the reviewer cannot know which is which.

    Without this it is not a before/after: a reviewer told which answer is the new model prefers
    it, and the comparison measures expectation rather than quality. Reproducible from ``seed``, so
    the presentation can be reconstructed when someone questions the result.

    Raises:
        ValueError: if the three sequences do not line up. A misaligned pair would compare one
            question's answer with another's and look like a normal row.
    """
    if not (len(questions) == len(base_answers) == len(tuned_answers)):
        raise ValueError(
            f"{len(questions)} question(s), {len(base_answers)} base and {len(tuned_answers)} "
            "fine-tuned answer(s); a misaligned pair compares one question's answer with another's"
        )
    if not questions:
        raise ValueError("no questions to compare")
    rng = Random(seed)
    pairs: list[Pair] = []
    for question, base, tuned in zip(questions, base_answers, tuned_answers, strict=True):
        tuned_first = rng.random() < 0.5
        pairs.append(
            Pair(
                question=question,
                a=tuned if tuned_first else base,
                b=base if tuned_first else tuned,
                tuned_side=Side.A if tuned_first else Side.B,
            )
        )
    return pairs


@dataclass(frozen=True)
class Preference:
    """One reviewer's blind choice on one pair."""

    question: str
    reviewer: str
    chose: Side


@dataclass
class BaselineComparison:
    """The M0.06 before/after, unblinded."""

    pairs: list[Pair] = field(default_factory=list)
    preferences: list[Preference] = field(default_factory=list)

    @property
    def by_question(self) -> dict[str, Pair]:
        """The pairs, keyed by question."""
        return {pair.question: pair for pair in self.pairs}

    @property
    def for_tuned(self) -> int:
        """Preferences that landed on the fine-tuned answer, once unblinded."""
        pairs = self.by_question
        return sum(
            1
            for preference in self.preferences
            if preference.question in pairs
            and preference.chose is pairs[preference.question].tuned_side
        )

    @property
    def ties(self) -> int:
        """Preferences recorded as a tie."""
        return sum(1 for preference in self.preferences if preference.chose is Side.TIE)

    @property
    def decided(self) -> int:
        """Preferences that were not ties."""
        return len(self.preferences) - self.ties

    @property
    def tuned_rate(self) -> float:
        """Share of decided preferences favouring the fine-tune."""
        return self.for_tuned / self.decided if self.decided else 0.0

    @property
    def consistency(self) -> float | None:
        """How often reviewers agreed, over questions more than one of them judged.

        Reported because a 6-4 split is not a before/after either: an aggregate built from
        reviewers who disagree question by question says the two models are hard to tell apart,
        which is a different claim from "the fine-tune is better".
        """
        grouped: dict[str, list[Side]] = {}
        for preference in self.preferences:
            grouped.setdefault(preference.question, []).append(preference.chose)
        contested = [choices for choices in grouped.values() if len(choices) > 1]
        if not contested:
            return None
        agreements = [
            max(choices.count(side) for side in Side) / len(choices) for choices in contested
        ]
        return statistics.fmean(agreements)


def render_baseline(comparison: BaselineComparison) -> str:
    """Human-readable before/after against the M0.06 baseline."""
    lines = [
        f"before/after over {len(comparison.pairs)} question(s): the fine-tune was preferred in "
        f"{comparison.for_tuned}/{comparison.decided} decided comparison(s) "
        f"({comparison.tuned_rate:.0%}), {comparison.ties} tie(s)",
        "  blind: each pair was shuffled from a seed, so the preference was recorded before anyone "
        "knew what they preferred",
    ]
    if len(comparison.pairs) != BASELINE_QUESTIONS:
        lines.append(
            f"  ⚠ M0.06 fixed {BASELINE_QUESTIONS} questions and this compares "
            f"{len(comparison.pairs)}; the before/after is only a before/after over the same set"
        )
    agreement = comparison.consistency
    if agreement is None:
        lines.append(
            "  ⚠ no question was judged by more than one reviewer, so nothing says whether the "
            "preference is shared or personal"
        )
    else:
        lines.append(f"  reviewers agreed on {agreement:.0%} of contested questions")
        if agreement < 0.7:
            lines.append(
                "  ⚠ reviewers largely disagree, so the aggregate says the two models are hard to "
                'tell apart — which is a different claim from "the fine-tune is better"'
            )
    return "\n".join(lines)


def unblind(pairs: Iterable[Pair]) -> dict[str, Side]:
    """The answer key, for archiving beside the recorded preferences."""
    return {pair.question: pair.tuned_side for pair in pairs}
