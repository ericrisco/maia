"""Genera un reproductor local filtrable per a la comparació dels clips forts."""

from html import escape
from pathlib import Path
import csv
import json

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"


def main() -> None:
    with (PROV / "qa-clips-forts-consens.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    payload = json.dumps(rows, ensure_ascii=False).replace("</", "<\\/")
    html = """<!doctype html>
<meta charset="utf-8">
<title>Auditoria dels clips forts — tres descodificacions</title>
<style>
body{font-family:system-ui,sans-serif;max-width:1500px;margin:2rem auto;padding:0 1rem;background:#f7f7f7;color:#202124}
h1{margin-bottom:.3rem}.note{color:#555}select,input{font-size:1rem;padding:.4rem;margin:.2rem .5rem .8rem 0}
table{border-collapse:collapse;width:100%;background:#fff}th,td{border:1px solid #ddd;padding:.45rem;vertical-align:top;text-align:left}th{position:sticky;top:0;background:#eee}audio{width:240px}.A-tres-models{background:#eef8ee}.B-dos-models{background:#fff8df}.C-un-model{background:#ffecec}
.small{font-size:.9rem;color:#555;max-width:300px}.text{max-width:340px;white-space:pre-wrap}
</style>
<h1>Auditoria dels clips forts</h1>
<p class="note">Comparació small/base/greedy. Les categories només prioritzen l’escolta i no són decisions lingüístiques.</p>
<label>Categoria <select id="category"><option value="">totes</option><option>A-tres-models</option><option>B-dos-models</option><option>C-un-model</option><option>D-cap-model</option></select></label>
<label>Persona <input id="person" placeholder="pa-010"></label>
<span id="count"></span>
<table><thead><tr><th>#</th><th>Persona · forma</th><th>Categoria</th><th>Àudio</th><th>Small</th><th>Base</th><th>Greedy</th></tr></thead><tbody id="rows"></tbody></table>
<script>
const items=__DATA__;
const category=document.querySelector('#category'),person=document.querySelector('#person'),body=document.querySelector('#rows'),count=document.querySelector('#count');
function esc(s){return String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function draw(){const c=category.value,p=person.value.trim().toLowerCase();const out=items.filter(x=>(!c||x.categoria===c)&&(!p||x.id_persona.toLowerCase().includes(p)));count.textContent=` ${out.length} clips`;body.innerHTML=out.map((x,i)=>`<tr class="${esc(x.categoria)}"><td>${i+1}</td><td><b>${esc(x.id_persona)}</b><br>${esc(x.forma)}<br><span class="small">${esc(x.clip)}</span></td><td>${esc(x.categoria)}<br>small ${esc(x.small)} · base ${esc(x.base)} · greedy ${esc(x.greedy)}</td><td><audio controls preload="none" src="${esc(x.clip)}"></audio></td><td class="text">${esc(x.text_small)}</td><td class="text">${esc(x.text_base)}</td><td class="text">${esc(x.text_greedy)}</td></tr>`).join('');}
category.addEventListener('change',draw);person.addEventListener('input',draw);draw();
</script>
""".replace("__DATA__", payload)
    (PROV / "auditoria-forts-triple.html").write_text(html, encoding="utf-8")
    print(f"{len(rows)} clips · auditoria-forts-triple.html")


if __name__ == "__main__":
    main()
