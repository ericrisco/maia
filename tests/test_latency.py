"""Tests for the M5.06 p95 latency gate (PLAN M5.06, DoD-F5)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from maia.serving.latency import (
    MIN_COLD_SAMPLES,
    MIN_WARM_SAMPLES,
    P95_COLD_SECONDS,
    P95_WARM_SECONDS,
    Latency,
    gate,
    main,
    measure,
    report,
)


def _warm(seconds: float, count: int = MIN_WARM_SAMPLES) -> tuple[float, ...]:
    return (seconds,) * count


def _cold(seconds: float, count: int = MIN_COLD_SAMPLES) -> tuple[float, ...]:
    return (seconds,) * count


@pytest.mark.unit
def test_the_targets_are_the_ones_the_po_decided() -> None:
    """Pinned: D-0043 fixed these, and a threshold that drifts quietly is not a decision."""
    assert P95_COLD_SECONDS == 20.0
    assert P95_WARM_SECONDS == 2.0


@pytest.mark.unit
def test_a_deployment_inside_both_targets_passes() -> None:
    assert gate(Latency(cold=_cold(18.0), warm=_warm(1.2))) == ()


@pytest.mark.unit
def test_cold_and_warm_are_gated_separately() -> None:
    """The reason there are two targets: a cold start slow enough to fail on its own disappears
    into an average dominated by warm requests, and the gate would pass a deployment whose first
    request takes a minute."""
    slow_cold = Latency(cold=_cold(45.0), warm=_warm(0.5))
    failures = gate(slow_cold)
    assert len(failures) == 1
    assert failures[0].startswith("cold: p95 45.0s")

    slow_warm = Latency(cold=_cold(5.0), warm=_warm(9.0))
    failures = gate(slow_warm)
    assert len(failures) == 1
    assert failures[0].startswith("warm: p95 9.0s")


@pytest.mark.unit
def test_a_stage_that_measured_nothing_fails_rather_than_passes() -> None:
    """The blocked-by-resource convention. An empty sample set is the exact shape a broken harness
    has — a deploy that never happened, a probe that errored — and it must never read as a pass."""
    failures = gate(Latency())
    assert len(failures) == 2
    assert all("NOT RUN" in reason for reason in failures)
    assert Latency().p95_cold is None
    assert Latency().p95_warm is None


@pytest.mark.unit
def test_too_few_samples_is_not_a_percentile() -> None:
    """At n=10 the nearest-rank p95 is the slowest sample, so one unlucky request fails the gate
    and one lucky run passes it. Below the minimum the answer is NOT RUN, not a verdict."""
    thin = Latency(cold=_cold(1.0, MIN_COLD_SAMPLES - 1), warm=_warm(0.1, MIN_WARM_SAMPLES - 1))
    failures = gate(thin)
    assert len(failures) == 2
    assert all("NOT RUN" in reason for reason in failures)
    # Fast enough to pass on the numbers alone — it is the sample count that fails it.
    assert thin.p95_warm == 0.1


@pytest.mark.unit
def test_p95_ignores_the_slowest_tail() -> None:
    """A p95 that the worst sample can move on its own is a max. One outlier in twenty must not
    fail a deployment that is otherwise inside the target."""
    warm = (*(0.5,) * 19, 30.0)
    assert Latency(cold=_cold(1.0), warm=warm).p95_warm == 0.5
    assert gate(Latency(cold=_cold(1.0), warm=warm)) == ()


@pytest.mark.unit
def test_exactly_on_target_passes() -> None:
    """``>`` not ``>=``: a deployment that meets the number meets it."""
    assert gate(Latency(cold=_cold(P95_COLD_SECONDS), warm=_warm(P95_WARM_SECONDS))) == ()


@pytest.mark.unit
def test_measure_keeps_the_two_temperatures_apart() -> None:
    durations = iter([21.0, 22.0, 23.0, *(0.4,) * MIN_WARM_SAMPLES])
    measured = measure(lambda: next(durations), cold_samples=3, warm_samples=MIN_WARM_SAMPLES)
    assert measured.cold == (21.0, 22.0, 23.0)
    assert measured.warm == (0.4,) * MIN_WARM_SAMPLES


@pytest.mark.unit
def test_the_report_carries_the_samples_not_just_the_verdict() -> None:
    """A later reader must be able to recompute the percentile instead of trusting this code."""
    measured = Latency(cold=_cold(19.0), warm=_warm(1.0))
    payload = json.loads(measured.to_json())
    assert payload["cold_seconds"] == list(measured.cold)
    assert payload["warm_seconds"] == list(measured.warm)
    assert payload["p95_cold_seconds"] == 19.0
    assert payload["target_warm_seconds"] == P95_WARM_SECONDS


@pytest.mark.unit
def test_report_renders_pass_and_fail() -> None:
    assert "**PASS**" in report(Latency(cold=_cold(1.0), warm=_warm(0.1)))
    failed = report(Latency(cold=_cold(99.0), warm=_warm(0.1)))
    assert "**FAIL**" in failed
    assert "p95 99.0s" in failed
    assert "NOT RUN" in report(Latency())


@pytest.mark.unit
def test_cli_passes_writes_and_fails(tmp_path: Path) -> None:
    good = tmp_path / "good.json"
    good.write_text(
        json.dumps({"cold_seconds": [15.0, 16.0, 17.0], "warm_seconds": [1.0] * MIN_WARM_SAMPLES}),
        encoding="utf-8",
    )
    out = tmp_path / "report.md"
    assert main([str(good), "--out", str(out)]) == 0
    assert "**PASS**" in out.read_text(encoding="utf-8")

    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"cold_seconds": [90.0] * 3}), encoding="utf-8")
    assert main([str(bad)]) == 1


@pytest.mark.unit
def test_cli_rejects_a_missing_or_unreadable_file(tmp_path: Path) -> None:
    assert main([str(tmp_path / "nope.json")]) == 1
    broken = tmp_path / "broken.json"
    broken.write_text("[not an object]", encoding="utf-8")
    assert main([str(broken)]) == 1
    wrong_type = tmp_path / "wrong.json"
    wrong_type.write_text(json.dumps({"cold_seconds": ["fast"]}), encoding="utf-8")
    assert main([str(wrong_type)]) == 1
