"""Extreu contextos localitzables per als trets candidats de cada transcripció."""

from pathlib import Path
import csv
import re
import unicodedata

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"


def normalized_with_map(text: str):
    out = []
    mapping = []
    for index, char in enumerate(text):
        normalized = unicodedata.normalize("NFD", char).lower()
        for piece in normalized:
            if unicodedata.category(piece) != "Mn":
                out.append(piece)
                mapping.append(index)
    return "".join(out), mapping


def snippets(text: str, form: str, limit: int = 3):
    hits = []
    pattern = re.compile(r"(?<!\w)" + re.escape(form) + r"(?!\w)", re.IGNORECASE)
    for match in pattern.finditer(text):
        hits.append((match.start(), match.end()))
    if not hits:
        normalized, mapping = normalized_with_map(text)
        target, _ = normalized_with_map(form)
        if target:
            start = 0
            while len(hits) < limit:
                index = normalized.find(target, start)
                if index < 0:
                    break
                end = index + len(target)
                if (index == 0 or not normalized[index - 1].isalnum()) and (end == len(normalized) or not normalized[end].isalnum()):
                    hits.append((mapping[index], mapping[end - 1] + 1))
                start = max(index + 1, end)
    result = []
    for start, end in hits[:limit]:
        left = max(0, start - 95)
        right = min(len(text), end + 95)
        snippet = re.sub(r"\s+", " ", text[left:right]).strip()
        result.append(snippet)
    return result


def main() -> None:
    with (ROOT / "persones.tsv").open(encoding="utf-8", newline="") as handle:
        people = [r["id_persona"] for r in csv.DictReader(handle, delimiter="\t")]
    with (OUT := (ROOT / "grafo" / "trets-linguistics.tsv")).open(encoding="utf-8", newline="") as handle:
        traits = list(csv.DictReader(handle, delimiter="\t"))
    forms = [(r["categoria"], r["forma"]) for r in traits]
    rows = []
    report_data = {}
    for person in people:
        text = (ROOT / "transcripcions" / f"{person}.txt").read_text(encoding="utf-8", errors="replace")
        report_data[person] = []
        for category, form in forms:
            found = snippets(text, form)
            if not found:
                continue
            report_data[person].append((category, form, len(found), found[0]))
            for index, snippet in enumerate(found, start=1):
                rows.append({
                    "categoria": category,
                    "forma": form,
                    "id_persona": person,
                    "ocurrencia": str(index),
                    "snippet": snippet,
                    "font": f"transcripcions/{person}.txt",
                    "estat": "ASR; pendent d'audicio",
                })
    output = PROV / "evidencia-formes.tsv"
    fields = ["categoria", "forma", "id_persona", "ocurrencia", "snippet", "font", "estat"]
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    changed = 0
    for person, evidence in report_data.items():
        path = ROOT / "persones" / f"{person}.md"
        text = path.read_text(encoding="utf-8")
        if "### Evidència textual localitzable" in text:
            continue
        section = [
            "### Evidència textual localitzable",
            "",
            f"`../proveniencia/evidencia-formes.tsv` conserva **{sum(item[2] for item in evidence)} fragments** ASR per a aquesta veu. Són contextos per localitzar al WAV; no són transcripció validada.",
            "",
        ]
        for category, form, count, sample in evidence[:12]:
            section.append(f"- **{form}** ({category}, {count} fragments): «{sample}»")
        if len(evidence) > 12:
            section.append(f"- ... i {len(evidence) - 12} formes més; consultar la taula completa.")
        section.extend(["", ""])
        marker = "### Perfil lingüístic automatitzat\n\n"
        if marker in text:
            text = text.replace(marker, "\n".join(section) + marker, 1)
            path.write_text(text, encoding="utf-8")
            changed += 1
    print(f"{len(rows)} evidències · {len(report_data)} persones · informes actualitzats: {changed}")


if __name__ == "__main__":
    main()
