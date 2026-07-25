"""Unit tests for text normalization and the boilerplate filter (PLAN M1.08)."""

from __future__ import annotations

import unicodedata

import pytest

from maia.corpus.clean import assess, boilerplate_score, clean_text

PROSE = (
    "Les falles són una tradició molt antiga que se celebra a diverses parròquies del "
    "Principat. Cada any, quan arriba el solstici d'estiu, els fallaires baixen de la "
    "muntanya amb les falles enceses i il·luminen el poble sencer durant tota la nit."
)


@pytest.mark.unit
def test_nfc_normalization() -> None:
    decomposed = unicodedata.normalize("NFD", "Andorra la Vella és a l'Urgell")
    assert decomposed != "Andorra la Vella és a l'Urgell"
    assert clean_text(decomposed) == "Andorra la Vella és a l'Urgell"


@pytest.mark.unit
def test_invisible_characters_are_removed() -> None:
    # A zero-width space survives NFC and is not matched by \s, so it would make two
    # identical pages hash differently and defeat dedup entirely.
    assert clean_text("Andorra\u200bés\u00adun\ufeffestat") == "Andorraésunestat"


@pytest.mark.unit
def test_non_breaking_space_becomes_a_normal_space() -> None:
    assert clean_text("Andorra\u00a0la\u00a0Vella") == "Andorra la Vella"


@pytest.mark.unit
def test_curly_quotes_and_ligatures_are_folded() -> None:
    assert clean_text("l\u2019aigua i \u201cel bosc\u201d") == 'l\'aigua i "el bosc"'
    assert clean_text("de\ufb01nitiu") == "definitiu"


@pytest.mark.unit
def test_guillemets_survive_because_legal_text_uses_them() -> None:
    assert clean_text("l'article diu «vigent a Andorra»") == "l'article diu «vigent a Andorra»"


@pytest.mark.unit
def test_control_characters_and_crlf_are_cleaned() -> None:
    assert clean_text("línia u\r\nlínia dos\x00\x07") == "línia u\nlínia dos"


@pytest.mark.unit
def test_whitespace_is_collapsed_but_paragraphs_survive() -> None:
    assert clean_text("un  \t dos\n\n\n\ntres\n  ") == "un dos\n\ntres"


@pytest.mark.unit
def test_normalization_is_idempotent() -> None:
    once = clean_text("Andorra\u200b  la\u00a0Vella\r\n\n\n\nés  aquí ")
    assert clean_text(once) == once


@pytest.mark.unit
def test_prose_scores_low_and_a_menu_scores_high() -> None:
    menu = "\n".join(["Inici", "Notícies", "Contacte", "Inici", "Notícies", "Contacte"] * 4)
    assert boilerplate_score(PROSE) < 0.3
    assert boilerplate_score(menu) > 0.6


@pytest.mark.unit
def test_cookie_wall_is_detected_by_its_phrases() -> None:
    wall = (
        "Aquest lloc web utilitza cookies per millorar l'experiència de navegació. "
        "Si continueu navegant considerem que accepta les cookies. Podeu consultar la "
        "nostra política de cookies en qualsevol moment des del peu de pàgina del web."
    )
    assert boilerplate_score(wall) > 0.6
    assert not assess(wall).keep


@pytest.mark.unit
def test_prose_is_kept() -> None:
    verdict = assess(PROSE)
    assert verdict.keep
    assert verdict.reason == "clean"


@pytest.mark.unit
def test_short_text_is_dropped_by_default() -> None:
    verdict = assess("Massa curt.")
    assert not verdict.keep
    assert "shorter than 200" in verdict.reason


@pytest.mark.unit
def test_min_chars_is_overridable_for_sources_that_need_it() -> None:
    assert assess("El català és la llengua oficial de l'Estat.", min_chars=1).keep


@pytest.mark.unit
def test_symbol_soup_is_dropped_on_letter_ratio() -> None:
    soup = "→ ← ↑ ↓ " * 60
    assert not assess(soup).keep


@pytest.mark.unit
def test_one_phrase_repeated_is_dropped_on_vocabulary() -> None:
    # Long, letter-rich, and no duplicated *lines* — only the unique-word ratio catches it.
    repeated = "el mateix text una vegada i una altra " * 20
    verdict = assess(repeated)
    assert not verdict.keep
    assert "unique-word ratio" in verdict.reason


@pytest.mark.unit
def test_degenerate_input_does_not_divide_by_zero() -> None:
    # Empty and whitespace-only text score as maximally non-prose rather than raising.
    assert boilerplate_score("") == 1.0
    assert boilerplate_score("   \n\n ") == 1.0
    assert not assess("").keep


@pytest.mark.unit
def test_vocabulary_check_survives_text_with_no_words() -> None:
    # A caller that disables the boilerplate score still must not divide by zero on text
    # containing no word characters at all.
    verdict = assess("!!! ??? ... --- ;;; ... !!! ??? ... --- ;;; ..." * 6, max_boilerplate=1.0)
    assert not verdict.keep
    assert "unique-word ratio 0.00" in verdict.reason
