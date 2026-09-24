"""Audita que les pàgines README tinguin un títol identificable."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parents[1]
DOCS = ROOT / "docs"
OUT = DOCS / "raw" / "auditoria-readme-titols.tsv"
GENERIC = {"readme", "font", "font:"}


def main() -> None:
    rows: list[dict[str, str]] = []
    # Inclou tant README.md com les fitxes amb sufix .README.md.
    paths = sorted(set(DOCS.rglob("README.md")) | set(DOCS.rglob("*.README.md")))
    for path in paths:
        title = ""
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                title = line[2:].strip()
                break
        normalized = re.sub(r"\s+", " ", title.casefold()).strip()
        if not title:
            state, note = "revisar", "falta un H1"
        elif normalized in GENERIC:
            state, note = "revisar", "títol genèric"
        else:
            state, note = "identificable", ""
        rows.append(
            {"fitxer": str(path.relative_to(DOCS)), "titol": title, "estat": state, "nota": note}
        )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["fitxer", "titol", "estat", "nota"],
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)
    counts = Counter(row["estat"] for row in rows)
    print(
        f"{len(rows)} README auditats · identificables={counts['identificable']}"
        f" · revisar={counts['revisar']} · {OUT}"
    )


if __name__ == "__main__":
    main()
