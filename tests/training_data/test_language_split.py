from __future__ import annotations

import json
from pathlib import Path

from training_data.knowledge_split import SplitConfig
from training_data.language_conversations import SpeechConversationCandidate
from training_data.language_split import split_language_conversations, write_language_splits


def _candidate(
    family_id: str,
    piece_id: str,
    conversation_id: str,
    speaker_id: str | None,
) -> SpeechConversationCandidate:
    return SpeechConversationCandidate(
        family_id=family_id,
        source_path=f"parla/oral/{piece_id}.md",
        piece_id=piece_id,
        conversation_id=conversation_id,
        speaker_id=speaker_id,
        user=f"Pregunta {family_id}?",
        assistant=f"Resposta {family_id}.",
        user_start=0,
        user_end=1,
        assistant_start=1,
        assistant_end=2,
        normalization_status="verbatim",
    )


def test_splits_are_deterministic_and_never_divide_piece_or_speaker_groups(
    tmp_path: Path,
) -> None:
    candidates = tuple(
        _candidate(f"turn-{index}", piece, conversation, speaker)
        for index, (piece, conversation, speaker) in enumerate(
            [
                ("piece-a", "conversation-a", "speaker-1"),
                ("piece-a", "conversation-b", "speaker-1"),
                ("piece-b", "conversation-c", "speaker-1"),
                ("piece-c", "conversation-d", "speaker-2"),
                ("piece-d", "conversation-e", None),
            ]
        )
    )
    config = SplitConfig()

    first = split_language_conversations(candidates, config=config)
    second = split_language_conversations(candidates, config=config)

    assert first.manifest.assignments == second.manifest.assignments
    speaker_group_splits = {
        first.manifest.candidate_splits[candidate.family_id] for candidate in candidates[:3]
    }
    assert len(speaker_group_splits) == 1
    assert sum(first.manifest.actual_counts.values()) == len(candidates)
    paths = write_language_splits(first, output=tmp_path / "output", work=tmp_path / "work")
    for name, path in paths.items():
        records = [json.loads(line) for line in path.read_text().splitlines()]
        assert len(records) == first.manifest.actual_counts[name]
        assert all(set(record) == {"messages"} for record in records)
    manifest = json.loads((tmp_path / "work/split-manifest.json").read_text())
    assert manifest["seed"] == "maia-training-data-v1"


def test_empty_language_dataset_writes_three_valid_empty_splits(tmp_path: Path) -> None:
    result = split_language_conversations((), config=SplitConfig())

    paths = write_language_splits(result, output=tmp_path / "output", work=tmp_path / "work")

    assert set(paths) == {"train", "validation", "test"}
    assert all(path.read_text() == "" for path in paths.values())
    assert result.manifest.actual_counts == {"train": 0, "validation": 0, "test": 0}
