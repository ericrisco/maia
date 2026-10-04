"""Splits deterministes de Maia Language sense barrejar peces o parlants."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path

from training_data.knowledge_split import SPLIT_NAMES, SplitConfig
from training_data.language_conversations import SpeechConversationCandidate


@dataclass(frozen=True, slots=True)
class LanguageSplitManifest:
    """Assignació per grup i per candidat, amb els volums reals."""

    seed: str
    target_ratios: dict[str, float]
    assignments: dict[str, str]
    candidate_splits: dict[str, str]
    actual_counts: dict[str, int]
    group_counts: dict[str, int]


@dataclass(frozen=True, slots=True)
class LanguageSplit:
    """Registres de cada split i el seu manifest."""

    train: tuple[SpeechConversationCandidate, ...]
    validation: tuple[SpeechConversationCandidate, ...]
    test: tuple[SpeechConversationCandidate, ...]
    manifest: LanguageSplitManifest


def _group_candidates(
    candidates: tuple[SpeechConversationCandidate, ...],
) -> dict[str, list[SpeechConversationCandidate]]:
    parents = list(range(len(candidates)))

    def find(index: int) -> int:
        while parents[index] != index:
            parents[index] = parents[parents[index]]
            index = parents[index]
        return index

    def union(left: int, right: int) -> None:
        left_root = find(left)
        right_root = find(right)
        if left_root != right_root:
            parents[right_root] = left_root

    owners: dict[str, int] = {}
    seen_family_ids: set[str] = set()
    for index, candidate in enumerate(candidates):
        if not candidate.family_id or not candidate.piece_id:
            raise ValueError("every Language candidate needs family_id and piece_id")
        if candidate.family_id in seen_family_ids:
            raise ValueError(f"duplicate Language candidate family_id: {candidate.family_id}")
        seen_family_ids.add(candidate.family_id)
        candidate_keys = [f"piece:{candidate.piece_id}"]
        if candidate.conversation_id:
            candidate_keys.append(f"conversation:{candidate.conversation_id}")
        if candidate.speaker_id:
            candidate_keys.append(f"speaker:{candidate.speaker_id}")
        for label in candidate_keys:
            if label in owners:
                union(index, owners[label])
            else:
                owners[label] = index

    components: dict[int, list[SpeechConversationCandidate]] = {}
    for index, candidate in enumerate(candidates):
        components.setdefault(find(index), []).append(candidate)

    groups: dict[str, list[SpeechConversationCandidate]] = {}
    for members in components.values():
        labels = {f"piece:{candidate.piece_id}" for candidate in members}
        labels.update(
            f"conversation:{candidate.conversation_id}"
            for candidate in members
            if candidate.conversation_id
        )
        labels.update(
            f"speaker:{candidate.speaker_id}" for candidate in members if candidate.speaker_id
        )
        digest = hashlib.sha256("\0".join(sorted(labels)).encode()).hexdigest()[:16]
        groups[f"language:{digest}"] = members
    return groups


def split_language_conversations(
    candidates: tuple[SpeechConversationCandidate, ...], *, config: SplitConfig | None = None
) -> LanguageSplit:
    """Assigna famílies a splits amb seed fixa i cap fuga entre grups."""

    selected = config or SplitConfig()
    groups = _group_candidates(candidates)
    total = len(candidates)
    targets = {name: total * selected.target_ratios[name] for name in SPLIT_NAMES}
    ordered = sorted(
        groups,
        key=lambda group_id: hashlib.sha256(f"{selected.seed}\0{group_id}".encode()).digest(),
    )
    assignments: dict[str, str] = {}
    actual = {name: 0 for name in SPLIT_NAMES}
    group_counts = {name: 0 for name in SPLIT_NAMES}
    candidate_splits: dict[str, str] = {}
    records: dict[str, list[SpeechConversationCandidate]] = {name: [] for name in SPLIT_NAMES}
    for group_id in ordered:
        group = groups[group_id]
        available = [name for name in SPLIT_NAMES if selected.target_ratios[name] > 0]
        split_name = max(
            available,
            key=lambda name: (
                (targets[name] - actual[name]) / targets[name],
                -SPLIT_NAMES.index(name),
            ),
        )
        assignments[group_id] = split_name
        actual[split_name] += len(group)
        group_counts[split_name] += 1
        records[split_name].extend(group)
        for candidate in group:
            candidate_splits[candidate.family_id] = split_name

    manifest = LanguageSplitManifest(
        seed=selected.seed,
        target_ratios=selected.target_ratios.copy(),
        assignments=assignments,
        candidate_splits=candidate_splits,
        actual_counts=actual,
        group_counts=group_counts,
    )
    return LanguageSplit(
        train=tuple(records["train"]),
        validation=tuple(records["validation"]),
        test=tuple(records["test"]),
        manifest=manifest,
    )


def write_language_splits(split: LanguageSplit, *, output: Path, work: Path) -> dict[str, Path]:
    """Escriu els tres JSONL simples i el manifest local de grups."""

    records_by_name = {
        "train": split.train,
        "validation": split.validation,
        "test": split.test,
    }
    paths: dict[str, Path] = {}
    for name, records in records_by_name.items():
        path = output / f"{name}.jsonl"
        content = "".join(
            json.dumps(record.to_public_record(), ensure_ascii=False, separators=(",", ":")) + "\n"
            for record in records
        )
        _atomic_write(path, content)
        paths[name] = path
    work.mkdir(parents=True, exist_ok=True)
    _atomic_write(
        work / "split-manifest.json",
        json.dumps(asdict(split.manifest), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    )
    return paths


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content, encoding="utf-8", newline="")
    temporary.replace(path)
