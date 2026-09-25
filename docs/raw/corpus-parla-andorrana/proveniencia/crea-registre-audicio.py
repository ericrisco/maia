"""Consolida la cua de revisió amb evidència ASR, acústica i camps humans."""

from pathlib import Path
import csv

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"


def read(rel: str):
    with (PROV / rel).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    priority = read("prioritat-audicio.tsv")
    qa = {(r["id_persona"], r["forma"]): r for r in read("qa-clips.tsv")}
    acoustic = {(r["id_persona"], r["forma"]): r for r in read("analisi-acustica-clips.tsv")}
    json_qa = {(r["id_persona"], r["forma"]): r for r in read("qa-clips-json.tsv")} if (PROV / "qa-clips-json.tsv").exists() else {}
    token_rows = read("qa-formes-tokens.tsv") if (PROV / "qa-formes-tokens.tsv").exists() else []
    tokens = {}
    for r in token_rows:
        tokens.setdefault((r["id_persona"], r["forma"]), []).append(r)
    rows = []
    for order, p in enumerate(priority, start=1):
        key = (p["id_persona"], p["forma"])
        q = qa[key]
        a = acoustic[key]
        tok = tokens.get(key, [])
        tok_yes = [r for r in tok if r["coincidencia_token"] == "sí"]
        rows.append({
            "ordre": str(order),
            "categoria": p["categoria"],
            "score_evidencia": p["score_evidencia"],
            "id_persona": p["id_persona"],
            "forma": p["forma"],
            "interval_escolta": p["interval_escolta"],
            "clip": p["clip"],
            "transcripcio_qa": q["transcripcio_qa"],
            "json_qa": json_qa.get(key, {}).get("json", ""),
            "token_coincidencia": "sí" if tok_yes else ("no" if tok else ""),
            "token_intervals_absolute": ";".join(f"{r['absolute_start_s']}-{r['absolute_end_s']}" for r in tok_yes),
            "token_prob_min": ";".join(r["prob_min"] for r in tok_yes),
            "token_prob_mean": ";".join(r["prob_mean"] for r in tok_yes),
            "token_text": ";".join(r["tokens"] for r in tok_yes),
            "text_qa": q["text_qa"],
            "consens_dos_asr": p["consens_dos_asr"],
            "coincidencia_temporal_asr": p["coincidencia_temporal_asr"],
            "forma_en_qa": p["forma_en_qa"],
            "conf_min_segment": p["conf_min_segment"],
            "conf_min_base_segment": p["conf_min_base_segment"],
            "veu_proporcio": a["veu_proporcio"],
            "rms_p50_db": a["rms_p50_db"],
            "f0_median_hz": a["f0_median_hz"],
            "f0_iqr_hz": a["f0_iqr_hz"],
            "centroid_median_hz": a["centroid_median_hz"],
            "pausa_mediana_s": a["pausa_mediana_s"],
            "estat_audicio": "pendent",
            "forma_confirmada_auditivament": "",
            "variant_transcrita": "",
            "trets_fonetics_observats": "",
            "observacions_prosodiques": "",
            "nota_audicio": "",
        })
    output = PROV / "registre-audicio.tsv"
    fields = list(rows[0])
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} files · {output}")


if __name__ == "__main__":
    main()
