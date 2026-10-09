#!/usr/bin/env python3
"""Build exhaustive Markdown inventories while preserving review progress."""

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "training-data"
FIELDS = ["path", "topic", "title", "type", "voice", "period", "language_eligible", "status", "conversation_ids", "notes"]


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        return {}
    fields = {}
    for line in text[4:end].splitlines():
        match = re.match(r"^([\w-]+):\s*(.*?)\s*$", line)
        if match:
            fields[match.group(1)] = match.group(2).strip("\"'")
    return fields


def previous_rows(target: Path) -> dict[str, dict[str, str]]:
    if not target.exists():
        return {}
    with target.open(encoding="utf-8", newline="") as stream:
        return {row["path"]: row for row in csv.DictReader(stream)}


def build(source_root: Path, target: Path) -> int:
    previous = previous_rows(target)
    rows = []
    for path in sorted(source_root.rglob("*.md")):
        rel = path.relative_to(ROOT).as_posix()
        meta = frontmatter(path)
        rel_to_domain = path.relative_to(source_root)
        topic = meta.get("tema", "/".join(rel_to_domain.parts[:-1]))
        voice = meta.get("veu", "")
        period = meta.get("epoca", "")
        declared = meta.get("apte_llengua", "").lower() == "true"
        eligible = declared and voice == "originaria" and period == "contemporania"
        old = previous.get(rel, {})
        rows.append({
            "path": rel,
            "topic": topic,
            "title": meta.get("title", ""),
            "type": meta.get("type", ""),
            "voice": voice,
            "period": period,
            "language_eligible": str(eligible).lower(),
            "status": old.get("status") or "pending",
            "conversation_ids": old.get("conversation_ids", ""),
            "notes": old.get("notes", ""),
        })
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def main() -> None:
    knowledge = build(ROOT / "docs/temes", DATA / "knowledge/work/coverage.csv")
    language = build(ROOT / "docs/parla", DATA / "language/work/coverage.csv")
    print(f"Knowledge: {knowledge} documents; Language: {language} documents.")


if __name__ == "__main__":
    main()
