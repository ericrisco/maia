"""Construeix una cua curta d'escolta per a les veus en quarantena."""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
MANIFEST = PROV / "qa-quarantena-20s.tsv"
OUT_TSV = PROV / "cua-audicio-quarantena-20s.tsv"
OUT_HTML = PROV / "auditoria-quarantena-20s.html"
CONSENS = PROV / "qa-quarantena-20s-consens.tsv"
ACOUSTIC = PROV / "analisi-acustica-quarantena-20s.tsv"
PERSONES = ("pa-044", "pa-047", "pa-050")
PER_PERSONA = 5


def read() -> list[dict[str, str]]:
    with MANIFEST.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def choose(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    consens = {}
    if CONSENS.exists():
        with CONSENS.open(encoding="utf-8", newline="") as handle:
            consens = {(row["id_persona"], row["inici_s"]): row for row in csv.DictReader(handle, delimiter="\t")}
    acoustic = {}
    if ACOUSTIC.exists():
        with ACOUSTIC.open(encoding="utf-8", newline="") as handle:
            acoustic = {(row["id_persona"], row["inici_s"]): row for row in csv.DictReader(handle, delimiter="\t")}
    chosen: list[dict[str, str]] = []
    for person in PERSONES:
        candidates = [row for row in rows if row["id_persona"] == person]
        voiced = [row for row in candidates if float(acoustic.get((person, row["inici_s"]), {}).get("veu_proporcio", "1")) >= 0.2]
        if len(voiced) >= PER_PERSONA:
            candidates = voiced
        # First prefer non-repetitive windows, then spread the selected starts.
        candidates.sort(key=lambda row: (-float(consens.get((person, row["inici_s"]), {}).get("jaccard_tokens", "0")), -float(row["ratio_uniques"]), -float(acoustic.get((person, row["inici_s"]), {}).get("veu_proporcio", "0")), int(row["inici_s"])))
        selected: list[dict[str, str]] = []
        for row in candidates:
            if all(abs(int(row["inici_s"]) - int(other["inici_s"])) >= 60 for other in selected):
                selected.append(row)
            if len(selected) == PER_PERSONA:
                break
        if len(selected) < PER_PERSONA:
            for row in candidates:
                if row not in selected:
                    selected.append(row)
                if len(selected) == PER_PERSONA:
                    break
        for row in selected:
            comparison = consens.get((person, row["inici_s"]), {})
            for key in ("text_small", "consens_textual", "jaccard_tokens", "transcripcio_small"):
                row[f"_consens_{key}"] = comparison.get(key, "")
            measurement = acoustic.get((person, row["inici_s"]), {})
            for key in ("veu_proporcio", "f0_median_hz", "f0_iqr_hz", "pausa_mediana_s"):
                row[f"_acoustic_{key}"] = measurement.get(key, "")
        chosen.extend(sorted(selected, key=lambda row: int(row["inici_s"])))
    return chosen


def main() -> None:
    rows = choose(read())
    output: list[dict[str, str]] = []
    for index, row in enumerate(rows, start=1):
        text = (PROV / row["transcripcio"]).read_text(encoding="utf-8", errors="replace").strip().replace("\n", " ")
        output.append({
            "ordre": str(index),
            "id_persona": row["id_persona"],
            "inici_s": row["inici_s"],
            "durada_s": row["durada_s"],
            "clip": row["clip"],
            "transcripcio": row["transcripcio"],
            "ratio_uniques": row["ratio_uniques"],
            "text_qa": text,
            "text_small": row.get("_consens_text_small", ""),
            "jaccard_tokens": row.get("_consens_jaccard_tokens", ""),
            "consens_textual": row.get("_consens_consens_textual", ""),
            "veu_proporcio": row.get("_acoustic_veu_proporcio", ""),
            "f0_median_hz": row.get("_acoustic_f0_median_hz", ""),
            "f0_iqr_hz": row.get("_acoustic_f0_iqr_hz", ""),
            "pausa_mediana_s": row.get("_acoustic_pausa_mediana_s", ""),
            "veu": "pendent",
            "decisio": "pendent",
            "variant_transcrita": "",
            "trets_fonetics_observats": "",
            "observacions_prosodiques": "",
            "nota_audicio": "",
            "estat_audicio": "pendent",
        })
    fields = list(output[0])
    with OUT_TSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(output)
    payload = json.dumps(output, ensure_ascii=False).replace("</", "<\\/")
    title = "Auditoria de quarantena — finestres de 20 segons"
    html = f'''<!doctype html><html lang="ca"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>body{{font:16px system-ui,sans-serif;max-width:1000px;margin:2rem auto;padding:0 1rem;color:#222}}select,input,textarea,button{{font:inherit;padding:.4rem}}textarea{{width:100%;min-height:4rem}}audio{{width:100%;margin:1rem 0}}.meta{{background:#f3f3f3;padding:.8rem;border-radius:.4rem}}.warn{{background:#fff4ce;padding:.6rem;border-radius:.4rem}}.progress{{float:right;color:#666}}.filters{{display:flex;gap:.6rem;flex-wrap:wrap}}</style></head><body><h1>{title} <span class="progress" id="progress"></span></h1><p>{len(output)} clips, cinc per veu. Les anotacions es guarden al navegador; exporta el TSV quan acabis.</p><div class="filters"><label>Veu<select id="filter"><option value="totes">totes</option><option>pa-044</option><option>pa-047</option><option>pa-050</option></select></label><label>Només pendents<select id="pending"><option value="sí">sí</option><option value="no">no</option></select></label></div><p><button id="prev">Anterior</button> <button id="next">Següent</button> <button id="download">Descarrega TSV</button></p><main id="app"></main><script>const allItems={payload};const key='maia-auditoria-quarantena-20s-v1';let notes=JSON.parse(localStorage.getItem(key)||'{{}}'),index=0,view=[];const app=document.querySelector('#app'),filter=document.querySelector('#filter'),pending=document.querySelector('#pending');function refresh(){{view=allItems.filter(x=>(filter.value==='totes'||x.id_persona===filter.value)&&(pending.value==='no'||!notes[x.ordre]||!notes[x.ordre].decisio||notes[x.ordre].decisio==='pendent'));index=Math.min(index,Math.max(0,view.length-1));render()}}function render(){{if(!view.length){{app.innerHTML='<p>No hi ha clips amb aquests filtres.</p>';document.querySelector('#progress').textContent='0/0';return}}const x=view[index],n=notes[x.ordre]||{{}};document.querySelector('#progress').textContent=`${{index+1}}/${{view.length}}`;app.innerHTML=`<h2>${{x.id_persona}} · ${{x.inici_s}}–${{Number(x.inici_s)+Number(x.durada_s)}} s</h2><div class="meta"><p><b>Clip:</b> <code>${{x.clip}}</code> · <b>línies úniques:</b> ${{x.ratio_uniques}} · <b>Jaccard ASR:</b> ${{x.jaccard_tokens||'—'}}</p><p><b>Acústica orientativa:</b> veu activa ${{x.veu_proporcio||'—'}} · F0 ${{x.f0_median_hz||'—'}} Hz · IQR F0 ${{x.f0_iqr_hz||'—'}} Hz · pausa mediana ${{x.pausa_mediana_s||'—'}} s</p><p><b>Text base:</b> ${{x.text_qa||'—'}}</p><p><b>Text small:</b> ${{x.text_small||'—'}}</p></div><audio controls preload="metadata" src="${{x.clip}}"></audio><p class="warn">Escolta abans d'escriure. Les dues sortides ASR només localitzen el fragment; no són una decisió lingüística.</p><label>Veu<select id="speaker"><option>pendent</option><option>persona</option><option>entrevistador</option><option>mixt</option><option>incerta</option></select></label><label>Decisió<select id="decision"><option>pendent</option><option>sí</option><option>no</option><option>incerta</option></select></label><label>Variant escoltada<input id="variant"></label><label>Trets fonètics<textarea id="phon"></textarea></label><label>Prosòdia / pauses<textarea id="pros"></textarea></label><label>Nota<textarea id="note"></textarea></label>`;for(const [id,k] of [['speaker','veu'],['decision','decisio'],['variant','variant_transcrita'],['phon','trets_fonetics_observats'],['pros','observacions_prosodiques'],['note','nota_audicio']]){{const el=document.querySelector('#'+id);el.value=n[k]||'';el.addEventListener('input',()=>save(x))}}}}function save(x){{notes[x.ordre]={{veu:document.querySelector('#speaker').value,decisio:document.querySelector('#decision').value,variant_transcrita:document.querySelector('#variant').value,trets_fonetics_observats:document.querySelector('#phon').value,observacions_prosodiques:document.querySelector('#pros').value,nota_audicio:document.querySelector('#note').value}};localStorage.setItem(key,JSON.stringify(notes));if(pending.value==='sí')refresh()}}document.querySelector('#prev').onclick=()=>{{index=Math.max(0,index-1);render()}};document.querySelector('#next').onclick=()=>{{index=Math.min(view.length-1,index+1);render()}};filter.onchange=refresh;pending.onchange=refresh;document.querySelector('#download').onclick=()=>{{const h=Object.keys(allItems[0]);const lines=[h.join('\t')];for(const x of allItems){{const n=notes[x.ordre]||{{}};lines.push([x.ordre,x.id_persona,x.inici_s,x.durada_s,x.clip,x.transcripcio,x.ratio_uniques,x.text_qa,x.text_small,x.jaccard_tokens,x.consens_textual,x.veu_proporcio,x.f0_median_hz,x.f0_iqr_hz,x.pausa_mediana_s,n.veu||'pendent',n.decisio||'pendent',n.variant_transcrita||'',n.trets_fonetics_observats||'',n.observacions_prosodiques||'',n.nota_audicio||'',x.estat_audicio].map(v=>String(v).replace(/[\t\n]/g,' ')).join('\t'))}}const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([lines.join('\n')],{{type:'text/tab-separated-values'}}));a.download='anotacions-quarantena-20s.tsv';a.click()}};refresh();</script></body></html>'''
    OUT_HTML.write_text(html, encoding="utf-8")
    print(f"{len(output)} clips · {OUT_TSV} · {OUT_HTML}")


if __name__ == "__main__":
    main()
