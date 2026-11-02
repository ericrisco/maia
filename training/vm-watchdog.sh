#!/bin/bash
# Startup script of the watchdog VM (small, standard, not spot). Runs as root on boot.
# Keeps one run moving without anyone's laptop: starts the spot training VM again when it is
# interrupted, creates the evaluation VM (vm-eval.sh) once training is DONE, starts that one again
# when it is interrupted, deletes the finished VMs and shuts itself down at the end.
#
# Metadata: bucket, run, tag, bench, account (service account of the evaluation VM), train_account
# (service account of the training VM), zones. The launcher uploads vm-startup.sh and vm-eval.sh to
# gs://<bucket>/runs/<run>/input/.
set -uo pipefail

MD=http://metadata.google.internal/computeMetadata/v1/instance/attributes
meta() { curl -sf -H "Metadata-Flavor: Google" "$MD/$1"; }
BUCKET=$(meta bucket)
RUN=$(meta run)
TAG=$(meta tag)
BENCH=$(meta bench)
ACCOUNT=$(meta account)
ZONES=$(meta zones)
TRAIN_ACCOUNT=$(meta train_account)
GS="gs://$BUCKET/runs/$RUN"
TRAIN_VM="maia-$RUN"
EVAL_VM="maia-eval-$RUN"
LOG=/var/log/maia-watchdog.log
exec > >(tee -a "$LOG") 2>&1
step() { echo "=== $(date -Is) $*"; }
exists() { gcloud storage ls "$1" >/dev/null 2>&1; }
zone_of() { gcloud compute instances list --filter="name=$1" --format='value(zone.basename())' 2>/dev/null; }
status_of() {
  local z
  z=$(zone_of "$1")
  [ -n "$z" ] && gcloud compute instances describe "$1" --zone="$z" --format='value(status)' 2>/dev/null
}
# Starts a stopped VM again. After 3 failed starts in its zone (no spot capacity), the VM is deleted and
# recreated in the first zone with capacity: training resumes from the checkpoints in the bucket, and
# the evaluation skips the steps whose results are already uploaded.
declare -A FAILS
restart() {
  local z
  z=$(zone_of "$1")
  step "$1 is stopped without a result: starting it again"
  if gcloud compute instances start "$1" --zone="$z" --quiet >/dev/null 2>&1; then
    FAILS[$1]=0
    return 0
  fi
  FAILS[$1]=$(( ${FAILS[$1]:-0} + 1 ))
  step "start failed in $z (${FAILS[$1]}/3)"
  if [ "${FAILS[$1]}" -ge 3 ]; then
    delete "$1"
    FAILS[$1]=0
    if [ "$1" = "$TRAIN_VM" ]; then create_train; else create_eval; fi
  fi
}
delete() {
  local z
  z=$(zone_of "$1")
  [ -n "$z" ] && gcloud compute instances delete "$1" --zone="$z" --quiet >/dev/null 2>&1 && step "deleted $1"
}
create_train() {
  local zone
  for zone in $ZONES; do
    if gcloud compute instances create "$TRAIN_VM" --zone="$zone" --machine-type=g2-standard-8 \
        --maintenance-policy=TERMINATE --image-family=common-cu129-ubuntu-2204-nvidia-580 \
        --image-project=deeplearning-platform-release --boot-disk-size=200GB --boot-disk-type=pd-balanced \
        --service-account="$TRAIN_ACCOUNT" --scopes=cloud-platform \
        --metadata="bucket=$BUCKET,run=$RUN,install-nvidia-driver=True" \
        --metadata-from-file=startup-script=/opt/maia/vm-startup.sh \
        --labels="maia=training,run=$RUN" --max-run-duration=10h --instance-termination-action=STOP \
        --provisioning-model=SPOT >/dev/null 2>&1; then
      step "training VM recreated in $zone"
      return 0
    fi
  done
  step "no zone with capacity for the training VM, will retry"
}
create_eval() {
  local zone
  for zone in $ZONES; do
    if gcloud compute instances create "$EVAL_VM" --zone="$zone" --machine-type=g2-standard-8 \
        --maintenance-policy=TERMINATE --image-family=common-cu129-ubuntu-2204-nvidia-580 \
        --image-project=deeplearning-platform-release --boot-disk-size=200GB --boot-disk-type=pd-balanced \
        --service-account="$ACCOUNT" --scopes=cloud-platform \
        --metadata="bucket=$BUCKET,run=$RUN,tag=$TAG,bench=$BENCH,account=$ACCOUNT,install-nvidia-driver=True" \
        --metadata-from-file=startup-script=/opt/maia/vm-eval.sh \
        --labels="maia=eval,run=$RUN" --max-run-duration=12h --instance-termination-action=STOP \
        --provisioning-model=SPOT >/dev/null 2>&1; then
      step "evaluation VM created in $zone"
      return 0
    fi
  done
  step "no zone with capacity for the evaluation VM, will retry"
}

mkdir -p /opt/maia
gcloud storage cp "$GS/input/vm-eval.sh" /opt/maia/vm-eval.sh
gcloud storage cp "$GS/input/vm-startup.sh" /opt/maia/vm-startup.sh
step "watching run $RUN"
while true; do
  if exists "$GS/FAILED"; then step "training FAILED"; break; fi
  if exists "$GS/eval/FAILED"; then step "evaluation FAILED"; break; fi
  if exists "$GS/eval/DONE"; then
    step "evaluation DONE"
    delete "$EVAL_VM"
    break
  fi
  if ! exists "$GS/DONE"; then
    case "$(status_of "$TRAIN_VM")" in
      TERMINATED|STOPPED) restart "$TRAIN_VM" ;;
    esac
  else
    [ -n "$(zone_of "$TRAIN_VM")" ] && delete "$TRAIN_VM"
    case "$(status_of "$EVAL_VM")" in
      "") create_eval ;;
      TERMINATED|STOPPED) restart "$EVAL_VM" ;;
    esac
  fi
  gcloud storage cp -q "$LOG" "$GS/watchdog.log" >/dev/null 2>&1
  sleep 300
done
gcloud storage cp -q "$LOG" "$GS/watchdog.log" >/dev/null 2>&1
shutdown -h now
