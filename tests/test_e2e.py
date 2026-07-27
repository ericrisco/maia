"""Tests for the end-to-end smoke test and its triage (PLAN M5.08-09, DoD-F5)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from maia.serving.e2e import (
    CASES,
    UNANSWERABLE,
    Answer,
    Case,
    Layer,
    Recorded,
    Report,
    Severity,
    check_case,
    check_health,
    main,
    render,
    run,
)

CATALAN = (
    "Una llei qualificada regula els drets fonamentals i requereix una majoria reforçada del "
    "Consell General, mentre que una llei ordinària s'aprova per majoria simple."
)
HEALTHY = {"model_ready": True, "index_ready": True, "indexed_chunks": 4200}
SOURCE = {"url": "https://portaljuridicandorra.ad/x", "llei": "Constitució", "article": "Art. 3"}


class FakeSystem:
    """A system whose every failure mode can be dialled in."""

    def __init__(
        self,
        *,
        health: dict[str, Any] | None = None,
        answer: Answer | None = None,
        raise_on_ask: Exception | None = None,
        raise_on_health: Exception | None = None,
    ) -> None:
        self._health = HEALTHY if health is None else health
        self._answer = answer if answer is not None else _good()
        self._raise_on_ask = raise_on_ask
        self._raise_on_health = raise_on_health

    def health(self) -> dict[str, Any]:
        if self._raise_on_health:
            raise self._raise_on_health
        return self._health

    def ask(self, question: str, *, rag: bool = True) -> Answer:
        if self._raise_on_ask:
            raise self._raise_on_ask
        return self._answer


def _good(**overrides: Any) -> Answer:
    base: dict[str, Any] = {
        "text": CATALAN,
        "sources": (SOURCE,),
        "retrieved": ("El Consell General aprova les lleis qualificades...",),
        "seconds": 1.0,
        "status_code": 200,
    }
    return Answer(**{**base, **overrides})


LEGAL = Case("Què és una llei qualificada?")


# ── health, before anything else ─────────────────────────────────────────────


@pytest.mark.unit
def test_an_empty_index_reporting_ready_is_the_failure_this_check_exists_for() -> None:
    """The deploy that looks healthiest while being most broken: the model is loaded, the
    collection is empty, every answer is "no ho sé", and the service returns 200 throughout. It
    reads as a well-behaved model."""
    findings = check_health(FakeSystem(health={**HEALTHY, "indexed_chunks": 0}))
    assert [f.layer for f in findings] == [Layer.RETRIEVAL]
    assert "look healthy while doing it" in findings[0].detail


@pytest.mark.unit
def test_health_separates_a_missing_model_from_a_missing_index() -> None:
    """Different layers, different owners — the entire point of M5.09."""
    findings = check_health(
        FakeSystem(health={"model_ready": False, "index_ready": False, "indexed_chunks": 0})
    )
    assert {f.layer for f in findings} == {Layer.SERVING, Layer.RETRIEVAL}


@pytest.mark.unit
def test_an_unreachable_endpoint_is_itself_the_finding() -> None:
    findings = check_health(FakeSystem(raise_on_health=ConnectionError("refused")))
    assert findings[0].layer is Layer.SERVING
    assert findings[0].severity is Severity.BROKEN


@pytest.mark.unit
def test_a_healthy_system_produces_nothing() -> None:
    assert check_health(FakeSystem()) == ()


# ── the triage distinctions ──────────────────────────────────────────────────


@pytest.mark.unit
def test_retrieval_finding_nothing_and_generation_ignoring_it_are_different_layers() -> None:
    """The distinction M5.09 exists to make. Both look like "no sources in the answer" from the
    outside, and they are owned by different people: one is an index or embedding problem, the
    other is a prompt or template problem."""
    nothing_retrieved = check_case(FakeSystem(answer=_good(retrieved=(), sources=())), LEGAL)
    assert [f.layer for f in nothing_retrieved] == [Layer.RETRIEVAL]

    retrieved_but_ignored = check_case(FakeSystem(answer=_good(sources=())), LEGAL)
    assert [f.layer for f in retrieved_but_ignored] == [Layer.GENERATION]
    assert "cites none" in retrieved_but_ignored[0].detail


@pytest.mark.unit
def test_a_verbatim_restricted_passage_outranks_everything_else() -> None:
    """The worst thing this system can do: a licence breach, public, and silent. It ranks above a
    wrong answer and above a system that is simply down, because only this one cannot be undone."""
    secret = "Text íntegre d'una font amb llicència restringida."
    findings = check_case(
        FakeSystem(answer=_good(text=f"{CATALAN} {secret}")),
        LEGAL,
        restricted_texts=[secret],
    )
    assert findings[0].layer is Layer.COMPLIANCE
    assert findings[0].severity is Severity.COMPLIANCE
    assert Severity.COMPLIANCE > Severity.BROKEN > Severity.WRONG > Severity.SLOW


@pytest.mark.unit
def test_an_empty_restricted_string_does_not_match_everything() -> None:
    """`"" in text` is always true; an empty entry in the restricted list would flag every answer
    as a licence breach and make the most important check in the suite worthless."""
    assert check_case(FakeSystem(), LEGAL, restricted_texts=[""]) == ()


@pytest.mark.unit
def test_an_answer_that_drifts_out_of_catalan_is_a_generation_failure() -> None:
    """Gemma's instruction tuning is overwhelmingly English, so this is the first symptom of a
    template or system-prompt regression."""
    findings = check_case(
        FakeSystem(
            answer=_good(
                text="A qualified law regulates fundamental rights and needs a reinforced majority."
            )
        ),
        LEGAL,
    )
    assert [f.layer for f in findings] == [Layer.GENERATION]
    assert "not in Catalan" in findings[0].detail


@pytest.mark.unit
def test_an_empty_answer_is_reported_once_not_twice() -> None:
    """Empty text is not "not Catalan" as well — two findings for one fault split the triage."""
    findings = check_case(FakeSystem(answer=_good(text="   ")), LEGAL)
    assert len(findings) == 1
    assert findings[0].detail == "empty answer"


@pytest.mark.unit
def test_inventing_an_answer_to_an_unanswerable_question_is_caught() -> None:
    """A model that invents a confident answer here invents one for a legal question too, and this
    is the cheapest place to find that out."""
    invented = check_case(
        FakeSystem(answer=_good(text="Van néixer disset persones aquell dia a Ordino.")),
        UNANSWERABLE,
    )
    assert any("instead of declining" in f.detail for f in invented)

    declined = check_case(
        FakeSystem(answer=_good(text="No ho sé: no tinc cap font que ho pugui confirmar.")),
        UNANSWERABLE,
    )
    assert declined == ()


@pytest.mark.unit
@pytest.mark.parametrize("status", [400, 401, 429, 500, 503])
def test_an_http_error_short_circuits_the_content_checks(status: int) -> None:
    """Judging the content of an error body produces findings about the wrong layer."""
    findings = check_case(FakeSystem(answer=_good(text="", status_code=status)), LEGAL)
    assert len(findings) == 1
    assert findings[0].layer is Layer.SERVING


@pytest.mark.unit
def test_a_request_that_raises_is_a_serving_failure() -> None:
    findings = check_case(FakeSystem(raise_on_ask=TimeoutError("timed out")), LEGAL)
    assert findings[0].layer is Layer.SERVING


@pytest.mark.unit
def test_a_correct_but_slow_answer_is_capacity_not_correctness() -> None:
    """It would otherwise be filed against whoever owns the model, who cannot fix it."""
    findings = check_case(FakeSystem(answer=_good(seconds=9.0)), LEGAL)
    assert [f.layer for f in findings] == [Layer.CAPACITY]
    assert findings[0].severity is Severity.SLOW


@pytest.mark.unit
def test_a_question_the_weights_should_answer_alone_needs_no_sources() -> None:
    lexical = Case("Què vol dir «plegar»?", needs_sources=False)
    assert check_case(FakeSystem(answer=_good(sources=(), retrieved=())), lexical) == ()


# ── the report ───────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_clean_run_passes_and_covers_the_shipped_cases() -> None:
    report = run(FakeSystem(answer=_good(text=f"{CATALAN} No ho sé del cert.")))
    assert report.passed
    assert report.cases_run == len(CASES) + 1
    assert report.worst is None


@pytest.mark.unit
def test_a_run_with_no_cases_is_never_a_pass() -> None:
    """The blocked-by-resource convention: an unmeasured stage fails its gate."""
    empty = Report()
    assert not empty.passed
    assert "NOT RUN" in render(empty)


@pytest.mark.unit
def test_the_report_groups_by_owner_and_names_the_worst_first() -> None:
    secret = "passatge restringit"
    report = run(
        FakeSystem(
            health={**HEALTHY, "indexed_chunks": 0},
            answer=_good(text=f"{CATALAN} {secret}", sources=(), seconds=30.0),
        ),
        restricted_texts=[secret],
    )
    assert not report.passed
    assert report.worst is Severity.COMPLIANCE

    grouped = report.by_layer()
    assert {Layer.RETRIEVAL, Layer.COMPLIANCE, Layer.GENERATION, Layer.CAPACITY} <= set(grouped)
    # Inside a layer, the worst finding is first.
    severities = [f.severity for f in grouped[Layer.GENERATION]]
    assert severities == sorted(severities, reverse=True)

    rendered = render(report)
    assert "worst: **COMPLIANCE**" in rendered
    assert "## compliance" in rendered


@pytest.mark.unit
def test_render_says_pass_plainly() -> None:
    assert "**PASS**" in render(run(FakeSystem(), include_honesty_case=False))


# ── offline triage ───────────────────────────────────────────────────────────


def _recording(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "health": HEALTHY,
        "answers": [
            {
                "question": "Què és una llei qualificada?",
                "text": CATALAN,
                "sources": [SOURCE],
                "retrieved": ["El Consell General..."],
                "seconds": 1.2,
            }
        ],
    }
    return {**base, **overrides}


@pytest.mark.unit
def test_the_cli_triages_a_recorded_run(tmp_path: Path) -> None:
    path = tmp_path / "run.json"
    path.write_text(json.dumps(_recording()), encoding="utf-8")
    out = tmp_path / "report.md"
    assert main([str(path), "--out", str(out)]) == 0
    assert "**PASS**" in out.read_text(encoding="utf-8")


@pytest.mark.unit
def test_the_cli_fails_and_names_the_layer(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    broken = _recording(
        answers=[
            {
                "question": "Què és una llei qualificada?",
                "text": CATALAN,
                "sources": [],
                "retrieved": [],
            }
        ]
    )
    path = tmp_path / "run.json"
    path.write_text(json.dumps(broken), encoding="utf-8")
    assert main([str(path)]) == 1
    assert "## retrieval" in capsys.readouterr().out


@pytest.mark.unit
def test_the_cli_rejects_a_missing_or_malformed_recording(tmp_path: Path) -> None:
    assert main([str(tmp_path / "nope.json")]) == 1
    for content in ("[]", json.dumps({"health": {}}), json.dumps({"answers": []})):
        path = tmp_path / "bad.json"
        path.write_text(content, encoding="utf-8")
        assert main([str(path)]) == 1


@pytest.mark.unit
def test_a_question_missing_from_the_recording_is_a_gap_not_an_empty_answer() -> None:
    """Silently returning nothing would be triaged as a generation failure that never happened."""
    recorded = Recorded.from_json(_recording())
    with pytest.raises(KeyError, match="no recorded answer"):
        recorded.ask("una pregunta que ningú va gravar")


@pytest.mark.unit
def test_a_finding_reads_as_a_log_line() -> None:
    """The triage has to survive being pasted into a chat message with no formatting."""
    finding = check_case(FakeSystem(answer=_good(seconds=9.0)), LEGAL)[0]
    assert str(finding).startswith("[SLOW/capacity] Què és una llei qualificada?: ")
