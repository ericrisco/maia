"""Genera el reproductor local dels cinquanta-tres expedients de prospecció nova."""
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).parents[1]
PROSPECCIO = ROOT / "proveniencia" / "prospeccio"
OUT = ROOT / "proveniencia" / "auditoria-prospeccio-nova.html"
LEADS = [
    "lead-rtva-009-isidre-bartumeu",
    "lead-rtva-010-lurdes-riba",
    "lead-rtva-011-josep-dalleres",
    "lead-rtva-012-marc-forne",
    "lead-rtva-013-pere-vilanova",
    "lead-rtva-014-joan-burgues",
    "lead-rtva-015-isidre-baro",
    "lead-rtva-016-josep-areny",
    "lead-rtva-017-simo-duro",
    "lead-rtva-018-ricard-fiter",
    "lead-rtva-019-lisa-cruz",
    "lead-rtva-020-monica-bonell",
    "lead-rtva-021-bonaventura-riberaygua",
    "lead-rtva-022-josep-marsal",
    "lead-rtva-023-josep-maria-cases",
    "lead-rtva-024-denisa-font",
    "lead-rtva-025-albert-gelabert",
    "lead-rtva-026-rosa-maria-mandico",
    "lead-rtva-027-jordi-guillamet",
    "lead-rtva-028-pere-besoli",
    "lead-rtva-029-angelina-mas",
    "lead-rtva-030-casimir-arajol",
    "lead-rtva-031-ramon-rossell",
    "lead-rtva-032-anna-riberaygua",
    "lead-yt-033-david-montane",
    "lead-yt-034-antoni-marti",
    "lead-yt-035-cerni-escale",
    "lead-yt-036-xavier-espot",
    "lead-yt-037-oscar-ribas",
    "lead-yt-038-conxita-marsol",
    "lead-yt-039-marta-roure",
    "lead-yt-040-guillem-forne",
    "lead-yt-041-guillem-areny",
    "lead-yt-042-andreu-gonzalez",
    "lead-yt-043-oriol-agorreta",
    "lead-yt-044-laura-casanovas",
    "lead-yt-045-arnau-rius",
    "lead-yt-046-alberto-villagrasa",
    "lead-yt-047-katia-ustina",
    "lead-yt-048-ander-mirambell",
    "lead-yt-049-joan-piquet",
    "lead-yt-050-pau-chica",
    "lead-yt-051-albert-vilaro",
    "lead-yt-052-valenti-closa",
    "lead-yt-053-sonia-andorrita",
    "lead-yt-054-francesc-solana",
    "lead-yt-055-enric-flix",
    "lead-yt-056-arnau-fortuny",
    "lead-yt-057-gabriel-lezkano",
    "lead-yt-058-nuria-pablos",
    "lead-rtva-059-carles-ensenyat",
    "lead-rtva-060-xavier-espot-actual",
    "lead-rtva-061-antoni-morell",
]


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    items = []
    for lead in LEADS:
        folder = PROSPECCIO / lead
        info = json.loads((folder / "source.info.json").read_text(encoding="utf-8"))
        for number, row in enumerate(read(folder / "cua-audicio.tsv"), 1):
            items.append({
                "id": f"{lead}::{row.get('forma', '')}::{number}",
                "candidate": lead,
                "form": row.get("forma", ""),
                "clip": f"prospeccio/{lead}/{row['clip']}",
                "report": f"prospeccio/{lead}/informe.md",
                "source": info.get("source_url", ""),
                "small_transcript": f"prospeccio/{lead}/asr/{lead.split('-', 3)[3]}-small-nocontext.txt",
                "base_transcript": f"prospeccio/{lead}/asr/{lead.split('-', 3)[3]}-base-nocontext.txt",
                "start": row.get("inici_ms", ""),
                "end": row.get("final_ms", ""),
                "status": row.get("estat_audicio", "pendent"),
            })

    payload = json.dumps(items, ensure_ascii=False).replace("</", "<\\/")
    template = r'''<!doctype html>
<html lang="ca"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Audició — prospecció nova del corpus de parla andorrana</title>
<meta name="prospect-items" content="__COUNT__">
<style>body{font:16px system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem;color:#222}label{display:block;margin:.5rem 0}select,input,textarea,button{font:inherit;padding:.4rem}textarea{width:100%;min-height:4rem}audio{width:100%;margin:1rem 0}.meta{background:#f3f3f3;padding:.8rem;border-radius:.4rem}.warn{background:#fff4ce;padding:.6rem}.progress{float:right;color:#666}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:.6rem}code{overflow-wrap:anywhere}</style></head>
<body><h1>Audició — prospecció nova <span class="progress" id="progress"></span></h1>
<p>__COUNT__ clips dels cinquanta-tres expedients nous. Els textos ASR són suport automàtic; les decisions humanes es guarden al navegador i s'exporten en TSV, separades del registre canònic.</p>
<div class="grid"><label>Expedient<select id="candidate"><option value="tots">tots</option></select></label><label>Forma<select id="form"><option value="totes">totes</option></select></label><label>Només pendents<select id="pending"><option value="sí">sí</option><option value="no">no</option></select></label></div>
<p><button id="prev">Anterior</button> <button id="next">Següent</button> <button id="download">Descarrega TSV</button></p><main id="app"></main>
<script>const items=__PAYLOAD__;const key='maia-auditoria-prospeccio-nova-v1';let notes=JSON.parse(localStorage.getItem(key)||'{}'),index=0,view=[];const app=document.querySelector('#app'),candidate=document.querySelector('#candidate'),form=document.querySelector('#form'),pending=document.querySelector('#pending'),progress=document.querySelector('#progress');const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));for(const [el,values] of [[candidate,[...new Set(items.map(x=>x.candidate))].sort()],[form,[...new Set(items.map(x=>x.form))].sort()]])for(const v of values)el.insertAdjacentHTML('beforeend',`<option>${esc(v)}</option>`);function refresh(){view=items.filter(x=>(candidate.value==='tots'||x.candidate===candidate.value)&&(form.value==='totes'||x.form===form.value)&&(pending.value==='no'||!notes[x.id]||!notes[x.id].decision||notes[x.id].decision==='pendent'));index=Math.min(index,Math.max(0,view.length-1));render()}function render(){if(!view.length){app.innerHTML='<p>No hi ha clips amb aquests filtres.</p>';progress.textContent='0/0';return}const x=view[index],n=notes[x.id]||{};progress.textContent=`${index+1}/${view.length}`;app.innerHTML=`<h2>${esc(x.form)} · ${esc(x.candidate)}</h2><div class="meta"><p><b>Interval ASR:</b> ${esc(x.start)}–${esc(x.end)} ms · <b>Estat:</b> ${esc(x.status)}</p><p><b>Clip:</b> <code>${esc(x.clip)}</code> · <a href="${esc(x.report)}">informe</a> · <a href="${esc(x.source)}">font</a></p><p><a href="${esc(x.small_transcript)}">transcripció small</a> · <a href="${esc(x.base_transcript)}">transcripció base</a></p></div><audio controls preload="metadata" src="${esc(x.clip)}"></audio><p class="warn">Escolta la veu abans d'anotar la forma. El consens ASR no confirma identitat ni tret dialectal.</p><label>Veu<select id="speaker"><option>pendent</option><option>persona-candidata</option><option>entrevistador</option><option>mixt</option><option>incerta</option></select></label><label>Decisió de la forma<select id="decision"><option>pendent</option><option>sí</option><option>no</option><option>incerta</option></select></label><label>Variant escoltada<input id="variant"></label><label>Trets fonètics<textarea id="phon"></textarea></label><label>Prosòdia / pauses<textarea id="pros"></textarea></label><label>Nota<textarea id="note"></textarea></label>`;for(const [id,k] of [['speaker','speaker'],['decision','decision'],['variant','variant'],['phon','phon'],['pros','pros'],['note','note']]){const el=document.querySelector('#'+id);el.value=n[k]||'';el.addEventListener('input',()=>save(x))}}function save(x){notes[x.id]={speaker:document.querySelector('#speaker').value,decision:document.querySelector('#decision').value,variant:document.querySelector('#variant').value,phon:document.querySelector('#phon').value,pros:document.querySelector('#pros').value,note:document.querySelector('#note').value};localStorage.setItem(key,JSON.stringify(notes));if(pending.value==='sí')refresh()}document.querySelector('#prev').onclick=()=>{index=Math.max(0,index-1);render()};document.querySelector('#next').onclick=()=>{index=Math.min(view.length-1,index+1);render()};for(const el of [candidate,form,pending])el.onchange=()=>{index=0;refresh()};document.querySelector('#download').onclick=()=>{const h=['id','candidate','form','clip','start','end','speaker','decision','variant','phon','pros','note'];const lines=[h.join('\t')];for(const x of items){const n=notes[x.id]||{};lines.push([x.id,x.candidate,x.form,x.clip,x.start,x.end,n.speaker||'pendent',n.decision||'pendent',n.variant||'',n.phon||'',n.pros||'',n.note||''].map(v=>String(v).replace(/[\t\n]/g,' ')).join('\t'))}const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([lines.join('\n')],{type:'text/tab-separated-values'}));a.download='anotacions-auditoria-prospeccio-nova.tsv';a.click()};refresh();</script></body></html>'''
    OUT.write_text(template.replace("__COUNT__", str(len(items))).replace("__PAYLOAD__", payload), encoding="utf-8")
    print(f"OK reproductor prospecció nova: {len(items)} clips · {len(set(item['candidate'] for item in items))} expedients")


if __name__ == "__main__":
    main()
