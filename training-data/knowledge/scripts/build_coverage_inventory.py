#!/usr/bin/env python3
"""Inventory Maia Knowledge articles and summarize conversation coverage.

This report is a source-level backlog aid. A cited article is not necessarily
fully covered; content-level evidence must be reviewed separately.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DOCS = ROOT / "docs" / "temes"
TRAINING = ROOT / "training-data" / "knowledge"
INVENTORY = TRAINING / "work" / "document-inventory.json"
REPORT = TRAINING / "reports" / "coverage-summary.md"


def frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.S)
    if not match:
        return {}
    result: dict[str, str] = {}
    for line in match.group(1).splitlines():
        item = re.match(r"^([\w-]+):\s*(.*?)\s*$", line)
        if item:
            result[item.group(1)] = item.group(2).strip().strip("\"'")
    return result


def document_counts(text: str) -> dict[str, int]:
    headings = len(re.findall(r"^#{1,6}\s+.+$", text, re.M))
    table_rows = 0
    for line in text.splitlines():
        if line.strip().startswith("|") and "|" in line.strip()[1:]:
            if not re.fullmatch(r"\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?", line.strip()):
                table_rows += 1
    bullets = len(re.findall(r"^\s*(?:[-*+] |\d+[.)] )\S", text, re.M))
    links = len(re.findall(r"\[[^\]]+\]\([^)]*\)", text))
    return {"headings": headings, "table_rows_including_headers": table_rows,
            "list_items": bullets, "markdown_links": links}


def font_ids(value: str) -> list[str]:
    return [part.strip().strip("[]\"'") for part in value.strip().strip("[]").split(",") if part.strip()]


def main() -> None:
    docs: list[dict[str, object]] = []
    for path in sorted(DOCS.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        meta = frontmatter(text)
        rel = path.relative_to(ROOT).as_posix()
        ids = font_ids(meta.get("font", ""))
        source_rights = []
        for font_id in ids:
            font_path = ROOT / "docs" / "fonts" / f"{font_id}.md"
            font_meta = frontmatter(font_path.read_text(encoding="utf-8")) if font_path.exists() else {}
            source_rights.append({
                "font_id": font_id,
                "redistribution": font_meta.get("redistribucio", "missing"),
                "license": font_meta.get("llicencia", "missing"),
            })
        statuses = {str(r["redistribution"]) for r in source_rights}
        if not source_rights or "missing" in statuses:
            rights_triage = "missing"
        elif "no" in statuses:
            rights_triage = "no"
        elif "pendent" in statuses or "unknown" in statuses:
            rights_triage = "pending"
        else:
            rights_triage = "yes"
        docs.append({
            "path": rel,
            "kind": meta.get("type", "unknown"),
            "title": meta.get("title", path.stem),
            "topic": meta.get("tema", ""),
            "theme": path.relative_to(DOCS).parts[0],
            "font_ids": ids,
            "source_rights_from_frontmatter": source_rights,
            "rights_triage_from_frontmatter": rights_triage,
            "counts": document_counts(text),
        })

    source_docs: set[str] = set()
    conv_path = TRAINING / "review" / "provenance.jsonl"
    if conv_path.exists():
        for line in conv_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            source_docs.update(record.get("source_documents", []))

    article_docs = [d for d in docs if d["kind"] == "article"]
    cited = {d["path"] for d in article_docs if d["path"] in source_docs}
    by_theme: dict[str, list[dict[str, object]]] = defaultdict(list)
    by_rights: dict[str, list[dict[str, object]]] = defaultdict(list)
    for doc in article_docs:
        by_theme[str(doc["theme"])].append(doc)
        by_rights[str(doc["rights_triage_from_frontmatter"])].append(doc)

    INVENTORY.parent.mkdir(parents=True, exist_ok=True)
    INVENTORY.write_text(json.dumps({"documents": docs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    counts = Counter(str(d["kind"]) for d in docs)
    total = len(article_docs)
    lines = [
        "# Cobertura de Maia Knowledge",
        "",
        "Informe generat amb `scripts/build_coverage_inventory.py`.",
        "La cobertura és per document citat i és només un límit inferior: una cita no prova que totes les seccions, files o afirmacions del document tinguin conversa.",
        "",
        "## Inventari",
        "",
        f"- Fitxers Markdown a `docs/temes/`: **{len(docs)}**.",
        f"- Fitxes factuals (`type: article`): **{counts['article']}**.",
        f"- Índexs (`type: index`): **{counts['index']}**; s'usen per navegar, no com a font factual autònoma.",
        f"- Seccions: **{sum(int(d['counts']['headings']) for d in article_docs)}**.",
        f"- Files de taula incloent capçaleres: **{sum(int(d['counts']['table_rows_including_headers']) for d in article_docs)}**.",
        f"- Elements de llista: **{sum(int(d['counts']['list_items']) for d in article_docs)}**.",
        f"- Enllaços Markdown: **{sum(int(d['counts']['markdown_links']) for d in article_docs)}**.",
        "",
        "## Cobertura citada per tema principal",
        "",
        "| Tema | Fitxes article | Amb conversa citada | Sense conversa citada |",
        "|---|---:|---:|---:|",
    ]
    for theme, items in sorted(by_theme.items()):
        covered = sum(1 for d in items if d["path"] in cited)
        lines.append(f"| `{theme}` | {len(items)} | {covered} | {len(items) - covered} |")
    lines += [
        "",
        "## Tria inicial de drets a la font principal declarada",
        "",
        "Aquesta tria només mira el camp `font` de la capçalera i la seva fitxa a `docs/fonts/`. No comprova totes les fonts citades al cos, ni substitueix una revisió de drets per registre.",
        "",
        "| Estat declarat | Fitxes |",
        "|---|---:|",
    ]
    for status in ("yes", "no", "pending", "missing"):
        lines.append(f"| `{status}` | {len(by_rights[status])} |")
    lines += [
        "",
        f"**Total:** {total} fitxes article; **{len(cited)}** tenen almenys una conversa citada i **{total - len(cited)}** encara no en tenen.",
        "",
        "## Límits",
        "",
        "- La cobertura citada només indica que una conversa apunta a la fitxa. No acredita cobertura de cada secció, taula, fila, llista, data o excepció.",
        "- Els registres de revisió poden tenir drets pendents i no són exports d'entrenament.",
        "- La font de veritat és el corpus actual; torneu a generar aquest informe després de canvis a `docs/temes/` o als registres de procedència.",
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {INVENTORY.relative_to(ROOT)}")
    print(f"Wrote {REPORT.relative_to(ROOT)}")
    print(f"Articles: {counts['article']}; indexes: {counts['index']}; cited article docs: {len(cited)}")


if __name__ == "__main__":
    main()
