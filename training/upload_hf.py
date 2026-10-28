"""Uploads a run's LoRA adapter to Hugging Face as a new version, with a generated model card.

Usage:
    HF_TOKEN=... python training/upload_hf.py runs/<run> [--repo user/name] [--public]

Reads the downloaded run (input/config.json, output/adapter, output/metrics.json,
output/samples.md). There is one repo per model size, `<user>/gemma-maia-<size>` (private by
default): each run is a new commit on `main`, tagged with the run name, so `main` is always the
latest version and any earlier one loads with `revision="<run>"`. Checkpoints are not uploaded.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from huggingface_hub import HfApi


def eval_curve(log_history: list[dict]) -> list[tuple[int, float, float]]:
    """(step, epoch, validation loss) of each evaluation, without repeated steps."""
    seen: dict[int, tuple[int, float, float]] = {}
    for entry in log_history:
        if "eval_loss" in entry:
            seen[entry["step"]] = (entry["step"], entry["epoch"], entry["eval_loss"])
    return sorted(seen.values())


def model_card(
    run: str, cfg: dict, metrics: dict, samples: str, system: str, versions: list[str]
) -> str:
    curve = eval_curve(metrics.get("log_history", []))
    rows = "\n".join(f"| {step} | {epoch:.2f} | {loss:.4f} |" for step, epoch, loss in curve)
    final = metrics.get("final_eval", {}).get("eval_loss")
    final_text = f"{final:.4f}" if final is not None else "—"
    effective_batch = cfg["batch_size"] * cfg["grad_accum"]
    samples_body = samples.split("\n", 1)[1].strip() if samples.startswith("#") else samples.strip()
    version_rows = "\n".join(f"- `{tag}`" for tag in sorted(versions, reverse=True))
    return f"""---
base_model: {cfg["model"]}
library_name: peft
pipeline_tag: text-generation
license: apache-2.0
language:
- ca
tags:
- maia
- andorra
- lora
- qlora
- unsloth
- sft
---

# gemma-maia-{run.split("-")[2]}

LoRA adapter of **maia**, a model specialised in Andorra built from Gemma 4.
Experimental: **not a final model yet**.

This card describes the latest version, **`{run}`**.
Every training run is a tagged version of this repo:

{version_rows}

Load a specific version with `revision="<tag>"`.

- Base model: `{cfg["model"]}`
- Data: variant **{cfg["variant"]}** of the `training-data` export
  (conversations in Andorran Catalan)
- Code: [github.com/ericrisco/maia](https://github.com/ericrisco/maia) (`training/train.py`)

## Training

QLoRA with Unsloth on 1 NVIDIA L4. The loss is computed on the model's responses only.

| Parameter | Value |
|---|---|
| LoRA r / alpha | {cfg["lora_r"]} / {cfg["lora_alpha"]} |
| Epochs | {cfg["epochs"]} |
| Learning rate | {cfg["learning_rate"]} (cosine, 3 % warmup) |
| Effective batch | {effective_batch} ({cfg["batch_size"]} x {cfg["grad_accum"]}) |
| Max length | {cfg["max_seq_length"]} tokens |
| Chat template | `{cfg["chat_template"]}` |
| Seed | {cfg["seed"]} |

Final validation loss: **{final_text}**

| Step | Epoch | Validation loss |
|---:|---:|---:|
{rows}

## System message

The model was always trained with this system message (in Catalan). Use it at inference time too:

> {system}

## Samples

Generated at the end of training (temperature 1.0, top_p 0.95, top_k 64).

{samples_body}

## Usage

```python
from unsloth import FastModel

model, tokenizer = FastModel.from_pretrained("<this repo>", revision="{run}", load_in_4bit=True)
```
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--repo", help="user/name (default <user>/gemma-maia-<size>)")
    parser.add_argument("--public", action="store_true", help="create the repo as public")
    args = parser.parse_args()

    run_dir: Path = args.run_dir
    adapter = run_dir / "output" / "adapter"
    if not (adapter / "adapter_model.safetensors").is_file():
        sys.exit(f"ERROR: no adapter in {adapter}")
    cfg = json.loads((run_dir / "input" / "config.json").read_text(encoding="utf-8"))
    metrics_path = run_dir / "output" / "metrics.json"
    metrics = json.loads(metrics_path.read_text(encoding="utf-8")) if metrics_path.is_file() else {}
    samples_path = run_dir / "output" / "samples.md"
    samples = samples_path.read_text(encoding="utf-8") if samples_path.is_file() else ""
    with (run_dir / "input" / "data" / "valid.jsonl").open(encoding="utf-8") as stream:
        system = json.loads(stream.readline())["messages"][0]["content"]

    api = HfApi()
    run = cfg["run"]
    size = run.split("-")[2]  # <date>-<time>-<size>-<variant>[-test]
    repo = args.repo or f"{api.whoami()['name']}/gemma-maia-{size}"
    api.create_repo(repo, repo_type="model", private=not args.public, exist_ok=True)
    tags = [ref.name for ref in api.list_repo_refs(repo).tags]
    if run in tags:
        sys.exit(f"ERROR: {repo} already has version {run}")

    # The model card replaces the generic README that PEFT writes.
    api.upload_folder(
        repo_id=repo,
        folder_path=adapter,
        ignore_patterns=["README.md"],
        commit_message=f"LoRA adapter of run {run}",
    )
    for path in (metrics_path, samples_path, run_dir / "input" / "config.json"):
        if path.is_file():
            api.upload_file(path_or_fileobj=path, path_in_repo=path.name, repo_id=repo)
    api.upload_file(
        path_or_fileobj=model_card(run, cfg, metrics, samples, system, [*tags, run]).encode(),
        path_in_repo="README.md",
        repo_id=repo,
        commit_message=f"Model card for {run}",
    )
    api.create_tag(repo, tag=run, tag_message=f"Training run {run}")
    print(f"https://huggingface.co/{repo} (version {run})")


if __name__ == "__main__":
    main()
