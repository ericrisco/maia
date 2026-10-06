"""Genera candidats locals de converses fonamentades en unitats de coneixement."""

from __future__ import annotations

from pathlib import Path

from training_data.inventory import scan_tree
from training_data.knowledge import extract_knowledge
from training_data.knowledge_coverage import build_knowledge_coverage, write_knowledge_coverage
from training_data.knowledge_deduplicate import (
    deduplicate_knowledge_candidates,
    write_knowledge_deduplication,
)
from training_data.knowledge_generate import (
    build_knowledge_candidates,
    build_relation_candidates,
    classify_knowledge_candidates,
    write_knowledge_candidates,
)
from training_data.knowledge_split import split_knowledge_candidates, write_knowledge_splits


def main() -> int:
    """Construeix candidats de treball sense crides de xarxa ni canvis a docs/."""

    knowledge_root = Path(__file__).resolve().parents[1]
    repository_root = knowledge_root.parents[1]
    ledger = extract_knowledge(scan_tree(repository_root / "docs"))
    candidates = (
        *build_knowledge_candidates(ledger),
        *build_relation_candidates(ledger),
    )
    classification = classify_knowledge_candidates(candidates, ledger)
    deduplicated = deduplicate_knowledge_candidates(classification.eligible_candidates)
    write_knowledge_candidates(
        candidates,
        work=knowledge_root / "work",
        classification=classification,
        public_candidates=deduplicated.candidates,
        deduplicated_candidates=deduplicated.candidates,
    )
    coverage = build_knowledge_coverage(ledger, classification)
    write_knowledge_coverage(coverage, reports=knowledge_root / "reports")
    write_knowledge_deduplication(deduplicated.report, reports=knowledge_root / "reports")
    split = split_knowledge_candidates(deduplicated.candidates)
    if sum(split.manifest.actual_counts.values()):
        write_knowledge_splits(
            split,
            output=knowledge_root / "output",
            work=knowledge_root / "work",
        )
    else:
        print("Knowledge splits not written: no human-reviewed, redistribution-cleared records.")
    print(
        f"Knowledge candidates: {classification.included_count} included, "
        f"{classification.excluded_count} excluded, "
        f"{classification.unresolved_count} unresolved from {len(candidates)} candidates."
    )
    print(
        f"Knowledge deduplication: {deduplicated.report.exact_records_removed} exact duplicates "
        f"removed; {deduplicated.report.near_duplicate_family_count} related families reported."
    )
    print(
        f"Evidence coverage: {coverage.represented_units}/{coverage.total_evidence_units} "
        f"total classified ({coverage.total_coverage:.1%}); "
        f"{coverage.trainable_represented_units}/{coverage.trainable_units} "
        f"trainable represented ({coverage.trainable_coverage:.1%})."
    )
    print(
        "Knowledge splits: "
        + ", ".join(f"{name}={count}" for name, count in split.manifest.actual_counts.items())
        + f" (seed {split.manifest.seed})."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
