"""Contributing to AndBench, and running against it — PLAN M4.01-M4.02.

The coupling document is explicit about the boundary, and it decides most of this module:

> *"MAIA is evaluated with **AndBench's harness** (LM Evaluation Harness for MCQ tracks +
> LLM-judge with calibrated rubric for And-Obert). MAIA keeps **no** eval harness of its own;
> discrepancies are fixed in the `andbench` repo. MAIA's 100 manual PO questions + test split
> are contributed to And-Obert (step B2.01)."*

So there is **no scoring code here**. No MCQ accuracy, no LLM-judge rubric, no leaderboard
arithmetic. Writing any of it would produce a second implementation that can disagree with the one
the numbers are supposed to come from, and then two projects argue about whose score is right. What
this module does instead is the two things that are MAIA's side of the boundary:

**Exporting the contribution (M4.01) — with the anti-contamination check that makes it safe.**
Contributing an item to a benchmark MAIA is then measured on is only sound if MAIA never trained on
it. The frozen ``test`` split is not *trained* on, which is necessary and not sufficient: what
matters is that its **grounding passages** are not shared with ``train``. M2.08 separates the splits
by grounding group precisely so that holds, and :func:`contamination` re-checks it rather than
trusting it — if it ever fails, MAIA scores itself on passages it learned from, and the number
flatters the model while looking independent.

**Running the harness (M4.02) — a seam, not a reimplementation.** :class:`Harness` is AndBench's,
**blocked-by-resource** (a separate repo, and a GPU for the model under test). :func:`run`
normalises what it returns into :class:`TrackResult` so the M4.05 matrix has one shape to read, and
refuses a track name AndBench does not define rather than reporting zero for a typo.
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Protocol

from maia.schemas import CorpusDocument, DatasetExample, Split
from maia.synth.publish import restricted
from maia.synth.splits import grounding_groups


class Track(StrEnum):
    """AndBench's four tracks. MCQ except the last, which is generative and LLM-judged."""

    CONEIX = "and_coneix"
    LLENGUA = "and_llengua"
    COTIDIA = "and_cotidia"
    OBERT = "and_obert"

    @property
    def generative(self) -> bool:
        """Whether this track is scored by an LLM judge rather than by multiple choice."""
        return self is Track.OBERT


#: What MAIA contributes, per the coupling document: its test split and the PO's manual questions,
#: both to the generative track.
CONTRIBUTED_TRACK = Track.OBERT

#: The plan's figure for the PO's hand-written questions.
PO_QUESTIONS = 100


class ContaminationError(RuntimeError):
    """Raised when a contribution would let MAIA be scored on passages it trained on."""


class RestrictedContributionError(RuntimeError):
    """Raised when a contribution would publish an item derived from non-redistributable text."""


class UnknownTrackError(RuntimeError):
    """Raised when a harness reports a track AndBench does not define."""


@dataclass(frozen=True)
class Item:
    """One contributed And-Obert item, in the shape AndBench ingests."""

    id: str
    question: str
    reference: str
    topic: str
    grounding_ids: tuple[str, ...]
    source: str = "maia"

    def to_json(self) -> str:
        """One JSONL line for the ``andbench`` repo."""
        return json.dumps(
            {
                "id": self.id,
                "question": self.question,
                "reference": self.reference,
                "topic": self.topic,
                "grounding_ids": list(self.grounding_ids),
                "source": self.source,
            },
            ensure_ascii=False,
        )


def to_item(example: DatasetExample) -> Item:
    """Convert a §3.2 example into a contributed item.

    Raises:
        ValueError: if the example is not a single question and answer. And-Obert scores one answer
            against one reference; a multi-turn conversation has no single reference, and flattening
            it would invent one.
    """
    if len(example.messages) != 2:
        raise ValueError(
            f"{example.id}: {len(example.messages)} messages — And-Obert scores one answer against "
            "one reference, and flattening a conversation would invent the reference"
        )
    # §3.2 already guarantees a conversation opens with the user and alternates, so with exactly
    # two messages the order is user then assistant.
    question, answer = example.messages
    return Item(
        id=str(example.id),
        question=question.content,
        reference=answer.content,
        topic=example.topic,
        grounding_ids=tuple(example.grounding_ids),
    )


def contamination(
    examples: Sequence[DatasetExample], *, contributed: Split = Split.TEST
) -> list[str]:
    """Grounding passages shared between the contributed split and ``train``.

    The check that makes the contribution sound. Being un-*trained* is necessary and not sufficient:
    if a contributed item's grounding passage also grounds a training example, MAIA learned that
    passage, and the resulting number flatters the model while looking independent.

    M2.08's group split is what makes this hold; this re-checks rather than trusting, because the
    consequence of it silently not holding is a benchmark result nobody can rely on.
    """
    trained = {
        ident
        for example in examples
        if example.split is Split.TRAIN
        for ident in example.grounding_ids
    }
    return sorted(
        {
            ident
            for example in examples
            if example.split is contributed
            for ident in example.grounding_ids
            if ident in trained
        }
    )


def contribution(
    examples: Sequence[DatasetExample],
    *,
    manual: Iterable[Item] = (),
    contributed: Split = Split.TEST,
    corpus: Mapping[str, CorpusDocument] | None = None,
) -> list[Item]:
    """The items MAIA contributes to And-Obert.

    ``corpus`` is required to contribute at all, and the reason is the same one M2.11 acts on:
    **AndBench is a public artifact.** An item generated from a ``no-redistribute`` passage is a
    derivative of text the project may not redistribute, and contributing it publishes that
    derivative under a benchmark's name. A §3.2 example carries no licence of its own — only its
    grounding does (D-0024) — so provenance cannot be established without the corpus.

    Raises:
        ContaminationError: if any contributed passage is also a training passage. Naming the
            passages, because the fix is a re-split (M2.08), not a smaller contribution.
        RestrictedContributionError: if the corpus is absent, or if any item is grounded in
            non-redistributable text.
    """
    shared = contamination(examples, contributed=contributed)
    if shared:
        raise ContaminationError(
            f"{len(shared)} grounding passage(s) are in both the {contributed.value} split and "
            f"train (e.g. {shared[0]}); contributing these would let MAIA be scored on passages it "
            "learned from. Re-split by grounding group (M2.08) rather than trimming the "
            "contribution"
        )
    candidates = [example for example in examples if example.split is contributed]
    if corpus is None:
        raise RestrictedContributionError(
            "contributing needs the corpus to establish provenance: AndBench is a public artifact, "
            "a §3.2 example carries no licence of its own (D-0024), and an item generated from "
            "no-redistribute text would publish a derivative of it"
        )
    blocked = restricted(candidates, corpus)
    if blocked:
        raise RestrictedContributionError(
            f"{len(blocked)} contributed item(s) are grounded in text that may not be "
            f"redistributed (e.g. {blocked[0].id}); contributing them would publish a derivative "
            "of it under AndBench's name. Exclude those passages from pool_bench, or drop the "
            "items deliberately"
        )
    return [*(to_item(example) for example in candidates), *manual]


def write_contribution(items: Sequence[Item], path: Path) -> Path:
    """Write the contribution as JSONL for the ``andbench`` repo."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(f"{item.to_json()}\n" for item in items), encoding="utf-8")
    return path


def read_manual(path: Path) -> list[Item]:
    """Read the PO's hand-written questions.

    Raises:
        ValueError: naming the line. A silently dropped question shrinks the benchmark MAIA is
            measured on, which is the last place to be casual about missing data.
    """
    items: list[Item] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
            items.append(
                Item(
                    id=str(payload["id"]),
                    question=str(payload["question"]),
                    reference=str(payload["reference"]),
                    topic=str(payload.get("topic", "manual")),
                    grounding_ids=tuple(str(item) for item in payload.get("grounding_ids", [])),
                    source=str(payload.get("source", "po-manual")),
                )
            )
        except (json.JSONDecodeError, KeyError, TypeError) as error:
            raise ValueError(f"{path}:{number}: not a question item ({error})") from error
    return items


@dataclass(frozen=True)
class TrackResult:
    """One track's score, normalised so the M4.05 matrix has one shape to read.

    The score itself comes from AndBench. Nothing here recomputes it.
    """

    track: Track
    score: float
    items: int
    detail: Mapping[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not 0.0 <= self.score <= 1.0:
            raise ValueError(f"{self.track.value}: score {self.score} is outside 0.0-1.0")
        if self.items <= 0:
            raise ValueError(
                f"{self.track.value}: {self.items} item(s) — a score over nothing is not a score"
            )


class Harness(Protocol):
    """AndBench's evaluation harness. Blocked-by-resource: a separate repo, and a GPU."""

    def evaluate(
        self, model: str, tracks: Sequence[str], *, revision: str | None = None
    ) -> Mapping[str, Mapping[str, float]]:
        """Run the named tracks and return ``{track: {"score": …, "items": …, …}}``."""


def parse_results(payload: Mapping[str, Mapping[str, float]]) -> list[TrackResult]:
    """Normalise the harness's output.

    Raises:
        UnknownTrackError: for a track AndBench does not define. Reporting zero for a typo'd track
            name would look like a failing track, and the two are very different problems.
        ValueError: if a track reports no score or no item count.
    """
    results: list[TrackResult] = []
    for name, values in payload.items():
        try:
            track = Track(name)
        except ValueError as error:
            raise UnknownTrackError(
                f"{name!r} is not an AndBench track; known: "
                + ", ".join(item.value for item in Track)
            ) from error
        if "score" not in values or "items" not in values:
            raise ValueError(
                f"{name}: the harness reported {sorted(values)}; a result without a score and an "
                "item count cannot be compared with anything"
            )
        results.append(
            TrackResult(
                track=track,
                score=float(values["score"]),
                items=int(values["items"]),
                detail={
                    key: float(value)
                    for key, value in values.items()
                    if key not in {"score", "items"}
                },
            )
        )
    return sorted(results, key=lambda result: result.track.value)


def run(
    harness: Harness,
    model: str,
    *,
    tracks: Sequence[Track] = tuple(Track),
    revision: str | None = None,
) -> list[TrackResult]:
    """Run AndBench's harness over ``tracks`` and normalise the result.

    A thin adapter on purpose. MAIA keeps no harness of its own, so a discrepancy is a bug in the
    ``andbench`` repo and gets fixed there — not worked around here, where it would become a second
    definition of the score.
    """
    if not tracks:
        raise ValueError("no tracks to run")
    payload = harness.evaluate(model, [track.value for track in tracks], revision=revision)
    return parse_results(payload)


def render(results: Sequence[TrackResult], *, label: str = "") -> str:
    """Human-readable track scores."""
    heading = f"AndBench{f' — {label}' if label else ''}"
    lines = [heading, "", "| track | score | items | scoring |", "| --- | --: | --: | --- |"]
    for result in results:
        how = "LLM-judge" if result.track.generative else "MCQ"
        lines.append(f"| `{result.track.value}` | {result.score:.3f} | {result.items} | {how} |")
    lines.append("")
    lines.append("Scores produced by AndBench's harness; MAIA keeps no harness of its own (D9).")
    return "\n".join(lines)


def render_contribution(items: Sequence[Item]) -> str:
    """Human-readable summary of what is being contributed."""
    from_dataset = sum(1 for item in items if item.source == "maia")
    manual = len(items) - from_dataset
    lines = [
        f"contributing {len(items)} item(s) to {CONTRIBUTED_TRACK.value}: "
        f"{from_dataset} from the frozen test split, {manual} hand-written",
        "  no grounding passage is shared with the train split — checked, not assumed",
    ]
    if manual < PO_QUESTIONS:
        lines.append(
            f"  ⚠ the plan asks for {PO_QUESTIONS} manual PO questions and {manual} were supplied"
        )
    return "\n".join(lines)


def groups_are_separated(examples: Sequence[DatasetExample]) -> bool:
    """Whether no grounding group spans two splits — M2.08's guarantee, verified here.

    A stronger statement than :func:`contamination`: that one asks whether *these* passages leaked,
    this asks whether the split is sound at all.
    """
    by_id = {str(example.id): example.split for example in examples}
    return all(len({by_id[key] for key in group}) == 1 for group in grounding_groups(examples))
