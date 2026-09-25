"""Compara una segona passada ASR sobre la cua curta de quarantena."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
QUEUE = PROV / "cua-audicio-quarantena-20s.tsv"
OUT_DIR = PROV / "qa-quarantena-20s-small"
OUT = PROV / "qa-quarantena-20s-consens.tsv"
MODEL = Path("/Users/ericrisco/.codex/local-maia-models/ggml-small.bin")
REPORT_MARKER = "### Comparació ASR de la cua curta"


def normalize(text: str) -> str:
    return " ".join(text.lower().split())


def jaccard_tokens(left: str, right: str) -> float:
    a = set(normalize(left).split())
    b = set(normalize(right).split())
    return len(a & b) / len(a | b) if a or b else 1.0


def main() -> None:
    with QUEUE.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    OUT_DIR.mkdir(exist_ok=True)
    result_rows: list[dict[str, str]] = []
    for row in rows:
        clip = PROV / row["clip"]
        stem = clip.stem
        prefix = OUT_DIR / stem
        txt = prefix.with_suffix(".txt")
        vtt = prefix.with_suffix(".vtt")
        js = prefix.with_suffix(".json")
        if not txt.exists() or not vtt.exists() or not js.exists():
            subprocess.run(
                ["whisper-cli", "-m", str(MODEL), "-l", "ca", "-t", "8", "-mc", "0", "-bs", "5", "-bo", "5", "-nf", "-sow", "-otxt", "-ovtt", "-oj", "-of", str(prefix), str(clip)],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        base = row["text_qa"]
        small = txt.read_text(encoding="utf-8", errors="replace").strip().replace("\n", " ")
        result_rows.append({
            "ordre": row["ordre"],
            "id_persona": row["id_persona"],
            "inici_s": row["inici_s"],
            "clip": row["clip"],
            "transcripcio_base": row["transcripcio"],
            "transcripcio_small": f"qa-quarantena-20s-small/{txt.name}",
            "sha256": hashlib.sha256(clip.read_bytes()).hexdigest(),
            "text_base": base,
            "text_small": small,
            "consens_textual": "sí" if normalize(base) == normalize(small) else "no",
            "jaccard_tokens": f"{jaccard_tokens(base, small):.4f}",
            "estat_audicio": row["estat_audicio"],
        })
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result_rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(result_rows)
    for person in sorted({row["id_persona"] for row in result_rows}):
        report = ROOT / "persones" / f"{person}.md"
        text = report.read_text(encoding="utf-8")
        if REPORT_MARKER in text:
            text = text[: text.index(REPORT_MARKER)].rstrip() + "\n"
        items = [row for row in result_rows if row["id_persona"] == person]
        lines = [REPORT_MARKER, "", "La passada `ggml-small.bin` es conserva separada de la passada base. La coincidència exacta és estricta; el Jaccard només orienta la prioritat i no substitueix l’escolta.", "", "| inici | coincidència exacta | Jaccard de tokens |", "|---:|---|---:|"]
        lines.extend(f"| {row['inici_s']} s | {row['consens_textual']} | {row['jaccard_tokens']} |" for row in items)
        report.write_text(text.rstrip() + "\n\n" + "\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(result_rows)} clips · consens={sum(r['consens_textual']=='sí' for r in result_rows)} · {OUT}")


if __name__ == "__main__":
    main()
