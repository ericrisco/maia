"""Uploads the training data of a run to Hugging Face as a dataset, with a generated card.

Usage:
    HF_TOKEN=... python training/upload_dataset_hf.py runs/<run> [--repo user/name] [--public]

Uploads the exact files the run trained on (input/data/train.jsonl and valid.jsonl), plus the
held-out fact probe, as a new tagged version of one dataset repo (`<user>/maia-training-data`),
the same way upload_hf.py versions the model: `main` is the latest, older runs load by tag.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from huggingface_hub import HfApi

ROOT = Path(__file__).resolve().parents[1]
PROBE = ROOT / "training-data" / "facts" / "canon-facts-probe.jsonl"


def count(path: Path) -> int:
    with path.open(encoding="utf-8") as stream:
        return sum(1 for _ in stream)


def dataset_card(run: str, cfg: dict, n_train: int, n_valid: int, n_probe: int, system: str) -> str:
    return f"""---
language:
- ca
license: other
task_categories:
- text-generation
tags:
- andorra
- catalan
- sft
- maia
pretty_name: maia training data
size_categories:
- 10K<n<100K
configs:
- config_name: default
  data_files:
  - split: train
    path: train.jsonl
  - split: validation
    path: valid.jsonl
---

# maia training data

Conversations in Andorran Catalan used to fine-tune **maia**, a Gemma 4 model specialised in
Andorra. This version is the exact data of training run **`{run}`** (variant `{cfg["variant"]}`).

| Split | Conversations |
|---|---:|
| train | {n_train} |
| validation | {n_valid} |

Each row is `{{"messages": [...]}}` in chat format. Every conversation starts with the same
system message, which the model also expects at inference time:

> {system}

## What is in it

- Knowledge conversations written from curated articles about Andorra (history, institutions,
  territory, society, culture, economy, sports, language).
- An **augmented canon of facts**: verified atomic facts, each asked about in about 11 different
  ways (direct, reverse, paraphrase, context, two-turn, false premise, abstention), plus
  contrast examples between facts that are easy to confuse.
- `probe.jsonl`: {n_probe} held-out questions (never in train) with the keywords a correct answer
  must contain. They measure fact recall before and after training.

Questions of the maia-bench benchmark and the articles it reserves are excluded.

## Sources and licence

Every source has a provenance record (owner, licence, terms, redistribution status) in the maia
repository (`docs/fonts/`). Redistribution is decided by the project owner per source; see the
records before reusing a portion of the data. Code: [github.com/ericrisco/maia](https://github.com/ericrisco/maia).
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--repo", help="user/name (default <user>/maia-training-data)")
    parser.add_argument("--public", action="store_true", help="create the repo as public")
    args = parser.parse_args()

    data = args.run_dir / "input" / "data"
    train, valid = data / "train.jsonl", data / "valid.jsonl"
    if not train.is_file() or not valid.is_file():
        sys.exit(f"ERROR: no train/valid data in {data}")
    cfg = json.loads((args.run_dir / "input" / "config.json").read_text(encoding="utf-8"))
    with valid.open(encoding="utf-8") as stream:
        system = json.loads(stream.readline())["messages"][0]["content"]

    api = HfApi()
    run = cfg["run"]
    repo = args.repo or f"{api.whoami()['name']}/maia-training-data"
    api.create_repo(repo, repo_type="dataset", private=not args.public, exist_ok=True)
    tags = [ref.name for ref in api.list_repo_refs(repo, repo_type="dataset").tags]
    if run in tags:
        sys.exit(f"ERROR: {repo} already has version {run}")
    for path, name in ((train, "train.jsonl"), (valid, "valid.jsonl"), (PROBE, "probe.jsonl")):
        api.upload_file(path_or_fileobj=path, path_in_repo=name, repo_id=repo, repo_type="dataset")
    card = dataset_card(run, cfg, count(train), count(valid), count(PROBE), system)
    api.upload_file(
        path_or_fileobj=card.encode(),
        path_in_repo="README.md",
        repo_id=repo,
        repo_type="dataset",
        commit_message=f"Dataset card for {run}",
    )
    api.create_tag(repo, tag=run, tag_message=f"Training data of run {run}", repo_type="dataset")
    print(f"https://huggingface.co/datasets/{repo} (version {run})")


if __name__ == "__main__":
    main()
