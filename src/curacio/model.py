"""Models immutables compartits entre etapes de curació."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class Gap:
    """Un buit epistèmic extret d'un article."""

    state: str
    text: str
    source_block_id: str
    reason: str
    decision: str = "incloure"


@dataclass(slots=True)
class Block:
    """Unitat tipada d'un document abans de formar chunks."""

    id: str
    kind: str
    section: str
    raw: str
    text: str = ""
    reason: str = ""
    decision: str = "incloure"
    gap_state: str = ""
    volatility: float | None = None
    pii: bool = False
    template: bool = False


@dataclass(slots=True)
class Chunk:
    """Fragment utilitzable o pendent amb traçabilitat al document origen."""

    id: str
    section: str
    blocks: list[Block]
    text: str
    volatility: float
    uses: list[str] = field(default_factory=list)
    decision: str = "incloure"
    reason: str = ""
    review_status: str = "unreviewed"
    pii: bool = False
    template: bool = False


@dataclass(slots=True)
class CuratedDoc:
    """Resultat de curar un document complet."""

    doc_id: str
    path: Path
    data: dict[str, Any]
    source_sha: str
    blocks: list[Block]
    chunks: list[Chunk]
    gaps: list[Gap]
    corrections: list[tuple[str, str]] = field(default_factory=list)
    source_paragraphs: list[str] = field(default_factory=list)

    @property
    def title(self) -> str:
        return str(self.data.get("title", self.doc_id.rsplit("/", maxsplit=1)[-1]))
