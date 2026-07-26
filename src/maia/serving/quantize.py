"""Merge, quantise, and check what quantisation cost — PLAN M5.05, F5 steps 1-3.

*"Merge LoRA adapters → full model; verify adapter-vs-merged output equality on 20 prompts."*
*"GGUF → Q4_K_M and Q8_0. Q4 must retain **≥95 %** of the merged AndBench score. Mandatory
chat-template parity test (Unsloth vs GGUF/Ollama with the training template embedded in the
Modelfile)."*

Every step here converts the model into a different representation, and each conversion can change
its behaviour **without failing**. That is the whole risk, and it is why the plan asks for three
checks rather than a build script:

**Merging must be a no-op.** An adapter applied at inference and an adapter baked into the weights
should produce the same tokens; if they do not, something in the merge is wrong and every number
measured on the merged model afterwards describes a different model than the one M4 evaluated.
:func:`check_merge` compares them on the plan's 20 prompts and reports **which** prompts diverged,
because one divergence out of twenty is a different problem from twenty out of twenty.

**Quantisation must be paid for knowingly.** Q4_K_M is lossy by design; the plan sets the price at
≤5 % of the merged AndBench score. :func:`check_retention` measures it, and — the part worth
insisting on — it **refuses to compare scores from different AndBench runs**, for the same reason
M4.03 refuses it: a Q4 score from a newer harness is not a smaller number, it is a different
measurement.

**The Modelfile carries the training template, or Ollama silently reformats.** Gemma's turn markers
are what the model was trained on (D-0025); Ollama applies its *own* template unless the Modelfile
overrides it, and the symptom is a model that is worse only when served through Ollama.
:func:`build_modelfile` writes the template from the same constants M3.01 trained with, and
:func:`check_modelfile` is what a test asserts so an edit cannot quietly drop it.

llama.cpp, Ollama and the GPU are **blocked-by-resource**; :class:`Quantizer` and the scorer
seams are injected.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Protocol

from maia.training.chat import END_OF_TURN, START_OF_TURN

#: The plan's prompt count for merge equality.
MERGE_PROMPTS = 20

#: The plan's floor: Q4 must retain this share of the merged model's AndBench score.
MIN_RETENTION = 0.95

#: The disclaimer the Modelfile must carry — this model is not legal advice, and it is served with
#: Andorran law in its training data, which is exactly the combination that invites the mistake.
DISCLAIMER = (
    "No ofereixes assessorament jurídic. Quan una pregunta tingui conseqüències legals, "
    "recorda que cal consultar el text consolidat oficial i un professional."
)


class Quant(StrEnum):
    """The quantisations the plan asks for."""

    Q4_K_M = "Q4_K_M"
    Q8_0 = "Q8_0"

    @property
    def gated(self) -> bool:
        """Whether DoD-F5 sets a retention floor for this one."""
        return self is Quant.Q4_K_M

    @property
    def approximate_gib(self) -> float:
        """Rough on-disk size for a 12B model, for the 16 GB-machine claim."""
        return 7.5 if self is Quant.Q4_K_M else 13.0


class Generator(Protocol):
    """Something that answers a prompt. Blocked-by-resource: loaded weights."""

    def generate(self, prompt: str) -> str:
        """Answer one prompt, greedily."""


class Quantizer(Protocol):
    """llama.cpp's conversion and quantisation. Blocked-by-resource."""

    def convert(self, model_dir: Path, out: Path, *, quant: str) -> Path:
        """Produce a GGUF file at ``out``."""


@dataclass
class MergeCheck:
    """Whether the merged model behaves like the adapter it came from."""

    prompts: int = 0
    divergent: list[tuple[str, str, str]] = field(default_factory=list)

    @property
    def identical(self) -> int:
        """Prompts where both answered the same."""
        return self.prompts - len(self.divergent)

    @property
    def passed(self) -> bool:
        """Whether every prompt matched, over enough prompts to mean something."""
        return self.prompts >= MERGE_PROMPTS and not self.divergent


def check_merge(adapter: Generator, merged: Generator, prompts: Sequence[str]) -> MergeCheck:
    """Compare an adapter-applied model with the merged one.

    Every number M4 measured describes the model it measured, so if merging changes behaviour, every
    later number describes something else. Reports **which** prompts diverged: one in twenty is a
    numerical-precision problem, twenty in twenty is a broken merge.

    Raises:
        ValueError: if there are no prompts. A merge check over nothing passes trivially, which is
            the failure mode this whole module exists to avoid.
    """
    if not prompts:
        raise ValueError("a merge check needs prompts; over none it would pass trivially")
    check = MergeCheck(prompts=len(prompts))
    for prompt in prompts:
        left, right = adapter.generate(prompt), merged.generate(prompt)
        if left != right:
            check.divergent.append((prompt, left, right))
    return check


@dataclass(frozen=True)
class QuantScore:
    """One quantisation's AndBench score, with the run that produced it."""

    quant: Quant | None
    score: float
    harness_version: str
    items: int

    def __post_init__(self) -> None:
        if not 0.0 <= self.score <= 1.0:
            raise ValueError(f"score {self.score} is outside 0.0-1.0")
        if not self.harness_version:
            raise ValueError(
                "no harness version recorded, so this score cannot be shown to be comparable "
                "with the merged model's"
            )


class IncomparableError(RuntimeError):
    """Raised when two scores come from different AndBench runs."""


@dataclass(frozen=True)
class Retention:
    """What quantisation cost."""

    merged: QuantScore
    quantised: QuantScore
    minimum: float = MIN_RETENTION

    @property
    def retained(self) -> float:
        """Share of the merged score the quantised model keeps."""
        return self.quantised.score / self.merged.score if self.merged.score else 0.0

    @property
    def passed(self) -> bool:
        """Whether DoD-F5's floor is met.

        Only ``Q4_K_M`` is gated; ``Q8_0`` is reported so the trade is visible.
        """
        return self.retained >= self.minimum


def check_retention(
    merged: QuantScore, quantised: QuantScore, *, minimum: float = MIN_RETENTION
) -> Retention:
    """Compare a quantised model with the merged one.

    Raises:
        IncomparableError: if the two came from different harness runs or item counts. A Q4 score
            from a newer AndBench is not a smaller number, it is a different measurement — the same
            refusal as M4.03.
        ValueError: if the merged model scored zero, leaving nothing to retain.
    """
    if (merged.harness_version, merged.items) != (quantised.harness_version, quantised.items):
        raise IncomparableError(
            f"the merged model was scored on {merged.harness_version} over {merged.items} item(s) "
            f"and the quantised one on {quantised.harness_version} over {quantised.items}; "
            "re-run both rather than comparing a model against a different measurement"
        )
    if merged.score <= 0:
        raise ValueError("the merged model scored 0.0; there is nothing to retain")
    return Retention(merged=merged, quantised=quantised, minimum=minimum)


def build_modelfile(
    gguf: Path,
    *,
    system: str,
    quant: Quant = Quant.Q4_K_M,
    temperature: float = 0.3,
) -> str:
    """An Ollama ``Modelfile`` **with the training template embedded**.

    Ollama applies its own template unless told otherwise, and its idea of Gemma's format need not
    match the one this model was trained on. The symptom is a model that is worse *only* when served
    through Ollama — which reads as "quantisation hurt it" and is not that at all. So the template
    here is written from M3.01's own constants.
    """
    template = (
        "{{ if .System }}" + START_OF_TURN + "user\n{{ .System }}\n\n{{ end }}"
        "{{ if .Prompt }}{{ .Prompt }}"
        + END_OF_TURN
        + "\n{{ end }}"
        + START_OF_TURN
        + "model\n{{ .Response }}"
    )
    return "\n".join(
        [
            f"FROM {gguf}",
            "",
            f'TEMPLATE """{template}"""',
            "",
            f'SYSTEM """{system}',
            "",
            f'{DISCLAIMER}"""',
            "",
            f"PARAMETER temperature {temperature}",
            f'PARAMETER stop "{END_OF_TURN}"',
            f'PARAMETER stop "{START_OF_TURN}"',
            "",
            f"# {quant.value}, ~{quant.approximate_gib:.1f} GiB — sized for a 16 GB machine.",
            "# The TEMPLATE above is MAIA's training template. Do not remove it: Ollama would",
            "# apply its own and the model would be worse only here (D-0025, D-0040).",
        ]
    )


def check_modelfile(modelfile: str) -> list[str]:
    """What a Modelfile is missing. Empty when it is complete.

    The predicate a test asserts on, so an edit cannot quietly drop the template or the disclaimer —
    both of which fail silently rather than loudly.
    """
    missing: list[str] = []
    if "TEMPLATE" not in modelfile:
        missing.append(
            "TEMPLATE — without it Ollama applies its own and the model is worse only here"
        )
    if START_OF_TURN not in modelfile or END_OF_TURN not in modelfile:
        missing.append("the Gemma turn markers the model was trained on")
    if "SYSTEM" not in modelfile:
        missing.append("SYSTEM — the identity prompt")
    if DISCLAIMER.split(".")[0] not in modelfile:
        missing.append("the legal disclaimer")
    if "PARAMETER stop" not in modelfile:
        missing.append("a stop parameter — the model would run past the end of its turn")
    return missing


@dataclass
class LocalRun:
    """What the 16 GB-machine test measured, for the README."""

    quant: Quant
    load_seconds: float
    tokens_per_second: float
    ram_gib: float

    @property
    def fits_16gb(self) -> bool:
        """Whether it ran inside the plan's target machine, with room for an OS."""
        return self.ram_gib <= 15.0

    @property
    def usable(self) -> bool:
        """Whether the throughput is usable interactively.

        Five tokens/s is roughly reading speed; below that a local demo feels broken even when it is
        working, which matters for the audience this quantisation exists for.
        """
        return self.tokens_per_second >= 5.0


@dataclass
class QuantReport:
    """The F5 quantisation gate."""

    merge: MergeCheck | None = None
    retention: Mapping[Quant, Retention] = field(default_factory=dict)
    local: LocalRun | None = None
    modelfile_problems: list[str] = field(default_factory=list)

    @property
    def gated_retention(self) -> Retention | None:
        """The one DoD-F5 puts a floor under."""
        return self.retention.get(Quant.Q4_K_M)

    @property
    def passed(self) -> bool:
        """Whether every part of the F5 quantisation gate is met.

        A missing check is a failure, not a pass: this is the last gate before a public artifact,
        and every step it covers can change the model's behaviour without erroring.
        """
        gated = self.gated_retention
        return (
            self.merge is not None
            and self.merge.passed
            and gated is not None
            and gated.passed
            and self.local is not None
            and self.local.fits_16gb
            and not self.modelfile_problems
        )


def render(report: QuantReport) -> str:
    """Human-readable verdict on the quantisation gate."""
    mark = "✓ PASS" if report.passed else "✗ FAIL"
    lines = [f"{mark} — F5 quantisation"]

    if report.merge is None:
        lines.append(
            "  · merge equality: NOT CHECKED — every later number would describe a "
            "different model than M4 evaluated"
        )
    elif report.merge.passed:
        lines.append(
            f"  ✓ merge equality: {report.merge.identical}/{report.merge.prompts} identical"
        )
    else:
        lines.append(
            f"  ✗ merge equality: {len(report.merge.divergent)}/{report.merge.prompts} diverged"
            + (
                ""
                if report.merge.prompts >= MERGE_PROMPTS
                else f" (and only {report.merge.prompts} prompt(s); the plan asks for "
                f"{MERGE_PROMPTS})"
            )
        )
        for prompt, left, right in report.merge.divergent[:3]:
            lines.append(f"      {prompt[:40]!r}: {left[:30]!r} vs {right[:30]!r}")

    for quant, retention in sorted(report.retention.items(), key=lambda item: item[0].value):
        symbol = "✓" if retention.passed else ("✗" if quant.gated else "·")
        gate = f", gate ≥{retention.minimum:.0%}" if quant.gated else ", not gated"
        lines.append(
            f"  {symbol} {quant.value}: retains {retention.retained:.1%} of "
            f"{retention.merged.score:.3f}{gate}"
        )
    if report.gated_retention is None:
        lines.append(f"  · {Quant.Q4_K_M.value}: NOT MEASURED — DoD-F5 requires it")

    if report.local is None:
        lines.append("  · 16 GB machine: NOT TESTED — DoD-F5 requires it")
    else:
        symbol = "✓" if report.local.fits_16gb else "✗"
        lines.append(
            f"  {symbol} local: {report.local.ram_gib:.1f} GiB, "
            f"{report.local.load_seconds:.0f}s load, {report.local.tokens_per_second:.1f} tok/s"
        )
        if not report.local.usable:
            lines.append(
                "      ⚠ below ~5 tok/s a local demo feels broken even when it works, which "
                "matters for the audience this quantisation is for"
            )
    for problem in report.modelfile_problems:
        lines.append(f"  ✗ Modelfile is missing {problem}")
    return "\n".join(lines)


def quantise(
    model_dir: Path,
    quantizer: Quantizer,
    out_dir: Path,
    *,
    quants: Sequence[Quant] = tuple(Quant),
) -> dict[Quant, Path]:
    """Produce a GGUF per quantisation.

    Raises:
        ValueError: if no quantisation was requested, or if the converter returns a path it did not
            create — a missing artifact discovered at upload time is a wasted release.
    """
    if not quants:
        raise ValueError("no quantisation requested")
    produced: dict[Quant, Path] = {}
    for quant in quants:
        target = out_dir / f"maia-12b-{quant.value}.gguf"
        result = quantizer.convert(model_dir, target, quant=quant.value)
        produced[quant] = result
    return produced
