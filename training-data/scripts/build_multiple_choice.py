"""Builds multiple-choice conversations from the canon facts, so the model keeps the answer format.

The fine-tuned 12B answered maia-bench multiple-choice questions with a sentence instead of the letter
(67 of 604): the corpus had no multiple-choice conversation at all. This script asks Gemini (one Vertex AI
batch job, nothing runs locally) for two questions per canon fact with the correct option and three
plausible wrong ones; siblings of the fact's contrast group are offered as distractors. The letters are
shuffled here with a fixed seed, the assistant answers with the letter only, and questions close to any
maia-bench question are dropped.

Usage:
    python3 training-data/scripts/build_multiple_choice.py [--model gemini-3.8-flash]
    -> training-data/datasets/canon-multiple-choice.jsonl (overwritten)
"""

from __future__ import annotations

import argparse
import datetime
import io
import json
import random
import re
import subprocess
import sys
import tarfile
import time
import unicodedata
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
BENCH = ROOT.parent / "maia-bench"
FACTS = ROOT / "training-data/facts/canon-facts.jsonl"
GROUPS = ROOT / "training-data/facts/canon-contrast-groups.jsonl"
BASIC = ROOT / "training-data/datasets/canon-basic.jsonl"
OUT = ROOT / "training-data/datasets/canon-multiple-choice.jsonl"
PROJECT, ACCOUNT = "maia-andorra", "ericriscodelatorre@gmail.com"
BUCKET = "gs://maia-andorra-entrenaments/multiple-choice-batch"
API = f"https://aiplatform.googleapis.com/v1/projects/{PROJECT}/locations/global/batchPredictionJobs"
FINAL_STATES = ("JOB_STATE_SUCCEEDED", "JOB_STATE_FAILED", "JOB_STATE_CANCELLED", "JOB_STATE_EXPIRED",
                "JOB_STATE_PARTIALLY_SUCCEEDED")
# Same wording as maia-bench's tools/run.py: the format the model has to keep.
INSTRUCTION = "Respon només amb la lletra de l'opció correcta (A, B, C o D)."
SEED = 20261104
MAX_BENCH_SIMILARITY = 0.5

PROMPT = """Ets un redactor de preguntes de tipus test sobre Andorra, en català.

Fet verificat: {fact}
{siblings}
Escriu DUES preguntes de tipus test diferents sobre aquest fet (formulació i angle diferents).
Per a cada pregunta:
- La pregunta s'ha de poder respondre només amb el fet, sense dir «segons el text» ni citar cap document.
- "correct": l'opció correcta, breu.
- "distractors": tres opcions falses però versemblants, del mateix tipus que la correcta (dates amb dates,
  persones amb persones...), clarament incorrectes segons el fet i sense repetir-se.
- Res de «totes les anteriors» ni «cap de les anteriors».

Respon només amb JSON: {{"questions": [{{"question": "...", "correct": "...", "distractors": ["...", "...", "..."]}}, ...]}}"""


def gcloud(*args: str) -> str:
    return subprocess.run(["gcloud", *args, f"--project={PROJECT}", f"--account={ACCOUNT}"],
                          check=True, capture_output=True, text=True).stdout


def api(url: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
    token = subprocess.run(["gcloud", "auth", "print-access-token", f"--account={ACCOUNT}"],
                           check=True, capture_output=True, text=True).stdout.strip()
    request = urllib.request.Request(url, data=json.dumps(body).encode() if body else None,
                                     headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(request, timeout=120))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def words(text: str) -> set[str]:
    text = unicodedata.normalize("NFKD", text.lower())
    return set(re.findall(r"[a-z0-9]{3,}", "".join(c for c in text if not unicodedata.combining(c))))


def bench_questions() -> list[set[str]]:
    """Every maia-bench question at origin/main, as word sets."""
    archive = subprocess.run(["git", "-C", str(BENCH), "archive", "origin/main", "knowledge", "holdout"],
                             capture_output=True, check=True).stdout
    out = []
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        for member in tar.getmembers():
            if member.isfile() and member.name.endswith(".jsonl"):
                for line in tar.extractfile(member).read().decode("utf-8").splitlines():
                    if line.strip():
                        out.append(words(json.loads(line)["question"]))
    return out


def similarity(a: set[str], b: set[str]) -> float:
    return len(a & b) / len(a | b) if a and b else 0.0


def requests(facts: list[dict[str, Any]], groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    siblings: dict[str, tuple[str, list[str]]] = {}
    for group in groups:
        for member in group["members"]:
            others = [m["entity_name"] for m in group["members"] if m["fact_id"] != member["fact_id"]]
            siblings[member["fact_id"]] = (group["entity_class"], others)
    rows = []
    for fact in facts:
        hint = ""
        if fact["fact_id"] in siblings:
            kind, others = siblings[fact["fact_id"]]
            hint = f"Altres {kind} del mateix grup (bons distractors si escau): {'; '.join(others)}\n"
        rows.append({"key": fact["fact_id"], "request": {
            "contents": [{"role": "user", "parts": [{"text": PROMPT.format(fact=fact["fact"], siblings=hint)}]}],
            "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4000,
                                 "responseMimeType": "application/json"}}})
    return rows


def run_batch(rows: list[dict[str, Any]], model: str) -> dict[str, str]:
    stamp = time.strftime("%Y%m%d-%H%M%S")
    source = f"{BUCKET}/{stamp}/input.jsonl"
    subprocess.run(["gcloud", "storage", "cp", "-", source, f"--project={PROJECT}", f"--account={ACCOUNT}"],
                   input="".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), text=True, check=True,
                   capture_output=True)
    job = api(API, {"displayName": f"multiple-choice-{stamp}", "model": f"publishers/google/models/{model}",
                    "inputConfig": {"instancesFormat": "jsonl", "gcsSource": {"uris": [source]}},
                    "outputConfig": {"predictionsFormat": "jsonl",
                                     "gcsDestination": {"outputUriPrefix": f"{BUCKET}/{stamp}/out"}}})
    job_id = job["name"].split("/")[-1]
    print(f"job {job_id} ({len(rows)} requests)", file=sys.stderr, flush=True)
    while job["state"] not in FINAL_STATES:
        time.sleep(60)
        job = api(f"{API}/{job_id}")
    print(f"state {job['state']} {job.get('completionStats', '')}", file=sys.stderr)
    texts = {}
    for path in gcloud("storage", "ls", "-r", f"{BUCKET}/{stamp}/out/").split():
        if path.endswith(".jsonl"):
            for line in gcloud("storage", "cat", path).splitlines():
                result = json.loads(line)
                try:
                    parts = result["response"]["candidates"][0]["content"]["parts"]
                except (KeyError, IndexError):
                    continue
                texts[result["key"]] = "".join(p.get("text", "") for p in parts if not p.get("thought"))
    return texts


def documents(fact: dict[str, Any], basic: dict[str, list[str]]) -> list[str]:
    """The fact's own documents plus those of the canon-basic rows it comes from (train/valid split, reserve)."""
    docs = [s for s in fact["source_ids"] if s.startswith("docs/")]
    for source in fact["source_ids"]:
        docs += [d for d in basic.get(source, []) if d not in docs]
    return docs


def valid_question(q: Any) -> bool:
    if not isinstance(q, dict) or not isinstance(q.get("question"), str) or not isinstance(q.get("correct"), str):
        return False
    distractors = q.get("distractors")
    if not isinstance(distractors, list) or len(distractors) != 3 or not all(isinstance(d, str) for d in distractors):
        return False
    options = [q["correct"].strip(), *(d.strip() for d in distractors)]
    lowered = {o.lower() for o in options}
    return all(options) and q["question"].strip() != "" and len(lowered) == 4 \
        and not any("anteriors" in o for o in lowered) and "segons el text" not in q["question"].lower()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gemini-3.8-flash")
    args = parser.parse_args()

    facts = read_jsonl(FACTS)
    basic = {r["id"]: r.get("documents", []) for r in read_jsonl(BASIC)}
    texts = run_batch(requests(facts, read_jsonl(GROUPS)), args.model)
    bench = bench_questions()
    rng = random.Random(SEED)
    today = datetime.date.today().isoformat()
    rows, dropped_bench, dropped_invalid = [], 0, 0
    for fact in facts:
        try:
            questions = json.loads(texts.get(fact["fact_id"], ""))["questions"]
        except (ValueError, KeyError, TypeError):
            questions = []
        for n, q in enumerate(questions[:2], 1):
            if not valid_question(q):
                dropped_invalid += 1
                continue
            if max(similarity(words(q["question"]), b) for b in bench) >= MAX_BENCH_SIMILARITY:
                dropped_bench += 1
                continue
            options = [q["correct"].strip(), *(d.strip() for d in q["distractors"])]
            rng.shuffle(options)
            letter = "ABCD"[options.index(q["correct"].strip())]
            listing = "\n".join(f"{k}) {o}" for k, o in zip("ABCD", options))
            rows.append({
                "id": f"canon-multiple-choice/{fact['fact_id']}/{n:02d}",
                "type": "test",
                "fact_id": fact["fact_id"],
                "messages": [
                    {"role": "system", "content": ""},
                    {"role": "user", "content": f"{q['question'].strip()}\n\n{listing}\n\n{INSTRUCTION}"},
                    {"role": "assistant", "content": letter},
                ],
                "documents": documents(fact, basic),
                "verificat": today,
            })
    OUT.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    letters = {k: sum(r["messages"][-1]["content"] == k for r in rows) for k in "ABCD"}
    print(f"{len(rows)} questions from {len(facts)} facts -> {OUT.relative_to(ROOT)}; "
          f"dropped: {dropped_invalid} invalid, {dropped_bench} close to maia-bench; letters {letters}")


if __name__ == "__main__":
    main()
