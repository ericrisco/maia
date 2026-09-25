"""Genera el reproductor HTML de la cua de formes escasses."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = PROV / "auditoria-formes-escasses.html"


def main() -> None:
    with (PROV / "cua-audicio-formes-escasses.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    items = [
        {
            "id": f"{row['forma']}::{row['id_persona']}::{row['rang']}",
            "form": row["forma"],
            "category": row["categoria"],
            "person": row["id_persona"],
            "clip": row["clip"],
            "interval": row["interval_vtt"],
            "text": row["text_asr"],
            "status": row["decisio_humana"],
        }
        for row in rows
    ]
    payload = json.dumps(items, ensure_ascii=False).replace("</", "<\\/")
    title = "Audició — formes escasses del corpus de parla andorrana"
    document = f'''<!doctype html><html lang="ca"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>body{{font:16px system-ui,sans-serif;max-width:1000px;margin:2rem auto;padding:0 1rem;color:#222}}select,input,textarea,button{{font:inherit;padding:.4rem}}textarea{{width:100%;min-height:4rem}}audio{{width:100%;margin:1rem 0}}.meta{{background:#f3f3f3;padding:.8rem;border-radius:.4rem}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:.5rem}}.progress{{float:right}}.warn{{background:#fff4ce;padding:.6rem;border-radius:.4rem}}</style></head><body><h1>{title} <span class="progress" id="progress"></span></h1><p>30 clips: tres per cadascuna de les 10 formes amb cobertura escassa. Les anotacions es guarden al navegador i es descarreguen com a TSV.</p><div class="grid"><label>Forma<select id="form"></select></label><label>Persona<select id="person"></select></label><label>Estat<select id="filter"><option value="all">Tots</option><option>pendent</option><option>confirmada</option><option>descartada</option><option>incerta</option></select></label></div><p><button id="prev">Anterior</button> <button id="next">Següent</button> <button id="download">Descarrega TSV</button></p><main id="app"></main><script>const items={payload};const key='maia-formes-escasses-v1';let notes=JSON.parse(localStorage.getItem(key)||'{{}}'),index=0,view=[];const form=document.querySelector('#form'),person=document.querySelector('#person'),filter=document.querySelector('#filter'),app=document.querySelector('#app'),esc=v=>String(v??'').replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));for(const [el,values] of [[form,[...new Set(items.map(x=>x.form))].sort()],[person,[...new Set(items.map(x=>x.person))].sort()]])el.innerHTML='<option value="all">Tots</option>'+values.map(v=>`<option>${{esc(v)}}</option>`).join('');function refresh(){{view=items.filter(x=>(form.value==='all'||x.form===form.value)&&(person.value==='all'||x.person===person.value)&&(filter.value==='all'||(notes[x.id]?.status||x.status)===filter.value));index=Math.min(index,Math.max(0,view.length-1));render()}}function render(){{if(!view.length){{app.innerHTML='<p>No hi ha clips amb aquest filtre.</p>';progress.textContent='0/0';return}}const x=view[index],n=notes[x.id]||{{}};progress.textContent=`${{index+1}}/${{view.length}}`;app.innerHTML=`<h2>${{esc(x.form)}} · ${{esc(x.person)}}</h2><div class="meta"><p><b>Categoria:</b> ${{esc(x.category)}} · <b>Interval:</b> ${{esc(x.interval)}}</p><p><b>ASR:</b> ${{esc(x.text)}}</p><p><b>Clip:</b> <code>${{esc(x.clip)}}</code></p></div><audio controls preload="metadata" src="${{esc(x.clip)}}"></audio><p class="warn">La forma escrita és una hipòtesi ASR. Escolta abans de decidir.</p><label>Decisió<select id="status"><option>pendent</option><option>confirmada</option><option>descartada</option><option>incerta</option></select></label><label>Variant escoltada<input id="variant"></label><label>Trets fonètics<textarea id="phon"></textarea></label><label>Prosòdia / pauses<textarea id="pros"></textarea></label><label>Nota<textarea id="note"></textarea></label>`;for(const [id,keyName] of [['status','status'],['variant','variant'],['phon','phon'],['pros','pros'],['note','note']]){{const el=document.querySelector('#'+id);el.value=n[keyName]||x[keyName]||'';el.addEventListener('input',()=>save(x))}}}}function save(x){{notes[x.id]={{status:document.querySelector('#status').value,variant:document.querySelector('#variant').value,phon:document.querySelector('#phon').value,pros:document.querySelector('#pros').value,note:document.querySelector('#note').value}};localStorage.setItem(key,JSON.stringify(notes))}}document.querySelector('#prev').onclick=()=>{{index=Math.max(0,index-1);render()}};document.querySelector('#next').onclick=()=>{{index=Math.min(view.length-1,index+1);render()}};for(const el of [form,person,filter])el.onchange=()=>{{index=0;refresh()}};document.querySelector('#download').onclick=()=>{{const h=['id','form','person','clip','status','variant','phon','pros','note'];const lines=[h.join('\\t')];for(const x of items){{const n=notes[x.id]||{{}};lines.push([x.id,x.form,x.person,x.clip,n.status||x.status||'pendent',n.variant||'',n.phon||'',n.pros||'',n.note||''].map(v=>String(v).replace(/[\\t\\n]/g,' ')).join('\\t'))}}const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([lines.join('\\n')],{{type:'text/tab-separated-values'}}));a.download='anotacions-formes-escasses.tsv';a.click()}};refresh();</script></body></html>'''
    OUT.write_text(document, encoding="utf-8")
    print(f"generat {OUT} amb {len(items)} clips")


if __name__ == "__main__":
    main()
