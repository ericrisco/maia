"""Resumeix i prepara l'audició del candidat RTVA Ian Moya."""

from __future__ import annotations

import csv
import difflib
import hashlib
import html
import json
import re
import wave
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).parents[1]
CAND = ROOT / "proveniencia" / "candidats" / "lead-rtva-002-ian-moya"
SMALL = CAND / "asr" / "ian-moya.json"
BASE = CAND / "asr" / "ian-moya-base.json"
FORM_MATRIX = ROOT / "grafo" / "matriu-formes.tsv"
WORD = re.compile(r"[^\W_]+(?:['’][^\W_]+)?", re.UNICODE)


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def seconds(value: str) -> float:
    hours, minutes, raw = value.replace(",", ".").split(":")
    return int(hours) * 3600 + int(minutes) * 60 + float(raw)


def match(text: str, form: str) -> bool:
    return re.search(rf"(?<![\wà-ÿ]){re.escape(form)}(?![\wà-ÿ])", text, re.IGNORECASE) is not None


def model_rows(path: Path, model: str, forms: list[tuple[str, str]]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    occurrences: list[dict[str, object]] = []
    segments: list[dict[str, object]] = []
    for number, segment in enumerate(data.get("transcription", []), start=1):
        text = segment.get("text", "").strip()
        if not text or text == "#":
            continue
        start = seconds(segment["timestamps"]["from"])
        end = seconds(segment["timestamps"]["to"])
        probs = [
            float(token.get("p", 0))
            for token in segment.get("tokens", [])
            if not str(token.get("text", "")).startswith("[_")
        ]
        pmin = min(probs) if probs else 0.0
        segments.append({"model": model, "segment": number, "start": start, "end": end, "text": text, "pmin": pmin})
        for category, form in forms:
            if match(text, form):
                occurrences.append({
                    "model": model,
                    "categoria": category,
                    "forma": form,
                    "segment": number,
                    "inici_s": f"{start:.3f}",
                    "final_s": f"{end:.3f}",
                    "prob_min_segment": f"{pmin:.4f}",
                    "text_asr": text,
                    "estat": "candidat ASR; pendent d'audició",
                })
    return occurrences, segments


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def write_auditor(rows: list[dict[str, str]]) -> None:
    items = [
        {
            "id": f"{row['forma']}::{row['segment']}",
            "form": row["forma"],
            "segment": row["segment"],
            "clip": row["clip"],
            "start": row["inici_clip_s"],
            "end": row["final_clip_s"],
            "small": row["small"],
            "base": row["base"],
        }
        for row in rows
    ]
    payload = json.dumps(items, ensure_ascii=False).replace("</", "<\\/")
    title = "Audició — candidat RTVA Ian Moya"
    key = "maia-candidat-ian-moya-audicio-v1"
    download = "anotacions-ian-moya.tsv"
    doc = f'''<!doctype html><html lang="ca"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>body{{font:16px system-ui,sans-serif;max-width:980px;margin:2rem auto;padding:0 1rem;color:#222}}label{{display:block;margin:.7rem 0}}select,input,textarea,button{{font:inherit;padding:.4rem}}textarea{{width:100%;min-height:4rem}}audio{{width:100%;margin:1rem 0}}.meta{{background:#f3f3f3;padding:.8rem;border-radius:.4rem}}.warn{{background:#fff4ce;padding:.6rem;border-radius:.4rem}}.progress{{float:right;color:#666}}</style></head><body><h1>{html.escape(title)} <span class="progress" id="progress"></span></h1><p>{len(rows)} clips representatius de formes candidates. Les anotacions es guarden localment al navegador i es poden descarregar com a TSV.</p><p><button id="prev">Anterior</button> <button id="next">Següent</button> <button id="download">Descarrega TSV</button></p><main id="app"></main><script>const items={payload};const key='{key}';let notes=JSON.parse(localStorage.getItem(key)||'{{}}'),index=0;const app=document.querySelector('#app');function render(){{const x=items[index];const n=notes[x.id]||{{}};document.querySelector('#progress').textContent=`${{index+1}}/${{items.length}}`;app.innerHTML=`<h2>${{x.form}}</h2><div class="meta"><p><b>Segment:</b> ${{x.segment}} · <b>Clip:</b> <code>${{x.clip}}</code></p><p><b>Finestra:</b> ${{x.start}}–${{x.end}} s · <b>small:</b> ${{x.small}} · <b>base:</b> ${{x.base}}</p></div><audio controls preload="metadata" src="${{x.clip}}"></audio><p class="warn">La forma ASR és una hipòtesi. Indica si la veu és d'Ian, de la persona entrevistadora o incerta abans d'anotar la variant.</p><label>Veu<select id="speaker"><option>pendent</option><option>ian</option><option>entrevistador</option><option>mixt</option><option>incerta</option></select></label><label>Decisió de la forma<select id="decision"><option>pendent</option><option>sí</option><option>no</option><option>incerta</option></select></label><label>Variant escoltada<input id="variant"></label><label>Trets fonètics<textarea id="phon"></textarea></label><label>Prosòdia / pauses<textarea id="pros"></textarea></label><label>Nota<textarea id="note"></textarea></label>`;for(const [id,k] of [['speaker','speaker'],['decision','decision'],['variant','variant'],['phon','phon'],['pros','pros'],['note','note']]){{const el=document.querySelector('#'+id);el.value=n[k]||'';el.addEventListener('input',()=>save(x))}}}}function save(x){{notes[x.id]={{speaker:document.querySelector('#speaker').value,decision:document.querySelector('#decision').value,variant:document.querySelector('#variant').value,phon:document.querySelector('#phon').value,pros:document.querySelector('#pros').value,note:document.querySelector('#note').value}};localStorage.setItem(key,JSON.stringify(notes))}}document.querySelector('#prev').onclick=()=>{{index=Math.max(0,index-1);render()}};document.querySelector('#next').onclick=()=>{{index=Math.min(items.length-1,index+1);render()}};document.querySelector('#download').onclick=()=>{{const h=['id','forma','segment','clip','speaker','decision','variant','phon','pros','note'];const lines=[h.join('\\t')];for(const x of items){{const n=notes[x.id]||{{}};lines.push([x.id,x.form,x.segment,x.clip,n.speaker||'pendent',n.decision||'pendent',n.variant||'',n.phon||'',n.pros||'',n.note||''].map(v=>String(v).replace(/[\\t\\n]/g,' ')).join('\\t'))}}const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([lines.join('\\n')],{{type:'text/tab-separated-values'}}));a.download='{download}';a.click()}};render();</script></body></html>'''
    (CAND / "auditoria.html").write_text(doc, encoding="utf-8")


def main() -> None:
    forms = []
    seen = set()
    for row in read(FORM_MATRIX):
        key = (row["categoria"], row["forma"])
        if key not in seen:
            forms.append(key)
            seen.add(key)
    small_occ, small_segments = model_rows(SMALL, "small", forms)
    base_occ, base_segments = model_rows(BASE, "base", forms)
    all_occ = small_occ + base_occ
    with (CAND / "formes.tsv").open("w", encoding="utf-8", newline="") as handle:
        fields = list(all_occ[0])
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(all_occ)

    by_model_form = Counter((row["model"], row["forma"]) for row in all_occ)
    consensus_rows = []
    for category, form in forms:
        small = by_model_form[("small", form)]
        base = by_model_form[("base", form)]
        consensus_rows.append({"categoria": category, "forma": form, "small": small, "base": base, "consens": "sí" if small and base else "no", "estat": "ASR textual; pendent d'audició"})
    with (CAND / "formes-consens.tsv").open("w", encoding="utf-8", newline="") as handle:
        fields = list(consensus_rows[0])
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(consensus_rows)

    small_text = " ".join(str(row["text"]) for row in small_segments)
    base_text = " ".join(str(row["text"]) for row in base_segments)
    ratio = difflib.SequenceMatcher(None, small_text, base_text).ratio()
    (CAND / "comparacio-asr.md").write_text(
        f"""# Comparació ASR — Ian Moya

La passada `small` té **{len(small_segments)} segments** i la `base` **{len(base_segments)} segments**. La similitud textual global de les cadenes concatenades és **{ratio:.4f}**; la segmentació i els textos poden variar per la música, les pauses i els torns de ràdio.

| estat | formes |
|---|---:|
| presents en small i base | {sum(1 for row in consensus_rows if row['small'] and row['base'])} |
| només small | {sum(1 for row in consensus_rows if row['small'] and not row['base'])} |
| només base | {sum(1 for row in consensus_rows if row['base'] and not row['small'])} |
| cap model | {sum(1 for row in consensus_rows if not row['small'] and not row['base'])} |

Les coincidències són una priorització textual i no confirmen qui parla ni la realització fonètica.
""", encoding="utf-8")

    consensus_forms = [row["forma"] for row in consensus_rows if row["small"] and row["base"]]
    chosen = []
    for form in consensus_forms + [row["forma"] for row in consensus_rows if row["small"] and not row["base"]]:
        candidates = [row for row in small_occ if row["forma"] == form]
        if not candidates:
            candidates = [row for row in base_occ if row["forma"] == form]
        if candidates:
            chosen.append(candidates[0])
    clips_dir = CAND / "clips"
    clips_dir.mkdir(exist_ok=True)
    with wave.open(str(CAND / "audio.wav"), "rb") as source:
        params = source.getparams()
        frames = source.readframes(source.getnframes())
    max_frames = len(frames) // (params.sampwidth * params.nchannels)
    clip_rows = []
    for row in chosen:
        start = max(0.0, float(row["inici_s"]) - 1.0)
        end = min(max_frames / params.framerate, float(row["final_s"]) + 1.0)
        first = int(start * params.framerate) * params.sampwidth * params.nchannels
        last = int(end * params.framerate) * params.sampwidth * params.nchannels
        filename = f"ian__{slug(str(row['forma']))}__{float(row['inici_s']):.2f}.wav"
        with wave.open(str(clips_dir / filename), "wb") as target:
            target.setparams(params); target.writeframes(frames[first:last])
        counts = next(item for item in consensus_rows if item["forma"] == row["forma"])
        clip_rows.append({
            "forma": row["forma"], "segment": row["segment"], "inici_forma_s": row["inici_s"], "final_forma_s": row["final_s"],
            "clip": f"clips/{filename}", "inici_clip_s": f"{start:.3f}", "final_clip_s": f"{end:.3f}",
            "small": counts["small"], "base": counts["base"], "prioritat": "A-consens-ASR" if counts["small"] and counts["base"] else "B-un-model-ASR", "estat": "pendent d'audició",
        })
    with (CAND / "formes-clips.tsv").open("w", encoding="utf-8", newline="") as handle:
        fields = list(clip_rows[0]) if clip_rows else ["forma", "segment", "inici_forma_s", "final_forma_s", "clip", "inici_clip_s", "final_clip_s", "small", "base", "prioritat", "estat"]
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(clip_rows)
    (CAND / "quadern-clips-formes.md").write_text(
        "# Clips de formes — Ian Moya\n\n" + f"S'han extret **{len(clip_rows)} clips** representatius. La prioritat de doble ASR és textual i tots els camps humans continuen pendents.\n\n" + "\n".join(f"- `{row['forma']}` · `{row['clip']}` · small={row['small']} · base={row['base']} · {row['prioritat']}" for row in clip_rows) + "\n",
        encoding="utf-8",
    )
    write_auditor(clip_rows)

    tokens = [token.lower() for segment in small_segments for token in WORD.findall(str(segment["text"]))]
    marker_counts = Counter(row["forma"] for row in small_occ)
    territorial = Counter(token for token in tokens if token in {"andorra", "andorrà", "andorrana", "escaldes", "país", "català", "eufòria", "muntanya", "cançó", "parròquia"})
    duration = max((float(row["end"]) for row in small_segments), default=0.0)
    report_lines = [
        "# Candidat RTVA — Ian Moya", "",
        "Aquest expedient és independent del recompte canònic. La pàgina RTVA identifica Ian Moya com a d'Escaldes-Engordany, però l'àudio és una entrevista de ràdio amb torns alterns i encara no té diarització auditiva.", "",
        "## Procedència i derivats", "",
        "- Font: [RTVA — Entrevista a Ian Moya, Les coses grans (23/02/2026)](https://www.rtva.ad/programes/entrevista-a-l-ian-moya-el-primer-concursant-d-euforia-andorra-les-coses-grans-23-02-2026).",
        "- Actiu directe: la URL queda conservada a `source-url.txt`; el fitxer original és `audio-original.mp3`.",
        f"- Àudio WAV: `audio.wav`, {duration/60:.2f} minuts, SHA-256 `{sha256(CAND / 'audio.wav')}`.",
        f"- Àudio original MP3: SHA-256 `{sha256(CAND / 'audio-original.mp3')}`.",
        "- ASR: `whisper-cli`, models `ggml-small.bin` i `ggml-base.bin`, llengua `ca`, beam 5, 8 fils.",
        "- Termes: RTVA no declara una llicència oberta a la página; els derivats es conserven per a recerca local i no es redistribueix l'original.", "",
        "## Cobertura automàtica", "",
        f"- `small`: {len(small_segments)} segments i {len(tokens)} tokens aproximats; `base`: {len(base_segments)} segments.",
        f"- `formes.tsv`: {len(all_occ)} ocurrències de les 35 formes candidates entre els dos models; {sum(1 for row in consensus_rows if row['small'] and row['base'])} formes apareixen en ambdós.",
        f"- Marcadors small més freqüents: " + "; ".join(f"{form}={count}" for form, count in marker_counts.most_common(12)) + ".",
        f"- Lèxic territorial small localitzat: " + ("; ".join(f"{form}={count}" for form, count in territorial.items()) or "cap dels termes de control") + ".", "",
        "## Lectura lingüística provisional", "",
        "- El registre radiofònic combina la veu d'Ian amb la de la persona entrevistadora; cap forma es pot atribuir a Ian sense escolta i anotació de veu.",
        "- Els connectors i les formes territorials són candidats textuals; les grafies ASR no permeten decidir obertura vocàlica, consonants finals, prosòdia, clítics ni contacte lingüístic.",
        "- La baixa similitud entre les dues passades ASR s'ha conservat a `comparacio-asr.md` i justifica una revisió directa dels clips.", "",
        "## Revisió preparada", "",
        f"- `formes-clips.tsv`, `quadern-clips-formes.md` i `auditoria.html` preparen {len(clip_rows)} clips representatius.",
        "- El candidat no entra a `persones.tsv` ni als grafs canònics fins a confirmar la veu, la transcripció i els termes d'ús.", "",
        "## Buits registrats", "",
        "- No s'ha separat encara la veu d'Ian de l'entrevistador.",
        "- No hi ha decisions auditives, variants escoltades ni anotació fonètica/prosòdica.",
        "- La pàgina no declara una llicència oberta; l'ús es limita a recerca local.",
    ]
    (CAND / "informe.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    print(f"{len(small_segments)} small · {len(base_segments)} base · {len(all_occ)} ocurrències · {len(consensus_forms)} formes consensuals · {len(clip_rows)} clips")


if __name__ == "__main__":
    main()
