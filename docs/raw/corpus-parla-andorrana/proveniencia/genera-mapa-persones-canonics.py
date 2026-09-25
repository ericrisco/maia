"""Agrupa registres de font que corresponen a la mateixa persona."""
from collections import defaultdict
from pathlib import Path
import csv
ROOT=Path(__file__).parents[1]; OUT=ROOT/'proveniencia/persones-canonics.tsv'

def main():
 with (ROOT/'persones.tsv').open(encoding='utf-8',newline='') as h: rows=list(csv.DictReader(h,delimiter='\t'))
 groups=defaultdict(list)
 for row in rows: groups[row['nom_public'].strip()].append(row)
 canonical={name:f'spk-{i:03d}' for i,name in enumerate(sorted(groups),1)}
 fields=['id_persona','id_parlant','nom_public','n_mostres','mostres_id','font_principal','estat_font']
 out=[]
 for row in rows:
  group=groups[row['nom_public'].strip()]
  out.append({'id_persona':row['id_persona'],'id_parlant':canonical[row['nom_public'].strip()],'nom_public':row['nom_public'],'n_mostres':str(len(group)),'mostres_id':','.join(r['id_persona'] for r in group),'font_principal':row['font_principal'],'estat_font':'registre de font; agrupació nominal exacta'})
 with OUT.open('w',encoding='utf-8',newline='') as h:
  w=csv.DictWriter(h,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(out)
 print(f'{len(rows)} registres · {len(groups)} persones canòniques · {sum(len(v)>1 for v in groups.values())} persones amb més d’una mostra')
if __name__=='__main__':main()
