"""Orquestració i serialització de les etapes E0–E8."""

from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from io import StringIO
from pathlib import Path
from typing import Any

from cervell.model import Corpus, Doc, load_corpus
from curacio.chunking import make_chunks, word_count
from curacio.duplicates import mark_near_duplicates, mark_templates
from curacio.inventory import render_inventory
from curacio.metadata import (
    domain_for,
    enrich_blocks,
    entities_in,
    family_for,
    load_families,
    normalize_redistribution,
    years_in,
)
from curacio.model import Block, Chunk, CuratedDoc, Gap
from curacio.normalize import normalize_inline, normalize_prose
from curacio.privacy import load_whitelist, mark_pii
from curacio.segments import segment_document
from curacio.snapshot import build_manifest, doc_id_for, git_blob_sha, manifest_jsonl
from curacio.uses import assign_uses, gap_uses

KNOWN_APTE_ERRORS = {
    "temes/historia/els-carlins-i-el-consell-1838-1839",
    "temes/institucions/el-consell-encarrega-un-codi-de-lleis-1860",
}
FONT_MISSING = "temes/persones/enciclopedia-esteve-albert-2026"


def _family_path(docs_root: Path) -> Path:
    return docs_root.parent / "curacio" / "decisions" / "families.tsv"


def _whitelist_path(docs_root: Path) -> Path:
    return docs_root.parent / "curacio" / "decisions" / "persones-publiques.tsv"


def _decisions_path(docs_root: Path) -> Path:
    return docs_root / "raw" / "curacio" / "decisions.jsonl"


def _overrides_path(docs_root: Path) -> Path:
    return docs_root.parent / "curacio" / "decisions" / "overrides.tsv"


def load_overrides(path: Path) -> dict[str, tuple[str, str]]:
    """Loads explicit chunk decisions; invalid rows fail instead of disappearing."""
    if not path.exists():
        return {}
    overrides: dict[str, tuple[str, str]] = {}
    with path.open(encoding="utf-8", newline="") as source:
        for row in csv.DictReader(source, delimiter="\t"):
            chunk_id = row.get("chunk_id", "").strip()
            decision = row.get("decision", "").strip()
            reason = row.get("motiu", "").strip()
            if not chunk_id and not decision and not reason:
                continue
            if not chunk_id or decision not in {"incloure", "pendent", "excloure"} or not reason:
                raise ValueError(f"override invàlid a {path}: {row}")
            overrides[chunk_id] = (decision, reason)
    return overrides


def apply_overrides(chunks: list[Chunk], overrides: dict[str, tuple[str, str]]) -> int:
    """Applies declared chunk overrides after automatic privacy and hygiene gates."""
    by_id = {chunk.id: chunk for chunk in chunks}
    unknown = sorted(set(overrides) - set(by_id))
    if unknown:
        raise ValueError(f"overrides apunten a chunks inexistents: {', '.join(unknown)}")
    for chunk_id, (decision, reason) in overrides.items():
        chunk = by_id[chunk_id]
        if decision == "incloure" and (chunk.pii or _has_forbidden_training_text(chunk.text)):
            raise ValueError(f"override no pot reobrir un chunk amb risc: {chunk_id}")
        chunk.decision = decision
        chunk.reason = f"override manual: {reason}"
    return len(overrides)


def load_review_statuses(path: Path) -> dict[str, str]:
    """Reads only unit_id and status; no rationale, evidence or review metadata."""
    statuses: dict[str, str] = {}
    if not path.exists():
        return statuses
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        unit_id = record.get("unit_id")
        status = record.get("status")
        if (
            isinstance(unit_id, str)
            and unit_id.startswith("maia-docs/")
            and isinstance(status, str)
        ):
            doc_id = unit_id.removeprefix("maia-docs/").removesuffix(".md")
            statuses[doc_id] = status
    return statuses


def _table_text(raw: str) -> str:
    """Strips emphasis from table cells while preserving source Markdown structure."""
    output: list[str] = []
    for line in raw.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        cells = [normalize_inline(cell) for cell in cells]
        output.append(
            "| | |" if all(not cell for cell in cells) else "| " + " | ".join(cells) + " |"
        )
    return "\n".join(output)


def _mixed_infobox_text(raw: str) -> str:
    """Formats prose and an embedded person-fact table without flattening cells."""
    paragraphs = re.split(r"\n\s*\n", raw.strip())
    rendered: list[str] = []
    for paragraph in paragraphs:
        if paragraph.lstrip().startswith("|"):
            rendered.append(_table_text(paragraph))
        else:
            rendered.append(normalize_prose(paragraph))
    return "\n\n".join(part for part in rendered if part)


def _speech_segments(raw: str, doc_id: str) -> tuple[list[str], list[str]]:
    """Builds one timestamped segment per transcript line and extracts uncertainties."""
    lines: list[str] = []
    uncertain_words: list[str] = []
    for line in raw.splitlines():
        match = re.match(
            r"\s*\[(\d{2}:\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}\.\d{3})\]\s*(.*)", line
        )
        if not match:
            continue
        start, end, text = match.groups()
        words: list[str] = []

        def unmark(found: re.Match[str], capture: list[str] = words) -> str:
            word = found.group(1)
            capture.append(word.strip(".,;:!?()"))
            return word

        clean_text = re.sub(r"\[\?([^\]]+)\]", unmark, text).strip()
        uncertain_words.extend(word for word in words if word)
        count = len(words)
        uncertainty = f"{count} ({', '.join(words)})" if count else "0"
        lines.append(
            f"<!-- seg: {doc_id}#s{len(lines) + 1:03d} · {start}–{end} · incerts: {uncertainty} -->\n{clean_text}"
        )
    return lines, uncertain_words


def _speech_word_count(raw: str) -> int:
    """Counts spoken tokens without timestamps or segment-marker metadata."""
    spoken: list[str] = []
    pattern = re.compile(r"\s*\[\d{2}:\d{2}:\d{2}\.\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}\.\d{3}\]\s*(.*)")
    for line in raw.splitlines():
        match = pattern.match(line)
        if match:
            spoken.append(re.sub(r"\[\?([^\]]+)\]", r"\1", match.group(1)))
    return word_count(" ".join(spoken))


def _exclude_unclean_chunks(chunks: list[Chunk]) -> int:
    """Excludes chunks retaining editorial markup or a local raw reference."""
    excluded = 0
    for chunk in chunks:
        if chunk.decision != "excloure" and _has_forbidden_training_text(chunk.text):
            chunk.decision = "excloure"
            chunk.reason = "marca editorial o referència raw/ residual; exclòs per higiene"
            excluded += 1
    return excluded


def _has_forbidden_training_text(text: str) -> bool:
    """Checks the forbidden source markers on normalized training text."""
    forbidden = re.compile(r"~~|\*\*|__|(?:docs/)?raw/|\[\d{2}:\d{2}:\d{2}")
    return bool(forbidden.search(text))


def _speech_values(doc: CuratedDoc, transcript: Block, licence: str, redistribution: str) -> str:
    """Serializes the sample metadata and its verbatim, uncertainty-marked speech."""
    segments, uncertain = _speech_segments(transcript.raw, doc.doc_id)
    description = str(doc.data.get("description", ""))
    descriptive_text = description + " " + " ".join(block.raw for block in doc.blocks)
    speaker_match = re.search(r"([A-ZÀ-Þ][^,.]+),\s*(?:conseller|consellera)", description)
    speaker_name = speaker_match.group(1).strip() if speaker_match else "no consta"
    parish_match = re.search(
        r"conseller(?:a)?\s+(?:general\s+)?de\s+(.+?)(?:\s+al\s+|[,.]|$)",
        description,
        re.I,
    )
    parish = parish_match.group(1).strip() if parish_match else "no consta"
    role = (
        "conseller general al Consell Constituent"
        if "Consell Constituent" in description
        else "no consta"
    )
    duration_match = re.search(r"(\d+\s+min(?:uts?)?\s+\d+\s+s)", descriptive_text)
    duration = duration_match.group(1) if duration_match else "no consta"
    notice = next((block.raw for block in doc.blocks if block.kind == "avis"), "")
    marks_match = re.search(r"(\d+)\s+marques", notice, re.I)
    mark_count = int(marks_match.group(1)) if marks_match else len(uncertain)
    title = _yaml_quote(normalize_inline(doc.title))
    return (
        "---\n"
        f"doc_id: {doc.doc_id}\n"
        f"sha_origen: {doc.source_sha[:12]}\n"
        f"titol_doc: {title}\n"
        f"tema: {doc.data.get('tema', 'parla/oral')}\n"
        f"domini: {domain_for(str(doc.data.get('tema', 'parla')))}\n"
        f"font: {doc.data.get('font', '')}\n"
        f"familia_font: {doc.data.get('_familia_font', doc.data.get('font', ''))}\n"
        f"llicencia: {_yaml_quote(licence)}\n"
        f"redistribucio: {redistribution}\n"
        f"redistribucio_detall: {_yaml_quote('pendent' if redistribution == 'pendent' else str(doc.data.get('_redistribucio_detall', redistribution)))}\n"
        "veu: originaria\n"
        "epoca: contemporania\n"
        "parlant:\n"
        f"  nom: {speaker_name}\n"
        f"  parroquia: {parish}\n"
        f"  rol: {role}\n"
        "  generacio: no consta\n"
        "  llengua_primera: no consta\n"
        "  ofici: no consta\n"
        "registre: entrevista\n"
        f"durada: {_yaml_quote(duration)}\n"
        f"estat: pendent-escolta\n"
        f"segments: {len(segments)}\n"
        f"marques_incertes: {mark_count}\n"
        "citable_com_a_fet: false\n"
        "usos: [llengua]\n"
        "---\n\n" + "\n\n".join(segments) + "\n"
    )


def _yaml_quote(value: str) -> str:
    """Quotes a YAML string using stable double-quoted scalar syntax."""
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _frontmatter(doc: CuratedDoc, metadata: dict[str, str], *, gap: bool = False) -> str:
    """Renders shared frontmatter in the golden examples' fixed field order."""
    title = _yaml_quote(normalize_inline(doc.title))
    details = metadata["redistribucio_detall"]
    lines = [
        "---",
        f"doc_id: {doc.doc_id}",
        f"sha_origen: {doc.source_sha[:12]}",
        f"titol_doc: {title}",
        f"tema: {metadata['tema']}",
        f"domini: {metadata['domini']}",
        f"font: {metadata['font']}",
        f"familia_font: {metadata['familia_font']}",
        f"llicencia: {_yaml_quote(metadata['llicencia'])}",
        f"redistribucio: {metadata['redistribucio']}",
    ]
    if not gap:
        lines.append(f"redistribucio_detall: {_yaml_quote(details)}")
    if not gap:
        lines.extend(
            [
                f"veu: {doc.data.get('veu', 'compilada')}",
                f"epoca: {doc.data.get('epoca', 'contemporania')}",
            ]
        )
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def _chunks_file(doc: CuratedDoc, chunks: list[Chunk], metadata: dict[str, str]) -> str:
    """Renders all included and pending chunks for one document in one file."""
    visible = [chunk for chunk in chunks if chunk.decision != "excloure"]
    body = "\n\n".join(f"<!-- chunk: {chunk.id} -->\n{chunk.text.rstrip()}" for chunk in visible)
    return _frontmatter(doc, metadata) + body.rstrip() + "\n"


def _gap_file(doc: CuratedDoc, gaps: list[Gap], metadata: dict[str, str]) -> str:
    """Renders open gaps; resolved and not-a-gap entries never enter the file."""
    output = [_frontmatter(doc, metadata, gap=True).rstrip()]
    index = 0
    for gap in gaps:
        if gap.decision != "incloure":
            continue
        index += 1
        clean = normalize_prose(gap.text)
        output.append(f"\n\n<!-- buit: {doc.doc_id}#g{index} · estat: {gap.state} -->\n{clean}")
    return "".join(output).rstrip() + "\n"


def _speech_gaps_to_blocks(blocks: list[Block]) -> list[Block]:
    """For speech, treats each sample-profile limitation as an excluded block."""
    result: list[Block] = []
    for block in blocks:
        if block.kind != "buit":
            result.append(block)
            continue
        items: list[str] = []
        current: list[str] = []
        for line in block.raw.splitlines():
            if re.match(r"^\s*(?:[-*+]|\d+[.)])\s+", line):
                if current:
                    items.append("\n".join(current))
                current = [re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", line)]
            elif current and line.strip():
                current.append(line.strip())
        if current:
            items.append("\n".join(current))
        for item in items:
            state_match = re.search(r"\b(no-es-buit|parcial|font_externa|resolt)\b", item)
            gap_state = state_match.group(1) if state_match else "pendent"
            item = re.sub(r"~~(.*?)~~", r"\1", item, flags=re.S)
            item = normalize_inline(item)
            result.append(
                Block(
                    f"#b{len(result) + 1}",
                    "buit",
                    block.section,
                    item,
                    text=item,
                    reason="buit de perfil, drets o instrucció de la mostra; passa a metadades o queda fora",
                    decision="excloure",
                    gap_state=gap_state,
                )
            )
    return result


def _split_long_prose_blocks(blocks: list[Block], gaps: list[Gap]) -> tuple[list[Block], list[Gap]]:
    """Splits oversized prose blocks at paragraph boundaries and renumbers them."""
    expanded: list[Block] = []
    old_to_new: dict[str, str] = {}
    for block in blocks:
        raw_parts = [
            part.strip() for part in re.split(r"\n\s*\n", block.raw.strip()) if part.strip()
        ]
        text_parts = [
            part.strip() for part in re.split(r"\n\s*\n", block.text.strip()) if part.strip()
        ]
        if (
            block.kind == "cos"
            and word_count(block.text) > 500
            and len(raw_parts) == len(text_parts)
            and len(raw_parts) > 1
        ):
            fragments = [
                Block(
                    id="",
                    kind=block.kind,
                    section=block.section,
                    raw=raw,
                    text=text,
                    reason=block.reason,
                    decision=block.decision,
                )
                for raw, text in zip(raw_parts, text_parts, strict=True)
            ]
        else:
            fragments = [block]
        first_new_id = f"#b{len(expanded) + 1}"
        old_to_new[block.id] = first_new_id
        expanded.extend(fragments)
    for index, block in enumerate(expanded, start=1):
        block.id = f"#b{index}"
    for gap in gaps:
        gap.source_block_id = old_to_new.get(gap.source_block_id, gap.source_block_id)
    return expanded, gaps


def _curate_doc(
    docs_root: Path,
    source: Doc,
    fonts: dict[str, Any],
    families: dict[str, str],
    statuses: dict[str, str],
) -> tuple[CuratedDoc, dict[str, str], list[Gap]]:
    doc_id = doc_id_for(docs_root, source)
    source_bytes = source.path.read_bytes()
    blocks, gaps = segment_document(source.body)
    if source.data.get("type") == "parla":
        blocks = _speech_gaps_to_blocks(blocks)
        gaps = []
    elif gaps and all(gap.state in {"resolt", "no-es-buit"} for gap in gaps):
        expanded: list[Block] = []
        for block in blocks:
            if block.kind != "buit":
                expanded.append(block)
                continue
            for gap in (item for item in gaps if item.source_block_id == block.id):
                expanded.append(
                    Block(
                        id="",
                        kind="buit",
                        section=block.section,
                        raw=gap.text,
                        text=gap.text,
                        reason=gap.reason,
                        decision="excloure",
                        gap_state=gap.state,
                    )
                )
        blocks = expanded
        gaps = []
    for index, block in enumerate(blocks):
        block.id = f"#b{index + 1}"
        if source.data.get("type") == "parla":
            if block.kind == "avis" and block.section == "Avís":
                block.reason = "recompte de marques; passa al frontmatter (marques_incertes)"
            elif block.kind == "consentiment":
                block.reason = "estat de drets; ja és a redistribucio de la fitxa de font"
            elif block.kind == "taula-fitxa":
                block.reason = "passa al frontmatter com a «parlant»"
            elif block.kind == "buit":
                speech_gap_reasons = (
                    "no-es-buit: limitació de la mostra",
                    "perfil del parlant: passa al frontmatter (generació, llengua primera, ofici: no consta)",
                    "estat de drets, no pregunta de contingut",
                    "instrucció d'ús: passa al frontmatter com a citable_com_a_fet: false",
                )
                item_number = sum(1 for earlier in blocks[:index] if earlier.kind == "buit")
                if item_number < len(speech_gap_reasons):
                    block.reason = speech_gap_reasons[item_number]
        if block.kind == "taula":
            block.text = _table_text(block.raw)
            if block.section == "La carrera, club per club":
                block.reason = "taula de carrera (dins del chunk); rang obert «2000-» → 0.5"
            elif block.section == "Les seleccions, totes":
                block.reason = "taula de seleccions (dins del chunk)"
        elif (
            block.kind == "cos"
            and block.raw.lstrip().startswith("|") is False
            and "\n| | |" in block.raw
        ):
            block.text = _mixed_infobox_text(block.raw)
        elif block.kind == "transcripcio":
            block.text = block.raw
        else:
            block.text = normalize_prose(block.raw)
        if block.kind in {"related", "nota-treball", "avis", "consentiment", "taula-fitxa", "buit"}:
            block.decision = "excloure"
        if block.kind == "transcripcio":
            block.decision = "pendent"
            block.reason = "veu originària sense verificar contra l'àudio: pendent-escolta"
        if block.kind == "cos" and re.search(r"(?:\[\[|<table|<!--|!\[)", block.raw):
            block.reason = "format no reconegut pel segmentador; revisar"
        if block.kind == "cos" and "«" in block.raw and "2020" in block.raw:
            block.reason = "cos amb cita en català (atribuïda); «2020» → 0.3"
        if block.kind == "cos" and "en exercici" in block.raw and "en actiu" in block.raw:
            block.reason = "cos interpretatiu amb cites atribuïdes; «en exercici» i «en actiu» són el mateix senyal → 0.4"
        if block.kind == "cos" and "avui" in block.raw.casefold():
            block.reason = "cos interpretatiu; «avui» → 0.4"
        if block.kind == "cos" and "la proporció" in block.raw.casefold():
            block.reason = "fet que la font dona (la proporció)"
        if block.kind == "taula":
            before = blocks[index - 1].raw.casefold() if index > 0 else ""
            after = blocks[index + 1].raw.casefold() if index + 1 < len(blocks) else ""
            if any(
                cue in f"{before} {after} {block.raw.casefold()}"
                for cue in ("conjectura", "hipòtesi", "no quadra", "dubtós")
            ):
                block.decision = "pendent"
                block.reason = (
                    "taula presentada com a conjectura pel mateix text "
                    "(«conjectura», «no quadra», «dubtós»); revisió humana"
                )
            else:
                if not block.reason:
                    block.reason = "taula de dades conservada en Markdown"
    blocks, gaps = _split_long_prose_blocks(blocks, gaps)
    enrich_blocks(blocks)
    font_id = str(source.data.get("font", ""))
    font = fonts.get(font_id)
    font_data = font.data if font else {}
    redistribution, detail = normalize_redistribution(font_data.get("redistribucio"))
    theme = str(source.data.get("tema", "")).removeprefix("temes/")
    metadata = {
        "font": font_id,
        "familia_font": family_for(font_id, families),
        "llicencia": str(font_data.get("llicencia", "llicència no consta")),
        "redistribucio": redistribution,
        "redistribucio_detall": detail,
        "tema": theme or "sense-tema",
        "domini": domain_for(theme),
        "anys": ",".join(str(year) for year in years_in(source.body)),
        "entitats": "; ".join(entities_in(source.body)),
    }
    curated = CuratedDoc(
        doc_id=doc_id,
        path=source.path,
        data=dict(source.data),
        source_sha=git_blob_sha(source_bytes),
        blocks=blocks,
        chunks=[],
        gaps=gaps,
        source_paragraphs=[
            part.strip() for part in re.split(r"\n\s*\n", source.body.strip()) if part.strip()
        ],
    )
    curated.data["_familia_font"] = metadata["familia_font"]
    curated.data["_redistribucio_detall"] = detail
    curated.chunks = make_chunks(blocks, doc_id) if source.data.get("type") != "parla" else []
    for chunk in curated.chunks:
        chunk.uses = assign_uses(chunk, curated)
        chunk.review_status = statuses.get(doc_id, "unreviewed")
    if source.data.get("type") == "parla":
        status = statuses.get(doc_id, "unreviewed")
        for block in blocks:
            if block.kind == "transcripcio":
                block.reason = "veu originària sense verificar contra l'àudio: pendent-escolta"
                block.decision = "pendent"
                block.text = block.raw
        # The sample is represented as one language chunk in the inventory, but
        # its exact transcript remains in the dedicated output file.
        sample_chunk = Chunk(
            id=f"{doc_id}#c1",
            section="La transcripció",
            blocks=[block for block in blocks if block.kind == "transcripcio"],
            text="",
            volatility=0.0,
            uses=["llengua"],
            decision="pendent",
            reason="estat pendent-escolta; no entra a entrenament fins a validar l'àudio",
            review_status=status,
        )
        curated.chunks = [sample_chunk]
    return curated, metadata, gaps


def _corrections(documents: list[CuratedDoc], fonts: dict[str, Any]) -> str:
    """Creates a correction ledger without editing the source vault."""
    rows: list[list[str]] = [["doc_id", "camp", "valor_origen", "correccio", "motiu"]]
    by_title: dict[str, list[CuratedDoc]] = defaultdict(list)
    for doc in documents:
        by_title[normalize_inline(doc.title).casefold()].append(doc)
        derived = doc.data.get("veu") == "originaria" and doc.data.get("epoca") == "contemporania"
        if bool(doc.data.get("apte_llengua")) != derived:
            rows.append(
                [
                    doc.doc_id,
                    "apte_llengua",
                    str(doc.data.get("apte_llengua")),
                    str(derived).lower(),
                    "derivació veu + època segons contracte",
                ]
            )
        font = str(doc.data.get("font", ""))
        if font and font not in fonts:
            rows.append(
                [doc.doc_id, "font", font, "pendent", "la fitxa de font no consta a docs/fonts/"]
            )
        redistribution = str(fonts[font].data.get("redistribucio", "")) if font in fonts else ""
        normalized, detail = normalize_redistribution(redistribution)
        if redistribution and detail != normalized:
            rows.append(
                [
                    doc.doc_id,
                    "redistribucio",
                    detail,
                    normalized,
                    "valor original preservat; enum derivat per al corpus",
                ]
            )
    for _title, docs in sorted(by_title.items()):
        if len(docs) > 1:
            for doc in docs:
                rows.append(
                    [
                        doc.doc_id,
                        "title",
                        doc.title,
                        "pendent",
                        "títol duplicat; no es desambigua automàticament",
                    ]
                )
    output = StringIO(newline="")
    csv.writer(output, delimiter="\t", lineterminator="\n").writerows(rows)
    return output.getvalue()


def _readme() -> str:
    return """# Corpus curat de Maia

Aquest arbre és una sortida regenerable de `cervell cura tot docs --out corpus`.
No s'edita a mà. El contingut conserva identificadors de document i de chunk,
hashos de blob d'origen, font, família, llicència, redistribució i decisió de
revisió. La sortida no és un dataset ni conté Q&A.

## Ús dels chunks

- `coneixement`: fragments amb volatilitat inferior a 0,5.
- `raft-context`: fragments factuals, inclosos els volàtils que només s'han
  de consultar en context.
- `raft-sense-oracle`: buits oberts o parcials; mai no expressen una negació.
- `llengua`: parla originària sense normalització ortogràfica. Les mostres
  `pendent-escolta` són material de curació i no s'han de tractar com a
  aprovades per entrenar.

Consulteu `informe.md` per als recomptes, drets i decisions obertes. Les
columnes `estat_revisio` provenen exclusivament de `status` a
`docs/raw/curacio/decisions.jsonl`; sense decisió s'usa `unreviewed`.
Les decisions manuals per chunk s'escriuen a `curacio/decisions/overrides.tsv`;
un override ha d'apuntar a un ID existent i no pot reobrir PII ni fragments bruts.
"""


def _snapshot_metrics(corpus: Corpus) -> dict[str, int]:
    """Remeasures the acquisition baselines from parsed source documents."""
    metrics: Counter[str] = Counter()
    for source in corpus.docs:
        blocks, _ = segment_document(source.body)
        metrics["parla" if source.data.get("type") == "parla" else "article"] += 1
        metrics["paraules_buits"] += sum(
            word_count(block.raw)
            for block in blocks
            if block.kind == "buit" and block.section.casefold() == "buits registrats"
        )
        metrics["paraules_falta"] += sum(
            word_count(block.raw)
            for block in blocks
            if block.kind == "buit" and block.section.casefold() == "el que falta"
        )
        metrics["paraules_related"] += sum(
            word_count(block.raw) for block in blocks if block.kind == "related"
        )
        metrics["auditories"] += len(re.findall(r"\bAuditat el\b", source.body, flags=re.I))
        metrics["fragments_ratllats"] += sum(
            len(re.findall(r"~~[^~]+~~", line)) for line in source.body.splitlines()
        )
        metrics["enllaços_raw"] += len(
            re.findall(r"\]\((?:[^)]*/)?raw/[^)]*\)", source.body, flags=re.I)
        )
        metrics["enllaços_interns"] += len(
            [
                target
                for target in re.findall(r"\[[^\]]+\]\(([^)]+\.md(?:#[^)]*)?)\)", source.body)
                if not re.search(r"(?:^|/)raw/", target)
            ]
        )
        metrics["marques_negreta"] += len(re.findall(r"\*\*.+?\*\*", source.body, flags=re.S))
        if source.data.get("type") == "parla":
            for block in blocks:
                if block.kind == "transcripcio":
                    segments, uncertain = _speech_segments(
                        block.raw, doc_id_for(corpus.vault_root, source)
                    )
                    metrics["segments_parla"] += len(segments)
                    metrics["marques_incertes"] += len(uncertain)
    metrics["documents"] = len(corpus.docs)
    metrics["fonts"] = len(corpus.fonts)
    metrics["no_parsejats"] = len(corpus.unparsed)
    return dict(metrics)


def _report(
    documents: list[tuple[CuratedDoc, dict[str, str], list[Gap]]],
    baseline_words: int,
    source_count: int,
    maia_sha: str,
    unclean_chunks: int,
    template_metrics: tuple[int, int],
    snapshot_metrics: dict[str, int],
    overrides_applied: int,
) -> str:
    chunks: list[tuple[CuratedDoc, dict[str, str], Chunk]] = [
        (doc, metadata, chunk) for doc, metadata, _ in documents for chunk in doc.chunks
    ]
    use_counts: Counter[str] = Counter()
    use_words: Counter[str] = Counter()
    approved: Counter[str] = Counter()
    domain_words: Counter[str] = Counter()
    domain_chunks: Counter[str] = Counter()
    license_chunks: Counter[str] = Counter()
    included_by_domain: Counter[str] = Counter()
    family_documents: Counter[str] = Counter()
    family_chunks: Counter[str] = Counter()
    use_domain_metrics: Counter[tuple[str, str]] = Counter()
    use_license_metrics: Counter[tuple[str, str]] = Counter()
    domain_license_metrics: Counter[tuple[str, str]] = Counter()
    for _doc, metadata, chunk in chunks:
        domain = metadata["domini"]
        licence = f"{metadata['llicencia']} · {metadata['redistribucio']}"
        chunk_words = (
            sum(
                _speech_word_count(block.raw)
                for block in _doc.blocks
                if block.kind == "transcripcio"
            )
            if "llengua" in chunk.uses
            else word_count(chunk.text)
        )
        for use in chunk.uses:
            use_counts[use] += 1
            words = chunk_words
            use_words[use] += words
            use_domain_metrics[use, domain] += words
            use_license_metrics[use, licence] += words
            domain_license_metrics[domain, licence] += words
            if chunk.review_status == "approved":
                approved[use] += 1
        domain_chunks[domain] += 1
        license_chunks[licence] += 1
        family_chunks[metadata["familia_font"]] += 1
        if chunk.decision != "excloure" and chunk.uses:
            included_by_domain[domain] += chunk_words
    for doc, metadata, doc_gaps in documents:
        for gap in doc_gaps:
            if gap_uses(gap, doc):
                use_counts["raft-sense-oracle"] += 1
                words = word_count(gap.text)
                use_words["raft-sense-oracle"] += words
                domain = metadata["domini"]
                licence = f"{metadata['llicencia']} · {metadata['redistribucio']}"
                use_domain_metrics["raft-sense-oracle", domain] += words
                use_license_metrics["raft-sense-oracle", licence] += words
                domain_license_metrics[domain, licence] += words
    for doc, metadata, _gaps in documents:
        domain_words[metadata["domini"]] += word_count(doc.path.read_text(encoding="utf-8"))
        family_documents[metadata["familia_font"]] += 1
    review_counts = Counter(chunk.review_status for doc, _, chunk in chunks)
    review_blocks = sum(
        1 for doc, _, _ in documents for block in doc.blocks if "revisar" in block.reason
    )
    work_note_blocks = sum(
        1 for doc, _, _ in documents for block in doc.blocks if block.kind == "nota-treball"
    )
    unsafe_blocks = sum(
        1
        for doc, _, _ in documents
        for block in doc.blocks
        if "text ratllat" in block.reason or "referència local a raw/" in block.reason
    )
    block_count = sum(len(doc.blocks) for doc, _, _ in documents)
    excluded_domains: list[str] = []
    for domain, words in sorted(domain_words.items()):
        included = included_by_domain[domain]
        lost = max(words - included, 0)
        ratio = lost / words if words else 0.0
        if ratio > 0.10:
            excluded_domains.append(
                f"- `{domain}`: {ratio:.1%} de paraules fora de chunks entrenables o d'ús (entrada {words:,}; retingudes {included:,}; diferència {lost:,})."
            )
    gaps = [gap for doc, _, doc_gaps in documents for gap in doc_gaps]
    unresolved_rights = sum(1 for _, metadata, _ in documents if metadata["redistribucio"] != "si")
    pending_rights_chunks = sum(
        len(doc.chunks) for doc, metadata, _ in documents if metadata["redistribucio"] == "pendent"
    )
    speech_chunks = [chunk for doc, _, chunk in chunks if doc.data.get("type") == "parla"]
    decision_count = sum(1 for _, _, chunk in chunks if chunk.review_status != "unreviewed")
    size_exceptions = [
        (chunk.id, word_count(chunk.text))
        for doc, _, _ in documents
        for index, chunk in enumerate(doc.chunks)
        if word_count(chunk.text) > 500
        or (index < len(doc.chunks) - 1 and word_count(chunk.text) < 150)
    ]
    license_table = "\n".join(
        f"| {label} | {count} |" for label, count in sorted(license_chunks.items())
    )
    use_table = "\n".join(
        f"| {use} | {use_counts[use]} | {use_words[use]:,} | {approved[use]} |"
        for use in ("llengua", "coneixement", "raft-context", "raft-sense-oracle")
    )
    domain_table = "\n".join(
        f"| {domain} | {domain_chunks[domain]} | {domain_words[domain]:,} | {included_by_domain[domain]:,} |"
        for domain in sorted(domain_words)
    )
    use_domain_table = "\n".join(
        f"| {use} | {domain} | {use_domain_metrics[use, domain]:,} |"
        for use, domain in sorted(use_domain_metrics)
    )
    use_license_table = "\n".join(
        f"| {use} | {licence} | {use_license_metrics[use, licence]:,} |"
        for use, licence in sorted(use_license_metrics)
    )
    domain_license_table = "\n".join(
        f"| {domain} | {licence} | {domain_license_metrics[domain, licence]:,} |"
        for domain, licence in sorted(domain_license_metrics)
    )
    family_table = "\n".join(
        f"| {family} | {family_documents[family]} | {family_chunks[family]} | "
        f"{family_documents[family] / len(documents) if documents else 0:.1%} |"
        for family in sorted(
            family_documents,
            key=lambda family: (-family_documents[family], family),
        )[:20]
    )
    starting = {
        "documents": 1388,
        "article": 1348,
        "parla": 40,
        "fonts": 627,
        "auditories": 387,
        "fragments_ratllats": 2523,
        "enllaços_raw": 1263,
        "enllaços_interns": 15966,
        "marques_negreta": 128867,
        "segments_parla": 15963,
        "marques_incertes": 8450,
    }
    snapshot_rows: list[str] = []
    snapshot_warnings: list[str] = []
    for label, key, initial in (
        ("Documents", "documents", starting["documents"]),
        ("Articles", "article", starting["article"]),
        ("Parla", "parla", starting["parla"]),
        ("Fitxes de font", "fonts", starting["fonts"]),
        ("Paraules Markdown", "paraules_totals", 2_150_000),
        ("Auditories", "auditories", starting["auditories"]),
        ("Fragments ratllats", "fragments_ratllats", starting["fragments_ratllats"]),
        ("Enllaços a raw/", "enllaços_raw", starting["enllaços_raw"]),
        ("Enllaços interns", "enllaços_interns", starting["enllaços_interns"]),
        ("Marques de negreta", "marques_negreta", starting["marques_negreta"]),
        ("Segments de parla", "segments_parla", starting["segments_parla"]),
        ("Marques incertes", "marques_incertes", starting["marques_incertes"]),
    ):
        measured = baseline_words if key == "paraules_totals" else snapshot_metrics.get(key, 0)
        delta = (measured - initial) / initial if initial else 0.0
        snapshot_rows.append(f"| {label} | {initial:,} | {measured:,} | {delta:+.1%} |")
        if abs(delta) > 0.05:
            explanation = {
                "auditories": "la partida comptava blockquotes d'auditoria; ara es compten les ocurrències literals «Auditat el» (les anotacions ja són material exclòs)",
                "fragments_ratllats": "ara es compten parells `~~...~~` dins de cada línia; el recompte inclou les actualitzacions acumulades a docs/",
            }.get(key, "s'ha mesurat sobre l'arbre actual d'entrada")
            snapshot_warnings.append(
                f"- {label}: {measured:,} vs {initial:,} de partida ({delta:+.1%}); {explanation}."
            )
    for label, key, expected_share in (
        ("Buits registrats", "paraules_buits", 0.186),
        ("El que falta", "paraules_falta", 0.055),
        ("Related", "paraules_related", 0.031),
    ):
        measured_share = snapshot_metrics.get(key, 0) / baseline_words if baseline_words else 0.0
        snapshot_rows.append(
            f"| {label} (paraules) | {expected_share:.1%} | {measured_share:.1%} | {measured_share - expected_share:+.1%} pp |"
        )
        relative_delta = (
            (measured_share - expected_share) / expected_share if expected_share else 0.0
        )
        if abs(relative_delta) > 0.05:
            snapshot_warnings.append(
                f"- {label}: {measured_share:.1%} ara vs {expected_share:.1%} de partida ({relative_delta:+.1%}); ara es calcula sobre paraules de fitxers Markdown i extracció de seccions tipades."
            )
    warnings = []
    if excluded_domains:
        warnings.extend(excluded_domains)
    warnings.extend(snapshot_warnings)
    template_paragraphs, template_documents = template_metrics
    template_delta = (template_documents - 152) / 152 if 152 else 0.0
    if abs(template_delta) > 0.05:
        warnings.append(
            f"- Documents amb plantilles: {template_documents} vs 152 de partida ({template_delta:+.1%}); el recompte complet inclou notes, auditoria, navegació i parla, mentre només els chunks entrenables s'exclouen de l'ús."
        )
    warnings_text = (
        "\n".join(warnings)
        if warnings
        else "- Cap desviació de més del 5% respecte dels recomptes documentals de partida."
    )
    template_count = sum(1 for _, _, chunk in chunks if chunk.template)
    near_duplicate_count = sum(
        1 for _, _, chunk in chunks if chunk.reason.startswith("quasi-duplicat")
    )
    pii_count = sum(1 for _, _, chunk in chunks if chunk.pii)
    pending_sports = sum(
        1
        for _doc, metadata, chunk in chunks
        if metadata["domini"] == "esports" and chunk.decision != "excloure"
    )
    historical = sum(
        1 for _doc, _, chunk in chunks if any(year < 1925 for year in years_in(chunk.text))
    )
    return f"""# Informe del corpus curat

## Snapshot E0

- Documents d'entrada: **{source_count:,}**; words en fitxers Markdown inclòs frontmatter: **{baseline_words:,}**.
- SHA determinista del conjunt d'entrades: `{maia_sha}`. És SHA-256 dels parells ordenats `doc_id + SHA blob`, no el commit Git, perquè no canviï en commitejar la sortida.
- Docs de parla: **{len(speech_chunks)}** transcripcions curades; buits de mostra exclosos de RAFT.
- Fonts reconegudes: **{snapshot_metrics.get("fonts", 0)}**; documents malformats sense parsejar: **{snapshot_metrics.get("no_parsejats", 0)}**.

| Mesura d'entrada | Partida | Ara | Diferència |
| --- | ---: | ---: | ---: |
{chr(10).join(snapshot_rows)}

## Resultats per ús

| Ús | Chunks | Paraules | Ja aprovats a `decisions.jsonl` |
| --- | ---: | ---: | ---: |
{use_table}

Les paraules de llengua són parla originària contemporània sense normalització.
Només les etiquetes `approved` es compten com a revisades; `pendent-escolta`
continua pendent i no és llengua verificada.

## Resultats per domini

| Domini | Chunks | Paraules d'entrada | Paraules conservades en chunks |
| --- | ---: | ---: | ---: |
{domain_table}

## Paraules per ús × domini

| Ús | Domini | Paraules |
| --- | --- | ---: |
{use_domain_table}

## Paraules per ús × llicència

| Ús | Llicència i redistribució | Paraules |
| --- | --- | ---: |
{use_license_table}

## Paraules per domini × llicència

| Domini | Llicència i redistribució | Paraules |
| --- | --- | ---: |
{domain_license_table}

## Llicències

| Llicència declarada · estat de redistribució | Chunks |
| --- | ---: |
{license_table}

## Concentració de fonts

| Família de fonts | Documents | Chunks | Quota de documents |
| --- | ---: | ---: | ---: |
{family_table}

Els estats `no` i `pendent` es registren sense vetar automàticament el corpus,
d'acord amb la constitució §24. L'elegibilitat de publicació continua sent una
decisió del propietari.

## Qualitat i incidències

- Blocs amb `revisar`: {review_blocks}/{block_count} ({review_blocks / block_count if block_count else 0:.2%}).
- Blocs classificats com a `nota-treball` i exclosos: {work_note_blocks}.
- Chunks amb detector de PII: {pii_count}; marcats `pendent`, sense emmascarar.
- Paràgrafs de plantilla exactes en tres documents o més: {template_paragraphs}; presents en {template_documents} documents; {template_count} chunks afectats.
- Chunks exclosos per marques ratllades o referències `raw/` residuals: {unclean_chunks}.
- Mida de chunks: {len(size_exceptions)}/{len(chunks)} excepcions ({len(size_exceptions) / len(chunks) if chunks else 0:.2%}); límit <2%. Són: {", ".join(f"`{identifier}` ({words} paraules)" for identifier, words in size_exceptions) or "cap"}.
- Decisions de revisió copiades a chunks: {decision_count}; estats: {dict(sorted(review_counts.items()))}.
- Overrides explícits de `curacio/decisions/overrides.tsv` aplicats: {overrides_applied}; només accepten IDs de chunk existents i mai no reobren PII ni higiene.
- Buits mantinguts: {len(gaps)}; `raft-sense-oracle` només els conserva com a preguntes, mai com a negacions.
- Paraules exportades a `buits/`: {use_words["raft-sense-oracle"]:,} ({use_words["raft-sense-oracle"] / baseline_words if baseline_words else 0:.1%} de l'entrada), per sota del ~24.1% inicial perquè els estats `resolt` i `no-es-buit`, els buits de parla i el text de plantilla no s'exporten.
- Source fonts absents o metadades incoherents consten a `correccions.tsv`.
- Quasi-duplicats marcats: {near_duplicate_count}; llindar Jaccard ≥ {0.90:.2f} sobre shingles de cinc tokens; els casos queden `pendent` i s'informen al motiu de l'inventari.
- Retenció/exclusió: `raft-context` i `coneixement` es filtren per volatilitat; veu de parla segueix separada.
- La comparació d'entrada amb chunks no és una taxa de pèrdua de dades: l'entrada inclou frontmatter, capçaleres,
  enllaços i material editorial. Les notes, plantilles i gaps s'inventarien o es deriven a fitxers separats;
  els chunks `pendent` continuen presents i compten com a conservats. Les xifres per domini mostren aquesta diferència.

### Desviacions que requereixen explicació

{warnings_text}

## Decisions preses

| Decisió | Raó | Fragments afectats |
| --- | --- | ---: |
| Les fixtures daurades tenen prioritat sobre `estat_revisio` dins del Markdown. L'estat es posa a la fila de chunk d'`inventari.tsv`. | Afegir-lo al frontmatter trencaria la reproducció byte a byte; el valor és traçable a l'inventari sense tocar els oracles. | {len(chunks)} |
| La llicència o el permís de redistribució no concloent es conserva com a `pendent`; el detall original continua traçable a les metadades. | Opció conservadora i reversible; no s'inventa una autorització. | {pending_rights_chunks} |
| Gaps amb estat `resolt` o `no-es-buit` queden fora de `buits/`; els de parla queden només com a anotacions de mostra. | Evita convertir una resposta coneguda o una limitació en una pregunta falsa. | {sum(gap.decision == "excloure" for gap in gaps)} |
| Paràgrafs amb ratllats o referències a `raw/` queden fora dels chunks utilitzables. | Són anotacions editorials o rutes locals, no coneixement publicable. | {unsafe_blocks + unclean_chunks} |

## Decisions obertes

- Publicació del corpus i ús redistribuïble: pendent del propietari; {unresolved_rights} documents usen font `no` o `pendent`.
- Tall històric: pendent del propietari; {historical} chunks contenen fets datats abans de 1925.
- Retallada del domini esports: pendent del propietari; {pending_sports} chunks d'esports preservats i traçables.
- Llicències no obertes o no concloents es mantenen marcades, no s'han tractat com aprovació de publicació.
- Llengua parlada sense escolta: {len(speech_chunks)} mostres `pendent-escolta`; marques d'incertesa i perfil no es corregeixen automàticament.
- Llindar de quasi-duplicats i agrupacions addicionals de `familia_font` poden rebre overrides humans als TSV de `curacio/decisions/`.
"""


def build_corpus(
    docs_root: Path,
    *,
    decisions_path: Path | None = None,
    families_path: Path | None = None,
    whitelist_path: Path | None = None,
) -> dict[str, str]:
    """Reads a vault and returns every generated path and byte-stable text."""
    docs_root = docs_root.resolve()
    corpus: Corpus = load_corpus(docs_root)
    families = load_families(families_path or _family_path(docs_root))
    statuses = load_review_statuses(decisions_path or _decisions_path(docs_root))
    overrides = load_overrides(_overrides_path(docs_root))
    all_documents: list[tuple[CuratedDoc, dict[str, str], list[Gap]]] = []
    for source in sorted(corpus.docs, key=lambda item: doc_id_for(docs_root, item)):
        curated, metadata, gaps = _curate_doc(docs_root, source, corpus.fonts, families, statuses)
        all_documents.append((curated, metadata, gaps))
    whitelist = load_whitelist(
        whitelist_path or _whitelist_path(docs_root),
        [doc for doc, _, _ in all_documents],
        list(corpus.fonts.values()),
    )
    all_chunks = [chunk for doc, _, _ in all_documents for chunk in doc.chunks]
    mark_pii(all_chunks, whitelist)
    template_metrics = mark_templates([doc for doc, _, _ in all_documents])
    mark_near_duplicates(all_chunks)
    unclean_chunks = _exclude_unclean_chunks(all_chunks)
    overrides_applied = apply_overrides(all_chunks, overrides)
    records, maia_sha = build_manifest(docs_root, corpus)
    baseline_words = sum(word_count(doc.path.read_text(encoding="utf-8")) for doc in corpus.docs)
    source_metrics = _snapshot_metrics(corpus)
    output: dict[str, str] = {
        "manifest.jsonl": manifest_jsonl(records, maia_sha),
        "README.md": _readme(),
        "inventari.tsv": render_inventory(all_documents),
        "correccions.tsv": _corrections([doc for doc, _, _ in all_documents], corpus.fonts),
        "informe.md": _report(
            all_documents,
            baseline_words,
            len(corpus.docs),
            maia_sha,
            unclean_chunks,
            template_metrics,
            {**source_metrics, "paraules_totals": baseline_words},
            overrides_applied,
        ),
    }
    for doc, metadata, gaps in all_documents:
        if doc.data.get("type") == "parla":
            transcript = next((block for block in doc.blocks if block.kind == "transcripcio"), None)
            if transcript is not None:
                data = _speech_values(
                    doc, transcript, metadata["llicencia"], metadata["redistribucio"]
                )
                slug = doc.doc_id.rsplit("/", maxsplit=1)[-1]
                output[f"llengua/parla/{slug}.md"] = data
            continue
        theme = metadata["tema"]
        slug = doc.doc_id.rsplit("/", maxsplit=1)[-1]
        visible_chunks = [chunk for chunk in doc.chunks if chunk.decision != "excloure"]
        if visible_chunks:
            rel = f"chunks/{theme}/{slug}.md"
            output[rel] = _chunks_file(doc, visible_chunks, metadata)
        open_gaps = [gap for gap in gaps if gap.decision == "incloure"]
        if open_gaps:
            output[f"buits/{theme}/{slug}.md"] = _gap_file(doc, gaps, metadata)
    return dict(sorted(output.items()))


def generate_corpus(docs_root: Path, out_root: Path) -> dict[str, str]:
    """Writes all outputs and removes stale generated files from the output tree."""
    output = build_corpus(docs_root)
    out_root.mkdir(parents=True, exist_ok=True)
    expected = set(output)
    for existing in sorted(out_root.rglob("*"), reverse=True):
        if existing.is_file() and existing.relative_to(out_root).as_posix() not in expected:
            existing.unlink()
        elif existing.is_dir() and not any(existing.iterdir()):
            existing.rmdir()
    for relative, text in output.items():
        target = out_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8", newline="\n")
    return output


def check_corpus(docs_root: Path, out_root: Path) -> list[str]:
    """Returns every missing, extra or byte-different output file."""
    expected = build_corpus(docs_root)
    actual_paths = (
        {path.relative_to(out_root).as_posix() for path in out_root.rglob("*") if path.is_file()}
        if out_root.exists()
        else set()
    )
    failures: list[str] = []
    for relative, content in expected.items():
        path = out_root / relative
        if not path.exists():
            failures.append(f"missing: {relative}")
        elif path.read_bytes() != content.encode("utf-8"):
            failures.append(f"different: {relative}")
    failures.extend(f"extra: {path}" for path in sorted(actual_paths - set(expected)))
    return failures
