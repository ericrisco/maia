#!/usr/bin/env python3
"""Reconcile all Knowledge evidence with reviewed conversations and exclusions."""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))

from training_data.inventory import scan_tree  # noqa: E402
from training_data.knowledge import extract_knowledge  # noqa: E402
from training_data.knowledge_coverage import (  # noqa: E402
    build_knowledge_coverage,
    write_knowledge_coverage,
)
from training_data.knowledge_generate import (  # noqa: E402
    classify_knowledge_candidates,
    load_review_conversations,
    write_knowledge_candidates,
)


def _atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def main() -> int:
    inventory = scan_tree(REPO / "docs")
    ledger = extract_knowledge(inventory)
    review = REPO / "training-data/knowledge/review"
    candidates = load_review_conversations(
        review / "conversations.jsonl", review / "provenance.jsonl", ledger
    )
    classification = classify_knowledge_candidates(candidates, ledger)
    coverage = build_knowledge_coverage(ledger, classification)
    reports = REPO / "training-data/knowledge/reports"
    work = REPO / "training-data/knowledge/work"

    write_knowledge_candidates(candidates, work=work, classification=classification)
    write_knowledge_coverage(coverage, reports=reports)

    documents = {document.path: document for document in coverage.documents}
    topic_counts: dict[str, dict[str, int]] = defaultdict(
        lambda: {
            "documents": 0,
            "evidence_units": 0,
            "represented": 0,
            "excluded": 0,
            "unresolved": 0,
        }
    )
    for path, counts in documents.items():
        topic_parts = PurePosixPath(path).parts[:2]
        topic = "/".join(topic_parts)
        target = topic_counts[topic]
        target["documents"] += 1
        target["evidence_units"] += counts.detected_units
        target["represented"] += counts.represented_units
        target["excluded"] += counts.excluded_units
        target["unresolved"] += counts.unresolved_units

    draft_evidence = {
        evidence_id for candidate in candidates for evidence_id in candidate.evidence_ids
    }
    rights_counts: Counter[str] = Counter()
    for trace in (review / "provenance.jsonl").read_text(encoding="utf-8").splitlines():
        row = json.loads(trace)
        for state in row.get("source_redistribution", {}).values():
            rights_counts[str(state)] += 1

    summary = {
        "scope": "all Markdown documents and structural evidence under docs/temes/",
        "processed_documents": coverage.processed_documents,
        "markdown_errors": coverage.markdown_errors,
        "evidence_units": coverage.total_evidence_units,
        "evidence_referenced_by_review_drafts": len(draft_evidence),
        "evidence_represented_by_approved_records": coverage.represented_units,
        "evidence_explicitly_excluded": coverage.excluded_units,
        "evidence_unresolved": coverage.unresolved_units,
        "records_in_review": len(candidates),
        "records_requiring_human_review": sum(
            candidate.review_status != "human_reviewed" for candidate in candidates
        ),
        "export_ready_records": len(classification.eligible_candidates),
        "decision_reasons": dict(
            sorted(Counter(item.reason for item in classification.decisions).items())
        ),
        "source_redistribution_states_in_review": dict(sorted(rights_counts.items())),
        "topic_coverage": dict(sorted(topic_counts.items())),
    }
    _atomic_json(reports / "coverage-summary.json", summary)
    print(
        f"Knowledge coverage: {summary['evidence_referenced_by_review_drafts']} / "
        f"{summary['evidence_units']} units referenced; "
        f"{summary['export_ready_records']} export-ready records."
    )
    return 1 if coverage.markdown_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
