"""Genera una vista provisional del candidato RTVA contra el graf canònic."""
from __future__ import annotations
import csv
from pathlib import Path
ROOT=Path(__file__).parents[1]; PROV=ROOT/'proveniencia'; CAND=PROV/'candidats'/'lead-rtva-001'; OUT=CAND/'graf'; OUT.mkdir(exist_ok=True)

def read(path):
 with path.open(encoding='utf-8',newline='') as h:return list(csv.DictReader(h,delimiter='\t'))

def main():
 consensus=[r['forma'] for r in read(CAND/'formes-consens.tsv') if int(r['small'])>0 and int(r['base'])>0]
 candidate=set(consensus)
 nodes=read(ROOT/'grafo'/'nodes-small-token-canonics.tsv')
 edges=[]
 for n in nodes:
  forms=set(filter(None,n['formes'].split(',')))
  shared=sorted(candidate & forms)
  if len(shared)>=2:
   edges.append({'id_a':'lead-rtva-001','id_b':n['id_parlant'],'n_formes_compartides':str(len(shared)),'formes':','.join(shared),'estat':'candidat RTVA; consens ASR textual; pendent d’audició'})
 with (OUT/'nodes.tsv').open('w',encoding='utf-8',newline='') as h:
  w=csv.writer(h,delimiter='\t',lineterminator='\n');w.writerow(['id_parlant','nom_public','n_formes','formes','estat']);w.writerow(['lead-rtva-001','Joan Verdú',len(candidate),','.join(sorted(candidate)),'candidat separat; pendent de veu i audició'])
  for n in nodes:w.writerow([n['id_parlant'],n['nom_public'],n['n_formes'],n['formes'],'persona canònica; graf small textual'])
 with (OUT/'arestes.tsv').open('w',encoding='utf-8',newline='') as h:
  w=csv.DictWriter(h,fieldnames=['id_a','id_b','n_formes_compartides','formes','estat'],delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(edges)
 with (OUT/'trets.tsv').open('w',encoding='utf-8',newline='') as h:
  w=csv.writer(h,delimiter='\t',lineterminator='\n');w.writerow(['forma','font','estat']);w.writerows([[f,'Joan Verdú + graf canònic small','consens textual; pendent d’audició'] for f in sorted(candidate)])
 lines=['graph TD','  C["Joan Verdú — candidat"]']
 for e in edges:
  n=next(n for n in nodes if n['id_parlant']==e['id_b']); label=n['nom_public'].replace('"','\\"'); lines.append(f'  {e["id_b"]}["{label}"]'); lines.append(f'  C -- "{e["n_formes_compartides"]} formes" --> {e["id_b"]}')
 (OUT/'graf.mmd').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 (OUT/'README.md').write_text(f'''# Graf provisional — Joan Verdú\n\nAquesta vista separa el candidat RTVA del graf canònic. Usa només les **{len(candidate)} formes** presents en small i base i connecta el candidat amb **{len(edges)} persones** que en comparteixen almenys dues.\n\nLes arestes són semblances textuals ASR; no indiquen dialecte, identitat lingüística ni veu confirmada. Joan no entra encara al recompte canònic.\n''',encoding='utf-8')
 print(f'{len(candidate)} formes · {len(edges)} arestes · {len(nodes)+1} nodes')
if __name__=='__main__':main()
