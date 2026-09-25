"""Genera un revisor HTML local para los 656 clips de la cua d'audició."""

from __future__ import annotations

import csv
import html
import json
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = PROV / "auditoria-cua.html"


def read(name: str) -> list[dict[str, str]]:
    with (PROV / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    rows = read("registre-audicio.tsv")
    priorities = {
        (row["id_persona"], row["forma"]): row for row in read("prioritat-audicio.tsv")
    }
    items = []
    for row in rows:
        priority = priorities[(row["id_persona"], row["forma"])]
        items.append(
            {
                "id": f"{row['id_persona']}::{row['forma']}::{row['interval_escolta']}",
                "person": row["id_persona"],
                "form": row["forma"],
                "clip": row["clip"],
                "interval": row["interval_escolta"],
                "text": row["text_qa"],
                "transcript": row["transcripcio_qa"],
                "category": priority["categoria"],
                "score": priority["score_evidencia"],
                "prob": row["token_prob_min"],
                "voice": row["veu_proporcio"],
                "f0": row["f0_median_hz"],
                "pause": row["pausa_mediana_s"],
                "status": row["estat_audicio"],
            }
        )

    payload = json.dumps(items, ensure_ascii=False).replace("</", "<\\/")
    title = "Audició — cua completa del corpus independent"
    html_doc = f"""<!doctype html>
<html lang="ca"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>body{{font:16px system-ui,sans-serif;max-width:1040px;margin:2rem auto;padding:0 1rem;color:#222}}
label{{display:block;margin:.6rem 0}}select,input,textarea,button{{font:inherit;padding:.4rem}}
textarea{{width:100%;min-height:4rem}}audio{{width:100%;margin:1rem 0}}
.meta{{background:#f3f3f3;padding:.8rem;border-radius:.4rem}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:.5rem}}
.progress{{float:right}}.muted{{color:#666}}.warn{{background:#fff4ce;padding:.6rem;border-radius:.4rem}}</style></head>
<body><h1>{title} <span class="progress" id="progress"></span></h1>
<p class="muted">656 clips, ordenats per categoria i puntuació. Les anotacions es guarden al navegador.
Descarrega el TSV i incorpora'l amb <code>importa-auditoria.py</code>.</p>
<div class="grid"><label>Persona<select id="person"></select></label>
<label>Categoria<select id="category"><option value="all">Totes</option><option>A-triple-consens</option><option>B-doble-ASR</option><option>C-una-passada</option><option>D-divergent</option></select></label>
<label>Estat<select id="filter"><option value="all">Tots</option><option value="pendent">Pendents</option><option value="confirmada">Confirmades</option><option value="descartada">Descartades</option><option value="incerta">Incertes</option></select></label></div>
<p><button id="prev">Anterior</button> <button id="next">Següent</button> <button id="download">Descarrega TSV</button> <button id="clear">Neteja anotació actual</button></p>
<main id="app"></main><script>
const items={payload};const key='maia-corpus-audicio-cua-v1';
let notes=JSON.parse(localStorage.getItem(key)||'{{}}'),index=0;
const person=document.querySelector('#person'),category=document.querySelector('#category'),filter=document.querySelector('#filter'),app=document.querySelector('#app');
const people=[...new Set(items.map(x=>x.person))].sort();
person.innerHTML='<option value="all">Totes les persones</option>'+people.map(x=>`<option>${{x}}</option>`).join('');
function visible(){{return items.filter(x=>(person.value==='all'||x.person===person.value)&&(category.value==='all'||x.category===category.value)&&(filter.value==='all'||(notes[x.id]?.status||x.status||'pendent')===filter.value))}}
function current(){{let v=visible();if(!v.length){{app.innerHTML='<p>No hi ha casos amb aquest filtre.</p>';return null}}index=Math.max(0,Math.min(index,v.length-1));return v[index]}}
function render(){{let x=current();if(!x)return;let n=notes[x.id]||{{}};document.querySelector('#progress').textContent=`${{index+1}}/${{visible().length}}`;
app.innerHTML=`<h2>${{x.person}} — ${{x.form}}</h2><div class="meta"><p><b>Categoria:</b> ${{x.category}} · <b>Interval:</b> ${{x.interval}} · <b>Puntuació:</b> ${{x.score||'—'}}</p><p><b>Clip:</b> <a href="${{x.clip}}">${{x.clip}}</a></p><p><b>Text QA:</b> ${{x.text||'—'}}</p><p><b>Transcripció:</b> ${{x.transcript||'—'}}</p><p><b>Prob. token:</b> ${{x.prob||'—'}} · <b>Veu:</b> ${{x.voice||'—'}} · <b>F0:</b> ${{x.f0||'—'}} Hz · <b>Pausa:</b> ${{x.pause||'—'}} s</p></div><audio controls preload="metadata" src="${{x.clip}}"></audio><p class="warn">La forma escrita és una hipòtesi ASR. Decideix després d'escoltar el clip.</p><label>Decisió auditiva<select id="status"><option>pendent</option><option>confirmada</option><option>descartada</option><option>incerta</option></select></label><label>Variant escoltada<input id="variant"></label><label>Trets fonètics<textarea id="phon"></textarea></label><label>Prosòdia / pauses<textarea id="pros"></textarea></label><label>Nota<textarea id="note"></textarea></label>`;
document.querySelector('#status').value=n.status||x.status||'pendent';for(const [id,k] of [['variant','variant'],['phon','phon'],['pros','pros'],['note','note']])document.querySelector('#'+id).value=n[k]||'';for(const id of ['status','variant','phon','pros','note'])document.querySelector('#'+id).addEventListener('input',()=>save(x))}}
function save(x){{notes[x.id]={{status:document.querySelector('#status').value,variant:document.querySelector('#variant').value,phon:document.querySelector('#phon').value,pros:document.querySelector('#pros').value,note:document.querySelector('#note').value}};localStorage.setItem(key,JSON.stringify(notes));}}
function move(delta){{index+=delta;render()}}document.querySelector('#prev').onclick=()=>move(-1);document.querySelector('#next').onclick=()=>move(1);
for(const control of [person,category,filter])control.onchange=()=>{{index=0;render()}};
document.querySelector('#clear').onclick=()=>{{let x=current();if(x){{delete notes[x.id];localStorage.setItem(key,JSON.stringify(notes));render()}}}};
document.querySelector('#download').onclick=()=>{{let header=['id','person','form','interval','clip','status','variant','phon','pros','note'];let lines=[header.join('\\t')];for(const x of items){{let n=notes[x.id]||{{}};lines.push([x.id,x.person,x.form,x.interval,x.clip,n.status||x.status||'pendent',n.variant||'',n.phon||'',n.pros||'',n.note||''].map(v=>String(v).replace(/[\\t\\n]/g,' ')).join('\\t'))}}let a=document.createElement('a');a.href=URL.createObjectURL(new Blob([lines.join('\\n')],{{type:'text/tab-separated-values'}}));a.download='anotacions-audicio-cua.tsv';a.click()}};render();</script></body></html>"""
    OUT.write_text(html_doc, encoding="utf-8")
    print(f"generat {OUT} amb {len(items)} clips")


if __name__ == "__main__":
    main()
