"""Genera candidats locals de converses fonamentades en unitats de coneixement."""

from __future__ import annotations

from pathlib import Path

from training_data.inventory import scan_tree
from training_data.knowledge import extract_knowledge
from training_data.knowledge_generate import (
    build_knowledge_candidates,
    build_relation_candidates,
    write_knowledge_candidates,
)


def main() -> int:
    """Construeix candidats de treball sense crides de xarxa ni canvis a docs/."""

    knowledge_root = Path(__file__).resolve().parents[1]
    repository_root = knowledge_root.parents[1]
    ledger = extract_knowledge(scan_tree(repository_root / "docs"))
    candidates = (
        *build_knowledge_candidates(ledger),
        *build_relation_candidates(ledger),
    )
    write_knowledge_candidates(candidates, work=knowledge_root / "work")
    print(
        f"Knowledge candidates: {len(candidates)} candidates from "
        f"{ledger.report.units_detected} evidence units."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
