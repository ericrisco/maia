"""Extreu contextos textuals de patrons gramaticals i de contacte.

La sortida és evidència candidata de l'ASR. No afirma que la forma s'hagi
pronunciat així fins que el clip corresponent tingui una decisió auditiva.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
import csv
import re
import unicodedata

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
MARKER = "### Evidència gramatical i de contacte textual"

POSSESSIUS = {
    "meu", "meva", "meus", "meves", "teu", "teva", "teus", "teves",
    "seu", "seva", "seus", "seves", "nostre", "nostra", "nostres",
    "vostre", "vostra", "vostres",
}
CONTACTE_CASTELLA = {"bueno", "pues", "entonces", "vale", "oiga", "o sigui"}
AUXILIARS = {"vaig", "vas", "va", "vam", "vàrem", "vau", "van"}
TOKEN_RE = re.compile(r"[a-zàèéíïòóúüç·']+", re.IGNORECASE)
INCOATIU_RE = re.compile(r"^.{3,}(?:eix|eixes|eixem|eixen|eixi|eixis|eixeu)$", re.IGNORECASE)
INCOATIU_EXCLUSIONS = {"mateix", "mateixa", "mateixos", "mateixes", "peix", "peixos", "feix", "feixos"}


def norm(value: str) -> str:
    return unicodedata.normalize("NFC", value.lower())


def context(tokens: list[str], index: int, radius: int = 5) -> str:
    start = max(0, index - radius)
    end = min(len(tokens), index + radius + 1)
    return " ".join(tokens[start:end])


def add(rows: list[dict[str, str]], seen: set[tuple[str, str, int]], pid: str, category: str, form: str, index: int, tokens: list[str]) -> None:
    key = (category, form, index)
    if key in seen:
        return
    seen.add(key)
    rows.append({
        "id_persona": pid,
        "categoria": category,
        "forma": form,
        "index_token": str(index),
        "context": context(tokens, index),
        "estat": "candidat textual ASR; revisió auditiva pendent",
    })


def replace_section(text: str, marker: str, section: str) -> str:
    if marker not in text:
        return text.rstrip() + "\n" + section
    start = text.index(marker)
    next_heading = text.find("\n### ", start + len(marker))
    end = len(text) if next_heading == -1 else next_heading + 1
    return text[:start].rstrip() + "\n" + section.rstrip() + "\n\n" + text[end:].lstrip()


def main() -> None:
    people = []
    with (ROOT / "persones.tsv").open(encoding="utf-8", newline="") as handle:
        people = list(csv.DictReader(handle, delimiter="\t"))
    evidence: list[dict[str, str]] = []
    per_person: dict[str, Counter[str]] = defaultdict(Counter)
    for person in people:
        pid = person["id_persona"]
        text = norm((ROOT / "transcripcions" / f"{pid}.txt").read_text(encoding="utf-8", errors="ignore"))
        tokens = [match.group(0).strip("'") for match in TOKEN_RE.finditer(text)]
        seen: set[tuple[str, str, int]] = set()
        for index, token in enumerate(tokens):
            if token in POSSESSIUS:
                add(evidence, seen, pid, "possessius_candidat", token, index, tokens)
            if token in {"en", "n"} or token.startswith("n'"):
                add(evidence, seen, pid, "pronom_en_candidat", token, index, tokens)
            if token == "hi":
                add(evidence, seen, pid, "pronom_hi_candidat", token, index, tokens)
            if token == "ho":
                add(evidence, seen, pid, "pronom_ho_candidat", token, index, tokens)
            if INCOATIU_RE.match(token) and token not in INCOATIU_EXCLUSIONS:
                add(evidence, seen, pid, "incoatiu_eix_candidat", token, index, tokens)
            if token in CONTACTE_CASTELLA:
                add(evidence, seen, pid, "contacte_castella_candidat", token, index, tokens)
            if token in {"mai", "tampoc", "gens"}:
                add(evidence, seen, pid, "negacio_lexical_candidat", token, index, tokens)
            if token == "no" and any(candidate == "pas" for candidate in tokens[index + 1:index + 5]):
                add(evidence, seen, pid, "negacio_no_pas_candidat", "no ... pas", index, tokens)
            if token in AUXILIARS and index + 1 < len(tokens):
                following = tokens[index + 1]
                if following not in {"a", "de", "que", "hi", "ho", "les", "els", "la", "el"}:
                    add(evidence, seen, pid, "perifrasi_past_candidata", f"{token} {following}", index, tokens)
        for row in evidence:
            if row["id_persona"] == pid:
                per_person[pid][row["categoria"]] += 1
    fields = ["id_persona", "categoria", "forma", "index_token", "context", "estat"]
    with (PROV / "evidencia-gramatica.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(evidence)
    summary_fields = ["id_persona", "n_contextos", "categories", "estat"]
    summary = []
    for person in people:
        pid = person["id_persona"]
        counts = per_person.get(pid, Counter())
        summary.append({
            "id_persona": pid,
            "n_contextos": str(sum(counts.values())),
            "categories": ";".join(f"{key}={counts[key]}" for key in sorted(counts)),
            "estat": "candidat textual ASR; revisió auditiva pendent",
        })
        report = ROOT / "persones" / f"{pid}.md"
        text = report.read_text(encoding="utf-8")
        if counts:
            details = "; ".join(f"{key}={counts[key]}" for key in sorted(counts))
            section = f"\n{MARKER}\n\nLa transcripció ASR conté **{sum(counts.values())} contextos candidats** en aquestes categories: {details}. Els contextos localitzables queden a `../proveniencia/evidencia-gramatica.tsv`; són indicadors textuals i requereixen escolta.\n"
        else:
            section = f"\n{MARKER}\n\nNo s'han detectat aquests patrons en la transcripció ASR; la resta de dimensions continua pendent d'escolta.\n"
        report.write_text(replace_section(text, MARKER, section), encoding="utf-8")
    with (PROV / "resum-evidencia-gramatica.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=summary_fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(summary)
    print(f"{len(evidence)} contextos · {len(people)} persones · {len({r['categoria'] for r in evidence})} categories")


if __name__ == "__main__":
    main()
