"""Golden + unit tests for the Diari de Sessions parser (PLAN M1.04)."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from maia.schemas import License, Registre, Source
from maia.scraping.diari import (
    clean_oral,
    parse_session,
    read_whitelist,
    split_interventions,
)

FIXTURE = (Path(__file__).parent / "fixtures" / "diari_session_sample.txt").read_text(
    encoding="utf-8"
)
SESSION_URL = "https://www.consellgeneral.ad/ca/arxiu/diari/2024-03-15"
STAMP = datetime(2026, 8, 1, tzinfo=UTC)
WHITELIST = {"Maria Font", "Joan Martí"}


@pytest.mark.unit
def test_split_interventions_finds_all_speakers() -> None:
    turns = split_interventions(FIXTURE)
    assert [t.speaker for t in turns] == [
        "Síndic General",
        "Maria Font",
        "Joan Martí",
        "Pere Nadal",
    ]


@pytest.mark.unit
def test_clean_oral_removes_stage_directions() -> None:
    assert clean_oral("Bon dia. (Aplaudiments) Gràcies.") == "Bon dia. Gràcies."
    assert clean_oral("Text [inaudible] final.") == "Text final."


@pytest.mark.unit
def test_parse_session_keeps_only_whitelisted_and_long_enough() -> None:
    docs = parse_session(FIXTURE, whitelist=WHITELIST, session_url=SESSION_URL, fetched_at=STAMP)
    # Síndic (not whitelisted), Pere (not whitelisted + too short), and Joan (too short
    # after cleaning) are excluded → only Maria Font remains.
    assert len(docs) == 1
    doc = docs[0]
    assert doc.speaker == "Maria Font"
    assert doc.source is Source.CONSELL_DIARI_SESSIONS
    assert doc.registre is Registre.ANDORRA_PARLAT
    assert doc.license is License.PUBLIC_OFFICIAL
    assert str(doc.url) == SESSION_URL
    assert doc.fetched_at == STAMP
    assert "Aplaudiments" not in doc.text  # stage direction cleaned


@pytest.mark.unit
def test_parse_session_low_min_chars_includes_short_turns() -> None:
    docs = parse_session(
        FIXTURE,
        whitelist=WHITELIST,
        session_url=SESSION_URL,
        fetched_at=STAMP,
        min_chars=10,
    )
    speakers = {d.speaker for d in docs}
    assert speakers == {"Maria Font", "Joan Martí"}
    joan = next(d for d in docs if d.speaker == "Joan Martí")
    assert "inaudible" not in joan.text


@pytest.mark.unit
def test_parse_session_excludes_non_whitelisted_even_if_long() -> None:
    # Síndic's intervention is long but he is not on the whitelist.
    docs = parse_session(
        FIXTURE, whitelist={"Maria Font"}, session_url=SESSION_URL, fetched_at=STAMP
    )
    assert {d.speaker for d in docs} == {"Maria Font"}


@pytest.mark.unit
def test_whitelist_matching_is_whitespace_and_case_insensitive() -> None:
    docs = parse_session(
        FIXTURE,
        whitelist={"  maria   font "},
        session_url=SESSION_URL,
        fetched_at=STAMP,
    )
    assert {d.speaker for d in docs} == {"Maria Font"}


@pytest.mark.unit
def test_read_whitelist_ignores_comments_and_blanks(tmp_path: Path) -> None:
    path = tmp_path / "whitelist.txt"
    path.write_text(
        "# Parliamentarian whitelist (PO input, M1.05)\n"
        "Maria Font\n"
        "\n"
        "Joan Martí\n"
        "   # trailing comment\n",
        encoding="utf-8",
    )
    assert read_whitelist(path) == {"Maria Font", "Joan Martí"}


@pytest.mark.unit
def test_empty_transcript_yields_no_docs() -> None:
    assert parse_session("", whitelist=WHITELIST, session_url=SESSION_URL) == []
