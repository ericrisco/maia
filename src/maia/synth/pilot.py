"""The 500-example pilot — PLAN M2.06, a PO-blocking gate.

*"Pilot: 500 examples, joint PO+dev review to calibrate the ``judge_score`` threshold and confirm
the style sounds Andorran, not Wikipedia. No mass generation without PO OK."*

Two jobs, and the second is the one that earns its keep.

**Make the review answerable.** *"Is this factually correct?"* is unanswerable without the passage
the answer was generated from, so every row of the review package carries its grounding text
alongside the conversation. And DoD-F2 asks for **two different rates against two different bars**
(≥95 % factual, ≥98 % correct Catalan) while the pilot gate asks a third question (does it sound
Andorran?) — so the sheet has **three independent columns**, not one verdict. Collapsing them would
make it impossible to tell a factually wrong answer from a badly written one, which are different
problems with different fixes.

**Calibrate the threshold against the humans, not against a hunch.** M2.05 ships
``judge.DEFAULT_THRESHOLD = 0.7``, which is a starting point nobody measured. Here the pilot's human
``factual`` labels and the machine's ``judge_score`` sit side by side, so :func:`calibrate` can
answer the question the plan actually asks: **what is the lowest threshold at which the surviving
examples are ≥95 % factually correct?** Lowest, because every point above that throws away good
examples for nothing.

Three ways this could produce a comfortable lie, each refused:

* A threshold that reaches 95 % on four surviving examples is arithmetic, not evidence.
  :attr:`Calibration.support` is reported and :data:`MIN_SUPPORT` is enforced.
* Exempt types (``general_ca``, ``estil_andorra``) carry ``judge_score = 0.0`` by construction
  (D-0018), so including them would put a wall of unjudged zeros at the bottom of the curve and
  make every threshold look good. They are excluded from calibration and counted.
* If **no** threshold reaches the bar, that is the finding — the judge cannot be used as a gate on
  this dataset — and :attr:`Calibration.achievable` says so rather than returning the best of a bad
  set.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import sys
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from random import Random

from maia.corpus.sampling import allocate
from maia.schemas import CorpusDocument, DatasetExample, ExampleType
from maia.synth.judge import is_exempt

#: The plan's pilot size.
DEFAULT_PILOT_SIZE = 500

#: DoD-F2's two bars, and the pilot's third question.
MIN_FACTUAL_RATE = 0.95
MIN_CATALAN_RATE = 0.98
#: The plan gives no number for "sounds Andorran"; a majority is the weakest defensible reading and
#: is recorded so the PO can raise it.
MIN_ANDORRAN_RATE = 0.50

#: Fewest surviving examples a calibrated threshold may rest on. Below this the rate is noise.
MIN_SUPPORT = 20

#: Thresholds tried, coarse enough to be meaningful and fine enough to be useful.
CANDIDATE_THRESHOLDS = tuple(index / 20 for index in range(21))

#: Review-sheet columns. The last four are the reviewers' to fill.
FIELDNAMES = (
    "id",
    "type",
    "topic",
    "judge_score",
    "grounding_ids",
    "conversation",
    "passages",
    "factual",
    "catalan",
    "andorran",
    "note",
)


class Label(StrEnum):
    """A reviewer's answer to one question about one example."""

    PENDING = "pending"
    YES = "yes"
    NO = "no"
    #: For a question that does not apply — a ``general_ca`` example is not meant to sound
    #: Andorran, and scoring it against that bar would penalise it for doing its job.
    NA = "na"


class IncompleteReviewError(RuntimeError):
    """Raised when a pilot is scored while any answer is still ``pending``."""


@dataclass(frozen=True)
class ReviewedExample:
    """One pilot example with the reviewers' three answers."""

    example: DatasetExample
    passages: tuple[str, ...] = ()
    factual: Label = Label.PENDING
    catalan: Label = Label.PENDING
    andorran: Label = Label.PENDING
    note: str = ""

    @property
    def answers(self) -> tuple[Label, Label, Label]:
        """The three answers, for the pending check."""
        return (self.factual, self.catalan, self.andorran)


def conversation_of(example: DatasetExample) -> str:
    """The example as a reviewer reads it."""
    return "\n\n".join(
        f"{message.role.value.upper()}: {message.content}" for message in example.messages
    )


def stratum_of(example: DatasetExample) -> str:
    """The stratum one example belongs to: its **type and split**.

    Type, so that ``no_ho_se`` and ``traduccio`` cannot escape the gate behind a mass of ``qa``.
    Split too, because ``test`` is the frozen benchmark: a review that happened to miss it would
    say nothing about the 5 % of the dataset every Phase 4 number is computed on.
    """
    return f"{example.type.value}|{example.split.value}"


def dataset_digest(examples: Iterable[DatasetExample]) -> str:
    """A digest of the whole dataset, recorded in the review sheet.

    Without it nothing ties a filled sheet to the dataset it claims to describe: a `judge_score`
    could be edited by hand and the calibration would believe it, and a review could be scored
    against a dataset that has since changed. Order-independent, so re-serialising does not
    invalidate it.
    """
    hasher = hashlib.sha256()
    for line in sorted(example.model_dump_json() for example in examples):
        hasher.update(line.encode("utf-8"))
        hasher.update(b"\n")
    return hasher.hexdigest()


def draw_pilot(
    examples: Sequence[DatasetExample],
    corpus: Mapping[str, CorpusDocument] | None = None,
    *,
    size: int = DEFAULT_PILOT_SIZE,
    seed: int,
) -> list[ReviewedExample]:
    """Draw ``size`` examples, **stratified by type and split**, reproducibly from ``seed``.

    Stratified for the same reason M1.11 stratifies by source: a uniform draw over a dataset that
    is 40 % ``qa`` returns mostly ``qa``, and the review would say nothing about whether
    ``no_ho_se`` actually declines or ``traduccio`` is any good. ``allocate`` guarantees at least
    one of every stratum present, so neither a type nor the frozen ``test`` split escapes the gate.

    Each row carries its grounding text, because "is this factually correct?" cannot be answered
    without it. A cited passage missing from ``corpus`` is rendered as an explicit marker rather
    than silently omitted — a reviewer must never mark something factual against no evidence.
    """
    pool = list(examples)
    if len(pool) <= size:
        chosen = pool
    else:
        strata: dict[str, list[DatasetExample]] = {}
        for item in pool:
            strata.setdefault(stratum_of(item), []).append(item)
        for group in strata.values():
            group.sort(key=lambda item: str(item.id))
        allocation = allocate(Counter({key: len(value) for key, value in strata.items()}), size)
        rng = Random(seed)
        chosen = []
        for stratum in sorted(allocation):
            chosen.extend(rng.sample(strata[stratum], allocation[stratum]))

    ordered = sorted(chosen, key=lambda item: (item.type.value, item.split.value, str(item.id)))
    return [
        ReviewedExample(
            example=item,
            passages=_passages_of(item, corpus),
            # A type that is not meant to sound Andorran is not asked to.
            andorran=Label.NA if item.type is ExampleType.GENERAL_CA else Label.PENDING,
        )
        for item in ordered
    ]


def _passages_of(
    example: DatasetExample, corpus: Mapping[str, CorpusDocument] | None
) -> tuple[str, ...]:
    """The grounding text a reviewer needs, or an explicit marker where it is missing."""
    if corpus is None:
        return ()
    return tuple(
        corpus[ident].text
        if ident in corpus
        else f"[MISSING FROM CORPUS: {ident[:16]}… — cannot verify this example]"
        for ident in example.grounding_ids
    )


def to_csv(sample: Sequence[ReviewedExample], *, seed: int, digest: str = "") -> str:
    """The fillable review sheet.

    ``digest`` pins the sheet to the dataset it was drawn from — see :func:`dataset_digest`.
    """
    buffer = io.StringIO()
    buffer.write(f"# MAIA review sheet (M2.06 / M2.10) — {len(sample)} examples, seed {seed}\n")
    buffer.write(f"# dataset-digest: {digest}\n")
    buffer.write(
        f"# factual/catalan/andorran: yes | no | na. Bars: factual >={MIN_FACTUAL_RATE:.0%}, "
        f"catalan >={MIN_CATALAN_RATE:.0%}, andorran >={MIN_ANDORRAN_RATE:.0%}\n"
    )
    writer = csv.DictWriter(buffer, fieldnames=FIELDNAMES, lineterminator="\n")
    writer.writeheader()
    for item in sample:
        writer.writerow(
            {
                "id": str(item.example.id),
                "type": item.example.type.value,
                "topic": item.example.topic,
                "judge_score": f"{item.example.judge_score:.3f}",
                # Carried so the sheet is auditable against the corpus, and so the row can be
                # read back as a valid §3.2 example — the schema requires grounded types to cite.
                "grounding_ids": " ".join(item.example.grounding_ids),
                "conversation": conversation_of(item.example),
                "passages": "\n\n---\n\n".join(item.passages),
                "factual": item.factual.value,
                "catalan": item.catalan.value,
                "andorran": item.andorran.value,
                "note": item.note,
            }
        )
    return buffer.getvalue()


def digest_in(raw: str) -> str:
    """The ``dataset-digest`` a sheet declares, or ``""`` if it declares none."""
    for line in raw.splitlines():
        if line.startswith("# dataset-digest:"):
            return line.split(":", 1)[1].strip()
        if not line.startswith("#"):
            break
    return ""


def from_csv(raw: str) -> list[ReviewedExample]:
    """Read a filled-in review sheet back.

    Raises:
        ValueError: on a missing column, an unrecognised label, or a row that is not a valid §3.2
            example. A typo must not quietly become a ``yes``.
    """
    lines = [line for line in raw.splitlines(keepends=True) if not line.startswith("#")]
    reader = csv.DictReader(io.StringIO("".join(lines)))
    if reader.fieldnames is None:
        return []
    missing = set(FIELDNAMES) - set(reader.fieldnames)
    if missing:
        raise ValueError(f"review sheet is missing column(s): {', '.join(sorted(missing))}")

    reviewed: list[ReviewedExample] = []
    for number, row in enumerate(reader, start=1):
        labels = {
            column: _label(row.get(column), number, row.get("id", "?"))
            for column in ("factual", "catalan", "andorran")
        }
        reviewed.append(
            ReviewedExample(
                example=_example_of(row, number),
                passages=tuple(
                    part for part in (row.get("passages") or "").split("\n\n---\n\n") if part
                ),
                note=(row.get("note") or "").strip(),
                **labels,
            )
        )
    return reviewed


def _label(raw: str | None, row: int, identifier: str) -> Label:
    """One cell, or an error naming the row."""
    value = (raw or "").strip().lower()
    try:
        return Label(value)
    except ValueError as error:
        allowed = ", ".join(item.value for item in Label)
        raise ValueError(
            f"row {row} ({identifier[:12]}...): unrecognised label {value!r}; expected {allowed}"
        ) from error


def _example_of(row: Mapping[str, str], number: int) -> DatasetExample:
    """Rebuild the §3.2 example from a review row.

    The sheet holds a rendered conversation rather than the message list, so the example is
    reconstructed from the fields the score actually needs: id, type, ``judge_score`` and the
    grounding ids §3.2 requires a grounded type to cite. The conversation is carried for the
    reviewer, not for the arithmetic — hence the placeholder messages.
    """
    try:
        return DatasetExample.model_validate(
            {
                "id": row["id"],
                "messages": [
                    {"role": "user", "content": row.get("conversation") or "-"},
                    {"role": "assistant", "content": "-"},
                ],
                "type": row["type"],
                "topic": row["topic"],
                "grounding_ids": (row.get("grounding_ids") or "").split(),
                "generator": "review-sheet",
                "judge_score": float(row.get("judge_score") or 0.0),
                "split": "train",
            }
        )
    except (ValueError, KeyError) as error:
        raise ValueError(f"row {number}: not a readable review row: {error}") from error


def to_markdown(sample: Sequence[ReviewedExample], *, seed: int) -> str:
    """A reading companion — the pilot laid out for humans, passages beside each answer."""
    lines = [
        "# MAIA dataset pilot (M2.06)",
        "",
        f"{len(sample)} examples, drawn with seed `{seed}`, stratified by type.",
        "",
        "Fill three columns per example in the CSV sheet:",
        "",
        f"- **`factual`** - is every claim supported by the passages below it? Bar: "
        f">={MIN_FACTUAL_RATE:.0%} (DoD-F2).",
        f"- **`catalan`** - is the Catalan correct? Bar: >={MIN_CATALAN_RATE:.0%} (DoD-F2).",
        f"- **`andorran`** - does it sound Andorran rather than like Viquipèdia? Bar: "
        f">={MIN_ANDORRAN_RATE:.0%}.",
        "",
        "Use `na` where a question does not apply. For a `no_ho_se` example, *factual* means: is "
        "declining the right answer given these passages?",
        "",
    ]
    by_type = Counter(item.example.type.value for item in sample)
    lines += ["| type | sampled |", "| --- | --: |"]
    lines += [f"| `{kind}` | {count} |" for kind, count in sorted(by_type.items())]
    lines.append("")

    for index, item in enumerate(sample, start=1):
        example = item.example
        lines += [
            "---",
            "",
            f"### {index}. `{example.type.value}` · {example.topic}",
            "",
            f"- id: `{example.id}`",
            f"- judge_score: {example.judge_score:.3f}"
            + ("  _(exempt - not judged)_" if is_exempt(example) else ""),
            "",
            "**Conversation**",
            "",
            "```text",
            conversation_of(example),
            "```",
            "",
        ]
        if item.passages:
            lines += ["**Grounding passages**", ""]
            for passage in item.passages:
                lines += ["```text", passage, "```", ""]
        elif example.grounding_ids:
            lines += ["> ⚠ grounding passages not supplied - factual review is not possible.", ""]
        else:
            lines += ["> This type cites no passages by construction.", ""]
    return "\n".join(lines) + "\n"


@dataclass(frozen=True)
class Rate:
    """One reviewed question: how many said yes, out of how many were asked."""

    yes: int
    no: int
    not_applicable: int
    bar: float

    @property
    def asked(self) -> int:
        """How many examples this question actually applied to."""
        return self.yes + self.no

    @property
    def rate(self) -> float:
        """Share of applicable examples answered yes."""
        return self.yes / self.asked if self.asked else 0.0

    @property
    def passed(self) -> bool:
        """Whether this bar is met. An unasked question does not pass by default."""
        return self.asked > 0 and self.rate >= self.bar


@dataclass(frozen=True)
class Calibration:
    """Where the ``judge_score`` threshold should sit, according to the humans."""

    threshold: float | None
    factual_rate: float
    support: int
    retained: float
    achievable: bool
    agreement: float
    judged: int
    excluded_exempt: int
    curve: tuple[tuple[float, float, int], ...] = ()

    @property
    def summary(self) -> str:
        """One line a human can act on."""
        if not self.achievable:
            return (
                f"no threshold reaches {MIN_FACTUAL_RATE:.0%} factual on >={MIN_SUPPORT} "
                "examples - the judge cannot gate this dataset; keep human review in the loop"
            )
        return (
            f"threshold {self.threshold:.2f} -> {self.factual_rate:.1%} factual on "
            f"{self.support} example(s), retaining {self.retained:.1%} of the judged pilot"
        )


def calibrate(
    reviewed: Sequence[ReviewedExample],
    *,
    bar: float = MIN_FACTUAL_RATE,
    min_support: int = MIN_SUPPORT,
    candidates: Sequence[float] = CANDIDATE_THRESHOLDS,
) -> Calibration:
    """Find the **lowest** ``judge_score`` threshold whose survivors clear ``bar``.

    Lowest, because any higher threshold discards good examples for no gain in quality. Only
    examples that were actually judged take part — see the module docstring for the three ways this
    could otherwise flatter itself.
    """
    judged = [
        item
        for item in reviewed
        if not is_exempt(item.example) and item.factual in {Label.YES, Label.NO}
    ]
    excluded = sum(1 for item in reviewed if is_exempt(item.example))

    curve: list[tuple[float, float, int]] = []
    best: tuple[float, float, int] | None = None
    for threshold in candidates:
        surviving = [item for item in judged if item.example.judge_score >= threshold]
        if not surviving:
            continue
        rate = sum(1 for item in surviving if item.factual is Label.YES) / len(surviving)
        curve.append((threshold, rate, len(surviving)))
        if best is None and rate >= bar and len(surviving) >= min_support:
            best = (threshold, rate, len(surviving))

    if best is None:
        return Calibration(
            threshold=None,
            factual_rate=0.0,
            support=0,
            retained=0.0,
            achievable=False,
            agreement=_agreement(judged),
            judged=len(judged),
            excluded_exempt=excluded,
            curve=tuple(curve),
        )
    threshold, rate, support = best
    return Calibration(
        threshold=threshold,
        factual_rate=rate,
        support=support,
        retained=support / len(judged) if judged else 0.0,
        achievable=True,
        agreement=_agreement(judged),
        judged=len(judged),
        excluded_exempt=excluded,
        curve=tuple(curve),
    )


def _agreement(judged: Sequence[ReviewedExample], threshold: float = 0.7) -> float:
    """How often the judge and the human agree at ``threshold`` — is the judge worth anything?

    A calibrated threshold with poor agreement means the judge is sorting on something other than
    factual support, and the number should not be trusted just because the arithmetic worked.
    """
    if not judged:
        return 0.0
    agreed = sum(
        1
        for item in judged
        if (item.example.judge_score >= threshold) == (item.factual is Label.YES)
    )
    return agreed / len(judged)


@dataclass
class PilotResult:
    """The outcome of a completed pilot review."""

    reviewed: int
    factual: Rate
    catalan: Rate
    andorran: Rate
    calibration: Calibration
    by_type: dict[str, tuple[int, int]] = field(default_factory=dict)
    notes: list[tuple[str, str]] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        """Whether the pilot gate is met on every axis.

        The PO's OK is still required and cannot be computed — this only says whether the numbers
        stand in its way.
        """
        return self.factual.passed and self.catalan.passed and self.andorran.passed


def score(
    reviewed: Sequence[ReviewedExample],
    *,
    min_factual: float = MIN_FACTUAL_RATE,
    min_catalan: float = MIN_CATALAN_RATE,
    min_andorran: float = MIN_ANDORRAN_RATE,
) -> PilotResult:
    """Score a completed pilot review.

    Raises:
        IncompleteReviewError: if any answer is still ``pending``. A half-finished review must
            never read as a pass — the one way this gate could quietly fail.
        ValueError: if there is nothing to score.
    """
    if not reviewed:
        raise ValueError("nothing to score: the pilot is empty")
    pending = [item for item in reviewed if Label.PENDING in item.answers]
    if pending:
        raise IncompleteReviewError(
            f"{len(pending)} of {len(reviewed)} example(s) still pending review; "
            "score only a completed sheet"
        )

    by_type: dict[str, tuple[int, int]] = {}
    for item in reviewed:
        good, bad = by_type.get(item.example.type.value, (0, 0))
        if item.factual is Label.NO:
            by_type[item.example.type.value] = (good, bad + 1)
        else:
            by_type[item.example.type.value] = (good + 1, bad)

    return PilotResult(
        reviewed=len(reviewed),
        factual=_rate(reviewed, "factual", min_factual),
        catalan=_rate(reviewed, "catalan", min_catalan),
        andorran=_rate(reviewed, "andorran", min_andorran),
        calibration=calibrate(reviewed, bar=min_factual),
        by_type=by_type,
        notes=[
            (str(item.example.id), item.note)
            for item in reviewed
            if item.note and Label.NO in item.answers
        ],
    )


def _rate(reviewed: Iterable[ReviewedExample], column: str, bar: float) -> Rate:
    """Tally one question."""
    labels = [getattr(item, column) for item in reviewed]
    return Rate(
        yes=sum(1 for label in labels if label is Label.YES),
        no=sum(1 for label in labels if label is Label.NO),
        not_applicable=sum(1 for label in labels if label is Label.NA),
        bar=bar,
    )


def render(result: PilotResult) -> str:
    """Human-readable verdict on the pilot gate."""
    status = "✓ PASS" if result.passed else "✗ FAIL"
    lines = [f"{status} — pilot of {result.reviewed} example(s)"]
    for name, rate in (
        ("factual", result.factual),
        ("catalan", result.catalan),
        ("andorran", result.andorran),
    ):
        mark = "✓" if rate.passed else "✗"
        applicable = f", {rate.not_applicable} n/a" if rate.not_applicable else ""
        lines.append(
            f"  {mark} {name}: {rate.yes}/{rate.asked} ({rate.rate:.1%}, bar "
            f">={rate.bar:.0%}{applicable})"
        )
    lines.append(f"  threshold: {result.calibration.summary}")
    lines.append(
        f"  judge/human agreement at 0.70: {result.calibration.agreement:.1%} over "
        f"{result.calibration.judged} judged example(s), "
        f"{result.calibration.excluded_exempt} exempt excluded"
    )
    for kind, (good, bad) in sorted(result.by_type.items()):
        if bad:
            lines.append(f"    {kind}: {bad}/{good + bad} not factual")
    if result.notes:
        lines.append("  flagged:")
        lines += [f"    {ident[:12]}... {note}" for ident, note in result.notes[:10]]
    lines.append(
        "  PO OK is still required and is not computable — this only says whether the numbers "
        "stand in its way (M2.06 is a PO-blocking gate)"
    )
    return "\n".join(lines)


#: DoD-F2 asks for a 200-example human sample as the Phase 2 exit gate.
DOD_SAMPLE_SIZE = 200


class DigestMismatchError(RuntimeError):
    """Raised when a filled sheet was drawn from a different dataset than the one being scored."""


def verify_sheet(raw: str, examples: Iterable[DatasetExample]) -> None:
    """Check a filled sheet was drawn from ``examples``.

    Raises:
        DigestMismatchError: if the sheet declares a digest that does not match, or declares none
            at all when one is being demanded. A review scored against a dataset that has since
            changed is not evidence, and DoD-F2 is a phase exit — the number has to be auditable
            after the fact.
    """
    declared = digest_in(raw)
    actual = dataset_digest(examples)
    if not declared:
        raise DigestMismatchError(
            "the review sheet declares no dataset-digest, so nothing ties it to the dataset it "
            "is being scored against; re-draw it with a current version of this tool"
        )
    if declared != actual:
        raise DigestMismatchError(
            f"the sheet was drawn from dataset {declared[:16]}... but this dataset is "
            f"{actual[:16]}... — the dataset changed after the review; re-draw and re-review, or "
            "score against the dataset that was actually reviewed"
        )


def evidence(result: PilotResult, *, digest: str, seed: int, size: int) -> str:
    """The DoD-F2 evidence artifact, as Markdown.

    A gate that passes without a record of *what* passed cannot be relied on later, so this pins
    the dataset digest, the seed and the sample size beside the rates.
    """
    status = "PASS" if result.passed else "FAIL"
    lines = [
        "# DoD-F2 — human sample (M2.10)",
        "",
        f"**{status}** on {result.reviewed} reviewed example(s).",
        "",
        "| axis | yes | asked | rate | bar | verdict |",
        "| --- | --: | --: | --: | --: | :-: |",
    ]
    for name, rate in (
        ("factually correct", result.factual),
        ("correct Catalan", result.catalan),
        ("sounds Andorran", result.andorran),
    ):
        lines.append(
            f"| {name} | {rate.yes} | {rate.asked} | {rate.rate:.1%} | "
            f">={rate.bar:.0%} | {'✓' if rate.passed else '✗'} |"
        )
    lines += [
        "",
        "## Provenance",
        "",
        f"- dataset digest: `{digest}`",
        f"- sample: {size} example(s), seed `{seed}`, stratified by type and split",
        f"- judge threshold suggested by these labels: {result.calibration.summary}",
        f"- judge/human agreement at 0.70: {result.calibration.agreement:.1%} over "
        f"{result.calibration.judged} judged example(s)",
        "",
        "## Notes",
        "",
    ]
    lines += (
        [f"- `{ident[:12]}...` {note}" for ident, note in result.notes]
        if result.notes
        else ["- none recorded."]
    )
    lines += [
        "",
        "> The PO's sign-off is required and is not computable from these numbers; this artifact "
        "records only whether they stand in its way.",
        "",
    ]
    return "\n".join(lines)


def read_dataset(path: Path) -> list[DatasetExample]:
    """Read a §3.2 dataset from JSONL."""
    return [
        DatasetExample.model_validate_json(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def read_corpus(paths: Sequence[Path]) -> dict[str, CorpusDocument]:
    """Index §3.1 corpus documents by id, for the grounding passages."""
    documents = (
        CorpusDocument.model_validate_json(line)
        for path in paths
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    )
    return {document.id: document for document in documents}


def _draw(args: argparse.Namespace) -> int:
    """``draw`` subcommand: write the review package."""
    for path in [args.dataset, *(args.corpus or [])]:
        if not path.is_file():
            print(f"error: no such file: {path}", file=sys.stderr)
            return 1
    examples = read_dataset(args.dataset)
    corpus = read_corpus(args.corpus) if args.corpus else None
    if corpus is None:
        print(
            "warning: no --corpus given, so the sheet carries no grounding passages and the "
            "factual column cannot honestly be filled",
            file=sys.stderr,
        )
    sample = draw_pilot(examples, corpus, size=args.size, seed=args.seed)
    digest = dataset_digest(examples)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(to_csv(sample, seed=args.seed, digest=digest), encoding="utf-8")
    companion = args.out.with_suffix(".md")
    companion.write_text(to_markdown(sample, seed=args.seed), encoding="utf-8")
    missing = sum(1 for item in sample for passage in item.passages if "MISSING FROM" in passage)
    print(f"wrote {len(sample)} example(s) to {args.out} and {companion}")
    print(f"dataset digest: {digest}")
    if missing:
        print(f"⚠ {missing} cited passage(s) are missing from the corpus and are marked as such")
    return 0


def _score(args: argparse.Namespace) -> int:
    """``score`` subcommand: read a filled sheet and rule on the gate."""
    for path in (args.sheet, *([args.dataset] if args.dataset else ())):
        if not path.is_file():
            print(f"error: no such file: {path}", file=sys.stderr)
            return 1
    raw = args.sheet.read_text(encoding="utf-8")
    try:
        if args.dataset:
            verify_sheet(raw, read_dataset(args.dataset))
        reviewed = from_csv(raw)
        result = score(reviewed)
    except (ValueError, IncompleteReviewError, DigestMismatchError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    if args.evidence:
        if not args.dataset:
            print(
                "error: --evidence needs --dataset, or the artifact would record a provenance it "
                "never checked",
                file=sys.stderr,
            )
            return 1
        args.evidence.parent.mkdir(parents=True, exist_ok=True)
        args.evidence.write_text(
            evidence(
                result,
                digest=digest_in(raw),
                seed=args.seed,
                size=result.reviewed,
            ),
            encoding="utf-8",
        )
        print(f"wrote DoD-F2 evidence to {args.evidence}")

    print(render(result))
    return 0 if result.passed else 1


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point: ``draw`` a pilot for review, then ``score`` the filled sheet."""
    parser = argparse.ArgumentParser(
        description="Human review of a §3.2 dataset. Draw a stratified sample, then score the "
        "filled sheet and calibrate the judge_score threshold against the human labels. "
        f"--size {DEFAULT_PILOT_SIZE} is the M2.06 pilot gate; --size {DOD_SAMPLE_SIZE} with "
        "--evidence is the M2.10 DoD-F2 exit gate."
    )
    subcommands = parser.add_subparsers(dest="command", required=True)

    draw = subcommands.add_parser("draw", help="write the review package")
    draw.add_argument("dataset", type=Path, help="the generated §3.2 dataset (JSONL)")
    draw.add_argument("--corpus", type=Path, nargs="+", help="§3.1 corpus JSONL, for the passages")
    draw.add_argument("--out", type=Path, default=Path("pilot.csv"))
    draw.add_argument(
        "--size",
        type=int,
        default=DEFAULT_PILOT_SIZE,
        help=f"{DEFAULT_PILOT_SIZE} for the M2.06 pilot, {DOD_SAMPLE_SIZE} for the M2.10 DoD-F2 "
        "sample",
    )
    draw.add_argument("--seed", type=int, default=20260725)
    draw.set_defaults(handler=_draw)

    scoring = subcommands.add_parser("score", help="score a filled review sheet")
    scoring.add_argument("sheet", type=Path, help="the filled-in CSV")
    scoring.add_argument(
        "--dataset",
        type=Path,
        help="the dataset the sheet was drawn from; verifies the sheet's dataset-digest",
    )
    scoring.add_argument(
        "--evidence",
        type=Path,
        help="write the DoD-F2 evidence artifact here (M2.10); requires --dataset",
    )
    scoring.add_argument("--seed", type=int, default=20260725, help="recorded in the evidence")
    scoring.set_defaults(handler=_score)

    args = parser.parse_args(argv)
    handler: object = args.handler
    assert callable(handler)
    result = handler(args)
    assert isinstance(result, int)
    return result


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
