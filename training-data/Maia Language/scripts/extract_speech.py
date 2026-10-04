"""Inventaria les peces de parla i selecciona les fonts lingüístiques elegibles."""

from __future__ import annotations

from pathlib import Path

from training_data.inventory import scan_tree
from training_data.language import (
    extract_language,
    write_authentic_speech_segments,
    write_language_selection,
)
from training_data.language_conversations import (
    build_human_conversations,
    write_human_conversations,
)
from training_data.language_uncertainty import (
    filter_uncertain_conversations,
    write_language_uncertainty_result,
)


def main() -> int:
    """Escriu el ledger local de parla sense alterar ni reescriure'n el text."""

    language_root = Path(__file__).resolve().parents[1]
    repository_root = language_root.parents[1]
    ledger = extract_language(scan_tree(repository_root / "docs"))
    report = write_language_selection(
        ledger,
        work=language_root / "work",
        reports=language_root / "reports",
    )
    authenticity = write_authentic_speech_segments(
        ledger,
        work=language_root / "work",
        reports=language_root / "reports",
    )
    conversations = write_human_conversations(ledger, work=language_root / "work")
    filtered = filter_uncertain_conversations(ledger, build_human_conversations(ledger))
    uncertainty_report = write_language_uncertainty_result(
        ledger,
        filtered,
        work=language_root / "work",
        reports=language_root / "reports",
    )
    print(
        f"Language selection: {report.eligible_pieces} eligible, "
        f"{report.excluded_pieces} excluded, {report.unresolved_pieces} unresolved "
        f"from {report.speech_documents} speech pieces; "
        f"{report.uncertainty_spans} uncertainty spans preserved; "
        f"{authenticity.generated_segments} generated segments; "
        f"{conversations.candidates} explicit chat turns; "
        f"{uncertainty_report.excluded_candidates} excluded for uncertainty."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
