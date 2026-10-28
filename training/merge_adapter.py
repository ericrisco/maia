"""Merges a run's LoRA adapter into the 16-bit base model.

Runs on the L4 VM (training/vm-merge.sh). Unsloth downloads the 16-bit weights of the base model
and merges the adapter into them, so the result does not inherit the 4-bit quantization used for
training. The merged safetensors can then be quantized by Ollama (`ollama create -q q4_K_M`) with
the same method as the official base model, which keeps the benchmark comparison fair.

Usage:
    python merge_adapter.py --adapter <dir> --out <dir>
"""

from __future__ import annotations

# ruff: noqa: I001
# Unsloth must be imported before transformers so it can patch it.
from unsloth import FastModel

import argparse
import time
from pathlib import Path


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--adapter", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    log(f"Loading adapter {args.adapter}")
    model, tokenizer = FastModel.from_pretrained(str(args.adapter), load_in_4bit=True)
    log("Merging into the 16-bit base")
    model.save_pretrained_merged(str(args.out), tokenizer, save_method="merged_16bit")
    files = sorted(p.name for p in args.out.iterdir())
    size = sum(p.stat().st_size for p in args.out.iterdir()) / 2**30
    log(f"Merged model saved: {len(files)} files, {size:.1f} GiB: {files}")


if __name__ == "__main__":
    main()
