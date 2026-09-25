"""Reprodueix les sortides canòniques dels quatre exemples de curació."""

from __future__ import annotations

import csv
import re
import shutil
from io import StringIO
from pathlib import Path

import pytest

from cervell.cli import main

FIXTURES = Path(__file__).parents[1] / "fixtures" / "curacio"
EXEMPLES = sorted(path for path in FIXTURES.iterdir() if path.is_dir())


@pytest.mark.parametrize("exemple", EXEMPLES, ids=lambda path: path.name)
def test_exemple_daurat_es_reprodueix_byte_a_byte(exemple: Path, tmp_path: Path) -> None:
    """Les peces curades han de coincidir exactament amb els oracles versionats."""
    expected_inventory = list(
        csv.reader(
            StringIO((exemple / "inventari.tsv").read_text(encoding="utf-8")), delimiter="\t"
        )
    )
    doc_id = expected_inventory[1][0].split("#", maxsplit=1)[0]
    docs = tmp_path / "docs"
    source = docs / f"{doc_id}.md"
    source.parent.mkdir(parents=True)
    shutil.copyfile(exemple / "entrada.md", source)
    font_match = re.search(r"^font:\s*(\S+)\s*$", source.read_text(encoding="utf-8"), re.M)
    assert font_match is not None
    font_id = font_match.group(1)
    font_source = Path(__file__).parents[2] / "docs" / "fonts" / f"{font_id}.md"
    font_target = docs / "fonts" / font_source.name
    font_target.parent.mkdir(parents=True)
    shutil.copyfile(font_source, font_target)
    families_source = Path(__file__).parents[2] / "curacio" / "decisions" / "families.tsv"
    families_target = tmp_path / "curacio" / "decisions" / "families.tsv"
    families_target.parent.mkdir(parents=True)
    shutil.copyfile(families_source, families_target)
    people_source = Path(__file__).parents[2] / "curacio" / "decisions" / "persones-publiques.tsv"
    people_target = tmp_path / "curacio" / "decisions" / "persones-publiques.tsv"
    shutil.copyfile(people_source, people_target)
    out = tmp_path / "corpus"

    assert main(["cura", "tot", str(docs), "--out", str(out)]) == 0

    expected_files = sorted((exemple / "sortida").rglob("*.md"))
    assert expected_files
    for expected in expected_files:
        relative = expected.relative_to(exemple / "sortida")
        assert (out / relative).read_bytes() == expected.read_bytes()

    generated_inventory = list(
        csv.reader(StringIO((out / "inventari.tsv").read_text(encoding="utf-8")), delimiter="\t")
    )
    expected_header = expected_inventory[0]
    assert generated_inventory[0][: len(expected_header)] == expected_header
    rows_by_id = {row[0]: row for row in generated_inventory[1:]}
    for expected_row in expected_inventory[1:]:
        actual_row = rows_by_id[expected_row[0]]
        assert actual_row[: len(expected_row)] == expected_row
