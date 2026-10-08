"""Revisable text-only Language samples from literal, eligible speech spans."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Iterable
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from training_data.knowledge_split import SPLIT_NAMES, SplitConfig
from training_data.language import (
    AuthenticSpeechSegment,
    LanguageLedger,
    UNCERTAIN_SPAN,
    build_authentic_speech_segments,
    extract_language,
    validate_authentic_speech_segments,
    write_authentic_speech_segments,
    write_language_selection,
)
from training_data.inventory import scan_tree

MIN_TRAINING_SAMPLE_CHARS = 80


@dataclass(frozen=True, slots=True)
class LanguageTextSplit:
    """Text records grouped by source piece to prevent split leakage."""

    train: tuple[LanguageTextSample, ...]
    validation: tuple[LanguageTextSample, ...]
    test: tuple[LanguageTextSample, ...]
    assignments: dict[str, str]
    counts: dict[str, int]
    excluded_short_count: int
    minimum_sample_chars: int


@dataclass(frozen=True, slots=True)
class LanguageTextSample:
    """Readable text assembled from adjacent, literal transcript spans."""

    sample_id: str
    source_path: str
    piece_id: str
    text: str
    source_spans: tuple[AuthenticSpeechSegment, ...]


def _provenance_record(
    sample: LanguageTextSample, ledger: LanguageLedger
) -> dict[str, object]:
    piece = next(piece for piece in ledger.pieces if piece.path == sample.source_path)
    return {
        "sample_id": sample.sample_id,
        "source_path": sample.source_path,
        "piece_id": sample.piece_id,
        "assembly": "literal transcript spans joined with single spaces",
        "source_spans": [
            {
                "segment_id": span.segment_id,
                "source_start": span.source_start,
                "source_end": span.source_end,
                "text_sha256": hashlib.sha256(span.text.encode("utf-8")).hexdigest(),
            }
            for span in sample.source_spans
        ],
        "source_records": [
            {
                "source_id": reference.source_id,
                "source_path": reference.source_path,
                "licence": reference.licence,
                "provenance_status": reference.status,
                "redistribution": reference.redistribution,
            }
            for reference in piece.provenance
        ],
        "transcript_review_status": "audio_verification_pending",
        "training_status": (
            "excluded_too_short"
            if len(sample.text) < MIN_TRAINING_SAMPLE_CHARS
            else "candidate_pending_audio_review"
        ),
        "text_sha256": hashlib.sha256(sample.text.encode("utf-8")).hexdigest(),
    }


def build_language_text_samples(
    ledger: LanguageLedger, *, min_chars: int = 180, max_chars: int = 600
) -> tuple[LanguageTextSample, ...]:
    """Join adjacent certain transcript lines into readable text samples."""

    if min_chars < 1 or max_chars < min_chars:
        raise ValueError("Language sample length limits are invalid")
    spans = build_authentic_speech_segments(ledger)
    pieces = {piece.path: piece for piece in ledger.pieces}
    samples: list[LanguageTextSample] = []
    pending: list[AuthenticSpeechSegment] = []
    sample_numbers: dict[str, int] = defaultdict(int)

    def flush() -> None:
        if not pending:
            return
        piece_id = pending[0].piece_id
        sample_numbers[piece_id] += 1
        samples.append(
            LanguageTextSample(
                sample_id=f"{piece_id}#sample-{sample_numbers[piece_id]:05d}",
                source_path=pending[0].source_path,
                piece_id=piece_id,
                text=" ".join(span.text for span in pending),
                source_spans=tuple(pending),
            )
        )
        pending.clear()

    for span in spans:
        piece = pieces[span.source_path]
        if pending:
            previous = pending[-1]
            gap = piece.text[previous.source_end : span.source_start]
            proposed = " ".join([*(item.text for item in pending), span.text])
            source_break = (
                previous.source_path != span.source_path
                or bool(UNCERTAIN_SPAN.search(gap))
                or "\n\n" in gap
            )
            if source_break or len(proposed) > max_chars:
                flush()

        pending.append(span)
        current_text = " ".join(item.text for item in pending)
        if len(current_text) >= min_chars and pending[-1].text.rstrip().endswith(
            (".", "?", "!", "…")
        ):
            flush()
    flush()
    validate_language_text_samples(ledger, spans, tuple(samples))
    return tuple(samples)


def validate_language_text_samples(
    ledger: LanguageLedger,
    spans: tuple[AuthenticSpeechSegment, ...],
    samples: tuple[LanguageTextSample, ...],
) -> None:
    """Ensure every sample is assembled from each certain source span once."""

    validate_authentic_speech_segments(ledger, spans)
    span_by_id = {span.segment_id: span for span in spans}
    seen: set[str] = set()
    for sample in samples:
        if not sample.text or not sample.source_spans:
            raise ValueError(f"empty Language sample: {sample.sample_id}")
        if sample.text != " ".join(span.text for span in sample.source_spans):
            raise ValueError(f"Language sample changes source wording: {sample.sample_id}")
        for span in sample.source_spans:
            if span.segment_id not in span_by_id or span_by_id[span.segment_id] != span:
                raise ValueError(f"unknown Language source span: {span.segment_id}")
            if span.segment_id in seen:
                raise ValueError(f"Language source span is duplicated: {span.segment_id}")
            seen.add(span.segment_id)
    if seen != set(span_by_id):
        raise ValueError("Language samples omit one or more certain source spans")


def split_language_text(
    samples: tuple[LanguageTextSample, ...],
    *,
    config: SplitConfig | None = None,
    min_sample_chars: int = MIN_TRAINING_SAMPLE_CHARS,
) -> LanguageTextSplit:
    """Split useful-length samples by source piece and count short exclusions."""

    if min_sample_chars < 1:
        raise ValueError("minimum Language sample length must be positive")
    selected = config or SplitConfig()
    groups: dict[str, list[LanguageTextSample]] = defaultdict(list)
    seen: set[str] = set()
    for sample in samples:
        if not sample.piece_id or not sample.sample_id:
            raise ValueError("every Language sample needs a piece and sample ID")
        if sample.sample_id in seen:
            raise ValueError(f"duplicate Language sample: {sample.sample_id}")
        seen.add(sample.sample_id)
        if len(sample.text) < min_sample_chars:
            continue
        groups[sample.piece_id].append(sample)

    if not groups:
        raise ValueError("no Language samples meet the minimum length")
    total = sum(len(group) for group in groups.values())
    targets = {name: total * selected.target_ratios[name] for name in SPLIT_NAMES}
    ordered_groups = sorted(
        groups,
        key=lambda piece_id: (
            -len(groups[piece_id]),
            hashlib.sha256(f"{selected.seed}\0{piece_id}".encode()).digest(),
        ),
    )
    records: dict[str, list[LanguageTextSample]] = {name: [] for name in SPLIT_NAMES}
    assignments: dict[str, str] = {}
    for piece_id in ordered_groups:
        available = [name for name in SPLIT_NAMES if selected.target_ratios[name] > 0]
        split_name = max(
            available,
            key=lambda name: (
                (targets[name] - len(records[name])) / targets[name],
                -SPLIT_NAMES.index(name),
            ),
        )
        assignments[piece_id] = split_name
        records[split_name].extend(groups[piece_id])

    return LanguageTextSplit(
        train=tuple(records["train"]),
        validation=tuple(records["validation"]),
        test=tuple(records["test"]),
        assignments=assignments,
        counts={name: len(records[name]) for name in SPLIT_NAMES},
        excluded_short_count=len(samples) - total,
        minimum_sample_chars=min_sample_chars,
    )


def validate_language_text_split(
    ledger: LanguageLedger,
    samples: tuple[LanguageTextSample, ...],
    split: LanguageTextSplit,
) -> None:
    """Verify text fidelity, full inclusion, and source-level split isolation."""

    spans = tuple(span for sample in samples for span in sample.source_spans)
    validate_language_text_samples(ledger, spans, samples)
    split_records = {
        "train": split.train,
        "validation": split.validation,
        "test": split.test,
    }
    by_id = {sample.sample_id: sample for sample in samples}
    seen_ids: set[str] = set()
    source_splits: dict[str, set[str]] = defaultdict(set)
    for split_name, records in split_records.items():
        for sample in records:
            if sample.sample_id not in by_id or by_id[sample.sample_id] != sample:
                raise ValueError(f"unknown or changed Language sample: {sample.sample_id}")
            if sample.sample_id in seen_ids:
                raise ValueError(
                    f"Language sample occurs in multiple splits: {sample.sample_id}"
                )
            seen_ids.add(sample.sample_id)
            source_splits[sample.piece_id].add(split_name)
    expected_ids = {
        sample_id
        for sample_id, sample in by_id.items()
        if len(sample.text) >= split.minimum_sample_chars
    }
    if seen_ids != expected_ids:
        raise ValueError("Language splits omit a trainable sample or include a short one")
    if any(len(names) != 1 for names in source_splits.values()):
        raise ValueError("a Language source piece appears in multiple splits")
    observed_assignments = {
        piece_id: next(iter(names)) for piece_id, names in source_splits.items()
    }
    if split.assignments != observed_assignments:
        raise ValueError("Language split manifest does not match its records")


def write_language_review_segments(ledger: LanguageLedger, *, review: Path) -> int:
    """Write assembled text samples and aligned provenance rows for review."""

    samples = build_language_text_samples(ledger)
    review.mkdir(parents=True, exist_ok=True)
    _atomic_jsonl(review / "segments.jsonl", ({"text": item.text} for item in samples))
    _atomic_jsonl(
        review / "provenance.jsonl",
        (_provenance_record(item, ledger) for item in samples),
    )
    return len(samples)


def validate_language_review_segments(ledger: LanguageLedger, *, review: Path) -> int:
    """Verify public text and provenance against every eligible source span."""

    samples = build_language_text_samples(ledger)
    records = _read_jsonl(review / "segments.jsonl")
    traces = _read_jsonl(review / "provenance.jsonl")
    if len(records) != len(samples) or len(traces) != len(samples):
        raise ValueError("Language text and provenance row counts do not match source spans")
    for index, (segment, record, trace) in enumerate(
        zip(samples, records, traces, strict=True), 1
    ):
        if record != {"text": segment.text}:
            raise ValueError(f"Language text differs from its source at row {index}")
        if trace != _provenance_record(segment, ledger):
            raise ValueError(f"Language provenance differs from its source at row {index}")
    return len(samples)


def write_language_text_splits(
    ledger: LanguageLedger,
    *,
    output: Path,
    work: Path,
    config: SplitConfig | None = None,
) -> LanguageTextSplit:
    """Create reproducible text-only train/validation/test files locally."""

    samples = build_language_text_samples(ledger)
    split = split_language_text(samples, config=config)
    validate_language_text_split(ledger, samples, split)
    output.mkdir(parents=True, exist_ok=True)
    for name in SPLIT_NAMES:
        records = ({"text": item.text} for item in getattr(split, name))
        _atomic_jsonl(output / f"{name}.jsonl", records)
    work.mkdir(parents=True, exist_ok=True)
    _atomic_write(
        work / "text-split-manifest.json",
        json.dumps(
            {
                "seed": (config or SplitConfig()).seed,
                "target_ratios": (config or SplitConfig()).target_ratios,
                "piece_assignments": split.assignments,
                "counts": split.counts,
                "excluded_short_count": split.excluded_short_count,
                "minimum_sample_chars": split.minimum_sample_chars,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
    )
    return split


def _atomic_jsonl(path: Path, records: Iterable[object]) -> None:
    _atomic_write(
        path,
        "".join(
            json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n"
            for record in records
        ),
    )


def _read_jsonl(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{line_number}: expected a JSON object")
        rows.append(value)
    return rows


def _atomic_write(path: Path, content: str) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content, encoding="utf-8", newline="")
    temporary.replace(path)


def main() -> None:
    """Rebuild local Language review files, reports, and provisional text splits."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--docs", type=Path, default=Path("docs"))
    parser.add_argument("--review", type=Path, default=Path("training-data/language/review"))
    parser.add_argument("--output", type=Path, default=Path("training-data/language/output"))
    parser.add_argument("--work", type=Path, default=Path("training-data/language/work"))
    parser.add_argument("--reports", type=Path, default=Path("training-data/language/reports"))
    args = parser.parse_args()

    ledger = extract_language(scan_tree(args.docs))
    write_language_selection(ledger, work=args.work, reports=args.reports)
    authenticity = write_authentic_speech_segments(ledger, work=args.work, reports=args.reports)
    review_count = write_language_review_segments(ledger, review=args.review)
    validate_language_review_segments(ledger, review=args.review)
    split = write_language_text_splits(
        ledger, output=args.output, work=args.work
    )
    print(
        json.dumps(
            {
                "eligible_pieces": ledger.report.eligible_pieces,
                "unresolved_pieces": ledger.report.unresolved_pieces,
                "review_segments": review_count,
                "training_samples": sum(split.counts.values()),
                "short_samples_excluded": split.excluded_short_count,
                "uncertain_transcript_lines_excluded": (
                    authenticity.uncertain_transcript_lines_excluded
                ),
                "split_counts": split.counts,
                "piece_assignments": len(split.assignments),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
