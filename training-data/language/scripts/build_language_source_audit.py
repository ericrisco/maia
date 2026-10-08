#!/usr/bin/env python3
"""Build a source, rights and transcript status report for Maia Language."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CORPUS = ROOT / "docs" / "raw" / "corpus-parla-andorrana" / "proveniencia"
SOURCES = CORPUS / "auditoria-proveniencia.tsv"
TRANSCRIPTS = CORPUS / "auditoria-integritat-transcripcions.tsv"
IDENTITIES = CORPUS / "auditoria-identitat-linguistica.tsv"
REPORT = ROOT / "training-data" / "language" / "reports" / "source-audit.md"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as source:
        return list(csv.DictReader(source, delimiter="\t"))


def build_report() -> str:
    sources = read_tsv(SOURCES)
    transcripts = read_tsv(TRANSCRIPTS)
    identities = read_tsv(IDENTITIES)
    source_ids = {row["id_persona"] for row in sources}
    transcript_ids = {row["id_persona"] for row in transcripts}
    if source_ids != transcript_ids:
        raise ValueError("Source and transcript audits do not contain the same speaker records")

    license_group = Counter()
    for row in sources:
        license_text = row["llicencia"].lower()
        if "creative commons attribution" in license_text:
            group = "CC BY declarada"
        elif "només per ús educatiu" in license_text:
            group = "Ús educatiu declarat; sense difusió"
        else:
            group = "Llicència estàndard de YouTube; sense llicència oberta declarada"
        license_group[group] += 1

    transcript_status = Counter(row["estat"] for row in transcripts)
    identity_status = Counter(row["estat"] for row in identities)
    unresolved_identity = sum(
        1 for row in identities if "pendent" in (row["estat"] + " " + row["accio"]).lower()
    )

    rows = [
        "# Auditoria de fonts de Maia Language",
        "",
        "Informe regenerable a partir de les auditories de procedència, integritat de transcripcions i identitat lingüística del subcorpus de parla.",
        "",
        f"- Registres de font: **{len(sources)}**.",
        f"- Registres de transcripció comparats amb la procedència: **{len(transcripts)}**.",
        f"- Persones canòniques amb revisió d'identitat lingüística pendent: **{unresolved_identity}/{len(identities)}**.",
        "",
        "## Termes d'ús declarats per font",
        "",
        "| Estat de llicència registrat | Registres |",
        "| --- | ---: |",
    ]
    for label in (
        "CC BY declarada",
        "Llicència estàndard de YouTube; sense llicència oberta declarada",
        "Ús educatiu declarat; sense difusió",
    ):
        rows.append(f"| {label} | {license_group[label]} |")

    rows.extend(
        [
            "",
            "## Revisió pendent abans d'exportar",
            "",
            f"- **{license_group['CC BY declarada']} mostres amb CC BY declarada** són candidates de revisió. Cal conservar atribució i comprovar per cada font que la llicència registrada cobreix l'ús previst, així com completar la revisió auditiva i contextual abans d'aprovar una transcripció.",
            f"- **{license_group['Llicència estàndard de YouTube; sense llicència oberta declarada']} mostres** no tenen una llicència oberta declarada al registre. No s'inclouen en un export sense autorització o termes de reutilització verificats.",
            f"- **{license_group['Ús educatiu declarat; sense difusió']} mostres** tenen termes d'ús educatiu i de recerca sense difusió. Queden excloses d'un export amb els termes actuals.",
            f"- La integritat estructural de les transcripcions: **{transcript_status.get('complet', 0)} completes**, **{transcript_status.get('pendent', 0)} amb incidències**. «Completa» descriu timestamps i estructura, no una transcripció escoltada ni validada.",
            f"- **{unresolved_identity}/{len(identities)} perfils** encara tenen pendent confirmar lloc de socialització, llengües d'ús i veu a l'àudio.",
            "- Les transcripcions són sortides ASR. No s'aprova cap text només perquè coincideixi entre models o tingui timestamps vàlids; cal escoltar el fragment i corregir el text sense normalitzar-ne la parla.",
            "",
            "## Font d'aquests recomptes",
            "",
            "- `docs/raw/corpus-parla-andorrana/proveniencia/auditoria-proveniencia.tsv`.",
            "- `docs/raw/corpus-parla-andorrana/proveniencia/auditoria-integritat-transcripcions.tsv`.",
            "- `docs/raw/corpus-parla-andorrana/proveniencia/auditoria-identitat-linguistica.tsv`.",
            "- Els recomptes expressen l'estat documentat en aquests fitxers; no equivalen a aprovació per entrenar.",
            "",
        ]
    )
    return "\n".join(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if the checked-in report is stale")
    args = parser.parse_args()
    report = build_report()
    if args.check:
        if not REPORT.exists() or REPORT.read_text(encoding="utf-8") != report:
            print("language source audit is missing or stale; run this script without --check")
            return 1
        print("language source audit is current")
        return 0
    REPORT.write_text(report, encoding="utf-8")
    print(f"wrote {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
