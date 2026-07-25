"""Tests for the Gemma chat template (PLAN M3.01) — the spec's named gotcha."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from itertools import pairwise
from uuid import UUID, uuid5

import pytest

from maia.schemas import DatasetExample, ExampleType, Role, compute_id
from maia.training.chat import (
    BOS,
    END_OF_TURN,
    GEMMA_ROLES,
    INSTRUCTION_PART,
    RESPONSE_PART,
    START_OF_TURN,
    Span,
    TemplateMismatchError,
    check_parity,
    format_dataset,
    masked_share,
    prefixed,
    render,
    render_turn,
    to_messages,
    trainable_spans,
    trainable_text,
)

_NAMESPACE = UUID("6ba7b818-9dad-11d1-80b4-00c04fd430c8")
GROUNDING = compute_id("El Consell General es compon de 28 consellers generals.")


def example(
    *, turns: int = 2, kind: ExampleType = ExampleType.QA, prompt: str = "Quants consellers hi ha?"
) -> DatasetExample:
    messages = [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": "Vint-i-vuit consellers generals."},
    ]
    if turns > 2:
        messages += [
            {"role": "user", "content": "I qui els presideix?"},
            {"role": "assistant", "content": "El síndic general."},
        ]
    return DatasetExample.model_validate(
        {
            "id": str(uuid5(_NAMESPACE, f"{kind.value}|{turns}|{prompt}")),
            "messages": messages,
            "type": kind.value,
            "topic": "institucions/consell-general",
            "grounding_ids": [GROUNDING] if kind.requires_grounding() else [],
            "generator": "claude-opus-5",
            "judge_score": 0.9 if kind.requires_grounding() else 0.0,
            "split": "train",
        }
    )


@dataclass
class FakeTokenizer:
    """A stand-in for the real tokenizer, rendering Gemma's documented template.

    Deliberately written from the documented format rather than from :func:`render`, so the parity
    test compares two independent implementations instead of one with itself.
    """

    add_bos: bool = True
    assistant_role: str = "model"
    seen: list[Sequence[dict[str, str]]] = field(default_factory=list)

    def apply_chat_template(
        self,
        conversation: Sequence[dict[str, str]],
        *,
        tokenize: bool = False,
        add_generation_prompt: bool = False,
    ) -> str:
        self.seen.append(conversation)
        parts = [BOS] if self.add_bos else []
        for message in conversation:
            role = self.assistant_role if message["role"] == "model" else message["role"]
            parts.append(f"<start_of_turn>{role}\n{message['content']}<end_of_turn>\n")
        if add_generation_prompt:
            parts.append("<start_of_turn>model\n")
        return "".join(parts)


# ─────────────────────────────────────────────────────────────
# The role mapping — the gotcha itself
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_gemma_calls_the_assistant_model() -> None:
    """A dataset rendered with a literal `assistant` turn trains the model to answer to a role
    marker it will never be given at inference."""
    assert GEMMA_ROLES[Role.ASSISTANT] == "model"
    assert GEMMA_ROLES[Role.USER] == "user"
    assert "assistant" not in render(example())
    assert f"{START_OF_TURN}model\n" in render(example())


@pytest.mark.unit
def test_the_mapping_happens_in_exactly_one_place() -> None:
    messages = to_messages(example())
    assert [message["role"] for message in messages] == ["user", "model"]
    assert messages[1]["content"] == "Vint-i-vuit consellers generals."


@pytest.mark.unit
def test_a_turn_is_delimited_and_terminated() -> None:
    turn = render_turn(Role.USER, "Hola")
    assert turn == f"{START_OF_TURN}user\nHola{END_OF_TURN}\n"


# ─────────────────────────────────────────────────────────────
# BOS
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_render_does_not_emit_bos() -> None:
    """The tokenizer adds it, and so do most inference engines; emitting it here trains the model
    on a double-BOS prefix it never sees again."""
    assert not render(example()).startswith(BOS)


@pytest.mark.unit
def test_prefixing_bos_is_idempotent() -> None:
    once = prefixed("text")
    assert once == f"{BOS}text"
    assert prefixed(once) == once


# ─────────────────────────────────────────────────────────────
# The rendered training text
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_two_turn_example_renders_both_turns_in_order() -> None:
    text = render(example())
    assert text == (
        f"{START_OF_TURN}user\nQuants consellers hi ha?{END_OF_TURN}\n"
        f"{START_OF_TURN}model\nVint-i-vuit consellers generals.{END_OF_TURN}\n"
    )


@pytest.mark.unit
def test_training_text_has_no_generation_prompt() -> None:
    """An unterminated model turn is what inference needs and training must not have."""
    text = render(example())
    assert text.endswith(f"{END_OF_TURN}\n")
    assert not text.endswith(RESPONSE_PART)


@pytest.mark.unit
def test_the_generation_prompt_opens_an_unterminated_model_turn() -> None:
    assert render(example(), add_generation_prompt=True).endswith(RESPONSE_PART)


@pytest.mark.unit
def test_a_multiturn_example_renders_four_turns() -> None:
    text = render(example(turns=4, kind=ExampleType.MULTITURN))
    assert text.count(INSTRUCTION_PART) == 2
    assert text.count(RESPONSE_PART) == 2


@pytest.mark.unit
def test_the_dataset_is_formatted_as_text_rows() -> None:
    rows = format_dataset([example(), example(prompt="Una altra?")])
    assert [set(row) for row in rows] == [{"text"}, {"text"}]
    assert rows[0]["text"] == render(example())


# ─────────────────────────────────────────────────────────────
# The loss mask — "train only on the visible final response"
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_only_the_model_turn_is_trainable() -> None:
    single = example()
    text = render(single)
    spans = trainable_spans(single)
    assert len(spans) == 1
    assert spans[0].of(text) == f"Vint-i-vuit consellers generals.{END_OF_TURN}\n"
    assert "Quants consellers" not in trainable_text(single)


@pytest.mark.unit
def test_the_terminator_is_inside_the_mask() -> None:
    """The model has to learn to stop; a mask ending before <end_of_turn> trains it to run on."""
    assert trainable_text(example()).endswith(f"{END_OF_TURN}\n")


@pytest.mark.unit
def test_a_multiturn_example_has_one_span_per_model_turn() -> None:
    """The mask has to skip back into the middle of the text, not cover one trailing block."""
    multi = example(turns=4, kind=ExampleType.MULTITURN)
    text = render(multi)
    spans = trainable_spans(multi)
    assert len(spans) == 2
    assert spans[0].of(text).startswith("Vint-i-vuit")
    assert spans[1].of(text).startswith("El síndic general.")
    assert "I qui els presideix?" not in trainable_text(multi)


@pytest.mark.unit
def test_the_spans_do_not_overlap_and_stay_in_order() -> None:
    multi = example(turns=4, kind=ExampleType.MULTITURN)
    spans = trainable_spans(multi)
    assert all(left.end <= right.start for left, right in pairwise(spans))
    assert all(span.start < span.end for span in spans)


@pytest.mark.unit
def test_no_span_covers_a_role_marker() -> None:
    """The markers are the mask's boundaries; training on them teaches the model to emit them."""
    multi = example(turns=4, kind=ExampleType.MULTITURN)
    trainable = trainable_text(multi)
    assert START_OF_TURN not in trainable


@pytest.mark.unit
def test_the_masked_share_is_reported() -> None:
    """A share near 1.0 is the shape of the "zero loss" failure Unsloth warns about."""
    share = masked_share(example())
    assert 0.0 < share < 1.0
    # The prompt side is masked, so more prompt means more masked.
    assert masked_share(example(prompt="Q" * 500)) > share


@pytest.mark.unit
def test_a_span_slices_what_it_says() -> None:
    assert Span(2, 5).of("abcdefg") == "cde"


# ─────────────────────────────────────────────────────────────
# Parity with the real tokenizer
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_parity_holds_against_the_documented_template() -> None:
    check_parity(example(), FakeTokenizer())
    check_parity(example(turns=4, kind=ExampleType.MULTITURN), FakeTokenizer())


@pytest.mark.unit
def test_parity_holds_with_a_generation_prompt() -> None:
    check_parity(example(), FakeTokenizer(), add_generation_prompt=True)


@pytest.mark.unit
def test_a_tokenizer_that_omits_bos_still_matches() -> None:
    """Ours never emits it, so the comparison is on the body either way."""
    check_parity(example(), FakeTokenizer(add_bos=False))


@pytest.mark.unit
def test_a_role_name_mismatch_is_caught() -> None:
    """The exact failure the spec calls the #1 cause of "the model got worse on export"."""
    with pytest.raises(TemplateMismatchError, match="chat template mismatch"):
        check_parity(example(), FakeTokenizer(assistant_role="assistant"))


@pytest.mark.unit
def test_the_mismatch_error_shows_both_sides() -> None:
    with pytest.raises(TemplateMismatchError) as caught:
        check_parity(example(), FakeTokenizer(assistant_role="assistant"))
    message = str(caught.value)
    assert "ours:" in message
    assert "tokenizer:" in message
    assert "worse after export" in message


@pytest.mark.unit
def test_a_length_only_difference_is_caught() -> None:
    """No differing character, so the comparison cannot rely on finding one."""

    @dataclass
    class Truncating(FakeTokenizer):
        def apply_chat_template(
            self,
            conversation: Sequence[dict[str, str]],
            *,
            tokenize: bool = False,
            add_generation_prompt: bool = False,
        ) -> str:
            full = super().apply_chat_template(
                conversation, tokenize=tokenize, add_generation_prompt=add_generation_prompt
            )
            return full[:-10]

    with pytest.raises(TemplateMismatchError, match="chat template mismatch"):
        check_parity(example(), Truncating())


@pytest.mark.unit
def test_the_tokenizer_receives_gemma_role_names() -> None:
    tokenizer = FakeTokenizer()
    check_parity(example(), tokenizer)
    assert [message["role"] for message in tokenizer.seen[0]] == ["user", "model"]


@pytest.mark.unit
def test_the_unsloth_masking_markers_are_the_documented_ones() -> None:
    """These strings are passed verbatim to `train_on_responses_only`."""
    assert INSTRUCTION_PART == "<start_of_turn>user\n"
    assert RESPONSE_PART == "<start_of_turn>model\n"


@pytest.mark.unit
def test_the_markers_appear_in_the_rendered_text_exactly_as_written() -> None:
    """If they did not, Unsloth's literal matching would mask nothing and loss would be zero."""
    text = render(example(turns=4, kind=ExampleType.MULTITURN))
    assert text.count(INSTRUCTION_PART) == 2
    assert text.count(RESPONSE_PART) == 2


@pytest.mark.unit
def test_the_real_tokenizer_is_loaded_through_the_seam(monkeypatch: pytest.MonkeyPatch) -> None:
    """Downloading a tokenizer is blocked-by-resource, so only the wiring is exercised."""
    import sys
    import types

    loaded: list[str] = []

    class FromPretrained:
        @staticmethod
        def from_pretrained(model: str) -> FakeTokenizer:
            loaded.append(model)
            return FakeTokenizer()

    module = types.ModuleType("transformers")
    module.AutoTokenizer = FromPretrained  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "transformers", module)

    from maia.training.chat import gemma_tokenizer

    tokenizer = gemma_tokenizer("unsloth/gemma-4-12b-it")
    assert loaded == ["unsloth/gemma-4-12b-it"]
    check_parity(example(), tokenizer)
