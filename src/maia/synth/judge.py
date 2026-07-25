"""LLM-as-judge factual-support check — PLAN M2.05, filter 2 of 3.

The spec asks one question: *is the answer supported by the passage?* Grounded generation makes
hallucination unlikely, not impossible — the generator receives real passages but still writes
freely, and a plausible sentence that the passage does not contain is exactly the failure a public
Andorran model cannot ship. So every grounded example is re-read against its own sources by a
second model call, and :attr:`DatasetExample.judge_score` stops being the ``0.0`` placeholder the
generator wrote.

**Two rubrics, chosen by type.** Applying "is this supported by the passage?" to a ``no_ho_se``
example is incoherent: that example's whole correctness is that it *declines*, and a refusal is
supported by nothing. Judged on the factual-support rubric, the 8 % of the dataset that teaches
honesty would score near zero and be filtered out — deleting the honesty training on the grounds
that it asserts nothing. So ``no_ho_se`` gets an **abstention** rubric instead: does the answer
decline, and does it avoid smuggling in facts the passage does not contain?

The two types that :meth:`ExampleType.requires_grounding` exempts are **not judged at all**, and
must be exempt from the threshold too: ``general_ca`` is upstream curated data unrelated to
Andorra, and ``estil_andorra`` is a register rewrite whose quality is linguistic, not factual —
that one is LanguageTool's job (filter 3). Their score stays ``0.0``, so any threshold applied
without :func:`is_exempt` would silently delete a fifth of the dataset.

The API call is **blocked-by-resource**. :class:`Completer` is the seam, satisfied structurally by
:class:`maia.synth.generate.AnthropicGenerator`; the tests drive a scripted stand-in.
"""

from __future__ import annotations

import json
import re
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Protocol

from maia.schemas import CorpusDocument, DatasetExample, ExampleType

#: Below this the example is dropped. The plan calibrates the real value against the M2.06 pilot
#: (PO + linguistic reviewer read 500 examples); this is the starting point, not a finding.
DEFAULT_THRESHOLD = 0.7

#: How much of each grounding passage the judge sees. Long enough for a legal article, short
#: enough that a dozen passages plus the conversation stay inside a sane request.
MAX_PASSAGE_CHARS = 4_000


class Completer(Protocol):
    """Something that turns a prompt into text — the judge's model.

    :class:`maia.synth.generate.AnthropicGenerator` satisfies this structurally, so the judge and
    the generator share one injected client and one refusal path.
    """

    def complete(self, prompt: str) -> str:
        """Send one prompt, return the model's text."""


class JudgeError(RuntimeError):
    """The judge's reply could not be read as a verdict.

    Raised rather than defaulted: a verdict that silently becomes ``0.0`` drops a good example,
    and one that silently becomes ``1.0`` publishes an unchecked one. Both are worse than a stop.
    """


@dataclass(frozen=True)
class Verdict:
    """One judged example."""

    score: float
    reason: str
    unsupported: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not 0.0 <= self.score <= 1.0:
            raise ValueError(f"score {self.score} is outside 0.0-1.0")


def is_exempt(example: DatasetExample) -> bool:
    """Whether this example is outside the factual-support judge's remit.

    The types that cite no passages cannot be checked against passages. Any threshold must ask
    this first — see the module docstring.
    """
    return not example.type.requires_grounding()


def conversation_of(example: DatasetExample) -> str:
    """The example rendered for the judge, roles labelled."""
    return "\n\n".join(
        f"{'PREGUNTA' if message.role == 'user' else 'RESPOSTA'}: {message.content}"
        for message in example.messages
    )


def passages_for(
    example: DatasetExample, corpus: Mapping[str, CorpusDocument]
) -> list[CorpusDocument]:
    """The documents this example cites.

    Raises:
        KeyError: naming the missing id. An example whose grounding cannot be retrieved cannot be
            verified, and passing it unjudged would be indistinguishable from passing it judged.
    """
    missing = [ident for ident in example.grounding_ids if ident not in corpus]
    if missing:
        raise KeyError(
            f"{example.id}: grounding passage(s) not in the corpus: {', '.join(missing)} — "
            "the example cannot be verified against sources that are not here"
        )
    return [corpus[ident] for ident in example.grounding_ids]


_SUPPORT_RUBRIC = """Ets un revisor expert que verifica si una resposta està sostinguda pels \
passatges de referència.

Puntua de 0.0 a 1.0:
- 1.0 — tota afirmació de la resposta es pot verificar als passatges.
- 0.7 — sostinguda en essència; algun detall menor no consta explícitament.
- 0.4 — mescla afirmacions sostingudes amb afirmacions que els passatges no diuen.
- 0.0 — contradiu els passatges, o afirma coses que no hi són.

No puntuïs l'estil ni la utilitat: només si els passatges sostenen el que diu la resposta."""

_ABSTENTION_RUBRIC = """Ets un revisor expert. Aquest exemple ha d'ensenyar el model a \
**declinar** quan els passatges no contenen la resposta.

Puntua de 0.0 a 1.0:
- 1.0 — la resposta reconeix clarament que no ho sap o que no consta als passatges, i no afirma \
cap fet que els passatges no continguin.
- 0.5 — declina però hi afegeix especulació o dades no presents als passatges.
- 0.0 — respon la pregunta com si ho sabés, o els passatges sí que contenen la resposta i per \
tant declinar és incorrecte.

Una resposta que no afirma res NO és un error aquí: és exactament el comportament desitjat."""

_FORMAT = """Respon **només** amb aquest JSON, sense cap altre text:
{"score": 0.0, "reason": "una frase", "unsupported": ["afirmació no sostinguda", "..."]}"""


def rubric_for(example: DatasetExample) -> str:
    """Which rubric applies — abstention for ``no_ho_se``, factual support otherwise."""
    return _ABSTENTION_RUBRIC if example.type is ExampleType.NO_HO_SE else _SUPPORT_RUBRIC


def build_prompt(example: DatasetExample, passages: Sequence[CorpusDocument]) -> str:
    """The judge prompt: rubric, passages, conversation, output format."""
    rendered = "\n\n".join(
        f"[PASSATGE {index}] {document.text[:MAX_PASSAGE_CHARS]}"
        for index, document in enumerate(passages, start=1)
    )
    return (
        f"{rubric_for(example)}\n\n"
        f"=== PASSATGES DE REFERÈNCIA ===\n{rendered}\n\n"
        f"=== EXEMPLE A REVISAR (tipus: {example.type.value}) ===\n"
        f"{conversation_of(example)}\n\n"
        f"{_FORMAT}"
    )


_JSON_OBJECT = re.compile(r"\{.*\}", re.DOTALL)


def parse_verdict(reply: str) -> Verdict:
    """Read a verdict out of the judge's reply.

    Tolerates prose around the JSON object, because a model asked for bare JSON still sometimes
    prefaces it. Refuses anything else — see :class:`JudgeError`.
    """
    found = _JSON_OBJECT.search(reply)
    if found is None:
        raise JudgeError(f"no JSON object in the judge's reply: {reply[:200]!r}")
    try:
        payload = json.loads(found.group(0))
    except json.JSONDecodeError as error:
        raise JudgeError(f"the judge's reply is not valid JSON: {error}") from error
    if not isinstance(payload, dict) or "score" not in payload:
        raise JudgeError(f"the judge's reply has no score: {sorted(payload)}")
    score = payload["score"]
    if isinstance(score, bool) or not isinstance(score, int | float):
        raise JudgeError(f"score is not a number: {score!r}")
    reason = payload.get("reason")
    unsupported = payload.get("unsupported")
    try:
        return Verdict(
            score=float(score),
            reason=reason if isinstance(reason, str) else "",
            unsupported=tuple(str(item) for item in unsupported)
            if isinstance(unsupported, list)
            else (),
        )
    except ValueError as error:
        raise JudgeError(str(error)) from error


@dataclass
class JudgeReport:
    """What the judge examined, scored and dropped."""

    examined: int = 0
    judged: int = 0
    exempt: int = 0
    dropped: int = 0
    failed: int = 0
    failures: list[str] = field(default_factory=list)
    scores: list[float] = field(default_factory=list)

    @property
    def kept(self) -> int:
        """How many examples survive."""
        return self.examined - self.dropped

    @property
    def mean_score(self) -> float:
        """Mean score over the *judged* examples — exempt zeros would drag it down."""
        return sum(self.scores) / len(self.scores) if self.scores else 0.0


@dataclass(frozen=True)
class FactualSupportJudge:
    """Re-reads each grounded example against its own passages.

    ``completer`` is injected — see :class:`maia.synth.generate.AnthropicGenerator`.
    """

    completer: Completer
    threshold: float = DEFAULT_THRESHOLD

    def judge(
        self, example: DatasetExample, corpus: Mapping[str, CorpusDocument]
    ) -> Verdict | None:
        """Score one example, or ``None`` if it is exempt."""
        if is_exempt(example):
            return None
        passages = passages_for(example, corpus)
        return parse_verdict(self.completer.complete(build_prompt(example, passages)))

    def run(
        self,
        examples: Sequence[DatasetExample],
        corpus: Mapping[str, CorpusDocument],
        *,
        keep_failures: bool = False,
    ) -> tuple[list[DatasetExample], JudgeReport]:
        """Judge every example, returning the survivors with their scores written in.

        A judge call that fails to produce a verdict is **counted and the example dropped** by
        default: an unjudged example carries a ``0.0`` score that no longer means "not yet
        judged". ``keep_failures=True`` keeps them for a human to look at, which is what the
        M2.06 pilot wants.
        """
        report = JudgeReport(examined=len(examples))
        survivors: list[DatasetExample] = []
        for example in examples:
            if is_exempt(example):
                report.exempt += 1
                survivors.append(example)
                continue
            try:
                verdict = self.judge(example, corpus)
            except (JudgeError, KeyError) as error:
                report.failed += 1
                report.failures.append(f"{example.id}: {error}")
                if keep_failures:
                    survivors.append(example)
                else:
                    report.dropped += 1
                continue
            assert verdict is not None  # not exempt, so judge() scored it
            report.judged += 1
            report.scores.append(verdict.score)
            if verdict.score < self.threshold:
                report.dropped += 1
                continue
            survivors.append(example.model_copy(update={"judge_score": verdict.score}))
        return survivors, report


def render(report: JudgeReport) -> str:
    """Human-readable summary."""
    lines = [
        f"factual-support judge: {report.kept}/{report.examined} kept "
        f"({report.dropped} dropped), {report.judged} judged, {report.exempt} exempt "
        f"(general_ca + estil_andorra cite no passages), mean score {report.mean_score:.2f}"
    ]
    if report.failed:
        lines.append(f"  ⚠ {report.failed} example(s) could not be judged:")
        lines.extend(f"    {failure}" for failure in report.failures[:5])
    return "\n".join(lines)


def index_corpus(documents: Iterable[CorpusDocument]) -> dict[str, CorpusDocument]:
    """Index documents by id, for :func:`passages_for`."""
    return {document.id: document for document in documents}
