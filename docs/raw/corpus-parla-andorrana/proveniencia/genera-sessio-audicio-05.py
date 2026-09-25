"""Genera la cinquena sessió d'audició canònica.

Selecciona vint clips d'alta prioritat que encara no apareixen a les sessions
01 i 02. Els camps humans es mantenen buits.
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
SESSIONS = PROV / "sessions"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    used = {
        row["clip"]
        for session in (SESSIONS / "sessio-01.tsv", SESSIONS / "sessio-02.tsv")
        for row in read(session)
    }
    acoustic = {row["clip"]: row for row in read(PROV / "analisi-acustica-clips.tsv")}
    formants = {
        (row["id_persona"], row["forma"], row["clip"]): row
        for row in read(PROV / "analisi-formants-qa.tsv")
    }
    selected: list[dict[str, str]] = []
    for candidate in read(PROV / "prioritat-audicio-triple.tsv"):
        if candidate["clip"] in used or len(selected) >= 20:
            continue
        if not candidate["id_persona"].startswith("pa-"):
            continue
        signal = acoustic.get(candidate["clip"], {})
        token = formants.get((candidate["id_persona"], candidate["forma"], candidate["clip"]), {})
        ordinal = len(selected) + 1
        selected.append(
            {
                "ordre_sessio": str(ordinal),
                "id_global": f"canon::{candidate['id_persona']}::{candidate['forma']}::s05-{ordinal}",
                "origen": "canònic",
                "persona": candidate["id_persona"],
                "forma": candidate["forma"],
                "clip": candidate["clip"],
                "prioritat": candidate["prioritat_triple"],
                "prob_min": candidate["token_prob_min"],
                "text": candidate["text_greedy"],
                "motiu": "sessió 05: clip canònic d'alta prioritat fora de les sessions 01–02",
                "estat": "pendent",
                "text_small": candidate["small"],
                "text_base": candidate["base"],
                "rol_provisional": "",
                "motiu_rol": "segment canònic; el rol es confirma amb l'audició",
                "f0_median_hz": signal.get("f0_median_hz", ""),
                "f0_iqr_hz": signal.get("f0_iqr_hz", ""),
                "pausa_mediana_s": signal.get("pausa_mediana_s", ""),
                "f1_hz": token.get("f1_hz", ""),
                "f2_hz": token.get("f2_hz", ""),
                "f3_hz": token.get("f3_hz", ""),
                "estat_instrumental": "suport automàtic; pendent d'audició",
            }
        )
    if len(selected) != 20:
        raise SystemExit(f"només s'han seleccionat {len(selected)} clips")
    write_tsv(SESSIONS / "sessio-05.tsv", selected)
    lines = [
        "# Sessió d'audició 05 — clips canònics prioritaris",
        "",
        "Aquesta sessió conté **20 clips canònics** d'alta prioritat que no apareixen a les sessions 01–02. Els textos i les mètriques són suport automàtic; les decisions de veu, forma, variant, fonètica i prosòdia continuen buides.",
        "",
        "| ordre | persona | forma | prioritat | clip |",
        "|---:|---|---|---|---|",
    ]
    lines.extend(
        f"| {row['ordre_sessio']} | `{row['persona']}` | **{row['forma']}** | {row['prioritat']} | `{row['clip']}` |"
        for row in selected
    )
    lines.extend(
        [
            "",
            "La sessió es pot obrir amb `../auditoria-global.html`; les anotacions exportades només s'incorporen al registre mestre després d'una decisió humana explícita.",
        ]
    )
    (SESSIONS / "sessio-05.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(selected)} clips · {SESSIONS / 'sessio-05.tsv'}")


if __name__ == "__main__":
    main()
