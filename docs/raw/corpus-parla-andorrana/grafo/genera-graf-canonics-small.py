"""Genera una vista del graf small agrupada per persona canònica."""
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
import csv
ROOT=Path(__file__).parents[1]; PROV=ROOT/'proveniencia'; GRAFO=ROOT/'grafo'

def read(path):
 with path.open(encoding='utf-8',newline='') as h:return list(csv.DictReader(h,delimiter='\t'))
def main():
 mapping={r['id_persona']:r for r in read(PROV/'persones-canonics.tsv')}
 occ=read(PROV/'qa-cua-small-token-occurrences.tsv')
 by=defaultdict(set); counts=Counter()
 for r in occ:
  sp=mapping[r['id_persona']]['id_parlant']; by[sp].add(r['forma']); counts[(sp,r['forma'])]+=1
 people={r['id_parlant']:r for r in mapping.values()}
 traits=[]
 for form in sorted({r['forma'] for r in occ}):
  speakers=sorted({mapping[r['id_persona']]['id_parlant'] for r in occ if r['forma']==form})
  n=sum(1 for r in occ if r['forma']==form)
  traits.append({'forma':form,'n_parlants':len(speakers),'comptatge_total':n,'parlants':','.join(speakers),'estat':'tokenització small agrupada per persona canònica; pendent d’audició'})
 with (GRAFO/'trets-small-token-canonics.tsv').open('w',encoding='utf-8',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(traits[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(traits)
 edges=[]
 for a,b in combinations(sorted(by),2):
  shared=sorted(by[a]&by[b])
  if len(shared)>=3: edges.append({'id_a':a,'id_b':b,'n_formes_compartides':len(shared),'formes':','.join(shared),'estat':'semblança textual small; no és relació dialectal; pendent d’audició'})
 with (GRAFO/'arestes-parlants-small-token-canonics.tsv').open('w',encoding='utf-8',newline='') as h:
  fields=list(edges[0]) if edges else ['id_a','id_b','n_formes_compartides','formes','estat'];w=csv.DictWriter(h,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(edges)
 nodes=[]
 for sp in sorted(people):
  fs=sorted(by.get(sp,set())); total=sum(counts[(sp,f)] for f in fs)
  nodes.append({'id_parlant':sp,'nom_public':people[sp]['nom_public'],'n_mostres':people[sp]['n_mostres'],'n_formes':len(fs),'n_ocurrencies':total,'formes':','.join(fs),'estat':'perfil small agrupat; pendent d’audició'})
 with (GRAFO/'nodes-small-token-canonics.tsv').open('w',encoding='utf-8',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(nodes[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(nodes)
 matrix=[]
 forms=sorted({r['forma'] for r in occ})
 for sp in sorted(people):
  for form in forms:
   n=counts[(sp,form)];matrix.append({'id_parlant':sp,'forma':form,'n_ocurrencies':n,'present':'sí' if n else 'no','estat':'small; pendent d’audició'})
 with (GRAFO/'matriu-formes-small-token-canonics.tsv').open('w',encoding='utf-8',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(matrix[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(matrix)
 lines=['graph TD']
 for e in sorted(edges,key=lambda x:(-x['n_formes_compartides'],x['id_a'],x['id_b'])):
  if e['n_formes_compartides']>=4: lines.append(f"  {e['id_a']}[{people[e['id_a']]['nom_public']}] ---|{e['n_formes_compartides']} formes| {e['id_b']}[{people[e['id_b']]['nom_public']}]")
 (GRAFO/'graf-parlants-small-token-canonics.mmd').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 print(f"{len(nodes)} persones canòniques · {len(traits)} formes · {len(edges)} arestes >=3 · {sum(e['n_formes_compartides']>=4 for e in edges)} arestes Mermaid")
if __name__=='__main__':main()
