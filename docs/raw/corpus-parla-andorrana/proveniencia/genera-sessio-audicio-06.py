"""Genera una sessió que cobreix parlants canònics absents de les cues anteriors."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
SESSIONS = PROV / "sessions"
QUARANTINE = {"pa-044", "pa-047", "pa-050"}


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    canonical = read(PROV / "persones-canonics.tsv")
    source_to_speaker = {row["id_persona"]: row["id_parlant"] for row in canonical}
    covered_sources = set()
    for name in ("sessio-01.tsv", "sessio-02.tsv", "sessio-05.tsv"):
        covered_sources.update(
            row["persona"]
            for row in read(SESSIONS / name)
            if row.get("origen") == "canònic"
        )
    covered_speakers = {source_to_speaker[source] for source in covered_sources if source in source_to_speaker}
    needed = set(source_to_speaker.values()) - covered_speakers
    needed = {
        speaker
        for speaker in needed
        if any(source not in QUARANTINE for source, value in source_to_speaker.items() if value == speaker)
    }
    used = {
        row["clip"]
        for name in ("sessio-01.tsv", "sessio-02.tsv", "sessio-05.tsv")
        for row in read(SESSIONS / name)
    }
    acoustic = {row["clip"]: row for row in read(PROV / "analisi-acustica-clips.tsv")}
    formants = {
        (row["id_persona"], row["forma"], row["clip"]): row
        for row in read(PROV / "analisi-formants-qa.tsv")
    }
    selected: list[dict[str, str]] = []
    selected_speakers: set[str] = set()
    for candidate in read(PROV / "prioritat-audicio-triple.tsv"):
        source = candidate["id_persona"]
        speaker = source_to_speaker.get(source)
        if speaker not in needed or speaker in selected_speakers or candidate["clip"] in used:
            continue
        signal = acoustic.get(candidate["clip"], {})
        token = formants.get((source, candidate["forma"], candidate["clip"]), {})
        ordinal = len(selected) + 1
        selected.append(
            {
                "ordre_sessio": str(ordinal),
                "id_global": f"canon::{source}::{candidate['forma']}::s06-{ordinal}",
                "origen": "canònic",
                "persona": source,
                "forma": candidate["forma"],
                "clip": candidate["clip"],
                "prioritat": candidate["prioritat_triple"],
                "prob_min": candidate["token_prob_min"],
                "text": candidate["text_greedy"],
                "motiu": "sessió 06: primer clip prioritzat per a un parlant canònic absent de les sessions 01–02 i 05",
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
        selected_speakers.add(speaker)
    if selected_speakers != needed:
        raise SystemExit(f"cobertura incompleta: seleccionats={len(selected_speakers)} necessaris={len(needed)}")
    with (SESSIONS / "sessio-06.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(selected[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(selected)
    lines = [
        "# Sessió d'audició 06 — cobertura dels parlants absents",
        "",
        f"Aquesta sessió conté **{len(selected)} clips**, un per cadascun dels {len(selected)} parlants canònics actius que no apareixien a les sessions 01–02 i 05. Les dades automàtiques només orienten l'escolta; les decisions humanes continuen buides.",
        "",
        "| ordre | persona | forma | prioritat | clip |",
        "|---:|---|---|---|---|",
    ]
    lines.extend(
        f"| {row['ordre_sessio']} | `{row['persona']}` | **{row['forma']}** | {row['prioritat']} | `{row['clip']}` |"
        for row in selected
    )
    lines.extend(["", "Les tres veus en quarantena es mantenen fora d'aquesta sessió i conserven la seva cua específica."])
    (SESSIONS / "sessio-06.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(selected)} clips · {len(selected_speakers)} parlants absents coberts")


if __name__ == "__main__":
    main()
