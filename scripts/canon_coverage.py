"""Measures how well the training data covers the Andorran canon.

The canon is the list of topics that any Andorran knows (parishes, institutions, key dates, symbols,
places, festivities...). For each topic this counts, by regex over the text:
  - conversations of an export (default export/K/train.jsonl) that mention it anywhere;
  - conversations where the user asks about it (it appears in a user turn);
  - corpus files (docs/temes, docs/fonts) that mention it.
A topic with knowledge in the corpus but few conversations is a dataset gap; a topic missing from
the corpus too is a corpus gap.

Usage:
    python scripts/canon_coverage.py [--export export/K/train.jsonl] [--md report.md]
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (group, topic, regex). Topics and patterns stay in Catalan: they are matched against Catalan text.
CANON: list[tuple[str, str, str]] = [
    ("territori", "set parròquies", r"set parròquies"),
    ("territori", "Canillo", r"\bCanillo\b"),
    ("territori", "Encamp", r"\bEncamp\b"),
    ("territori", "Ordino", r"\bOrdino\b"),
    ("territori", "la Massana", r"\bla Massana\b"),
    ("territori", "Andorra la Vella", r"Andorra la Vella"),
    ("territori", "Sant Julià de Lòria", r"Sant Juli[àa] de L[òo]ria"),
    ("territori", "Escaldes-Engordany", r"Escaldes"),
    ("territori", "Coma Pedrosa", r"Coma ?[Pp]edrosa"),
    ("territori", "Gran Valira / Valira", r"\bValira\b"),
    ("territori", "Port d'Envalira", r"Envalira"),
    ("territori", "Pas de la Casa", r"Pas de la Casa"),
    ("territori", "Madriu-Perafita-Claror", r"Madriu"),
    ("territori", "Engolasters", r"Engolasters"),
    ("territori", "Sorteny", r"Sorteny"),
    (
        "territori",
        "estacions d'esquí (Grandvalira, Pal, Arinsal, Arcalís)",
        r"Grandvalira|Arcal[íi]s|\bPal\b|Arinsal",
    ),
    ("institucions", "coprínceps", r"copr[íi]ncep"),
    ("institucions", "bisbe d'Urgell", r"bisbe d.Urgell"),
    (
        "institucions",
        "president de la República Francesa",
        r"president (de la República )?franc[eè]s",
    ),
    ("institucions", "Consell General", r"Consell General"),
    ("institucions", "síndic general", r"s[íi]ndic general"),
    ("institucions", "cap de Govern", r"cap de Govern"),
    ("institucions", "comú / cònsol", r"\bcomú\b|cònsol"),
    ("institucions", "Tribunal Constitucional", r"Tribunal Constitucional"),
    ("institucions", "Consell Superior de la Justícia", r"Consell Superior de la Just[íi]cia"),
    ("institucions", "batlles / Tribunal de Corts", r"\bbatlle|Tribunal de Corts"),
    ("institucions", "veguers", r"\bveguer"),
    ("institucions", "Raonador del Ciutadà", r"Raonador"),
    ("institucions", "quarts", r"\bquarts?\b"),
    ("historia", "Pareatges (1278, 1288)", r"[Pp]areatge"),
    ("historia", "Acta de consagració (839)", r"Acta de consagraci|\b839\b"),
    ("historia", "Carlemany", r"Carlemany"),
    ("historia", "Querimònia", r"Querim[òo]nia"),
    ("historia", "Manual Digest (1748)", r"Manual Digest"),
    ("historia", "Politar (1763)", r"Politar"),
    ("historia", "Nova Reforma (1866)", r"Nova Reforma|\b1866\b"),
    ("historia", "Constitució del 1993", r"Constituci[óo]"),
    ("historia", "14 de març", r"14 de març"),
    ("historia", "ingrés a l'ONU (1993)", r"\bONU\b|Nacions Unides"),
    ("historia", "Consell d'Europa", r"Consell d.Europa"),
    ("historia", "Borís Skóssyreff", r"Sk[óo]ssyreff|Skossyreff|Bor[íi]s I"),
    ("historia", "contraban", r"contraban"),
    ("historia", "neutralitat", r"neutral"),
    ("historia", "acord duaner amb la UE", r"acord duaner|unió duanera"),
    ("historia", "sufragi femení", r"sufragi femen|vot de les dones|dret de vot.{0,40}dones"),
    ("simbols", "bandera", r"\bbandera"),
    ("simbols", "escut", r"\bescut\b"),
    ("simbols", "himne «El gran Carlemany»", r"\bhimne|gran Carlemany"),
    ("simbols", "Meritxell", r"Meritxell"),
    ("simbols", "Casa de la Vall", r"Casa de la Vall"),
    ("costums", "Sant Antoni", r"Sant Antoni"),
    ("costums", "falles / Sant Joan", r"\bfalles\b|Sant Joan"),
    ("costums", "caramelles", r"caramelles"),
    ("costums", "festes majors", r"festa major|festes majors"),
    ("costums", "contrapàs", r"contrap[àa]s"),
    ("costums", "marratxa", r"marratxa"),
    ("costums", "Ball de Santa Anna", r"Santa Anna"),
    ("costums", "Sant Jordi", r"Sant Jordi"),
    ("costums", "Carnaval / Carnestoltes", r"Carnestoltes|[Cc]arnaval"),
    ("cultura", "romànic", r"rom[àa]nic"),
    ("cultura", "Sant Joan de Caselles", r"Caselles"),
    ("cultura", "Santa Coloma (església)", r"Santa Coloma"),
    ("cultura", "Sant Climent de Pal", r"Sant Climent"),
    ("cultura", "llegendes", r"llegend"),
    ("cultura", "Caldea", r"Caldea"),
    ("gastronomia", "trinxat", r"trinxat"),
    ("gastronomia", "escudella", r"escudella"),
    ("gastronomia", "cargols a la llauna", r"cargols"),
    ("gastronomia", "truita de carreroles", r"carreroles"),
    ("gastronomia", "coca / coques", r"\bcoques?\b"),
    ("gastronomia", "embotits / girella", r"girella|embotit"),
    ("economia", "tabac", r"\btabac"),
    ("economia", "turisme", r"turis"),
    ("economia", "banca", r"\bbanca\b|\bbancs?\b"),
    ("economia", "IGI / impostos", r"\bIGI\b|\bIRPF\b|imp[oò]st"),
    ("economia", "FEDA / energia", r"\bFEDA\b"),
    ("economia", "Andorra Telecom", r"Andorra Telecom|\bSTA\b"),
    ("llengua", "català llengua oficial", r"llengua oficial"),
    ("llengua", "parla andorrana / dialecte", r"parla andorrana|dialect"),
    ("societat", "residents i nacionalitat", r"nacionalitat"),
    ("societat", "immigració", r"immigra"),
    ("societat", "sistemes educatius", r"escola andorrana|sistema educatiu|sistemes educatius"),
    ("societat", "CASS", r"\bCASS\b"),
    ("persones", "Òscar Ribas Reig", r"Ribas Reig"),
    ("persones", "Joan Martí Alanis", r"Mart[íi] Alanis"),
    ("persones", "Joan Enric Vives", r"Joan Enric Vives|\bVives\b"),
    ("persones", "Antoni Martí", r"Antoni Mart[íi]\b"),
    ("persones", "Xavier Espot", r"Espot\b"),
    ("persones", "Marc Forné", r"Forn[ée]\b"),
    ("persones", "Albert Pintat", r"Pintat"),
    ("esports", "futbol / FC Andorra", r"FC Andorra|futbol"),
    ("esports", "esquí alpí", r"\besquí"),
    ("esports", "bàsquet / MoraBanc Andorra", r"b[àa]squet|MoraBanc"),
]


def load_conversations(path: Path) -> list[tuple[str, str]]:
    """(all text, user text) of each conversation, without the system message."""
    out = []
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            messages = json.loads(line)["messages"]
            turns = [m for m in messages if m["role"] != "system"]
            everything = "\n".join(m["content"] for m in turns)
            user = "\n".join(m["content"] for m in turns if m["role"] == "user")
            out.append((everything, user))
    return out


def load_corpus() -> list[str]:
    files = sorted((ROOT / "docs" / "temes").rglob("*.md")) + sorted(
        (ROOT / "docs" / "fonts").rglob("*.md")
    )
    return [f.read_text(encoding="utf-8", errors="ignore") for f in files]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--export", type=Path, default=ROOT / "export" / "K" / "train.jsonl")
    parser.add_argument("--md", type=Path, help="write the table as Markdown to this path")
    args = parser.parse_args()

    conversations = load_conversations(args.export)
    corpus = load_corpus()
    rows = []
    for group, topic, pattern in CANON:
        # Patterns with capitals (names, acronyms) are case-sensitive: «Pal» must not match «pal».
        rx = re.compile(pattern, re.IGNORECASE if pattern.islower() else 0)
        mentioned = sum(1 for text, _ in conversations if rx.search(text))
        asked = sum(1 for _, user in conversations if rx.search(user))
        in_corpus = sum(1 for text in corpus if rx.search(text))
        rows.append((group, topic, mentioned, asked, in_corpus))

    header = (
        "| Grup | Tema | Converses | Preguntat | Fitxers del corpus |\n|---|---|---:|---:|---:|"
    )
    lines = [header] + [f"| {g} | {t} | {m} | {a} | {c} |" for g, t, m, a, c in rows]
    table = "\n".join(lines)
    print(f"{len(conversations)} conversations in {args.export}, {len(corpus)} corpus files\n")
    print(table)
    if args.md:
        args.md.write_text(table + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
