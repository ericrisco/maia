"""Prepara un expedient de prospecció RTVA fora del cànon.

La font té dues veus (entrevistador i convidat), de manera que cap clip es
projecta al registre canònic fins a una revisió d'atribució i d'escolta.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from collections import Counter
from datetime import date
from pathlib import Path


ROOT = Path(__file__).parent
ASR = ROOT / "asr"
CLIPS = ROOT / "clips"
SMALL = json.loads((ASR / "isidre-bartumeu-nocontext.json").read_text(encoding="utf-8"))
BASE = json.loads((ASR / "isidre-bartumeu-base-nocontext.json").read_text(encoding="utf-8"))
FORMS_SOURCE = Path(__file__).parents[2] / "candidats/lead-rtva-008-mireia-pedescoll/formes-consens.tsv"


def rows(data):
    return data.get("transcription", [])


def plain(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"\[_[^]]+\]", "", text)).strip()


def count(text: str, form: str) -> int:
    return len(re.findall(r"(?i)(?<!\w)" + re.escape(form) + r"(?!\w)", text))


def first_hit(data, form):
    for seg in rows(data):
        text = plain(seg.get("text", ""))
        if re.search(r"(?i)(?<!\w)" + re.escape(form) + r"(?!\w)", text):
            return seg, text
    return None, ""


def segment_confidence(seg):
    values = [float(token["p"]) for token in seg.get("tokens", []) if token.get("p") is not None and not str(token.get("text", "")).startswith("[_")]
    return (min(values), sum(values) / len(values)) if values else ("", "")


def main():
    CLIPS.mkdir(exist_ok=True)
    small_text = " ".join(plain(s.get("text", "")) for s in rows(SMALL))
    base_text = " ".join(plain(s.get("text", "")) for s in rows(BASE))
    with FORMS_SOURCE.open(encoding="utf-8", newline="") as handle:
        forms = list(csv.DictReader(handle, delimiter="\t"))

    form_rows = []
    queue_rows = []
    for idx, form_row in enumerate(forms, 1):
        form = form_row["forma"]
        seg, text = first_hit(SMALL, form)
        model = "small"
        small_context = text
        small_conf_min, small_conf_mean = segment_confidence(seg) if seg else ("", "")
        if seg is None:
            seg, text = first_hit(BASE, form)
            model = "base" if seg is not None else ""
        base_seg, base_context = first_hit(BASE, form)
        base_conf_min, base_conf_mean = segment_confidence(base_seg) if base_seg else ("", "")
        clip_name = ""
        start_ms = end_ms = ""
        if seg is not None:
            start_ms = int(seg["offsets"]["from"])
            end_ms = int(seg["offsets"]["to"])
            clip_start = max(0, start_ms - 2000)
            clip_end = end_ms + 2000
            clip_name = f"lead-rtva-009__{idx:02d}__{re.sub(r'[^a-z0-9]+', '-', form.lower()).strip('-')}.wav"
            out = CLIPS / clip_name
            if not out.exists():
                source = ROOT / "audio.wav"
                subprocess.run(
                    ["ffmpeg", "-y", "-ss", f"{clip_start/1000:.3f}", "-i", str(source),
                     "-t", f"{(clip_end-clip_start)/1000:.3f}", "-ac", "1", "-ar", "16000",
                     "-c:a", "pcm_s16le", str(out), "-loglevel", "error"],
                    check=True,
                )
        small_n = count(small_text, form)
        base_n = count(base_text, form)
        form_rows.append({
            "forma": form,
            "categoria": form_row.get("categoria", ""),
            "small": str(small_n),
            "base": str(base_n),
            "consens": "sí" if small_n and base_n else "no",
            "model_localitzador": model,
            "context_small": small_context,
            "context_base": base_context,
            "prob_min_segment_small": f"{small_conf_min:.4f}" if isinstance(small_conf_min, float) else "",
            "prob_mean_segment_small": f"{small_conf_mean:.4f}" if isinstance(small_conf_mean, float) else "",
            "prob_min_segment_base": f"{base_conf_min:.4f}" if isinstance(base_conf_min, float) else "",
            "prob_mean_segment_base": f"{base_conf_mean:.4f}" if isinstance(base_conf_mean, float) else "",
            "clip": clip_name,
            "inici_ms": str(start_ms),
            "final_ms": str(end_ms),
            "estat": "ASR textual; atribució i audició pendents",
        })
        if clip_name:
            queue_rows.append({
                "candidate": "lead-rtva-009-isidre-bartumeu",
                "forma": form,
                "clip": f"clips/{clip_name}",
                "veu_confirmada": "pendent",
                "forma_confirmada": "pendent",
                "variant_transcrita": "pendent",
                "trets_fonetics": "pendent",
                "prosodia": "pendent",
                "nota_audicio": "pendent",
                "estat_audicio": "pendent",
            })

    def write_tsv(path, data, fields):
        with path.open("w", encoding="utf-8", newline="") as handle:
            w = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
            w.writeheader()
            w.writerows(data)

    form_fields = list(form_rows[0])
    write_tsv(ROOT / "formes.tsv", form_rows, form_fields)
    queue_fields = list(queue_rows[0]) if queue_rows else ["candidate", "forma", "clip", "veu_confirmada", "forma_confirmada", "variant_transcrita", "trets_fonetica", "prosodia", "nota_audicio", "estat_audicio"]
    write_tsv(ROOT / "cua-audicio.tsv", queue_rows, queue_fields)

    source_files = ["source-page.html", "legal-page.html", "source-original.mp4", "audio.wav"]
    hashes = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in source_files}
    info = {
        "id_candidat": "lead-rtva-009-isidre-bartumeu",
        "nom_public": "Isidre Bartumeu Martínez",
        "font": "RTVA — El Camí de la Vida, capítol 23",
        "url": "https://www.rtva.ad/programes/capitol-23-isidre-bartumeu-el-cami-de-la-vida",
        "stream_url": "https://vodov.rtva.hiway.media/vod/1548022/hls/manifest.m3u8?t=",
        "data_publicacio": "2025-11-13",
        "data_consulta": str(date.today()),
        "durada_s": 2930.40475,
        "language": "ca-AD",
        "access_type": "free",
        "terms": "RTVA: els continguts estan subjectes a drets; ús local de recerca, sense redistribució",
        "voice_status": "pendent; entrevista amb entrevistador i convidat",
        "asr_small": "asr/isidre-bartumeu-nocontext.json",
        "asr_base": "asr/isidre-bartumeu-base-nocontext.json",
        "first_pass_issue": "asr/isidre-bartumeu.json mostra repetició i offsets incoherents; es conserva però no és la passada principal",
        "hashes": hashes,
    }
    (ROOT / "source.info.json").write_text(json.dumps(info, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def stats(data):
        segs = rows(data)
        return len(segs), (segs[-1]["offsets"]["to"] if segs else 0)

    ss, sd = stats(SMALL)
    bs, bd = stats(BASE)
    low = [t for seg in rows(SMALL) for t in seg.get("tokens", []) if t.get("p", 1) < 0.55 and re.search(r"\w", t.get("text", ""))]
    repeated = sum(1 for a, b in zip(rows(SMALL), rows(SMALL)[1:]) if plain(a.get("text", "")) == plain(b.get("text", "")) and plain(a.get("text", "")))
    top = Counter(re.findall(r"\b[\wàèéíòóúïüç']+\b", small_text.lower())).most_common(20)
    top_text = ", ".join(f"{w} ({n})" for w, n in top)
    acoustic = []
    acoustic_path = ROOT / "analisi-acustica.tsv"
    if acoustic_path.exists():
        with acoustic_path.open(encoding="utf-8", newline="") as handle:
            acoustic = list(csv.DictReader(handle, delimiter="\t"))
    acoustic_summary = ""
    if acoustic:
        rms = [float(r["rms_db"]) for r in acoustic if r.get("rms_db")]
        f0 = [float(r["f0_median_hz"]) for r in acoustic if r.get("f0_median_hz")]
        active = [float(r["veu_activa"]) for r in acoustic if r.get("veu_activa")]
        acoustic_summary = (
            f"`analisi-acustica.tsv` conserva descriptors dels {len(acoustic)} clips "
            f"(RMS mediana {min(rms):.1f}–{max(rms):.1f} dB, F0 mediana "
            f"{min(f0):.1f}–{max(f0):.1f} Hz, activitat de veu {min(active):.2f}–{max(active):.2f}). "
            "Són mesures instrumentals per ordenar l'escolta, no trets fonètics confirmats.\n\n"
        )
    (ROOT / "informe.md").write_text(f"""# Expedient de prospecció — Isidre Bartumeu Martínez

## Estat

`lead-rtva-009-isidre-bartumeu` és una font candidata fora del recompte canònic
i fora dels grafs canònics. La pàgina de RTVA presenta Isidre Bartumeu com a
notari amb trajectòria professional al país i l'entrevista és en català. La
font conté com a mínim dos torns de veu; per això els clips no s'atribueixen al
convidat fins a l'audició.

## Procedència i fitxers

- Font: [RTVA — capítol 23 d'El Camí de la Vida](https://www.rtva.ad/programes/capitol-23-isidre-bartumeu-el-cami-de-la-vida).
- Pàgina conservada: `source-page.html`; termes: `legal-page.html`.
- Flux original local: `source-original.mp4` (només recerca local).
- WAV de treball: `audio.wav`, mono, 16 kHz, 2.930,40 s.
- Hashes i metadades: `source.info.json`.

## Transcripcions

La passada principal és `asr/isidre-bartumeu-nocontext.*` (small, català,
sense context acumulat): {ss} segments fins a {sd/1000:.2f} s. La passada
independent `asr/isidre-bartumeu-base-nocontext.*` té {bs} segments fins a
{bd/1000:.2f} s. La primera passada amb context (`asr/isidre-bartumeu.*`) es
conserva com a incidència: entra en repetició i produeix offsets de tokens
incoherents a partir d'una part de l'entrevista, de manera que no s'utilitza
com a text principal.

La passada small conté {len(low)} tokens amb probabilitat inferior a 0,55 i
{repeated} repeticions consecutives exactes. El text i la forma s'han de
contrastar amb l'àudio.

## Inventari i anàlisi provisional

`formes.tsv` conserva les 35 formes candidates amb recompte independent small i
base. `clips/` conté {len(queue_rows)} clips locals, un per forma localitzada;
`cua-audicio.tsv` manté veu, variant, fonètica, prosòdia i nota en `pendent`.

{acoustic_summary} 

Seqüències lèxiques més repetides en la passada small (no són trets dialectals):
{top_text}

No es publica cap tret fonètic, prosòdic ni dialectal com a confirmat. La font
és una entrevista institucional i els marcadors poden pertànyer a
l'entrevistador o al convidat. Qualsevol incorporació al corpus canònic exigirà
atribució de veu, revisió dels termes d'ús i escolta clip per clip.
""", encoding="utf-8")

    print(f"OK dossier Isidre: {len(form_rows)} formes · {len(queue_rows)} clips · {ss}/{bs} segments small/base")


if __name__ == "__main__":
    main()
