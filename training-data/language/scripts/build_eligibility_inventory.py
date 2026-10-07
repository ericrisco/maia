#!/usr/bin/env python3
"""Inventory Maia oral-language documents and summarize eligibility evidence."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PARLA = ROOT / "docs" / "parla"
FONTS = ROOT / "docs" / "fonts"
TRAINING = ROOT / "training-data" / "language"
INVENTORY = TRAINING / "work" / "eligibility-inventory.json"
REPORT = TRAINING / "reports" / "eligibility.md"
ARI_CC_BY_VERIFIED_IDS = {34, 49, 56, 57, 60, 65}


def metadata(text: str) -> dict[str, str]:
    match = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.S)
    if not match:
        return {}
    result: dict[str, str] = {}
    for line in match.group(1).splitlines():
        item = re.match(r"^([\w-]+):\s*(.*?)\s*$", line)
        if item:
            result[item.group(1)] = item.group(2).strip().strip("\"'")
    return result


def main() -> None:
    records: list[dict[str, object]] = []
    for path in sorted(PARLA.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        meta = metadata(text)
        if meta.get("type") != "parla":
            continue
        font_id = meta.get("font", "")
        font_path = FONTS / f"{font_id}.md"
        font_meta = metadata(font_path.read_text(encoding="utf-8")) if font_path.exists() else {}
        capsule_match = re.search(r"Càpsula\s+#(\d+)", text, re.I)
        capsule_id = int(capsule_match.group(1)) if capsule_match else None
        timed_segments = len(re.findall(r"^\[\d{2}:\d{2}:\d{2}(?:\.\d+)?\s+-->", text, re.M))
        uncertain_markers = len(re.findall(r"\[\?", text))
        records.append({
            "path": path.relative_to(ROOT).as_posix(),
            "title": meta.get("title", path.stem),
            "apte_llengua": meta.get("apte_llengua", "").lower() == "true",
            "font_id": font_id,
            "font_redistribution": font_meta.get("redistribucio", "unknown"),
            "font_license": font_meta.get("llicencia", "unknown"),
            "capsule_id": capsule_id,
            "ari_piece_cc_by_verified_in_source_record": capsule_id in ARI_CC_BY_VERIFIED_IDS,
            "timed_segments": timed_segments,
            "uncertainty_markers": uncertain_markers,
            "transcript_tagged_unverified": "transcripcio-no-verificada" in meta.get("tags", ""),
        })

    INVENTORY.parent.mkdir(parents=True, exist_ok=True)
    INVENTORY.write_text(json.dumps({"pieces": records}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    eligible = [r for r in records if r["apte_llengua"]]
    by_font = Counter(str(r["font_id"]) for r in eligible)
    lines = [
        "# Elegibilitat inicial de Maia Language",
        "",
        "Informe generat amb `scripts/build_eligibility_inventory.py` a partir de `docs/parla/` i els registres de `docs/fonts/`.",
        "Aquesta és una auditoria documental, no una aprovació per entrenar.",
        "",
        "## Estat",
        "",
        f"- Fitxes `type: parla`: **{len(records)}**.",
        f"- Marcades `apte_llengua: true`: **{len(eligible)}**.",
        f"- Marcades no aptes: **{len(records) - len(eligible)}**.",
        "- Cap fitxa `apte_llengua: true` té ara permís global confirmat al registre de font.",
        "- A les càpsules AR+I, el registre només confirma CC BY per a peces individuals #34, #49, #56, #57, #60 i #65; cal comprovar quina fitxa correspon a cada vídeo i validar-ne la transcripció i el parlant.",
        "- Les entrevistes del Consell General tenen llicència estàndard de YouTube; les preguntes de l'entrevistador s'han eliminat de les transcripcions.",
        "",
        "## Candidates per font",
        "",
        "| Font | Peces marcades aptes | Estat de redistribució del registre |",
        "|---|---:|---|",
    ]
    for font_id, count in sorted(by_font.items()):
        exemplar = next(r for r in eligible if r["font_id"] == font_id)
        lines.append(f"| `{font_id}` | {count} | `{exemplar['font_redistribution']}` |")
    lines += [
        "",
        "## Decisions necessàries abans de crear registres",
        "",
        "1. Comprovar els drets de cada peça i de cada transcripció. Un permís d'un vídeo no cobreix tota una sèrie.",
        "2. Confirmar que cada parlant i cada text representen català andorrà contemporani, en lloc d'inferir-ho del lloc de publicació.",
        "3. Revisar els fragments marcats amb `[?]`; aquests són propostes automàtiques de transcripció i no es poden tractar com a parla verificada.",
        "4. Fer servir només torns humans que es conservin a la font. Les entrevistes sense preguntes ni monòlegs no es convertiran en diàlegs de xat inventats.",
        "",
        "## Inventari per peça",
        "",
        "| Peça | Apta segons corpus | Font | Vídeo AR+I | Segments temporitzats | Marques `[?]` | Drets per peça confirmats al registre |",
        "|---|---|---|---:|---:|---:|---|",
    ]
    for item in records:
        capsule = item["capsule_id"] if item["capsule_id"] is not None else "—"
        confirmed = "sí, cal verificar peça" if item["ari_piece_cc_by_verified_in_source_record"] else "no / pendent"
        lines.append(
            f"| `{item['path']}` | {'sí' if item['apte_llengua'] else 'no'} | `{item['font_id']}` | {capsule} | {item['timed_segments']} | {item['uncertainty_markers']} | {confirmed} |"
        )
    lines += ["", "El manifest detallat queda a `work/eligibility-inventory.json` (ignorat per Git).", ""]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {INVENTORY.relative_to(ROOT)}")
    print(f"Wrote {REPORT.relative_to(ROOT)}")
    print(f"Pieces: {len(records)}; marked eligible: {len(eligible)}; sources: {dict(by_font)}")


if __name__ == "__main__":
    main()
