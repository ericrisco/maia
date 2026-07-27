"""Serverless vLLM endpoint configuration — PLAN M5.06 step 4, *"serverless vLLM on RunPod
serving the merged model (bf16/AWQ), on-demand"*, and half of DoD-F5.

The deploy itself is **blocked-by-resource**: it needs a RunPod account, a paid GPU and a merged
model that does not exist yet. What *can* be built now is everything that decides whether the
deploy will work, and that turns out to be most of it — the ways a serverless LLM endpoint fails
are configuration mistakes, and they are all checkable on paper:

**The GPU has to fit the weights, and the weights are not the whole story.** A 12B model in bf16 is
about 23 GiB of parameters. On a 24 GiB card that leaves roughly nothing for the KV cache, and the
endpoint does not fail at deploy time — it deploys, serves one short request, and then OOMs on the
first long context. :func:`fits` accounts for weights, KV cache at the configured context length
and concurrency, and vLLM's own overhead, so the failure surfaces here instead of in production.

**Scale-to-zero is the entire cost model and the entire latency problem.** ``min_workers = 0`` is
what makes a demo affordable, and it is also what makes the first request pay for a container start
plus a multi-gigabyte weight load. That is the D-0043 cold target. This module refuses to pretend
the two are independent: :func:`check` fails a configuration whose *stated* cold budget is smaller
than what a cold start plausibly costs, because the honest fix is a warm worker — a budget
decision — and not a smaller number in a config file.

**An idle timeout shorter than a conversation turns every turn into a cold start.** A user reading
a paragraph before typing the next question is idle for longer than the default anyone reaches for.

Secrets never appear here. The API key is PO-custodied and read from the environment by whoever
runs the deploy; :meth:`EndpointConfig.to_request` emits the endpoint spec and nothing else, so the
result is safe to commit as DoD-F5 evidence.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path

from maia.serving.latency import P95_COLD_SECONDS

#: Parameter count of the model being served, in billions (Gemma 4 12B).
MODEL_PARAMS_B = 12.0

#: Bytes per parameter for the two precisions M5.06 names. AWQ is 4-bit weights plus scales and
#: zero-points, which is why it is 0.6 and not 0.5 — the difference is ~1.4 GiB on a 12B model,
#: enough to decide whether a 24 GiB card fits.
_BYTES_PER_PARAM = {"bf16": 2.0, "awq": 0.6}

#: Gemma 4 12B geometry, for the KV cache: 48 layers, 8 key-value heads (GQA), 128 head dim, and
#: two tensors (K and V) at 2 bytes each. Per token, per sequence: 48 * 8 * 128 * 2 * 2 bytes.
_KV_BYTES_PER_TOKEN = 48 * 8 * 128 * 2 * 2

#: vLLM's non-weight, non-cache footprint: CUDA graphs, activations, the framework itself. A flat
#: allowance rather than a derivation, because it is dominated by things that do not scale with the
#: model — but omitting it is how a configuration that fits on paper OOMs on the machine.
_RUNTIME_OVERHEAD_GIB = 2.0

#: vLLM will not allocate the whole card; the default `gpu_memory_utilization` is 0.90 and raising
#: it is how people cause allocator failures under load.
_USABLE_FRACTION = 0.90

_GIB = 1024**3


class Gpu(StrEnum):
    """The serverless GPU tiers worth considering, by VRAM.

    Names match RunPod's, so a config maps to a real deploy without a translation table nobody
    maintains.
    """

    A10G_24 = "NVIDIA A10G"
    L4_24 = "NVIDIA L4"
    L40S_48 = "NVIDIA L40S"
    A100_80 = "NVIDIA A100 80GB"
    H100_80 = "NVIDIA H100 80GB"

    @property
    def vram_gib(self) -> int:
        """Physical VRAM. Not what a model may use — see :data:`_USABLE_FRACTION`."""
        return {
            Gpu.A10G_24: 24,
            Gpu.L4_24: 24,
            Gpu.L40S_48: 48,
            Gpu.A100_80: 80,
            Gpu.H100_80: 80,
        }[self]


def weights_gib(precision: str) -> float:
    """On-GPU size of the weights for ``precision``.

    Raises:
        ValueError: for a precision this project does not serve. M5.06 names bf16 and AWQ; a typo
            silently falling back to one of them would size the deploy for the wrong model.
    """
    if precision not in _BYTES_PER_PARAM:
        raise ValueError(
            f"unknown precision {precision!r}: expected one of {sorted(_BYTES_PER_PARAM)}"
        )
    return MODEL_PARAMS_B * 1e9 * _BYTES_PER_PARAM[precision] / _GIB


def kv_cache_gib(*, max_context: int, concurrency: int) -> float:
    """KV cache for ``concurrency`` sequences each at the full ``max_context``.

    The worst case on purpose. Sizing for the average is how an endpoint survives its demo and
    dies on the day several people use it at once.
    """
    return _KV_BYTES_PER_TOKEN * max_context * concurrency / _GIB


@dataclass(frozen=True)
class EndpointConfig:
    """A serverless vLLM endpoint, as configuration rather than as a deploy."""

    name: str
    model: str
    gpu: Gpu
    precision: str = "bf16"
    max_context: int = 8192
    concurrency: int = 4
    min_workers: int = 0
    max_workers: int = 2
    idle_timeout_s: int = 300
    #: Extra vLLM server flags. Kept as data so the deploy record shows exactly what ran.
    extra_args: tuple[str, ...] = field(default_factory=tuple)

    @property
    def required_gib(self) -> float:
        """Everything that has to be resident at once, at full context and full concurrency."""
        return (
            weights_gib(self.precision)
            + kv_cache_gib(max_context=self.max_context, concurrency=self.concurrency)
            + _RUNTIME_OVERHEAD_GIB
        )

    @property
    def available_gib(self) -> float:
        """What vLLM may actually allocate on this card."""
        return self.gpu.vram_gib * _USABLE_FRACTION

    def fits(self) -> bool:
        """True when the model, its worst-case cache and the runtime fit the card."""
        return self.required_gib <= self.available_gib

    @property
    def scales_to_zero(self) -> bool:
        """True when idle costs nothing — and every first request is a cold start."""
        return self.min_workers == 0

    def to_request(self) -> dict[str, object]:
        """The endpoint spec, as the deploy API wants it. **Contains no secrets.**"""
        return {
            "name": self.name,
            "gpu": self.gpu.value,
            "workersMin": self.min_workers,
            "workersMax": self.max_workers,
            "idleTimeout": self.idle_timeout_s,
            "env": {
                "MODEL_NAME": self.model,
                "MAX_MODEL_LEN": str(self.max_context),
                "MAX_NUM_SEQS": str(self.concurrency),
                **({"QUANTIZATION": "awq"} if self.precision == "awq" else {}),
            },
            "vllmArgs": list(self.extra_args),
        }


def check(config: EndpointConfig) -> tuple[str, ...]:
    """Everything wrong with ``config``. Empty means it is deployable.

    Every finding here is a failure that would otherwise appear *after* the deploy, in front of
    whoever is being shown the demo.
    """
    problems: list[str] = []

    # First and alone: every memory figure below is derived from the precision, so an unknown one
    # cannot be reported alongside the others — it makes them uncomputable.
    if config.precision not in _BYTES_PER_PARAM:
        return (
            f"unknown precision {config.precision!r}: expected one of "
            f"{sorted(_BYTES_PER_PARAM)}. Nothing else can be checked without it.",
        )

    if not config.fits():
        problems.append(
            f"{config.gpu.value} has {config.gpu.vram_gib} GiB "
            f"({config.available_gib:.1f} usable) but this needs {config.required_gib:.1f} GiB: "
            f"{weights_gib(config.precision):.1f} weights + "
            f"{kv_cache_gib(max_context=config.max_context, concurrency=config.concurrency):.1f} "
            f"KV at {config.max_context} tokens x {config.concurrency} + "
            f"{_RUNTIME_OVERHEAD_GIB:.1f} runtime. It serves short requests and OOMs on long ones."
        )

    if config.max_workers < 1:
        problems.append("max_workers < 1: the endpoint can never serve a request")
    if config.min_workers > config.max_workers:
        problems.append(
            f"min_workers ({config.min_workers}) above max_workers ({config.max_workers})"
        )

    if config.idle_timeout_s < 60 and config.scales_to_zero:
        problems.append(
            f"idle_timeout {config.idle_timeout_s}s with scale-to-zero: a user who reads an answer "
            "before asking the next question pays a cold start on every turn"
        )

    return tuple(problems)


def cold_start_note(config: EndpointConfig) -> str:
    """What this configuration means for the D-0043 cold-start target.

    Not a prediction — nothing here has been measured, and a made-up number would be worse than
    none. It states which regime the configuration is in, and that the target applies.
    """
    if config.scales_to_zero:
        return (
            f"Scales to zero: every request after {config.idle_timeout_s}s idle pays a container "
            f"start plus a {weights_gib(config.precision):.0f} GiB weight load. That is the "
            f"p95 cold ≤ {P95_COLD_SECONDS:.0f}s target (D-0043), and it is the number to measure "
            "first. If it misses, the fix is min_workers ≥ 1 — a cost decision, not a tuning one."
        )
    return (
        f"min_workers = {config.min_workers}: a worker is always resident, so there is no cold "
        "start and no scale-to-zero saving. The warm target still applies."
    )


def render(config: EndpointConfig) -> str:
    """Markdown for the DoD-F5 evidence: the configuration, its verdict and its cost regime."""
    problems = check(config)
    lines = [
        f"# M5.06 — serverless endpoint `{config.name}`",
        "",
        f"- **Model**: `{config.model}` ({config.precision})",
        f"- **GPU**: {config.gpu.value} — {config.gpu.vram_gib} GiB, "
        f"{config.available_gib:.1f} usable",
        f"- **Memory**: {config.required_gib:.1f} GiB required at {config.max_context} tokens x "
        f"{config.concurrency} concurrent",
        f"- **Workers**: {config.min_workers}-{config.max_workers}, "
        f"idle timeout {config.idle_timeout_s}s",
        "",
        cold_start_note(config),
        "",
        "**FAIL**" if problems else "**PASS** — deployable as configured",
    ]
    lines += [f"- {problem}" for problem in problems]
    return "\n".join(lines) + "\n"


#: The default deploy: AWQ on a 24 GiB card. bf16 needs a 48 GiB card that costs several times as
#: much for a demo endpoint, and M5.02 already requires the quantised model to retain ≥95 % of the
#: merged AndBench score — so if AWQ is not good enough, that gate says so before this one does.
DEFAULT = EndpointConfig(
    name="maia-12b-it",
    model="ericrisco/maia-12b-it",
    gpu=Gpu.L4_24,
    precision="awq",
)


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point. Renders and checks an endpoint configuration; non-zero when unusable."""
    parser = argparse.ArgumentParser(
        description="Check and render the M5.06 serverless vLLM endpoint configuration. "
        "Deploying is blocked-by-resource; this validates the configuration that will be deployed."
    )
    parser.add_argument("--name", default=DEFAULT.name)
    parser.add_argument("--model", default=DEFAULT.model)
    parser.add_argument("--gpu", default=DEFAULT.gpu.value, choices=[g.value for g in Gpu])
    parser.add_argument("--precision", default=DEFAULT.precision, choices=sorted(_BYTES_PER_PARAM))
    parser.add_argument("--max-context", type=int, default=DEFAULT.max_context)
    parser.add_argument("--concurrency", type=int, default=DEFAULT.concurrency)
    parser.add_argument("--min-workers", type=int, default=DEFAULT.min_workers)
    parser.add_argument("--max-workers", type=int, default=DEFAULT.max_workers)
    parser.add_argument("--idle-timeout", type=int, default=DEFAULT.idle_timeout_s)
    parser.add_argument("--out", type=Path, help="write the Markdown report here")
    parser.add_argument("--request", type=Path, help="write the deploy request JSON here")
    args = parser.parse_args(argv)

    config = EndpointConfig(
        name=args.name,
        model=args.model,
        gpu=Gpu(args.gpu),
        precision=args.precision,
        max_context=args.max_context,
        concurrency=args.concurrency,
        min_workers=args.min_workers,
        max_workers=args.max_workers,
        idle_timeout_s=args.idle_timeout,
    )

    rendered = render(config)
    if args.out:
        args.out.write_text(rendered, encoding="utf-8")
    if args.request:
        args.request.write_text(
            json.dumps(config.to_request(), indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(rendered)
    if problems := check(config):
        print(f"{len(problems)} problem(s)", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
