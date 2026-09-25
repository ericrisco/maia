"""Compara les dues transcripcions ASR del candidat RTVA per forma."""
from __future__ import annotations

import csv
import json
import re
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).parents[1]
CAND = ROOT / 'proveniencia' / 'candidats' / 'lead-rtva-001'
FORMS = [
    'a nivell','a veure','aleshores','aviam','bé','bueno','clar','crec','de fet',
    'diguem','doncs','evidentment','és a dir','llavors','no?','o sigui','per tant',
    'perquè','tirar endavant','vull dir','ensenyança',
]

def text(path: Path) -> str:
    data=json.loads(path.read_text(encoding='utf-8'))
    return ' '.join(seg.get('text','').strip() for seg in data['transcription'])

def count(form, corpus):
    return len(re.findall(rf'(?<![\wà-ÿ]){re.escape(form)}(?![\wà-ÿ])', corpus, re.I))

def main():
    small=text(CAND/'asr/joan-verdu.json')
    base=text(CAND/'asr/joan-verdu-base.json')
    rows=[]
    for form in FORMS:
        a=count(form,small); b=count(form,base)
        rows.append({'forma':form,'small':a,'base':b,'consens_presencia':'sí' if a and b else 'no','estat':"consens ASR; pendent d'audició" if a and b else "divergència o absència ASR; pendent d'audició"})
    with (CAND/'formes-consens.tsv').open('w',encoding='utf-8',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n'); writer.writeheader(); writer.writerows(rows)
    similarity=SequenceMatcher(None,small,base).ratio()
    report=CAND/'comparacio-asr.md'
    lines=['# Comparació ASR — Joan Verdú','',f'La comparació textual global small/base té una similitud de **{similarity:.4f}**. Les dues sortides són automàtiques i poden repetir els mateixos errors; cap coincidència substitueix l\'audició.','', '| forma | small | base | presència en tots dos |','|---|---:|---:|---|']
    for r in rows: lines.append(f"| `{r['forma']}` | {r['small']} | {r['base']} | {r['consens_presencia']} |")
    lines += ['', 'La taula `formes-consens.tsv` conserva el recompte i l’estat de cada forma. Les variants ortogràfiques detectades als textos ASR s’han de revisar contra l’àudio.']
    report.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    candidate=CAND/'informe.md'; s=candidate.read_text(encoding='utf-8')
    marker='## Separació acústica provisional\n'
    addition=f'## Contrast independent small/base\n\nLes dues transcripcions ASR tenen una similitud textual global de **{similarity:.4f}**. `formes-consens.tsv` conserva els recomptes per marcador; les coincidències continuen pendents d\'audició.\n\n'
    if '## Contrast independent small/base' not in s:
        s=s.replace(marker,addition+marker,1); candidate.write_text(s,encoding='utf-8')
    print(f'similitud {similarity:.4f} · {sum(r["small"] and r["base"] for r in rows)} formes presents en tots dos')

if __name__=='__main__': main()
