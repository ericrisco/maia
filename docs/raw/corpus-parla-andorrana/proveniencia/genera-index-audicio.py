"""Genera l'índex navegable de les cues d'audició del corpus."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = PROV / "INDEX-AUDICIO.md"


def read(name: str) -> list[dict[str, str]]:
    with (PROV / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    general = read("registre-audicio.tsv")
    scarce = read("registre-audicio-formes-escasses.tsv")
    summary = read("resum-estat-audicio.tsv")
    pending_sources = read("fonts-pendents.tsv")
    pending_permission = sum(row.get("estat") == "pendent-permis" for row in pending_sources)
    candidate_sources = sum(row.get("estat") == "preanalisi-candidat" for row in pending_sources)
    new_references = sum(row.get("estat") == "pendent-recollida" for row in pending_sources)
    sessions = [PROV / "sessions" / f"sessio-0{i}.tsv" for i in range(1, 7)]
    lines = [
        "# Índex d’audició del corpus de parla andorrana",
        "",
        "Aquesta és la porta d’entrada a la revisió humana. Les transcripcions, els descriptors acústics i les puntuacions ASR només prioritzen fragments; cap decisió lingüística entra al graf fins que s’escolta el WAV.",
        "",
        "## Ordre recomanat",
        "",
        f"1. [Resum per persona](resum-estat-audicio.md) — {len(summary)} persones canòniques i {len(general) + len(scarce)} clips totals.",
        f"2. [Sessions canòniques](auditoria-sessions-canoniques.html) — cua curta amb cobertura per persona; els manifests són {', '.join(p.name for p in sessions if p.exists())}.",
        f"3. [Formes escasses](auditoria-formes-escasses.html) — {len(scarce)} clips sobre 10 formes amb cobertura baixa.",
        "4. [Cua de quarantena](auditoria-quarantena-20s.html) — 15 clips de pa-044, pa-047 i pa-050.",
        f"5. [Cua completa](auditoria-cua.html) — {len(general)} intervals generals.",
        f"6. [Fonts pendents](fonts-pendents.tsv) — {pending_permission} pendents de permís, {candidate_sources} candidats preanalitzats i {new_references} referències noves per recollir; no formen part del recompte canònic.",
        "",
        "## Registres i guies",
        "",
        "- [Registre general](registre-audicio.tsv) — camps humans de decisió, variant, fonètica, prosòdia i nota.",
        "- [Registre de formes escasses](registre-audicio-formes-escasses.tsv) — separat del registre general.",
        "- [Guia de formes escasses](guia-audicio-formes-escasses.tsv) — criteris d’escolta per forma.",
        "- [Perfil acústic de formes escasses](analisi-acustica-formes-escasses.tsv) — descriptors instrumentals, sense anotació fonètica.",
        "- [Auditoria de cobertura de formes](auditoria-cobertura-formes.tsv) — les 35 formes candidates.",
        "- [Auditoria de cobertura per persona](auditoria-cobertura-sessions.tsv) — 60 persones canòniques.",
        "",
        "## Importació segura",
        "",
        "Les exportacions HTML es validen amb la clau exacta `(persona, forma, clip)`. Els importadors simulen per defecte i només escriuen amb `--write`:",
        "",
        "- `python3 importa-auditoria.py anotacions.tsv` per al registre general.",
        "- `python3 importa-auditoria-formes-escasses.py anotacions-formes-escasses.tsv` per a la cua separada.",
        "",
        "Les files continuen `pendent` fins que hi ha una decisió humana. Les veus en quarantena no entren al graf per aquesta via.",
        "",
        "## Verificació",
        "",
        "- `python3 verifica-corpus.py` comprova fitxers, hashes, independència, informes i registres.",
        "- `python3 verifica-sessions-audicio.py` comprova els manifests i evita solapaments.",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generat {OUT} amb {len(lines)} línies")


if __name__ == "__main__":
    main()
