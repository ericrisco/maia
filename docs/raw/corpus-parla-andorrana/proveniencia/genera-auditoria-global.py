"""Genera un anotador local únic per al corpus canònic i els onze candidats."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
OUT = PROV / "auditoria-global.html"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def candidate_rows(folder: str, manifest_name: str, label: str) -> list[dict[str, str]]:
    base = PROV / "candidats" / folder
    manifests = read(base / manifest_name)
    greedy = {row["clip"]: row for row in read(base / "qa-greedy.tsv")} if (base / "qa-greedy.tsv").exists() else {}
    rows = []
    for index, row in enumerate(manifests, start=1):
        clip = row["clip"]
        g = greedy.get(clip, {})
        rows.append({
            "id": f"{folder}::{row['forma']}::{index}",
            "origen": label,
            "persona": label,
            "forma": row["forma"],
            "clip": f"candidats/{folder}/{clip}",
            "prioritat": row.get("prioritat", "candidat-ASR"),
            "text": g.get("text_greedy", ""),
            "small": row.get("small", ""),
            "base": row.get("base", ""),
            "greedy": g.get("greedy", ""),
            "estat": "candidat; pendent d'audició",
        })
    return rows


def main() -> None:
    rows = []
    for row in read(PROV / "registre-audicio.tsv"):
        rows.append({
            "id": f"canon::{row['id_persona']}::{row['forma']}::{row['ordre']}",
            "origen": "canònic",
            "persona": row["id_persona"],
            "forma": row["forma"],
            "clip": row["clip"],
            "prioritat": row.get("prioritat_global", row.get("categoria", "")),
            "text": row.get("transcripcio_qa", row.get("text_qa", "")),
            "small": row.get("conf_min_segment", ""),
            "base": row.get("conf_min_base_segment", ""),
            "greedy": "",
            "estat": row.get("estat_audicio", "pendent"),
        })
    candidate_specs = [
        ("lead-rtva-001", "formes-joan-clips.tsv", "Joan Verdú"),
        ("lead-rtva-002-ian-moya", "formes-clips.tsv", "Ian Moya"),
        ("lead-rtva-003-dj-neura", "formes-clips.tsv", "DJ Neura"),
        ("lead-rtva-004-joan-mico", "formes-clips.tsv", "Joan Micó"),
        ("lead-cg-001-xavier-espot", "formes-clips.tsv", "Xavier Espot"),
        ("lead-cg-002-pere-lopez", "formes-clips.tsv", "Pere López"),
        ("lead-cg-003-roser-sune", "formes-clips.tsv", "Roser Suñé"),
        ("lead-rtva-005-carine-montaner", "formes-clips.tsv", "Carine Montaner"),
        ("lead-rtva-006-jaume-tomas", "formes-clips.tsv", "Jaume Tomàs"),
        ("lead-rtva-007-robert-guirao", "formes-clips.tsv", "Robert Guirao"),
        ("lead-rtva-008-mireia-pedescoll", "formes-clips.tsv", "Mireia Pedescoll"),
    ]
    for folder, manifest, label in candidate_specs:
        rows.extend(candidate_rows(folder, manifest, label))
    candidate_labels = [label for _, _, label in candidate_specs]
    candidate_options = "".join(f"<option>{label}</option>" for label in candidate_labels)
    candidate_description = ", ".join(candidate_labels)
    payload = json.dumps(rows, ensure_ascii=False).replace("</", "<\\/")
    title = "Auditoria global — corpus de parla andorrana"
    doc = f'''<!doctype html><html lang="ca"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>body{{font:16px system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem;color:#222}}label{{display:block;margin:.6rem 0}}select,input,textarea,button{{font:inherit;padding:.4rem}}textarea{{width:100%;min-height:4rem}}audio{{width:100%;margin:1rem 0}}.meta{{background:#f3f3f3;padding:.8rem;border-radius:.4rem}}.warn{{background:#fff4ce;padding:.6rem;border-radius:.4rem}}.progress{{float:right;color:#666}}.filters{{display:flex;gap:.5rem;flex-wrap:wrap}}</style></head><body><h1>{title} <span class="progress" id="progress"></span></h1><p>{len(rows)} clips: 656 del corpus canònic i els candidats audiovisuals {candidate_description}. Les anotacions es guarden al navegador; exporta el TSV quan acabis una sessió.</p><div class="filters"><label>Origen<select id="filter"><option value="tots">tots</option><option>canònic</option>{candidate_options}</select></label><label>Només pendents<select id="pending"><option value="sí">sí</option><option value="no">no</option></select></label></div><p><button id="prev">Anterior</button> <button id="next">Següent</button> <button id="download">Descarrega TSV</button></p><main id="app"></main><script>const allItems={payload};const key='maia-auditoria-global-v1';let notes=JSON.parse(localStorage.getItem(key)||'{{}}'),index=0,view=[];const app=document.querySelector('#app'),filter=document.querySelector('#filter'),pending=document.querySelector('#pending');function refresh(){{view=allItems.filter(x=>(filter.value==='tots'||x.origen===filter.value)&&(pending.value==='no'||!notes[x.id]||!notes[x.id].decision||notes[x.id].decision==='pendent'));index=Math.min(index,Math.max(0,view.length-1));render()}}function render(){{if(!view.length){{app.innerHTML='<p>No hi ha clips amb aquests filtres.</p>';document.querySelector('#progress').textContent='0/0';return}}const x=view[index],n=notes[x.id]||{{}};document.querySelector('#progress').textContent=`${{index+1}}/${{view.length}}`;app.innerHTML=`<h2>${{x.forma}} · ${{x.persona}}</h2><div class="meta"><p><b>Origen:</b> ${{x.origen}} · <b>Clip:</b> <code>${{x.clip}}</code></p><p><b>Prioritat:</b> ${{x.prioritat}} · <b>small/base/greedy:</b> ${{x.small}} / ${{x.base}} / ${{x.greedy}}</p><p><b>Text ASR:</b> ${{x.text||'—'}}</p></div><audio controls preload="metadata" src="${{x.clip}}"></audio><p class="warn">Escolta abans d'escriure. La sortida ASR és una hipòtesi; separa la identitat de la veu de la decisió sobre la forma.</p><label>Veu<select id="speaker"><option>pendent</option><option>persona</option><option>entrevistador</option><option>mixt</option><option>incerta</option></select></label><label>Decisió de la forma<select id="decision"><option>pendent</option><option>sí</option><option>no</option><option>incerta</option></select></label><label>Variant escoltada<input id="variant"></label><label>Trets fonètics<textarea id="phon"></textarea></label><label>Prosòdia / pauses<textarea id="pros"></textarea></label><label>Nota<textarea id="note"></textarea></label>`;for(const [id,k] of [['speaker','speaker'],['decision','decision'],['variant','variant'],['phon','phon'],['pros','pros'],['note','note']]){{const el=document.querySelector('#'+id);el.value=n[k]||'';el.addEventListener('input',()=>save(x))}}}}function save(x){{notes[x.id]={{speaker:document.querySelector('#speaker').value,decision:document.querySelector('#decision').value,variant:document.querySelector('#variant').value,phon:document.querySelector('#phon').value,pros:document.querySelector('#pros').value,note:document.querySelector('#note').value}};localStorage.setItem(key,JSON.stringify(notes));if(pending.value==='sí')refresh()}}document.querySelector('#prev').onclick=()=>{{index=Math.max(0,index-1);render()}};document.querySelector('#next').onclick=()=>{{index=Math.min(view.length-1,index+1);render()}};filter.onchange=refresh;pending.onchange=refresh;document.querySelector('#download').onclick=()=>{{const h=['id','origen','persona','forma','clip','speaker','decision','variant','phon','pros','note'];const lines=[h.join('\\t')];for(const x of allItems){{const n=notes[x.id]||{{}};lines.push([x.id,x.origen,x.persona,x.forma,x.clip,n.speaker||'pendent',n.decision||'pendent',n.variant||'',n.phon||'',n.pros||'',n.note||''].map(v=>String(v).replace(/[\\t\\n]/g,' ')).join('\\t'))}}const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([lines.join('\\n')],{{type:'text/tab-separated-values'}}));a.download='anotacions-auditoria-global.tsv';a.click()}};refresh();</script></body></html>'''
    OUT.write_text(doc, encoding="utf-8")
    (PROV / "quadern-audicio-global.md").write_text(
        f"# Quadern d'audició global\n\nLa cua unificada té **{len(rows)} clips**: 656 canònics i 124 clips dels 11 candidats (inclou Joan Verdú, Ian Moya, DJ Neura, Joan Micó, Xavier Espot, Pere López, Roser Suñé, Carine Montaner, Jaume Tomàs, Robert Guirao i Mireia Pedescoll). El reproductor és `auditoria-global.html`; totes les decisions automàtiques es mantenen separades de les anotacions humanes.\n",
        encoding="utf-8",
    )
    print(f"{len(rows)} clips globals")


if __name__ == "__main__":
    main()
