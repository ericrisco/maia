"""Tests for the §3.2 dataset contract (blocks Phase 2)."""

from __future__ import annotations

from uuid import UUID, uuid4

import pytest
from pydantic import ValidationError

from maia.schemas import DatasetExample, ExampleType, Message, Role, Split, compute_id

GROUNDING = compute_id("Les falles són una tradició del solstici d'estiu.")
OTHER_GROUNDING = compute_id("El Consell General exerceix la potestat legislativa.")


def turns(count: int) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = []
    for index in range(count):
        messages.append({"role": "user", "content": f"Pregunta {index}?"})
        messages.append({"role": "assistant", "content": f"Resposta {index}."})
    return messages


def payload(**overrides: object) -> dict[str, object]:
    base: dict[str, object] = {
        "id": str(uuid4()),
        "messages": turns(1),
        "type": "qa",
        "topic": "historia/pareatges-1278",
        "grounding_ids": [GROUNDING],
        "generator": "claude-opus-5",
        "judge_score": 0.87,
        "split": "train",
    }
    base.update(overrides)
    return base


# ─────────────────────────────────────────────────────────────
# Shape
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_valid_example_round_trips() -> None:
    example = DatasetExample.model_validate(payload())
    reloaded = DatasetExample.model_validate(example.model_dump(mode="json"))
    assert reloaded == example
    assert isinstance(example.id, UUID)
    assert example.messages[0].role is Role.USER


@pytest.mark.unit
def test_unknown_fields_are_rejected() -> None:
    with pytest.raises(ValidationError, match="Extra inputs"):
        DatasetExample.model_validate(payload(nota="no forma part del contracte"))


@pytest.mark.unit
def test_the_enum_members_match_the_contract() -> None:
    assert {t.value for t in ExampleType} == {
        "qa",
        "explicacio",
        "multiturn",
        "resum",
        "traduccio",
        "no_ho_se",
        "rag_style",
        "estil_andorra",
        "general_ca",
    }
    assert {s.value for s in Split} == {"train", "val", "test"}
    assert {r.value for r in Role} == {"user", "assistant"}


@pytest.mark.unit
@pytest.mark.parametrize("score", [-0.01, 1.01])
def test_judge_score_must_be_a_probability(score: float) -> None:
    with pytest.raises(ValidationError):
        DatasetExample.model_validate(payload(judge_score=score))


@pytest.mark.unit
@pytest.mark.parametrize("score", [0.0, 1.0])
def test_judge_score_boundaries_are_allowed(score: float) -> None:
    assert DatasetExample.model_validate(payload(judge_score=score)).judge_score == score


@pytest.mark.unit
def test_empty_topic_generator_and_content_are_rejected() -> None:
    for override in (
        {"topic": ""},
        {"generator": ""},
        {"messages": [{"role": "user", "content": ""}, {"role": "assistant", "content": "a"}]},
    ):
        with pytest.raises(ValidationError):
            DatasetExample.model_validate(payload(**override))


@pytest.mark.unit
def test_a_non_uuid_id_is_rejected() -> None:
    with pytest.raises(ValidationError):
        DatasetExample.model_validate(payload(id="not-a-uuid"))


# ─────────────────────────────────────────────────────────────
# Conversation invariants
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_conversation_must_open_with_the_user() -> None:
    with pytest.raises(ValidationError, match="open with a user message"):
        DatasetExample.model_validate(
            payload(
                messages=[
                    {"role": "assistant", "content": "Hola."},
                    {"role": "user", "content": "Hola?"},
                ]
            )
        )


@pytest.mark.unit
def test_a_conversation_must_end_with_the_assistant() -> None:
    with pytest.raises(ValidationError, match="end with an assistant message"):
        DatasetExample.model_validate(
            payload(
                type="multiturn",
                messages=[*turns(1), {"role": "user", "content": "I ara?"}],
            )
        )


@pytest.mark.unit
def test_roles_must_alternate() -> None:
    with pytest.raises(ValidationError, match="alternate"):
        DatasetExample.model_validate(
            payload(
                type="multiturn",
                messages=[
                    {"role": "user", "content": "Una."},
                    {"role": "user", "content": "Dues."},
                    {"role": "assistant", "content": "Resposta."},
                    {"role": "assistant", "content": "Una altra."},
                ],
            )
        )


@pytest.mark.unit
def test_multiturn_needs_more_than_one_turn() -> None:
    with pytest.raises(ValidationError, match="at least two"):
        DatasetExample.model_validate(payload(type="multiturn", messages=turns(1)))


@pytest.mark.unit
def test_multiturn_accepts_several_turns() -> None:
    example = DatasetExample.model_validate(payload(type="multiturn", messages=turns(3)))
    assert len(example.messages) == 6


@pytest.mark.unit
def test_a_single_turn_type_may_not_carry_several_turns() -> None:
    # Otherwise the type field stops describing the example, and the training mix is wrong.
    with pytest.raises(ValidationError, match="single turn; use multiturn"):
        DatasetExample.model_validate(payload(type="qa", messages=turns(2)))


# ─────────────────────────────────────────────────────────────
# Grounding invariants — the anti-hallucination measure
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
@pytest.mark.parametrize(
    "example_type", ["qa", "explicacio", "resum", "traduccio", "no_ho_se", "rag_style"]
)
def test_grounded_types_must_cite_the_corpus(example_type: str) -> None:
    """Grounding is *the* anti-hallucination measure, so an ungrounded example is a defect.

    The generator always receives real corpus passages; an example citing none was not
    grounded in anything.
    """
    with pytest.raises(ValidationError, match="must cite the corpus passages"):
        DatasetExample.model_validate(payload(type=example_type, grounding_ids=[]))


@pytest.mark.unit
def test_multiturn_must_also_be_grounded() -> None:
    with pytest.raises(ValidationError, match="must cite the corpus passages"):
        DatasetExample.model_validate(
            payload(type="multiturn", messages=turns(2), grounding_ids=[])
        )


@pytest.mark.unit
def test_general_ca_must_not_be_grounded() -> None:
    # It is the anti-forgetting mix and deliberately unrelated to Andorra: grounding it would
    # mean it came from the corpus, which defeats its purpose.
    with pytest.raises(ValidationError, match="anti-forgetting mix"):
        DatasetExample.model_validate(payload(type="general_ca", grounding_ids=[GROUNDING]))


@pytest.mark.unit
def test_general_ca_and_estil_andorra_are_valid_without_grounding() -> None:
    assert (
        DatasetExample.model_validate(payload(type="general_ca", grounding_ids=[])).grounding_ids
        == []
    )
    assert (
        DatasetExample.model_validate(payload(type="estil_andorra", grounding_ids=[])).grounding_ids
        == []
    )


@pytest.mark.unit
def test_estil_andorra_may_be_grounded_if_it_happens_to_be() -> None:
    example = DatasetExample.model_validate(payload(type="estil_andorra"))
    assert example.grounding_ids == [GROUNDING]


@pytest.mark.unit
def test_grounding_ids_must_be_corpus_ids() -> None:
    for bad in ["abc", GROUNDING.upper(), GROUNDING[:-1], f"{GROUNDING}0"]:
        with pytest.raises(ValidationError, match=r"not a §3\.1 document id"):
            DatasetExample.model_validate(payload(grounding_ids=[bad]))


@pytest.mark.unit
def test_grounding_ids_must_not_repeat() -> None:
    with pytest.raises(ValidationError, match="must not repeat"):
        DatasetExample.model_validate(payload(grounding_ids=[GROUNDING, GROUNDING]))


@pytest.mark.unit
def test_several_distinct_grounding_ids_are_fine() -> None:
    example = DatasetExample.model_validate(payload(grounding_ids=[GROUNDING, OTHER_GROUNDING]))
    assert len(example.grounding_ids) == 2


# ─────────────────────────────────────────────────────────────
# Type predicates
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_requires_grounding_exempts_exactly_two_types() -> None:
    exempt = {t for t in ExampleType if not t.requires_grounding()}
    assert exempt == {ExampleType.GENERAL_CA, ExampleType.ESTIL_ANDORRA}


@pytest.mark.unit
def test_only_rag_style_embeds_source_text() -> None:
    # This is what makes rag_style the one unambiguous licence violation when grounded on a
    # no-redistribute document: the passage *is* the context.
    embedding = {t for t in ExampleType if t.embeds_source_text()}
    assert embedding == {ExampleType.RAG_STYLE}


@pytest.mark.unit
def test_message_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        Message.model_validate({"role": "user", "content": "Hola", "name": "eric"})
