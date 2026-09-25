"""Audita que el subcorpus no tenga enlaces desde el resto de Maia.

La frontera se comprueba fuera del directorio del corpus: una referencia
textual al slug del subcorpus queda registrada para revisarla manualmente.
"""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).parents[1]
DOCS = ROOT.parents[1]
SLUG = "corpus-parla-andorrana"
OUT = ROOT / "proveniencia" / "auditoria-aillament-brain.tsv"
REPORT = ROOT / "proveniencia" / "auditoria-aillament-brain.md"
TEXT_EXTENSIONS = {
    ".md", ".markdown", ".txt", ".tsv", ".csv", ".json", ".yaml", ".yml",
    ".html", ".htm", ".py", ".js", ".ts", ".toml",
}


def main() -> None:
    rows = []
    for path in sorted(DOCS.rglob("*")):
        relative = path.relative_to(DOCS)
        # Obsidian's open-file state and the title-audit export are navigation
        # metadata, not semantic links between corpus documents.
        if (
            not path.is_file()
            or ROOT in path.parents
            or path.suffix.lower() not in TEXT_EXTENSIONS
            or relative.parts[0] == ".obsidian"
            or relative == Path("raw/auditoria-readme-titols.tsv")
        ):
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for lineno, line in enumerate(lines, 1):
            if SLUG not in line or not ("](" in line or "href=" in line):
                continue
            rows.append(
                {
                    "fitxer": str(path.relative_to(DOCS)),
                    "linia": str(lineno),
                    "referencia": SLUG,
                    "estat": "referència-fora-del-subcorpus",
                    "fragment": " ".join(line.strip().split())[:240],
                }
            )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fields = ["fitxer", "linia", "referencia", "estat", "fragment"]
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    REPORT.write_text(
        "# Auditoria d'aïllament del subcorpus\n\n"
        "Aquesta auditoria busca el slug `corpus-parla-andorrana` fora del seu "
        "propi directori dins de `maia/docs`.\n\n"
        f"- Referències fora del subcorpus: **{len(rows)}**.\n"
        f"- Registre regenerable: `{OUT.name}`.\n\n"
        + ("No s'ha trobat cap referència fora del subcorpus.\n" if not rows else
           "Les referències trobades queden registrades per decidir si són només una entrada de navegació o un enllaç semàntic que cal retirar.\n"),
        encoding="utf-8",
    )
    print(f"OK aïllament brain: {len(rows)} referències fora del subcorpus")


if __name__ == "__main__":
    main()
