"""Genera el reproductor local dels 124 clips dels candidats fora del cànon."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
CANDIDATES = PROV / "candidats"
OUT = PROV / "auditoria-candidats-completa.html"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def transcript_link(folder: Path, base: bool) -> str:
    files = [p for p in (folder / "asr").glob("*.txt") if ("base" in p.stem) == base]
    if not files:
        return ""
    # Prefer the longest transcript when a full and an extracte coexistixen.
    path = max(files, key=lambda item: item.stat().st_size)
    return f"candidats/{folder.name}/asr/{path.name}"


def main() -> None:
    items: list[dict[str, str]] = []
    for folder in sorted(p for p in CANDIDATES.iterdir() if p.is_dir() and p.name.startswith("lead-")):
        clip_table = folder / "formes-clips.tsv"
        if not clip_table.exists():
            clip_table = folder / "formes-joan-clips.tsv"
        source_file = folder / "source-url.txt"
        source = source_file.read_text(encoding="utf-8").splitlines()[0].strip() if source_file.exists() else ""
        for row_number, row in enumerate(read(clip_table), start=1):
            clip = row["clip"]
            items.append({
                "id": f"{folder.name}::{row.get('forma', '')}::{row.get('segment', row_number)}::{row_number}",
                "candidate": folder.name,
                "form": row.get("forma", ""),
                "segment": row.get("segment", ""),
                "clip": f"candidats/{folder.name}/{clip}",
                "start": row.get("inici_clip_s", ""),
                "end": row.get("final_clip_s", ""),
                "small": row.get("small", ""),
                "base": row.get("base", ""),
                "priority": row.get("prioritat", ""),
                "status": row.get("estat", "pendent d'audició"),
                "source": source,
                "report": f"candidats/{folder.name}/informe.md",
                "small_transcript": transcript_link(folder, False),
                "base_transcript": transcript_link(folder, True),
            })
    payload = json.dumps(items, ensure_ascii=False).replace("</", "<\\/")
    document = f'''<!doctype html>
<html lang="ca"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Audició completa dels candidats — corpus de parla andorrana</title>
<meta name="candidate-items" content="{len(items)}">
<style>body{{font:16px system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem;color:#222}}label{{display:block;margin:.5rem 0}}select,input,textarea,button{{font:inherit;padding:.4rem}}textarea{{width:100%;min-height:4rem}}audio{{width:100%;margin:1rem 0}}.meta{{background:#f3f3f3;padding:.8rem;border-radius:.4rem}}.warn{{background:#fff4ce;padding:.6rem;border-radius:.4rem}}.progress{{float:right;color:#666}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:.6rem}}code{{overflow-wrap:anywhere}}</style></head>
<body><h1>Audició completa dels candidats <span class="progress" id="progress"></span></h1>
<p>{len(items)} clips locals dels 11 expedients separats. Les transcripcions i mètriques són suport automàtic; les decisions de veu, forma, variant, fonètica i prosòdia es guarden localment i s'exporten fora del registre canònic.</p>
<div class="grid"><label>Candidat<select id="candidate"><option value="tots">tots</option></select></label><label>Forma<select id="form"><option value="totes">totes</option></select></label><label>Només pendents<select id="pending"><option value="sí">sí</option><option value="no">no</option></select></label></div>
<p><button id="prev">Anterior</button> <button id="next">Següent</button> <button id="download">Descarrega TSV</button></p><main id="app"></main>
<script>const items={payload};const key='maia-auditoria-candidats-completa-v1';let notes=JSON.parse(localStorage.getItem(key)||'{{}}'),index=0,view=[];const app=document.querySelector('#app'),candidate=document.querySelector('#candidate'),form=document.querySelector('#form'),pending=document.querySelector('#pending'),progress=document.querySelector('#progress');const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));for(const [el,values] of [[candidate,[...new Set(items.map(x=>x.candidate))].sort()],[form,[...new Set(items.map(x=>x.form))].sort()]])for(const v of values)el.insertAdjacentHTML('beforeend',`<option>${{esc(v)}}</option>`);function refresh(){{view=items.filter(x=>(candidate.value==='tots'||x.candidate===candidate.value)&&(form.value==='totes'||x.form===form.value)&&(pending.value==='no'||!notes[x.id]||!notes[x.id].decision||notes[x.id].decision==='pendent'));index=Math.min(index,Math.max(0,view.length-1));render()}}function render(){{if(!view.length){{app.innerHTML='<p>No hi ha clips amb aquests filtres.</p>';progress.textContent='0/0';return}}const x=view[index],n=notes[x.id]||{{}};progress.textContent=`${{index+1}}/${{view.length}}`;app.innerHTML=`<h2>${{esc(x.form)}} · ${{esc(x.candidate)}}</h2><div class="meta"><p><b>Segment:</b> ${{esc(x.segment)}} · <b>Interval clip:</b> ${{esc(x.start)}}–${{esc(x.end)}} s · <b>Prioritat:</b> ${{esc(x.priority)}}</p><p><b>ASR small:</b> ${{esc(x.small)}} ocurrències · <b>ASR base:</b> ${{esc(x.base)}} ocurrències · <b>Estat automàtic:</b> ${{esc(x.status)}}</p><p><b>Clip:</b> <code>${{esc(x.clip)}}</code> · <a href="${{esc(x.report)}}">informe</a> ${{x.source?`· <a href="${{esc(x.source)}}">font</a>`:''}}</p><p><a href="${{esc(x.small_transcript)}}">transcripció small</a> · <a href="${{esc(x.base_transcript)}}">transcripció base</a></p></div><audio controls preload="metadata" src="${{esc(x.clip)}}"></audio><p class="warn">Escolta primer la veu candidata i després la forma. El recompte ASR no confirma cap tret dialectal ni la identitat del parlant.</p><label>Veu<select id="speaker"><option>pendent</option><option>persona-candidata</option><option>entrevistador</option><option>mixt</option><option>incerta</option></select></label><label>Decisió de la forma<select id="decision"><option>pendent</option><option>sí</option><option>no</option><option>incerta</option></select></label><label>Variant escoltada<input id="variant"></label><label>Trets fonètics<textarea id="phon"></textarea></label><label>Prosòdia / pauses<textarea id="pros"></textarea></label><label>Nota<textarea id="note"></textarea></label>`;for(const [id,k] of [['speaker','speaker'],['decision','decision'],['variant','variant'],['phon','phon'],['pros','pros'],['note','note']]){{const el=document.querySelector('#'+id);el.value=n[k]||'';el.addEventListener('input',()=>save(x))}}}}function save(x){{notes[x.id]={{speaker:document.querySelector('#speaker').value,decision:document.querySelector('#decision').value,variant:document.querySelector('#variant').value,phon:document.querySelector('#phon').value,pros:document.querySelector('#pros').value,note:document.querySelector('#note').value}};localStorage.setItem(key,JSON.stringify(notes));if(pending.value==='sí')refresh()}}document.querySelector('#prev').onclick=()=>{{index=Math.max(0,index-1);render()}};document.querySelector('#next').onclick=()=>{{index=Math.min(view.length-1,index+1);render()}};for(const el of [candidate,form,pending])el.onchange=()=>{{index=0;refresh()}};document.querySelector('#download').onclick=()=>{{const h=['id','candidate','form','segment','clip','start','end','speaker','decision','variant','phon','pros','note'];const lines=[h.join('\\t')];for(const x of items){{const n=notes[x.id]||{{}};lines.push([x.id,x.candidate,x.form,x.segment,x.clip,x.start,x.end,n.speaker||'pendent',n.decision||'pendent',n.variant||'',n.phon||'',n.pros||'',n.note||''].map(v=>String(v).replace(/[\\t\\n]/g,' ')).join('\\t'))}}const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([lines.join('\\n')],{{type:'text/tab-separated-values'}}));a.download='anotacions-auditoria-candidats-completa.tsv';a.click()}};refresh();</script></body></html>'''
    OUT.write_text(document, encoding="utf-8")
    print(f"{len(items)} clips candidats · {len(set(item['candidate'] for item in items))} expedients")


if __name__ == "__main__":
    main()
