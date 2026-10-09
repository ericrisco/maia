"""Build the complete, source-traceable Maia Language eligibility ledger."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "src"))

from training_data.inventory import scan_tree  # noqa: E402
from training_data.language import (  # noqa: E402
    extract_language,
    write_authentic_speech_segments,
    write_language_selection,
)
from training_data.language_conversations import (  # noqa: E402
    SpeechConversationCandidate,
    build_human_conversations,
    write_human_conversations,
)

CAPSULE_NUMBER = re.compile(r"Càpsula\s+#(?P<number>\d+)", re.IGNORECASE)


def write_piece_rights(
    ledger,
    dialogue_candidates: tuple[SpeechConversationCandidate, ...],
    *,
    repo: Path,
    work: Path,
    reports: Path,
) -> dict[str, object]:
    """Resolve AR+I licence captures per video; keep all other rights pending."""

    rows: list[dict[str, object]] = []
    counts: Counter[str] = Counter()
    dialogue_counts = Counter(candidate.source_path for candidate in dialogue_candidates)
    candidates = 0
    for piece in ledger.pieces:
        if piece.document_type != "parla":
            continue
        source = piece.provenance[0] if piece.provenance else None
        row: dict[str, object] = {
            "piece_path": f"docs/{piece.path}",
            "eligibility": piece.eligibility,
            "eligibility_reason": piece.reason,
            "source_id": source.source_id if source else None,
            "source_card_status": source.redistribution if source else None,
            "piece_licence_status": "pendent",
            "piece_licence": None,
            "licence_evidence": [],
            "uncertainty_spans": len(piece.uncertainty_spans),
            "explicit_dialogue_pairs": dialogue_counts[piece.path],
            "exportable": False,
        }
        if source is not None and source.source_id == "ari-capsules":
            match = CAPSULE_NUMBER.search(piece.text)
            if match:
                capsule_dir = repo / "docs/raw/parla" / f"ari-capsula-{match.group('number')}"
                captures = sorted(capsule_dir.glob("youtube-info-*.json"))
                metadata: list[tuple[Path, str]] = []
                for capture in captures:
                    payload = json.loads(capture.read_text(encoding="utf-8"))
                    license_name = str(payload.get("metadata", {}).get("license") or "").strip()
                    if license_name:
                        metadata.append((capture, license_name))
                distinct_licenses = {name for _, name in metadata}
                if metadata and len(distinct_licenses) == 1:
                    license_name = metadata[0][1]
                    if "creative commons attribution" in license_name.casefold():
                        row["piece_licence_status"] = "permesa_amb_atribucio"
                        row["piece_licence"] = license_name
                        row["licence_evidence"] = [
                            path.relative_to(repo).as_posix() for path, _ in metadata
                        ]
        rows.append(row)
        counts[str(row["piece_licence_status"])] += 1
        if (
            row["eligibility"] == "eligible"
            and row["piece_licence_status"] == "permesa_amb_atribucio"
        ):
            candidates += 1

    work.mkdir(parents=True, exist_ok=True)
    (work / "piece-rights.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )
    report = {
        "speech_pieces": len(rows),
        "content_eligible": sum(row["eligibility"] == "eligible" for row in rows),
        "content_excluded": sum(row["eligibility"] == "excluded" for row in rows),
        "piece_licence_counts": dict(sorted(counts.items())),
        "eligible_with_piece_level_licence": candidates,
        "explicit_dialogue_pairs": len(dialogue_candidates),
        "exportable_pieces": 0,
    }
    reports.mkdir(parents=True, exist_ok=True)
    (reports / "piece-rights.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return report


def main() -> None:
    inventory = scan_tree(REPO / "docs")
    ledger = extract_language(inventory)
    work = REPO / "training-data/language/work"
    reports = REPO / "training-data/language/reports"

    selection = write_language_selection(ledger, work=work, reports=reports)
    authenticity = write_authentic_speech_segments(ledger, work=work, reports=reports)
    dialogue_candidates = build_human_conversations(ledger)
    conversations = write_human_conversations(ledger, work=work)
    rights = write_piece_rights(
        ledger,
        dialogue_candidates,
        repo=REPO,
        work=work,
        reports=reports,
    )

    print(f"Speech Markdown entries: {selection.processed_entries}")
    print(f"Speech documents: {selection.speech_documents}")
    print(f"Markdown errors: {selection.markdown_errors}")
    print(
        "Eligibility (eligible / excluded / unresolved): "
        f"{selection.eligible_pieces} / {selection.excluded_pieces} / "
        f"{selection.unresolved_pieces}"
    )
    print(f"Uncertain transcript spans: {selection.uncertainty_spans}")
    print(f"Verbatim timestamped segments: {authenticity.authentic_segments}")
    print(f"Explicit human Q&A pairs: {conversations.candidates}")
    generated = authenticity.generated_segments + authenticity.rewritten_segments
    print(f"Generated or rewritten Language segments: {generated}")
    print(
        "Piece-level licences (permitted / pending): "
        f"{rights['eligible_with_piece_level_licence']} / "
        f"{rights['piece_licence_counts'].get('pendent', 0)}"
    )


if __name__ == "__main__":
    main()
