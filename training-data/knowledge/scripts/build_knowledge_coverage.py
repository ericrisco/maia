#!/usr/bin/env python3
"""Build a topic and document coverage report for Maia Knowledge review data."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "training-data" / "knowledge"
INVENTORY = DATA / "work" / "documents.jsonl"
UNITS = DATA / "work" / "document-units.jsonl"
CONVERSATIONS = DATA / "review" / "conversations.jsonl"
RECORDS = DATA / "review" / "records.jsonl"
REPORT = DATA / "reports" / "coverage.md"


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def build_report() -> str:
    documents = read_jsonl(INVENTORY)
    conversations = read_jsonl(CONVERSATIONS)
    records = read_jsonl(RECORDS)
    unit_ids = {row["unit_id"] for row in read_jsonl(UNITS)}

    if len(conversations) != len(records):
        raise ValueError(f"JSONL count mismatch: {len(conversations)} conversations, {len(records)} records")

    seen_ids: set[str] = set()
    article_docs: dict[str, dict] = {}
    topic_articles: Counter[str] = Counter()
    for doc in documents:
        path = doc["path"]
        topic = doc.get("topic") or "(sense tema)"
        if doc.get("type") == "article":
            article_docs[path] = doc
            topic_articles[topic] += 1

    topic_conversations: dict[str, set[str]] = defaultdict(set)
    topic_covered_docs: dict[str, set[str]] = defaultdict(set)
    covered_articles: set[str] = set()
    mapped_units: set[str] = set()
    record_counts = Counter()

    for index, record in enumerate(records, start=1):
        record_id = record.get("id")
        if not record_id or record_id in seen_ids:
            raise ValueError(f"Missing or duplicate record id at line {index}: {record_id!r}")
        seen_ids.add(record_id)
        if record.get("conversation_line") != index:
            raise ValueError(f"Record {record_id} points to line {record.get('conversation_line')}, expected {index}")
        conversation_id = record_id
        for coverage in record.get("coverage", []):
            path = coverage.get("document")
            if path not in article_docs:
                raise ValueError(f"Record {record_id} cites a missing or non-article document: {path}")
            topic = article_docs[path].get("topic") or "(sense tema)"
            topic_conversations[topic].add(conversation_id)
            topic_covered_docs[topic].add(path)
            covered_articles.add(path)
            record_counts[topic] += 1
            for unit_id in coverage.get("unit_ids", []):
                if unit_id not in unit_ids:
                    raise ValueError(f"Record {record_id} cites an unknown unit id: {unit_id}")
                mapped_units.add(unit_id)

    rows = [
        "# Cobertura de Maia Knowledge",
        "",
        "Informe regenerable a partir de l'inventari, `conversations.jsonl` i `records.jsonl`.",
        "",
        f"- Documents Markdown inventariats: **{len(documents)}**.",
        f"- Articles del brain: **{len(article_docs)}**.",
        f"- Converses de revisió amb registre: **{len(conversations)}**.",
        f"- Articles citats per almenys una conversa: **{len(covered_articles)}**.",
        f"- Unitats estructurals enllaçades explícitament amb `unit_ids`: **{len(mapped_units)}**.",
        "",
        "> La cobertura d'un article només indica que hi ha una conversa que el cita. No implica que tot el document, tema o coneixement estigui cobert. Les unitats sense enllaç explícit no es compten.",
        "",
        "## Articles i converses per tema",
        "",
        "| Tema del corpus | Articles | Articles citats | Converses |",
        "| --- | ---: | ---: | ---: |",
    ]
    for topic in sorted(topic_articles):
        rows.append(
            f"| `{topic}` | {topic_articles[topic]} | "
            f"{len(topic_covered_docs.get(topic, set()))} | "
            f"{len(topic_conversations.get(topic, set()))} |"
        )
    rows.extend(
        [
            "",
            "## Límits de l'informe",
            "",
            "- Els recomptes de converses són registres associats a documents del tema, no una quota objectiu.",
            "- Una conversa pot citar més d'un document; els recomptes per tema poden solapar-se.",
            "- La cobertura es calcula a nivell de document i d'unitat només quan `unit_ids` és explícit; no s'infereix a partir del títol, del tema o de les afirmacions.",
            "- L'informe no avalua qualitat de conversa, exactitud factual ni drets; aquests camps continuen a la revisió de cada registre.",
            "",
        ]
    )
    return "\n".join(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if the checked-in report is stale")
    args = parser.parse_args()
    report = build_report()
    if args.check:
        if not REPORT.exists() or REPORT.read_text(encoding="utf-8") != report:
            print("coverage report is missing or stale; run this script without --check")
            return 1
        print("coverage report is current")
        return 0
    REPORT.write_text(report, encoding="utf-8")
    print(f"wrote {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
