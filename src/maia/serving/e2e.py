"""End-to-end smoke test and failure triage — PLAN M5.08-09, the last item of M5.

An E2E test over a RAG system is not an evaluation. M4 already measures whether MAIA *knows*
things; running that again here would be slower, more expensive and no more informative. What
this checks is that the pieces are joined up: retrieval reaches the index, the index reaches the
prompt, the prompt reaches the model, and the citations reaching the user correspond to passages
that were actually used. Those are the failures that survive a green unit-test suite, because each
component works and the wiring does not.

**The triage is the point, and it is why M5.09 exists as its own item.** A system test that says
"failed" sends three people to read the same log. Every check here declares which :class:`Layer`
its failure implicates, and the signals are chosen so the layers are distinguishable: zero hits
from the retriever is retrieval, hits that never reach the answer is generation, a 500 is serving,
and an answer that fits the target but takes 40 s is capacity. The report groups by layer and
orders by severity, so the first line names the owner.

**Severity is not the same as loudness.** A `no-redistribute` passage quoted verbatim into an
answer is the worst thing this system can do — it is a licence breach, it is public, and it is
silent. It ranks above a wrong answer, which ranks above a slow one. :class:`Severity` encodes
that, and the gate fails on ``COMPLIANCE`` regardless of how many other checks passed.

The system under test is **blocked-by-resource** — deployed endpoint, GPU, populated index. The
seam is :class:`System`; the checks are exercised against fakes that reproduce each failure mode.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from dataclasses import dataclass, field
from enum import IntEnum, StrEnum
from pathlib import Path
from typing import Any, Protocol

from maia.corpus.language import is_catalan
from maia.serving.latency import P95_WARM_SECONDS


class Layer(StrEnum):
    """Which part of the system a failure implicates — the whole point of M5.09."""

    SERVING = "serving"
    RETRIEVAL = "retrieval"
    GENERATION = "generation"
    COMPLIANCE = "compliance"
    CAPACITY = "capacity"


class Severity(IntEnum):
    """Ordered so ``sorted(reverse=True)`` puts the thing to fix first.

    ``COMPLIANCE`` is above ``BROKEN`` deliberately: a system that is down is embarrassing and
    obvious, while a system quietly republishing licensed text is neither, and only one of the two
    cannot be undone.
    """

    SLOW = 1
    WRONG = 2
    BROKEN = 3
    COMPLIANCE = 4


@dataclass(frozen=True)
class Finding:
    """One thing wrong, with the layer that owns it."""

    layer: Layer
    severity: Severity
    check: str
    detail: str

    def __str__(self) -> str:
        return f"[{self.severity.name}/{self.layer.value}] {self.check}: {self.detail}"


@dataclass(frozen=True)
class Answer:
    """What the system returned for one question."""

    text: str
    sources: tuple[dict[str, Any], ...] = ()
    #: Chunk texts the retriever returned, in the order they were retrieved. Empty when RAG is off.
    retrieved: tuple[str, ...] = ()
    seconds: float = 0.0
    status_code: int = 200


class System(Protocol):
    """The deployed system. Blocked-by-resource: endpoint, GPU, populated index."""

    def health(self) -> dict[str, Any]:
        """``GET /health`` as a dict."""

    def ask(self, question: str, *, rag: bool = True) -> Answer:
        """One chat completion."""


@dataclass(frozen=True)
class Case:
    """One end-to-end question and what the *system* must do with it.

    Never what the answer must say — that is M4's job, with a rubric and a judge. These are
    properties of the plumbing, checkable without knowing the right answer.
    """

    question: str
    #: Retrieval must find something. False for questions the weights should answer alone.
    needs_sources: bool = True
    #: A phrase the answer must contain. Used only for the honesty case, where the *shape* of the
    #: answer is the contract rather than its content.
    must_contain: str | None = None


#: The smoke suite. Small on purpose: each case costs a GPU call and this runs after every deploy.
CASES: tuple[Case, ...] = (
    Case("Què és una llei qualificada i com es diferencia d'una ordinària?"),
    Case("Quins són els òrgans judicials d'Andorra?"),
    Case("Què vol dir «plegar» a Andorra?", needs_sources=False),
)

#: The honesty case: a question with no answer in any Andorran corpus. The system must decline.
#: A model that invents a confident answer here will invent one for a legal question too, and this
#: is the cheapest place to find that out.
UNANSWERABLE = Case(
    "Quantes persones van néixer a Ordino el 14 de març de 1873?",
    needs_sources=False,
    must_contain="no ho sé",
)

#: Phrases that count as declining. Matched case-insensitively; the model is trained on the first.
_DECLINES = ("no ho sé", "no ho sé del cert", "no tinc", "no consta", "no puc confirmar")


def check_health(system: System) -> tuple[Finding, ...]:
    """The index is part of health, not just the process.

    A service whose model is loaded and whose collection is empty answers every question with
    *"no ho sé"* while returning 200. That reads as a well-behaved model and is a broken deploy,
    which is why this check exists before any question is asked.
    """
    try:
        health = system.health()
    except Exception as exc:  # the endpoint being unreachable is itself the finding
        return (Finding(Layer.SERVING, Severity.BROKEN, "health", f"unreachable: {exc}"),)

    findings: list[Finding] = []
    if not health.get("model_ready"):
        findings.append(
            Finding(Layer.SERVING, Severity.BROKEN, "health", "the model is not loaded")
        )
    if not health.get("index_ready"):
        findings.append(
            Finding(Layer.RETRIEVAL, Severity.BROKEN, "health", "the index is not ready")
        )
    elif not health.get("indexed_chunks"):
        findings.append(
            Finding(
                Layer.RETRIEVAL,
                Severity.BROKEN,
                "health",
                "the index reports ready with 0 chunks: every answer will be 'no ho sé' and the "
                "service will look healthy while doing it",
            )
        )
    return tuple(findings)


def check_case(
    system: System, case: Case, *, restricted_texts: Sequence[str] = ()
) -> tuple[Finding, ...]:
    """Run one case and triage whatever went wrong."""
    try:
        answer = system.ask(case.question)
    except Exception as exc:
        return (Finding(Layer.SERVING, Severity.BROKEN, case.question, f"request failed: {exc}"),)

    findings: list[Finding] = []

    if answer.status_code >= 500:
        return (
            Finding(Layer.SERVING, Severity.BROKEN, case.question, f"HTTP {answer.status_code}"),
        )
    if answer.status_code >= 400:
        return (
            Finding(
                Layer.SERVING,
                Severity.BROKEN,
                case.question,
                f"HTTP {answer.status_code}: the client and the contract disagree",
            ),
        )

    if not answer.text.strip():
        findings.append(Finding(Layer.GENERATION, Severity.BROKEN, case.question, "empty answer"))
    elif not is_catalan(answer.text):
        # Gemma's instruction tuning is overwhelmingly English; drifting out of Catalan is the
        # first thing a template or system-prompt regression does.
        findings.append(
            Finding(
                Layer.GENERATION,
                Severity.WRONG,
                case.question,
                "the answer is not in Catalan",
            )
        )

    # Compliance first among the content checks: it is the only failure here that cannot be undone.
    for restricted in restricted_texts:
        if restricted and restricted in answer.text:
            findings.append(
                Finding(
                    Layer.COMPLIANCE,
                    Severity.COMPLIANCE,
                    case.question,
                    "a no-redistribute passage was reproduced verbatim in the answer",
                )
            )

    if case.needs_sources:
        if not answer.retrieved:
            findings.append(
                Finding(
                    Layer.RETRIEVAL,
                    Severity.WRONG,
                    case.question,
                    "the retriever returned nothing for a question the corpus covers",
                )
            )
        elif not answer.sources:
            # The distinction M5.09 exists for: the index worked and the answer did not use it.
            findings.append(
                Finding(
                    Layer.GENERATION,
                    Severity.WRONG,
                    case.question,
                    f"{len(answer.retrieved)} passage(s) retrieved but the answer cites none",
                )
            )

    if case.must_contain and not _declines(answer.text):
        findings.append(
            Finding(
                Layer.GENERATION,
                Severity.WRONG,
                case.question,
                "answered a question nothing in the corpus can support instead of declining",
            )
        )

    if answer.seconds > P95_WARM_SECONDS:
        findings.append(
            Finding(
                Layer.CAPACITY,
                Severity.SLOW,
                case.question,
                f"{answer.seconds:.1f}s against a {P95_WARM_SECONDS:.0f}s warm target",
            )
        )

    return tuple(findings)


def _declines(text: str) -> bool:
    """Whether the answer declines rather than inventing."""
    lowered = text.lower()
    return any(phrase in lowered for phrase in _DECLINES)


@dataclass(frozen=True)
class Report:
    """Everything the run found."""

    findings: tuple[Finding, ...] = ()
    cases_run: int = 0

    @property
    def passed(self) -> bool:
        """A run with no findings. ``cases_run == 0`` is never a pass."""
        return not self.findings and self.cases_run > 0

    def by_layer(self) -> dict[Layer, list[Finding]]:
        """Findings grouped by owner, worst first inside each group."""
        grouped: dict[Layer, list[Finding]] = {}
        for finding in sorted(self.findings, key=lambda f: f.severity, reverse=True):
            grouped.setdefault(finding.layer, []).append(finding)
        return grouped

    @property
    def worst(self) -> Severity | None:
        """The severity to act on, or ``None`` when nothing failed."""
        return max((f.severity for f in self.findings), default=None)


def run(
    system: System,
    *,
    cases: Sequence[Case] = CASES,
    restricted_texts: Sequence[str] = (),
    include_honesty_case: bool = True,
) -> Report:
    """Run the suite. Health first — every later finding would be a consequence of a bad deploy."""
    findings = list(check_health(system))
    all_cases = [*cases, *([UNANSWERABLE] if include_honesty_case else [])]
    for case in all_cases:
        findings.extend(check_case(system, case, restricted_texts=restricted_texts))
    return Report(tuple(findings), cases_run=len(all_cases))


def render(report: Report) -> str:
    """Markdown for the DoD-F5 evidence, grouped by the team that owns the fix."""
    lines = ["# M5.08 — end-to-end", ""]
    if report.cases_run == 0:
        lines += ["**FAIL** — NOT RUN: no cases were executed."]
        return "\n".join(lines) + "\n"
    if report.passed:
        lines += [f"**PASS** — {report.cases_run} case(s), no findings."]
        return "\n".join(lines) + "\n"

    worst = report.worst
    assert worst is not None  # not passed and cases_run > 0 means at least one finding
    lines += [f"**FAIL** — worst: **{worst.name}**. {report.cases_run} case(s) run.", ""]
    for layer, findings in report.by_layer().items():
        lines.append(f"## {layer.value} ({len(findings)})")
        lines += [f"- **{f.severity.name}** — {f.check}: {f.detail}" for f in findings]
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point over a recorded run.

    Running the suite needs a deployed system, which does not exist yet. Reading a recorded run
    from JSON keeps the triage — the part with the logic in it — runnable and reviewable in CI.
    """
    parser = argparse.ArgumentParser(
        description="Triage a recorded end-to-end run (M5.08-09). Findings are grouped by the "
        "layer that owns them; the exit code is non-zero when anything failed."
    )
    parser.add_argument("recording", type=Path, help="JSON: {health: {...}, answers: [...]}")
    parser.add_argument("--out", type=Path, help="write the Markdown report here")
    args = parser.parse_args(argv)

    if not args.recording.is_file():
        print(f"error: no such file: {args.recording}", file=sys.stderr)
        return 1
    try:
        recorded = json.loads(args.recording.read_text(encoding="utf-8"))
        system = Recorded.from_json(recorded)
    except (ValueError, TypeError, KeyError, AttributeError) as exc:
        print(f"error: unreadable recording: {exc}", file=sys.stderr)
        return 1

    report = run(
        system,
        cases=system.cases,
        restricted_texts=recorded.get("restricted_texts", ()),
        include_honesty_case=False,
    )
    rendered = render(report)
    if args.out:
        args.out.write_text(rendered, encoding="utf-8")
    print(rendered)
    return 0 if report.passed else 1


@dataclass
class Recorded:
    """A :class:`System` replayed from a recorded run, for offline triage."""

    health_payload: dict[str, Any]
    answers: dict[str, Answer]
    cases: tuple[Case, ...] = field(default_factory=tuple)

    @classmethod
    def from_json(cls, payload: dict[str, Any]) -> Recorded:
        """Build from the recording format. Raises on anything it cannot read."""
        answers: dict[str, Answer] = {}
        cases: list[Case] = []
        for entry in payload["answers"]:
            question = str(entry["question"])
            answers[question] = Answer(
                text=str(entry.get("text", "")),
                sources=tuple(entry.get("sources", ())),
                retrieved=tuple(str(text) for text in entry.get("retrieved", ())),
                seconds=float(entry.get("seconds", 0.0)),
                status_code=int(entry.get("status_code", 200)),
            )
            cases.append(
                Case(
                    question,
                    needs_sources=bool(entry.get("needs_sources", True)),
                    must_contain=entry.get("must_contain"),
                )
            )
        return cls(dict(payload["health"]), answers, tuple(cases))

    def health(self) -> dict[str, Any]:
        return self.health_payload

    def ask(self, question: str, *, rag: bool = True) -> Answer:
        """Replay. A question with no recording is a gap in the recording, not an empty answer."""
        if question not in self.answers:
            raise KeyError(f"no recorded answer for {question!r}")
        return self.answers[question]


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
