"""E8: serialization estable de l'inventari de blocs, chunks i buits."""

from __future__ import annotations

import csv
import re
from io import StringIO

from curacio.model import Block, CuratedDoc, Gap

EXAMPLE_COLUMNS = [
    "id",
    "tipus",
    "seccio",
    "desti",
    "usos",
    "decisio",
    "motiu",
    "volatilitat",
    "estat_buit",
]
DOCUMENT_COLUMNS = [
    "doc_id",
    "font",
    "familia_font",
    "llicencia",
    "redistribucio",
    "domini",
    "anys",
    "entitats",
    "estat_revisio",
]


def _float(value: float | None) -> str:
    """Renders volatility as a stable decimal or a missing marker."""
    return "-" if value is None else f"{value:.1f}"


def _block_reason(block: Block, destination: str) -> str:
    """Provides a stable evidence-based reason when segmentation has none."""
    if block.reason:
        return block.reason
    if destination != "chunks":
        return "fora dels usos de dades"
    lowered = block.raw.casefold()
    if re.search(r"en\s+exercici", lowered) and re.search(r"en\s+actiu", lowered):
        return (
            "cos interpretatiu amb cites atribuïdes; «en exercici» i «en actiu» "
            f"són el mateix senyal → {block.volatility:.1f}"
        )
    return "cos factual"


def _row(
    identifier: str,
    kind: str,
    section: str,
    destination: str,
    uses: list[str],
    decision: str,
    reason: str,
    volatility: float | None,
    gap_state: str,
    doc: CuratedDoc,
    metadata: dict[str, str],
    review_status: str = "-",
) -> list[str]:
    return [
        identifier,
        kind,
        section or "-",
        destination,
        ",".join(uses) if uses else "-",
        decision,
        reason or "-",
        _float(volatility),
        gap_state or "-",
        doc.doc_id,
        metadata.get("font", ""),
        metadata.get("familia_font", ""),
        metadata.get("llicencia", ""),
        metadata.get("redistribucio", "pendent"),
        metadata.get("domini", "sense-domini"),
        metadata.get("anys", ""),
        metadata.get("entitats", ""),
        review_status,
    ]


def inventory_rows(
    doc: CuratedDoc,
    metadata: dict[str, str],
    gaps: list[Gap],
) -> list[list[str]]:
    """Builds stable rows in source-block, chunk, then individual-gap order."""
    rows: list[list[str]] = []
    doc_id = doc.doc_id
    gaps_by_block: dict[str, list[Gap]] = {}
    for gap in gaps:
        gaps_by_block.setdefault(gap.source_block_id, []).append(gap)
    for block in doc.blocks:
        associated = gaps_by_block.get(block.id, [])
        if block.kind == "buit":
            eligible = [gap for gap in associated if gap.decision == "incloure"]
            uses = ["raft-sense-oracle"] if eligible else []
            decision = "incloure" if eligible else "excloure"
            states = {gap.state for gap in associated}
            state = next(iter(states)) if len(states) == 1 else block.gap_state or "-"
            if len(states) == 1 and states:
                reason = f"buit {state}"
            elif len(associated) > 1:
                counts: dict[str, int] = {}
                for gap in associated:
                    counts[gap.state] = counts.get(gap.state, 0) + 1
                state_summary = ", ".join(f"{count} {label}" for label, count in counts.items())
                reason = f"{len(associated)} ítems: {state_summary}"
            else:
                reason = associated[0].reason if associated else block.reason or "sense ítems"
            rows.append(
                _row(
                    f"{doc_id}{block.id}",
                    block.kind,
                    block.section,
                    "buits" if eligible else "-",
                    uses,
                    decision,
                    reason,
                    None,
                    state,
                    doc,
                    metadata,
                )
            )
            continue
        parent_chunk = next((chunk for chunk in doc.chunks if block in chunk.blocks), None)
        if block.kind == "transcripcio" and doc.data.get("type") == "parla":
            destination = "llengua"
            uses = ["llengua"]
        elif parent_chunk is not None and block.decision == "incloure":
            destination = "chunks"
            uses = parent_chunk.uses
        else:
            destination = "-"
            uses = []
        decision = block.decision
        rows.append(
            _row(
                f"{doc_id}{block.id}",
                block.kind,
                block.section,
                destination,
                uses,
                decision,
                _block_reason(block, destination),
                block.volatility
                if block.kind in {"cos", "taula", "cita"} and block.decision == "incloure"
                else None,
                block.gap_state,
                doc,
                metadata,
            )
        )
    for chunk in doc.chunks:
        rows.append(
            _row(
                chunk.id,
                "chunk",
                chunk.section,
                "chunks" if chunk.decision != "excloure" else "-",
                chunk.uses,
                chunk.decision,
                chunk.reason,
                chunk.volatility,
                "",
                doc,
                metadata,
                chunk.review_status,
            )
        )
    for index, gap in enumerate(gaps, start=1):
        if gap.decision == "excloure" and doc.data.get("type") == "parla":
            continue
        rows.append(
            _row(
                f"{doc_id}#g{index}",
                "buit",
                "Buits registrats",
                "buits" if gap.decision == "incloure" else "-",
                ["raft-sense-oracle"] if gap.decision == "incloure" else [],
                gap.decision,
                gap.reason,
                None,
                gap.state,
                doc,
                metadata,
            )
        )
    return rows


def render_inventory(documents: list[tuple[CuratedDoc, dict[str, str], list[Gap]]]) -> str:
    """Serializes the complete inventory with UTF-8, tabs and LF line endings."""
    stream = StringIO(newline="")
    writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
    writer.writerow(EXAMPLE_COLUMNS + DOCUMENT_COLUMNS)
    for doc, metadata, gaps in documents:
        writer.writerows(inventory_rows(doc, metadata, gaps))
    return stream.getvalue()
