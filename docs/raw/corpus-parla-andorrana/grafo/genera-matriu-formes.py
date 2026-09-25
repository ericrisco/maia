"""Construeix una matriu persona-forma amb recompte ASR i QA de clip."""

from pathlib import Path
import csv
import re
import unicodedata

ROOT = Path(__file__).parents[1]


def norm(value: str) -> str:
    value = unicodedata.normalize("NFD", value.lower())
    return "".join(ch for ch in value if unicodedata.category(ch) != "Mn")


def count_form(text: str, form: str) -> int:
    return len(re.findall(r"(?<!\w)" + re.escape(norm(form)) + r"(?!\w)", norm(text)))


def read(path: Path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    people = [r["id_persona"] for r in read(ROOT / "persones.tsv")]
    traits = read(ROOT / "grafo" / "trets-linguistics.tsv")
    qa_rows = read(ROOT / "proveniencia" / "qa-clips.tsv")
    qa = {(r["id_persona"], r["forma"]): r for r in qa_rows}
    texts = {
        person: (ROOT / "transcripcions" / f"{person}.txt").read_text(encoding="utf-8", errors="replace")
        for person in people
    }
    rows = []
    for person in people:
        for trait in traits:
            form = trait["forma"]
            search_form = form.split("=", 1)[1] if "=" in form else form
            count = count_form(texts[person], search_form)
            q = qa.get((person, form))
            rows.append({
                "id_persona": person,
                "categoria": trait["categoria"],
                "forma": form,
                "recompte_asr": str(count),
                "clip_qa": q["clip"] if q else "",
                "forma_en_qa": q["forma_en_qa"] if q else "no-clip",
                "estat": "ASR; pendent d'audicio",
            })
    output = ROOT / "grafo" / "matriu-formes-linguistics.tsv"
    fields = list(rows[0])
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} files · {output}")


if __name__ == "__main__":
    main()
