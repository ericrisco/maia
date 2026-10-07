#!/usr/bin/env python3
"""Validate approved Knowledge records and calculate structural unit coverage."""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "training-data" / "knowledge"
REVIEW = DATA / "review"
WORK = DATA / "work"
REPORTS = DATA / "reports"
STATUSES = {"draft", "approved", "approved_sample", "rejected"}
EXCLUSIONS = {"excluded_rights", "no_natural_question", "not_knowledge", "duplicate"}
FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---(?:\s*\n|\Z)", re.DOTALL)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{number}: invalid JSON: {exc}") from exc
        if not isinstance(row, dict):
            raise ValueError(f"{path}:{number}: expected a JSON object")
        rows.append(row)
    return rows


def validate_conversation(row: dict[str, Any], number: int) -> None:
    if set(row) != {"messages"}:
        raise ValueError(f"conversations.jsonl:{number}: only the messages field is allowed")
    messages = row["messages"]
    if not isinstance(messages, list) or len(messages) < 2 or len(messages) % 2:
        raise ValueError(f"conversations.jsonl:{number}: expected at least one complete user/assistant exchange")
    for index, message in enumerate(messages):
        expected_role = "user" if index % 2 == 0 else "assistant"
        if not isinstance(message, dict) or set(message) != {"role", "content"}:
            raise ValueError(f"conversations.jsonl:{number}: message {index + 1} has invalid fields")
        if message["role"] != expected_role or not isinstance(message["content"], str) or not message["content"].strip():
            raise ValueError(f"conversations.jsonl:{number}: message {index + 1} has an invalid role or empty content")


def require_string_list(value: Any, field: str, number: int) -> list[str]:
    if not isinstance(value, list) or not value or any(not isinstance(item, str) or not item.strip() for item in value):
        raise ValueError(f"provenance.jsonl:{number}: {field} must be a non-empty list of strings")
    return value


def is_redistributable(value: Any) -> bool:
    return str(value).strip().lower() in {"si", "sí", "yes", "true"}


def font_metadata(source_id: str, number: int) -> dict[str, Any]:
    path = ROOT / source_id
    if not path.is_file():
        raise ValueError(f"provenance.jsonl:{number}: source ID does not exist: {source_id}")
    match = FRONTMATTER.match(path.read_text(encoding="utf-8"))
    if not match:
        raise ValueError(f"provenance.jsonl:{number}: source has no YAML frontmatter: {source_id}")
    try:
        metadata = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        raise ValueError(f"provenance.jsonl:{number}: invalid source YAML: {source_id}: {exc}") from exc
    if not isinstance(metadata, dict):
        raise ValueError(f"provenance.jsonl:{number}: source frontmatter is not a mapping: {source_id}")
    return metadata


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate records and regenerate coverage reports")
    args = parser.parse_args()
    inventory_path = WORK / "document-inventory.json"
    if not inventory_path.exists():
        raise SystemExit("document inventory missing; run build_knowledge_inventory.py first")
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    unit_to_document: dict[str, str] = {}
    document_data: dict[str, dict[str, Any]] = {}
    for document in inventory["documents"]:
        document_data[document["path"]] = document
        for unit in document["units"]:
            unit_to_document[unit["unit_id"]] = document["path"]

    conversations = read_jsonl(REVIEW / "conversations.jsonl")
    provenance = read_jsonl(REVIEW / "provenance.jsonl")
    if len(conversations) != len(provenance):
        raise ValueError(f"{len(conversations)} conversations but {len(provenance)} provenance records")

    record_ids: set[str] = set()
    conversation_keys: set[str] = set()
    approved_units: set[str] = set()
    units_by_document: dict[str, set[str]] = defaultdict(set)
    records_by_document: dict[str, set[str]] = defaultdict(set)
    approved_records = 0
    for number, (conversation, record) in enumerate(zip(conversations, provenance), 1):
        validate_conversation(conversation, number)
        key = json.dumps(conversation, ensure_ascii=False, sort_keys=True)
        if key in conversation_keys:
            raise ValueError(f"conversations.jsonl:{number}: exact duplicate conversation")
        conversation_keys.add(key)

        record_id = record.get("record_id")
        if not isinstance(record_id, str) or not record_id.strip() or record_id in record_ids:
            raise ValueError(f"provenance.jsonl:{number}: missing or duplicate record_id")
        record_ids.add(record_id)
        source_documents = require_string_list(record.get("source_documents"), "source_documents", number)
        source_ids = require_string_list(record.get("source_ids"), "source_ids", number)
        claims = require_string_list(record.get("claims_supported"), "claims_supported", number)
        del claims
        for field in ("license", "attribution", "limits", "split_group"):
            if not isinstance(record.get(field), str) or not record[field].strip():
                raise ValueError(f"provenance.jsonl:{number}: missing {field}")
        review_status = record.get("review_status")
        if not isinstance(review_status, str) or review_status not in STATUSES:
            raise ValueError(f"provenance.jsonl:{number}: review_status must be one of {sorted(STATUSES)}")
        if review_status == "approved_sample":
            require_string_list(record.get("source_locations"), "source_locations", number)
            unit_ids = record.get("unit_ids", [])
            if not isinstance(unit_ids, list) or any(not isinstance(item, str) for item in unit_ids):
                raise ValueError(f"provenance.jsonl:{number}: unit_ids must be a list of strings")
        else:
            unit_ids = require_string_list(record.get("unit_ids"), "unit_ids", number)
        if len(unit_ids) != len(set(unit_ids)):
            raise ValueError(f"provenance.jsonl:{number}: duplicate unit_ids")

        for source in source_documents:
            if not (ROOT / source).is_file():
                raise ValueError(f"provenance.jsonl:{number}: source does not exist: {source}")
        for source_id in source_ids:
            metadata = font_metadata(source_id, number)
            if review_status in {"approved", "approved_sample"} and not is_redistributable(metadata.get("redistribucio")):
                raise ValueError(f"provenance.jsonl:{number}: source is not cleared for redistribution: {source_id}")
        for unit_id in unit_ids:
            document_path = unit_to_document.get(unit_id)
            if not document_path:
                raise ValueError(f"provenance.jsonl:{number}: unknown unit_id: {unit_id}")
            if document_path not in source_documents:
                raise ValueError(f"provenance.jsonl:{number}: unit is not listed in source_documents: {unit_id}")
            if review_status == "approved":
                approved_units.add(unit_id)
                units_by_document[document_path].add(unit_id)
                records_by_document[document_path].add(record_id)
        if review_status == "approved":
            approved_records += 1

    sample_records = sum(record.get("review_status") == "approved_sample" for record in provenance)

    decisions = read_jsonl(REVIEW / "unit-decisions.jsonl")
    excluded_units: set[str] = set()
    excluded_reasons: Counter[str] = Counter()
    for number, decision in enumerate(decisions, 1):
        unit_id = decision.get("unit_id")
        status = decision.get("decision")
        reason = decision.get("reason")
        source_ids = require_string_list(decision.get("source_ids"), "source_ids", number)
        del source_ids
        if unit_id not in unit_to_document:
            raise ValueError(f"unit-decisions.jsonl:{number}: unknown unit_id: {unit_id}")
        if status not in EXCLUSIONS or not isinstance(reason, str) or not reason.strip():
            raise ValueError(f"unit-decisions.jsonl:{number}: invalid decision or missing reason")
        if unit_id in excluded_units:
            raise ValueError(f"unit-decisions.jsonl:{number}: duplicate unit decision: {unit_id}")
        if unit_id in approved_units:
            raise ValueError(f"unit-decisions.jsonl:{number}: unit is both covered and excluded: {unit_id}")
        excluded_units.add(unit_id)
        excluded_reasons[status] += 1

    if approved_units.intersection(excluded_units):
        raise ValueError("a unit cannot be both covered and excluded")
    all_units = set(unit_to_document)
    unresolved_units = all_units - approved_units - excluded_units
    status_documents: dict[str, Any] = {}
    by_topic: dict[str, dict[str, int]] = defaultdict(lambda: {"documents": 0, "units": 0, "covered": 0, "excluded": 0, "open": 0})
    for path, document in document_data.items():
        doc_units = {unit["unit_id"] for unit in document["units"]}
        covered_count = len(doc_units & approved_units)
        excluded_count = len(doc_units & excluded_units)
        open_count = len(doc_units - approved_units - excluded_units)
        state = "complete" if open_count == 0 else "in_progress" if covered_count or excluded_count else "not_started"
        status_documents[path] = {
            "title": document["title"],
            "type": document["type"],
            "topic": document["topic"],
            "status": state,
            "unit_count": len(doc_units),
            "covered_unit_ids": sorted(doc_units & approved_units),
            "excluded_unit_count": excluded_count,
            "open_unit_count": open_count,
            "conversation_ids": sorted(records_by_document.get(path, set())),
        }
        topic = document["topic"] or "(sense tema)"
        aggregate = by_topic[topic]
        aggregate["documents"] += 1
        aggregate["units"] += len(doc_units)
        aggregate["covered"] += covered_count
        aggregate["excluded"] += excluded_count
        aggregate["open"] += open_count

    WORK.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    status_path = WORK / "document-status.json"
    status_path.write_text(json.dumps({"source_root": "docs/temes/", "documents": status_documents}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    coverage = len(approved_units) / len(all_units) * 100 if all_units else 0
    lines = [
        "# Cobertura de Maia Knowledge", "",
        "La cobertura es per unitat estructural de l'inventari. Un bloc només compta com a cobert quan una conversa aprovada hi apunta. Les exclusions necessiten una decisió i un motiu per unitat.", "",
        f"- Documents inventariats: **{len(document_data)}** ({inventory['article_count']} articles).",
        f"- Unitats estructurals totals: **{len(all_units)}**.",
        f"- Unitats cobertes per converses aprovades: **{len(approved_units)}** ({coverage:.3f}%).",
        f"- Unitats excloses amb motiu: **{len(excluded_units)}**.",
        f"- Unitats encara obertes: **{len(unresolved_units)}**.",
        f"- Converses candidates: **{len(conversations)}**; aprovades: **{approved_records}**; mostres de calibratge: **{sample_records}** (no compten com a cobertura).",
        "", "## Estat per tema", "", "| Tema | Documents | Unitats | Cobertes | Excloses | Obertes |", "|---|---:|---:|---:|---:|---:|",
    ]
    for topic, counts in sorted(by_topic.items()):
        lines.append(f"| `{topic}` | {counts['documents']} | {counts['units']} | {counts['covered']} | {counts['excluded']} | {counts['open']} |")
    if excluded_reasons:
        lines += ["", "## Exclusions per motiu", ""]
        lines.extend(f"- `{reason}`: {count}." for reason, count in sorted(excluded_reasons.items()))
    (REPORTS / "coverage-summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Documents: {len(document_data)}; units: {len(all_units)}; covered: {len(approved_units)}; excluded: {len(excluded_units)}; open: {len(unresolved_units)}; approved conversations: {approved_records}; calibration samples: {sample_records}")


if __name__ == "__main__":
    main()
