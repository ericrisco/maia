"""Genera un índex navegable de les 66 fitxes individuals del corpus."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).parents[1]
OUT = ROOT / "persones" / "INDEX.md"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def cell(value: str) -> str:
    return (value or "").replace("|", "\\|").replace("\n", " ").strip()


def main() -> None:
    rows = read(ROOT / "persones.tsv")
    canonical = read(ROOT / "proveniencia" / "persones-canonics.tsv")
    canonical_by_source = {row["id_persona"]: row for row in canonical}
    lines = [
        "# Índex de persones del corpus de parla andorrana",
        "",
        f"Aquest índex recull **{len(rows)} registres de font** que corresponen a **{len({row['id_parlant'] for row in canonical})} persones canòniques**. Cada fila enllaça amb l'informe individual, l'àudio local i la font pública; les anàlisis continuen provisionals fins a l'audició.",
        "",
        "| id | persona | font | estat | durada | informe | font pública |",
        "|---|---|---|---|---:|---|---|",
    ]
    for row in rows:
        canonical_row = canonical_by_source.get(row["id_persona"], {})
        report = f"[{row['id_persona']}]({row['id_persona']}.md)"
        source = f"[{cell(row['tipus_font'])}]({row['url']})" if row.get("url") else "—"
        canonical_id = canonical_row.get("id_parlant", "")
        person = cell(row["nom_public"])
        if canonical_id and canonical_id != row["id_persona"]:
            person = f"{person} (`{canonical_id}`)"
        lines.append(f"| `{row['id_persona']}` | {person} | {cell(row['font_principal'])} | `{cell(row['estat'])}` | {cell(row['audio_s'])} | {report} | {source} |")
    lines += [
        "",
        "Les fonts en preanàlisi i els seus clips no entren en aquest índex canònic; es mantenen a [candidats fora del cànon](../proveniencia/candidats/README.md) i a la seva [auditoria separada](../proveniencia/auditoria-candidats.md).",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"{len(rows)} fitxes indexades · {len({row['id_parlant'] for row in canonical})} persones canòniques")


if __name__ == "__main__":
    main()
