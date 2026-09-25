"""L'eina de línia d'ordres del cervell."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from cervell.model import load_corpus
from cervell.render import contract, index
from cervell.schema import load
from curacio.pipeline import check_corpus, generate_corpus

REPO = Path(__file__).resolve().parents[2]
SCHEMA = REPO / "schema" / "corpus.toml"


def _write_or_check(desti: Path, nou: str, *, check: bool) -> int:
    canvia = not desti.exists() or desti.read_text(encoding="utf-8") != nou
    if check:
        if canvia:
            print(f"R012 · {desti} no coincideix amb la seva font. Regenereu-lo.", file=sys.stderr)
            return 1
        print(f"ok · {desti} al dia")
        return 0
    desti.write_text(nou, encoding="utf-8")
    print(f"{'escrit' if canvia else 'sense canvis'} · {desti}")
    return 0


def cmd_render(args: argparse.Namespace) -> int:
    """Regenera els fitxers generats des de les seves fonts."""
    root = Path(args.root)
    schema = load(Path(args.schema))
    codi = _write_or_check(root / "CONTRACT.md", contract(schema), check=args.check)
    corpus = load_corpus(root)
    codi |= _write_or_check(root / "index.md", index(corpus), check=args.check)
    for u in corpus.unparsed:
        print(f"R011 · {u.path} · {u.reason}", file=sys.stderr)
        codi = 1
    return codi


def cmd_cura(args: argparse.Namespace) -> int:
    """Genera o comprova el corpus curat."""
    docs = Path(getattr(args, "root", "docs"))
    out = Path(getattr(args, "out", "corpus"))
    if getattr(args, "check", False):
        failures = check_corpus(docs, out)
        if failures:
            for failure in failures:
                print(f"divergència · {failure}", file=sys.stderr)
            return 1
        print(f"ok · {out} coincideix amb les entrades i les regles de curació")
        return 0
    generated = generate_corpus(docs, out)
    print(f"escrits · {len(generated)} fitxers a {out}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="cervell", description="El cervell andorrà.")
    sub = parser.add_subparsers(dest="ordre", required=True)

    r = sub.add_parser("render", help="Regenera els fitxers generats.")
    r.add_argument("root", nargs="?", default="docs", help="Arrel de la bóveda.")
    r.add_argument("--schema", default=str(SCHEMA), help="Ruta de l'esquema.")
    r.add_argument("--check", action="store_true", help="No escriu; falla si hi ha divergència.")
    r.set_defaults(func=cmd_render)

    c = sub.add_parser("cura", help="Genera o comprova el corpus curat.")
    c.add_argument(
        "--check", action="store_true", help="Falla si corpus/ difereix de la sortida calculada."
    )
    cura_sub = c.add_subparsers(dest="cura_ordre")
    tot = cura_sub.add_parser("tot", help="Executa totes les etapes de curació.")
    tot.add_argument("root", nargs="?", default="docs", help="Arrel de documents d'entrada.")
    tot.add_argument("--out", default="corpus", help="Arrel de sortida regenerable.")
    tot.set_defaults(func=cmd_cura)
    c.set_defaults(func=cmd_cura)

    args = parser.parse_args(argv)
    resultat: int = args.func(args)
    return resultat


if __name__ == "__main__":
    raise SystemExit(main())
