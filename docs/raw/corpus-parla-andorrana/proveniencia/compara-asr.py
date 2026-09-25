"""Compara la transcripció principal amb una segona passada Whisper base.

No és una revisió humana ni prova dialectal. Serveix per separar formes que
sobreviuen a dos decodificadors de conjectures dependents d'un sol ASR.
"""
from __future__ import annotations
import csv, re
from pathlib import Path

ROOT=Path(__file__).parents[1]
FORMS=["bé","de fet","és a dir","aleshores","evidentment","diguem","crec","bueno","clar","vull dir","o sigui","llavors","a veure","aviam","doncs","perquè","a nivell","tirar endavant","ensenyança","reformeta"]
WORD_RE=re.compile(r"\b[\wàèéíòóúïüç']+\b",re.UNICODE)
def count(text,form):
    return len(re.findall(r"(?i)(?<!\w)"+re.escape(form)+r"(?!\w)",text))
def norm_words(text):
    return {w.lower() for w in WORD_RE.findall(text)}

def main():
    out=ROOT/'proveniencia'/'auditoria-creuada-asr.tsv'
    exclusions=ROOT/'proveniencia'/'qa-exclusions.tsv'
    excluded=set()
    if exclusions.exists():
        with exclusions.open(encoding='utf-8', newline='') as handle:
            excluded={row['id_persona'] for row in csv.DictReader(handle, delimiter='\t') if row.get('estat')=='quarantena-asr'}
    rows=[]
    for p in sorted((ROOT/'proveniencia').glob('pa-*/qa-base/transcripcio.txt')):
        pid=p.parent.parent.name
        if pid in excluded:
            continue
        small=(ROOT/'transcripcions'/f'{pid}.txt').read_text(encoding='utf-8')
        base=p.read_text(encoding='utf-8')
        ws=norm_words(small); wb=norm_words(base)
        for form in FORMS:
            a=count(small,form); b=count(base,form)
            rows.append({'id_persona':pid,'forma':form,'recompte_small':a,'recompte_base':b,'consens_dos_asr':'sí' if a and b else 'no','observacio':'coincidència textual entre dos passades' if a and b else 'revisar contra àudio'})
        shared=sorted(ws&wb)
        (p.parent/'consens-paraules.txt').write_text('\n'.join(shared)+'\n',encoding='utf-8')
        (p.parent/'resum.txt').write_text(f"{pid}\nparaules_small={len(ws)}\nparaules_base={len(wb)}\nparaules_compartides={len(ws&wb)}\n",encoding='utf-8')
    with out.open('w',encoding='utf-8',newline='') as f:
        fields=list(rows[0])
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(rows)
    print(f'{len(rows)} comparacions · {out}')
if __name__=='__main__': main()
