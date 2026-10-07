#!/usr/bin/env python3
"""Inventory all Maia Knowledge articles and report reviewed document coverage."""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "training-data" / "knowledge"
REVIEW = DATA / "review"
WORK = DATA / "work"
REPORTS = DATA / "reports"
ALLOWED_STATUS = {"not_started", "in_progress", "complete", "no_natural_question"}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    if not path.exists():
        return result
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{number}: JSON invàlid: {exc}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{number}: s'esperava un objecte")
        result.append(value)
    return result


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: falta el frontmatter YAML inicial")
    _, block, _ = text.split("---", 2)
    result: dict[str, str] = {}
    for key in ("type", "title", "tema", "font"):
        match = re.search(rf"(?m)^{key}:\s*(.*?)\s*$", block)
        if match:
            value = match.group(1).strip()
            if len(value) > 1 and value[0] in "\"'" and value[-1] == value[0]:
                value = value[1:-1]
            result[key] = value
    if "type" not in result or "title" not in result:
        raise ValueError(f"{path}: falta type o title al frontmatter")
    return result


def main() -> None:
    status_path = WORK / "document-status.json"
    human_status = json.loads(status_path.read_text(encoding="utf-8")) if status_path.exists() else {}
    if not isinstance(human_status, dict):
        raise ValueError("document-status.json ha de ser un objecte per ruta")

    provenance = read_jsonl(REVIEW / "provenance.jsonl")
    records_by_source: dict[str, list[str]] = defaultdict(list)
    for row in provenance:
        example_id = row.get("example_id")
        for source in row.get("source_documents", []):
            if isinstance(source, str) and source.startswith("docs/temes/"):
                records_by_source[source].append(str(example_id))

    files = sorted((ROOT / "docs" / "temes").rglob("*.md"))
    inventory: list[dict[str, Any]] = []
    totals: Counter[str] = Counter()
    by_topic: dict[str, Counter[str]] = defaultdict(Counter)
    known_paths: set[str] = set()
    for path in files:
        relative = path.relative_to(ROOT).as_posix()
        known_paths.add(relative)
        metadata = frontmatter(path)
        state = human_status.get(relative, {})
        status = state.get("status") if isinstance(state, dict) else None
        if status is None:
            status = "in_progress" if records_by_source.get(relative) else "not_started"
        if status not in ALLOWED_STATUS:
            raise ValueError(f"{relative}: estat desconegut {status!r}")
        if status == "complete" and not state.get("completion_note"):
            raise ValueError(f"{relative}: complete necessita completion_note")
        if status == "no_natural_question" and not state.get("reason"):
            raise ValueError(f"{relative}: no_natural_question necessita reason")
        record = {
            "path": relative,
            "title": metadata["title"],
            "type": metadata["type"],
            "topic": metadata.get("tema", ""),
            "source": metadata.get("font", ""),
            "status": status,
            "conversation_count": len(records_by_source.get(relative, [])),
            "conversation_ids": sorted(set(records_by_source.get(relative, []))),
            "reviewed_units": state.get("reviewed_units", []) if isinstance(state, dict) else [],
            "completion_note": state.get("completion_note", "") if isinstance(state, dict) else "",
            "reason": state.get("reason", "") if isinstance(state, dict) else "",
        }
        inventory.append(record)
        if metadata["type"] == "article":
            totals[status] += 1
            by_topic[metadata.get("tema", "(sense tema)")][status] += 1

    stale_status = sorted(set(human_status) - known_paths)
    if stale_status:
        raise ValueError(f"Rutes de document-status.json que no existeixen: {stale_status}")

    article_count = sum(1 for row in inventory if row["type"] == "article")
    (WORK / "document-inventory.json").write_text(
        json.dumps(
            {
                "source_root": "docs/temes/",
                "article_count": article_count,
                "file_count": len(inventory),
                "status_totals": {status: totals[status] for status in sorted(ALLOWED_STATUS)},
                "documents": inventory,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    lines = [
        "# Cobertura de Maia Knowledge",
        "",
        "Cada fitxa article es revisa sencera. Una conversa només marca la fitxa com a iniciada; no demostra que tots els fets hi estiguin coberts.",
        "",
        f"- Fitxes article: **{article_count}**.",
        f"- Fitxers totals, inclosos índexs: **{len(inventory)}**.",
        f"- Converses candidates: **{len({example_id for ids in records_by_source.values() for example_id in ids})}**.",
        "",
        "| Estat de revisió | Fitxes |",
        "|---|---:|",
    ]
    labels = {
        "not_started": "No començades",
        "in_progress": "En curs",
        "complete": "Revisades completes",
        "no_natural_question": "Revisades sense pregunta natural",
    }
    lines.extend(f"| {labels[status]} | {totals[status]} |" for status in sorted(ALLOWED_STATUS))
    lines += ["", "## Estat per tema", "", "| Tema | Articles | No començades | En curs | Completes | Sense pregunta natural |", "|---|---:|---:|---:|---:|---:|"]
    for topic, counts in sorted(by_topic.items()):
        total = sum(counts.values())
        lines.append(
            f"| `{topic}` | {total} | {counts['not_started']} | {counts['in_progress']} | "
            f"{counts['complete']} | {counts['no_natural_question']} |"
        )
    (REPORTS / "coverage-summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Inventariades {article_count} fitxes article de {len(inventory)} fitxers")
    print("Estats:", ", ".join(f"{key}={totals[key]}" for key in sorted(ALLOWED_STATUS)))


if __name__ == "__main__":
    main()
