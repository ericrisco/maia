"""Tests for the serverless vLLM endpoint configuration (PLAN M5.06 step 4, DoD-F5)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from maia.serving.serverless import (
    DEFAULT,
    EndpointConfig,
    Gpu,
    check,
    cold_start_note,
    kv_cache_gib,
    main,
    render,
    weights_gib,
)


@pytest.mark.unit
def test_bf16_does_not_fit_a_24_gib_card_and_awq_does() -> None:
    """The decision the whole module exists to make. A 12B in bf16 is ~22 GiB of weights, so a
    24 GiB card has nothing left for the KV cache — and that endpoint *deploys fine*, serves one
    short request, then OOMs on a long context in front of whoever is watching the demo."""
    bf16 = EndpointConfig(name="x", model="m", gpu=Gpu.L4_24, precision="bf16")
    assert not bf16.fits()
    assert "OOM" in check(bf16)[0]

    awq = EndpointConfig(name="x", model="m", gpu=Gpu.L4_24, precision="awq")
    assert awq.fits()
    assert check(awq) == ()


@pytest.mark.unit
def test_bf16_fits_once_the_card_is_big_enough() -> None:
    assert EndpointConfig(name="x", model="m", gpu=Gpu.L40S_48, precision="bf16").fits()


@pytest.mark.unit
def test_the_kv_cache_is_sized_for_the_worst_case_not_the_average() -> None:
    """Full context times full concurrency. Sizing for the average is how an endpoint survives its
    demo and dies the day several people use it at once."""
    one = kv_cache_gib(max_context=8192, concurrency=1)
    four = kv_cache_gib(max_context=8192, concurrency=4)
    assert four == pytest.approx(one * 4)
    assert kv_cache_gib(max_context=16384, concurrency=1) == pytest.approx(one * 2)


@pytest.mark.unit
def test_context_length_can_push_a_fitting_config_over() -> None:
    """The cache is not a rounding error: at 4x the context it is larger than the AWQ weights."""
    roomy = EndpointConfig(name="x", model="m", gpu=Gpu.L4_24, precision="awq")
    assert roomy.fits()
    long_context = EndpointConfig(
        name="x", model="m", gpu=Gpu.L4_24, precision="awq", max_context=32768
    )
    assert not long_context.fits()


@pytest.mark.unit
def test_weights_reject_a_precision_this_project_does_not_serve() -> None:
    """A typo falling back to a default would size the deploy for the wrong model."""
    with pytest.raises(ValueError, match="unknown precision"):
        weights_gib("fp8")
    assert weights_gib("bf16") > weights_gib("awq")
    bad = EndpointConfig(name="x", model="m", gpu=Gpu.A100_80, precision="fp8")
    assert any("unknown precision" in problem for problem in check(bad))


@pytest.mark.unit
def test_a_worker_count_that_cannot_serve_is_a_failure() -> None:
    assert any("never serve" in p for p in check(_ok(max_workers=0)))
    assert any("above max_workers" in p for p in check(_ok(min_workers=3, max_workers=2)))


@pytest.mark.unit
def test_a_short_idle_timeout_makes_every_turn_a_cold_start() -> None:
    """Scale-to-zero plus a 30 s idle window means a user who reads the answer before typing the
    next question pays a container start and a weight load on every single turn."""
    problems = check(_ok(idle_timeout_s=30))
    assert any("cold start on every turn" in p for p in problems)
    # The same timeout is harmless when a worker is always resident.
    assert check(_ok(idle_timeout_s=30, min_workers=1)) == ()


@pytest.mark.unit
def test_the_cold_start_note_names_the_target_and_the_real_fix() -> None:
    """Not a prediction — nothing is measured yet, and an invented number is worse than none. It
    says which regime the config is in and that the fix for missing the target costs money."""
    zero = cold_start_note(_ok())
    assert "20s target" in zero
    assert "min_workers ≥ 1" in zero
    assert "cost decision" in zero

    warm = cold_start_note(_ok(min_workers=1))
    assert "no cold start" in warm
    assert not _ok(min_workers=1).scales_to_zero


@pytest.mark.unit
def test_the_deploy_request_carries_no_secrets() -> None:
    """It is committed as DoD-F5 evidence. The API key is PO-custodied and read from the
    environment by whoever runs the deploy."""
    request = DEFAULT.to_request()
    blob = json.dumps(request).lower()
    for forbidden in ("key", "token", "secret", "password", "api_key"):
        assert forbidden not in blob
    assert request["workersMin"] == 0
    env = request["env"]
    assert isinstance(env, dict)
    assert env["QUANTIZATION"] == "awq"
    assert env["MODEL_NAME"] == DEFAULT.model


@pytest.mark.unit
def test_bf16_request_omits_the_quantization_flag() -> None:
    """Passing `QUANTIZATION=awq` to a bf16 checkpoint fails at load, not at deploy."""
    env = EndpointConfig(name="x", model="m", gpu=Gpu.A100_80, precision="bf16").to_request()["env"]
    assert isinstance(env, dict)
    assert "QUANTIZATION" not in env


@pytest.mark.unit
def test_the_shipped_default_is_deployable() -> None:
    assert check(DEFAULT) == ()
    assert DEFAULT.scales_to_zero


@pytest.mark.unit
def test_render_shows_pass_and_fail() -> None:
    assert "**PASS**" in render(DEFAULT)
    failed = render(EndpointConfig(name="x", model="m", gpu=Gpu.L4_24, precision="bf16"))
    assert "**FAIL**" in failed
    assert "OOM" in failed


@pytest.mark.unit
def test_cli_writes_the_report_and_the_request(tmp_path: Path) -> None:
    report, request = tmp_path / "r.md", tmp_path / "r.json"
    assert main(["--out", str(report), "--request", str(request)]) == 0
    assert "**PASS**" in report.read_text(encoding="utf-8")
    assert json.loads(request.read_text(encoding="utf-8"))["name"] == DEFAULT.name


@pytest.mark.unit
def test_cli_fails_an_undeployable_configuration(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["--gpu", Gpu.L4_24.value, "--precision", "bf16"]) == 1
    assert "problem(s)" in capsys.readouterr().err


def _ok(**overrides: object) -> EndpointConfig:
    """A configuration that passes, so each test changes exactly one thing."""
    base: dict[str, object] = {
        "name": "maia",
        "model": "m",
        "gpu": Gpu.L4_24,
        "precision": "awq",
    }
    return EndpointConfig(**{**base, **overrides})  # type: ignore[arg-type]
