# Training

How to train, evaluate and publish a maia model on Google Cloud. The story behind these choices, including what
failed, is on [how maia was trained](https://ericrisco.github.io/maia-bench/training.html).

## Requirements

- A Google Cloud project with L4 quota and a bucket. The names are constants at the top of `launch_cloud.py`
  (`PROJECT`, `BUCKET`, `ACCOUNT`, `TRAIN_SA`, `CLOUD_SA`), so change them to use your own project.
- `gcloud` authenticated, and a checkout of [maia-bench](https://github.com/ericrisco/maia-bench) next to this repo.
- A Hugging Face token with write access, as `HF_TOKEN`, to publish.

## Run it

```bash
# 1. Build export/K from training-data/datasets/ (export/ is not versioned).
python3 scripts/exporta_dataset.py

# 2. Start training, then evaluation. Add --dry-run to stage the input without touching the cloud.
python training/launch_cloud.py --size e4b --model unsloth/gemma-4-E4B-it-unsloth-bnb-4bit
python training/launch_cloud.py --size 12b --model unsloth/gemma-4-12b-it \
    --batch-size 2 --grad-accum 8 --eval-machine g2-standard-16
```

No further command is needed until the evaluation ends. Results land in `gs://<bucket>/runs/<run>/`; the run is named
`<date>-<time>-<size>-<variant>`. `DONE` marks the end of training, and `eval/DONE` or `eval/FAILED` the end of the
evaluation.

## What runs where

| File | Runs on | What it does |
|---|---|---|
| `launch_cloud.py` | Your machine | Stages the run, uploads it, and creates the training and watchdog VMs. |
| `vm-startup.sh`, `train.py` | Spot VM with one L4 | QLoRA with Unsloth. Loss on the responses only. A checkpoint every `eval_steps`; resumes from the last one. |
| `vm-watchdog.sh` | Small standard VM | Restarts reclaimed VMs. After 3 failed starts it recreates the VM in another zone. Starts the evaluation when training is done. |
| `vm-eval.sh`, `merge_adapter.py` | Spot VM with one L4 | Merge on the 16-bit base, GGUF, Q4_K_M, Ollama, fact probe, maia-bench, Vertex batch judge. Every step is skipped if its output exists. |
| `upload_hf.py` | Any machine with the run folder | Adapter, GGUF and card to `<user>/gemma-maia-<size>`, tagged with the run name. |
| `upload_dataset_hf.py` | Any machine with the run folder | Train and valid files and the fact probe to `<user>/maia-training-data`, with the same tag. |

`train.ipynb` and `vm-merge.sh` are the earlier manual route, and they are not part of this chain.

## Before publishing

1. **Compare with the base model.** Paired bootstrap on question ids, on the same benchmark version.
2. **Check similarity with the benchmark.** Compare the training questions with the benchmark's, and report the gain
   on questions with no similar practice question. `training-data/scripts/build_multiple_choice.py` drops only those
   with a word overlap of 0.5 or more (`MAX_BENCH_SIMILARITY`), which proved too loose.
3. **Sweep for personal data.** Emails, phones, identity documents and names of private individuals. Generated wrong
   options can contain invented names, so check them too. To leave rows out of the public file:

   ```bash
   python training/upload_dataset_hf.py runs/<run> --public --train <filtered.jsonl> --withheld <n>
   ```

4. **Publish.**

   ```bash
   python training/upload_hf.py runs/<run> --public --gguf <file.gguf> --evaluation <evaluation.md>
   ```

   `runs/<run>` needs `input/` and `output/` copied from the bucket, without the checkpoints.

## Known limits

- The watchdog changes zone only after failed starts, not when a zone keeps interrupting a running VM.
- Fine-tuning can erase a format the base model already knew. The first 12B answered 67 of 604 multiple-choice
  questions with a sentence, because the data had none.
