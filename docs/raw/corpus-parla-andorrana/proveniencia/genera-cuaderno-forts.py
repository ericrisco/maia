"""Genera un cuaderno Markdown navegable per revisar els candidats forts."""

from pathlib import Path
import csv

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"


def read(rel):
    with (PROV / rel).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def link(rel: str, label: str) -> str:
    return f"[{label}](<{rel}>)"


def main() -> None:
    candidates = read("candidats-forts.tsv")
    qa = {(r["id_persona"], r["forma"]): r for r in read("qa-clips.tsv")}
    acoustic = {(r["id_persona"], r["forma"]): r for r in read("analisi-acustica-clips.tsv")}
    tokens = {}
    for row in read("qa-formes-tokens.tsv"):
        tokens.setdefault((row["id_persona"], row["forma"]), []).append(row)
    by_person = {}
    for row in candidates:
        by_person.setdefault(row["id_persona"], []).append(row)
    lines = [
        "# Quadern d'audició — candidats forts",
        "",
        "Aquest quadern ordena 109 clips amb triple consens ASR i probabilitat",
        "tokenitzada mínima de 0,80. Els camps d'observació són humans i continuen",
        "pendents; cap entrada és un tret dialectal confirmat.",
        "",
        "## Criteri",
        "",
        "Escoltar el WAV, comprovar la forma, anotar la variant real, vocalisme,",
        "consonants, accent, pauses i contacte lingüístic. Si el fragment no és",
        "audible o la forma no coincideix, registrar-ho i no forçar cap etiqueta.",
        "",
    ]
    for person in sorted(by_person):
        lines.extend([f"## {person}", ""])
        for row in by_person[person]:
            key = (person, row["forma"])
            q = qa[key]
            a = acoustic[key]
            tok = tokens.get(key, [])
            token_line = "; ".join(
                f"{t['absolute_start_s']}–{t['absolute_end_s']} s, pmin={t['prob_min']}"
                for t in tok if t["coincidencia_token"] == "sí"
            ) or "sense coincidència tokenitzada"
            clip_link = link("clips/" + Path(row["clip"]).name, "WAV")
            txt_link = link(q["transcripcio_qa"], "text QA")
            lines.extend([
                f"### {row['forma']}",
                "",
                f"- Clip: {clip_link} · {txt_link}",
                f"- Interval: `{row['interval_escolta']}` · tokens: `{token_line}`",
                f"- Text QA: {q['text_qa']}",
                f"- Veu: `{a['veu_proporcio']}` · F0 mediana: `{a['f0_median_hz']} Hz` · IQR F0: `{a['f0_iqr_hz']} Hz` · pausa mediana: `{a['pausa_mediana_s']} s`",
                "- **Confirmació auditiva:** pendent · **variant:** · **trets fonètics:** · **prosòdia:**",
                "",
            ])
    output = PROV / "quadern-audicio-forts.md"
    output.write_text("\n".join(lines), encoding="utf-8")
    print(f"{len(candidates)} clips · {len(by_person)} persones · {output}")


if __name__ == "__main__":
    main()
