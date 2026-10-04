"""Reconciliació de les evidències Knowledge amb candidats i exclusions."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

from training_data.knowledge import EvidenceUnit, KnowledgeLedger
from training_data.knowledge_generate import CandidateClassification

EvidenceStatus = Literal["represented", "excluded", "unresolved"]
TABLE_SEPARATOR = re.compile(r"^:?-{3,}:?$")
NON_CONVERSATIONAL_KINDS = {"heading", "code_block", "other", "metadata_title"}


@dataclass(frozen=True, slots=True)
class EvidenceCoverage:
    """Estat final d'una unitat i si entra al denominador entrenable."""

    evidence_id: str
    document_path: str
    status: EvidenceStatus
    reason: str
    trainable_eligible: bool


@dataclass(frozen=True, slots=True)
class DocumentCoverage:
    """Reconciliació de les unitats d'una fitxa temàtica."""

    path: str
    detected_units: int
    represented_units: int
    excluded_units: int
    unresolved_units: int


@dataclass(frozen=True, slots=True)
class KnowledgeCoverageReport:
    """Cobertura global total i entrenable, amb detall per fitxa i unitat."""

    processed_documents: int
    markdown_errors: int
    total_evidence_units: int
    represented_units: int
    excluded_units: int
    unresolved_units: int
    total_classified_units: int
    total_coverage: float
    trainable_units: int
    trainable_represented_units: int
    trainable_coverage: float
    documents: tuple[DocumentCoverage, ...]
    units: tuple[EvidenceCoverage, ...]


def _is_table_separator(unit: EvidenceUnit) -> bool:
    if unit.block_kind != "table_row":
        return False
    cells = [cell.strip() for cell in unit.content.strip().strip("|").split("|")]
    return bool(cells) and all(TABLE_SEPARATOR.fullmatch(cell) for cell in cells)


def _is_trainable_eligible(unit: EvidenceUnit) -> bool:
    return (
        bool(unit.provenance)
        and all(reference.status == "recorded" for reference in unit.provenance)
        and unit.volatility_score < 0.5
        and unit.block_kind not in NON_CONVERSATIONAL_KINDS
        and not _is_table_separator(unit)
    )


def build_knowledge_coverage(
    ledger: KnowledgeLedger, classification: CandidateClassification
) -> KnowledgeCoverageReport:
    """Classifica cada unitat detectada i calcula les dues cobertures."""

    by_evidence: dict[str, list[tuple[str, str]]] = {}
    for decision in classification.decisions:
        for evidence_id in decision.evidence_ids:
            by_evidence.setdefault(evidence_id, []).append((decision.status, decision.reason))

    evidence_rows: list[EvidenceCoverage] = []
    for unit in ledger.units:
        decisions = by_evidence.get(unit.id, [])
        if any(status == "included" for status, _ in decisions):
            status: EvidenceStatus = "represented"
            reason = "candidate_included"
        elif any(status == "excluded" for status, _ in decisions):
            status = "excluded"
            reason = next(reason for state, reason in decisions if state == "excluded")
        elif any(state == "unresolved" for state, _ in decisions):
            status = "unresolved"
            reason = next(reason for state, reason in decisions if state == "unresolved")
        elif unit.block_kind in NON_CONVERSATIONAL_KINDS:
            status = "excluded"
            reason = "structural_context_not_a_conversation"
        elif _is_table_separator(unit):
            status = "excluded"
            reason = "table_separator_not_evidence"
        else:
            status = "unresolved"
            reason = "no_conversation_candidate"
        evidence_rows.append(
            EvidenceCoverage(
                evidence_id=unit.id,
                document_path=unit.document_path,
                status=status,
                reason=reason,
                trainable_eligible=_is_trainable_eligible(unit),
            )
        )

    by_document: dict[str, list[EvidenceCoverage]] = {
        document.path: [] for document in ledger.documents
    }
    for row in evidence_rows:
        by_document.setdefault(row.document_path, []).append(row)
    document_rows = tuple(
        DocumentCoverage(
            path=path,
            detected_units=len(rows),
            represented_units=sum(row.status == "represented" for row in rows),
            excluded_units=sum(row.status == "excluded" for row in rows),
            unresolved_units=sum(row.status == "unresolved" for row in rows),
        )
        for path, rows in sorted(by_document.items())
    )
    total = len(evidence_rows)
    represented = sum(row.status == "represented" for row in evidence_rows)
    excluded = sum(row.status == "excluded" for row in evidence_rows)
    unresolved = sum(row.status == "unresolved" for row in evidence_rows)
    trainable_rows = [row for row in evidence_rows if row.trainable_eligible]
    trainable_represented = sum(row.status == "represented" for row in trainable_rows)
    classified = represented + excluded + unresolved
    return KnowledgeCoverageReport(
        processed_documents=ledger.report.processed_documents,
        markdown_errors=ledger.report.markdown_errors,
        total_evidence_units=total,
        represented_units=represented,
        excluded_units=excluded,
        unresolved_units=unresolved,
        total_classified_units=classified,
        total_coverage=classified / total if total else 1.0,
        trainable_units=len(trainable_rows),
        trainable_represented_units=trainable_represented,
        trainable_coverage=trainable_represented / len(trainable_rows) if trainable_rows else 1.0,
        documents=document_rows,
        units=tuple(evidence_rows),
    )


def write_knowledge_coverage(report: KnowledgeCoverageReport, *, reports: Path) -> Path:
    """Escriu el report extens de cobertura amb substitució atòmica."""

    reports.mkdir(parents=True, exist_ok=True)
    path = reports / "coverage.json"
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(
        json.dumps(asdict(report), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)
    return path
