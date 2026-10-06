"""Generació local i traçable de candidats de conversa per a Maia Knowledge."""

from __future__ import annotations

import json
import re
from collections.abc import Iterable
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Literal, Protocol

from training_data.knowledge import EvidenceUnit, KnowledgeLedger
from training_data.text import markdown_to_plain_text

ReviewStatus = Literal["needs_review", "human_reviewed"]
CandidateStatus = Literal["included", "excluded", "unresolved"]
TABLE_SEPARATOR = re.compile(r"^:?-{3,}:?$")
CONFLICT_MARKERS = (
    "discrep",
    "contradi",
    "no coincideixen",
    "versions diferents",
    "divergeixen",
    "dues lectures",
)
UNKNOWN_MARKERS = (
    "no consta",
    "no permet determinar",
    "no permet establir",
    "no s'ha pogut",
    "no s'ha trobat",
    "no se sap",
    "no sabem",
    "buit registrat",
    "buit pendent",
    "desconegut",
)


@dataclass(frozen=True, slots=True)
class ConversationCandidate:
    """Candidat intern amb traça cap a les evidències que fonamenten la resposta."""

    family_id: str
    evidence_ids: tuple[str, ...]
    user: str
    assistant: str
    review_status: ReviewStatus

    def to_public_record(self) -> dict[str, list[dict[str, str]]]:
        """Retorna només l'esquema de missatges que s'exporta al dataset."""

        return {
            "messages": [
                {"role": "user", "content": self.user},
                {"role": "assistant", "content": self.assistant},
            ]
        }


@dataclass(frozen=True, slots=True)
class CandidateDecision:
    """Disposició explícita d'un candidat, amb la traça que permet auditar-la."""

    family_id: str
    evidence_ids: tuple[str, ...]
    status: CandidateStatus
    reason: str


@dataclass(frozen=True, slots=True)
class CandidateClassification:
    """Candidats elegibles i comptadors de les decisions de qualitat."""

    eligible_candidates: tuple[ConversationCandidate, ...]
    decisions: tuple[CandidateDecision, ...]
    included_count: int
    excluded_count: int
    unresolved_count: int
    explicit_conflict_count: int
    explicit_unknown_count: int


class CandidateGenerator(Protocol):
    """Interfície substituïble per a generadors de preguntes i respostes."""

    def generate(self, evidence: EvidenceUnit, title: str) -> ConversationCandidate | None:
        """Construeix un candidat o indica que la unitat no és conversacional."""


class LiteralEvidenceGenerator:
    """Crea esborranys literals només per a la cua interna de revisió humana."""

    def generate(self, evidence: EvidenceUnit, title: str) -> ConversationCandidate | None:
        content = markdown_to_plain_text(evidence.content, block_kind=evidence.block_kind)
        if not content or evidence.block_kind in {
            "heading",
            "code_block",
            "other",
            "metadata_title",
        }:
            return None
        if evidence.block_kind == "table_row":
            cells = [cell.strip() for cell in content.strip().strip("|").split("|")]
            if cells and all(TABLE_SEPARATOR.fullmatch(cell) for cell in cells):
                return None

        title = markdown_to_plain_text(title) or "aquesta fitxa"
        section = (
            markdown_to_plain_text(evidence.heading_path[-1]) if evidence.heading_path else None
        )
        section = section or None
        if section == title:
            section = None
        if evidence.block_kind == "metadata_description":
            question = f"Quin resum presenta la fitxa «{title}»?"
        elif evidence.block_kind == "table_row":
            question = (
                f"Què indica aquesta fila de «{section}»?"
                if section
                else f"Què indica aquesta fila de la fitxa «{title}»?"
            )
        elif evidence.block_kind == "list_item":
            question = (
                f"Quin element recull «{section}»?"
                if section
                else f"Quin element recull la fitxa «{title}»?"
            )
        elif section:
            question = f"Què explica la secció «{section}» de la fitxa «{title}»?"
        else:
            question = f"Quina informació recull la fitxa «{title}»?"
        return ConversationCandidate(
            family_id=evidence.id,
            evidence_ids=(evidence.id,),
            user=question,
            assistant=content,
            review_status="needs_review",
        )


def build_knowledge_candidates(
    ledger: KnowledgeLedger, generator: CandidateGenerator | None = None
) -> tuple[ConversationCandidate, ...]:
    """Crea candidats locals; l'exportació final encara requereix revisió i filtres."""

    selected_generator = generator or LiteralEvidenceGenerator()
    titles = {document.path: document.title or document.path for document in ledger.documents}
    candidates: list[ConversationCandidate] = []
    for evidence in ledger.units:
        candidate = selected_generator.generate(
            evidence, titles.get(evidence.document_path, evidence.document_path)
        )
        if candidate is not None:
            candidates.append(candidate)
    return tuple(candidates)


def review_candidate(
    candidate: ConversationCandidate,
    *,
    evidence_by_id: dict[str, EvidenceUnit],
    user: str,
    assistant: str,
) -> ConversationCandidate:
    """Aplica wording revisat per una persona sense canviar-ne la traçabilitat."""

    if not candidate.evidence_ids or any(
        evidence_id not in evidence_by_id for evidence_id in candidate.evidence_ids
    ):
        raise ValueError("candidate evidence IDs must resolve to known evidence units")
    if not user.strip() or not assistant.strip():
        raise ValueError("reviewed user and assistant wording must be non-empty")
    return replace(
        candidate,
        user=user.strip(),
        assistant=assistant.strip(),
        review_status="human_reviewed",
    )


def build_relation_candidates(ledger: KnowledgeLedger) -> tuple[ConversationCandidate, ...]:
    """Combina una relació interna amb fragments literals de les dues fitxes."""

    titles = {document.path: document.title or document.path for document in ledger.documents}
    units_by_path: dict[str, list[EvidenceUnit]] = {}
    for unit in ledger.units:
        units_by_path.setdefault(unit.document_path, []).append(unit)

    candidates: list[ConversationCandidate] = []
    seen: set[tuple[str, str]] = set()
    for relation in ledger.relations:
        target_path = relation.target_path
        if (
            not relation.internal
            or not relation.resolved
            or target_path is None
            or target_path == relation.source_path
            or target_path not in titles
        ):
            continue
        pair = (relation.source_path, target_path)
        if pair in seen:
            continue
        source_unit = _relation_evidence(
            units_by_path.get(relation.source_path, []), linked_target=relation.target
        )
        target_unit = _relation_evidence(units_by_path.get(target_path, []))
        if source_unit is None or target_unit is None:
            continue

        source_title = titles[relation.source_path]
        target_title = titles[target_path]
        source_text = markdown_to_plain_text(source_unit.content, block_kind=source_unit.block_kind)
        target_text = markdown_to_plain_text(target_unit.content, block_kind=target_unit.block_kind)
        if not source_text or not target_text:
            continue
        candidates.append(
            ConversationCandidate(
                family_id=f"relation:{relation.source_path}->{target_path}",
                evidence_ids=(source_unit.id, target_unit.id),
                user=f"Quina relació hi ha entre «{source_title}» i «{target_title}»?",
                assistant=(
                    f"La fitxa «{source_title}» enllaça amb «{target_title}». "
                    f"A la primera hi consta: «{source_text}» "
                    f"A la segona hi consta: «{target_text}»"
                ),
                review_status="needs_review",
            )
        )
        seen.add(pair)
    return tuple(candidates)


def classify_knowledge_candidates(
    candidates: tuple[ConversationCandidate, ...], ledger: KnowledgeLedger
) -> CandidateClassification:
    """Bloqueja esborranys, procedència no autoritzada i fets volàtils."""

    evidence_by_id = {unit.id: unit for unit in ledger.units}
    decisions: list[CandidateDecision] = []
    eligible: list[ConversationCandidate] = []
    conflict_count = 0
    unknown_count = 0
    for candidate in candidates:
        units = [evidence_by_id[item] for item in candidate.evidence_ids if item in evidence_by_id]
        if not candidate.evidence_ids or len(units) != len(candidate.evidence_ids):
            decision = CandidateDecision(
                candidate.family_id,
                candidate.evidence_ids,
                "unresolved",
                "evidence_reference_missing",
            )
        elif candidate.review_status != "human_reviewed":
            decision = CandidateDecision(
                candidate.family_id,
                candidate.evidence_ids,
                "unresolved",
                "human_review_required",
            )
        elif any(reference.status != "recorded" for unit in units for reference in unit.provenance):
            decision = CandidateDecision(
                candidate.family_id,
                candidate.evidence_ids,
                "unresolved",
                "missing_or_invalid_provenance",
            )
        elif any(
            reference.redistribution in {"pendent", "pending"}
            for unit in units
            for reference in unit.provenance
        ):
            decision = CandidateDecision(
                candidate.family_id,
                candidate.evidence_ids,
                "unresolved",
                "source_redistribution_pending",
            )
        elif any(
            reference.redistribution == "no" for unit in units for reference in unit.provenance
        ):
            decision = CandidateDecision(
                candidate.family_id,
                candidate.evidence_ids,
                "excluded",
                "source_redistribution_no",
            )
        elif any(unit.volatility_score >= 0.5 for unit in units):
            decision = CandidateDecision(
                candidate.family_id,
                candidate.evidence_ids,
                "excluded",
                "volatility_threshold",
            )
        else:
            content = " ".join((candidate.assistant, *(unit.content for unit in units))).casefold()
            if any(marker in content for marker in CONFLICT_MARKERS):
                conflict_count += 1
                reason = "explicit_conflict_preserved"
            elif any(marker in content for marker in UNKNOWN_MARKERS):
                unknown_count += 1
                reason = "explicit_unknown_preserved"
            else:
                reason = "source_and_evidence_resolved"
            decision = CandidateDecision(
                candidate.family_id,
                candidate.evidence_ids,
                "included",
                reason,
            )
            eligible.append(candidate)
        decisions.append(decision)

    return CandidateClassification(
        eligible_candidates=tuple(eligible),
        decisions=tuple(decisions),
        included_count=sum(item.status == "included" for item in decisions),
        excluded_count=sum(item.status == "excluded" for item in decisions),
        unresolved_count=sum(item.status == "unresolved" for item in decisions),
        explicit_conflict_count=conflict_count,
        explicit_unknown_count=unknown_count,
    )


def _relation_evidence(
    units: list[EvidenceUnit], *, linked_target: str | None = None
) -> EvidenceUnit | None:
    preference = {
        "paragraph": 0,
        "blockquote": 1,
        "list_item": 2,
        "table_row": 3,
        "metadata_description": 4,
    }
    eligible = [unit for unit in units if unit.block_kind in preference and unit.content.strip()]
    if linked_target is not None:
        linked = [unit for unit in eligible if linked_target in unit.content]
        if linked:
            return min(linked, key=lambda unit: preference[unit.block_kind])
    return min(eligible, key=lambda unit: preference[unit.block_kind]) if eligible else None


def write_knowledge_candidates(
    candidates: tuple[ConversationCandidate, ...],
    *,
    work: Path,
    classification: CandidateClassification | None = None,
    public_candidates: tuple[ConversationCandidate, ...] | None = None,
    deduplicated_candidates: tuple[ConversationCandidate, ...] | None = None,
) -> Path:
    """Escriu candidats interns i missatges aprovats per la classificació local."""

    work.mkdir(parents=True, exist_ok=True)
    internal_path = work / "candidates.jsonl"
    public_path = work / "candidate-messages.jsonl"
    _atomic_jsonl(internal_path, (asdict(candidate) for candidate in candidates))
    if deduplicated_candidates is not None:
        _atomic_jsonl(
            work / "deduplicated-candidates.jsonl",
            (asdict(candidate) for candidate in deduplicated_candidates),
        )
    selected_public = public_candidates
    if selected_public is None:
        selected_public = classification.eligible_candidates if classification else candidates
    if classification is not None:
        eligible_evidence = {
            evidence_id
            for item in classification.eligible_candidates
            for evidence_id in item.evidence_ids
        }
        selected_public = tuple(
            candidate
            for candidate in selected_public
            if candidate.review_status == "human_reviewed"
            and set(candidate.evidence_ids) <= eligible_evidence
        )
    else:
        selected_public = tuple(
            candidate
            for candidate in selected_public
            if candidate.review_status == "human_reviewed"
        )
    _atomic_jsonl(public_path, (candidate.to_public_record() for candidate in selected_public))
    if classification is not None:
        _atomic_jsonl(
            work / "candidate-decisions.jsonl",
            (asdict(decision) for decision in classification.decisions),
        )
        summary_path = work / "candidate-classification.json"
        temporary = summary_path.with_suffix(".json.tmp")
        temporary.write_text(
            json.dumps(
                {
                    "included": classification.included_count,
                    "excluded": classification.excluded_count,
                    "unresolved": classification.unresolved_count,
                    "explicit_conflicts": classification.explicit_conflict_count,
                    "explicit_unknowns": classification.explicit_unknown_count,
                },
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        temporary.replace(summary_path)
    return internal_path


def _atomic_jsonl(path: Path, records: Iterable[object]) -> None:
    content = "".join(
        json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in records
    )
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content, encoding="utf-8", newline="")
    temporary.replace(path)
