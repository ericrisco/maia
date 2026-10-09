"""Build the complete, source-traceable Maia Language eligibility ledger."""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "src"))

from training_data.inventory import scan_tree  # noqa: E402
from training_data.language import (  # noqa: E402
    extract_language,
    write_authentic_speech_segments,
    write_language_selection,
)
from training_data.language_conversations import write_human_conversations  # noqa: E402


def main() -> None:
    inventory = scan_tree(REPO / "docs")
    ledger = extract_language(inventory)
    work = REPO / "training-data/language/work"
    reports = REPO / "training-data/language/reports"

    selection = write_language_selection(ledger, work=work, reports=reports)
    authenticity = write_authentic_speech_segments(ledger, work=work, reports=reports)
    conversations = write_human_conversations(ledger, work=work)

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


if __name__ == "__main__":
    main()
