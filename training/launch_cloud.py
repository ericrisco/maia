"""Launches a full maia run on Google Cloud (training, evaluation, watchdog), no laptop involved.

Stages runs/<run>/input (export/<variant>, train.py, config.json), uploads it with the evaluation
bundle (maia-bench at origin/main + the fact probe) and the VM scripts to gs://<bucket>/runs/<run>/,
then creates the spot training VM (vm-startup.sh) and the standard watchdog VM (vm-watchdog.sh).
The watchdog restarts or moves the spot VMs, starts the evaluation (vm-eval.sh) when training is
DONE and shuts itself down when the evaluation is DONE. Results end up in gs://<bucket>/runs/<run>/eval/.

Usage:
    python training/launch_cloud.py --size e4b --model unsloth/gemma-4-E4B-it-unsloth-bnb-4bit
    python training/launch_cloud.py --size 12b --model unsloth/gemma-4-12b-it \
        --batch-size 2 --grad-accum 8 --eval-machine g2-standard-16
    (add --dry-run to stage the input locally without touching the cloud)
"""

from __future__ import annotations

import argparse
import datetime
import io
import json
import shutil
import subprocess
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT.parent / "maia-bench"
PROJECT, BUCKET = "maia-andorra", "maia-andorra-entrenaments"
ACCOUNT = "ericriscodelatorre@gmail.com"
TRAIN_SA = f"maia-entrenament@{PROJECT}.iam.gserviceaccount.com"
# Default Compute service account (project editor): creates VMs and calls the Vertex batch judge.
CLOUD_SA = "617635882638-compute@developer.gserviceaccount.com"
ZONES = [
    *("europe-west4-a", "europe-west4-b", "europe-west4-c", "europe-west1-b", "europe-west1-c"),
    *("europe-west3-a", "europe-west3-b", "europe-west2-a", "europe-west2-b", "europe-west6-b"),
    *("europe-west6-c", "europe-west9-a", "europe-west9-b", "europe-west9-c"),
    *("europe-southwest1-a", "europe-southwest1-b", "europe-southwest1-c"),
]
PROBE_FILES = [
    "training-data/scripts/run_fact_probe.py",
    "training-data/scripts/score_fact_probe.py",
    "training-data/facts/canon-facts-probe.jsonl",
    "training-data/missatge-sistema.txt",
]
PROMPTS = [
    "Què és el Consell de la Terra?",
    "Quines són les set parròquies d'Andorra?",
    "Explica'm què era la Querimònia.",
    "Què es menja per Sant Jordi a Andorra?",
    "Com va anar la reforma constitucional del 1993?",
]


def gcloud(*args: str) -> str:
    result = subprocess.run(
        ["gcloud", *args, f"--project={PROJECT}", f"--account={ACCOUNT}"],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result.stdout.strip()


def eval_bundle(path: Path) -> None:
    """maia-bench at origin/main (without stored results) and maia's probe files, as one tgz."""
    archive = subprocess.run(
        ["git", "-C", str(BENCH), "archive", "origin/main"], capture_output=True, check=True
    ).stdout
    with (
        tarfile.open(fileobj=io.BytesIO(archive)) as bench,
        tarfile.open(path, "w:gz") as out,
    ):
        for member in bench.getmembers():
            if member.name.startswith("results/") and member.name.count("/") > 1:
                continue
            data = bench.extractfile(member) if member.isfile() else None
            member.name = f"bench/{member.name}"
            out.addfile(member, data)
        for name in PROBE_FILES:
            out.add(ROOT / name, arcname=f"maia/{name}")


def create_vm(name: str, zones: list[str], **flags: str) -> str:
    """Creates the VM in the first zone with capacity and returns that zone."""
    for zone in zones:
        try:
            gcloud(
                "compute", "instances", "create", name, f"--zone={zone}",
                *(f"--{key.replace('_', '-')}={value}" for key, value in flags.items()),
            )  # fmt: skip
            return zone
        except RuntimeError as error:
            message = str(error)
            if "EXHAUSTED" not in message and "STOCKOUT" not in message:
                raise
            print(f"{zone}: no capacity", flush=True)
    raise SystemExit(f"ERROR: no zone with capacity for {name}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", required=True, help="e4b, 12b... (run name, Ollama names)")
    parser.add_argument("--model", required=True, help="Unsloth model id, loaded in 4 bits")
    parser.add_argument("--variant", default="K", help="export/<variant>")
    parser.add_argument("--epochs", type=int, default=2)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--grad-accum", type=int, default=4)
    parser.add_argument("--train-machine", default="g2-standard-8")
    parser.add_argument("--eval-machine", default="g2-standard-8")
    parser.add_argument("--hours", type=int, default=10, help="max run duration of each spot boot")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    stamp = f"{datetime.datetime.now():%Y%m%d-%H%M}"
    run = f"{stamp}-{args.size}-{args.variant.lower()}-canon"
    gs = f"gs://{BUCKET}/runs/{run}"
    stage = ROOT / "runs" / run / "input"
    (stage / "data").mkdir(parents=True)
    for name in ("train.jsonl", "valid.jsonl"):
        shutil.copy(ROOT / "export" / args.variant / name, stage / "data" / name)
    shutil.copy(ROOT / "training" / "train.py", stage / "train.py")
    config = {
        "model": args.model,
        "variant": f"{args.variant}-canon",
        "chat_template": "gemma-4",
        "max_seq_length": 2048,
        "lora_r": 32,
        "lora_alpha": 32,
        "epochs": args.epochs,
        "learning_rate": 0.0002,
        "batch_size": args.batch_size,
        "grad_accum": args.grad_accum,
        "eval_steps": 200,
        "seed": 3407,
        "export_gguf": False,
        "greedy_samples": True,
        "env": {"UNSLOTH_BLOCK_COMPILE": "0"},
        "prompts": PROMPTS,
        "run": run,
    }
    (stage / "config.json").write_text(
        json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    for name in ("vm-startup.sh", "vm-eval.sh", "merge_adapter.py"):
        shutil.copy(ROOT / "training" / name, stage / name)
    eval_bundle(stage / "eval-bundle.tgz")
    print(f"staged {stage}")
    if args.dry_run:
        return

    gcloud("storage", "rsync", "-r", str(stage), f"{gs}/input")
    print(f"uploaded {gs}/input", flush=True)
    zone = create_vm(
        f"maia-{run}",
        ZONES,
        machine_type=args.train_machine,
        maintenance_policy="TERMINATE",
        image_family="common-cu129-ubuntu-2204-nvidia-580",
        image_project="deeplearning-platform-release",
        boot_disk_size="200GB",
        boot_disk_type="pd-balanced",
        service_account=TRAIN_SA,
        scopes="cloud-platform",
        metadata=f"bucket={BUCKET},run={run},install-nvidia-driver=True",
        metadata_from_file=f"startup-script={ROOT / 'training' / 'vm-startup.sh'}",
        labels=f"maia=training,run={run}",
        max_run_duration=f"{args.hours}h",
        instance_termination_action="STOP",
        provisioning_model="SPOT",
    )
    print(f"training VM in {zone}", flush=True)
    watchdog = {
        "bucket": BUCKET,
        "run": run,
        "size": args.size,
        "tag": stamp,
        "bench": f"maia_{args.size}_{stamp}",
        "account": CLOUD_SA,
        "train_account": TRAIN_SA,
        "train_machine": args.train_machine,
        "eval_machine": args.eval_machine,
        "zones": " ".join(ZONES),
    }
    create_vm(
        f"maia-watchdog-{run}",
        [zone],
        machine_type="e2-small",
        image_family="debian-12",
        image_project="debian-cloud",
        boot_disk_size="10GB",
        service_account=CLOUD_SA,
        scopes="cloud-platform",
        metadata="^;^" + ";".join(f"{key}={value}" for key, value in watchdog.items()),
        metadata_from_file=f"startup-script={ROOT / 'training' / 'vm-watchdog.sh'}",
        labels=f"maia=watchdog,run={run}",
    )
    print(f"watchdog VM in {zone}. Results: {gs}/eval/ (log {gs}/eval.log)")


if __name__ == "__main__":
    main()
