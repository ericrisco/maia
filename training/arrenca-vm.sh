#!/bin/bash
# Startup script de la VM d'entrenament. S'executa com a root a cada arrencada.
# Llegeix el bucket i el run de les metadades, entrena, puja els resultats i apaga la VM.
# Si una VM spot s'interromp i es torna a engegar, reprèn des de l'últim checkpoint pujat.
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
exec > >(tee -a "$LOG") 2>&1

echo "=== arrencada $(date -Is) run=$RUN"
if gcloud storage ls "$GS/DONE" >/dev/null 2>&1; then
  echo "El run ja està acabat: apago."
  shutdown -h now
  exit 0
fi

# Puja el log cada minut perquè el notebook el pugui seguir.
( while true; do gcloud storage cp -q "$LOG" "$GS/train.log" >/dev/null 2>&1; sleep 60; done ) &

gcloud storage rsync -r "$GS/input" "$WORK/input"
# Checkpoints d'una arrencada anterior (si n'hi ha).
gcloud storage rsync -r "$GS/output" "$WORK/output" 2>/dev/null || true

nvidia-smi || { echo "ERROR: no hi ha GPU"; echo gpu | gcloud storage cp - "$GS/FAILED"; shutdown -h now; exit 1; }

if [ ! -x "$WORK/venv/bin/python" ]; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
  "$HOME/.local/bin/uv" venv --python 3.12 "$WORK/venv"
  "$HOME/.local/bin/uv" pip install --python "$WORK/venv/bin/python" unsloth
fi
"$WORK/venv/bin/python" -c "import unsloth, torch; print('unsloth', unsloth.__version__, 'torch', torch.__version__)"

# Còpia de seguretat dels checkpoints cada 5 minuts (una VM spot pot caure en qualsevol moment).
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
echo "=== final $(date -Is) estat=$STATUS"
gcloud storage cp "$LOG" "$GS/train.log"
shutdown -h now
