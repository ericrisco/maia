"""Ordena la cua mestra incorporant el consens de tres descodificacions."""
from collections import defaultdict
from pathlib import Path
import csv

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = PROV / "prioritat-audicio-triple.tsv"
MD = PROV / "quadern-audicio-triple-complet.md"


def read(name):
    with (PROV / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def number(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return -1.0


def main():
    master = read("registre-audicio.tsv")
    triple = {(row["id_persona"], row["forma"]): row for row in read("qa-clips-triple-full.tsv")}
    ranked = []
    for source in master:
        row = triple[(source["id_persona"], source["forma"])]
        probability = number(source.get("token_prob_min", ""))
        category = row["categoria"]
        if category == "A-tres-models" and probability >= 0.8:
            rank, priority, reason = 1, "A-triple-token-fort", "tres models i probabilitat de token >= 0,80"
        elif category == "A-tres-models":
            rank, priority, reason = 2, "B-triple-token-baix", "tres models amb probabilitat baixa"
        elif category == "B-dos-models":
            rank, priority, reason = 3, "C-dos-models", "dos models; requereix contrast auditiu"
        elif category == "C-un-model":
            rank, priority, reason = 4, "D-un-model", "un model; requereix contrast auditiu"
        else:
            rank, priority, reason = 5, "E-cap-model", "cap model; requereix escolta prioritària"
        output = dict(source)
        output.update({
            "rang": rank,
            "prioritat_triple": priority,
            "small": row["small"],
            "base": row["base"],
            "greedy": row["greedy"],
            "text_greedy": row["text_greedy"],
            "justificacio": reason,
        })
        ranked.append(output)
    ranked.sort(key=lambda row: (int(row["rang"]), -number(row.get("token_prob_min", "")), row["id_persona"], row["forma"]))
    for order, row in enumerate(ranked, 1):
        row["ordre_triple"] = order
    fields = ["ordre_triple", "rang", "prioritat_triple", "id_persona", "forma", "interval_escolta", "clip", "token_prob_min", "small", "base", "greedy", "forma_en_qa", "consens_dos_asr", "text_qa", "text_greedy", "justificacio", "estat_audicio", "forma_confirmada_auditivament", "variant_transcrita", "trets_fonetics_observats", "observacions_prosodiques", "nota_audicio"]
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(ranked)
    groups = defaultdict(list)
    for row in ranked:
        groups[row["prioritat_triple"]].append(row)
    lines = ["# Quadern d’audició de la cua completa — prioritat triple", "", "Ordre de revisió dels 656 clips segons small/base/greedy i la probabilitat del token. Les prioritats són automàtiques i no confirmen cap forma.", ""]
    for priority in ("A-triple-token-fort", "B-triple-token-baix", "C-dos-models", "D-un-model", "E-cap-model"):
        lines += [f"## {priority}", ""]
        for row in groups[priority]:
            lines.append(f"- **{row['id_persona']} · {row['forma']}** · `{row['clip']}` · p={row.get('token_prob_min') or '—'} · small/base/greedy={row['small']}/{row['base']}/{row['greedy']} · text: `{row['text_greedy']}`")
        lines.append("")
    lines += ["## Anotació", "", "Completar `registre-audicio.tsv` amb decisió, variant, fonètica, prosòdia i nota segons `protocol-audicio-anotacio.md`."]
    MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    from collections import Counter
    print(len(ranked), Counter(row["prioritat_triple"] for row in ranked))


if __name__ == "__main__":
    main()
