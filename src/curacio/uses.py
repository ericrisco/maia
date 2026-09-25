"""E5: assignació dels usos de destí als fragments."""

from __future__ import annotations

from curacio.model import Chunk, CuratedDoc, Gap


def assign_uses(chunk: Chunk, doc: CuratedDoc) -> list[str]:
    """Returns uses from volatility and voice; no retrieval content is invented."""
    if doc.data.get("type") == "parla":
        return ["llengua"] if doc.data.get("veu") == "originaria" else []
    uses = ["raft-context"]
    if chunk.volatility < 0.5:
        uses.insert(0, "coneixement")
    return uses


def gap_uses(gap: Gap, doc: CuratedDoc) -> list[str]:
    """Open and partial article gaps can supply RAFT no-oracle candidates."""
    if doc.data.get("type") == "parla" or gap.decision != "incloure":
        return []
    return ["raft-sense-oracle"]
