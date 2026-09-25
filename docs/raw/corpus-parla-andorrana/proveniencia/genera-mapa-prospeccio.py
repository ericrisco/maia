"""Genera un mapa legible de fonts canòniques, candidats i permisos pendents."""
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = PROV / "mapa-prospeccio.md"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    sources = read(PROV / "fonts-resum.tsv")
    pending = read(PROV / "fonts-pendents.tsv")
    candidates = read(PROV / "auditoria-candidats.tsv")
    channels = Counter(row["canal"] for row in sources)
    states = Counter(row["estat"] for row in pending)
    permission = [row for row in pending if row["estat"] == "pendent-permis"]
    lines = [
        "# Mapa de prospecció del corpus de parla andorrana",
        "",
        f"El mapa conserva **{len(sources)} fonts canòniques** ({len({row['canal'] for row in sources})} canals), **{len(candidates)} candidats preanalitzats** fora del cànon i **{len(permission)} referències** que no es poden descarregar fins a confirmar el permís.",
        "",
        "## Fonts canòniques",
        "",
        "| canal | registres |",
        "|---|---:|",
    ]
    for channel, count in sorted(channels.items()):
        lines.append(f"| {channel} | {count} |")
    lines.extend([
        "",
        "## Candidats separats",
        "",
        "| candidat | clips | estat | veu | termes |",
        "|---|---:|---|---|---|",
    ])
    for row in candidates:
        lines.append(f"| `{row['id_candidat']}` | {row['n_clips']} | {row['estat']} | {row['veu_confirmada']} | {row['termes_confirmats']} |")
    lines.extend([
        "",
        "## Referències bloquejades per permís",
        "",
        "| referència | font | criteri | termes | motiu |",
        "|---|---|---|---|---|",
    ])
    for row in permission:
        lines.append(f"| `{row['id_persona_provisional']}` · {row['nom_public']} | {row['font']} | {row['criteri_parla']} | {row['llicencia_termes']} | {row['nota']} |")
    lines.extend([
        "",
        f"`fonts-pendents.tsv` conserva també {states.get('incorporat-pa-051', 0) + states.get('incorporat-pa-052', 0) + states.get('incorporat-pa-053', 0) + states.get('incorporat-pa-054', 0)} registres que ja es van incorporar a pa-051—pa-054 i no són noves fonts obertes.",
        "",
        "Criteri operatiu: no s'afegeix cap veu al cànon sense audio local, transcripció, procedència i termes d'ús explícits. Els candidats continuen fora del graf canònic fins a l'audició.",
    ])
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(sources)} fonts · {len(candidates)} candidats · {len(permission)} permisos pendents · {OUT}")


if __name__ == "__main__":
    main()
