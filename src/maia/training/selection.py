"""Choosing between epoch checkpoints — PLAN M3.04.

*"Evaluate each epoch against AndBench-val; watch overfitting to synthetic style (symptom: clonic
answers, lost variety). **The best is not always the last.**"*

That last sentence is the whole module. Taking the final checkpoint is the default everywhere, it
requires no code, and it is wrong often enough that the plan calls it out — so the selection has to
be a computation with reasons attached, not a convention.

**Accuracy alone cannot see the failure the plan describes.** A model overfitted to 12,000
synthetic examples answers *well* on questions shaped like its training data while having collapsed
into a house style: the same openings, the same length, the same three constructions. Its AndBench
score can be the highest of the three epochs. What has been lost is variety, and variety is
measurable:

* **Self-similarity.** Overfitted answers resemble *each other*. Reusing M2.05's cosine machinery,
  :func:`variety` reports the mean pairwise similarity across a checkpoint's answers — a number that
  rises as the model collapses.
* **Distinct openings.** Clonic answers start the same way. Counting distinct first-few-words across
  the sample catches a model that has learned one way to begin a sentence.
* **Length spread.** A collapsed model answers everything at the same length; the coefficient of
  variation of answer length falls towards zero.

:func:`select` therefore picks the highest-scoring checkpoint **whose variety has not collapsed
relative to the others**, and says in words when that is not the last one. Where accuracy and
variety disagree it does not silently average them into one number — it reports both and names the
trade-off, because which to prefer is a judgement DoD-F3 gives to the PO and the Tech Lead.

Everything here needs a loaded model and an AndBench harness, both **blocked-by-resource**;
:class:`Answerer` and :class:`Scorer` are the seams.
"""

from __future__ import annotations

import statistics
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from itertools import combinations
from pathlib import Path
from typing import Protocol

from maia.synth.semdedup import Embedder, cosine

#: How many leading words define an "opening" for the clonic-answer check.
OPENING_WORDS = 4

#: A checkpoint whose variety falls more than this below the best of the run has collapsed, however
#: well it scores. Deliberately generous: normal epoch-to-epoch drift is small, and this is meant to
#: catch collapse rather than to referee close calls.
MAX_VARIETY_DROP = 0.15

#: Below this many answers, none of the variety statistics mean anything.
MIN_SAMPLE = 10


class Answerer(Protocol):
    """Generates answers from one checkpoint. Blocked-by-resource: loads the model."""

    def answer(self, checkpoint: Path, questions: Sequence[str]) -> list[str]:
        """Answer every question, in order."""


class Scorer(Protocol):
    """Scores answers against references — the AndBench harness (B1/B2, external)."""

    def score(self, answers: Sequence[str], references: Sequence[str]) -> float:
        """A single 0-1 quality score for a set of answers."""


@dataclass(frozen=True)
class Variety:
    """How varied one checkpoint's answers are. Higher is more varied, on every axis."""

    distinct_openings: float
    length_spread: float
    dissimilarity: float
    sample: int

    @property
    def score(self) -> float:
        """One number for ranking, the mean of the three axes.

        Averaged only for *ranking*; the three are reported separately because they fail
        differently and the report should say which one moved.
        """
        return (self.distinct_openings + self.length_spread + self.dissimilarity) / 3

    @property
    def measurable(self) -> bool:
        """Whether there were enough answers for these numbers to mean anything."""
        return self.sample >= MIN_SAMPLE


def openings(answers: Iterable[str], words: int = OPENING_WORDS) -> float:
    """Share of answers that begin differently.

    A model collapsed into a house style opens the same way every time — *"El Consell General
    és…"*, over and over. Case-folded, because capitalisation is not the variety at issue.
    """
    sample = [answer for answer in answers if answer.strip()]
    if not sample:
        return 0.0
    starts = {" ".join(answer.lower().split()[:words]) for answer in sample}
    return len(starts) / len(sample)


def length_spread(answers: Iterable[str]) -> float:
    """Coefficient of variation of answer length, clamped to ``[0, 1]``.

    A collapsed model answers everything at the same length. The coefficient of variation is used
    rather than the standard deviation so a model that is uniformly *long* is not mistaken for a
    varied one.
    """
    # Blank answers are filtered out, so every length is at least 1 and the mean is never zero.
    lengths = [len(answer) for answer in answers if answer.strip()]
    if len(lengths) < 2:
        return 0.0
    return min(1.0, statistics.stdev(lengths) / statistics.fmean(lengths))


def dissimilarity(answers: Sequence[str], embedder: Embedder) -> float:
    """``1 - mean pairwise cosine`` over the answers.

    The direct measurement of "clonic": overfitted answers resemble each other. Reuses M2.05's
    embedding seam, so the same vectors that detect duplicate *training examples* detect a model
    that has collapsed into repeating itself.
    """
    usable = [answer for answer in answers if answer.strip()]
    if len(usable) < 2:
        return 0.0
    vectors = embedder.embed(usable)
    if len(vectors) != len(usable):
        raise ValueError(
            f"embedder returned {len(vectors)} vectors for {len(usable)} answers — refusing to "
            "compare answers against embeddings that may not be theirs"
        )
    similarities = [cosine(left, right) for left, right in combinations(vectors, 2)]
    return max(0.0, min(1.0, 1.0 - statistics.fmean(similarities)))


def variety(answers: Sequence[str], embedder: Embedder) -> Variety:
    """Measure all three axes for one checkpoint's answers."""
    return Variety(
        distinct_openings=openings(answers),
        length_spread=length_spread(answers),
        dissimilarity=dissimilarity(answers, embedder),
        sample=sum(1 for answer in answers if answer.strip()),
    )


@dataclass(frozen=True)
class Candidate:
    """One epoch's checkpoint, measured."""

    epoch: int
    checkpoint: Path
    accuracy: float
    variety: Variety

    @property
    def label(self) -> str:
        """How the checkpoint is named in the report."""
        return f"epoch {self.epoch} ({self.checkpoint.name})"


@dataclass
class Selection:
    """Which checkpoint to promote, and why."""

    chosen: Candidate | None
    candidates: list[Candidate] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)
    rejected_for_variety: list[Candidate] = field(default_factory=list)

    @property
    def best_by_accuracy(self) -> Candidate | None:
        """What a naive "highest score wins" would have picked."""
        return max(self.candidates, key=lambda item: item.accuracy, default=None)

    @property
    def last(self) -> Candidate | None:
        """What "just take the final checkpoint" would have picked."""
        return max(self.candidates, key=lambda item: item.epoch, default=None)

    @property
    def differs_from_last(self) -> bool:
        """Whether the choice is *not* the final epoch — the case the plan warns about."""
        return (
            self.chosen is not None
            and self.last is not None
            and self.chosen.epoch != self.last.epoch
        )


def evaluate(
    checkpoints: Sequence[Path],
    questions: Sequence[str],
    references: Sequence[str],
    answerer: Answerer,
    scorer: Scorer,
    embedder: Embedder,
) -> list[Candidate]:
    """Score and measure every checkpoint.

    Raises:
        ValueError: if there are no checkpoints, or the questions and references do not line up.
            Scoring against a mismatched reference list produces a number that means nothing and
            looks like a result.
    """
    if not checkpoints:
        raise ValueError("no checkpoints to choose between")
    if len(questions) != len(references):
        raise ValueError(
            f"{len(questions)} question(s) against {len(references)} reference(s); a mismatched "
            "pairing produces a score that means nothing and looks like a result"
        )
    measured: list[Candidate] = []
    for epoch, checkpoint in enumerate(checkpoints, start=1):
        answers = answerer.answer(checkpoint, questions)
        if len(answers) != len(questions):
            raise ValueError(
                f"{checkpoint}: {len(answers)} answer(s) for {len(questions)} question(s)"
            )
        measured.append(
            Candidate(
                epoch=epoch,
                checkpoint=checkpoint,
                accuracy=scorer.score(answers, references),
                variety=variety(answers, embedder),
            )
        )
    return measured


def select(
    candidates: Sequence[Candidate], *, max_variety_drop: float = MAX_VARIETY_DROP
) -> Selection:
    """Pick the checkpoint to promote.

    The highest-scoring candidate **whose variety has not collapsed** relative to the best of the
    run. Accuracy alone cannot see the failure the plan describes: a model overfitted to synthetic
    data scores well on questions shaped like its training set while having lost the variety that
    makes it usable.

    Where the variety numbers are not measurable (too few answers) they are **not** used to reject
    anything, and the report says so — a rule applied on evidence nobody has is worse than no rule.
    """
    selection = Selection(chosen=None, candidates=list(candidates))
    if not candidates:
        selection.reasons.append("no candidates")
        return selection

    measurable = [item for item in candidates if item.variety.measurable]
    if not measurable:
        selection.chosen = max(candidates, key=lambda item: (item.accuracy, -item.epoch))
        selection.reasons.append(
            f"variety not measured: fewer than {MIN_SAMPLE} answers per checkpoint, so the "
            "collapse check was skipped and this is accuracy alone"
        )
        return selection

    best_variety = max(item.variety.score for item in measurable)
    eligible: list[Candidate] = []
    for item in candidates:
        if item.variety.measurable and best_variety - item.variety.score > max_variety_drop:
            selection.rejected_for_variety.append(item)
        else:
            eligible.append(item)

    if not eligible:  # pragma: no cover — the best-variety candidate is never rejected
        eligible = list(candidates)

    # Ties go to the earlier epoch: less training for the same result is less overfitting.
    selection.chosen = max(eligible, key=lambda item: (item.accuracy, -item.epoch))
    for item in selection.rejected_for_variety:
        selection.reasons.append(
            f"{item.label} rejected: variety {item.variety.score:.2f} is "
            f"{best_variety - item.variety.score:.2f} below the run's best, which is the "
            "clonic-answer collapse the plan warns about"
        )
    if selection.differs_from_last:
        selection.reasons.append(
            "the chosen checkpoint is not the last one — which is exactly the case the plan flags"
        )
    return selection


def render(selection: Selection) -> str:
    """Human-readable comparison of the epochs."""
    if selection.chosen is None:
        return "no checkpoint chosen: " + "; ".join(selection.reasons)
    lines = [
        f"chosen: {selection.chosen.label} — accuracy {selection.chosen.accuracy:.3f}, "
        f"variety {selection.chosen.variety.score:.2f}",
        "",
        "| epoch | accuracy | variety | openings | lengths | distinct |",
        "| --: | --: | --: | --: | --: | --: |",
    ]
    for item in sorted(selection.candidates, key=lambda candidate: candidate.epoch):
        mark = " ←" if item is selection.chosen else ""
        measure = item.variety
        lines.append(
            f"| {item.epoch}{mark} | {item.accuracy:.3f} | {measure.score:.2f} | "
            f"{measure.distinct_openings:.2f} | {measure.length_spread:.2f} | "
            f"{measure.dissimilarity:.2f} |"
        )
    lines.append("")
    for reason in selection.reasons:
        lines.append(f"- {reason}")

    naive = selection.best_by_accuracy
    if naive is not None and selection.chosen.epoch != naive.epoch:
        lines.append(
            f"- accuracy alone would have chosen {naive.label} "
            f"({naive.accuracy:.3f} vs {selection.chosen.accuracy:.3f}); it was rejected on "
            "variety, and which to prefer is the PO's and Tech Lead's call under DoD-F3"
        )
    return "\n".join(lines)
