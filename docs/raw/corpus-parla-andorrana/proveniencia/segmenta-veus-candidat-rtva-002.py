"""Ordena provisionalment els torns d'Ian Moya i l'entrevistador."""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).parents[1]
CAND = ROOT / "proveniencia" / "candidats" / "lead-rtva-002-ian-moya"
JSON = CAND / "asr" / "ian-moya.json"


def seconds(value: str) -> float:
    h, m, s = value.replace(",", ".").split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


QUESTION_START = re.compile(r"^(què|com|quan|quina|quin|per què|perquè|on|parla|explica|creus|t'agrada|quin)\b", re.I)
FIRST_PERSON = re.compile(r"\b(jo|em|meu|meva|meus|meves|crec|penso|m'agrada|he|soc|sóc|vaig)\b", re.I)


def classify(text: str) -> tuple[str, str, str]:
    words = re.findall(r"[^\W_]+(?:['’][^\W_]+)?", text, re.UNICODE)
    question = "?" in text or bool(QUESTION_START.search(text.strip()))
    first = bool(FIRST_PERSON.search(text))
    if question and first and len(words) >= 14:
        return "mixt-indeterminat", "baixa", "pregunta i resposta possible dins el mateix segment"
    if question and len(words) <= 32:
        return "entrevistador-probable", "mitjana", "marcador interrogatiu o inici de pregunta"
    if first and len(words) >= 8:
        return "ian-probable", "baixa", "primera persona i resposta desenvolupada"
    if len(words) >= 18:
        return "ian-probable", "baixa", "segment llarg compatible amb resposta"
    return "indeterminat", "baixa", "no hi ha senyal textual suficient"


def main() -> None:
    data = json.loads(JSON.read_text(encoding="utf-8"))
    rows = []
    for number, segment in enumerate(data.get("transcription", []), start=1):
        text = segment.get("text", "").strip()
        if not text or text == "#":
            continue
        role, confidence, reason = classify(text)
        rows.append({
            "segment": number,
            "inici_s": f"{seconds(segment['timestamps']['from']):.3f}",
            "final_s": f"{seconds(segment['timestamps']['to']):.3f}",
            "rol_provisional": role,
            "confiança": confidence,
            "motiu": reason,
            "text_asr": text,
            "estat": "heurística textual; pendent d'audició",
        })
    out = CAND / "segments-speaker-provisional.tsv"
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)
    counts = {}
    for row in rows:
        counts[row["rol_provisional"]] = counts.get(row["rol_provisional"], 0) + 1
    forms = []
    seen = set()
    with (ROOT / "grafo" / "matriu-formes.tsv").open(encoding="utf-8", newline="") as handle:
        for form_row in csv.DictReader(handle, delimiter="\t"):
            key = (form_row["categoria"], form_row["forma"])
            if key not in seen:
                forms.append(key)
                seen.add(key)
    form_rows = []
    form_counts = Counter()
    for row in rows:
        if row["rol_provisional"] != "ian-probable":
            continue
        for category, form in forms:
            if re.search(rf"(?<![\wà-ÿ]){re.escape(form)}(?![\wà-ÿ])", row["text_asr"], re.I):
                form_counts[form] += 1
                form_rows.append({"categoria": category, "forma": form, "segment": row["segment"], "inici_s": row["inici_s"], "final_s": row["final_s"], "text_asr": row["text_asr"], "estat": "rol Ian provisional; pendent d'audició"})
    with (CAND / "formes-ian-provisional.tsv").open("w", encoding="utf-8", newline="") as handle:
        fields = ["categoria", "forma", "segment", "inici_s", "final_s", "text_asr", "estat"]
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(form_rows)
    (CAND / "segmentacio-veus.md").write_text(
        """# Segmentació provisional de veus — Ian Moya

Aquesta taula ordena la revisió amb senyals textuals de preguntes, primera persona i longitud de segment. No és diarització: la veu real s'ha de confirmar escoltant l'àudio.

| rol provisional | segments |
|---|---:|
""" + "\n".join(f"| {role} | {count} |" for role, count in sorted(counts.items())) + f"\n\nLa columna `motiu` conserva la raó de cada hipòtesi i les etiquetes no modifiquen el recompte canònic. La hipòtesi `ian-probable` conté **{len(form_rows)} ocurrències** en **{len(form_counts)} formes**; el detall és a `formes-ian-provisional.tsv`.\n", encoding="utf-8")
    print(" · ".join(f"{role}={count}" for role, count in sorted(counts.items())))


if __name__ == "__main__":
    main()
