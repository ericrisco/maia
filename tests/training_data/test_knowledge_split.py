from __future__ import annotations

import json
from pathlib import Path

import pytest

from training_data.knowledge_generate import ConversationCandidate
from training_data.knowledge_split import (
    SplitConfig,
    split_knowledge_candidates,
    write_knowledge_splits,
)


def _candidates() -> tuple[ConversationCandidate, ...]:
    records = [
        ConversationCandidate(
            family_id=f"family-{index}",
            evidence_ids=(f"evidence-{index}",),
            user=f"Què és el concepte {index}?",
            assistant=f"El concepte {index} és una prova.",
            review_status="needs_review",
        )
        for index in range(37)
    ]
    records.extend(
        ConversationCandidate(
            family_id="shared-family",
            evidence_ids=(f"shared-evidence-{index}",),
            user=f"Variant {index}?",
            assistant=f"Resposta {index}.",
            review_status="needs_review",
        )
        for index in range(3)
    )
    return tuple(records)


def test_grouped_split_is_deterministic_complete_and_jsonl_valid(tmp_path: Path) -> None:
    candidates = _candidates()
    config = SplitConfig()

    first = split_knowledge_candidates(candidates, config=config)
    second = split_knowledge_candidates(candidates, config=config)

    assert first.manifest.assignments == second.manifest.assignments
    assert first.manifest.assignments["shared-family"] in {"train", "validation", "test"}
    assert sum(first.manifest.actual_counts.values()) == len(candidates)
    assert first.manifest.target_ratios == {"train": 0.8, "validation": 0.1, "test": 0.1}
    split_sets = {"train": first.train, "validation": first.validation, "test": first.test}
    shared_splits = {
        name
        for name, records in split_sets.items()
        if any(r.family_id == "shared-family" for r in records)
    }
    assert shared_splits == {first.manifest.assignments["shared-family"]}

    paths = write_knowledge_splits(first, output=tmp_path / "output", work=tmp_path / "work")
    assert set(paths) == {"train", "validation", "test"}
    for name, path in paths.items():
        lines = path.read_text(encoding="utf-8").splitlines()
        assert len(lines) == first.manifest.actual_counts[name]
        assert all(set(json.loads(line)) == {"messages"} for line in lines)
        assert all(
            [message["role"] for message in json.loads(line)["messages"]] == ["user", "assistant"]
            for line in lines
        )
    manifest = json.loads((tmp_path / "work/split-manifest.json").read_text(encoding="utf-8"))
    assert manifest["seed"] == "maia-training-data-v1"
    assert manifest["actual_counts"] == first.manifest.actual_counts


def test_split_config_rejects_invalid_ratios() -> None:
    with pytest.raises(ValueError, match="sum to 1"):
        SplitConfig(target_ratios={"train": 0.7, "validation": 0.2, "test": 0.2})
