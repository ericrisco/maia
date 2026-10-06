#!/usr/bin/env python3
"""Export reviewed Maia Knowledge conversations into source-grouped JSONL splits."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
KNOWLEDGE = ROOT / "training-data" / "knowledge"
CONVERSATIONS = KNOWLEDGE / "review" / "conversations.jsonl"
PROVENANCE = KNOWLEDGE / "review" / "provenance.jsonl"
ASSIGNMENTS = KNOWLEDGE / "split-assignments.json"
OUTPUT = KNOWLEDGE / "output"
REPORT = KNOWLEDGE / "reports" / "export-summary.md"
SPLITS = ("train", "validation", "test")


def read_jsonl(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    result = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{number}: invalid JSON: {exc}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{number}: each JSONL row must be an object")
        result.append(value)
    return result


def content_sources(provenance: dict[str, object]) -> set[str]:
    sources = provenance.get("source_documents")
    if not isinstance(sources, list):
        raise ValueError(f"{provenance.get('example_id')}: source_documents is missing")
    return {
        str(source)
        for source in sources
        if str(source).startswith(("docs/temes/", "docs/raw/"))
    }


def main() -> None:
    conversations = read_jsonl(CONVERSATIONS)
    provenance_rows = read_jsonl(PROVENANCE)
    policy = json.loads(ASSIGNMENTS.read_text(encoding="utf-8"))
    assignments = policy.get("groups", {})
    if not isinstance(assignments, dict):
        raise ValueError("split-assignments.json must contain a groups object")
    if any(split not in SPLITS for split in assignments.values()):
        raise ValueError("split assignments may only be train, validation, or test")

    conversations_by_id: dict[str, dict[str, object]] = {}
    for row in conversations:
        example_id = row.get("example_id")
        if not isinstance(example_id, str) or not example_id:
            raise ValueError("each review conversation needs a non-empty example_id")
        if example_id in conversations_by_id:
            raise ValueError(f"duplicate conversation id: {example_id}")
        conversations_by_id[example_id] = row

    provenance_by_id: dict[str, dict[str, object]] = {}
    for row in provenance_rows:
        example_id = row.get("example_id")
        if not isinstance(example_id, str) or not example_id:
            raise ValueError("each provenance row needs a non-empty example_id")
        if example_id in provenance_by_id:
            raise ValueError(f"duplicate provenance id: {example_id}")
        provenance_by_id[example_id] = row
    if conversations_by_id.keys() != provenance_by_id.keys():
        missing_provenance = sorted(conversations_by_id.keys() - provenance_by_id.keys())
        missing_conversation = sorted(provenance_by_id.keys() - conversations_by_id.keys())
        raise ValueError(
            f"conversation/provenance mismatch; missing provenance={missing_provenance}, "
            f"missing conversations={missing_conversation}"
        )

    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    source_splits: dict[str, set[str]] = defaultdict(set)
    exported_ids: set[str] = set()
    seen_payloads: set[str] = set()
    for example_id, provenance in provenance_by_id.items():
        sources = content_sources(provenance)
        if not sources:
            raise ValueError(f"{example_id}: no docs/temes or docs/raw content source")
        unassigned = sorted(source for source in sources if source not in assignments)
        if unassigned:
            raise ValueError(f"{example_id}: assign source groups before export: {unassigned}")
        chosen = {str(assignments[source]) for source in sources}
        if len(chosen) != 1:
            raise ValueError(f"{example_id}: linked sources cross splits: {sorted(chosen)}")
        split = chosen.pop()
        for source in sources:
            source_splits[source].add(split)
        if not provenance.get("exportable", False):
            continue
        if provenance.get("review_status") != "approved_editorial_and_rights":
            raise ValueError(f"{example_id}: exportable record lacks full editorial/rights approval")
        conversation = conversations_by_id[example_id]
        messages = conversation.get("messages")
        if not isinstance(messages, list) or len(messages) < 2 or len(messages) % 2:
            raise ValueError(f"{example_id}: messages must contain complete user/assistant turns")
        expected = ["user", "assistant"] * (len(messages) // 2)
        if [message.get("role") for message in messages if isinstance(message, dict)] != expected:
            raise ValueError(f"{example_id}: roles must alternate user and assistant")
        if any(not isinstance(message.get("content"), str) or not message["content"].strip()
               for message in messages if isinstance(message, dict)):
            raise ValueError(f"{example_id}: every message needs non-empty text")
        payload = {"messages": messages}
        serialized = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        if serialized in seen_payloads:
            raise ValueError(f"{example_id}: duplicate exported conversation")
        seen_payloads.add(serialized)
        grouped[split].append(payload)
        exported_ids.add(example_id)

    OUTPUT.mkdir(parents=True, exist_ok=True)
    OUTPUT_COUNTS: Counter[str] = Counter()
    for split in SPLITS:
        payloads = grouped[split]
        payloads.sort(key=lambda row: json.dumps(row, ensure_ascii=False, sort_keys=True))
        content = "".join(
            json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n"
            for row in payloads
        )
        target = OUTPUT / f"{split}.jsonl"
        target.write_text(content, encoding="utf-8")
        OUTPUT_COUNTS[split] = len(payloads)

    attributions = sorted({
        str(row["attribution"])
        for example_id, row in provenance_by_id.items()
        if example_id in exported_ids and row.get("attribution")
    })
    attribution_lines = [
        "# Atribució de Maia Knowledge",
        "",
        "Els fitxers JSONL contenen només `messages`. La procedència detallada per registre",
        "es conserva a `review/provenance.jsonl`.",
        "",
        "El conjunt derivat es distribueix sota [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/),",
        "d'acord amb les fonts CC BY-SA incorporades. Les dades del BOPA es reutilitzen",
        "segons les condicions oficials registrades al corpus; el BOPA no implica cap suport",
        "al projecte.",
        "",
        "## Fonts dels registres exportats",
        "",
    ]
    attribution_lines.extend(f"- {entry}" for entry in attributions)
    (OUTPUT / "ATTRIBUTION.md").write_text("\n".join(attribution_lines) + "\n", encoding="utf-8")

    article_sources = sorted({
        source
        for example_id in exported_ids
        for source in content_sources(provenance_by_id[example_id])
        if source.startswith("docs/temes/")
    })
    report_lines = [
        "# Export de Maia Knowledge",
        "",
        "Generat per `scripts/export_approved.py`. Cada línia dels JSONL conté una conversa amb `messages`; no hi ha camps interns.",
        "",
        f"- Converses aprovades exportades: **{len(exported_ids)}**.",
        f"- Fitxes `docs/temes/` representades: **{len(article_sources)}**.",
        f"- Converses de revisió no exportables: **{len(conversations_by_id) - len(exported_ids)}**.",
        "",
        "| Split | Converses |",
        "|---|---:|",
    ]
    report_lines.extend(f"| `{split}` | {OUTPUT_COUNTS[split]} |" for split in SPLITS)
    report_lines += [
        "",
        "## Fonts incloses",
        "",
    ]
    report_lines.extend(f"- `{source}` → `{assignments[source]}`" for source in article_sources)
    report_lines += [
        "",
        "Aquesta exportació és parcial. El recompte de fitxes representades no acredita cobertura exhaustiva del coneixement del corpus.",
        "",
    ]
    REPORT.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"Exported {len(exported_ids)} approved conversations: " + ", ".join(
        f"{split}={OUTPUT_COUNTS[split]}" for split in SPLITS
    ))
    print(f"Wrote {REPORT.relative_to(ROOT)} and output/ATTRIBUTION.md")


if __name__ == "__main__":
    main()
