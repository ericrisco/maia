"""Generació local i traçable de candidats de conversa per a Maia Knowledge."""

from __future__ import annotations

import json
import re
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal, Protocol

from training_data.knowledge import EvidenceUnit, KnowledgeLedger

ReviewStatus = Literal["needs_review"]
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
