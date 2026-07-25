"""PO quality sampling — PLAN M1.11.

The last F1 gate: *"PO sampling of 50 random docs ≥95 % clean"*. The judgement is the PO's
and cannot be automated — the compliance article is explicit that *"the PO domain sampling is
irreplaceable"* — so this module does the three things around it that **can** be got wrong:

1. **Draw a sample that represents the corpus.** A uniform random draw over a corpus that is
   mostly Viquipèdia returns mostly Viquipèdia, and a 96 % clean rate on Viquipèdia says
   nothing about whether the legal or spoken subcorpora are usable. :func:`draw_sample` is
   **stratified by source**, allocating proportionally by largest remainder and guaranteeing
   at least one document per source, so every subcorpus is actually looked at.
2. **Make the draw reproducible.** The seed is an argument and is recorded in the review
   sheet. A gate whose sample cannot be reproduced is not evidence; if the PO's verdict is
   ever questioned, the same 50 documents can be drawn again.
3. **Score it without wishful arithmetic.** :func:`score` refuses to compute a rate while any
   verdict is still ``pending``, so a half-finished review can never read as a pass, and an
   unrecognised verdict is an error rather than a silent zero.

The review sheet is CSV: it opens in any spreadsheet, the PO types in one column, and Python
round-trips it including the embedded newlines of the document text. A markdown companion is
produced for comfortable reading of long documents.
"""

from __future__ import annotations

import argparse
import csv
import io
import sys
from collections import Counter
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from random import Random

from maia.corpus.consolidate import ConsolidationReport, read_documents
from maia.schemas import CorpusDocument

#: F1's bar: at least this share of the sampled documents must be clean.
DEFAULT_MIN_CLEAN_RATE = 0.95

#: F1 asks for 50 documents.
DEFAULT_SAMPLE_SIZE = 50

#: Columns of the review sheet. ``verdict`` and ``note`` are the PO's to fill.
FIELDNAMES = ("id", "source", "license", "registre", "url", "verdict", "note", "text")


class Verdict(StrEnum):
    """The PO's judgement on one sampled document."""

    PENDING = "pending"
    CLEAN = "clean"
    DIRTY = "dirty"


@dataclass(frozen=True)
class SampledDocument:
    """One document drawn for review, with the PO's verdict once given."""

    document: CorpusDocument
    verdict: Verdict = Verdict.PENDING
    note: str = ""


class IncompleteReviewError(RuntimeError):
    """Raised when a sample is scored while verdicts are still ``pending``."""


def allocate(counts: Counter[str], size: int) -> dict[str, int]:
    """Split ``size`` across sources proportionally to ``counts``.

    Largest-remainder allocation, then a guarantee of **at least one per source** so a small
    subcorpus is never invisible to the review — which is the whole point of stratifying. If
    there are more sources than slots, the largest sources win the slots, because with fewer
    slots than strata something has to give and under-sampling the big ones would be worse.
    No source is ever allocated more documents than it has.
    """
    if size <= 0 or not counts:
        return {}

    total = sum(counts.values())
    if total <= size:
        return dict(counts)

    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    if len(ordered) > size:
        return {source: 1 for source, _ in ordered[:size]}

    exact = {source: size * count / total for source, count in ordered}
    allocation = {source: max(1, int(share)) for source, share in exact.items()}

    # Trim or pad to exactly `size`, always respecting the floor of 1 and each source's stock.
    while sum(allocation.values()) > size:
        candidates = [s for s in allocation if allocation[s] > 1]
        victim = max(candidates, key=lambda s: (allocation[s] - exact[s], s))
        allocation[victim] -= 1
    while sum(allocation.values()) < size:
        candidates = [s for s in allocation if allocation[s] < counts[s]]
        if not candidates:  # pragma: no cover — termination guard, see below
            # Unreachable: we returned early when the corpus was no larger than `size`, so
            # sum(counts) > size > sum(allocation) here and some source must still have
            # stock. Kept anyway, because being wrong about that would mean an infinite loop
            # rather than a slightly wrong sample.
            break
        winner = max(candidates, key=lambda s: (exact[s] - allocation[s], s))
        allocation[winner] += 1
    return allocation


def draw_sample(
    documents: Iterable[CorpusDocument],
    *,
    size: int = DEFAULT_SAMPLE_SIZE,
    seed: int,
    stratify: bool = True,
) -> list[SampledDocument]:
    """Draw ``size`` documents for review, stratified by source and reproducible from ``seed``.

    Returns the whole corpus when it is smaller than ``size`` — there is nothing to sample.
    The result is ordered by source then by id, so the review sheet groups a reviewer's
    attention rather than making them context-switch every row.
    """
    pool = list(documents)
    if len(pool) <= size:
        return [SampledDocument(doc) for doc in sorted(pool, key=lambda d: (d.source.value, d.id))]

    rng = Random(seed)
    if not stratify:
        chosen = rng.sample(pool, size)
    else:
        by_source: dict[str, list[CorpusDocument]] = {}
        for doc in pool:
            by_source.setdefault(doc.source.value, []).append(doc)
        # Sort each stratum so the draw depends only on the seed, not on input order.
        for docs in by_source.values():
            docs.sort(key=lambda d: d.id)

        allocation = allocate(Counter({k: len(v) for k, v in by_source.items()}), size)
        chosen = []
        for source in sorted(allocation):
            chosen.extend(rng.sample(by_source[source], allocation[source]))

    return [SampledDocument(doc) for doc in sorted(chosen, key=lambda d: (d.source.value, d.id))]


def to_csv(sample: Sequence[SampledDocument], *, seed: int) -> str:
    """The fillable review sheet.

    The seed rides along in a comment row so the sheet is self-describing: whoever reads the
    verdicts later can redraw exactly this sample.
    """
    buffer = io.StringIO()
    buffer.write(f"# maia corpus review sheet — seed={seed}, documents={len(sample)}\n")
    writer = csv.DictWriter(buffer, fieldnames=FIELDNAMES, lineterminator="\n")
    writer.writeheader()
    for item in sample:
        doc = item.document
        writer.writerow(
            {
                "id": doc.id,
                "source": doc.source.value,
                "license": doc.license.value,
                "registre": doc.registre.value,
                "url": str(doc.url),
                "verdict": item.verdict.value,
                "note": item.note,
                "text": doc.text,
            }
        )
    return buffer.getvalue()


def from_csv(raw: str) -> list[SampledDocument]:
    """Read a filled-in review sheet back.

    Raises:
        ValueError: if a row carries an unrecognised verdict. Treating an unknown value as
            anything other than an error would let a typo silently become a clean document.
    """
    lines = [line for line in raw.splitlines(keepends=True) if not line.startswith("#")]
    reader = csv.DictReader(io.StringIO("".join(lines)))
    if reader.fieldnames is None:
        return []
    missing = set(FIELDNAMES) - set(reader.fieldnames)
    if missing:
        raise ValueError(f"review sheet is missing column(s): {', '.join(sorted(missing))}")

    sample: list[SampledDocument] = []
    for number, row in enumerate(reader, start=1):
        raw_verdict = (row.get("verdict") or "").strip().lower()
        try:
            verdict = Verdict(raw_verdict)
        except ValueError as exc:
            allowed = ", ".join(v.value for v in Verdict)
            raise ValueError(
                f"row {number} ({row.get('id', '?')[:12]}…): unrecognised verdict "
                f"{raw_verdict!r}; expected one of {allowed}"
            ) from exc
        document = CorpusDocument.model_validate(
            {
                "id": row["id"],
                "text": row["text"],
                "source": row["source"],
                "url": row["url"],
                # The sheet is a review artifact, not a corpus file: it carries no timestamp,
                # so a fixed epoch stands in. Only id/text/source/licence drive the score.
                "fetched_at": "1970-01-01T00:00:00Z",
                "license": row["license"],
                "registre": row["registre"],
            }
        )
        sample.append(
            SampledDocument(document, verdict=verdict, note=(row.get("note") or "").strip())
        )
    return sample


def to_markdown(sample: Sequence[SampledDocument], *, seed: int) -> str:
    """A reading companion — the same sample, laid out for a human to actually read."""
    lines = [
        "# Corpus review sample (M1.11)",
        "",
        f"{len(sample)} documents, drawn with seed `{seed}`, stratified by source.",
        "",
        "For each document below, mark `clean` or `dirty` in the **`verdict`** column of the "
        f"CSV sheet. F1 passes at **≥{DEFAULT_MIN_CLEAN_RATE:.0%} clean**.",
        "",
        "A document is *dirty* if it is boilerplate, wrong-language, truncated, garbled, "
        "duplicated content, or not about Andorra at all.",
        "",
    ]
    by_source = Counter(item.document.source.value for item in sample)
    lines += ["| source | sampled |", "| --- | --: |"]
    lines += [f"| `{source}` | {count} |" for source, count in sorted(by_source.items())]
    lines.append("")

    for index, item in enumerate(sample, start=1):
        doc = item.document
        lines += [
            "---",
            "",
            f"### {index}. `{doc.source.value}` · `{doc.license.value}` · `{doc.registre.value}`",
            "",
            f"- id: `{doc.id[:16]}…`",
            f"- url: {doc.url}",
        ]
        if doc.speaker:
            lines.append(f"- speaker: {doc.speaker}")
        if doc.legal:
            llei = doc.legal.llei or doc.legal.rang.value
            lines.append(
                f"- legal: {llei}, article {doc.legal.article} "
                f"(consolidated {doc.legal.consolidacio_data.isoformat()})"
            )
        lines += ["", "```text", doc.text, "```", ""]
    return "\n".join(lines) + "\n"


@dataclass(frozen=True)
class SamplingResult:
    """The outcome of a completed review."""

    reviewed: int
    clean: int
    dirty: int
    min_clean_rate: float
    by_source: dict[str, tuple[int, int]]
    notes: list[tuple[str, str]]

    @property
    def clean_rate(self) -> float:
        """Share of reviewed documents judged clean."""
        return self.clean / self.reviewed if self.reviewed else 0.0

    @property
    def passed(self) -> bool:
        """Whether the F1 sampling gate is met."""
        return self.reviewed > 0 and self.clean_rate >= self.min_clean_rate


def score(
    sample: Sequence[SampledDocument], *, min_clean_rate: float = DEFAULT_MIN_CLEAN_RATE
) -> SamplingResult:
    """Score a completed review.

    Raises:
        IncompleteReviewError: if any verdict is still ``pending``. A partial review must not
            be able to read as a pass — that is the one way this gate could quietly fail.
        ValueError: if the sample is empty.
    """
    if not sample:
        raise ValueError("nothing to score: the sample is empty")
    pending = [item for item in sample if item.verdict is Verdict.PENDING]
    if pending:
        raise IncompleteReviewError(
            f"{len(pending)} of {len(sample)} document(s) still pending review; "
            "score only a completed sheet"
        )

    by_source: dict[str, tuple[int, int]] = {}
    for item in sample:
        clean, dirty = by_source.get(item.document.source.value, (0, 0))
        if item.verdict is Verdict.CLEAN:
            by_source[item.document.source.value] = (clean + 1, dirty)
        else:
            by_source[item.document.source.value] = (clean, dirty + 1)

    return SamplingResult(
        reviewed=len(sample),
        clean=sum(1 for item in sample if item.verdict is Verdict.CLEAN),
        dirty=sum(1 for item in sample if item.verdict is Verdict.DIRTY),
        min_clean_rate=min_clean_rate,
        by_source=by_source,
        notes=[
            (item.document.id, item.note)
            for item in sample
            if item.verdict is Verdict.DIRTY and item.note
        ],
    )


def render(result: SamplingResult) -> str:
    """Human-readable verdict on the sampling gate."""
    status = "✓ PASS" if result.passed else "✗ FAIL"
    lines = [
        f"{status} — {result.clean}/{result.reviewed} clean "
        f"({result.clean_rate:.1%}, gate ≥{result.min_clean_rate:.0%})",
    ]
    for source, (clean, dirty) in sorted(result.by_source.items()):
        total = clean + dirty
        lines.append(f"  {source}: {clean}/{total} clean ({clean / total:.0%})")
    if result.notes:
        lines.append("  flagged:")
        lines += [f"    {doc_id[:12]}… {note}" for doc_id, note in result.notes]
    return "\n".join(lines)


def _load(paths: Sequence[Path]) -> list[CorpusDocument] | None:
    """Read and validate corpus inputs, or ``None`` if any line failed."""
    report = ConsolidationReport()
    documents = read_documents(paths, report)
    if report.invalid:
        print(f"error: {len(report.invalid)} line(s) failed §3.1 validation", file=sys.stderr)
        for error in report.invalid[:20]:
            print(f"  ✗ line {error.line}: {error.reason}", file=sys.stderr)
        return None
    return documents


def _draw(args: argparse.Namespace) -> int:
    documents = _load(args.inputs)
    if documents is None:
        return 1
    if not documents:
        print("error: the corpus is empty", file=sys.stderr)
        return 1

    sample = draw_sample(documents, size=args.size, seed=args.seed, stratify=not args.uniform)
    args.csv_path.parent.mkdir(parents=True, exist_ok=True)
    args.csv_path.write_text(to_csv(sample, seed=args.seed), encoding="utf-8")
    if args.markdown:
        args.markdown.parent.mkdir(parents=True, exist_ok=True)
        args.markdown.write_text(to_markdown(sample, seed=args.seed), encoding="utf-8")

    by_source = Counter(item.document.source.value for item in sample)
    spread = ", ".join(f"{source}={count}" for source, count in sorted(by_source.items()))
    print(f"drew {len(sample)} documents (seed {args.seed}): {spread}")
    print(f"  → {args.csv_path}")
    if args.markdown:
        print(f"  → {args.markdown}")
    return 0


def _score(args: argparse.Namespace) -> int:
    try:
        sample = from_csv(args.sheet.read_text(encoding="utf-8"))
        result = score(sample, min_clean_rate=args.min_clean_rate)
    except (ValueError, IncompleteReviewError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(render(result))
    return 0 if result.passed else 1


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point: ``draw`` a review sample, or ``score`` a completed sheet."""
    parser = argparse.ArgumentParser(
        description="Draw a stratified corpus sample for PO review, and score the result "
        "against the F1 gate."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    draw = sub.add_parser("draw", help="draw a review sample")
    draw.add_argument("inputs", type=Path, nargs="+", help="consolidated JSONL corpus files")
    draw.add_argument("--csv", type=Path, dest="csv_path", required=True, help="review sheet out")
    draw.add_argument("--markdown", type=Path, help="also write a reading companion")
    draw.add_argument("--size", type=int, default=DEFAULT_SAMPLE_SIZE, help="documents to draw")
    draw.add_argument("--seed", type=int, required=True, help="makes the draw reproducible")
    draw.add_argument(
        "--uniform",
        action="store_true",
        help="draw uniformly instead of stratifying by source (not recommended: a "
        "uniform draw over an unbalanced corpus reviews only its largest source)",
    )
    draw.set_defaults(func=_draw)

    scorer = sub.add_parser("score", help="score a completed review sheet")
    scorer.add_argument("sheet", type=Path, help="the filled-in CSV review sheet")
    scorer.add_argument(
        "--min-clean-rate", type=float, default=DEFAULT_MIN_CLEAN_RATE, help="the gate"
    )
    scorer.set_defaults(func=_score)

    args = parser.parse_args(argv)
    if args.command == "draw":
        missing = [path for path in args.inputs if not path.is_file()]
        if missing:
            for path in missing:
                print(f"error: no such file: {path}", file=sys.stderr)
            return 1
    elif not args.sheet.is_file():
        print(f"error: no such file: {args.sheet}", file=sys.stderr)
        return 1

    exit_code: int = args.func(args)
    return exit_code


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
