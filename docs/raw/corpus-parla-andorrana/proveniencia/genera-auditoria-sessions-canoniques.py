"""Genera un anotador local para les sessions canòniques prioritzades."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = PROV / "auditoria-sessions-canoniques.html"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    rows = []
    for name in ("sessio-01.tsv", "sessio-02.tsv", "sessio-05.tsv", "sessio-06.tsv"):
        for row in read(PROV / "sessions" / name):
            if row.get("origen") != "canònic":
                continue
            item = dict(row)
            item["sessio"] = name.removesuffix(".tsv")
            rows.append(item)
    payload = json.dumps(rows, ensure_ascii=False).replace("</", "<\\/")
    doc = f'''<!doctype html><html lang="ca"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Audició de sessions canòniques — corpus de parla andorrana</title><style>body{{font:16px system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem;color:#222}}label{{display:block;margin:.5rem 0}}select,input,textarea,button{{font:inherit;padding:.4rem}}textarea{{width:100%;min-height:4rem}}audio{{width:100%;margin:1rem 0}}.meta{{background:#f3f3f3;padding:.8rem;border-radius:.4rem}}.warn{{background:#fff4ce;padding:.6rem;border-radius:.4rem}}.progress{{float:right;color:#666}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:.6rem}}</style></head><body><h1>Audició de sessions canòniques <span class="progress" id="progress"></span></h1><p>{len(rows)} clips prioritzats de les sessions 01, 02, 05 i 06. Les transcripcions i mesures automàtiques només orienten l'escolta; les anotacions es guarden localment i es projecten al registre mestre només després de validar-les.</p><div class="grid"><label>Sessió<select id="session"><option value="totes">totes</option><option>sessio-01</option><option>sessio-02</option><option>sessio-05</option><option>sessio-06</option></select></label><label>Persona<select id="person"><option value="totes">totes</option></select></label><label>Només pendents<select id="pending"><option value="sí">sí</option><option value="no">no</option></select></label></div><p><button id="prev">Anterior</button> <button id="next">Següent</button> <button id="download">Descarrega TSV</button></p><main id="app"></main><script>const items={payload};const key='maia-auditoria-sessions-canoniques-v3';let notes=JSON.parse(localStorage.getItem(key)||'{{}}'),index=0,view=[];const app=document.querySelector('#app'),session=document.querySelector('#session'),person=document.querySelector('#person'),pending=document.querySelector('#pending'),progress=document.querySelector('#progress');const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));for(const p of [...new Set(items.map(x=>x.persona))].sort())person.insertAdjacentHTML('beforeend',`<option>${{esc(p)}}</option>`);function refresh(){{view=items.filter(x=>(session.value==='totes'||x.sessio===session.value)&&(person.value==='totes'||x.persona===person.value)&&(pending.value==='no'||!notes[x.id_global]||!notes[x.id_global].decision||notes[x.id_global].decision==='pendent'));index=Math.min(index,Math.max(0,view.length-1));render()}}function render(){{if(!view.length){{app.innerHTML='<p>No hi ha clips amb aquests filtres.</p>';progress.textContent='0/0';return}}const x=view[index],n=notes[x.id_global]||{{}};progress.textContent=`${{index+1}}/${{view.length}}`;app.innerHTML=`<h2>${{esc(x.forma)}} · ${{esc(x.persona)}}</h2><div class="meta"><p><b>Sessió:</b> ${{esc(x.sessio)}} · <b>Clip:</b> <code>${{esc(x.clip)}}</code></p><p><b>Prioritat:</b> ${{esc(x.prioritat)}} · <b>Probabilitat mínima:</b> ${{esc(x.prob_min)}}</p><p><b>ASR small:</b> ${{esc(x.text_small)}}<br><b>ASR base:</b> ${{esc(x.text_base)}}<br><b>Context de selecció:</b> ${{esc(x.text)}}</p><p><b>F0:</b> ${{esc(x.f0_median_hz)}} Hz · <b>F1/F2/F3:</b> ${{esc(x.f1_hz)}} / ${{esc(x.f2_hz)}} / ${{esc(x.f3_hz)}} Hz · <b>Pausa:</b> ${{esc(x.pausa_mediana_s)}} s</p></div><audio controls preload="metadata" src="${{esc(x.clip)}}"></audio><p class="warn">Escolta el fragment complet. Confirma primer que parla la persona i després si la forma és real; el text ASR és només una hipòtesi.</p><label>Veu<select id="speaker"><option>pendent</option><option>persona</option><option>entrevistador</option><option>mixt</option><option>incerta</option></select></label><label>Decisió de la forma<select id="decision"><option>pendent</option><option>sí</option><option>no</option><option>incerta</option></select></label><label>Variant escoltada<input id="variant"></label><label>Trets fonètics<textarea id="phon"></textarea></label><label>Prosòdia / pauses<textarea id="pros"></textarea></label><label>Nota<textarea id="note"></textarea></label>`;for(const [id,k] of [['speaker','speaker'],['decision','decision'],['variant','variant'],['phon','phon'],['pros','pros'],['note','note']]){{const el=document.querySelector('#'+id);el.value=n[k]||'';el.addEventListener('input',()=>save(x))}}}}function save(x){{notes[x.id_global]={{speaker:document.querySelector('#speaker').value,decision:document.querySelector('#decision').value,variant:document.querySelector('#variant').value,phon:document.querySelector('#phon').value,pros:document.querySelector('#pros').value,note:document.querySelector('#note').value}};localStorage.setItem(key,JSON.stringify(notes));if(pending.value==='sí')refresh()}}document.querySelector('#prev').onclick=()=>{{index=Math.max(0,index-1);render()}};document.querySelector('#next').onclick=()=>{{index=Math.min(view.length-1,index+1);render()}};session.onchange=refresh;person.onchange=refresh;pending.onchange=refresh;document.querySelector('#download').onclick=()=>{{const h=['id_global','sessio','origen','persona','forma','clip','speaker','decision','variant','phon','pros','note'];const lines=[h.join('\\t')];for(const x of items){{const n=notes[x.id_global]||{{}};lines.push([x.id_global,x.sessio,x.origen,x.persona,x.forma,x.clip,n.speaker||'pendent',n.decision||'pendent',n.variant||'',n.phon||'',n.pros||'',n.note||''].map(v=>String(v).replace(/[\\t\\n]/g,' ')).join('\\t'))}}const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([lines.join('\\n')],{{type:'text/tab-separated-values'}}));a.download='anotacions-auditoria-sessions-canoniques.tsv';a.click()}};refresh();</script></body></html>'''
    OUT.write_text(doc, encoding="utf-8")
    print(f"{len(rows)} clips canònics")


if __name__ == "__main__":
    main()
