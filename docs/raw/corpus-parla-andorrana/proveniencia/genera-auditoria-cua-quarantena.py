"""Contrasta la cua humana de quarantena amb la passada ASR alternativa."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = PROV / "auditoria-cua-quarantena-20s.tsv"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    alternative = {row["id_clip"]: row for row in read(PROV / "qa-quarantena-20s-alt-resum.tsv")}
    rows: list[dict[str, str]] = []
    for source in read(PROV / "cua-audicio-quarantena-20s.tsv"):
        clip = Path(source["clip"]).stem
        alt = alternative.get(clip, {})
        rows.append(
            {
                "ordre": source["ordre"],
                "id_clip": clip,
                "id_persona": source["id_persona"],
                "clip": source["clip"],
                "estat_asr_alternatiu": alt.get("estat", "absent"),
                "repeticio_trigramas": alt.get("repeticio_trigramas", ""),
                "decisio_humana": source.get("decisio", "pendent"),
                "estat": "preparat" if alt.get("estat") == "text-localitzable" and source.get("decisio", "pendent") == "pendent" else "revisar",
            }
        )
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        fields = list(rows[0])
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} clips de cua · preparats={sum(row['estat'] == 'preparat' for row in rows)} · {OUT}")


if __name__ == "__main__":
    main()
