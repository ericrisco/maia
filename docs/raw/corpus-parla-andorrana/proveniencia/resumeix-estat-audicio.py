"""Resumeix l'estat d'audició per persona canònica i per cua."""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = PROV / "resum-estat-audicio.tsv"
MD = PROV / "resum-estat-audicio.md"


def read(name: str) -> list[dict[str, str]]:
    with (PROV / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def pending_count(rows: list[dict[str, str]]) -> int:
    return sum(row.get("estat_audicio", "pendent") in {"", "pendent", "pendent-audicio"} for row in rows)


def main() -> None:
    mapping = read("persones-canonics.tsv")
    master = read("registre-audicio.tsv")
    scarce = read("registre-audicio-formes-escasses.tsv") if (PROV / "registre-audicio-formes-escasses.tsv").exists() else []
    sample = read("cua-audicio-small-equilibrada.tsv")
    canonical = {row["id_persona"]: row["id_parlant"] for row in mapping}
    names = {row["id_parlant"]: row["nom_public"] for row in mapping}
    sources: defaultdict[str, set[str]] = defaultdict(set)
    for row in mapping:
        sources[row["id_parlant"]].add(row["id_persona"])
    grouped: defaultdict[str, list[dict[str, str]]] = defaultdict(list)
    grouped_general: defaultdict[str, list[dict[str, str]]] = defaultdict(list)
    grouped_scarce: defaultdict[str, list[dict[str, str]]] = defaultdict(list)
    for row in master:
        grouped[canonical[row["id_persona"]]].append(row)
        grouped_general[canonical[row["id_persona"]]].append(row)
    for row in scarce:
        grouped[canonical[row["id_persona"]]].append(row)
        grouped_scarce[canonical[row["id_persona"]]].append(row)

    fields = [
        "id_parlant", "nom_public", "n_registres_font", "n_intervals", "n_intervals_generals",
        "n_intervals_escasses", "pendent", "confirmada", "descartada", "incerta", "amb_nota",
        "amb_variant", "amb_fonetica", "amb_prosodia", "estat_global",
    ]
    output: list[dict[str, object]] = []
    for speaker in sorted(names):
        rows = grouped.get(speaker, [])
        stats = Counter(row.get("estat_audicio", "pendent") or "pendent" for row in rows)
        pending = stats["pendent"] + stats["pendent-audicio"]
        output.append(
            {
                "id_parlant": speaker,
                "nom_public": names[speaker],
                "n_registres_font": len(sources[speaker]),
                "n_intervals": len(rows),
                "n_intervals_generals": len(grouped_general.get(speaker, [])),
                "n_intervals_escasses": len(grouped_scarce.get(speaker, [])),
                "pendent": pending,
                "confirmada": stats["confirmada"],
                "descartada": stats["descartada"],
                "incerta": stats["incerta"],
                "amb_nota": sum(bool(row.get("nota_audicio", "").strip()) for row in rows),
                "amb_variant": sum(bool(row.get("variant_transcrita", "").strip()) for row in rows),
                "amb_fonetica": sum(bool(row.get("trets_fonetics_observats", "").strip()) for row in rows),
                "amb_prosodia": sum(bool(row.get("observacions_prosodiques", "").strip()) for row in rows),
                "estat_global": "pendent" if pending else "complet",
            }
        )

    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(output)

    total = Counter(row.get("estat_audicio", "pendent") or "pendent" for row in master)
    scarce_total = Counter(row.get("estat_audicio", "pendent") or "pendent" for row in scarce)
    sample_total = Counter(row.get("decisio_auditiva", "") or "pendent" for row in sample)
    lines = [
        "# Resum regenerable de l’estat d’audició",
        "",
        f"Registre mestre: **{len(master)} intervals** · pendent={pending_count(master)} · confirmada={total['confirmada']} · descartada={total['descartada']} · incerta={total['incerta']}.",
        f"Registre de formes escasses: **{len(scarce)} clips** · pendent={pending_count(scarce)} · confirmada={scarce_total['confirmada']} · descartada={scarce_total['descartada']} · incerta={scarce_total['incerta']}.",
        f"Total de cues: **{len(master) + len(scarce)} clips**.",
        f"Mostra equilibrada: **{len(sample)} clips** · pendent={sample_total['pendent']} · anotada={len(sample) - sample_total['pendent']}.",
        "",
        "La taula per persona canònica suma el registre general i la cua separada de formes escasses. Una persona només passa a `complet` quan no té intervals pendents; aquest estat no valida que la veu sigui dialectal, només que la cua s’ha escoltat.",
        "",
    ]
    for row in output:
        lines.append(f"- **{row['id_parlant']} · {row['nom_public']}** · {row['n_intervals']} intervals ({row['n_intervals_generals']} generals + {row['n_intervals_escasses']} escasses) · pendents {row['pendent']} · estat {row['estat_global']}")
    MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(output)} persones canòniques · general {len(master)} · escasses {len(scarce)} · pendents totals {pending_count(master) + pending_count(scarce)}")


if __name__ == "__main__":
    main()
