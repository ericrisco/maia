"""E4: combinació determinista de blocs en chunks amb límits documentats."""

from __future__ import annotations

import re

from curacio.model import Block, Chunk


def word_count(text: str) -> int:
    """Counts whitespace-delimited lexical tokens, including table cells."""
    return len(re.findall(r"\b[\wÀ-ÿ]+(?:['’][\wÀ-ÿ]+)*\b", text))


def make_chunks(blocks: list[Block], doc_id: str) -> list[Chunk]:
    """Merges eligible adjacent sections up to 300 words, hard-capping at 500."""
    eligible = [
        block
        for block in blocks
        if block.kind in {"cos", "taula", "cita"} and block.decision == "incloure" and block.text
    ]
    groups: list[list[Block]] = []
    current: list[Block] = []
    for block in eligible:
        if not current:
            current = [block]
            continue
        current_words = word_count("\n\n".join(item.text for item in current))
        block_words = word_count(block.text)
        section_changes = current[-1].section != block.section
        if section_changes and current_words >= 150 and current_words + block_words > 300:
            groups.append(current)
            current = [block]
            continue
        if current_words + block_words > 500:
            groups.append(current)
            current = [block]
            continue
        current.append(block)
    if current:
        groups.append(current)
    chunks: list[Chunk] = []
    for index, group in enumerate(groups, start=1):
        body = "\n\n".join(block.text for block in group).strip()
        volatility = max((block.volatility or 0.0 for block in group), default=0.0)
        if index == 1 and len(group) == 1:
            ref = group[0].id.removeprefix("#")
            reason = f"{ref} ({word_count(group[0].text)} paraules)"
        elif len(group) == 1 and index > 1:
            previous = chunks[-1]
            refs = "+".join(block.id.removeprefix("#") for block in group)
            previous_count = word_count(previous.text)
            reason = (
                f"{refs} ({word_count(body)} paraules); nou chunk perquè {previous.id.rsplit('#', maxsplit=1)[-1]} "
                f"({previous_count}) + {refs} passaria de 300; últim chunk del document, pot quedar sota 150"
            )
        elif volatility >= 0.5:
            refs = "+".join(block.id.removeprefix("#") for block in group)
            signal = next(
                block.id.removeprefix("#") for block in group if block.volatility == volatility
            )
            reason = (
                f"{refs}; volatilitat = màxim dels blocs ({volatility:.1f}, per {signal}) "
                "→ no entra a coneixement"
            )
        else:
            refs = "+".join(block.id.removeprefix("#") for block in group)
            counts = "+".join(str(word_count(block.text)) for block in group)
            reason = f"{refs} ({counts} = {word_count(body)} paraules)"
            if len(group) > 2:
                reason += "; volatilitat = màxim dels blocs"
        chunks.append(
            Chunk(
                id=f"{doc_id}#c{index}",
                section=" · ".join(dict.fromkeys(block.section for block in group)),
                blocks=group,
                text=body,
                volatility=volatility,
                reason=reason,
            )
        )
        chunk_words = word_count(body)
        if chunk_words > 500:
            chunks[-1].decision = "pendent"
            chunks[
                -1
            ].reason = (
                f"fragment indivisible de {chunk_words} paraules supera el màxim de 500; revisar"
            )
    return chunks
