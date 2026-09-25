"""Aplica el repertori de referència com a checklist prudent per parlant."""

from pathlib import Path
import csv

ROOT = Path(__file__).parents[1]


def read(path: Path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    people = read(ROOT / "persones.tsv")
    traits = read(ROOT / "grafo" / "repertori-referencia.tsv")
    linguistic = {r["id_persona"]: r for r in read(ROOT / "proveniencia" / "analisi-linguistica.tsv")}
    acoustic = {r["id_persona"]: r for r in read(ROOT / "proveniencia" / "analisi-acustica-densa.tsv")}
    context = {r["id_persona"]: r for r in read(ROOT / "proveniencia" / "context-persones.tsv")}
    rows = []
    for person in people:
        pid = person["id_persona"]
        ling = linguistic[pid]
        ac = acoustic[pid]
        for trait in traits:
            candidate = trait["candidat"]
            category = trait["categoria"]
            if candidate == "perífrasis i règim verbal":
                indicator = f"perifrasi_past_aparent={ling['perifrasi_past_aparent']} (ASR)"
                state = "indicador textual; validar àudio"
            elif candidate == "marcadors i reformulacions":
                indicator = ling["marcadors"]
                state = "indicador textual; validar àudio"
            elif category == "lèxic":
                indicator = f"formes_territorials={ling['formes_territorials']} (ASR)"
                state = "candidat lèxic; validar àudio"
            elif candidate == "entonació, ritme i pauses":
                indicator = (
                    f"f0_iqr_hz={ac['f0_iqr_hz']}; f0_sd_hz={ac['f0_sd_hz']}; "
                    f"pausa_mediana_s={ac['pausa_veu_mediana_s']}"
                )
                state = "descriptor acústic; no és tret confirmat"
            elif candidate == "localitat i generació":
                c = context.get(pid)
                indicator = c["parroquia_o_ambit"] if c else "context no documentat"
                state = "contextual; no prova varietat"
            elif category in {"vocalisme", "fonètica", "fonosintaxi"}:
                indicator = "no inferible de la grafia ASR"
                state = "requereix escolta"
            elif candidate == "contacte amb castellà i francès":
                indicator = "no inferible sense biografia i àudio"
                state = "requereix escolta i context"
            else:
                indicator = "pendent de revisió manual"
                state = "requereix escolta"
            rows.append({
                "id_persona": pid,
                "categoria": category,
                "candidat": candidate,
                "referencia": trait["evidencia_referencia"],
                "indicador_automatic": indicator,
                "estat_indicador": state,
                "observacio_auditiva": "",
            })
    output = ROOT / "grafo" / "repertori-aplicat.tsv"
    fields = list(rows[0])
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} files · {output}")


if __name__ == "__main__":
    main()
