#!/usr/bin/env python3
"""Index topic documents and show which ones have a cited review candidate."""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DOCS = ROOT / "docs" / "temes"
REVIEW = ROOT / "training-data" / "knowledge" / "review"
WORK = ROOT / "training-data" / "knowledge" / "work"
REPORTS = ROOT / "training-data" / "knowledge" / "reports"


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        return {}
    result: dict[str, str] = {}
    for line in text[4:end].splitlines():
        match = re.match(r"^([a-zA-Z0-9_-]+):\s*(.*?)\s*$", line)
        if match:
            result[match.group(1)] = match.group(2).strip("\"'")
    return result


def slug(text: str) -> str:
    value = text.strip().lower()
    value = re.sub(r"[`*_]", "", value)
    value = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE)
    return re.sub(r"[-\s]+", "-", value).strip("-")


def candidate_sources() -> tuple[dict[str, set[int]], dict[str, set[int]], int]:
    by_document: dict[str, set[int]] = defaultdict(set)
    by_section: dict[str, set[int]] = defaultdict(set)
    conversations = (REVIEW / "conversations.jsonl").read_text(encoding="utf-8").splitlines()
    traces = (REVIEW / "provenance.jsonl").read_text(encoding="utf-8").splitlines()
    if len(conversations) != len(traces):
        raise ValueError("conversation and provenance line counts differ")
    for line_number, raw in enumerate(traces, 1):
        trace = json.loads(raw)
        files = list(trace.get("source_documents", []))
        if trace.get("source_document"):
            files.append(trace["source_document"])
        for file in files:
            if file.startswith("docs/temes/"):
                by_document[file].add(line_number)
        for evidence_id in trace.get("evidence_ids", []):
            if "#" not in evidence_id or not evidence_id.startswith("docs/temes/"):
                continue
            file, anchor = evidence_id.split("#", 1)
            by_section[f"{file}#{anchor}"].add(line_number)
    return by_document, by_section, len(conversations)


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    by_document, by_section, candidate_count = candidate_sources()
    documents = []
    topic_totals: Counter[str] = Counter()
    topic_referenced: Counter[str] = Counter()
    total_sections = referenced_sections = 0

    for path in sorted(DOCS.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        metadata = frontmatter(text)
        if metadata.get("type") != "article":
            continue
        relative = path.relative_to(ROOT).as_posix()
        sections = []
        for heading in re.finditer(r"^(#{2,6})\s+(.+?)\s*#*\s*$", text, re.M):
            title = heading.group(2).strip()
            anchor = slug(title)
            section_key = f"{relative}#{anchor}"
            references = sorted(by_section.get(section_key, set()))
            sections.append({"title": title, "anchor": anchor, "candidate_lines": references})
            total_sections += 1
            referenced_sections += bool(references)
        topic = metadata.get("tema", "")
        topic_totals[topic] += 1
        candidate_lines = sorted(by_document.get(relative, set()))
        topic_referenced[topic] += bool(candidate_lines)
        documents.append(
            {
                "path": relative,
                "title": metadata.get("title", ""),
                "topic": topic,
                "candidate_lines": candidate_lines,
                "status": "candidate_source_cited" if candidate_lines else "no_candidate_source_cited",
                "sections": sections,
            }
        )

    inventory = {
        "scope": "docs/temes/**/*.md with frontmatter type=article",
        "warning": "A source citation does not prove that all facts or sections in a document are covered.",
        "documents": documents,
    }
    (WORK / "document-inventory.json").write_text(
        json.dumps(inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    summary = {
        "scope": inventory["scope"],
        "conversation_candidates": candidate_count,
        "article_documents": len(documents),
        "documents_with_candidate_source": sum(bool(item["candidate_lines"]) for item in documents),
        "documents_without_candidate_source": sum(not item["candidate_lines"] for item in documents),
        "sections": total_sections,
        "sections_with_explicit_evidence_reference": referenced_sections,
        "sections_without_explicit_evidence_reference": total_sections - referenced_sections,
        "warning": inventory["warning"],
        "by_topic": {
            topic: {
                "documents": topic_totals[topic],
                "documents_with_candidate_source": topic_referenced[topic],
                "documents_without_candidate_source": topic_totals[topic] - topic_referenced[topic],
            }
            for topic in sorted(topic_totals)
        },
    }
    (REPORTS / "coverage-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"Indexed {summary['article_documents']} articles and {total_sections} sections; "
        f"{summary['documents_with_candidate_source']} articles have cited candidates."
    )


if __name__ == "__main__":
    main()
