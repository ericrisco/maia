"""Audita els camps mínims de procedència de cada font del corpus."""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = PROV / "auditoria-proveniencia.tsv"
FIELDS = ("Font", "Canal", "URL", "Llicència declarada", "Consulta i descàrrega", "Derivat local", "ASR")


def main() -> None:
    rows: list[dict[str, str]] = []
    for path in sorted(PROV.glob("pa-*/README.md")):
        text = path.read_text(encoding="utf-8")
        values: dict[str, str] = {}
        for field in FIELDS:
            match = re.search(rf"^- \*\*{re.escape(field)}:\*\*\s*(.+)$", text, re.MULTILINE)
            values[field] = match.group(1).strip() if match else ""
        if not values["ASR"]:
            match = re.search(r"^- \*\*ASR inicial:\*\*\s*(.+)$", text, re.MULTILINE)
            values["ASR"] = match.group(1).strip() if match else ""
        required = [values[field] for field in FIELDS]
        policy = any(phrase in text.casefold() for phrase in ("no es redistribueix", "es pot redistribuir", "llicència oberta", "redistribució"))
        state = "complet" if all(required) and policy else "pendent"
        rows.append(
            {
                "id_persona": path.parent.name,
                "font": values["Font"],
                "canal": values["Canal"],
                "url": values["URL"],
                "llicencia": values["Llicència declarada"],
                "consulta": values["Consulta i descàrrega"],
                "derivat": values["Derivat local"],
                "asr": values["ASR"],
                "estat": state,
            }
        )
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        fields = ["id_persona", "font", "canal", "url", "llicencia", "consulta", "derivat", "asr", "estat"]
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    complete = sum(row["estat"] == "complet" for row in rows)
    print(f"{len(rows)} procedències auditades · completes={complete} · {OUT}")


if __name__ == "__main__":
    main()
