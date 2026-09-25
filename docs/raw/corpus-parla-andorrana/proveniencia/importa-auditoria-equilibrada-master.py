"""Projecta anotacions de la mostra equilibrada al registre mestre.

Només accepta coincidències exactes per (persona, forma, clip). Per defecte
simula; --write és necessari per modificar registre-audicio.tsv.
"""
from __future__ import annotations
import argparse,csv
from pathlib import Path
ROOT=Path(__file__).parents[1]; PROV=ROOT/'proveniencia'; TARGET=PROV/'registre-audicio.tsv'
STATUS={'sí':('confirmada','sí'),'no':('descartada','no'),'incerta':('incerta','incerta'),'pendent':('pendent','')}
def main():
 p=argparse.ArgumentParser();p.add_argument('tsv',type=Path);p.add_argument('--write',action='store_true');args=p.parse_args()
 with args.tsv.open(encoding='utf-8',newline='') as h: annotations=list(csv.DictReader(h,delimiter='\t'))
 with TARGET.open(encoding='utf-8',newline='') as h: reader=csv.DictReader(h,delimiter='\t'); rows=list(reader); fields=reader.fieldnames or []
 by={(r['id_persona'],r['forma'],r['clip']):r for r in rows}; updates=[];errors=[]
 for note in annotations:
  pid=note.get('person') or note.get('id_persona',''); form=note.get('form') or note.get('forma',''); clip=note.get('clip',''); key=(pid,form,clip); target=by.get(key)
  if target is None: errors.append(f'no hi ha coincidència exacta: {key}');continue
  status=note.get('status') or note.get('decisio_auditiva','') or 'pendent'
  if status in ('sí','no','incerta'): mapped=status
  elif status in ('confirmada','descartada'): mapped={'confirmada':'sí','descartada':'no'}[status]
  elif status in ('pendent',''): mapped='pendent'
  else: errors.append(f'estat desconegut {status!r}: {key}');continue
  state,confirmed=STATUS[mapped]
  values={'estat_audicio':state,'forma_confirmada_auditivament':confirmed,'variant_transcrita':note.get('variant') or note.get('variant_transcrita',''),'trets_fonetics_observats':note.get('phon') or note.get('trets_fonetics_observats',''),'observacions_prosodiques':note.get('pros') or note.get('observacions_prosodiques',''),'nota_audicio':note.get('note') or note.get('nota_audicio','')}
  # Only fields present in the master are projected.
  changed=False
  for field,value in values.items():
   current=target.get(field, '')
   pending_state = field == 'estat_audicio' and current in ('', 'pendent', 'pendent-audicio')
   if field in fields and value and current not in ('', value) and not pending_state: errors.append(f'conflicte a {field}: {key}');break
   if field in fields and current!=value: changed=True
  else: updates.append((target,values,changed))
 if errors:
  for e in errors: print('ERROR:',e)
  raise SystemExit(1)
 changed=0
 for target,values,did in updates:
  if did:
   for field,value in values.items():
    if field in fields: target[field]=value
   changed+=1
 print(f'anotacions llegides: {len(annotations)}; coincidències exactes: {len(updates)}; canvis: {changed}')
 if not args.write:
  print('simulació: usa --write per modificar registre-audicio.tsv');return
 with TARGET.open('w',encoding='utf-8',newline='') as h:
  w=csv.DictWriter(h,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
 print(f'escrit {TARGET}')
if __name__=='__main__':main()
