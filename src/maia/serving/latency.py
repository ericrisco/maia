"""The p95 latency gate — PLAN M5.06, *"serverless deploy + p95"*, and part of DoD-F5.

The plan left the target as a PO decision and nothing downstream could be built until it existed:
a gate with no threshold is not a gate. D-0043 sets it here, with the reasoning attached, because a
number in a YAML file with no argument behind it gets negotiated downward the first time it fails.

**Two targets, not one.** Serverless means the container is not running between requests. The first
request after a scale-to-zero pays for the container start *and* for pulling a multi-gigabyte
quantised model into memory; every request after it pays for neither. Averaging the two produces a
number that describes no real user: it is far too slow to represent the common case and far too
fast to represent the one users complain about. So cold and warm are measured separately and gated
separately, and a run that reports only one of them fails.

**Why 20 s cold.** It is what a container start plus a GGUF load actually costs on the hardware
this project can afford, and a target that the chosen architecture cannot meet is not a target, it
is a decision to change architecture. If 20 s is unacceptable for the demo, the fix is a warm
instance — a budget decision, not an optimisation — and this gate is where that shows up.

**Why 2 s warm.** A demo where the answer starts arriving in about a second reads as working;
several seconds of silence reads as broken, regardless of the answer. This bounds the full request,
not the first token: streaming makes perceived latency better than this number, never worse.

Measurement is **blocked-by-resource**: no deployment exists yet. The seam is :class:`Probe`, so
the gate is testable with a fake clock and no container. Per the project convention, a stage that
measured nothing prints ``NOT RUN`` and **fails** — :func:`gate` treats absent samples as a
failure, never as a pass, because an empty measurement is the exact shape a broken harness has.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from maia.percentiles import nearest_rank

#: p95 of the first request after a scale-to-zero: container start + model load, in seconds.
P95_COLD_SECONDS = 20.0

#: p95 of a request to an already-warm container, in seconds. Whole request, not first token.
P95_WARM_SECONDS = 2.0

#: Fewer samples than this and the "p95" is just the maximum wearing a percentile's name: at n=10
#: the nearest-rank p95 *is* the slowest sample, so a single unlucky request fails the gate and a
#: single lucky run passes it. Twenty is the smallest n where the 95th percentile is not the max.
MIN_WARM_SAMPLES = 20

#: Cold samples cost a scale-to-zero each, so they are minutes apart and few by nature. Three is
#: enough to catch a container that fails to start at all, which is what this measurement is for.
MIN_COLD_SAMPLES = 3


class Probe(Protocol):
    """One timed request against a deployed endpoint, in seconds.

    The seam that keeps M5.06 testable while the deployment is blocked-by-resource. Implementations
    time a real request; the tests supply a fake that returns fixed durations.
    """

    def __call__(self) -> float:
        """Return the wall-clock seconds a single complete request took."""


@dataclass(frozen=True)
class Latency:
    """Measured latencies for one deployment, in seconds, kept separate by temperature."""

    cold: tuple[float, ...] = ()
    warm: tuple[float, ...] = ()

    @property
    def p95_cold(self) -> float | None:
        """p95 of the cold samples, or ``None`` when nothing was measured."""
        return nearest_rank(sorted(self.cold), 95) if self.cold else None

    @property
    def p95_warm(self) -> float | None:
        """p95 of the warm samples, or ``None`` when nothing was measured."""
        return nearest_rank(sorted(self.warm), 95) if self.warm else None

    def to_json(self) -> str:
        """Serialise for the DoD-F5 evidence: the samples, not just the verdict.

        The raw numbers travel with the report so a later reader can recompute the percentile
        rather than trust this code's arithmetic.
        """
        return json.dumps(
            {
                "cold_seconds": list(self.cold),
                "warm_seconds": list(self.warm),
                "p95_cold_seconds": self.p95_cold,
                "p95_warm_seconds": self.p95_warm,
                "target_cold_seconds": P95_COLD_SECONDS,
                "target_warm_seconds": P95_WARM_SECONDS,
            },
            indent=2,
            sort_keys=True,
        )


def measure(probe: Probe, *, cold_samples: int, warm_samples: int) -> Latency:
    """Drive ``probe`` and collect samples.

    The caller is responsible for the temperature: it must force a scale-to-zero before each cold
    sample. This function cannot verify that, and pretending otherwise — by, say, calling the first
    sample of a batch "cold" — would produce a cold figure that is really a warm one and a gate
    that passes a deployment nobody has cold-started.
    """
    cold = tuple(probe() for _ in range(cold_samples))
    warm = tuple(probe() for _ in range(warm_samples))
    return Latency(cold=cold, warm=warm)


def gate(measured: Latency) -> tuple[str, ...]:
    """Reasons M5.06 fails. Empty means it passes.

    Thresholds are the module constants and are not arguments: a caller that could pass its own
    numbers could pass the ones its measurement happens to meet.
    """
    failures: list[str] = []

    if len(measured.cold) < MIN_COLD_SAMPLES:
        failures.append(
            f"cold: NOT RUN — {len(measured.cold)} samples, need {MIN_COLD_SAMPLES}. "
            "An unmeasured stage fails its gate."
        )
    elif (cold := measured.p95_cold) is not None and cold > P95_COLD_SECONDS:
        failures.append(f"cold: p95 {cold:.1f}s over the {P95_COLD_SECONDS:.0f}s target")

    if len(measured.warm) < MIN_WARM_SAMPLES:
        failures.append(
            f"warm: NOT RUN — {len(measured.warm)} samples, need {MIN_WARM_SAMPLES}. "
            "An unmeasured stage fails its gate."
        )
    elif (warm := measured.p95_warm) is not None and warm > P95_WARM_SECONDS:
        failures.append(f"warm: p95 {warm:.1f}s over the {P95_WARM_SECONDS:.0f}s target")

    return tuple(failures)


def report(measured: Latency) -> str:
    """Human-readable verdict for the DoD-F5 evidence."""
    lines = ["# M5.06 — latency", ""]
    for name, value, target in (
        ("cold", measured.p95_cold, P95_COLD_SECONDS),
        ("warm", measured.p95_warm, P95_WARM_SECONDS),
    ):
        shown = f"{value:.2f}s" if value is not None else "NOT RUN"
        lines.append(f"- **p95 {name}**: {shown} (target ≤ {target:.0f}s)")
    failures = gate(measured)
    lines += ["", "**FAIL**" if failures else "**PASS**"]
    lines += [f"- {reason}" for reason in failures]
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point. Reads a samples JSON, exits non-zero when the gate fails.

    Taking measurements from a file rather than probing here keeps the gate runnable in CI, where
    there is no deployment to probe: whoever ran the deploy writes the samples, CI judges them.
    """
    parser = argparse.ArgumentParser(
        description="Gate deployment latency against the M5.06 p95 targets (D-0043): "
        f"cold ≤ {P95_COLD_SECONDS:.0f}s, warm ≤ {P95_WARM_SECONDS:.0f}s."
    )
    parser.add_argument(
        "samples",
        type=Path,
        help='JSON: {"cold_seconds": [...], "warm_seconds": [...]}',
    )
    parser.add_argument("--out", type=Path, help="write the Markdown report here")
    args = parser.parse_args(argv)

    if not args.samples.is_file():
        print(f"error: no such file: {args.samples}", file=sys.stderr)
        return 1
    try:
        raw = json.loads(args.samples.read_text(encoding="utf-8"))
        measured = Latency(
            cold=tuple(float(v) for v in raw.get("cold_seconds", ())),
            warm=tuple(float(v) for v in raw.get("warm_seconds", ())),
        )
    except (ValueError, TypeError, AttributeError) as exc:
        print(f"error: unreadable samples: {exc}", file=sys.stderr)
        return 1

    rendered = report(measured)
    if args.out:
        args.out.write_text(rendered, encoding="utf-8")
    print(rendered)
    return 1 if gate(measured) else 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
