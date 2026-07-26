"""Running the training on Colab — PLAN M3, revised platform.

The plan budgets *"1x A100 80GB or H100 on RunPod/Vast"*. Training on Colab instead changes three
things that the rest of M3 assumed, and each one is a correctness problem rather than a preference:

1. **Half the VRAM.** Colab Pro+ offers an A100 **40 GB** or an L4 24 GB, not the 80 GB the plan
   budgets for. :func:`vram_estimate` and :func:`fits` make that arithmetic explicit *before* a
   session starts, because the alternative is discovering it as an OOM twenty minutes in.
2. **Sessions are cut off.** A Colab runtime has a wall-clock limit and disconnects besides, so a
   3-6 h run will not reliably finish in one sitting. Resuming therefore stops being a nice-to-have:
   :func:`resume_from` finds the newest checkpoint on disk and :func:`build_notebook` always passes
   it to ``trainer.train(resume_from_checkpoint=…)``.
3. **No API on ordinary Colab.** ``colab.research.google.com`` (free/Pro/Pro+) cannot be driven from
   a shell — it is a browser. Only **Colab Enterprise** (Vertex AI) has one, via
   ``gcloud colab executions create``. Either way the work runs from a notebook, so the notebook is
   **generated from the committed config** rather than written by hand.

That last point is the decision worth stating. A hand-written notebook redeclares the
hyperparameters, and the moment it does, ``configs/train/*.yaml`` stops being the source of truth
and *"every run is reproducible from a YAML + seed"* (D-0025) is no longer true — the YAML says one
thing and the cell that actually ran says another. So the generated notebook **reads the YAML** and
declares nothing itself; :func:`check_no_hyperparameters` enforces that, and it is the only test in
this module that would fail if someone "helpfully" inlined the values.
"""

from __future__ import annotations

import json
import re
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path

from maia.training.config import TrainingConfig

#: Colab's GPU offerings and their VRAM, in GiB. The plan's 80 GB is on none of them.
COLAB_GPUS: dict[str, int] = {
    "T4": 16,
    "L4": 24,
    "A100-40GB": 40,
    "A100-80GB": 80,
}

#: What the plan assumed.
PLANNED_VRAM_GIB = 80

#: Which Colab GPUs support bfloat16. It needs Ampere or newer, so the T4 (Turing) does not — and a
#: config asking for bf16 will not merely be slow there, it will fail or silently fall back. This is
#: the check VRAM arithmetic alone would miss: a 12B QLoRA run *fits* a T4 and still cannot use the
#: precision the config specifies.
BF16_CAPABLE = frozenset({"L4", "A100-40GB", "A100-80GB"})

#: Gemma 4 12B in NF4: roughly half a byte per parameter, plus quantisation constants.
BASE_WEIGHTS_GIB = 7.5

#: Activation cost per sequence-token per micro-batch item, in GiB, **with gradient checkpointing**.
#:
#: Derived rather than guessed: checkpointing keeps one hidden state per layer, so the stored
#: activations are roughly ``layers x hidden x bytes`` per token. For a 12B model (~48 layers,
#: hidden ~3840) in bf16 that is 48 x 3840 x 2 B ≈ 0.37 MiB per token, i.e. ~1.5 GiB for a single
#: 4k sequence. The first version of this constant was 100x smaller and reported that a 32k-context
#: batch of 16 would fit a T4, which is the kind of false "✓" this whole module exists to prevent.
ACTIVATION_GIB_PER_TOKEN_PER_ITEM = 3.7e-4

#: LoRA adapter weights plus their 8-bit optimiser state. Small, but not nothing at r=64+.
ADAPTER_GIB_PER_RANK = 0.045

#: Headroom for the CUDA context, fragmentation and the tokenizer. Colab has less slack than a
#: dedicated box because the runtime hosts a Jupyter kernel too.
OVERHEAD_GIB = 3.0

#: How much of the card may be planned for. Above this, fragmentation alone will OOM.
SAFE_FRACTION = 0.90


def vram_estimate(config: TrainingConfig) -> float:
    """Estimated peak VRAM for one training step, in GiB.

    An estimate, and labelled as one wherever it is printed: the activation term is calibrated to
    the order of magnitude rather than measured on Gemma 4. It exists to catch the configuration
    that obviously will not fit, not to promise that a marginal one will.
    """
    activations = (
        ACTIVATION_GIB_PER_TOKEN_PER_ITEM * config.max_seq_len * config.per_device_batch_size
    )
    return BASE_WEIGHTS_GIB + activations + ADAPTER_GIB_PER_RANK * config.r + OVERHEAD_GIB


def fits(config: TrainingConfig, gpu: str) -> bool:
    """Whether ``config`` is expected to fit ``gpu`` with headroom.

    Raises:
        KeyError: naming the GPUs it knows. A silent ``False`` for a typo'd name would read as "this
            configuration is too big" when the real problem is the question.
    """
    if gpu not in COLAB_GPUS:
        raise KeyError(f"unknown GPU {gpu!r}; known: {', '.join(sorted(COLAB_GPUS))}")
    return vram_estimate(config) <= COLAB_GPUS[gpu] * SAFE_FRACTION


def supports_dtype(config: TrainingConfig, gpu: str) -> bool:
    """Whether ``gpu`` can actually run the config's ``compute_dtype``.

    Fitting in VRAM is not the same as being able to run: bfloat16 needs Ampere or newer, so a T4
    has the memory for a 12B QLoRA run and cannot provide the precision the config asks for.
    """
    if gpu not in COLAB_GPUS:
        raise KeyError(f"unknown GPU {gpu!r}; known: {', '.join(sorted(COLAB_GPUS))}")
    return config.compute_dtype != "bfloat16" or gpu in BF16_CAPABLE


def usable(config: TrainingConfig, gpu: str) -> bool:
    """Whether ``gpu`` both fits the config and can run its precision."""
    return fits(config, gpu) and supports_dtype(config, gpu)


def largest_batch(config: TrainingConfig, gpu: str) -> int:
    """The biggest ``per_device_batch_size`` expected to fit ``gpu``, or ``0`` if none does.

    Useful because the honest response to a 40 GB card is usually to halve the micro-batch and
    double the accumulation, which keeps the effective batch the spec asks for.
    """
    budget = COLAB_GPUS[gpu] * SAFE_FRACTION - BASE_WEIGHTS_GIB - OVERHEAD_GIB
    budget -= ADAPTER_GIB_PER_RANK * config.r
    per_item = ACTIVATION_GIB_PER_TOKEN_PER_ITEM * config.max_seq_len
    return max(0, int(budget / per_item)) if per_item > 0 else 0


def resume_from(config: TrainingConfig, root: Path | None = None) -> Path | None:
    """The newest checkpoint to resume from, or ``None`` for a fresh run.

    On a dedicated box this is a convenience. On Colab it is the difference between a run that
    finishes and one that never does, because the runtime is cut off before a 3-6 h job completes.
    Checkpoints are ordered by their trailing number rather than by mtime, because a resumed run
    rewrites older files and mtime stops meaning "most trained".
    """
    directory = (root or config.output_dir) / config.name
    if not directory.is_dir():
        return None
    numbered: list[tuple[int, Path]] = []
    for path in directory.iterdir():
        found = re.fullmatch(r"checkpoint-(?:epoch-)?(\d+)", path.name)
        if path.is_dir() and found:
            numbered.append((int(found.group(1)), path))
    if not numbered:
        return None
    return max(numbered, key=lambda item: item[0])[1]


@dataclass(frozen=True)
class NotebookPlan:
    """What a generated notebook will do."""

    config_path: str
    dataset_path: str
    gpu: str
    repo: str = "https://github.com/ericrisco/maia"
    branch: str = "main"


def build_notebook(config: TrainingConfig, plan: NotebookPlan) -> dict[str, object]:
    """Generate the Colab notebook for one run, as an ``.ipynb`` document.

    The notebook **reads the committed YAML** and declares no hyperparameters of its own. That is
    the whole point: a hand-written notebook redeclares them, and from that moment the YAML and the
    cell that actually ran can disagree while both look right.
    """
    cells = [
        _markdown(
            f"# MAIA — QLoRA run `{config.name}`\n",
            "",
            "Generated by `maia.training.colab`. **Do not edit the hyperparameters here** —",
            f"they live in `{plan.config_path}` and this notebook reads them, so the committed",
            "YAML stays the single source of truth for what ran (D-0025).",
            "",
            f"Expected VRAM: **{vram_estimate(config):.1f} GiB estimated** on `{plan.gpu}` "
            f"({COLAB_GPUS[plan.gpu]} GiB).",
            "",
            "Colab cuts sessions off, so **re-running this notebook resumes** from the newest",
            "checkpoint rather than starting over.",
        ),
        _code(
            "# GPU actually allocated — Colab does not always give what was requested.",
            "!nvidia-smi --query-gpu=name,memory.total --format=csv",
        ),
        _code(
            "# Unsloth pulls its own pinned torch/trl/peft set; installing them separately is how",
            "# a Colab environment ends up with a mismatched stack.",
            '!pip install -q "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"',
            "!pip install -q --no-deps trl peft accelerate bitsandbytes",
        ),
        _code(
            f"!git clone --depth 1 --branch {plan.branch} {plan.repo} /content/maia",
            "!pip install -q -e /content/maia",
            "import os; os.chdir('/content/maia')",
        ),
        _code(
            "from maia.training.colab import resume_from, usable, vram_estimate",
            "from maia.training.config import load_config, render",
            "",
            f"config = load_config({plan.config_path!r})",
            "print(render(config))",
            f"assert usable(config, {plan.gpu!r}), (",
            f"    f'{{vram_estimate(config):.1f}} GiB estimated does not fit {plan.gpu} — halve '",
            "    'per_device_batch_size and double gradient_accumulation_steps to keep the same '",
            "    'effective batch'",
            ")",
        ),
        _code(
            "from maia.training.chat import format_dataset",
            "from maia.synth.publish import read_dataset",
            "",
            f"examples = read_dataset({plan.dataset_path!r})",
            "train = [e for e in examples if e.split.value == 'train']",
            "rows = format_dataset(train)",
            "print(f'{len(rows)} training row(s)')",
        ),
        _code(
            "import wandb",
            "from google.colab import userdata",
            "",
            "# Colab secrets, not literals: a token pasted into a cell is a token in the notebook.",
            "wandb.login(key=userdata.get('WANDB_API_KEY'))",
        ),
        _code(
            "from maia.training.unsloth_runner import unsloth_trainer",
            "",
            "trainer = unsloth_trainer()",
            "job = trainer.build(config, rows)",
            "checkpoint = resume_from(config)",
            "print(f'resuming from {checkpoint}' if checkpoint else 'starting fresh')",
            "job.train(resume_from_checkpoint=str(checkpoint) if checkpoint else None)",
        ),
        _code(
            "from maia.training.smoke import TrainingOutcome, check_loss",
            "from maia.training.unsloth_runner import epoch_checkpoints, losses_from_log",
            "",
            "losses = losses_from_log(job.state.log_history)",
            "outcome = TrainingOutcome(",
            "    losses=losses,",
            "    checkpoint=epoch_checkpoints(config)[-1],",
            "    hours=job.state.log_history[-1].get('train_runtime', 0) / 3600,",
            ")",
            "print(check_loss(outcome).detail)",
        ),
        _code(
            "# Checkpoints outlive the runtime only if they leave it.",
            "from huggingface_hub import HfApi",
            "from google.colab import userdata",
            "",
            "HfApi(token=userdata.get('HF_TOKEN')).upload_folder(",
            "    repo_id=f'ericrisco/maia-12b-{config.name}',",
            "    folder_path=str(config.output_dir / config.name),",
            "    repo_type='model',",
            "    commit_message=f'{config.name}: adapters',",
            ")",
        ),
    ]
    return {
        "cells": cells,
        "metadata": {
            "accelerator": "GPU",
            "colab": {"provenance": [], "gpuType": plan.gpu},
            "kernelspec": {"display_name": "Python 3", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 0,
    }


def _markdown(*lines: str) -> dict[str, object]:
    """One markdown cell."""
    return {"cell_type": "markdown", "metadata": {}, "source": _source(lines)}


def _code(*lines: str) -> dict[str, object]:
    """One code cell."""
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": _source(lines),
    }


def _source(lines: Sequence[str]) -> list[str]:
    """Notebook ``source`` is a list of lines, each keeping its newline except the last."""
    return [f"{line}\n" for line in lines[:-1]] + list(lines[-1:])


#: Hyperparameter names that must not appear as assignments in a generated notebook. If they do, the
#: YAML has stopped being the source of truth.
GUARDED_NAMES = (
    "learning_rate",
    "per_device_batch_size",
    "lora_alpha",
    "lora_dropout",
    "num_train_epochs",
    "max_seq_length",
    "max_seq_len",
    "per_device_train_batch_size",
    "gradient_accumulation_steps",
    "warmup_ratio",
    "target_modules",
    "seed",
    "r",
)


def check_no_hyperparameters(notebook: dict[str, object]) -> list[str]:
    """Assignments in the notebook that shadow a committed hyperparameter.

    The guard that keeps D-0025 true. A notebook is the easiest place in the project to "just set
    r = 32 to try something", and the result is a run whose YAML describes different settings from
    the ones that executed.
    """
    cells = notebook.get("cells")
    assert isinstance(cells, list)
    offences: list[str] = []
    for index, cell in enumerate(cells):
        if not isinstance(cell, dict) or cell.get("cell_type") != "code":
            continue
        source = cell.get("source")
        assert isinstance(source, list)
        for line in source:
            stripped = str(line).strip()
            for name in GUARDED_NAMES:
                if re.match(rf"^{re.escape(name)}\s*=[^=]", stripped):
                    offences.append(f"cell {index}: {stripped}")
    return offences


def write_notebook(config: TrainingConfig, plan: NotebookPlan, path: Path) -> Path:
    """Write the notebook, refusing to emit one that shadows the committed config.

    Raises:
        ValueError: listing the offending assignments.
    """
    notebook = build_notebook(config, plan)
    offences = check_no_hyperparameters(notebook)
    if offences:
        raise ValueError(
            "the generated notebook assigns hyperparameters, which would let it disagree with "
            f"{plan.config_path}:\n" + "\n".join(f"  {offence}" for offence in offences)
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def enterprise_command(
    notebook_uri: str,
    *,
    project: str,
    region: str = "europe-west4",
    runtime_template: str,
    output_uri: str,
    display_name: str,
) -> list[str]:
    """The ``gcloud`` invocation that runs a notebook on **Colab Enterprise**, unattended.

    Ordinary Colab (``colab.research.google.com``, free/Pro/Pro+) has no API and cannot be driven
    from a shell — it is a browser. Colab Enterprise is a Vertex AI service, billed per use rather
    than by the Colab subscription, and this is what makes an unattended run possible at all.

    Returned as a list rather than executed: the run costs money and starts a GPU, so it is the
    caller's to launch.
    """
    return [
        "gcloud",
        "colab",
        "executions",
        "create",
        f"--project={project}",
        f"--region={region}",
        f"--display-name={display_name}",
        f"--notebook-runtime-template={runtime_template}",
        f"--gcs-notebook-uri={notebook_uri}",
        f"--gcs-output-uri={output_uri}",
    ]


def render_fit(config: TrainingConfig, gpus: Iterable[str] = tuple(COLAB_GPUS)) -> str:
    """Human-readable VRAM verdict across Colab's cards."""
    estimate = vram_estimate(config)
    lines = [
        f"{config.name}: {estimate:.1f} GiB estimated peak "
        f"(batch {config.per_device_batch_size} x {config.max_seq_len} tokens, r={config.r})",
        f"  the plan assumed {PLANNED_VRAM_GIB} GiB; Colab offers less",
    ]
    for gpu in gpus:
        total = COLAB_GPUS[gpu]
        mark = "✓" if usable(config, gpu) else "✗"
        detail = f"{gpu}: {total} GiB"
        if not fits(config, gpu):
            biggest = largest_batch(config, gpu)
            detail += (
                f" — largest micro-batch that fits is {biggest}"
                if biggest
                else " — does not fit at any micro-batch; reduce max_seq_len or r"
            )
        elif not supports_dtype(config, gpu):
            detail += (
                f" — fits, but cannot run {config.compute_dtype}: bf16 needs Ampere or newer, so "
                "this card falls back to fp16 and the learning rate was not chosen for it"
            )
        lines.append(f"  {mark} {detail}")
    lines.append(
        "  estimated, not measured: the activation term is an order-of-magnitude calibration, so "
        "treat a marginal verdict as unknown"
    )
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point: generate the Colab notebook for a committed training config."""
    import argparse
    import shlex
    import sys

    from maia.training.config import load_config

    parser = argparse.ArgumentParser(
        description="Generate the Colab notebook for a training run. The notebook reads the "
        "committed YAML and declares no hyperparameters, so what runs is what is versioned."
    )
    parser.add_argument("config", type=Path, help="configs/train/*.yaml")
    parser.add_argument("--dataset", default="data/dataset.jsonl", help="path inside the notebook")
    parser.add_argument("--gpu", default="A100-40GB", choices=sorted(COLAB_GPUS))
    parser.add_argument("--branch", default="main")
    parser.add_argument("--out", type=Path, help="write the .ipynb here")
    args = parser.parse_args(argv)

    if not args.config.is_file():
        print(f"error: no such file: {args.config}", file=sys.stderr)
        return 1
    try:
        config = load_config(args.config)
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    print(render_fit(config))
    if not usable(config, args.gpu):
        print(
            f"error: {config.name} cannot run on {args.gpu} — see above",
            file=sys.stderr,
        )
        return 1

    plan = NotebookPlan(
        config_path=str(args.config),
        dataset_path=args.dataset,
        gpu=args.gpu,
        branch=args.branch,
    )
    out = args.out or Path("notebooks") / f"{config.name}.ipynb"
    try:
        written = write_notebook(config, plan, out)
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"wrote {written}")
    print("  ordinary Colab: upload it — colab.research.google.com has no API")
    print("  Colab Enterprise (Vertex AI), unattended:")
    print(
        "    "
        + shlex.join(
            enterprise_command(
                f"gs://YOUR_BUCKET/{written.name}",
                project="YOUR_PROJECT",
                runtime_template="YOUR_RUNTIME_TEMPLATE",
                output_uri="gs://YOUR_BUCKET/executions",
                display_name=config.name,
            )
        )
    )
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
