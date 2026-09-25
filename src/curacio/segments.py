"""E1: segmentació tipada de documents Markdown."""

from __future__ import annotations

import re

from curacio.model import Block, Gap
from curacio.normalize import is_work_note, strip_work_sentences

HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$")
GAP_STATE = re.compile(r"(?:—|–|-|\*\*)\s*`?(parcial|font_externa|resolt|no-es-buit)\b", re.I)


def _is_catalan_quote(text: str) -> bool:
    """Conservative heuristic: Catalan function words keep the quote in prose."""
    words = set(re.findall(r"[\wÀ-ÿ']+", text.casefold()))
    return len(words & {"de", "la", "el", "i", "que", "en", "els", "per", "una", "del"}) >= 2


def _split_paragraphs(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"\n\s*\n", text.strip()) if part.strip()]


def _gap_items(raw: str) -> list[Gap]:
    lines = raw.splitlines()
    items: list[str] = []
    current: list[str] = []
    for line in lines:
        if re.match(r"^\s*(?:[-*+]|\d+[.)])\s+", line):
            if current:
                items.append("\n".join(current))
            current = [re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", line)]
        elif current and (line.startswith("  ") or line.strip()):
            current.append(line.strip())
    if current:
        items.append("\n".join(current))
    gaps: list[Gap] = []
    for item in items:
        state_match = GAP_STATE.search(item)
        state = state_match.group(1).lower() if state_match else "obert"
        struck = re.search(r"~~(.*?)~~", item, re.S)
        if state == "parcial" and state_match and struck:
            annotation = item[state_match.end() :]
            finding = annotation.split(":", maxsplit=1)[-1] if ":" in annotation else ""
            finding = finding.strip()
            if finding:
                finding = finding[0].upper() + finding[1:]
            text = f"{struck.group(1)} {finding}"
        elif struck:
            text = struck.group(1)
        else:
            text = item
        text = re.sub(
            r"\s*[—–-]\s*\*\*`?(?:parcial|font_externa|resolt|no-es-buit).*?$",
            "",
            text,
            flags=re.I | re.S,
        )
        text = re.sub(
            r"\s*cal consultar fonts, registres o observació que el corpus no conserva\.?$",
            "",
            text,
            flags=re.I,
        )
        text = re.sub(
            r"\s*\*\*`?(?:parcial|font_externa|resolt|no-es-buit).*?$", "", text, flags=re.I | re.S
        )
        text = re.sub(r"^\*\*|\*\*$", "", text.strip())
        if text:
            text = text[0].upper() + text[1:]
        if state == "no-es-buit" or state == "resolt":
            reason = (
                "ítem ratllat amb estat no-es-buit (placeholder)"
                if state == "no-es-buit"
                else "ítem ratllat amb estat resolt (la resposta ja és a la taula)"
            )
            decision = "excloure"
        else:
            if state == "font_externa":
                reason = "font_externa"
            elif state == "parcial":
                reason = "parcial: es conserva la troballa parcial"
            else:
                reason = f"buit {state}"
            decision = "incloure"
        gaps.append(Gap(state, text.strip(), "", reason, decision))
    return gaps


def segment_document(body: str) -> tuple[list[Block], list[Gap]]:
    """Returns ordered typed blocks and gap records, numbering blocks by appearance."""
    blocks: list[Block] = []
    gaps: list[Gap] = []
    section = "(inici)"
    prose: list[str] = []
    mode: str | None = None
    special: list[str] = []
    special_kind = ""
    audit_quote_active = False

    def add(kind: str, raw: str, reason: str = "") -> None:
        if not raw.strip():
            return
        is_preface = kind == "avis" and raw.lstrip().startswith("Tanda ")
        label = "(preàmbul)" if is_preface else section
        note = (
            "fitxa editorial de la tanda; la durada passa al frontmatter" if is_preface else reason
        )
        blocks.append(Block(f"#b{len(blocks) + 1}", kind, label, raw.strip(), reason=note))

    def flush_prose() -> None:
        nonlocal prose
        paragraphs = _split_paragraphs("\n".join(prose))
        retained: list[str] = []
        retained_reasons: list[str] = []
        deferred_notes: list[tuple[str, str]] = []

        def emit_retained() -> None:
            nonlocal retained, retained_reasons
            if not retained:
                return
            raw = "\n\n".join(retained)
            if re.match(r"Tanda\s+\d+\s+de parla", raw, flags=re.I):
                kind = "avis"
            elif raw.lstrip().startswith(">") and not _is_catalan_quote(raw):
                kind = "cita"
            else:
                kind = "cos"
            add(kind, raw, "; ".join(retained_reasons))
            retained = []
            retained_reasons = []

        for paragraph in paragraphs:
            is_note, note_reason = is_work_note(paragraph)
            cleaned, empty, sentence_reason = strip_work_sentences(paragraph)
            if is_note:
                if "enllaç a fonts/" in note_reason:
                    deferred_notes.append((paragraph, note_reason))
                else:
                    emit_retained()
                    add("nota-treball", paragraph, note_reason)
            elif empty:
                emit_retained()
                add("nota-treball", paragraph, sentence_reason)
            elif cleaned:
                retained.append(cleaned)
                removed_sentence = re.search(r"Tota la font[^.!?]*[.!?]", paragraph, flags=re.I)
                if removed_sentence:
                    retained_reasons.append(
                        f"cita en català; s'elimina la frase «{removed_sentence.group(0)}»"
                    )
        emit_retained()
        for note, reason in deferred_notes:
            add("nota-treball", note, reason)
        prose = []

    def flush_special() -> None:
        nonlocal special, mode
        if not special:
            mode = None
            return
        raw = "\n".join(special).strip()
        if special_kind == "related":
            add("related", raw, "navegació interna")
        elif special_kind == "buit":
            block = Block(f"#b{len(blocks) + 1}", "buit", section, raw)
            blocks.append(block)
            for gap in _gap_items(raw):
                gap.source_block_id = block.id
                gaps.append(gap)
        else:
            add(special_kind, raw)
        special = []
        mode = None

    lines = body.splitlines()
    in_fence = False
    for line in lines:
        heading = HEADING.match(line)
        if heading and not in_fence:
            flush_prose()
            flush_special()
            section = heading.group(1).strip()
            normalized_section = section.casefold()
            if normalized_section == "related":
                mode, special_kind = "special", "related"
                special = [line]
            elif normalized_section == "qui parla":
                mode, special_kind = "special", "taula-fitxa"
                special = [line]
            elif normalized_section in {"buits registrats", "el que falta", "buits"}:
                mode, special_kind = "special", "buit"
                special = [line]
            elif normalized_section == "avís":
                mode, special_kind = "special", "avis"
                special = [line]
            elif normalized_section == "consentiment":
                mode, special_kind = "special", "consentiment"
                special = [line]
            elif normalized_section == "la transcripció":
                mode, special_kind = "special", "transcripcio"
                special = [line]
            continue
        if line.strip().startswith("```"):
            if in_fence:
                special.append(line)
                in_fence = False
                flush_special()
            else:
                flush_prose()
                mode, special_kind, in_fence = "special", "transcripcio", True
                special = [line]
            continue
        if in_fence:
            special.append(line)
            continue
        if mode == "special" and special_kind == "taula":
            if line.startswith("|"):
                special.append(line)
                continue
            flush_special()
        if mode == "special" and special_kind == "buit" and line.lstrip().startswith(">"):
            quote = line.lstrip()[1:].strip()
            if quote.casefold().startswith("**auditat el"):
                special = []
                add("nota-treball", quote, "blockquote d'auditoria («Auditat el»)")
                audit_quote_active = True
                continue
            if audit_quote_active:
                blocks[-1].raw += "\n" + quote
                continue
        if mode == "special" and special_kind == "buit" and line.strip():
            audit_quote_active = False
        if mode == "special":
            if line.strip():
                special.append(line)
            continue
        if line.startswith("|"):
            flush_prose()
            mode, special_kind = (
                "special",
                "taula-fitxa" if section.casefold() == "qui parla" else "taula",
            )
            special = [line]
            continue
        if line.startswith(">"):
            if line[1:].lstrip().casefold().startswith("auditat el"):
                flush_prose()
                add("nota-treball", line, "blockquote d'auditoria")
                continue
            prose.append(line[1:].lstrip())
            continue
        if not line.strip():
            if prose and prose[-1] != "":
                prose.append("")
            continue
        prose.append(line)

    flush_prose()
    flush_special()
    sections_with_infobox = {
        block.section
        for block in blocks
        if block.kind == "taula" and block.raw.lstrip().startswith("| | |")
    }
    for target_section in sections_with_infobox:
        section_blocks = [block for block in blocks if block.section == target_section]
        if any(block.kind == "nota-treball" for block in section_blocks):
            continue
        if len(section_blocks) < 2:
            continue
        first_index = blocks.index(section_blocks[0])
        merged = Block(
            section_blocks[0].id,
            "cos",
            target_section,
            "\n\n".join(block.raw for block in section_blocks),
            reason="cos factual amb taula de fitxa",
        )
        blocks = [block for block in blocks if block.section != target_section]
        blocks.insert(min(first_index, len(blocks)), merged)
    block_ids: dict[str, str] = {}
    for index, block in enumerate(blocks, start=1):
        previous_id = block.id
        block.id = f"#b{index}"
        block_ids[previous_id] = block.id
    for gap in gaps:
        gap.source_block_id = block_ids.get(gap.source_block_id, gap.source_block_id)
    return blocks, gaps
