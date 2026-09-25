"""Documenta les coincidències per subcadena descartades pel límit de paraula."""

from pathlib import Path
import csv

PROV = Path(__file__).parent
OUT = PROV / "informe-falsos-positius-boundary.md"


def main() -> None:
    with (PROV / "qa-clips-boundary.tsv").open(encoding="utf-8", newline="") as handle:
        rows = [row for row in csv.DictReader(handle, delimiter="\t") if row["small_subcadena"] == "sí" and row["base_subcadena"] == "sí" and row["consens_limit_paraula"] == "no"]
    lines = [
        "# Falsos positius per coincidència de subcadena",
        "",
        f"La comparació inicial trobava 263 consensos buscant la forma com a subcadena. "
        f"Amb límits alfanumèrics estrictes, **{len(rows)}** deixen de ser consensos: la forma apareix "
        "dins d'una paraula més gran o només en un dels dos textos. Aquests clips no es descarten "
        "de l'audició, però ja no entren al graf estricte de paraula.",
        "",
    ]
    for row in rows:
        lines.extend([
            f"## {row['id_persona']} — {row['forma']} — {row['interval_escolta']}",
            "",
            f"- Àudio: [`{row['clip']}`]({row['clip']})",
            f"- Text small: {row['text_small']}",
            f"- Text base: {row['text_base']}",
            "- Diagnòstic: coincidència de subcadena, no coincidència de paraula completa en ambdós textos.",
            "- Decisió auditiva: `pendent`",
            "",
        ])
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"{len(rows)} falsos positius documentats a {OUT}")


if __name__ == "__main__":
    main()
