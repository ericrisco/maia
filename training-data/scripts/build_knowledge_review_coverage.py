"""Build an auditable coverage report for reviewed Maia Knowledge conversations.

The report distinguishes material mentioned in review drafts from examples
that are approved, rights-cleared, and ready for a training export.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
TRAINING_DATA = ROOT / "training-data"
EVIDENCE_PATH = TRAINING_DATA / "knowledge/work/evidence.jsonl"
CONVERSATIONS_PATH = TRAINING_DATA / "knowledge/review/conversations.jsonl"
PROVENANCE_PATH = TRAINING_DATA / "knowledge/review/provenance.jsonl"
EXCLUSIONS_PATH = TRAINING_DATA / "knowledge/work/exclusions.jsonl"
REPORT_PATH = TRAINING_DATA / "knowledge/reports/coverage.json"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    with path.open(encoding="utf-8") as source:
        for line_number, line in enumerate(source, 1):
            if line.strip():
                value = json.loads(line)
                if not isinstance(value, dict):
                    raise ValueError(f"{path}:{line_number}: expected a JSON object")
                rows.append(value)
    return rows


def permission_state(record: dict[str, Any]) -> str:
    values = [record.get("redistribution")]
    values.extend(source.get("redistribution") for source in record.get("supporting_sources", []))
    states: list[str] = []
    for value in values:
        normalized = str(value or "").strip().lower()
        if normalized.startswith(("yes", "si", "sí")):
            states.append("allowed")
        elif normalized.startswith(("no", "not allowed")):
            states.append("prohibited")
        elif "pending" in normalized or "pendent" in normalized:
            states.append("pending")
        else:
            states.append("unknown")
    if all(state == "allowed" for state in states):
        return "allowed"
    if "pending" in states:
        return "pending"
    if "prohibited" in states:
        return "prohibited"
    if "allowed" in states:
        return "mixed"
    return "unknown"


def review_approved(record: dict[str, Any]) -> bool:
    status = str(record.get("status", "")).strip().lower()
    return status in {"approved", "accepted", "human_reviewed", "human reviewed"}


def topic_for(document_path: str) -> str:
    parts = document_path.split("/")
    if len(parts) >= 4:
        return "/".join(parts[:3])
    return "/".join(parts[:2])


def main() -> None:
    evidence_rows = read_jsonl(EVIDENCE_PATH)
    evidence_by_id = {str(row["id"]): row for row in evidence_rows}
    if len(evidence_by_id) != len(evidence_rows):
        raise ValueError("knowledge evidence ledger contains duplicate IDs")

    conversations = read_jsonl(CONVERSATIONS_PATH)
    provenance = read_jsonl(PROVENANCE_PATH)
    if len(conversations) != len(provenance):
        raise ValueError("conversation and provenance row counts differ")

    references: dict[str, list[dict[str, Any]]] = defaultdict(list)
    record_rights: Counter[str] = Counter()
    record_reviewed = 0
    stale_references: Counter[str] = Counter()
    for line_number, (conversation, trace) in enumerate(zip(conversations, provenance), 1):
        if trace.get("example_line") != line_number:
            raise ValueError(f"provenance example_line mismatch at row {line_number}")
        serialized = json.dumps(conversation, ensure_ascii=False, separators=(",", ":"))
        digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        if trace.get("messages_sha256") != digest:
            raise ValueError(f"conversation hash mismatch at row {line_number}")

        rights = permission_state(trace)
        approved = review_approved(trace)
        record_rights[rights] += 1
        record_reviewed += approved
        evidence_ids = set(trace.get("evidence_ids", []))
        for supporting_source in trace.get("supporting_sources", []):
            evidence_ids.update(supporting_source.get("evidence_ids", []))
        for evidence_id in evidence_ids:
            if evidence_id not in evidence_by_id:
                stale_references[evidence_id] += 1
                continue
            references[evidence_id].append(
                {
                    "example_line": line_number,
                    "rights": rights,
                    "approved": approved,
                    "export_ready": rights == "allowed" and approved,
                }
            )

    exclusions = read_jsonl(EXCLUSIONS_PATH)
    excluded_ids: set[str] = set()
    for exclusion in exclusions:
        excluded_ids.update(exclusion.get("evidence_ids", []))
        single_id = exclusion.get("evidence_id") or exclusion.get("id")
        if single_id:
            excluded_ids.add(str(single_id))
    excluded_ids.intersection_update(evidence_by_id)

    documents: dict[str, dict[str, int]] = defaultdict(
        lambda: {
            "evidence_units": 0,
            "mentioned_in_review": 0,
            "rights_cleared_in_review": 0,
            "rights_pending_or_restricted": 0,
            "export_ready": 0,
            "excluded": 0,
        }
    )
    topics: dict[str, dict[str, int]] = defaultdict(
        lambda: {
            "documents": 0,
            "evidence_units": 0,
            "mentioned_in_review": 0,
            "rights_cleared_in_review": 0,
            "rights_pending_or_restricted": 0,
            "export_ready": 0,
            "excluded": 0,
        }
    )

    for evidence_id, evidence in evidence_by_id.items():
        document_path = str(evidence.get("document_path", ""))
        topic = topic_for(document_path)
        document_counts = documents[document_path]
        topic_counts = topics[topic]
        for counts in (document_counts, topic_counts):
            counts["evidence_units"] += 1
            refs = references.get(evidence_id, [])
            if refs:
                counts["mentioned_in_review"] += 1
            if any(ref["rights"] == "allowed" for ref in refs):
                counts["rights_cleared_in_review"] += 1
            if any(ref["rights"] in {"pending", "prohibited", "mixed", "unknown"} for ref in refs):
                counts["rights_pending_or_restricted"] += 1
            if any(ref["export_ready"] for ref in refs):
                counts["export_ready"] += 1
            if evidence_id in excluded_ids:
                counts["excluded"] += 1

    topic_document_counts = Counter(topic_for(path) for path in documents)
    for topic, count in topic_document_counts.items():
        topics[topic]["documents"] = count

    for counts in (*documents.values(), *topics.values()):
        counts["remaining_unrepresented"] = (
            counts["evidence_units"] - counts["mentioned_in_review"] - counts["excluded"]
        )

    ready_records = sum(
        permission_state(trace) == "allowed" and review_approved(trace) for trace in provenance
    )
    report = {
        "scope": "docs/temes structural evidence; review mentions are not training approval",
        "documents_processed": len(documents),
        "evidence_units": len(evidence_by_id),
        "conversations": len(conversations),
        "provenance_rows": len(provenance),
        "evidence_units_mentioned_in_review": sum(bool(refs) for refs in references.values()),
        "evidence_units_with_redistributable_review_draft": sum(
            any(ref["rights"] == "allowed" for ref in refs) for refs in references.values()
        ),
        "evidence_units_export_ready": sum(
            any(ref["export_ready"] for ref in refs) for refs in references.values()
        ),
        "evidence_units_explicitly_excluded": len(excluded_ids),
        "evidence_units_remaining_unrepresented": len(evidence_by_id)
        - sum(bool(refs) for refs in references.values())
        - len(excluded_ids),
        "records_by_redistribution": dict(sorted(record_rights.items())),
        "human_reviewed_records": record_reviewed,
        "export_ready_records": ready_records,
        "stale_evidence_reference_count": sum(stale_references.values()),
        "stale_evidence_references": dict(sorted(stale_references.items())),
        "topic_coverage": dict(sorted(topics.items())),
        "document_coverage": dict(sorted(documents.items())),
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    temporary = REPORT_PATH.with_suffix(".json.tmp")
    temporary.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(REPORT_PATH)
    print(
        f"Knowledge review coverage: {report['evidence_units_mentioned_in_review']} / "
        f"{report['evidence_units']} evidence units referenced; "
        f"{report['export_ready_records']} export-ready records."
    )


if __name__ == "__main__":
    main()
