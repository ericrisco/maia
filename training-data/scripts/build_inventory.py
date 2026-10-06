"""Regenerate structural inventories and eligibility reports from the Maia corpus."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

def main() -> None:
    from training_data.inventory import scan_tree
    from training_data.knowledge import extract_knowledge, write_knowledge_extraction
    from training_data.language import extract_language, write_language_selection
    from training_data.language_conversations import write_human_conversations

    inventory = scan_tree(ROOT / "docs")

    knowledge = extract_knowledge(inventory)
    write_knowledge_extraction(
        knowledge,
        work=ROOT / "training-data/knowledge/work",
        reports=ROOT / "training-data/knowledge/reports",
    )

    language = extract_language(inventory)
    write_language_selection(
        language,
        work=ROOT / "training-data/language/work",
        reports=ROOT / "training-data/language/reports",
    )
    conversation_report = write_human_conversations(
        language, work=ROOT / "training-data/language/work"
    )
    report_path = ROOT / "training-data/language/reports/conversations.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(asdict(conversation_report), ensure_ascii=False, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )

    print("Knowledge:", knowledge.report)
    print("Language eligibility:", language.report)
    print("Language explicit conversations:", conversation_report)


if __name__ == "__main__":
    main()
