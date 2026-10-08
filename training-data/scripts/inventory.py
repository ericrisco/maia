#!/usr/bin/env python3
"""Build exhaustive pending inventories from Maia's Knowledge and Language corpus."""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TRAINING = ROOT / "training-data"
FIELDS = ("type", "title", "description", "tema", "veu", "epoca", "apte_llengua", "font", "timestamp", "tags")


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return {}
    result: dict[str, str] = {}
    for line in lines[1:end]:
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*?)\s*$", line)
        if match:
            result[match.group(1)] = match.group(2).strip().strip("\"'")
    if "title" not in result:
        for line in lines[end + 1 :]:
            match = re.match(r"^#\s+(.+?)\s*$", line)
            if match:
                result["title"] = match.group(1)
                break
    return result


def write_inventory(source: Path, target: Path, language: bool = False) -> int:
    fields = (
        ["path", "title", "type", "veu", "epoca", "apte_llengua", "font", "tags", "status", "review_notes"]
        if language
        else ["path", "title", "description", "tema", "type", "veu", "epoca", "font", "timestamp", "tags", "status", "conversation_ids", "exclusion_reason"]
    )
    files = sorted(source.rglob("*.md"), key=lambda item: item.as_posix().casefold())
    previous: dict[str, dict[str, str]] = {}
    if target.exists():
        with target.open(encoding="utf-8", newline="") as stream:
            previous = {row["path"]: row for row in csv.DictReader(stream)}
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for path in files:
            meta = frontmatter(path)
            row = {key: meta.get(key, "") for key in FIELDS}
            row["path"] = path.relative_to(ROOT).as_posix()
            prior = previous.get(row["path"], {})
            default_status = "pending-review" if language else "pending"
            row["status"] = prior.get("status") or default_status
            if language:
                row["review_notes"] = prior.get("review_notes", "")
            else:
                row["conversation_ids"] = prior.get("conversation_ids", "")
                row["exclusion_reason"] = prior.get("exclusion_reason", "")
            writer.writerow({key: row.get(key, "") for key in fields})
    return len(files)


def main() -> None:
    knowledge_count = write_inventory(
        ROOT / "docs/temes", TRAINING / "knowledge/work/coverage.csv"
    )
    language_count = write_inventory(
        ROOT / "docs/parla", TRAINING / "language/work/coverage.csv", language=True
    )
    print(f"Knowledge inventari: {knowledge_count} fitxers")
    print(f"Language inventari: {language_count} peces")
    print("Tots els registres comencen pendents de revisió.")


if __name__ == "__main__":
    main()
