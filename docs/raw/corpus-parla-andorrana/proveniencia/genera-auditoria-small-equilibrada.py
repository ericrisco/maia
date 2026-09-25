"""Genera un revisor HTML local per als 100 clips equilibrats small."""
from __future__ import annotations
import csv, html, json
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = PROV / "auditoria-small-equilibrada.html"

def main():
    with (PROV / "cua-audicio-small-equilibrada.tsv").open(encoding="utf-8", newline="") as h:
        rows = list(csv.DictReader(h, delimiter="\t"))
    items = []
    for row in rows:
        items.append({
            "id": f"{row['id_persona']}::{row['forma']}::{row['clip']}",
            "person": row["id_persona"], "form": row["forma"], "clip": row["clip"],
            "start": row["absolute_start_s"], "end": row["absolute_end_s"], "text": row["text"],
            "priority": row["prioritat"], "prob": row["prob_min"], "f0": row["f0_hz"],
            "f1": row["f1_hz"], "f2": row["f2_hz"], "f3": row["f3_hz"],
        })
    payload = json.dumps(items, ensure_ascii=False).replace("</", "<\\/")
    title = "Audició — mostra equilibrada small del corpus independent"
    doc = f'''<!doctype html>
<html lang="ca"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><style>body{{font:16px system-ui,sans-serif;max-width:1040px;margin:2rem auto;padding:0 1rem;color:#222}}label{{display:block;margin:.6rem 0}}select,input,textarea,button{{font:inherit;padding:.4rem}}textarea{{width:100%;min-height:4rem}}audio{{width:100%;margin:1rem 0}}.meta{{background:#f3f3f3;padding:.8rem;border-radius:.4rem}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:.5rem}}.progress{{float:right}}.muted{{color:#666}}.warn{{background:#fff4ce;padding:.6rem;border-radius:.4rem}}</style></head>
<body><h1>{html.escape(title)} <span class="progress" id="progress"></span></h1>
<p class="muted">100 clips, 63 parlants i 20 formes. Les anotacions es guarden al navegador; descarrega el TSV quan acabis.</p>
<div class="grid"><label>Persona<select id="person"></select></label><label>Forma<select id="form"><option value="all">Totes</option></select></label><label>Estat<select id="filter"><option value="all">Tots</option><option value="pendent">Pendents</option><option value="sí">Confirmades</option><option value="no">Descartades</option><option value="incerta">Incertes</option></select></label></div>
<p><button id="prev">Anterior</button> <button id="next">Següent</button> <button id="download">Descarrega TSV</button> <button id="clear">Neteja anotació actual</button></p><main id="app"></main><script>
const items={payload};const key='maia-corpus-audicio-small-equilibrada-v1';let notes=JSON.parse(localStorage.getItem(key)||'{{}}'),index=0;const person=document.querySelector('#person'),form=document.querySelector('#form'),filter=document.querySelector('#filter'),app=document.querySelector('#app');const people=[...new Set(items.map(x=>x.person))].sort();const forms=[...new Set(items.map(x=>x.form))].sort();person.innerHTML='<option value="all">Totes les persones</option>'+people.map(x=>`<option>${{x}}</option>`).join('');form.innerHTML+='<option>'+forms.join('</option><option>')+'</option>';
function visible(){{return items.filter(x=>(person.value==='all'||x.person===person.value)&&(form.value==='all'||x.form===form.value)&&(filter.value==='all'||(notes[x.id]?.status||'pendent')===filter.value))}}function current(){{let v=visible();if(!v.length){{app.innerHTML='<p>No hi ha casos amb aquest filtre.</p>';return null}}index=Math.max(0,Math.min(index,v.length-1));return v[index]}}function render(){{let x=current();if(!x)return;let n=notes[x.id]||{{}};document.querySelector('#progress').textContent=`${{index+1}}/${{visible().length}}`;app.innerHTML=`<h2>${{x.person}} — ${{x.form}}</h2><div class="meta"><p><b>Prioritat:</b> ${{x.priority}} · <b>Temps:</b> ${{x.start}}–${{x.end}} s · <b>Probabilitat:</b> ${{x.prob||'—'}}</p><p><b>Clip:</b> <a href="${{x.clip}}">${{x.clip}}</a></p><p><b>Text small:</b> ${{x.text||'—'}}</p><p><b>Formants:</b> F0 ${{x.f0||'—'}} · F1 ${{x.f1||'—'}} · F2 ${{x.f2||'—'}} · F3 ${{x.f3||'—'}}</p></div><audio controls preload="metadata" src="${{x.clip}}"></audio><p class="warn">La forma escrita és una hipòtesi ASR. Decideix només després d'escoltar el clip.</p><label>Decisió auditiva<select id="status"><option value="pendent">pendent</option><option value="sí">sí</option><option value="no">no</option><option value="incerta">incerta</option></select></label><label>Variant escoltada<input id="variant"></label><label>Trets fonètics<textarea id="phon"></textarea></label><label>Prosòdia / pauses<textarea id="pros"></textarea></label><label>Nota<textarea id="note"></textarea></label>`;document.querySelector('#status').value=n.status||'pendent';for(const [id,k] of [['variant','variant'],['phon','phon'],['pros','pros'],['note','note']])document.querySelector('#'+id).value=n[k]||'';for(const id of ['status','variant','phon','pros','note'])document.querySelector('#'+id).addEventListener('input',()=>save(x))}}function save(x){{notes[x.id]={{status:document.querySelector('#status').value,variant:document.querySelector('#variant').value,phon:document.querySelector('#phon').value,pros:document.querySelector('#pros').value,note:document.querySelector('#note').value}};localStorage.setItem(key,JSON.stringify(notes))}}function move(delta){{index+=delta;render()}}document.querySelector('#prev').onclick=()=>move(-1);document.querySelector('#next').onclick=()=>move(1);for(const c of [person,form,filter])c.onchange=()=>{{index=0;render()}};document.querySelector('#clear').onclick=()=>{{let x=current();if(x){{delete notes[x.id];localStorage.setItem(key,JSON.stringify(notes));render()}}}};document.querySelector('#download').onclick=()=>{{let h=['id','person','form','clip','start','end','status','variant','phon','pros','note'];let l=[h.join('\\t')];for(const x of items){{let n=notes[x.id]||{{}};l.push([x.id,x.person,x.form,x.clip,x.start,x.end,n.status||'pendent',n.variant||'',n.phon||'',n.pros||'',n.note||''].map(v=>String(v).replace(/[\\t\\n]/g,' ')).join('\\t'))}}let a=document.createElement('a');a.href=URL.createObjectURL(new Blob([l.join('\\n')],{{type:'text/tab-separated-values'}}));a.download='anotacions-audicio-small-equilibrada.tsv';a.click()}};render();</script></body></html>'''
    OUT.write_text(doc, encoding="utf-8")
    print(f"generat {OUT} amb {len(items)} clips")

if __name__ == "__main__":
    main()
