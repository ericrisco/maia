"""Genera una sessió d'audició per al candidat RTVA Joan Micó."""
from __future__ import annotations
import csv
from pathlib import Path
ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
CAND = PROV / "candidats" / "lead-rtva-004-joan-mico"

def read(path):
    with path.open(encoding="utf-8", newline="") as h:
        return list(csv.DictReader(h, delimiter="\t"))

def main():
    manifest = read(CAND / "formes-clips.tsv")
    greedy = {r["clip"]: r for r in read(CAND / "qa-greedy.tsv")}
    rows=[]
    for i, item in enumerate(manifest, 1):
        g=greedy.get(item["clip"], {})
        rows.append({
            "ordre_sessio": str(i),
            "id_global": f"candidate::lead-rtva-004-joan-mico::{item['forma']}::{i}",
            "origen": "Joan Micó (candidat RTVA)",
            "persona": "lead-rtva-004-joan-mico",
            "forma": item["forma"],
            "clip": f"candidats/lead-rtva-004-joan-mico/{item['clip']}",
            "prioritat": item.get("prioritat", "candidat-ASR"),
            "prob_min": "",
            "text": g.get("text_greedy", ""),
            "motiu": "candidat nou: confirmar veu de Joan Micó i forma abans de qualsevol incorporació",
            "estat": "pendent",
        })
    fields=list(rows[0])
    with (PROV / "sessions" / "sessio-03.tsv").open("w", encoding="utf-8", newline="") as h:
        w=csv.DictWriter(h, fieldnames=fields, delimiter="\t", lineterminator="\n"); w.writeheader(); w.writerows(rows)
    lines=["# Sessió d'audició 03 — Joan Micó", "", "Aquesta sessió conté **12 clips** del candidat RTVA Joan Micó. Cal confirmar primer qui parla i després la forma, la variant, els trets fonètics i la prosòdia; cap fila entra al registre canònic.", "", "| ordre | forma | prioritat | clip |", "|---:|---|---|---|"]
    lines += [f"| {r['ordre_sessio']} | **{r['forma']}** | {r['prioritat']} | `{r['clip']}` |" for r in rows]
    lines += ["", "La sessió es pot obrir amb `../auditoria-global.html`; les anotacions exportades es conserven separades fins a una decisió explícita."]
    (PROV / "sessions" / "sessio-03.md").write_text("\n".join(lines)+"\n", encoding="utf-8")
    print(f"{len(rows)} clips")
if __name__ == "__main__": main()
