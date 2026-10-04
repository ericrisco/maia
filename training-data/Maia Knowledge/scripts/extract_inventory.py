"""Genera el ledger local de coneixement i el primer informe d'inventari."""

from __future__ import annotations

from pathlib import Path

from training_data.inventory import scan_tree
from training_data.knowledge import extract_knowledge, write_knowledge_extraction


def main() -> int:
    """Llegeix el corpus temàtic sense modificar-ne les fonts."""

    knowledge_root = Path(__file__).resolve().parents[1]
    repository_root = knowledge_root.parents[1]
    ledger = extract_knowledge(scan_tree(repository_root / "docs"))
    report = write_knowledge_extraction(
        ledger,
        work=knowledge_root / "work",
        reports=knowledge_root / "reports",
    )
    print(
        "Knowledge inventory: "
        f"{report.processed_documents} documents, "
        f"{report.units_detected} evidence units, "
        f"{report.markdown_errors} Markdown errors, "
        f"{report.internal_links_detected} internal links."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
