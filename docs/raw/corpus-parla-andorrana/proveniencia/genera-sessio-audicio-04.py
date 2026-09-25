"""Genera una sessió d'audició per a l'extracte del Consell General."""
from __future__ import annotations
import csv
from pathlib import Path
ROOT=Path(__file__).parents[1]; PROV=ROOT/'proveniencia'; CAND=PROV/'candidats'/'lead-cg-001-xavier-espot'
def read(p):
 with p.open(encoding='utf-8',newline='') as h:return list(csv.DictReader(h,delimiter='\t'))
def main():
 m=read(CAND/'formes-clips.tsv'); g={r['clip']:r for r in read(CAND/'qa-greedy.tsv')}; rows=[]
 for i,x in enumerate(m,1):
  q=g.get(x['clip'],{}); rows.append({'ordre_sessio':str(i),'id_global':f"candidate::lead-cg-001-xavier-espot::{x['forma']}::{i}",'origen':'Xavier Espot (candidat Consell General)','persona':'lead-cg-001-xavier-espot','forma':x['forma'],'clip':f"candidats/lead-cg-001-xavier-espot/{x['clip']}",'prioritat':x.get('prioritat','candidat-ASR'),'prob_min':'','text':q.get('text_greedy',''),'motiu':'extracte institucional: confirmar atribució de veu i forma abans de qualsevol incorporació','estat':'pendent'})
 f=list(rows[0]);
 with (PROV/'sessions'/'sessio-04.tsv').open('w',encoding='utf-8',newline='') as h:
  w=csv.DictWriter(h,fieldnames=f,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
 lines=["# Sessió d'audició 04 — Xavier Espot",'',"Aquesta sessió conté **4 clips** de l'extracte inicial del discurs del Consell General. Cal confirmar primer l'atribució de veu i després la forma; cap fila entra al registre canònic.",'','| ordre | forma | prioritat | clip |','|---:|---|---|---|']
 lines += [f"| {r['ordre_sessio']} | **{r['forma']}** | {r['prioritat']} | `{r['clip']}` |" for r in rows]
 lines += ['',"La sessió es pot obrir amb `../auditoria-global.html`; les anotacions exportades es conserven separades fins a una decisió explícita."]
 (PROV/'sessions'/'sessio-04.md').write_text('\n'.join(lines)+'\n',encoding='utf-8'); print(f'{len(rows)} clips')
if __name__=='__main__':main()
