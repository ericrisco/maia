"""Build the traceable Knowledge ledger and per-document coverage register."""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter
from itertools import pairwise
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "src"))

from training_data.inventory import scan_tree  # noqa: E402
from training_data.knowledge import (  # noqa: E402
    EvidenceUnit,
    extract_knowledge,
    write_knowledge_extraction,
)
from training_data.knowledge_generate import load_review_conversations  # noqa: E402

TABLE_SEPARATOR = re.compile(r"^:?-{3,}:?$")
NON_CONVERSATIONAL_KINDS = {"heading", "code_block", "other", "metadata_title"}


def is_table_separator(unit: EvidenceUnit) -> bool:
    if unit.block_kind != "table_row":
        return False
    cells = [cell.strip() for cell in unit.content.strip().strip("|").split("|")]
    return bool(cells) and all(TABLE_SEPARATOR.fullmatch(cell) for cell in cells)


def table_header_ids(units: list[EvidenceUnit]) -> set[str]:
    """Return header rows immediately followed by a Markdown separator row."""

    return {
        current.id
        for current, following in pairwise(units)
        if current.block_kind == "table_row" and is_table_separator(following)
    }


def exclusion_reason(
    unit: EvidenceUnit, *, table_headers: set[str] | None = None
) -> str | None:
    """Exclude only structural blocks, never factual content by default."""

    block_kind = unit.block_kind
    if block_kind in NON_CONVERSATIONAL_KINDS:
        return "structural_block_not_conversational_knowledge"
    if unit.id in (table_headers or set()):
        return "table_header_context_not_standalone_knowledge"
    if is_table_separator(unit):
        return "table_separator_not_knowledge"
    return None


def load_manual_exclusions(path: Path, evidence_ids: set[str]) -> dict[str, str]:
    """Load reviewed exclusions for source-curation notes, not domain facts."""

    if not path.exists():
        return {}
    exclusions: dict[str, str] = {}
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        record = json.loads(line)
        evidence_id = record.get("evidence_id")
        reason = record.get("reason")
        if evidence_id not in evidence_ids:
            raise ValueError(f"Unknown manual exclusion at {path}:{line_number}: {evidence_id}")
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError(f"Missing exclusion reason at {path}:{line_number}")
        if evidence_id in exclusions:
            raise ValueError(f"Duplicate manual exclusion at {path}:{line_number}: {evidence_id}")
        exclusions[evidence_id] = reason.strip()
    return exclusions


def main() -> None:
    inventory = scan_tree(REPO / "docs")
    ledger = extract_knowledge(inventory)
    work = REPO / "training-data/knowledge/work"
    reports = REPO / "training-data/knowledge/reports"
    report = write_knowledge_extraction(ledger, work=work, reports=reports)

    review_conversations = REPO / "training-data/knowledge/review/conversations.jsonl"
    review_provenance = REPO / "training-data/knowledge/review/provenance.jsonl"
    candidates = load_review_conversations(review_conversations, review_provenance, ledger)
    candidate_evidence = {
        evidence_id
        for candidate in candidates
        if candidate.review_status != "human_reviewed"
        for evidence_id in candidate.evidence_ids
    }
    approved_evidence = {
        evidence_id
        for candidate in candidates
        if candidate.review_status == "human_reviewed"
        for evidence_id in candidate.evidence_ids
    }
    candidate_evidence -= approved_evidence

    units_by_document: dict[str, list[object]] = {}
    unit_exclusions: dict[str, str] = {}
    evidence_ids = {unit.id for unit in ledger.units}
    manual_exclusions = load_manual_exclusions(
        work / "manual-unit-exclusions.jsonl", evidence_ids
    )
    headers = table_header_ids(ledger.units)
    for unit in ledger.units:
        units_by_document.setdefault(unit.document_path, []).append(unit)
        reason = exclusion_reason(unit, table_headers=headers)
        if reason is not None:
            unit_exclusions[unit.id] = reason
    for evidence_id, reason in manual_exclusions.items():
        if evidence_id in unit_exclusions:
            raise ValueError(f"Manual exclusion duplicates structural exclusion: {evidence_id}")
        unit_exclusions[evidence_id] = reason
    links_by_document = Counter(relation.source_path for relation in ledger.relations)

    unit_exclusions_path = work / "unit-exclusions.jsonl"
    with unit_exclusions_path.open("w", encoding="utf-8", newline="") as output:
        for evidence_id, reason in sorted(unit_exclusions.items()):
            output.write(
                json.dumps(
                    {"evidence_id": evidence_id, "reason": reason},
                    ensure_ascii=False,
                    separators=(",", ":"),
                )
                + "\n"
            )

    coverage_path = work / "coverage.csv"
    with coverage_path.open("w", encoding="utf-8", newline="") as output:
        writer = csv.writer(output, lineterminator="\n")
        writer.writerow(
            [
                "source_path",
                "document_type",
                "title",
                "source_ids",
                "source_paths",
                "redistribucio",
                "evidence_units",
                "sections",
                "paragraphs",
                "list_items",
                "table_rows",
                "blockquotes",
                "links",
                "candidate_units",
                "approved_units",
                "excluded_units",
                "unresolved_units",
                "coverage_status",
                "review_notes",
            ]
        )
        for document in ledger.documents:
            units = units_by_document.get(document.path, [])
            kinds = Counter(unit.block_kind for unit in units)
            sections = {
                unit.heading_path
                for unit in units
                if unit.block_kind == "heading" and unit.heading_path
            }
            document_ids = {unit.id for unit in units}
            candidate_count = len(document_ids & candidate_evidence)
            approved_count = len(document_ids & approved_evidence)
            excluded_evidence_ids = document_ids & unit_exclusions.keys()
            excluded_evidence_ids -= candidate_evidence
            excluded_evidence_ids -= approved_evidence
            excluded_count = len(excluded_evidence_ids)
            unresolved_count = len(units) - candidate_count - approved_count - excluded_count
            if unresolved_count == 0 and candidate_count == 0:
                status = "complete"
            elif unresolved_count == 0:
                status = "awaiting_approval"
            elif candidate_count or approved_count:
                status = "in_progress"
            else:
                status = "not_started"
            references = document.provenance
            writer.writerow(
                [
                    f"docs/{document.path}",
                    document.document_type,
                    document.title,
                    ";".join(ref.source_id or "" for ref in references),
                    ";".join(ref.source_path or "" for ref in references),
                    ";".join(ref.redistribution or ref.status for ref in references),
                    len(units),
                    len(sections),
                    kinds["paragraph"],
                    kinds["list_item"],
                    kinds["table_row"],
                    kinds["blockquote"],
                    links_by_document[document.path],
                    candidate_count,
                    approved_count,
                    excluded_count,
                    unresolved_count,
                    status,
                    document.error or "",
                ]
            )
    print(f"Documents processed: {report.processed_documents}")
    print(f"Markdown errors: {report.markdown_errors}")
    print(f"Sections: {report.sections_processed}")
    print(f"Tables / rows: {report.tables_processed} / {report.table_rows_processed}")
    print(f"Evidence units: {report.units_detected}")
    print(f"Review candidates: {len(candidates)}")
    print(f"Structural exclusions: {len(unit_exclusions)}")
    print(
        f"Coverage register: {coverage_path.relative_to(REPO)} "
        f"({len(ledger.documents)} documents)"
    )


if __name__ == "__main__":
    main()
