"""Corpus consolidation pipeline — PLAN M1.08.

Takes the per-source JSONL files the scrapers produce and turns them into one consolidated,
deduplicated, schema-valid corpus, partitioned by source and ready for the private HF upload
(M1.09). The stages, in order, are the ones [Corpus — Phase 1] step 2 asks for:

1. **Read + validate** every line against §3.1 (a malformed line is reported, never guessed).
2. **Normalize** the text (Unicode NFC, invisibles, quotes, whitespace) — see
   :mod:`maia.corpus.clean`. This *changes the document id*, since the id is a hash of the
   normalized text, so each document is rebuilt through the schema rather than mutated.
   Normalizing first is what makes the next two stages work.
3. **Boilerplate filter** — drop navigation, cookie walls and one-phrase pages.
4. **Language filter** — drop documents that are clearly not Catalan.
5. **Exact dedup** by document id.
6. **Near-duplicate dedup** — MinHash + LSH, see :mod:`maia.corpus.dedup`.
7. **Write** one JSONL per source, plus a report of what each stage dropped.

Two rules exist to keep the pipeline from undoing decisions its producers made deliberately:

* **Length filtering is per source.** The juridical subcorpus is deliberately *not*
  length-filtered upstream (a one-line article is not boilerplate — see D-0009), so applying
  a 200-character floor here would delete exactly the articles chunk-by-article exists to
  preserve. :data:`MIN_CHARS_BY_SOURCE` overrides the default per source.
* **A document is dropped for language only when another language actually wins.** No signal
  (``und`` — a short article with no function words) is not evidence of a foreign language,
  and deleting a real document on absent evidence is the worse error.

When near-duplicates are collapsed, the survivor is chosen by :func:`survivor_rank`, which
puts **licence before length**: if a publishable document and a ``no-redistribute`` one are
near-duplicates, keeping the publishable one is the only safe choice, even if it is shorter.
Silently keeping the restricted copy would smuggle it into the public dataset at M1.09/M6.01.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from maia.corpus.clean import CleanVerdict, assess, clean_text
from maia.corpus.dedup import DEFAULT_CONFIG, MinHashConfig, NearDuplicateIndex, choose_survivors
from maia.corpus.language import detect_language
from maia.corpus.validate import LineError, validate_line
from maia.schemas import CorpusDocument, License, Source

#: Per-source minimum length, overriding :data:`DEFAULT_MIN_CHARS`. ``juridic`` is 1 because
#: the legal subcorpus is chunked by article and a short article must survive (D-0009).
MIN_CHARS_BY_SOURCE: dict[Source, int] = {Source.JURIDIC: 1}

#: Length floor for sources with no entry above.
DEFAULT_MIN_CHARS = 200


@dataclass(frozen=True)
class Dropped:
    """One document that did not make it, and why — the input to the M1.10 coverage report."""

    stage: str
    reason: str
    source: str
    url: str


@dataclass
class ConsolidationReport:
    """What each stage did. Every dropped document is accounted for."""

    read: int = 0
    kept: int = 0
    invalid: list[LineError] = field(default_factory=list)
    dropped: list[Dropped] = field(default_factory=list)
    by_source: Counter[str] = field(default_factory=Counter)
    by_license: Counter[str] = field(default_factory=Counter)

    @property
    def by_stage(self) -> Counter[str]:
        """How many documents each stage dropped."""
        return Counter(item.stage for item in self.dropped)

    @property
    def no_redistribute(self) -> int:
        """Surviving documents that must never enter public artifacts."""
        return self.by_license.get(License.NO_REDISTRIBUTE.value, 0)

    @property
    def balanced(self) -> bool:
        """Every document read is either kept, dropped, or invalid — nothing vanishes."""
        return self.read == self.kept + len(self.dropped) + len(self.invalid)


@dataclass(frozen=True)
class ConsolidationResult:
    """The surviving documents and the report explaining the rest."""

    documents: tuple[CorpusDocument, ...]
    report: ConsolidationReport


def renormalize(doc: CorpusDocument) -> CorpusDocument | None:
    """Rebuild ``doc`` with normalized text and a recomputed id.

    Returns ``None`` if nothing survives normalization. The document is re-validated through
    the schema rather than copied, because ``model_copy`` would keep the stale id — and a
    document whose id no longer matches its text is exactly what the §3.1 validator exists to
    catch.
    """
    cleaned = clean_text(doc.text)
    if not cleaned:
        return None
    data = doc.model_dump(mode="json")
    data["text"] = cleaned
    data["id"] = ""
    return CorpusDocument.model_validate(data)


def min_chars_for(source: Source) -> int:
    """The length floor that applies to ``source``."""
    return MIN_CHARS_BY_SOURCE.get(source, DEFAULT_MIN_CHARS)


def assess_document(doc: CorpusDocument, *, max_boilerplate: float = 0.6) -> CleanVerdict:
    """Apply the boilerplate filter with this document's source-appropriate length floor."""
    return assess(
        doc.text,
        min_chars=min_chars_for(doc.source),
        max_boilerplate=max_boilerplate,
    )


def passes_language_filter(
    text: str,
    *,
    min_confidence: float = 0.6,
    max_foreign_share: float = 0.25,
) -> tuple[bool, str]:
    """Whether ``text`` may stay, plus the verdict rendered for the report.

    Kept when Catalan wins clearly, and when there is **no signal at all** — a short legal
    article may contain no function word the profiles know, and absence of evidence is not
    evidence of a foreign language. Dropped when another language wins, and when Catalan wins
    but carries too much foreign signal to be anything but a bilingual page.
    """
    verdict = detect_language(text)
    rendered = (
        f"{verdict.language} (conf {verdict.confidence:.2f}, "
        f"{verdict.runner_up} {verdict.runner_up_share:.2f})"
    )
    if verdict.language == "und":
        return True, rendered
    keep = (
        verdict.language == "ca"
        and verdict.confidence >= min_confidence
        and verdict.runner_up_share <= max_foreign_share
    )
    return keep, rendered


def survivor_rank(doc: CorpusDocument) -> tuple[bool, int, str]:
    """Sort key deciding which near-duplicate survives; the greatest wins.

    **Licence first**: a publishable document always beats a ``no-redistribute`` one, because
    keeping the restricted copy would carry it into the public dataset. Then the longer text
    (the more complete rendering of the same content), then the id, purely so the outcome is
    deterministic.
    """
    return (doc.license.is_public(), len(doc.text), doc.id)


def read_documents(paths: Iterable[Path], report: ConsolidationReport) -> list[CorpusDocument]:
    """Read and §3.1-validate every line of every input file."""
    documents: list[CorpusDocument] = []
    for path in paths:
        with path.open(encoding="utf-8") as handle:
            for line_no, raw in enumerate(handle, start=1):
                if not raw.strip():
                    continue
                report.read += 1
                doc, error = validate_line(raw, line_no)
                if error is not None:
                    report.invalid.append(LineError(error.line, f"{path.name}: {error.reason}"))
                    continue
                assert doc is not None
                documents.append(doc)
    return documents


def consolidate(
    documents: Iterable[CorpusDocument],
    *,
    config: MinHashConfig = DEFAULT_CONFIG,
    near_dup_threshold: float = 0.85,
    max_boilerplate: float = 0.6,
    report: ConsolidationReport | None = None,
) -> ConsolidationResult:
    """Run stages 2-6 over already-validated documents."""
    report = report if report is not None else ConsolidationReport()
    surviving: dict[str, CorpusDocument] = {}

    for doc in documents:
        normalized = renormalize(doc)
        if normalized is None:
            report.dropped.append(
                Dropped("normalize", "empty after normalization", doc.source.value, str(doc.url))
            )
            continue

        verdict = assess_document(normalized, max_boilerplate=max_boilerplate)
        if not verdict.keep:
            report.dropped.append(
                Dropped("boilerplate", verdict.reason, normalized.source.value, str(normalized.url))
            )
            continue

        keep_language, rendered = passes_language_filter(normalized.text)
        if not keep_language:
            report.dropped.append(
                Dropped("language", rendered, normalized.source.value, str(normalized.url))
            )
            continue

        existing = surviving.get(normalized.id)
        if existing is not None:
            # Same text under two URLs. Which copy survives is decided by survivor_rank, not
            # by arrival order: two identical texts can carry *different licences*, and
            # first-wins would let a no-redistribute copy outlive a publishable one.
            winner, loser = (
                (normalized, existing)
                if survivor_rank(normalized) > survivor_rank(existing)
                else (existing, normalized)
            )
            surviving[normalized.id] = winner
            report.dropped.append(
                Dropped(
                    "exact-duplicate",
                    f"same text as {winner.url}",
                    loser.source.value,
                    str(loser.url),
                )
            )
            continue
        surviving[normalized.id] = normalized

    index = NearDuplicateIndex(config=config, threshold=near_dup_threshold)
    for doc_id, doc in surviving.items():
        index.add(doc_id, doc.text)
    clusters = index.clusters()
    _, dropped_ids = choose_survivors(clusters, lambda key: survivor_rank(surviving[key]))

    for doc_id in dropped_ids:
        doc = surviving.pop(doc_id)
        report.dropped.append(
            Dropped(
                "near-duplicate",
                "near-duplicate of a kept document",
                doc.source.value,
                str(doc.url),
            )
        )

    documents_out = tuple(surviving.values())
    report.kept = len(documents_out)
    for doc in documents_out:
        report.by_source[doc.source.value] += 1
        report.by_license[doc.license.value] += 1
    return ConsolidationResult(documents_out, report)


def write_partitioned(documents: Iterable[CorpusDocument], out_dir: Path) -> dict[str, Path]:
    """Write one JSONL per source under ``out_dir``; returns ``{source: path}``.

    One file per source is what the HF upload (M1.09) partitions on, and it keeps a
    ``no-redistribute`` source physically separate from publishable ones — a mistake at
    publication time then has to include a whole file, not slip through a filter.
    """
    grouped: dict[str, list[CorpusDocument]] = {}
    for doc in documents:
        grouped.setdefault(doc.source.value, []).append(doc)

    out_dir.mkdir(parents=True, exist_ok=True)
    written: dict[str, Path] = {}
    for source, docs in sorted(grouped.items()):
        path = out_dir / f"{source}.jsonl"
        with path.open("w", encoding="utf-8") as handle:
            for doc in docs:
                handle.write(f"{doc.model_dump_json()}\n")
        written[source] = path
    return written


def render(report: ConsolidationReport) -> str:
    """Human-readable summary — the shape the M1.10 coverage report builds on."""
    lines = [
        f"read: {report.read}  kept: {report.kept}  "
        f"dropped: {len(report.dropped)}  invalid: {len(report.invalid)}",
    ]
    if report.by_stage:
        lines.append(
            "  dropped by stage: "
            + ", ".join(f"{stage}={count}" for stage, count in sorted(report.by_stage.items()))
        )
    if report.by_source:
        lines.append(
            "  kept by source: "
            + ", ".join(f"{src}={count}" for src, count in sorted(report.by_source.items()))
        )
    if report.no_redistribute:
        lines.append(
            f"  ⚠ no-redistribute (grounding-only, never public): {report.no_redistribute}"
        )
    for error in report.invalid[:20]:
        lines.append(f"  ✗ invalid line {error.line}: {error.reason}")
    if len(report.invalid) > 20:
        lines.append(f"  … and {len(report.invalid) - 20} more invalid lines")
    return "\n".join(lines)


def dump_report(report: ConsolidationReport) -> str:
    """The report as JSON, for the coverage report (M1.10) to consume."""
    return json.dumps(
        {
            "read": report.read,
            "kept": report.kept,
            "invalid": len(report.invalid),
            "dropped_by_stage": dict(sorted(report.by_stage.items())),
            "kept_by_source": dict(sorted(report.by_source.items())),
            "kept_by_license": dict(sorted(report.by_license.items())),
            "balanced": report.balanced,
        },
        ensure_ascii=False,
        indent=2,
        sort_keys=False,
    )


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point. Exit 0 when a non-empty corpus was written, 1 otherwise."""
    parser = argparse.ArgumentParser(
        description="Consolidate per-source JSONL corpora: normalize, filter, dedup, partition."
    )
    parser.add_argument("inputs", type=Path, nargs="+", help="per-source JSONL corpus files")
    parser.add_argument("--out", type=Path, required=True, help="output directory")
    parser.add_argument(
        "--near-dup-threshold",
        type=float,
        default=0.85,
        help="Jaccard similarity at which two documents are near-duplicates (default 0.85)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="exit 1 if any input line failed §3.1 validation",
    )
    args = parser.parse_args(argv)

    missing = [path for path in args.inputs if not path.is_file()]
    if missing:
        for path in missing:
            print(f"error: no such file: {path}", file=sys.stderr)
        return 1

    report = ConsolidationReport()
    documents = read_documents(args.inputs, report)
    result = consolidate(documents, near_dup_threshold=args.near_dup_threshold, report=report)
    written = write_partitioned(result.documents, args.out)

    print(render(result.report))
    for source, path in sorted(written.items()):
        print(f"  → {source}: {path}")

    if not result.documents:
        print("error: consolidation produced no documents", file=sys.stderr)
        return 1
    if args.strict and result.report.invalid:
        print(
            f"error: {len(result.report.invalid)} invalid input lines (--strict)", file=sys.stderr
        )
        return 1
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
