"""Resumeix els descriptors acústics dels clips amb consens entre dos ASR."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from statistics import median
import csv

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
MARKER = "### Perfil acústic dels consensos"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def fmt(value: float | None, digits: int = 2) -> str:
    return "—" if value is None else f"{value:.{digits}f}"


def main() -> None:
    consens = {
        (row["id_persona"], row["forma"], row["interval_escolta"]): row
        for row in read(PROV / "qa-clips-consens.tsv")
        if row["consens_textual"] == "sí"
    }
    acoustic = {
        (row["id_persona"], row["forma"], row["interval_escolta"]): row
        for row in read(PROV / "analisi-acustica-clips.tsv")
    }
    fields = [
        "id_persona", "forma", "interval_escolta", "clip", "durada_s", "veu_proporcio",
        "rms_p10_db", "rms_p50_db", "rms_p90_db", "zcr_p10", "zcr_p90",
        "f0_median_hz", "f0_iqr_hz", "centroid_median_hz", "centroid_p90_hz",
        "segments_veu", "pausa_mediana_s", "mostres_f0",
    ]
    rows = []
    by_person: dict[str, list[dict[str, str]]] = defaultdict(list)
    by_form: dict[str, list[dict[str, str]]] = defaultdict(list)
    for key, q in consens.items():
        a = acoustic[key]
        row = {field: a.get(field, "") for field in fields}
        rows.append(row)
        by_person[q["id_persona"]].append(row)
        by_form[q["forma"]].append(row)
    with (PROV / "analisi-acustica-consens.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(sorted(rows, key=lambda r: (r["id_persona"], r["forma"])))

    summary = []
    for form, items in sorted(by_form.items()):
        def nums(name: str) -> list[float]:
            return [float(row[name]) for row in items if row.get(name) not in (None, "", "nan")]
        summary.append({
            "forma": form,
            "n_clips": str(len(items)),
            "n_parlants": str(len({row["id_persona"] for row in items})),
            "f0_median_hz": fmt(median(nums("f0_median_hz"))),
            "f0_iqr_median_hz": fmt(median(nums("f0_iqr_hz"))),
            "veu_proporcio_median": fmt(median(nums("veu_proporcio")), 3),
            "pausa_mediana_s": fmt(median(nums("pausa_mediana_s")), 3),
            "centroid_median_hz": fmt(median(nums("centroid_median_hz"))),
        })
    summary_fields = list(summary[0]) if summary else ["forma", "n_clips", "n_parlants", "f0_median_hz", "f0_iqr_median_hz", "veu_proporcio_median", "pausa_mediana_s", "centroid_median_hz"]
    with (PROV / "resum-acustica-formes-consens.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=summary_fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(summary)

    with (ROOT / "persones.tsv").open(encoding="utf-8", newline="") as handle:
        people = list(csv.DictReader(handle, delimiter="\t"))
    for person in people:
        pid = person["id_persona"]
        items = by_person.get(pid, [])
        report = ROOT / "persones" / f"{pid}.md"
        text = report.read_text(encoding="utf-8")
        if MARKER in text:
            text = text[: text.index(MARKER)].rstrip() + "\n"
        if items:
            def pnums(name: str) -> list[float]:
                return [float(row[name]) for row in items if row.get(name) not in (None, "", "nan")]
            section = (
                f"\n{MARKER}\n\n"
                f"En els **{len(items)} clips** amb consens textual entre els dos ASR, els descriptors "
                f"orientatius tenen mediana de F0 **{fmt(median(pnums('f0_median_hz')))} Hz**, IQR de F0 "
                f"**{fmt(median(pnums('f0_iqr_hz')))} Hz**, proporció de veu **{fmt(median(pnums('veu_proporcio')), 3)}**, "
                f"pausa mediana **{fmt(median(pnums('pausa_mediana_s')), 3)} s** i centroid espectral "
                f"**{fmt(median(pnums('centroid_median_hz')))} Hz**.\n\n"
                "Són mesures de selecció del senyal en fragments on dos models coincideixen textualment; "
                "no són medicions fonètiques ni permeten inferir un tret dialectal sense escolta i anotació. "
                "La taula de clips és `../proveniencia/analisi-acustica-consens.tsv`.\n"
            )
        else:
            section = f"\n{MARKER}\n\nNo hi ha clips amb consens textual per calcular aquest resum acústic.\n"
        report.write_text(text.rstrip() + "\n" + section, encoding="utf-8")
    print(f"{len(rows)} clips consensuals · {len(summary)} formes · {len(people)} informes actualitzats")


if __name__ == "__main__":
    main()
