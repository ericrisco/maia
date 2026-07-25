"""Tests for the LLM-as-judge factual-support filter (PLAN M2.05, filter 2)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from uuid import uuid4

import pytest

from maia.schemas import (
    CorpusDocument,
    DatasetExample,
    ExampleType,
    License,
    Registre,
    Source,
    compute_id,
)
from maia.synth.judge import (
    DEFAULT_THRESHOLD,
    MAX_PASSAGE_CHARS,
    FactualSupportJudge,
    JudgeError,
    JudgeReport,
    Verdict,
    build_prompt,
    conversation_of,
    index_corpus,
    is_exempt,
    parse_verdict,
    passages_for,
    render,
    rubric_for,
)

PASSAGE = (
    "El Consell General es compon de 28 consellers generals, la meitat elegits per circumscripció "
    "parroquial i l'altra meitat per circumscripció nacional."
)


def document(text: str = PASSAGE) -> CorpusDocument:
    return CorpusDocument.model_validate(
        {
            "id": compute_id(text),
            "text": text,
            "source": Source.JURIDIC.value,
            "url": "https://www.portaljuridicandorra.ad/llei/exemple",
            "fetched_at": "2026-07-25T10:00:00+00:00",
            "license": License.PUBLIC_OFFICIAL.value,
            "registre": Registre.ESTANDARD.value,
            "lang": "ca",
        }
    )


CORPUS = index_corpus([document()])


def example(
    *,
    kind: ExampleType = ExampleType.QA,
    prompt: str = "Quants consellers generals hi ha?",
    response: str = "Vint-i-vuit.",
    grounded: bool = True,
) -> DatasetExample:
    return DatasetExample.model_validate(
        {
            "id": str(uuid4()),
            "messages": [
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": response},
                *(
                    [
                        {"role": "user", "content": "I qui els presideix?"},
                        {"role": "assistant", "content": "El síndic general."},
                    ]
                    if kind is ExampleType.MULTITURN
                    else []
                ),
            ],
            "type": kind.value,
            "topic": "institucions/consell-general",
            "grounding_ids": [compute_id(PASSAGE)] if grounded else [],
            "generator": "claude-opus-5",
            "judge_score": 0.0,
            "split": "train",
        }
    )


@dataclass
class ScriptedCompleter:
    """The injected model — returns canned replies and records the prompts it saw."""

    replies: list[str]
    prompts: list[str] = field(default_factory=list)

    def complete(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return self.replies[min(len(self.prompts) - 1, len(self.replies) - 1)]


def verdict_json(score: float, reason: str = "Sostinguda pel passatge.") -> str:
    return json.dumps({"score": score, "reason": reason, "unsupported": []})


# ─────────────────────────────────────────────────────────────
# Exemption — the trap this filter has to avoid
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
@pytest.mark.parametrize("kind", [ExampleType.GENERAL_CA, ExampleType.ESTIL_ANDORRA])
def test_the_ungrounded_types_are_exempt(kind: ExampleType) -> None:
    """They cite no passages, so they cannot be checked against passages.

    Their score stays 0.0, so a threshold applied without asking this would delete a fifth of the
    dataset — the whole anti-forgetting mix and every register rewrite.
    """
    assert is_exempt(example(kind=kind, grounded=False))


@pytest.mark.unit
@pytest.mark.parametrize(
    "kind",
    [
        ExampleType.QA,
        ExampleType.EXPLICACIO,
        ExampleType.MULTITURN,
        ExampleType.RESUM,
        ExampleType.TRADUCCIO,
        ExampleType.NO_HO_SE,
        ExampleType.RAG_STYLE,
    ],
)
def test_every_grounded_type_is_judged(kind: ExampleType) -> None:
    assert not is_exempt(example(kind=kind))


@pytest.mark.unit
def test_an_exempt_example_survives_without_a_model_call() -> None:
    completer = ScriptedCompleter([verdict_json(0.0)])
    judge = FactualSupportJudge(completer)
    survivors, report = judge.run([example(kind=ExampleType.GENERAL_CA, grounded=False)], CORPUS)
    assert len(survivors) == 1
    assert report.exempt == 1
    assert report.judged == 0
    assert completer.prompts == []


@pytest.mark.unit
def test_an_exempt_example_keeps_its_zero_score() -> None:
    survivors, _ = FactualSupportJudge(ScriptedCompleter([verdict_json(1.0)])).run(
        [example(kind=ExampleType.GENERAL_CA, grounded=False)], CORPUS
    )
    assert survivors[0].judge_score == 0.0


@pytest.mark.unit
def test_judging_an_exempt_example_directly_returns_no_verdict() -> None:
    judge = FactualSupportJudge(ScriptedCompleter([verdict_json(1.0)]))
    assert judge.judge(example(kind=ExampleType.GENERAL_CA, grounded=False), CORPUS) is None


@pytest.mark.unit
def test_the_mean_score_ignores_exempt_zeros() -> None:
    """Otherwise the reported mean is dragged down by examples nobody scored."""
    completer = ScriptedCompleter([verdict_json(1.0)])
    _, report = FactualSupportJudge(completer).run(
        [example(), example(kind=ExampleType.GENERAL_CA, grounded=False)], CORPUS
    )
    assert report.mean_score == pytest.approx(1.0)


# ─────────────────────────────────────────────────────────────
# The two rubrics
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_no_ho_se_is_judged_on_abstention_not_factual_support() -> None:
    """Judged on factual support, an honest refusal scores zero for asserting nothing.

    That would filter out the 8 % of the dataset that teaches the model to decline — the exact
    opposite of what the rubric should reward.
    """
    rubric = rubric_for(example(kind=ExampleType.NO_HO_SE))
    assert "declinar" in rubric
    assert "NO és un error" in rubric
    assert rubric != rubric_for(example(kind=ExampleType.QA))


@pytest.mark.unit
@pytest.mark.parametrize(
    "kind", [ExampleType.QA, ExampleType.EXPLICACIO, ExampleType.RAG_STYLE, ExampleType.RESUM]
)
def test_every_other_type_is_judged_on_factual_support(kind: ExampleType) -> None:
    assert "sostinguda" in rubric_for(example(kind=kind))


@pytest.mark.unit
def test_the_prompt_carries_the_passages_the_rubric_and_the_conversation() -> None:
    prompt = build_prompt(example(), [document()])
    assert PASSAGE in prompt
    assert "[PASSATGE 1]" in prompt
    assert "Quants consellers generals hi ha?" in prompt
    assert "tipus: qa" in prompt
    assert '{"score"' in prompt


@pytest.mark.unit
def test_a_long_passage_is_truncated() -> None:
    # A distinctive character, so the count is the passage and not the Catalan rubric.
    long = document("Ж" * 9_000)
    prompt = build_prompt(example(), [long])
    assert prompt.count("Ж") == MAX_PASSAGE_CHARS


@pytest.mark.unit
def test_the_conversation_labels_both_roles() -> None:
    rendered = conversation_of(example(prompt="La pregunta", response="La resposta"))
    assert "PREGUNTA: La pregunta" in rendered
    assert "RESPOSTA: La resposta" in rendered


# ─────────────────────────────────────────────────────────────
# Grounding lookup
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_cited_passages_are_retrieved() -> None:
    assert [item.text for item in passages_for(example(), CORPUS)] == [PASSAGE]


@pytest.mark.unit
def test_a_missing_grounding_passage_is_an_error_not_a_pass() -> None:
    """Passing it unjudged would be indistinguishable from passing it judged."""
    with pytest.raises(KeyError, match="not in the corpus"):
        passages_for(example(), {})


@pytest.mark.unit
def test_an_unverifiable_example_is_dropped_and_named() -> None:
    unverifiable = example()
    survivors, report = FactualSupportJudge(ScriptedCompleter([verdict_json(1.0)])).run(
        [unverifiable], {}
    )
    assert survivors == []
    assert report.failed == 1
    assert report.dropped == 1
    assert str(unverifiable.id) in report.failures[0]
    assert "could not be judged" in render(report)


@pytest.mark.unit
def test_failures_can_be_kept_for_a_human() -> None:
    """What the M2.06 pilot wants: see them, do not lose them."""
    survivors, report = FactualSupportJudge(ScriptedCompleter([verdict_json(1.0)])).run(
        [example()], {}, keep_failures=True
    )
    assert len(survivors) == 1
    assert report.failed == 1
    assert report.dropped == 0


# ─────────────────────────────────────────────────────────────
# Reading the verdict
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_clean_verdict_is_read() -> None:
    parsed = parse_verdict(
        json.dumps({"score": 0.8, "reason": "Gairebé tot consta.", "unsupported": ["el 1866"]})
    )
    assert parsed.score == 0.8
    assert parsed.reason == "Gairebé tot consta."
    assert parsed.unsupported == ("el 1866",)


@pytest.mark.unit
def test_prose_around_the_json_is_tolerated() -> None:
    assert parse_verdict(f"He revisat l'exemple.\n{verdict_json(0.9)}\nGràcies.").score == 0.9


@pytest.mark.unit
def test_an_integer_score_is_accepted() -> None:
    assert parse_verdict('{"score": 1}').score == 1.0


@pytest.mark.unit
def test_missing_optional_fields_default_to_empty() -> None:
    parsed = parse_verdict('{"score": 0.5}')
    assert parsed.reason == ""
    assert parsed.unsupported == ()


@pytest.mark.unit
def test_a_non_list_unsupported_field_is_ignored() -> None:
    assert parse_verdict('{"score": 0.5, "unsupported": "cap"}').unsupported == ()


@pytest.mark.unit
@pytest.mark.parametrize(
    ("reply", "message"),
    [
        ("El resultat és bo.", "no JSON object"),
        ('{"score": 0.5,}', "not valid JSON"),
        ('{"reason": "bé"}', "has no score"),
        ('{"score": "alt"}', "score is not a number"),
        ('{"score": true}', "score is not a number"),
        ('{"score": 1.5}', "outside 0.0-1.0"),
        ('{"score": -0.2}', "outside 0.0-1.0"),
    ],
)
def test_an_unreadable_verdict_raises(reply: str, message: str) -> None:
    """A verdict silently defaulting to 0.0 drops a good example; to 1.0 it publishes an unchecked
    one. Both are worse than stopping."""
    with pytest.raises(JudgeError, match=message):
        parse_verdict(reply)


@pytest.mark.unit
def test_a_score_outside_the_range_is_refused_at_construction() -> None:
    with pytest.raises(ValueError, match=r"outside 0\.0-1\.0"):
        Verdict(score=2.0, reason="")


# ─────────────────────────────────────────────────────────────
# The pipeline stage
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_well_supported_example_survives_with_its_score_written_in() -> None:
    survivors, report = FactualSupportJudge(ScriptedCompleter([verdict_json(0.95)])).run(
        [example()], CORPUS
    )
    assert survivors[0].judge_score == 0.95
    assert report.judged == 1
    assert report.dropped == 0
    assert report.kept == 1


@pytest.mark.unit
def test_an_unsupported_example_is_dropped() -> None:
    survivors, report = FactualSupportJudge(ScriptedCompleter([verdict_json(0.2)])).run(
        [example(response="Hi ha 42 consellers, elegits cada dos anys.")], CORPUS
    )
    assert survivors == []
    assert report.dropped == 1
    assert report.judged == 1


@pytest.mark.unit
def test_the_threshold_is_inclusive() -> None:
    """An example scoring exactly the threshold is good enough — the band is documented as ≥."""
    survivors, _ = FactualSupportJudge(ScriptedCompleter([verdict_json(DEFAULT_THRESHOLD)])).run(
        [example()], CORPUS
    )
    assert len(survivors) == 1


@pytest.mark.unit
def test_the_threshold_is_configurable() -> None:
    kept, _ = FactualSupportJudge(ScriptedCompleter([verdict_json(0.5)]), threshold=0.4).run(
        [example()], CORPUS
    )
    dropped, _ = FactualSupportJudge(ScriptedCompleter([verdict_json(0.5)]), threshold=0.9).run(
        [example()], CORPUS
    )
    assert len(kept) == 1 and dropped == []


@pytest.mark.unit
def test_one_model_call_per_grounded_example() -> None:
    completer = ScriptedCompleter([verdict_json(1.0)])
    FactualSupportJudge(completer).run(
        [example(), example(), example(kind=ExampleType.GENERAL_CA, grounded=False)], CORPUS
    )
    assert len(completer.prompts) == 2


@pytest.mark.unit
def test_the_summary_reports_what_was_judged_and_what_was_excused() -> None:
    _, report = FactualSupportJudge(ScriptedCompleter([verdict_json(0.9)])).run(
        [example(), example(kind=ExampleType.ESTIL_ANDORRA, grounded=False)], CORPUS
    )
    rendered = render(report)
    assert "2/2 kept" in rendered
    assert "1 judged" in rendered
    assert "1 exempt" in rendered
    assert "mean score 0.90" in rendered


@pytest.mark.unit
def test_an_empty_report_renders_a_zero_mean() -> None:
    assert "mean score 0.00" in render(JudgeReport())
