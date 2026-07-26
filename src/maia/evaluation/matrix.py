"""The 4-config matrix and the quality gate — PLAN M4.05-M4.06.

*"4-config matrix: base -RAG / base +RAG / fine-tune -RAG / fine-tune +RAG. Quantifies what each
piece contributes — the star table of the model card."*

And the gate it feeds:

*"If any threshold fails → iterate F2 (data) or F3 (training); **do not advance to F5**."*

The matrix earns its place because it answers a question no single number can: **which piece is
doing the work?** A fine-tune that only beats the base when RAG is switched on has not learned
Andorra — RAG is answering and the fine-tune is along for the ride. A fine-tune that gains nothing
from RAG means the retrieval built in M5 is not contributing. Those are opposite problems with
opposite fixes, and only the four cells together tell them apart:

* **Fine-tune contribution** — the same RAG setting, base vs fine-tune.
* **RAG contribution** — the same model, -RAG vs +RAG.
* **Interaction** — whether the two together beat the sum of their parts, or fight.

:func:`contributions` computes all three, and :func:`render` names the diagnosis, because a table of
four numbers is only useful to someone who already knows which comparison to make.

**The gate refuses to be partially satisfied.** Every threshold in the plan is checked, and a
threshold whose measurement is **absent** fails rather than being skipped: *"all thresholds green
and documented"* cannot be satisfied by a threshold nobody measured. The verdict names which phase
to return to — F2 for data, F3 for training — because the plan assigns different failures to
different phases, and a bare "FAIL" leaves that to guesswork.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from enum import StrEnum

from maia.evaluation.andbench import Track, TrackResult

#: And-Obert's two thresholds, which differ by configuration: the plan asks more of the system when
#: retrieval is available, because that is how it will be served.
MIN_OBERT_WITH_RAG = 0.90
MIN_OBERT_WITHOUT_RAG = 0.70

#: A contribution below this is not a contribution. Same reasoning as D-0030's CLEAR_MARGIN: a
#: difference this small is noise, and reading it as a gain would credit a piece that did nothing.
MIN_CONTRIBUTION = 0.02


class Config(StrEnum):
    """The four cells of the matrix."""

    BASE = "base-norag"
    BASE_RAG = "base-rag"
    TUNED = "tuned-norag"
    TUNED_RAG = "tuned-rag"

    @property
    def tuned(self) -> bool:
        """Whether this cell uses the fine-tuned model."""
        return self in {Config.TUNED, Config.TUNED_RAG}

    @property
    def rag(self) -> bool:
        """Whether this cell has retrieval."""
        return self in {Config.BASE_RAG, Config.TUNED_RAG}

    @property
    def label(self) -> str:
        """How the cell is named in the published table."""
        return f"{'fine-tune' if self.tuned else 'base'} {'+RAG' if self.rag else '-RAG'}"


@dataclass
class Matrix:
    """The four configurations, each with its AndBench results."""

    cells: dict[Config, list[TrackResult]] = field(default_factory=dict)

    def score(self, config: Config, track: Track = Track.OBERT) -> float | None:
        """One cell's score on one track, or ``None`` if it was not measured."""
        for result in self.cells.get(config, []):
            if result.track is track:
                return result.score
        return None

    @property
    def complete(self) -> bool:
        """Whether all four cells were measured.

        The matrix is the thing that distinguishes *which piece works*, so three cells do not make a
        smaller matrix — they make an unanswerable question.
        """
        return all(self.score(config) is not None for config in Config)

    @property
    def missing(self) -> list[Config]:
        """Cells with no And-Obert score."""
        return [config for config in Config if self.score(config) is None]


@dataclass(frozen=True)
class Contribution:
    """What one piece added, measured by holding the other constant."""

    name: str
    without: float
    with_: float
    detail: str = ""

    @property
    def delta(self) -> float:
        """How much the piece added."""
        return self.with_ - self.without

    @property
    def contributed(self) -> bool:
        """Whether it added more than noise."""
        return self.delta >= MIN_CONTRIBUTION


def contributions(matrix: Matrix, track: Track = Track.OBERT) -> list[Contribution] | None:
    """Fine-tune contribution, RAG contribution, and their interaction. ``None`` if incomplete.

    Each is measured by holding the other piece constant, which is the only way the four cells
    answer the question they exist for.
    """
    if not matrix.complete:
        return None
    base = matrix.score(Config.BASE, track)
    base_rag = matrix.score(Config.BASE_RAG, track)
    tuned = matrix.score(Config.TUNED, track)
    tuned_rag = matrix.score(Config.TUNED_RAG, track)
    assert base is not None and base_rag is not None  # complete, so every cell has a score
    assert tuned is not None and tuned_rag is not None
    return [
        Contribution(
            "fine-tune (-RAG)", base, tuned, "does the fine-tune know Andorra on its own?"
        ),
        Contribution(
            "fine-tune (+RAG)", base_rag, tuned_rag, "does it still add anything once RAG answers?"
        ),
        Contribution("RAG (base)", base, base_rag, "how much does retrieval alone buy?"),
        Contribution("RAG (fine-tune)", tuned, tuned_rag, "and how much on top of the fine-tune?"),
        Contribution(
            "interaction",
            base + (tuned - base) + (base_rag - base),
            tuned_rag,
            "do the two together beat the sum of their parts, or fight?",
        ),
    ]


def diagnosis(matrix: Matrix, track: Track = Track.OBERT) -> list[str]:
    """What the four cells say about which piece is doing the work.

    The reason the matrix is published rather than a single score: a table of four numbers is only
    useful to someone who already knows which comparison to make.
    """
    computed = contributions(matrix, track)
    if computed is None:
        return [
            "the matrix is incomplete, so it cannot say which piece is doing the work — which is "
            "the only reason it exists"
        ]
    by_name = {item.name: item for item in computed}
    notes: list[str] = []
    tuned_alone = by_name["fine-tune (-RAG)"]
    tuned_with_rag = by_name["fine-tune (+RAG)"]
    rag_on_tuned = by_name["RAG (fine-tune)"]

    if not tuned_alone.contributed and tuned_with_rag.contributed:
        notes.append(
            "the fine-tune only helps once RAG is on: retrieval is answering and the fine-tune is "
            "along for the ride — a data problem (F2), not a training one"
        )
    elif tuned_alone.contributed and not tuned_with_rag.contributed:
        notes.append(
            "the fine-tune helps alone but adds nothing once RAG answers: what it learned is what "
            "retrieval already provides, so the dataset is teaching facts rather than register (F2)"
        )
    elif not tuned_alone.contributed and not tuned_with_rag.contributed:
        notes.append(
            "the fine-tune does not beat the base in either configuration — per M3.05-06, three "
            "runs like this mean the problem is the data (F2)"
        )
    if not rag_on_tuned.contributed:
        notes.append(
            "RAG adds nothing on top of the fine-tune: either retrieval is not finding the right "
            "passages (M4.04's gate) or the model is ignoring them"
        )
    if by_name["interaction"].delta < -MIN_CONTRIBUTION:
        notes.append(
            "the two together are worse than their parts suggest: the fine-tuned model may be "
            "answering from its weights instead of from the retrieved context"
        )
    if not notes:
        notes.append("both pieces contribute, and they do not fight")
    return notes


@dataclass(frozen=True)
class Threshold:
    """One of the plan's success metrics."""

    name: str
    measured: float | None
    minimum: float
    phase: str
    note: str = ""

    @property
    def passed(self) -> bool:
        """Whether it is met.

        An **unmeasured** threshold does not pass. *"All thresholds green and documented"* cannot be
        satisfied by one nobody measured, and treating absence as success is how a gate becomes
        decoration.
        """
        return self.measured is not None and self.measured >= self.minimum

    @property
    def unmeasured(self) -> bool:
        """Whether there is no measurement at all."""
        return self.measured is None


def thresholds(
    matrix: Matrix,
    *,
    catalan_drop: float | None = None,
    max_catalan_drop: float = 0.05,
    retrieval_hit_rate: float | None = None,
    min_retrieval: float = 0.85,
    human_correctness: float | None = None,
    min_human: float = 4.0,
) -> list[Threshold]:
    """Every threshold the plan lists, with the phase to return to when it fails.

    The phase matters: the plan assigns *"iterate F2 (data) or F3 (training)"* by kind of failure,
    and a bare "FAIL" leaves that to guesswork at the moment someone is deciding what to redo.
    """
    obert_rag = matrix.score(Config.TUNED_RAG)
    obert_norag = matrix.score(Config.TUNED)
    return [
        Threshold(
            "And-Obert +RAG",
            obert_rag,
            MIN_OBERT_WITH_RAG,
            "F2/F5",
            "how the model is actually served",
        ),
        Threshold(
            "And-Obert -RAG", obert_norag, MIN_OBERT_WITHOUT_RAG, "F3", "what the weights know"
        ),
        # A drop is a fall, so it is inverted into a headroom to keep every threshold "≥".
        Threshold(
            "general-Catalan headroom",
            None if catalan_drop is None else max_catalan_drop - catalan_drop,
            0.0,
            "F2",
            f"O3 allows a {max_catalan_drop:.0%} drop; the anti-forgetting mix is the lever",
        ),
        Threshold(
            "retrieval hit-rate@5",
            retrieval_hit_rate,
            min_retrieval,
            "F4",
            "fix chunking or embeddings here, not in F5",
        ),
        Threshold(
            "human linguistic correctness",
            human_correctness,
            min_human,
            "F2",
            "scored 1-5 by Andorran speakers",
        ),
    ]


@dataclass
class Gate:
    """DoD-F4: the matrix plus every threshold."""

    matrix: Matrix
    checks: list[Threshold] = field(default_factory=list)

    @property
    def failures(self) -> list[Threshold]:
        """Thresholds not met, including unmeasured ones."""
        return [check for check in self.checks if not check.passed]

    @property
    def unmeasured(self) -> list[Threshold]:
        """Thresholds with no measurement."""
        return [check for check in self.checks if check.unmeasured]

    @property
    def passed(self) -> bool:
        """Whether Phase 5 may proceed.

        Requires a **complete matrix** as well as green thresholds: DoD-F4 asks for the matrix to be
        published, and three cells cannot be published as four.
        """
        return self.matrix.complete and not self.failures

    @property
    def phases(self) -> list[str]:
        """Which phases to return to, in the plan's own terms."""
        return sorted({check.phase for check in self.failures})


def gate(
    matrix: Matrix,
    *,
    catalan_drop: float | None = None,
    retrieval_hit_rate: float | None = None,
    human_correctness: float | None = None,
    max_catalan_drop: float = 0.05,
    min_retrieval: float = 0.85,
    min_human: float = 4.0,
) -> Gate:
    """Assemble the DoD-F4 verdict from one matrix and the measurements taken beside it.

    The thresholds are derived **here** rather than accepted as an argument, so the And-Obert
    numbers in the verdict cannot come from a different matrix than the one being published. Taking
    them separately made that mistake possible, and a gate reporting one matrix's cells against
    another's thresholds would look entirely normal.
    """
    return Gate(
        matrix=matrix,
        checks=thresholds(
            matrix,
            catalan_drop=catalan_drop,
            max_catalan_drop=max_catalan_drop,
            retrieval_hit_rate=retrieval_hit_rate,
            min_retrieval=min_retrieval,
            human_correctness=human_correctness,
            min_human=min_human,
        ),
    )


def render_matrix(matrix: Matrix, track: Track = Track.OBERT) -> str:
    """The star table of the model card, as Markdown."""
    lines = [
        f"## 4-config matrix — {track.value}",
        "",
        "| configuration | score |",
        "| --- | --: |",
    ]
    for config in Config:
        score = matrix.score(config, track)
        lines.append(f"| {config.label} | {'—' if score is None else f'{score:.3f}'} |")
    lines.append("")
    computed = contributions(matrix, track)
    if computed:
        lines += ["| contribution | Δ | |", "| --- | --: | --- |"]
        for item in computed:
            mark = "✓" if item.contributed else "·"
            lines.append(f"| {item.name} | {item.delta:+.3f} {mark} | {item.detail} |")
        lines.append("")
    lines += [f"- {note}" for note in diagnosis(matrix, track)]
    return "\n".join(lines)


def render_gate(verdict: Gate) -> str:
    """DoD-F4's verdict, and where to go when it fails."""
    mark = "✓ PASS" if verdict.passed else "✗ FAIL"
    lines = [f"{mark} — DoD-F4", ""]
    if not verdict.matrix.complete:
        missing = ", ".join(config.label for config in verdict.matrix.missing)
        lines.append(f"  ✗ matrix incomplete: {missing} not measured")
    for check in verdict.checks:
        if check.unmeasured:
            symbol, value = "·", "NOT MEASURED"
        else:
            symbol = "✓" if check.passed else "✗"
            value = f"{check.measured:.3f}"
        lines.append(
            f"  {symbol} {check.name}: {value} (needs >={check.minimum:.2f}) — {check.note}"
        )
    if verdict.unmeasured:
        lines.append(
            f"  {len(verdict.unmeasured)} threshold(s) were never measured, and an unmeasured "
            'threshold does not pass: "all thresholds green and documented" cannot be satisfied '
            "by one nobody measured"
        )
    if not verdict.passed:
        lines.append(
            "  do **not** advance to F5; iterate " + " and ".join(verdict.phases)
            if verdict.phases
            else "  do **not** advance to F5"
        )
    else:
        lines.append(
            "  every threshold green and the matrix complete; F5 may proceed (PO validates)"
        )
    return "\n".join(lines)


def from_results(results: Mapping[Config, Sequence[TrackResult]]) -> Matrix:
    """Build a matrix from per-configuration AndBench results."""
    return Matrix(cells={config: list(items) for config, items in results.items()})
