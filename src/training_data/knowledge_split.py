"""Assignació determinista de famílies Knowledge i escriptura dels tres splits."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

from training_data.knowledge_generate import ConversationCandidate

DEFAULT_SEED = "maia-training-data-v1"
DEFAULT_RATIOS = {"train": 0.8, "validation": 0.1, "test": 0.1}
SPLIT_NAMES = ("train", "validation", "test")


@dataclass(frozen=True, slots=True)
class SplitConfig:
    """Seed i proporcions objectiu del split."""

    seed: str = DEFAULT_SEED
    target_ratios: dict[str, float] = field(default_factory=lambda: DEFAULT_RATIOS.copy())

    def __post_init__(self) -> None:
        if not self.seed:
            raise ValueError("split seed must be non-empty")
        if set(self.target_ratios) != set(SPLIT_NAMES):
            raise ValueError("target ratios must define train, validation and test")
        if any(ratio < 0 or ratio > 1 for ratio in self.target_ratios.values()):
            raise ValueError("target ratios must be between 0 and 1")
        if abs(sum(self.target_ratios.values()) - 1.0) > 1e-9:
            raise ValueError("target ratios must sum to 1")


@dataclass(frozen=True, slots=True)
class SplitManifest:
    """Reproducible family assignment and actual record volumes."""

    seed: str
    target_ratios: dict[str, float]
    assignments: dict[str, str]
    actual_counts: dict[str, int]
    family_counts: dict[str, int]


@dataclass(frozen=True, slots=True)
class KnowledgeSplit:
    """Three record sets and their split manifest."""

    train: tuple[ConversationCandidate, ...]
    validation: tuple[ConversationCandidate, ...]
    test: tuple[ConversationCandidate, ...]
    manifest: SplitManifest


def split_knowledge_candidates(
    candidates: tuple[ConversationCandidate, ...], *, config: SplitConfig | None = None
) -> KnowledgeSplit:
    """Distributes indivisible candidate families close to configured ratios."""

    selected = config or SplitConfig()
    grouped: dict[str, list[ConversationCandidate]] = {}
    for candidate in candidates:
        if not candidate.family_id:
            raise ValueError("every candidate must have a non-empty family_id")
        grouped.setdefault(candidate.family_id, []).append(candidate)

    total = len(candidates)
    targets = {name: total * selected.target_ratios[name] for name in SPLIT_NAMES}
    ordered_groups = sorted(
        grouped,
        key=lambda family_id: hashlib.sha256(f"{selected.seed}\0{family_id}".encode()).digest(),
    )
    actual = {name: 0 for name in SPLIT_NAMES}
    assignments: dict[str, str] = {}
    records: dict[str, list[ConversationCandidate]] = {name: [] for name in SPLIT_NAMES}
    family_counts = {name: 0 for name in SPLIT_NAMES}

    for family_id in ordered_groups:
        group = grouped[family_id]
        available = [name for name in SPLIT_NAMES if selected.target_ratios[name] > 0]
        split_name = max(
            available,
            key=lambda name: (
                (targets[name] - actual[name]) / targets[name],
                -SPLIT_NAMES.index(name),
            ),
        )
        assignments[family_id] = split_name
        actual[split_name] += len(group)
        family_counts[split_name] += 1
        records[split_name].extend(group)

    manifest = SplitManifest(
        seed=selected.seed,
        target_ratios=selected.target_ratios.copy(),
        assignments=assignments,
        actual_counts=actual,
        family_counts=family_counts,
    )
    return KnowledgeSplit(
        train=tuple(records["train"]),
        validation=tuple(records["validation"]),
        test=tuple(records["test"]),
        manifest=manifest,
    )


def write_knowledge_splits(split: KnowledgeSplit, *, output: Path, work: Path) -> dict[str, Path]:
    """Escriu JSONL públics només per a exemples revisats i no buits."""

    all_candidates = (*split.train, *split.validation, *split.test)
    if not all_candidates:
        raise ValueError("cannot write empty Knowledge splits")
    if any(candidate.review_status != "human_reviewed" for candidate in all_candidates):
        raise ValueError("only human-reviewed Knowledge conversations can be exported")

    records_by_name = {
        "train": split.train,
        "validation": split.validation,
        "test": split.test,
    }
    paths: dict[str, Path] = {}
    for name, records in records_by_name.items():
        path = output / f"{name}.jsonl"
        content = "".join(
            json.dumps(candidate.to_public_record(), ensure_ascii=False, separators=(",", ":"))
            + "\n"
            for candidate in records
        )
        _atomic_write(path, content)
        paths[name] = path

    work.mkdir(parents=True, exist_ok=True)
    manifest_path = work / "split-manifest.json"
    _atomic_write(
        manifest_path,
        json.dumps(asdict(split.manifest), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    )
    return paths


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content, encoding="utf-8", newline="")
    temporary.replace(path)
