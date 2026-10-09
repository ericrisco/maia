"""Reconcile series-level rights with verified per-video AR+I licenses."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "src"))

from training_data.inventory import scan_tree  # noqa: E402
from training_data.language import SpeechPiece, extract_language  # noqa: E402

VERIFIED_ARI_VIDEO_IDS = {34, 49, 56, 57, 66}
CAPSULE_NUMBER_BY_PATH = {
    "parla/oral/cal-pal-esther-jover.md": 49,
    "parla/oral/el-contrapas-teo-armengol.md": 66,
    "parla/oral/els-hostals-comunals-lacueva.md": 13,
    "parla/oral/els-molins-daigua.md": 20,
    "parla/oral/els-noms-dels-carrers.md": 27,
    "parla/oral/la-nissaga-dels-marti.md": 70,
    "parla/oral/la-vida-a-pages.md": 56,
    "parla/oral/les-campanes-robert-lizarte.md": 40,
    "parla/oral/les-falles-albert-roig.md": 34,
    "parla/oral/les-moles-de-farina.md": 11,
    "parla/oral/toponimia-preromana-xavier-planas.md": 45,
    "parla/oral/un-raco-descaldes.md": 57,
}


def _piece_rights(piece: SpeechPiece) -> dict[str, object]:
    reference = piece.provenance[0] if piece.provenance else None
    source_id = reference.source_id if reference else None
    record: dict[str, object] = {
        "path": piece.path,
        "piece_id": piece.piece_id,
        "title": piece.title,
        "eligibility": piece.eligibility,
        "eligibility_reason": piece.reason,
        "source_id": source_id,
        "series_redistribution": reference.redistribution if reference else None,
        "piece_redistribution": reference.redistribution if reference else None,
        "piece_license": reference.licence if reference else None,
        "verification_path": reference.source_path if reference else None,
        "rights_basis": "source_card",
        "transcript_review": "pending",
        "exportable": False,
    }
    if source_id != "ari-capsules":
        return record

    number = CAPSULE_NUMBER_BY_PATH.get(piece.path)
    if number is None:
        raise ValueError(f"AR+I capsule number is missing from title: {piece.path}")
    record["capsule_number"] = number
    if number not in VERIFIED_ARI_VIDEO_IDS:
        record["piece_redistribution"] = "pendent"
        record["rights_basis"] = "series_card_only; per-video verification missing"
        return record

    captures = sorted((REPO / "docs/raw/parla" / f"ari-capsula-{number}").glob("youtube-info-*.json"))
    if len(captures) != 1:
        raise ValueError(f"expected one verified YouTube capture for capsule #{number}, found {len(captures)}")
    capture_path = captures[0]
    capture = json.loads(capture_path.read_text(encoding="utf-8"))
    metadata = capture.get("metadata", {})
    license_label = str(metadata.get("license") or "")
    if "Creative Commons Attribution" not in license_label:
        raise ValueError(f"capsule #{number} has no verified CC Attribution license")
    record.update(
        {
            "piece_redistribution": "si",
            "piece_license": license_label,
            "verification_path": capture_path.relative_to(REPO).as_posix(),
            "rights_basis": "individual_youtube_video_metadata",
        }
    )
    return record


def main() -> None:
    ledger = extract_language(scan_tree(REPO / "docs"))
    pieces = [piece for piece in ledger.pieces if piece.document_type == "parla"]
    records = [_piece_rights(piece) for piece in pieces]
    rights_counts = Counter(
        (str(record["source_id"]), str(record["piece_redistribution"]))
        for record in records
    )
    eligible_counts = Counter(
        (str(record["source_id"]), str(record["piece_redistribution"]))
        for record in records
        if record["eligibility"] == "eligible"
    )

    work = REPO / "training-data/language/work"
    reports = REPO / "training-data/language/reports"
    work.mkdir(parents=True, exist_ok=True)
    reports.mkdir(parents=True, exist_ok=True)
    (work / "piece-rights.jsonl").write_text(
        "".join(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )
    summary = {
        "speech_pieces": len(pieces),
        "rights_by_source_and_piece_status": {
            f"{source_id}:{status}": count
            for (source_id, status), count in sorted(rights_counts.items())
        },
        "eligible_pieces_by_source_and_piece_status": {
            f"{source_id}:{status}": count
            for (source_id, status), count in sorted(eligible_counts.items())
        },
        "verified_ari_video_ids": sorted(VERIFIED_ARI_VIDEO_IDS),
        "transcript_review": "pending for all pieces",
        "exportable_pieces": 0,
    }
    (reports / "piece-rights.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
