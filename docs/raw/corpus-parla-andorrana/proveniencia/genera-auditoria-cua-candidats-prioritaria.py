"""Genera el reproductor local de la primera cola humana de candidatos."""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
QUEUE = PROV / "cua-audicio-candidats-prioritaria.tsv"
SOURCE = PROV / "auditoria-candidats-completa.html"
OUT = PROV / "auditoria-cua-candidats-prioritaria.html"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def source_items() -> dict[str, dict[str, str]]:
    text = SOURCE.read_text(encoding="utf-8")
    match = re.search(r"const items=(\[.*?\]);const key=", text, re.DOTALL)
    if not match:
        raise ValueError(f"no trobo els clips candidats a {SOURCE}")
    return {row["id"]: row for row in json.loads(match.group(1))}


def main() -> None:
    queue = read(QUEUE)
    items = source_items()
    payload = []
    for row in queue:
        item = dict(row)
        item.update({key: items.get(row["id"], {}).get(key, "") for key in ("small_transcript", "base_transcript")})
        payload.append(item)
    serialized = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    html = f'''<!doctype html>
<html lang="ca"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Audició prioritària de candidats — corpus de parla andorrana</title>
<style>body{{font:16px system-ui,sans-serif;max-width:1050px;margin:2rem auto;padding:0 1rem;color:#222}}label{{display:block;margin:.55rem 0}}select,input,textarea,button{{font:inherit;padding:.4rem}}textarea{{width:100%;min-height:4rem}}audio{{width:100%;margin:1rem 0}}.meta{{background:#f3f3f3;padding:.8rem;border-radius:.4rem}}.warn{{background:#fff4ce;padding:.7rem;border-radius:.4rem}}.progress{{float:right;color:#666}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:.6rem}}</style></head>
<body><h1>Audició prioritària de candidats <span class="progress" id="progress"></span></h1>
<p>20 clips de 11 veus candidates. Les dades automàtiques només orienten l'escolta; aquesta cua és separada del cànon i s'exporta a un TSV propi.</p>
<div class="grid"><label>Candidat<select id="candidate"><option value="tots">tots</option></select></label><label>Només pendents<select id="pending"><option value="sí">sí</option><option value="no">no</option></select></label></div>
<p><button id="prev">Anterior</button> <button id="next">Següent</button> <button id="download">Descarrega TSV</button></p><main id="app"></main>
<script>const items={serialized};const key='maia-auditoria-cua-candidats-prioritaria-v1';let notes=JSON.parse(localStorage.getItem(key)||'{{}}'),index=0,view=[];
const app=document.querySelector('#app'),candidate=document.querySelector('#candidate'),pending=document.querySelector('#pending'),progress=document.querySelector('#progress');
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));
for(const p of [...new Set(items.map(x=>x.candidate))].sort())candidate.insertAdjacentHTML('beforeend',`<option>${{esc(p)}}</option>`);
function refresh(){{view=items.filter(x=>(candidate.value==='tots'||x.candidate===candidate.value)&&(pending.value==='no'||!notes[x.id]||!notes[x.id].decision||notes[x.id].decision==='pendent'));index=Math.min(index,Math.max(0,view.length-1));render()}}
function render(){{if(!view.length){{app.innerHTML='<p>No hi ha clips amb aquests filtres.</p>';progress.textContent='0/0';return}}const x=view[index],n=notes[x.id]||{{}};progress.textContent=`${{index+1}}/${{view.length}}`;app.innerHTML=`<h2>${{esc(x.forma)}} · ${{esc(x.candidate)}}</h2><div class="meta"><p><b>Clip:</b> <code>${{esc(x.clip)}}</code> · <b>Interval:</b> ${{esc(x.inici_s)}}–${{esc(x.final_s)}} s · <b>Prioritat:</b> ${{esc(x.prioritat)}}</p><p><b>ASR small:</b> ${{esc(x.small_transcript)}}<br><b>ASR base:</b> ${{esc(x.base_transcript)}}</p><p><a href="${{esc(x.font)}}" target="_blank" rel="noreferrer">Font pública</a></p></div><audio controls preload="metadata" src="${{esc(x.clip)}}"></audio><p class="warn">Confirma primer si parla la persona candidata i després si la forma és real. No tractis l'ASR ni els descriptors com una decisió.</p><label>Veu<select id="speaker"><option>pendent</option><option>persona-candidata</option><option>entrevistador</option><option>mixt</option><option>incerta</option></select></label><label>Decisió de la forma<select id="decision"><option>pendent</option><option>sí</option><option>no</option><option>incerta</option></select></label><label>Variant escoltada<input id="variant"></label><label>Trets fonètics<textarea id="phon"></textarea></label><label>Prosòdia / pauses<textarea id="pros"></textarea></label><label>Nota<textarea id="note"></textarea></label>`;for(const [id,k] of [['speaker','speaker'],['decision','decision'],['variant','variant'],['phon','phon'],['pros','pros'],['note','note']]){{const e=document.querySelector('#'+id);e.value=n[k]||'';e.addEventListener('input',()=>save(x))}}}}
function save(x){{notes[x.id]={{speaker:document.querySelector('#speaker').value,decision:document.querySelector('#decision').value,variant:document.querySelector('#variant').value,phon:document.querySelector('#phon').value,pros:document.querySelector('#pros').value,note:document.querySelector('#note').value}};localStorage.setItem(key,JSON.stringify(notes));if(pending.value==='sí')refresh()}}
document.querySelector('#prev').onclick=()=>{{index=Math.max(0,index-1);render()}};document.querySelector('#next').onclick=()=>{{index=Math.min(view.length-1,index+1);render()}};candidate.onchange=refresh;pending.onchange=refresh;
document.querySelector('#download').onclick=()=>{{const h=['id','candidate','forma','clip','estat_audicio','veu_confirmada','forma_confirmada','variant_transcrita','trets_fonetics_observats','observacions_prosodiques','nota_audicio'];const lines=[h.join('\\t')];for(const x of items){{const n=notes[x.id]||{{}};lines.push([x.id,x.candidate,x.forma,x.clip,n.decision||'pendent',n.speaker||'pendent',n.decision||'pendent',n.variant||'',n.phon||'',n.pros||'',n.note||''].map(v=>String(v).replace(/[\\t\\n]/g,' ')).join('\\t'))}}const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([lines.join('\\n')],{{type:'text/tab-separated-values'}}));a.download='anotacions-cua-candidats-prioritaria.tsv';a.click()}};refresh();</script></body></html>'''
    OUT.write_text(html, encoding="utf-8")
    print(f"{len(payload)} clips · {len({row['candidate'] for row in payload})} candidats · {OUT}")


if __name__ == "__main__":
    main()
