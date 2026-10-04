"""Generació local i traçable de candidats de conversa per a Maia Knowledge."""

from __future__ import annotations

import json
import re
from collections.abc import Iterable
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Literal, Protocol

from training_data.knowledge import EvidenceUnit, KnowledgeLedger

ReviewStatus = Literal["needs_review", "human_reviewed"]
TABLE_SEPARATOR = re.compile(r"^:?-{3,}:?$")


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


class CandidateGenerator(Protocol):
    """Interfície substituïble per a generadors de preguntes i respostes."""

    def generate(self, evidence: EvidenceUnit, title: str) -> ConversationCandidate | None:
        """Construeix un candidat o indica que la unitat no és conversacional."""


class LiteralEvidenceGenerator:
    """Crea una pregunta plantilla i preserva literalment el text de l'evidència."""

    def generate(self, evidence: EvidenceUnit, title: str) -> ConversationCandidate | None:
        content = evidence.content.strip()
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

        section = evidence.heading_path[-1] if evidence.heading_path else None
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
        candidates.append(
            ConversationCandidate(
                family_id=f"relation:{relation.source_path}->{target_path}",
                evidence_ids=(source_unit.id, target_unit.id),
                user=f"Quina relació hi ha entre «{source_title}» i «{target_title}»?",
                assistant=(
                    f"La fitxa «{source_title}» enllaça amb «{target_title}». "
                    f"A la primera hi consta: «{source_unit.content.strip()}» "
                    f"A la segona hi consta: «{target_unit.content.strip()}»"
                ),
                review_status="needs_review",
            )
        )
        seen.add(pair)
    return tuple(candidates)


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
    candidates: tuple[ConversationCandidate, ...], *, work: Path
) -> Path:
    """Escriu candidats interns i la vista pública provisional en fitxers locals."""

    work.mkdir(parents=True, exist_ok=True)
    internal_path = work / "candidates.jsonl"
    public_path = work / "candidate-messages.jsonl"
    _atomic_jsonl(internal_path, (asdict(candidate) for candidate in candidates))
    _atomic_jsonl(public_path, (candidate.to_public_record() for candidate in candidates))
    return internal_path


def _atomic_jsonl(path: Path, records: Iterable[object]) -> None:
    content = "".join(
        json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in records
    )
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content, encoding="utf-8", newline="")
    temporary.replace(path)
