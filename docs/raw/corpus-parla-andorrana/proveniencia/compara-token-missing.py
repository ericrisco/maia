"""Compara la tokenització base i small dels 14 casos prioritaris."""

from __future__ import annotations

from pathlib import Path
import csv

PROV = Path(__file__).parent
OUT = PROV / "qa-token-missing-comparativa.tsv"
MARKER = "## Contraste tokenitzat independent"


def read(name: str) -> list[dict[str, str]]:
    with (PROV / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    base = {(r["id_persona"], r["forma"]): r for r in read("qa-consens-tokens-base.tsv")}
    small = {(r["id_persona"], r["forma"]): r for r in read("qa-token-missing-small.tsv")}
    rows = []
    for key, b in sorted(base.items()):
        if key not in small:
            continue
        s = small[key]
        rows.append({
            "id_persona": b["id_persona"], "forma": b["forma"], "interval_escolta": b["interval_escolta"],
            "clip": b["clip"], "base_token_match": b["token_match"], "small_token_match": s["token_match_small"],
            "small_token_texts": s["token_texts_small"], "base_token_matches": b["token_matches"],
        })
    fields = list(rows[0]) if rows else ["id_persona", "forma", "interval_escolta", "clip", "base_token_match", "small_token_match", "small_token_texts", "base_token_matches"]
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    report = PROV / "informe-token-missing.md"
    text = report.read_text(encoding="utf-8")
    if MARKER in text:
        text = text[: text.index(MARKER)].rstrip() + "\n"
    small_yes = [row for row in rows if row["small_token_match"] == "sí"]
    both_no = [row for row in rows if row["small_token_match"] == "no"]
    lines = [
        f"\n{MARKER}\n",
        f"Una segunda tokenització amb `ggml-small.bin` localitza **{len(small_yes)}** de les 14 formes "
        f"que `ggml-base.bin` no havia alineat; **{len(both_no)}** continuen sense token en cap dels dos JSON. "
        "Això separa una possible diferència de tokenitzador d'una incidència persistent, però no resol la "
        "pronúncia sense escolta.\n",
        "Casos recuperats pel small: " + "; ".join(f"{r['id_persona']} {r['forma']}" for r in small_yes) + ".\n",
        "Casos sense token en tots dos: " + "; ".join(f"{r['id_persona']} {r['forma']}" for r in both_no) + ".\n",
        f"La taula completa és `{OUT.name}`.\n",
    ]
    report.write_text(text + "\n".join(lines), encoding="utf-8")
    print(f"{len(rows)} casos comparats · small recupera {len(small_yes)} · persistents {len(both_no)}")


if __name__ == "__main__":
    main()
