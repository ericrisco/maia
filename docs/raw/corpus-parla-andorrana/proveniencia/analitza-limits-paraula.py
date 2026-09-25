"""Recalcula coincidències ASR amb límits de paraula, no subcadenes simples."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import csv
import re
import unicodedata

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
GRAPH = ROOT / "grafo"


def norm(value: str) -> str:
    value = unicodedata.normalize("NFD", value.lower())
    return "".join(ch for ch in value if unicodedata.category(ch) != "Mn")


def match(form: str, text: str) -> bool:
    target = re.escape(norm(form)).replace(r"\ ", r"\s+")
    return re.search(rf"(?<![a-z0-9]){target}(?![a-z0-9])", norm(text)) is not None


def read(name: str) -> list[dict[str, str]]:
    with (PROV / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    small = {(r["id_persona"], r["forma"]): r for r in read("qa-clips.tsv")}
    base = {(r["id_persona"], r["forma"]): r for r in read("qa-clips-base.tsv")}
    rows = []
    speakers: dict[str, set[str]] = defaultdict(set)
    for key, s in small.items():
        b = base[key]
        form = s["forma"]
        old_small = s["forma_en_qa"] == "sí"
        old_base = b["forma_en_base"] == "sí"
        boundary_small = match(form, s["text_qa"])
        boundary_base = match(form, b["text_base"])
        boundary_consens = boundary_small and boundary_base
        if boundary_consens:
            speakers[form].add(s["id_persona"])
        rows.append({
            "id_persona": s["id_persona"], "forma": form, "interval_escolta": s["interval_escolta"], "clip": s["clip"],
            "small_subcadena": "sí" if old_small else "no", "base_subcadena": "sí" if old_base else "no",
            "small_limit_paraula": "sí" if boundary_small else "no", "base_limit_paraula": "sí" if boundary_base else "no",
            "consens_limit_paraula": "sí" if boundary_consens else "no",
            "text_small": s["text_qa"], "text_base": b["text_base"],
        })
    write(PROV / "qa-clips-boundary.tsv", list(rows[0]), rows)
    trait_rows = [{"forma": form, "n_parlants": str(len(ids)), "parlants": ",".join(sorted(ids)), "tipus": "consens-limits-paraula"} for form, ids in sorted(speakers.items()) if len(ids) >= 3]
    write(GRAPH / "trets-boundary-consens.tsv", ["forma", "n_parlants", "parlants", "tipus"], trait_rows)
    edges = [{"id_persona": person, "forma": form, "relacio": "consens-limits-paraula", "pes": "1"} for form, ids in sorted(speakers.items()) if len(ids) >= 3 for person in sorted(ids)]
    write(GRAPH / "arestes-parlants-boundary-consens.tsv", ["id_persona", "forma", "relacio", "pes"], edges)
    lines = ["graph TD"]
    for i, row in enumerate(trait_rows, 1):
        fnode = f"F{i}"
        lines.append(f'  {fnode}["{row["forma"]}\\n{row["n_parlants"]} parlants"]')
        for person in row["parlants"].split(","):
            pnode = f"P{person.replace('-', '')}"
            lines.append(f'  {pnode}("{person}")')
            lines.append(f"  {pnode} --> {fnode}")
    (GRAPH / "graf-parlants-boundary-consens.mmd").write_text("\n".join(lines) + "\n", encoding="utf-8")
    old_both = sum(r["small_subcadena"] == "sí" and r["base_subcadena"] == "sí" for r in rows)
    new_both = sum(r["consens_limit_paraula"] == "sí" for r in rows)
    false_positive = sum(r["small_subcadena"] == "sí" and r["base_subcadena"] == "sí" and r["consens_limit_paraula"] == "no" for r in rows)
    print(f"{len(rows)} clips · consens subcadena={old_both} · consens límit paraula={new_both} · falsos positius detectats={false_positive} · formes >=3={len(trait_rows)}")


if __name__ == "__main__":
    main()
