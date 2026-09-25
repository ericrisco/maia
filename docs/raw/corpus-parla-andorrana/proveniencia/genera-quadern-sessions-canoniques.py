"""Genera el quadern Markdown de les sessions canòniques 01–02 i 05."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = PROV / "quadern-sessions-canoniques.md"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def clean(value: str) -> str:
    return (value or "").replace("\n", " ").replace("|", "\\|").strip()


def main() -> None:
    guide = {row["id_global"]: row for row in read(PROV / "guia-audicio-sessions-canoniques.tsv")}
    rows = []
    for name in ("sessio-01.tsv", "sessio-02.tsv", "sessio-05.tsv", "sessio-06.tsv"):
        for row in read(PROV / "sessions" / name):
            if row.get("origen") != "canònic":
                continue
            item = dict(row)
            item["sessio"] = name.removesuffix(".tsv")
            rows.append(item)
    lines = [
        "# Quadern d'audició — sessions canòniques 01–02, 05 i 06",
        "",
        f"La cua conté **{len(rows)} clips** canònics. Cada entrada conserva el WAV, els dos textos ASR i una guia de revisió. La transcripció automàtica i les mesures acústiques només orienten l'escolta.",
        "",
        "## Criteri d'anotació",
        "",
        "Confirma primer la veu i després la forma. Per a cada clip, registra decisió (`sí`, `no` o `incerta`), variant escoltada, trets fonètics, prosòdia i una nota justificativa. Projecta les anotacions amb `importa-auditoria-sessions-canoniques.py` només després de revisar-les.",
        "",
    ]
    for index, row in enumerate(rows, 1):
        g = guide.get(row["id_global"], {})
        lines.extend(
            [
                f"## {index}. {row['sessio']} — {row['persona']} — {row['forma']}",
                "",
                f"- Clip: [`{row['clip']}`]({row['clip']})",
                f"- Prioritat: `{row['prioritat']}` · probabilitat mínima: `{row['prob_min']}`",
                f"- Guia: {clean(g.get('guia_observacio', 'confirmar forma, variant i prosòdia'))}",
                f"- ASR small: {clean(row.get('text_small', ''))}",
                f"- ASR base: {clean(row.get('text_base', ''))}",
                f"- Mesures: F0 `{clean(row.get('f0_median_hz', ''))}` Hz; pausa `{clean(row.get('pausa_mediana_s', ''))}` s; F1/F2/F3 `{clean(row.get('f1_hz', ''))}`/`{clean(row.get('f2_hz', ''))}`/`{clean(row.get('f3_hz', ''))}` Hz.",
                "- Veu: `pendent` · decisió: `pendent`",
                "- Variant escoltada: _pendent_",
                "- Trets fonètics: _pendent_",
                "- Prosòdia i pauses: _pendent_",
                "- Nota: _pendent d'audició_",
                "",
            ]
        )
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"{len(rows)} clips")


if __name__ == "__main__":
    main()
