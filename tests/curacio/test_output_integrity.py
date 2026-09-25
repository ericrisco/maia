"""Tests the checked-in generated corpus for forbidden training-text material."""

import csv
import json
import re
from pathlib import Path

from cervell.model import load_corpus

CORPUS = Path(__file__).parents[2] / "corpus"
FORBIDDEN_TEXT = re.compile(r"\*\*|__|~~|(?:docs/)?raw/|\[\d{2}:\d{2}:\d{2}")
WORK_SENTENCE = re.compile(
    r"(?im)^\s*(?:el corpus|aquest corpus|tancat el|tota la font|el que sí que pot fer)\b"
)


def test_usable_chunks_have_no_editorial_marks_local_paths_or_timestamps() -> None:
    with (CORPUS / "inventari.tsv").open(encoding="utf-8", newline="") as source:
        rows = list(csv.DictReader(source, delimiter="\t"))
    expected = {
        row["id"]
        for row in rows
        if row["tipus"] == "chunk"
        and row["decisio"] != "excloure"
        and set(row["usos"].split(",")) & {"coneixement", "raft-context", "llengua"}
    }
    found: set[str] = set()
    for path in (CORPUS / "chunks").rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for match in re.finditer(
            r"<!-- chunk: ([^ ]+) -->\n(.*?)(?=\n\n<!-- chunk: |\Z)", text, re.S
        ):
            identifier, body = match.groups()
            found.add(identifier)
            assert FORBIDDEN_TEXT.search(body) is None, identifier
            assert WORK_SENTENCE.search(body) is None, identifier
    assert found == expected - {
        row["id"] for row in rows if row["tipus"] == "chunk" and row["usos"] == "llengua"
    }


def test_speech_segments_have_no_timestamp_in_transcribed_text() -> None:
    for path in (CORPUS / "llengua" / "parla").glob("*.md"):
        text = path.read_text(encoding="utf-8")
        for match in re.finditer(r"<!-- seg: [^>]+ -->\n(.*?)(?=\n\n<!-- seg: |\Z)", text, re.S):
            assert re.search(r"\[\d{2}:\d{2}:\d{2}", match.group(1)) is None, path.name


def test_known_source_errors_are_recorded_as_corrections() -> None:
    with (CORPUS / "correccions.tsv").open(encoding="utf-8", newline="") as source:
        rows = list(csv.DictReader(source, delimiter="\t"))
    corrections = {(row["doc_id"], row["camp"]): row for row in rows}

    for doc_id in (
        "temes/historia/segle-xix/els-carlins-i-el-consell-1838-1839",
        "temes/institucions/justicia/el-consell-encarrega-un-codi-de-lleis-1860",
    ):
        assert corrections[doc_id, "apte_llengua"]["correccio"] == "false"
    assert corrections["temes/persones/esteve-albert-i-corp", "font"]["correccio"] == "pendent"
    assert ("temes/historia/antic-regim/la-questia", "title") in corrections
    assert ("temes/institucions/coprincipat/la-questia", "title") in corrections


def test_snapshot_and_inventory_cover_every_source_with_a_decision_and_reason() -> None:
    manifest = [
        json.loads(line)
        for line in (CORPUS / "manifest.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    source_docs = load_corpus(Path(__file__).parents[2] / "docs").docs
    with (CORPUS / "inventari.tsv").open(encoding="utf-8", newline="") as source:
        rows = list(csv.DictReader(source, delimiter="\t"))

    assert len(manifest) == len(source_docs) == 1388
    assert len({row["doc_id"] for row in manifest}) == 1388
    assert all(row["decisio"] and row["motiu"] for row in rows)
