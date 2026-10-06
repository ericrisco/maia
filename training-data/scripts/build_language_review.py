#!/usr/bin/env python3
"""Audit eligible human speech and explicit, uncertainty-free dialogue turns."""

from __future__ import annotations

import json
import sys
from collections import Counter
from dataclasses import asdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))

from training_data.inventory import scan_tree  # noqa: E402
from training_data.language import (  # noqa: E402
    build_authentic_speech_segments,
    extract_language,
    validate_authentic_speech_segments,
    write_authentic_speech_segments,
    write_language_selection,
)
from training_data.language_conversations import (  # noqa: E402
    build_human_conversations,
    validate_human_conversations,
)
from training_data.language_uncertainty import (  # noqa: E402
    filter_uncertain_conversations,
    validate_uncertainty_filter,
    write_language_uncertainty_result,
)


def _atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def main() -> int:
    inventory = scan_tree(REPO / "docs")
    ledger = extract_language(inventory)
    candidates = build_human_conversations(ledger)
    validate_human_conversations(ledger, candidates)
    uncertainty = filter_uncertain_conversations(ledger, candidates)
    validate_uncertainty_filter(ledger, uncertainty)

    work = REPO / "training-data/language/work"
    reports = REPO / "training-data/language/reports"
    selection_report = write_language_selection(ledger, work=work, reports=reports)
    authentic_segments = build_authentic_speech_segments(ledger)
    validate_authentic_speech_segments(ledger, authentic_segments)
    authenticity_report = write_authentic_speech_segments(ledger, work=work, reports=reports)
    uncertainty_report = write_language_uncertainty_result(
        ledger, uncertainty, work=work, reports=reports
    )
    _atomic_json(
        reports / "conversations.json",
        {
            "eligible_pieces": selection_report.eligible_pieces,
            "pieces_with_explicit_dialogue": len({candidate.piece_id for candidate in candidates}),
            "candidate_conversations": len(candidates),
            "verbatim_assistant_turns": len(candidates),
            "generated_dialogue": 0,
        },
    )
    rights_counts: Counter[str] = Counter()
    for piece in ledger.pieces:
        for reference in piece.provenance:
            rights_counts[reference.redistribution or "unknown"] += 1
    _atomic_json(
        reports / "summary.json",
        {
            "selection": asdict(selection_report),
            "conversations": {
                "explicit_candidates": len(candidates),
                "accepted_after_uncertainty_filter": len(uncertainty.accepted),
                "excluded_for_uncertainty": len(uncertainty.excluded),
                "generated_messages": 0,
            },
            "authenticity": asdict(authenticity_report),
            "uncertainty": asdict(uncertainty_report),
            "source_redistribution_states": dict(sorted(rights_counts.items())),
            "output_records": 0,
            "output_reason": (
                "No uncertainty-free, explicit human dialogue pairs are currently available."
                if not uncertainty.accepted
                else "Candidate dialogue still requires source-rights and human review."
            ),
        },
    )
    print(
        f"Language audit: {selection_report.eligible_pieces} eligible pieces, "
        f"{len(candidates)} explicit conversations, {len(uncertainty.accepted)} accepted."
    )
    return 1 if selection_report.markdown_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
