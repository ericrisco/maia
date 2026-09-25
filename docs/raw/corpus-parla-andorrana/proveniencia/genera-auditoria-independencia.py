"""Comprova que el subcorpus no enllaci amb documents externs del brain."""
from __future__ import annotations

import csv
import re
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).parents[1]
OUT = ROOT / "proveniencia" / "auditoria-independencia.tsv"
LINK = re.compile(r"!?(?:\[[^\]]*\])\(([^)]+)\)")


def main() -> None:
    rows: list[dict[str, str]] = []
    for path in sorted(ROOT.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        outside: list[str] = []
        missing: list[str] = []
        external_urls = 0
        for raw in LINK.findall(text):
            target = raw.strip().split(" ", 1)[0].strip("<>")
            parsed = urlparse(target)
            if parsed.scheme or target.startswith("//"):
                external_urls += 1
                continue
            target_path = unquote(parsed.path)
            if not target_path:
                continue
            resolved = (path.parent / target_path).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                outside.append(target)
                continue
            if not resolved.exists():
                missing.append(target)
        mentions_brain = "brain" in text.casefold()
        state = "independent" if not outside and not missing else "revisar"
        rows.append(
            {
                "fitxer": str(path.relative_to(ROOT)),
                "enllacos_externs": str(external_urls),
                "fora_subcorpus": ";".join(outside),
                "fitxers_inexistents": ";".join(missing),
                "mencio_brain": "sí" if mentions_brain else "no",
                "estat": state,
            }
        )
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        fields = ["fitxer", "enllacos_externs", "fora_subcorpus", "fitxers_inexistents", "mencio_brain", "estat"]
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    independent = sum(row["estat"] == "independent" for row in rows)
    print(f"{len(rows)} documents auditats · independents={independent} · revisar={len(rows)-independent} · {OUT}")


if __name__ == "__main__":
    main()
