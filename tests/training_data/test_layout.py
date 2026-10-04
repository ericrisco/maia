from __future__ import annotations

import subprocess
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
TRAINING_DATA = REPOSITORY_ROOT / "training-data"


def test_both_dataset_areas_have_the_scaffold() -> None:
    required = (
        "README.md",
        "knowledge/README.md",
        "knowledge/scripts/README.md",
        "knowledge/work/.gitkeep",
        "knowledge/output/.gitkeep",
        "knowledge/reports/.gitkeep",
        "language/README.md",
        "language/scripts/README.md",
        "language/work/.gitkeep",
        "language/output/.gitkeep",
        "language/reports/.gitkeep",
        ".gitignore",
    )

    missing = [path for path in required if not (TRAINING_DATA / path).is_file()]

    assert not missing, f"Missing training-data scaffold files: {missing}"


def test_generated_files_are_ignored_but_scaffold_is_trackable() -> None:
    ignored = (
        "training-data/knowledge/output/train.jsonl",
        "training-data/language/work/intermediate.jsonl",
        "training-data/language/reports/summary.json",
    )
    trackable = (
        "training-data/knowledge/output/.gitkeep",
        "training-data/language/work/.gitkeep",
        "training-data/knowledge/scripts/README.md",
    )

    for relative_path in ignored:
        result = subprocess.run(
            ["git", "check-ignore", "--no-index", "--quiet", relative_path],
            cwd=REPOSITORY_ROOT,
            check=False,
        )
        assert result.returncode == 0, f"Expected generated path to be ignored: {relative_path}"

    for relative_path in trackable:
        result = subprocess.run(
            ["git", "check-ignore", "--no-index", "--quiet", relative_path],
            cwd=REPOSITORY_ROOT,
            check=False,
        )
        assert result.returncode == 1, (
            f"Expected scaffold path to remain trackable: {relative_path}"
        )
