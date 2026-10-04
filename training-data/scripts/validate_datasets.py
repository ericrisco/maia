"""Executa els validators de Maia Knowledge i Maia Language contra les sortides."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from training_data.inventory import scan_tree
from training_data.knowledge import extract_knowledge
from training_data.knowledge_coverage import build_knowledge_coverage
from training_data.knowledge_deduplicate import deduplicate_knowledge_candidates
from training_data.knowledge_generate import (
    build_knowledge_candidates,
    build_relation_candidates,
    classify_knowledge_candidates,
)
from training_data.knowledge_split import split_knowledge_candidates
from training_data.language import extract_language
from training_data.language_conversations import build_human_conversations
from training_data.language_split import split_language_conversations
from training_data.language_uncertainty import filter_uncertain_conversations
from training_data.validation import (
    validate_knowledge_dataset,
    validate_language_dataset,
    validate_training_data,
)


def _split_paths(root: Path) -> dict[str, Path]:
    return {name: root / f"{name}.jsonl" for name in ("train", "validation", "test")}


def main() -> int:
    """Valida JSONL, traçabilitat, cobertura i absència de fuites entre splits."""

    repository_root = Path(__file__).resolve().parents[2]
    training_root = repository_root / "training-data"
    inventory = scan_tree(repository_root / "docs")

    knowledge_root = training_root / "knowledge"
    knowledge_ledger = extract_knowledge(inventory)
    raw_knowledge = (
        *build_knowledge_candidates(knowledge_ledger),
        *build_relation_candidates(knowledge_ledger),
    )
    knowledge_classification = classify_knowledge_candidates(raw_knowledge, knowledge_ledger)
    knowledge_deduplication = deduplicate_knowledge_candidates(
        knowledge_classification.eligible_candidates
    )
    knowledge_split = split_knowledge_candidates(knowledge_deduplication.candidates)
    knowledge_coverage = build_knowledge_coverage(knowledge_ledger, knowledge_classification)
    knowledge_report = validate_knowledge_dataset(
        _split_paths(knowledge_root / "output"),
        knowledge_split,
        knowledge_ledger,
        knowledge_coverage,
    )

    language_root = training_root / "language"
    language_ledger = extract_language(inventory)
    language_candidates = build_human_conversations(language_ledger)
    filtered_language = filter_uncertain_conversations(language_ledger, language_candidates)
    language_split = split_language_conversations(filtered_language.accepted)
    language_report = validate_language_dataset(
        _split_paths(language_root / "output"), language_split, language_ledger
    )
    report = validate_training_data(
        knowledge_report,
        language_report,
        knowledge_coverage=knowledge_coverage.total_coverage,
    )

    report_path = knowledge_root / "reports" / "validation.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = report_path.with_suffix(".json.tmp")
    temporary.write_text(
        json.dumps(asdict(report), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(report_path)

    print(f"Training-data validation: {'PASS' if report.valid else 'FAIL'}.")
    for dataset_report in (report.knowledge, report.language):
        counts = ", ".join(
            f"{name}={count}" for name, count in dataset_report.record_counts.items()
        )
        print(
            f"{dataset_report.dataset}: {'PASS' if dataset_report.valid else 'FAIL'} "
            f"({counts}; {len(dataset_report.issues)} issues)."
        )
        for issue in dataset_report.issues[:20]:
            print(f"  {issue.code}: {issue.message}")
        if len(dataset_report.issues) > 20:
            print(f"  ... {len(dataset_report.issues) - 20} further issues recorded in the report.")
    return 0 if report.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
