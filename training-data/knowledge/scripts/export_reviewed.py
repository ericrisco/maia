#!/usr/bin/env python3
"""Export reviewed Knowledge conversations to stable train/validation/test JSONL."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "training-data" / "knowledge"
REVIEW = DATA / "review"
OUTPUT = DATA / "output"
REPORTS = DATA / "reports"
SPLITS = ("train", "validation", "test")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{number}: JSON invàlid: {exc}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{number}: cada línia ha de ser un objecte")
        rows.append(value)
    return rows


def messages_for(row: dict[str, Any]) -> list[dict[str, str]]:
    example_id = row["example_id"]
    messages = row.get("messages")
    if not isinstance(messages, list) or len(messages) < 4 or len(messages) % 2:
        raise ValueError(f"{example_id}: calen almenys dos intercanvis complets")
    expected = ["user", "assistant"] * (len(messages) // 2)
    if [message.get("role") for message in messages] != expected:
        raise ValueError(f"{example_id}: els rols han d'alternar user/assistant")
    for message in messages:
        if not isinstance(message.get("content"), str) or not message["content"].strip():
            raise ValueError(f"{example_id}: missatge sense text")
    return messages


def main() -> None:
    conversations = read_jsonl(REVIEW / "conversations.jsonl")
    provenance_rows = read_jsonl(REVIEW / "provenance.jsonl")
    policy = json.loads((DATA / "split-assignments.json").read_text(encoding="utf-8"))
    groups = policy.get("groups", {})
    if not isinstance(groups, dict):
        raise ValueError("split-assignments.json ha de tenir un objecte 'groups'")

    by_id: dict[str, dict[str, Any]] = {}
    for row in conversations:
        example_id = row.get("example_id")
        if not isinstance(example_id, str) or not example_id:
            raise ValueError("Cada conversa necessita un example_id")
        if example_id in by_id:
            raise ValueError(f"ID de conversa duplicat: {example_id}")
        by_id[example_id] = row

    provenance: dict[str, dict[str, Any]] = {}
    for row in provenance_rows:
        example_id = row.get("example_id")
        if not isinstance(example_id, str) or not example_id:
            raise ValueError("Cada procedència necessita un example_id")
        if example_id in provenance:
            raise ValueError(f"ID de procedència duplicat: {example_id}")
        provenance[example_id] = row
    if by_id.keys() != provenance.keys():
        raise ValueError("Les converses i les procedències no tenen els mateixos IDs")

    exported: dict[str, list[dict[str, Any]]] = {split: [] for split in SPLITS}
    exported_sources: set[str] = set()
    attributions: set[str] = set()
    rights: set[str] = set()
    seen: set[str] = set()
    for example_id, row in by_id.items():
        source = provenance[example_id]
        if not source.get("exportable", False):
            continue
        if source.get("editorial_status", "").split(";")[0] != "revisada":
            raise ValueError(f"{example_id}: conversa exportable sense revisió editorial")
        split_group = source.get("split_group")
        split = groups.get(split_group)
        if split not in SPLITS:
            raise ValueError(f"{example_id}: assigna el grup {split_group!r} a un split")
        source_documents = source.get("source_documents")
        if not isinstance(source_documents, list) or not source_documents:
            raise ValueError(f"{example_id}: falta source_documents")
        for source_path in source_documents:
            if not str(source_path).startswith("docs/temes/"):
                raise ValueError(f"{example_id}: font Knowledge no admesa: {source_path}")
            if not (ROOT / source_path).is_file():
                raise ValueError(f"{example_id}: no existeix la font {source_path}")
            exported_sources.add(str(source_path))
        payload = {"messages": messages_for(row)}
        serialized = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        if serialized in seen:
            raise ValueError(f"Conversa duplicada: {example_id}")
        seen.add(serialized)
        exported[split].append(payload)
        if source.get("attribution"):
            attributions.add(str(source["attribution"]))
        if source.get("rights_status"):
            rights.add(str(source["rights_status"]))

    OUTPUT.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    for split in SPLITS:
        content = "".join(
            json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n"
            for row in exported[split]
        )
        (OUTPUT / f"{split}.jsonl").write_text(content, encoding="utf-8")

    attribution_lines = [
        "# Procedència i drets de Maia Knowledge",
        "",
        "Cada JSONL d'exportació conté només `messages`. La procedència per registre",
        "és a `review/provenance.jsonl`. No s'atribueix una llicència global al conjunt.",
        "La inclusió al conjunt de preparació segueix la decisió del propietari del projecte.",
        "Les condicions de cada font s'han de revisar abans de redistribuir el dataset;",
        "la inclusió no converteix un estat pendent o negatiu en permís de redistribució.",
        "",
        "## Fonts dels registres exportats",
        "",
    ]
    attribution_lines.extend(f"- {item}" for item in sorted(attributions))
    attribution_lines.extend(["", "## Condicions registrades", ""])
    attribution_lines.extend(f"- {item}" for item in sorted(rights))
    (OUTPUT / "ATTRIBUTION.md").write_text("\n".join(attribution_lines) + "\n", encoding="utf-8")

    article_count = sum(1 for path in (ROOT / "docs" / "temes").rglob("*.md") if path.is_file())
    fact_articles = sum(
        1
        for path in (ROOT / "docs" / "temes").rglob("*.md")
        if path.is_file() and "type: article" in path.read_text(encoding="utf-8", errors="replace")[:1000]
    )
    counts = Counter({split: len(exported[split]) for split in SPLITS})
    report = [
        "# Export de Maia Knowledge",
        "",
        "Aquest report no acredita cobertura exhaustiva: mostra els registres aprovats i les fitxes representades fins ara.",
        "",
        f"- Converses candidates: **{len(by_id)}**.",
        f"- Converses exportades: **{sum(counts.values())}**.",
        f"- Fitxes font representades: **{len(exported_sources)}**.",
        f"- Fitxes article a `docs/temes/`: **{fact_articles}** (fitxers totals: {article_count}).",
        "",
        "| Split | Converses |",
        "|---|---:|",
    ]
    report.extend(f"| `{split}` | {counts[split]} |" for split in SPLITS)
    report += ["", "## Fitxes representades", ""]
    report.extend(f"- `{path}`" for path in sorted(exported_sources))
    (REPORTS / "export-summary.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(
        f"Exportades {sum(counts.values())} converses: "
        + ", ".join(f"{split}={counts[split]}" for split in SPLITS)
    )


if __name__ == "__main__":
    main()
