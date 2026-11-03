#!/bin/bash
# Startup script of the evaluation VM. Runs as root on every boot.
# For a finished run: merges the adapter into the 16-bit base, converts it to GGUF Q4_K_M, serves it
# with Ollama, runs the fact probe (base model and maia) and the full maia-bench, judges the open and
# trap questions with the Vertex batch judge, uploads everything to gs://<bucket>/runs/<run>/eval/ and
# shuts the VM down. Every step is skipped when its output already exists, so a spot VM that is
# interrupted and started again carries on where it stopped.
#
# Metadata: bucket, run, tag (Ollama tag), bench (results folder name), account (service account).
# The launcher uploads gs://<bucket>/runs/<run>/input/eval-bundle.tgz with maia-bench (git archive)
# under bench/ and maia's probe files under maia/.
set -uo pipefail

MD=http://metadata.google.internal/computeMetadata/v1/instance/attributes
meta() { curl -sf -H "Metadata-Flavor: Google" "$MD/$1"; }
BUCKET=$(meta bucket)
RUN=$(meta run)
TAG=$(meta tag)
BENCH=$(meta bench)
GCP_ACCOUNT=$(meta account)
export GCP_ACCOUNT
GS="gs://$BUCKET/runs/$RUN"
WORK=/opt/maia
export HOME=/root
export PATH="$HOME/.local/bin:$PATH"
mkdir -p "$WORK/eval"
LOG="$WORK/eval.log"
[ -f "$LOG" ] || gcloud storage cp "$GS/eval.log" "$LOG" >/dev/null 2>&1 || true
exec > >(tee -a "$LOG") 2>&1
step() { echo "=== $(date -Is) $*"; }
fail() {
  step "FAILED: $*"
  echo "$*" | gcloud storage cp - "$GS/eval/FAILED"
  gcloud storage cp "$LOG" "$GS/eval.log"
  shutdown -h now
  exit 1
}

step "boot run=$RUN tag=$TAG bench=$BENCH"
if gcloud storage ls "$GS/eval/DONE" >/dev/null 2>&1; then
  step "evaluation already finished: shutting down"
  shutdown -h now
  exit 0
fi
( while true; do gcloud storage cp -q "$LOG" "$GS/eval.log" >/dev/null 2>&1; sleep 60; done ) &

nvidia-smi >/dev/null || fail "no GPU"
command -v uv >/dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh

# 1. Merge (same method as vm-merge.sh: the adapter on top of the 16-bit base weights).
if [ ! -f "$WORK/merged/DONE" ]; then
  step "merge"
  gcloud storage rsync -r "$GS/output/adapter" "$WORK/adapter" || fail "no adapter"
  gcloud storage cp "$GS/input/merge_adapter.py" "$WORK/merge_adapter.py" || fail "no merge_adapter.py"
  if [ ! -x "$WORK/venv/bin/python" ]; then
    uv venv --python 3.12 "$WORK/venv"
    uv pip install --python "$WORK/venv/bin/python" unsloth
  fi
  UNSLOTH_BLOCK_COMPILE=0 "$WORK/venv/bin/python" "$WORK/merge_adapter.py" \
    --adapter "$WORK/adapter" --out "$WORK/merged" || fail "merge"
  gcloud storage rsync -r "$WORK/merged" "$GS/merged" && date -Is | gcloud storage cp - "$GS/merged/DONE"
  date -Is > "$WORK/merged/DONE"
fi

# 2. GGUF bf16 with llama.cpp's converter, then Q4_K_M with llama-quantize (same method as the v2 run).
GGUF="$WORK/gguf/maia-bf16.gguf"
if [ ! -f "$GGUF.done" ]; then
  step "convert to GGUF bf16"
  mkdir -p "$WORK/gguf"
  [ -d "$WORK/llama.cpp" ] || git clone -q --depth 1 https://github.com/ggml-org/llama.cpp "$WORK/llama.cpp"
  (cd "$WORK/llama.cpp" && uv run --no-project --python 3.12 --with transformers --with torch --with ./gguf-py \
    --with sentencepiece --with protobuf --with numpy --index-strategy unsafe-best-match \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    python convert_hf_to_gguf.py "$WORK/merged" --outtype bf16 --outfile "$GGUF") || fail "GGUF conversion"
  touch "$GGUF.done"
fi
# Ollama only quantizes safetensors imports: Q4_K_M is made with llama.cpp's llama-quantize.
Q4="$WORK/gguf/maia-Q4_K_M.gguf"
if [ ! -f "$Q4.done" ]; then
  step "quantize Q4_K_M"
  command -v cmake >/dev/null || (apt-get update -qq && apt-get install -y -qq cmake build-essential) \
    || fail "cmake install"
  (cd "$WORK/llama.cpp" && cmake -B build -DGGML_CUDA=OFF -DLLAMA_CURL=OFF >/dev/null \
    && cmake --build build --target llama-quantize -j "$(nproc)" >/dev/null) || fail "llama-quantize build"
  "$WORK/llama.cpp/build/bin/llama-quantize" "$GGUF" "$Q4" Q4_K_M | tail -2 || fail "quantize"
  touch "$Q4.done"
fi

# 3. Ollama on the GPU.
if ! command -v ollama >/dev/null; then
  step "install ollama"
  curl -fsSL https://ollama.com/install.sh | sh || fail "ollama install"
fi
systemctl start ollama 2>/dev/null || (ollama serve >/var/log/ollama.log 2>&1 &)
for _ in $(seq 60); do curl -sf localhost:11434/api/version >/dev/null && break; sleep 2; done
if ! ollama list | grep -q "maia-e4b:$TAG"; then
  step "ollama create maia-e4b:$TAG (Q4_K_M)"
  cat > "$WORK/gguf/Modelfile" <<EOF
FROM $Q4
RENDERER gemma4
PARSER gemma4
PARAMETER temperature 1
PARAMETER top_k 64
PARAMETER top_p 0.95
EOF
  (cd "$WORK/gguf" && ollama create "maia-e4b:$TAG" -f Modelfile) || fail "ollama create"
  # The quantized model is published later: keep a copy of its GGUF in the bucket.
  gcloud storage cp "$Q4" "$GS/gguf/maia-e4b-Q4_K_M.gguf"
fi
ollama list | grep -q "gemma4:e4b" || ollama pull gemma4:e4b || fail "pull gemma4:e4b"

# 4. Code: maia-bench and maia's probe files.
if [ ! -d "$WORK/bundle" ]; then
  mkdir -p "$WORK/bundle"
  gcloud storage cp "$GS/input/eval-bundle.tgz" "$WORK/eval-bundle.tgz" || fail "no eval bundle"
  tar -xzf "$WORK/eval-bundle.tgz" -C "$WORK/bundle"
fi
cd "$WORK/bundle/maia" || fail "no maia bundle"

# 5. Fact probe: base model and maia, both at temperature 0 through Ollama.
PROBE="$WORK/eval/probe"
mkdir -p "$PROBE"
if [ ! -f "$PROBE/score.txt" ]; then
  step "fact probe"
  [ -s "$PROBE/samples_before.md" ] || python3 training-data/scripts/run_fact_probe.py gemma4:e4b \
    "$PROBE/samples_before.md" --threads 4 || fail "probe (base)"
  [ -s "$PROBE/samples.md" ] || python3 training-data/scripts/run_fact_probe.py "maia-e4b:$TAG" \
    "$PROBE/samples.md" --threads 4 || fail "probe (maia)"
  python3 training-data/scripts/score_fact_probe.py "$PROBE" > "$PROBE/score.txt"
  tail -2 "$PROBE/score.txt"
  gcloud storage rsync -r "$PROBE" "$GS/eval/probe"
fi

# 6. maia-bench: answers (resumable), batch judge, summary.
cd "$WORK/bundle/bench" || fail "no maia-bench bundle"
step "bench answers"
uv run python tools/run.py --model "ollama:maia-e4b:$TAG" --name "$BENCH" --origin "maia (privat)" \
  --threads 4 || fail "bench answers"
gcloud storage rsync -r "results/$BENCH" "$GS/eval/bench"
step "batch judge"
uv run python tools/judge_batch.py "results/$BENCH" || fail "batch judge"
uv run python tools/score.py "results/$BENCH" --no-judge || fail "score"
gcloud storage rsync -r "results/$BENCH" "$GS/eval/bench"

date -Is | gcloud storage cp - "$GS/eval/DONE"
step "end"
gcloud storage cp "$LOG" "$GS/eval.log"
shutdown -h now
