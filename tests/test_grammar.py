"""Tests for the LanguageTool Catalan filter (PLAN M2.05, filter 3)."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4

import pytest

from maia.schemas import DatasetExample, ExampleType, compute_id
from maia.synth.glossary import Glossary
from maia.synth.grammar import (
    DEFAULT_MAX_DENSITY,
    LANGUAGE,
    CatalanCheck,
    GrammarReport,
    Match,
    andorran_terms,
    density,
    is_andorran_lexicon,
    languagetool_service,
    parse_matches,
    render,
    rule_histogram,
    text_of,
)

GROUNDING = compute_id("Un passatge del corpus andorrà.")

GLOSSARY = Glossary.model_validate(
    {
        "version": "test",
        "entries": [
            {"term": "comú", "category": "institucional", "gloss": "Govern de la parròquia."},
            {"term": "cònsol major", "category": "institucional", "gloss": "Presideix el comú."},
            {"term": "borda", "category": "geografic", "gloss": "Construcció de muntanya."},
        ],
    }
)


def example(response: str, *, prompt: str = "Què és el comú?") -> DatasetExample:
    return DatasetExample.model_validate(
        {
            "id": str(uuid4()),
            "messages": [
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": response},
            ],
            "type": ExampleType.QA.value,
            "topic": "institucions/comuns",
            "grounding_ids": [GROUNDING],
            "generator": "claude-opus-5",
            "judge_score": 0.9,
            "split": "train",
        }
    )


def spelling(text: str) -> Match:
    """What LanguageTool reports for an unknown word."""
    return Match(
        rule_id="MORFOLOGIK_RULE_CA_ES",
        category="TYPOS",
        message=f"Possible error d'escriptura: {text}",
        text=text,
    )


def grammatical(text: str = "a on") -> Match:
    """What LanguageTool reports for a construction, not a word."""
    return Match(
        rule_id="CA_SIMPLE_REPLACE",
        category="GRAMMAR",
        message="Expressió incorrecta.",
        text=text,
    )


@dataclass
class ScriptedService:
    """The injected LanguageTool — returns canned matches, records what it was asked."""

    matches: list[Match] = field(default_factory=list)
    seen: list[tuple[str, str]] = field(default_factory=list)

    def check(self, text: str, language: str = LANGUAGE) -> list[Match]:
        self.seen.append((text, language))
        return list(self.matches)


# ─────────────────────────────────────────────────────────────
# The Andorran-lexicon conflict — why this module exists
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_spellcheck_hit_on_a_glossary_term_is_excused() -> None:
    """LanguageTool has no Andorran variant.

    Left alone, filter 3 would systematically delete the examples M2.03 worked to produce, and
    report them as bad Catalan.
    """
    assert is_andorran_lexicon(spelling("comú"), andorran_terms(GLOSSARY))


@pytest.mark.unit
def test_a_grammatical_hit_is_never_excused() -> None:
    """An Andorran word in a sentence with a bad preposition is still a bad preposition."""
    assert not is_andorran_lexicon(grammatical("comú"), andorran_terms(GLOSSARY))


@pytest.mark.unit
def test_a_spellcheck_hit_on_an_ordinary_word_is_not_excused() -> None:
    assert not is_andorran_lexicon(spelling("aixo"), andorran_terms(GLOSSARY))


@pytest.mark.unit
def test_the_exemption_is_accent_insensitive() -> None:
    assert is_andorran_lexicon(spelling("Comu"), andorran_terms(GLOSSARY))


@pytest.mark.unit
def test_a_multiword_glossary_term_is_excused() -> None:
    assert is_andorran_lexicon(spelling("cònsol major"), andorran_terms(GLOSSARY))


@pytest.mark.unit
def test_surrounding_whitespace_does_not_defeat_the_exemption() -> None:
    assert is_andorran_lexicon(spelling("  comú "), andorran_terms(GLOSSARY))


@pytest.mark.unit
def test_without_a_glossary_nothing_is_excused() -> None:
    assert andorran_terms(None) == frozenset()
    assert not is_andorran_lexicon(spelling("comú"), andorran_terms(None))


@pytest.mark.unit
def test_excused_matches_are_counted_not_swallowed() -> None:
    """That count is also the evidence the register injection worked."""
    check = CatalanCheck(ScriptedService([spelling("comú"), spelling("borda")]), glossary=GLOSSARY)
    survivors, report = check.run([example("El comú de la borda gestiona el territori.")])
    assert len(survivors) == 1
    assert report.andorran_lexicon == 2
    assert report.matches == 0
    assert "excused as Andorran lexicon" in render(report)


@pytest.mark.unit
def test_a_morfologik_rule_is_lexical_whatever_its_category() -> None:
    match = Match(rule_id="MORFOLOGIK_RULE_CA_ES", category="MISC", message="", text="comú")
    assert match.is_lexical


@pytest.mark.unit
@pytest.mark.parametrize("category", ["TYPOS", "typos", "CASING", "CAT_ELA_GEMINADA"])
def test_the_lexical_categories_are_case_insensitive(category: str) -> None:
    assert Match(rule_id="X", category=category, message="", text="comú").is_lexical


# ─────────────────────────────────────────────────────────────
# What gets checked
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_only_the_assistant_turns_are_checked() -> None:
    """A clumsy question is a legitimate thing to train on answering.

    Checking both would drop examples for the quality of their questions.
    """
    service = ScriptedService()
    CatalanCheck(service).run([example("La resposta.", prompt="La pregunta mal escrita")])
    assert service.seen == [("La resposta.", LANGUAGE)]


@pytest.mark.unit
def test_the_text_of_a_multiturn_example_joins_every_assistant_turn() -> None:
    multiturn = DatasetExample.model_validate(
        {
            "id": str(uuid4()),
            "messages": [
                {"role": "user", "content": "Primera"},
                {"role": "assistant", "content": "Resposta u"},
                {"role": "user", "content": "Segona"},
                {"role": "assistant", "content": "Resposta dos"},
            ],
            "type": ExampleType.MULTITURN.value,
            "topic": "institucions/comuns",
            "grounding_ids": [GROUNDING],
            "generator": "claude-opus-5",
            "judge_score": 0.9,
            "split": "train",
        }
    )
    assert text_of(multiturn) == "Resposta u\n\nResposta dos"


@pytest.mark.unit
def test_the_configured_language_is_passed_through() -> None:
    service = ScriptedService()
    CatalanCheck(service, language="ca-ES-valencia").run([example("La resposta.")])
    assert service.seen[0][1] == "ca-ES-valencia"


# ─────────────────────────────────────────────────────────────
# Density and dropping
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_density_is_per_thousand_characters() -> None:
    assert density([spelling("a")] * 4, "x" * 1_000) == pytest.approx(4.0)
    assert density([spelling("a")] * 2, "x" * 500) == pytest.approx(4.0)


@pytest.mark.unit
def test_empty_text_has_no_density() -> None:
    assert density([spelling("a")], "") == 0.0


@pytest.mark.unit
def test_a_clean_example_survives() -> None:
    survivors, report = CatalanCheck(ScriptedService()).run([example("Una resposta impecable.")])
    assert len(survivors) == 1
    assert report.dropped == 0
    assert report.checked == 1
    assert "1/1 kept" in render(report)


@pytest.mark.unit
def test_one_typo_in_a_paragraph_is_not_worth_losing_a_grounded_example() -> None:
    long = "El comú gestiona el territori de la parròquia amb competències pròpies. " * 5
    survivors, report = CatalanCheck(ScriptedService([spelling("aixo")])).run([example(long)])
    assert len(survivors) == 1
    assert report.matches == 1


@pytest.mark.unit
def test_an_example_riddled_with_errors_is_dropped_and_named() -> None:
    bad = example("Aixo esta mal escrit.")
    survivors, report = CatalanCheck(ScriptedService([spelling("x")] * 20)).run([bad])
    assert survivors == []
    assert report.dropped == 1
    assert report.worst[0][0] == str(bad.id)
    assert "issues/1k chars" in render(report)


@pytest.mark.unit
def test_the_density_threshold_is_configurable() -> None:
    text = "x" * 1_000
    matches = [spelling("a")] * 5
    strict, _ = CatalanCheck(ScriptedService(matches), max_density=4.0).run([example(text)])
    lax, _ = CatalanCheck(ScriptedService(matches), max_density=9.0).run([example(text)])
    assert strict == [] and len(lax) == 1


@pytest.mark.unit
def test_exactly_the_threshold_survives() -> None:
    """The rule is *exceeds*, so a boundary example is kept."""
    survivors, _ = CatalanCheck(ScriptedService([spelling("a")] * 4)).run([example("x" * 1_000)])
    assert len(survivors) == 1
    assert DEFAULT_MAX_DENSITY == 4.0


@pytest.mark.unit
def test_an_example_with_no_assistant_text_is_kept_unchecked() -> None:
    """Nothing to be wrong about; the schema already refuses an empty message."""
    service = ScriptedService([spelling("x")] * 50)
    survivors, report = CatalanCheck(service).run([example("   ")])
    assert len(survivors) == 1
    assert report.checked == 0
    assert service.seen == []


@pytest.mark.unit
def test_the_worst_offenders_come_first() -> None:
    report = GrammarReport(worst=[("a", 5.0), ("b", 9.0)])
    report.worst.sort(key=lambda item: (-item[1], item[0]))
    assert report.worst == [("b", 9.0), ("a", 5.0)]


@pytest.mark.unit
def test_the_summary_lists_the_top_rules() -> None:
    check = CatalanCheck(ScriptedService([grammatical(), grammatical(), spelling("aixo")]))
    _, report = check.run([example("x" * 5_000)])
    rendered = render(report)
    assert "top rules:" in rendered
    assert "CA_SIMPLE_REPLACE=2" in rendered


@pytest.mark.unit
def test_a_histogram_counts_by_rule() -> None:
    assert rule_histogram([grammatical(), grammatical(), spelling("a")]) == {
        "CA_SIMPLE_REPLACE": 2,
        "MORFOLOGIK_RULE_CA_ES": 1,
    }


@pytest.mark.unit
def test_an_untouched_report_renders_cleanly() -> None:
    rendered = render(GrammarReport())
    assert "0/0 kept" in rendered
    assert "excused" not in rendered
    assert "top rules" not in rendered


# ─────────────────────────────────────────────────────────────
# The live service's response shape
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_languagetool_response_is_parsed() -> None:
    parsed = parse_matches(
        {
            "matches": [
                {
                    "message": "Possible error d'escriptura",
                    "offset": 3,
                    "rule": {"id": "MORFOLOGIK_RULE_CA_ES", "category": {"id": "TYPOS"}},
                    "context": {"text": "El comú gestiona", "offset": 3, "length": 4},
                }
            ]
        }
    )
    assert len(parsed) == 1
    assert parsed[0].rule_id == "MORFOLOGIK_RULE_CA_ES"
    assert parsed[0].category == "TYPOS"
    assert parsed[0].text == "comú"
    assert parsed[0].offset == 3


@pytest.mark.unit
def test_no_matches_parses_to_an_empty_list() -> None:
    assert parse_matches({"matches": []}) == []


@pytest.mark.unit
@pytest.mark.parametrize(
    "payload",
    [
        {"error": "Bad request"},
        {"matches": "none"},
        "not json",
        None,
    ],
)
def test_a_response_that_is_not_languagetool_is_refused(payload: object) -> None:
    """An error body returned as HTTP 200 must not read as "no problems found" — that would turn
    the Catalan check into a no-op reporting success."""
    with pytest.raises(ValueError, match="not a LanguageTool"):
        parse_matches(payload)


@pytest.mark.unit
def test_a_match_that_is_not_an_object_is_refused() -> None:
    with pytest.raises(ValueError, match="match is not an object"):
        parse_matches({"matches": ["nope"]})


@pytest.mark.unit
@pytest.mark.parametrize(
    "raw",
    [
        {},
        {"context": "not an object"},
        {"context": {"text": "El comú", "offset": "3", "length": 4}},
        {"context": {"offset": 3, "length": 4}},
    ],
)
def test_a_match_without_usable_context_parses_with_unknown_fields(raw: dict[str, object]) -> None:
    """Degrade to an unexcusable match rather than crashing: with no flagged text the exemption
    cannot apply, which is the safe direction — the issue still counts."""
    parsed = parse_matches({"matches": [raw]})
    assert parsed[0].text == ""
    assert parsed[0].rule_id == "UNKNOWN"
    assert parsed[0].category == "UNKNOWN"
    assert parsed[0].offset == 0
    assert not is_andorran_lexicon(parsed[0], andorran_terms(GLOSSARY))


@pytest.mark.unit
def test_a_non_object_rule_or_category_falls_back_to_unknown() -> None:
    parsed = parse_matches({"matches": [{"rule": "MORFOLOGIK", "context": {}}]})
    assert parsed[0].rule_id == "UNKNOWN"


@pytest.mark.unit
def test_newlines_in_the_flagged_text_are_collapsed() -> None:
    parsed = parse_matches(
        {"matches": [{"context": {"text": "el\n  comú gestiona", "offset": 0, "length": 9}}]}
    )
    assert parsed[0].text == "el comú"


# ─────────────────────────────────────────────────────────────
# The live wiring — blocked-by-resource, so the transport is faked, not the logic
# ─────────────────────────────────────────────────────────────


@dataclass
class FakeResponse:
    """Enough of a ``requests.Response`` for the LanguageTool client."""

    payload: object
    status: int = 200

    def raise_for_status(self) -> None:
        if self.status >= 400:
            raise RuntimeError(f"HTTP {self.status}")

    def json(self) -> object:
        return self.payload


@pytest.mark.unit
def test_the_live_service_posts_the_text_and_parses_the_reply(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sent: dict[str, object] = {}

    def fake_post(url: str, **kwargs: object) -> FakeResponse:
        sent["url"] = url
        sent.update(kwargs)
        return FakeResponse(
            {
                "matches": [
                    {
                        "rule": {"id": "MORFOLOGIK_RULE_CA_ES", "category": {"id": "TYPOS"}},
                        "context": {"text": "el comú", "offset": 3, "length": 4},
                    }
                ]
            }
        )

    monkeypatch.setattr("requests.post", fake_post)
    service = languagetool_service("http://localhost:8081/v2/check")
    matches = service.check("el comú", "ca-ES")
    assert [match.text for match in matches] == ["comú"]
    assert sent["url"] == "http://localhost:8081/v2/check"
    assert sent["data"] == {"text": "el comú", "language": "ca-ES"}


@pytest.mark.unit
def test_the_live_service_raises_on_an_http_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("requests.post", lambda url, **kwargs: FakeResponse({}, status=500))
    with pytest.raises(RuntimeError, match="HTTP 500"):
        languagetool_service().check("text")


@pytest.mark.unit
def test_the_live_service_refuses_a_reply_that_is_not_languagetool(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An error body served as 200 must not read as "no problems found"."""
    monkeypatch.setattr(
        "requests.post", lambda url, **kwargs: FakeResponse({"error": "unsupported language"})
    )
    with pytest.raises(ValueError, match="not a LanguageTool"):
        languagetool_service().check("text")
