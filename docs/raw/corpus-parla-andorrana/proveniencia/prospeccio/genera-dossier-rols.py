"""Genera els inventaris de tres veus institucionals/històriques noves."""
from __future__ import annotations
import csv, hashlib, json, re, subprocess
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
FORMS = Path(__file__).parents[1] / "candidats/lead-rtva-008-mireia-pedescoll/formes-consens.tsv"
CASES = {
    "lead-rtva-059-carles-ensenyat": ("Carles Ensenyat", "carles-ensenyat", "Discurs del síndic general amb motiu del dia de Meritxell 2026", "https://www.rtva.ad/programes/discurs-del-sindic-general-amb-motiu-del-dia-de-meritxell-2026"),
    "lead-rtva-060-xavier-espot-actual": ("Xavier Espot", "xavier-espot-actual", "Declaracions del cap de Govern per Meritxell 2026", "https://www.rtva.ad/noticies/societat/ensenyat-apel-la-al-coratge-per-canviar-allo-que-ja-no-respon-al-present"),
    "lead-rtva-061-antoni-morell": ("Antoni Morell", "antoni-morell", "Entrevista a Antoni Morell al programa Identitats", "https://www.rtva.ad/noticies/societat/mor-antoni-morell-principals-referents-literatura-andorrana"),
}
EXTRA = {
    "carles-ensenyat": [("síndic general", "institucions"), ("Sindicatura", "institucions"), ("Consell General", "institucions"), ("Meritxell", "memòria"), ("habitatge", "societat"), ("avortament", "societat"), ("Europa", "institucions"), ("coprincipat", "institucions"), ("andorrà", "gentilici")],
    "xavier-espot-actual": [("cap de Govern", "institucions"), ("Govern", "institucions"), ("avortament", "societat"), ("Santa Seu", "institucions"), ("eleccions", "institucions"), ("Andorra", "toponim"), ("andorrà", "gentilici")],
    "antoni-morell": [("literatura andorrana", "cultura"), ("identitat andorrana", "memòria"), ("Sindicatura General", "institucions"), ("secretari general", "institucions"), ("ambaixador", "institucions"), ("Constitució", "institucions"), ("Andorra", "toponim"), ("andorrà", "gentilici")],
}

def plain(t): return re.sub(r"\s+", " ", re.sub(r"\[_[^]]+\]", "", t or "")).strip()
def rx(form): return re.compile(r"(?i)(?<!\w)" + re.escape(form) + r"(?!\w)")
def rows(d): return d.get("transcription", [])
def conf(seg):
    vals = [float(t["p"]) for t in (seg or {}).get("tokens", []) if t.get("p") is not None and not str(t.get("text", "")).startswith("[_")]
    return (min(vals), sum(vals) / len(vals)) if vals else ("", "")
def sha(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""): h.update(b)
    return h.hexdigest()

def process(lead, cfg):
    name, nick, title, source_url = cfg
    root = ROOT / lead; small = json.loads((root / "asr" / f"{nick}-small-nocontext.json").read_text()); base = json.loads((root / "asr" / f"{nick}-base-nocontext.json").read_text())
    small_text = " ".join(plain(s.get("text", "")) for s in rows(small)); base_text = " ".join(plain(s.get("text", "")) for s in rows(base))
    forms, seen = [], set()
    with FORMS.open(encoding="utf-8", newline="") as h:
        for r in csv.DictReader(h, delimiter="\t"):
            if r["forma"] not in seen: forms.append((r["forma"], r.get("categoria", ""))); seen.add(r["forma"])
    for f, c in EXTRA[nick]:
        if f not in seen: forms.append((f, c)); seen.add(f)
    def hit(data, form):
        for seg in rows(data):
            ctx = plain(seg.get("text", ""))
            if rx(form).search(ctx): return seg, ctx
        return None, ""
    form_rows, queue = [], []
    for idx, (form, cat) in enumerate(forms, 1):
        ss, sctx = hit(small, form); bs, bctx = hit(base, form); seg = ss or bs
        clip = ""; start = end = ""
        if seg:
            start, end = int(seg["offsets"]["from"]), int(seg["offsets"]["to"]); cs, ce = max(0, start - 2000), end + 2000
            slug = re.sub(r"[^a-z0-9]+", "-", form.lower()).strip("-") or f"forma-{idx}"
            clip = f"{lead}__{idx:02d}__{slug}.wav"; out = root / "clips" / clip
            if not out.exists(): subprocess.run(["ffmpeg", "-y", "-ss", f"{cs/1000:.3f}", "-i", str(root / "audio.wav"), "-t", f"{(ce-cs)/1000:.3f}", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(out), "-loglevel", "error"], check=True)
        scm, sme = conf(ss); bcm, bme = conf(bs)
        form_rows.append({"forma": form, "categoria": cat, "small": str(len(rx(form).findall(small_text))), "base": str(len(rx(form).findall(base_text))), "consens": "sí" if rx(form).search(small_text) and rx(form).search(base_text) else "no", "model_localitzador": "small" if ss else ("base" if bs else ""), "context_small": sctx, "context_base": bctx, "prob_min_segment_small": f"{scm:.4f}" if isinstance(scm, float) else "", "prob_mean_segment_small": f"{sme:.4f}" if isinstance(sme, float) else "", "prob_min_segment_base": f"{bcm:.4f}" if isinstance(bcm, float) else "", "prob_mean_segment_base": f"{bme:.4f}" if isinstance(bme, float) else "", "clip": clip, "inici_ms": str(start), "final_ms": str(end), "estat": "ASR textual; atribució i audició pendents"})
        if clip: queue.append({"candidate": lead, "forma": form, "clip": f"clips/{clip}", "veu_confirmada": "pendent", "forma_confirmada": "pendent", "variant_transcrita": "pendent", "trets_fonetica": "pendent", "prosodia": "pendent", "nota_audicio": "pendent", "estat_audicio": "pendent"})
    def write(path, rows_):
        with path.open("w", encoding="utf-8", newline="") as h:
            w = csv.DictWriter(h, fieldnames=list(rows_[0]), delimiter="\t"); w.writeheader(); w.writerows(rows_)
    write(root / "formes.tsv", form_rows); write(root / "cua-audicio.tsv", queue)
    info = json.loads((root / "source.info.json").read_text()); info.update({"data_consulta": str(date.today()), "forms_count": len(form_rows), "clips_count": len(queue), "hashes": {x: sha(root / x) for x in ["source-page.html", "legal-page.html", "source-original.mp4", "audio.wav"]}}); (root / "source.info.json").write_text(json.dumps(info, ensure_ascii=False, indent=2) + "\n")
    ss, bs = len(rows(small)), len(rows(base)); top = ", ".join(f"{w} ({n})" for w, n in Counter(re.findall(r"\b[\wàèéíòóúïüç']+\b", small_text.lower())).most_common(20))
    desc = {"carles-ensenyat": "discurs institucional del síndic general", "xavier-espot-actual": "declaracions del cap de Govern", "antoni-morell": "entrevista d'arxiu a un referent de la literatura andorrana"}[nick]
    (root / "informe.md").write_text(f"""# Expedient de prospecció — {name}\n\n## Estat\n\n`{lead}` és una font candidata fora del recompte i dels grafs canònics. RTVA conserva {desc}; la veu principal i l'atribució dels clips continuen pendents d'audició humana.\n\n## Procedència i fitxers\n\n- Font: [RTVA — {title}]({source_url}).\n- Pàgina conservada: `source-page.html`; termes: [`terms.md`](terms.md).\n- Flux original local: `source-original.mp4`; WAV: `audio.wav`.\n- Metadades i hashes: `source.info.json`.\n\n## Transcripcions i inventari provisional\n\nLes passades small i base sense context acumulat tenen {ss} i {bs} segments. `formes.tsv` conserva {len(form_rows)} formes i `clips/` {len(queue)} clips locals. Les sortides són ASR de treball i no confirmen trets dialectals, identitat ni nacionalitat.\n\nSeqüències més repetides a small: {top}\n\nLa incorporació al cànon exigeix atribució de veu clip per clip, escolta i revisió dels termes d'ús.\n""", encoding="utf-8")
    print(lead, len(form_rows), len(queue))

for lead, cfg in CASES.items(): process(lead, cfg)
