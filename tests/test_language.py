"""Unit tests for the Catalan language filter (PLAN M1.08)."""

from __future__ import annotations

import pytest

from maia.corpus.language import _ALL_PROFILES, _DISCRIMINATIVE, detect_language, is_catalan

# The same passage in five languages — the realistic confusion set for Andorran sources.
SAMPLES = {
    "ca": (
        "Andorra és un Estat independent, de Dret, Democràtic i Social. La seva denominació "
        "oficial és Principat d'Andorra. La Constitució proclama com a principis inspiradors "
        "de l'acció de l'Estat andorrà el respecte i la promoció de la llibertat, amb la "
        "igualtat i la justícia. Això és el que estableix aquest article, però també cal "
        "tenir en compte les altres normes."
    ),
    "es": (
        "Andorra es un Estado independiente, de Derecho, Democrático y Social. Su "
        "denominación oficial es Principado de Andorra. La Constitución proclama como "
        "principios inspiradores de la acción del Estado andorrano el respeto y la promoción "
        "de la libertad, con la igualdad y la justicia. Esto es lo que establece este "
        "artículo, pero también hay que tener en cuenta las otras normas."
    ),
    "fr": (
        "L'Andorre est un État indépendant, de droit, démocratique et social. Sa dénomination "
        "officielle est Principauté d'Andorre. La Constitution proclame comme principes "
        "inspirateurs de l'action de l'État andorran le respect et la promotion de la "
        "liberté, avec l'égalité et la justice. Voilà ce que cet article établit, mais il "
        "faut aussi tenir compte des autres normes."
    ),
    "pt": (
        "Andorra é um Estado independente, de Direito, Democrático e Social. A sua "
        "denominação oficial é Principado de Andorra. A Constituição proclama como "
        "princípios inspiradores da ação do Estado andorrano o respeito e a promoção da "
        "liberdade, com a igualdade e a justiça. Isto é o que este artigo estabelece, mas "
        "também há que ter em conta as outras normas."
    ),
    "en": (
        "Andorra is an independent, democratic and social State governed by the rule of law. "
        "Its official name is the Principality of Andorra. The Constitution proclaims respect "
        "for and promotion of liberty, equality and justice as the guiding principles of the "
        "action of the Andorran State. That is what this article establishes, but the other "
        "rules must also be taken into account."
    ),
}


@pytest.mark.unit
@pytest.mark.parametrize("expected", sorted(SAMPLES))
def test_each_language_is_identified(expected: str) -> None:
    verdict = detect_language(SAMPLES[expected])
    assert verdict.language == expected
    assert verdict.confidence >= 0.5


@pytest.mark.unit
def test_only_catalan_passes_the_filter() -> None:
    assert is_catalan(SAMPLES["ca"])
    for lang, text in SAMPLES.items():
        if lang != "ca":
            assert not is_catalan(text), lang


@pytest.mark.unit
def test_profiles_are_discriminative_by_construction() -> None:
    # The guarantee the module rests on: no word counts for two languages at once.
    for lang, words in _DISCRIMINATIVE.items():
        for other, other_words in _DISCRIMINATIVE.items():
            if other != lang:
                assert not words & other_words, f"{lang}/{other}"


@pytest.mark.unit
def test_shared_words_are_actually_removed() -> None:
    # "del" is Catalan and Spanish; "que" is in four of the five lists; "les" is Catalan and
    # French. Each must be scored for nobody.
    for shared in ("del", "que", "les", "sobre", "entre", "cada"):
        assert not any(shared in words for words in _DISCRIMINATIVE.values()), shared
    # …and each really was present in the raw lists, so the test proves removal, not absence.
    for shared in ("del", "que", "les"):
        assert sum(shared in words for words in _ALL_PROFILES.values()) >= 2, shared


@pytest.mark.unit
def test_ela_geminada_and_elisions_reinforce_catalan() -> None:
    # Short text whose only strong signal is Catalan orthography.
    text = "La col·lecció de l'Arxiu s'ha instal·lat a l'edifici del Comú d'Encamp."
    assert detect_language(text).language == "ca"


@pytest.mark.unit
def test_a_bilingual_page_is_rejected_on_foreign_share() -> None:
    # Catalan still *wins* this 50/50 mix — a mixture tilts towards the richer profile, not
    # towards neither — so the amount of Spanish is the only signal that rejects it.
    mixed = SAMPLES["ca"] + " " + SAMPLES["es"]
    verdict = detect_language(mixed)
    assert verdict.language == "ca"
    assert verdict.runner_up == "es"
    assert verdict.runner_up_share > 0.25
    assert not is_catalan(mixed)


@pytest.mark.unit
def test_text_with_no_function_words_is_undetermined() -> None:
    verdict = detect_language("Canillo Encamp Ordino Massana Escaldes Engordany")
    assert verdict.language == "und"
    assert verdict.confidence == 0.0
    assert not is_catalan("Canillo Encamp Ordino")


@pytest.mark.unit
def test_empty_and_numeric_text_is_undetermined() -> None:
    for text in ("", "   ", "123 456 7.89", "— · —"):
        assert detect_language(text).language == "und"


@pytest.mark.unit
def test_thresholds_are_adjustable() -> None:
    mixed = SAMPLES["ca"] + " " + SAMPLES["es"]
    assert not is_catalan(mixed)
    # A caller willing to accept mixed text can say so explicitly.
    assert is_catalan(mixed, min_confidence=0.5, max_foreign_share=1.0)


@pytest.mark.unit
def test_margin_is_confidence_minus_runner_up() -> None:
    verdict = detect_language(SAMPLES["ca"] + " " + SAMPLES["es"])
    assert verdict.margin == pytest.approx(verdict.confidence - verdict.runner_up_share)


@pytest.mark.unit
def test_a_short_spanish_quote_inside_a_catalan_article_is_tolerated() -> None:
    # One quoted sentence should not cost us the whole document.
    text = SAMPLES["ca"] + ' El president va dir: "esto es lo que hay".'
    assert is_catalan(text)


@pytest.mark.unit
def test_detection_is_case_insensitive() -> None:
    assert detect_language(SAMPLES["ca"].upper()).language == "ca"
