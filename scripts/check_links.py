#!/usr/bin/env python3
"""El comprovador d'enllaços del corpus.

Existeix perquè `cervell render --check` valida el frontmatter i els fitxers
generats, però no mira el cos dels articles. Un enllaç trencat hi passava
sencer.

Comprova dues regles del corpus:

1. Tot enllaç relatiu ha d'apuntar a un fitxer que existeix.
2. Cap enllaç no apunta a un directori: sempre a un FITXER.

Els wikilinks ja els cobreix la regla `R009` de `cervell render --check`, i
aquí no es repeteixen.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
EXTERNAL = ("http://", "https://", "mailto:", "tel:", "data:", "ftp://")


def targets(text: str) -> list[str]:
    """Els destins d'enllaç d'un document, sense els externs ni les àncores."""
    out = []
    for raw in LINK.findall(text):
        # Markdown permet embolcallar una destinació amb espais entre <...>.
        # El delimitador no forma part del nom del fitxer.
        raw = raw[1:-1] if raw.startswith("<") and raw.endswith(">") else raw
        if raw.startswith(EXTERNAL) or raw.startswith("#"):
            continue
        out.append(raw)
    return out


def check(root: Path) -> list[str]:
    """Retorna la llista d'errors trobats sota `root`."""
    errors: list[str] = []
    for path in sorted(root.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(root.parent)

        for raw in targets(text):
            target = raw.split("#", 1)[0]
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            if resolved.is_dir():
                errors.append(f"{rel}: «{raw}» apunta a un directori, i ha d'apuntar a un fitxer")
            elif not resolved.exists():
                errors.append(f"{rel}: «{raw}» no existeix")
    return errors


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "docs")
    if not root.is_dir():
        print(f"no hi ha cap directori {root}", file=sys.stderr)
        return 2

    errors = check(root)
    total = len(list(root.rglob("*.md")))
    if errors:
        for e in errors:
            print(f"  ✗ {e}")
        print(f"\n{len(errors)} enllaços trencats en {total} documents")
        return 1
    print(f"ok · enllaços comprovats en {total} documents")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
