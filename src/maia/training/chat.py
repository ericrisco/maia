"""The Gemma chat template — PLAN M3.01, and the one gotcha the spec names.

*"Dataset in the **official Gemma 4 chat template** (not old role formats)"* and *"template mismatch
is the #1 cause of 'the model got worse on export'"*.

The failure is quiet and expensive. Training formats the conversation one way, inference formats it
another, and nothing errors — the model simply behaves worse than the base it started from, after a
€40 GPU run and a day of evaluation. Two details cause most of it:

* **Gemma calls the assistant ``model``.** §3.2 stores ``assistant`` (the interchange format every
  other tool understands), so the mapping happens exactly here and nowhere else. A dataset rendered
  with a literal ``assistant`` turn trains the model to answer to a role marker it will never be
  given at inference.
* **``<bos>`` is added by the tokenizer, and by most inference engines.** Writing it into the
  training text as well trains the model on a double-BOS prefix it never sees again. So
  :func:`render` does not emit it, and :func:`prefixed` exists for the one case that needs it.

Because a mismatch cannot be caught by looking at either side alone, :func:`check_parity` compares
this module's rendering against the real ``tokenizer.apply_chat_template`` and reports the first
difference. The tokenizer is **blocked-by-resource** — :class:`ChatTemplate` is the seam.

The plan also records the decision to *"train only on the visible final response"*. Unsloth
implements that with ``train_on_responses_only(instruction_part=…, response_part=…)``, matching on
literal strings; :data:`INSTRUCTION_PART` and :data:`RESPONSE_PART` are those strings, and
:func:`trainable_spans` computes the same masking here so it can be tested without a GPU — including
the case that makes it worth testing: a **multiturn** example, where the mask has to skip back into
the middle of the text rather than covering one trailing block.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import Protocol

from maia.schemas import DatasetExample, Role

#: Gemma's turn delimiters.
START_OF_TURN = "<start_of_turn>"
END_OF_TURN = "<end_of_turn>"
BOS = "<bos>"

#: What Gemma calls each §3.2 role. **The assistant is ``model``** — see the module docstring.
GEMMA_ROLES = {Role.USER: "user", Role.ASSISTANT: "model"}

#: The literal strings Unsloth's ``train_on_responses_only`` matches on for Gemma 2/3/4.
INSTRUCTION_PART = f"{START_OF_TURN}user\n"
RESPONSE_PART = f"{START_OF_TURN}model\n"


class ChatTemplate(Protocol):
    """A tokenizer's ``apply_chat_template``. Blocked-by-resource: needs the model's tokenizer."""

    def apply_chat_template(
        self,
        conversation: Sequence[dict[str, str]],
        *,
        tokenize: bool = False,
        add_generation_prompt: bool = False,
    ) -> str:
        """Render a conversation the way the model was trained."""


class TemplateMismatchError(RuntimeError):
    """Raised when this module and the real tokenizer disagree about the training text."""


def to_messages(example: DatasetExample) -> list[dict[str, str]]:
    """The example as a chat-template input, with Gemma's role names.

    This is the only place the ``assistant`` → ``model`` mapping happens.
    """
    return [
        {"role": GEMMA_ROLES[message.role], "content": message.content}
        for message in example.messages
    ]


def render_turn(role: Role, content: str) -> str:
    """One Gemma turn, terminated."""
    return f"{START_OF_TURN}{GEMMA_ROLES[role]}\n{content}{END_OF_TURN}\n"


def render(example: DatasetExample, *, add_generation_prompt: bool = False) -> str:
    """The training text for one example.

    No ``<bos>``: the tokenizer adds it, and so do most inference engines — emitting it here as well
    trains the model on a double-BOS prefix it will never see again. Use :func:`prefixed` when a raw
    string genuinely needs one.

    ``add_generation_prompt`` opens a model turn and leaves it unterminated, which is what inference
    needs and training must not have.
    """
    text = "".join(render_turn(message.role, message.content) for message in example.messages)
    return f"{text}{RESPONSE_PART}" if add_generation_prompt else text


def prefixed(text: str) -> str:
    """``text`` with a single ``<bos>``, idempotently.

    Adding a second one is a silent corruption, so this refuses to.
    """
    return text if text.startswith(BOS) else f"{BOS}{text}"


@dataclass(frozen=True)
class Span:
    """A half-open ``[start, end)`` character range of the rendered text."""

    start: int
    end: int

    def of(self, text: str) -> str:
        """The slice this span covers."""
        return text[self.start : self.end]


def trainable_spans(example: DatasetExample) -> list[Span]:
    """The character ranges loss is computed over — the model's turns and nothing else.

    Mirrors ``train_on_responses_only``: everything from just after a ``<start_of_turn>model\\n``
    marker up to and including its ``<end_of_turn>\\n``. A **multiturn** example therefore has
    several spans with user turns between them, which is why this is worth computing rather than
    assuming the answer is the trailing block.

    The terminator is included on purpose: the model has to learn to *stop*, and a mask that ends
    before ``<end_of_turn>`` trains it to run on.
    """
    spans: list[Span] = []
    cursor = 0
    text = render(example)
    for message in example.messages:
        turn = render_turn(message.role, message.content)
        if message.role is Role.ASSISTANT:
            spans.append(Span(cursor + len(RESPONSE_PART), cursor + len(turn)))
        cursor += len(turn)
    assert cursor == len(text)  # every turn accounted for
    return spans


def trainable_text(example: DatasetExample) -> str:
    """Just the parts loss is computed over, joined — a readable form of the mask."""
    text = render(example)
    return "".join(span.of(text) for span in trainable_spans(example))


def masked_share(example: DatasetExample) -> float:
    """Fraction of the rendered text that loss is *not* computed over.

    Reported by the smoke run: a share near 1.0 means the mask matched almost nothing, which is the
    shape of the "zero loss" failure Unsloth's own troubleshooting page warns about.
    """
    text = render(example)
    trainable = sum(span.end - span.start for span in trainable_spans(example))
    return 1.0 - trainable / len(text) if text else 0.0


def check_parity(
    example: DatasetExample, template: ChatTemplate, *, add_generation_prompt: bool = False
) -> None:
    """Compare this module's rendering with the real tokenizer's.

    Raises:
        TemplateMismatchError: naming the first differing character and showing both sides. A
            mismatch cannot be seen by looking at either side alone, and its symptom — a model that
            is simply worse after export — costs a GPU run and an evaluation to discover.
    """
    ours = render(example, add_generation_prompt=add_generation_prompt)
    theirs = template.apply_chat_template(
        to_messages(example), tokenize=False, add_generation_prompt=add_generation_prompt
    )
    # The tokenizer may prepend <bos>; ours deliberately does not.
    normalised = theirs[len(BOS) :] if theirs.startswith(BOS) else theirs
    if normalised == ours:
        return
    index = next(
        (
            position
            for position, (left, right) in enumerate(zip(ours, normalised, strict=False))
            if left != right
        ),
        min(len(ours), len(normalised)),
    )
    raise TemplateMismatchError(
        f"chat template mismatch at character {index}:\n"
        f"  ours:      {ours[max(0, index - 30) : index + 30]!r}\n"
        f"  tokenizer: {normalised[max(0, index - 30) : index + 30]!r}\n"
        "training and inference must format identically, or the model will simply be worse after "
        "export with nothing raising"
    )


def format_dataset(examples: Iterable[DatasetExample]) -> list[dict[str, str]]:
    """``[{"text": …}]`` — the shape ``SFTTrainer`` consumes."""
    return [{"text": render(example)} for example in examples]


def gemma_tokenizer(model: str) -> ChatTemplate:
    """The real tokenizer (blocked-by-resource: downloads the model's tokenizer).

    Imported locally so this module and its tests need neither the network nor ``transformers``.
    """
    from transformers import AutoTokenizer

    loaded: ChatTemplate = AutoTokenizer.from_pretrained(model)
    return loaded
