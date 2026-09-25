"""Calcula inventaris textuals comparables per als cinquanta expedients nous."""
from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).parents[1]
PROSPECCIO = ROOT / "proveniencia" / "prospeccio"
LEADS = [
    "lead-rtva-009-isidre-bartumeu",
    "lead-rtva-010-lurdes-riba",
    "lead-rtva-011-josep-dalleres",
    "lead-rtva-012-marc-forne",
    "lead-rtva-013-pere-vilanova",
    "lead-rtva-014-joan-burgues",
    "lead-rtva-015-isidre-baro",
    "lead-rtva-016-josep-areny",
    "lead-rtva-017-simo-duro",
    "lead-rtva-018-ricard-fiter",
    "lead-rtva-019-lisa-cruz",
    "lead-rtva-020-monica-bonell",
    "lead-rtva-021-bonaventura-riberaygua",
    "lead-rtva-022-josep-marsal",
    "lead-rtva-023-josep-maria-cases",
    "lead-rtva-024-denisa-font",
    "lead-rtva-025-albert-gelabert",
    "lead-rtva-026-rosa-maria-mandico",
    "lead-rtva-027-jordi-guillamet",
    "lead-rtva-028-pere-besoli",
    "lead-rtva-029-angelina-mas",
    "lead-rtva-030-casimir-arajol",
    "lead-rtva-031-ramon-rossell",
    "lead-rtva-032-anna-riberaygua",
    "lead-yt-033-david-montane",
    "lead-yt-034-antoni-marti",
    "lead-yt-035-cerni-escale",
    "lead-yt-036-xavier-espot",
    "lead-yt-037-oscar-ribas",
    "lead-yt-038-conxita-marsol",
    "lead-yt-039-marta-roure",
    "lead-yt-040-guillem-forne",
    "lead-yt-041-guillem-areny",
    "lead-yt-042-andreu-gonzalez",
    "lead-yt-043-oriol-agorreta",
    "lead-yt-044-laura-casanovas",
    "lead-yt-045-arnau-rius",
    "lead-yt-046-alberto-villagrasa",
    "lead-yt-047-katia-ustina",
    "lead-yt-048-ander-mirambell",
    "lead-yt-049-joan-piquet",
    "lead-yt-050-pau-chica",
    "lead-yt-051-albert-vilaro",
    "lead-yt-052-valenti-closa",
    "lead-yt-053-sonia-andorrita",
    "lead-yt-054-francesc-solana",
    "lead-yt-055-enric-flix",
    "lead-yt-056-arnau-fortuny",
    "lead-yt-057-gabriel-lezkano",
    "lead-yt-058-nuria-pablos",
    "lead-rtva-059-carles-ensenyat",
    "lead-rtva-060-xavier-espot-actual",
    "lead-rtva-061-antoni-morell",
]
MARKERS = ["bé", "bueno", "clar", "doncs", "llavors", "aleshores", "de fet", "és a dir", "o sigui", "vull dir", "a veure", "aviam", "diguem", "evidentment", "per tant", "a nivell", "no?"]
TERRITORIAL = ["andorrà", "andorrana", "parròquia", "comú", "comuns", "copríncep", "veguer", "vegueria", "comunal", "comunals", "bordes", "ramat", "pastura", "aiguat", "santuari", "padrí", "pagesia", "Canillo", "Encamp", "Ordino", "Escaldes", "Massana", "Sant Julià", "Constitució", "coprincipat", "principat"]
CONTACT = ["castellà", "espanyol", "espanyola", "francès", "francesa", "anglès", "barbarisme", "barbarismes"]
CLITICS = {"em", "m", "me", "ens", "el", "la", "els", "les", "ho", "hi", "en", "n", "se", "es"}


def count(text: str, form: str) -> int:
    return len(re.findall(r"(?i)(?<!\w)" + re.escape(form) + r"(?!\w)", text))


def analyse(text: str) -> dict[str, str]:
    words = re.findall(r"[a-zàèéíïòóúüç·']+", text.lower())
    bare = [word.strip("'·") for word in words if word.strip("'·")]
    grams = Counter(tuple(bare[i : i + 3]) for i in range(max(0, len(bare) - 2)))
    marker = ";".join(f"{form}={count(text, form)}" for form in MARKERS if count(text, form))
    territorial = ";".join(f"{form}={count(text, form)}" for form in TERRITORIAL if count(text, form))
    contact = ";".join(f"{form}={count(text, form)}" for form in CONTACT if count(text, form))
    clitic = sum(word in CLITICS or any(word.startswith(clitic + "'") for clitic in CLITICS) for word in bare)
    past = sum(word in {"vaig", "vas", "va", "vam", "vau", "van"} for word in bare)
    first = sum(count(text, form) for form in ["jo", "nosaltres", "nos", "me'n", "m'"])
    negation = sum(count(text, form) for form in ["no", "mai", "tampoc"])
    return {
        "tokens": str(len(bare)),
        "tipus_lexics": str(len(set(bare))),
        "type_token_ratio": f"{len(set(bare)) / len(bare):.4f}" if bare else "0",
        "repeticio_3gram": f"{sum(n - 1 for n in grams.values() if n > 1) / max(len(grams), 1):.4f}",
        "marcadors_discursius": marker,
        "formes_territorials": territorial,
        "formes_contacte": contact,
        "pronoms_clitics": str(clitic),
        "perifrasi_past_aparent": str(past),
        "primera_persona": str(first),
        "negacio": str(negation),
        "nota": "recompte ASR; validar contra àudio",
    }


def main() -> None:
    summary = []
    for lead in LEADS:
        slug = lead.split("-", 3)[3]
        rows = []
        for model in ("small", "base"):
            candidates = sorted((PROSPECCIO / lead / "asr").glob(f"*{model}*nocontext.txt"))
            if not candidates and model == "small":
                candidates = sorted((PROSPECCIO / lead / "asr").glob("*-nocontext.txt"))
            transcript = candidates[0]
            row = {"expedient": lead, "model": model, **analyse(transcript.read_text(encoding="utf-8", errors="ignore")), "estat": "inventari ASR; pendent d'audició"}
            rows.append(row)
        out = PROSPECCIO / lead / "analisi-linguistica.tsv"
        with out.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
            writer.writeheader(); writer.writerows(rows)
        report = PROSPECCIO / lead / "informe.md"
        report_text = report.read_text(encoding="utf-8")
        marker = "## Inventari lingüístic comparable"
        if marker not in report_text:
            table = "\n".join(
                f"| {row['model']} | {row['tokens']} | {row['tipus_lexics']} | {row['type_token_ratio']} | {row['pronoms_clitics']} | {row['perifrasi_past_aparent']} | {row['primera_persona']} | {row['negacio']} |"
                for row in rows
            )
            section = f"""\n\n{marker}\n\nLa taula [`analisi-linguistica.tsv`](analisi-linguistica.tsv) conserva, per a `small` i `base`, recompte de tokens i tipus, diversitat lèxica, marcadors discursius, formes territorials, contacte lingüístic, clítics, passat perifràstic aparent, primera persona i negació.\n\n| model | tokens | tipus | TTR | clítics | passat aparent | primera persona | negació |\n|---|---:|---:|---:|---:|---:|---:|---:|\n{table}\n\nAquests recomptes provenen de l'ASR i són candidats textuals; no confirmen trets dialectals, identitat de veu ni variants fonètiques.\n"""
            report.write_text(report_text.rstrip() + section, encoding="utf-8")
        summary.extend(rows)
    out = PROSPECCIO / "resum-analisi-linguistica.tsv"
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(summary)
    print(f"OK anàlisi lingüística de prospecció: {len(summary)} passades · {len(LEADS)} expedients")


if __name__ == "__main__":
    main()
