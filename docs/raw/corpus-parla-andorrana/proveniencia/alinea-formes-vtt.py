"""Associa formes candidates amb segments temporals de les VTT."""

from pathlib import Path
import csv
import re
import unicodedata

ROOT = Path(__file__).parents[1]


def norm(value: str) -> str:
    value = unicodedata.normalize("NFD", value.lower())
    return "".join(ch for ch in value if unicodedata.category(ch) != "Mn")


def seconds(value: str) -> float:
    h, m, rest = value.split(":")
    s, ms = rest.split(".")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def parse_vtt(path: Path):
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    segments = []
    index = 0
    while index < len(lines):
        line = lines[index].strip()
        if " --> " not in line:
            index += 1
            continue
        left, right = line.split(" --> ", 1)
        text_lines = []
        index += 1
        while index < len(lines) and lines[index].strip():
            text_lines.append(lines[index].strip())
            index += 1
        text = re.sub(r"\s+", " ", " ".join(text_lines)).strip()
        segments.append((seconds(left), seconds(right.split()[0]), text))
    return segments


def main() -> None:
    with (ROOT / "persones.tsv").open(encoding="utf-8", newline="") as handle:
        people = [r["id_persona"] for r in csv.DictReader(handle, delimiter="\t")]
    with (ROOT / "grafo" / "trets-linguistics.tsv").open(encoding="utf-8", newline="") as handle:
        traits = list(csv.DictReader(handle, delimiter="\t"))
    rows = []
    for person in people:
        segments = parse_vtt(ROOT / "transcripcions" / f"{person}.vtt")
        for trait in traits:
            target = norm(trait["forma"])
            found = 0
            for start, end, text in segments:
                count = len(re.findall(r"(?<!\w)" + re.escape(target) + r"(?!\w)", norm(text)))
                for _ in range(count):
                    found += 1
                    if found > 8:
                        break
                    rows.append({
                        "categoria": trait["categoria"],
                        "forma": trait["forma"],
                        "id_persona": person,
                        "ocurrencia": str(found),
                        "start_s": f"{start:.3f}",
                        "end_s": f"{end:.3f}",
                        "interval_vtt": f"{start:.3f}-{end:.3f}",
                        "text_segment": text,
                        "font": f"transcripcions/{person}.vtt",
                        "estat": "ASR temporal; pendent d'audicio",
                    })
                if found >= 8:
                    break
    output = ROOT / "proveniencia" / "evidencia-formes-vtt.tsv"
    fields = list(rows[0])
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} evidències VTT · {output}")


if __name__ == "__main__":
    main()
