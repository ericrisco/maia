"""Entrena maia amb QLoRA (Unsloth) sobre un export de training-data.

S'executa a la VM amb la L4, llançada des de training/entrena.ipynb. Llegeix:
  --config  config.json (model, variant i hiperparàmetres)
  --data    carpeta amb train.jsonl i valid.jsonl (export/<variant>/)
  --out     carpeta de sortida: checkpoints/, adapter/, metrics.json, mostres.md

Si a --out/checkpoints hi ha un checkpoint (VM spot interrompuda), es reprèn d'allà.
"""

from __future__ import annotations

# Unsloth s'ha d'importar abans que transformers i trl perquè hi apliqui els pegats
# (per això l'ordre d'imports no és l'alfabètic).
# ruff: noqa: I001
from unsloth import FastModel
from unsloth.chat_templates import get_chat_template, train_on_responses_only

import argparse
import json
import sys
import time
from pathlib import Path

from datasets import load_dataset
from transformers.trainer_utils import get_last_checkpoint
from trl import SFTConfig, SFTTrainer

# Marques de torn de la plantilla de Gemma 4 (comprovades sobre chat_template.jinja).
INSTRUCTION_PART = "<|turn>user\n"
RESPONSE_PART = "<|turn>model\n"


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def check_mask(trainer: SFTTrainer, tokenizer) -> None:
    """Atura l'entrenament si la pèrdua no es calcula només sobre les respostes."""
    sample = trainer.train_dataset[0]
    labels = sample["labels"]
    trained = [t for t in labels if t != -100]
    if not trained:
        sys.exit("ERROR: la màscara deixa la primera conversa sense cap token de resposta")
    decoded = tokenizer.decode(trained)
    if "<|turn>user" in decoded or "<|turn>system" in decoded:
        sys.exit("ERROR: la màscara entrena també sobre el torn de l'usuari o del sistema")
    log(f"Màscara correcta: {len(trained)}/{len(labels)} tokens entrenats a la primera conversa")
    log(f"Tokens entrenats (inici): {decoded[:300]!r}")


def write_samples(model, tokenizer, cfg: dict, system: str, path: Path) -> None:
    FastModel.for_inference(model)
    lines = ["# Mostres després d'entrenar\n"]
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
        log(f"Mostra: {question}")
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
        # La plantilla posa <bos>; el tokenitzador el torna a afegir en entrenar.
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
    log(f"Converses: train {len(data['train'])}, valid {len(data['valid'])}")

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
    log(f"Reprenent de {last}" if last else "Entrenament des de zero")
    trainer.train(resume_from_checkpoint=last)

    model.save_pretrained(str(out / "adapter"))
    tokenizer.save_pretrained(str(out / "adapter"))
    log("Adaptador LoRA desat")

    metrics = {
        "final_eval": trainer.evaluate(),
        "log_history": trainer.state.log_history,
        "config": cfg,
    }
    (out / "metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    log(f"Pèrdua final a valid: {metrics['final_eval'].get('eval_loss')}")

    # Les mostres i el GGUF són extres: si fallen, l'adaptador ja és desat.
    try:
        write_samples(model, tokenizer, cfg, system, out / "mostres.md")
    except Exception as exc:
        log(f"AVÍS: no s'han pogut generar mostres: {exc}")
    if cfg.get("export_gguf"):
        try:
            model.save_pretrained_gguf(str(out / "gguf"), tokenizer, quantization_method="q4_k_m")
            log("GGUF q4_k_m desat")
        except Exception as exc:
            log(f"AVÍS: no s'ha pogut exportar el GGUF: {exc}")


if __name__ == "__main__":
    main()
