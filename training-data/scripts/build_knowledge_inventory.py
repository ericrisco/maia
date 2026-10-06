#!/usr/bin/env python3
"""Parse all Maia docs and build the auditable Knowledge evidence ledger."""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))

from training_data.inventory import scan_tree  # noqa: E402
from training_data.knowledge import extract_knowledge, write_knowledge_extraction  # noqa: E402


def main() -> int:
    inventory = scan_tree(REPO / "docs")
    ledger = extract_knowledge(inventory)
    report = write_knowledge_extraction(
        ledger,
        work=REPO / "training-data/knowledge/work",
        reports=REPO / "training-data/knowledge/reports",
    )
    print(
        "Knowledge inventory: "
        f"{report.processed_documents} documents, "
        f"{report.sections_processed} sections, "
        f"{report.tables_processed} tables, "
        f"{report.table_rows_processed} table rows, "
        f"{report.units_detected} evidence units, "
        f"{report.links_detected} links, "
        f"{report.markdown_errors} Markdown errors."
    )
    return 1 if report.markdown_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
