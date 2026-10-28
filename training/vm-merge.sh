#!/bin/bash
# Startup script of the merge VM. Runs as root on boot.
# Downloads a finished run's adapter from the bucket, merges it into the 16-bit base model
# (merge_adapter.py), uploads the result to gs://<bucket>/runs/<run>/merged/ and shuts the VM down.
set -uo pipefail

MD=http://metadata.google.internal/computeMetadata/v1/instance/attributes
meta() { curl -sf -H "Metadata-Flavor: Google" "$MD/$1"; }
BUCKET=$(meta bucket)
RUN=$(meta run)
GS="gs://$BUCKET/runs/$RUN"
WORK=/opt/maia
export HOME=/root
mkdir -p "$WORK"
LOG="$WORK/merge.log"
exec > >(tee -a "$LOG") 2>&1

echo "=== boot $(date -Is) run=$RUN"
if gcloud storage ls "$GS/merged/DONE" >/dev/null 2>&1; then
  echo "Already merged: shutting down."
  shutdown -h now
  exit 0
fi
( while true; do gcloud storage cp -q "$LOG" "$GS/merge.log" >/dev/null 2>&1; sleep 60; done ) &

gcloud storage rsync -r "$GS/output/adapter" "$WORK/adapter"
gcloud storage cp "$GS/input/merge_adapter.py" "$WORK/merge_adapter.py"

if [ ! -x "$WORK/venv/bin/python" ]; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
  "$HOME/.local/bin/uv" venv --python 3.12 "$WORK/venv"
  "$HOME/.local/bin/uv" pip install --python "$WORK/venv/bin/python" unsloth
fi

UNSLOTH_BLOCK_COMPILE=0 "$WORK/venv/bin/python" "$WORK/merge_adapter.py" \
  --adapter "$WORK/adapter" --out "$WORK/merged"
STATUS=$?

if [ $STATUS -eq 0 ]; then
  gcloud storage rsync -r "$WORK/merged" "$GS/merged" && date -Is | gcloud storage cp - "$GS/merged/DONE"
else
  echo "$STATUS" | gcloud storage cp - "$GS/merged/FAILED"
fi
echo "=== end $(date -Is) status=$STATUS"
gcloud storage cp "$LOG" "$GS/merge.log"
shutdown -h now
