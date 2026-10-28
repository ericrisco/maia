"""Trains maia with QLoRA (Unsloth) on a training-data export.

Runs on the L4 VM, launched from training/train.ipynb. Reads:
  --config  config.json (model, variant and hyperparameters)
  --data    folder with train.jsonl and valid.jsonl (export/<variant>/)
  --out     output folder: checkpoints/, adapter/, metrics.json, samples.md

If --out/checkpoints holds a checkpoint (interrupted spot VM), training resumes from it.
"""

from __future__ import annotations

# ruff: noqa: I001
import json
import os
import sys

# Unsloth environment variables from the config (e.g. UNSLOTH_BLOCK_COMPILE=0): they must be set
# before importing it, because it reads them on load.
if "--config" in sys.argv:
    with open(sys.argv[sys.argv.index("--config") + 1], encoding="utf-8") as _stream:
        os.environ.update(json.load(_stream).get("env", {}))

# Unsloth must be imported before transformers and trl so it can patch them
# (that is why the imports are not in alphabetical order).
from unsloth import FastModel
from unsloth.chat_templates import get_chat_template, train_on_responses_only

import argparse
import time
from pathlib import Path

from datasets import load_dataset
from transformers.trainer_utils import get_last_checkpoint
from trl import SFTConfig, SFTTrainer

# Turn markers of the Gemma 4 chat template (checked against chat_template.jinja).
INSTRUCTION_PART = "<|turn>user\n"
RESPONSE_PART = "<|turn>model\n"


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def check_mask(trainer: SFTTrainer, tokenizer) -> None:
    """Stops training if the loss is not computed on the responses only."""
    sample = trainer.train_dataset[0]
    labels = sample["labels"]
    trained = [t for t in labels if t != -100]
    if not trained:
        sys.exit("ERROR: the mask leaves the first conversation without any response token")
    decoded = tokenizer.decode(trained)
    if "<|turn>user" in decoded or "<|turn>system" in decoded:
        sys.exit("ERROR: the mask also trains on the user or system turn")
    log(f"Mask OK: {len(trained)}/{len(labels)} tokens trained in the first conversation")
    log(f"Trained tokens (start): {decoded[:300]!r}")


def write_samples(model, tokenizer, cfg: dict, system: str, path: Path) -> None:
    FastModel.for_inference(model)
    lines = ["# Samples after training\n"]
    for question in cfg.get("prompts", []):
        messages = [{"role": "system", "content": system}, {"role": "user", "content": question}]
        text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        text = text.removeprefix("<bos>")
        inputs = tokenizer(text=[text], return_tensors="pt").to("cuda")
        output = model.generate(
            **inputs, max_new_tokens=300, do_sample=True, temperature=1.0, top_p=0.95, top_k=64
        )
        prompt_len = inputs["input_ids"].shape[1]
        answer = tokenizer.decode(output[0][prompt_len:], skip_special_tokens=True)
        lines.append(f"## {question}\n\n{answer.strip()}\n")
        log(f"Sample: {question}")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--data", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    cfg = json.loads(args.config.read_text(encoding="utf-8"))
    out: Path = args.out
    out.mkdir(parents=True, exist_ok=True)
    log(f"Run {cfg['run']}: model {cfg['model']}, variant {cfg['variant']}")
    log(f"Environment: {cfg.get('env', {})}")

    model, tokenizer = FastModel.from_pretrained(
        model_name=cfg["model"],
        max_seq_length=cfg["max_seq_length"],
        load_in_4bit=True,
        full_finetuning=False,
    )
    model = FastModel.get_peft_model(
        model,
        finetune_vision_layers=False,
        finetune_language_layers=True,
        finetune_attention_modules=True,
        finetune_mlp_modules=True,
        r=cfg["lora_r"],
        lora_alpha=cfg["lora_alpha"],
        lora_dropout=0,
        bias="none",
        random_state=cfg["seed"],
    )
    tokenizer = get_chat_template(tokenizer, chat_template=cfg["chat_template"])

    def to_text(batch: dict) -> dict:
        # The template adds <bos>; the tokenizer adds it again when training.
        return {
            "text": [
                tokenizer.apply_chat_template(
                    m, tokenize=False, add_generation_prompt=False
                ).removeprefix("<bos>")
                for m in batch["messages"]
            ]
        }

    data = load_dataset(
        "json",
        data_files={
            "train": str(args.data / "train.jsonl"),
            "valid": str(args.data / "valid.jsonl"),
        },
    )
    data = data.map(to_text, batched=True, remove_columns=["messages"])
    with (args.data / "valid.jsonl").open(encoding="utf-8") as stream:
        system = json.loads(stream.readline())["messages"][0]["content"]
    log(f"Conversations: train {len(data['train'])}, valid {len(data['valid'])}")

    ckpt_dir = out / "checkpoints"
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=data["train"],
        eval_dataset=data["valid"],
        args=SFTConfig(
            output_dir=str(ckpt_dir),
            dataset_text_field="text",
            per_device_train_batch_size=cfg["batch_size"],
            per_device_eval_batch_size=cfg["batch_size"],
            gradient_accumulation_steps=cfg["grad_accum"],
            num_train_epochs=cfg["epochs"],
            max_steps=cfg.get("max_steps", -1),
            learning_rate=cfg["learning_rate"],
            lr_scheduler_type="cosine",
            warmup_ratio=0.03,
            weight_decay=0.001,
            optim="adamw_8bit",
            logging_steps=10,
            eval_strategy="steps",
            eval_steps=cfg["eval_steps"],
            save_strategy="steps",
            save_steps=cfg["eval_steps"],
            save_total_limit=2,
            seed=cfg["seed"],
            report_to="none",
        ),
    )
    trainer = train_on_responses_only(
        trainer, instruction_part=INSTRUCTION_PART, response_part=RESPONSE_PART
    )
    check_mask(trainer, tokenizer)

    last = get_last_checkpoint(str(ckpt_dir)) if ckpt_dir.is_dir() else None
    log(f"Resuming from {last}" if last else "Training from scratch")
    trainer.train(resume_from_checkpoint=last)

    model.save_pretrained(str(out / "adapter"))
    tokenizer.save_pretrained(str(out / "adapter"))
    log("LoRA adapter saved")

    metrics = {
        "final_eval": trainer.evaluate(),
        "log_history": trainer.state.log_history,
        "config": cfg,
    }
    (out / "metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    log(f"Final validation loss: {metrics['final_eval'].get('eval_loss')}")

    # Samples and GGUF are extras: if they fail, the adapter is already saved.
    try:
        write_samples(model, tokenizer, cfg, system, out / "samples.md")
    except Exception as exc:
        log(f"WARNING: could not generate samples: {exc}")
    if cfg.get("export_gguf"):
        try:
            model.save_pretrained_gguf(str(out / "gguf"), tokenizer, quantization_method="q4_k_m")
            log("GGUF q4_k_m saved")
        except Exception as exc:
            log(f"WARNING: could not export the GGUF: {exc}")


if __name__ == "__main__":
    main()
