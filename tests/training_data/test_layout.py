from __future__ import annotations

import subprocess
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
TRAINING_DATA = REPOSITORY_ROOT / "training-data"


def test_both_dataset_areas_have_the_scaffold() -> None:
    required = (
        "README.md",
        "Maia Knowledge/README.md",
        "Maia Knowledge/scripts/README.md",
        "Maia Knowledge/work/.gitkeep",
        "Maia Knowledge/output/.gitkeep",
        "Maia Knowledge/reports/.gitkeep",
        "Maia Language/README.md",
        "Maia Language/scripts/README.md",
        "Maia Language/work/.gitkeep",
        "Maia Language/output/.gitkeep",
        "Maia Language/reports/.gitkeep",
        ".gitignore",
    )

    missing = [path for path in required if not (TRAINING_DATA / path).is_file()]

    assert not missing, f"Missing training-data scaffold files: {missing}"


def test_generated_files_are_ignored_but_scaffold_is_trackable() -> None:
    ignored = (
        "training-data/Maia Knowledge/output/train.jsonl",
        "training-data/Maia Language/work/intermediate.jsonl",
        "training-data/Maia Language/reports/summary.json",
    )
    trackable = (
        "training-data/Maia Knowledge/output/.gitkeep",
        "training-data/Maia Language/work/.gitkeep",
        "training-data/Maia Knowledge/scripts/README.md",
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
