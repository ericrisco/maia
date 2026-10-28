#!/bin/bash
# Startup script of the training VM. Runs as root on every boot.
# Reads the bucket and the run from the metadata, trains, uploads the results and shuts the VM down.
# If a spot VM is interrupted and started again, it resumes from the last uploaded checkpoint.
set -uo pipefail

MD=http://metadata.google.internal/computeMetadata/v1/instance/attributes
meta() { curl -sf -H "Metadata-Flavor: Google" "$MD/$1"; }
BUCKET=$(meta bucket)
RUN=$(meta run)
GS="gs://$BUCKET/runs/$RUN"
WORK=/opt/maia
export HOME=/root
mkdir -p "$WORK/output"
LOG="$WORK/train.log"
# A new VM (recreated in another zone) continues the run's log instead of overwriting it.
[ -f "$LOG" ] || gcloud storage cp "$GS/train.log" "$LOG" >/dev/null 2>&1 || true
exec > >(tee -a "$LOG") 2>&1

echo "=== boot $(date -Is) run=$RUN"
if gcloud storage ls "$GS/DONE" >/dev/null 2>&1; then
  echo "The run is already finished: shutting down."
  shutdown -h now
  exit 0
fi

# Upload the log every minute so the notebook can follow it.
( while true; do gcloud storage cp -q "$LOG" "$GS/train.log" >/dev/null 2>&1; sleep 60; done ) &

gcloud storage rsync -r "$GS/input" "$WORK/input"
# Checkpoints from a previous boot (if any).
gcloud storage rsync -r "$GS/output" "$WORK/output" 2>/dev/null || true

nvidia-smi || { echo "ERROR: no GPU"; echo gpu | gcloud storage cp - "$GS/FAILED"; shutdown -h now; exit 1; }

if [ ! -x "$WORK/venv/bin/python" ]; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
  "$HOME/.local/bin/uv" venv --python 3.12 "$WORK/venv"
  "$HOME/.local/bin/uv" pip install --python "$WORK/venv/bin/python" unsloth
fi
"$WORK/venv/bin/python" -c "import unsloth, torch; print('unsloth', unsloth.__version__, 'torch', torch.__version__)"

# Back up the checkpoints every 5 minutes (a spot VM can go away at any moment).
( while true; do sleep 300; gcloud storage rsync -r "$WORK/output" "$GS/output" >/dev/null 2>&1; done ) &

"$WORK/venv/bin/python" "$WORK/input/train.py" \
  --config "$WORK/input/config.json" --data "$WORK/input/data" --out "$WORK/output"
STATUS=$?

gcloud storage rsync -r "$WORK/output" "$GS/output"
if [ $STATUS -eq 0 ]; then
  date -Is | gcloud storage cp - "$GS/DONE"
else
  echo "$STATUS" | gcloud storage cp - "$GS/FAILED"
fi
echo "=== end $(date -Is) status=$STATUS"
gcloud storage cp "$LOG" "$GS/train.log"
shutdown -h now
