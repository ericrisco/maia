"""Verifica la integritat de les sessions d'audició del corpus."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
SESSIONS = PROV / "sessions"
EXPECTED = {"sessio-01": 65, "sessio-02": 20, "sessio-03": 12, "sessio-04": 4, "sessio-05": 20, "sessio-06": 19}


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> int:
    errors: list[str] = []
    sessions: dict[str, list[dict[str, str]]] = {}
    for name, expected in EXPECTED.items():
        path = SESSIONS / f"{name}.tsv"
        if not path.exists():
            errors.append(f"falta {path.relative_to(ROOT)}")
            continue
        rows = read(path)
        sessions[name] = rows
        if len(rows) != expected:
            errors.append(f"{name}: files={len(rows)} esperades={expected}")
        ids = [row.get("id_global", "") for row in rows]
        if len(ids) != len(set(ids)):
            errors.append(f"{name}: id_global duplicat")
        missing = [row.get("clip", "") for row in rows if not (PROV / row.get("clip", "")).exists()]
        if missing:
            errors.append(f"{name}: clips inexistents={len(missing)}")
        if any(row.get("estat") != "pendent" for row in rows):
            errors.append(f"{name}: hi ha files que no estan pendents d'audició")
    canonical = {
        name: {row.get("clip", "") for row in rows}
        for name, rows in sessions.items()
        if name in {"sessio-01", "sessio-02", "sessio-05", "sessio-06"}
    }
    for left, right in (("sessio-01", "sessio-02"), ("sessio-01", "sessio-05"), ("sessio-02", "sessio-05"), ("sessio-01", "sessio-06"), ("sessio-02", "sessio-06"), ("sessio-05", "sessio-06")):
        overlap = canonical.get(left, set()) & canonical.get(right, set())
        if overlap:
            errors.append(f"solapament canònic {left}/{right}: {len(overlap)}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("OK sessions: 6 manifests · 140 files · audio local i sense solapament canònic")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
