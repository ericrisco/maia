"""Afegeix el resum de trajectòries base a les fitxes."""
from collections import defaultdict
from pathlib import Path
from statistics import median
import csv
ROOT=Path(__file__).parents[1];PROV=ROOT/'proveniencia';MARKER='### Trajectòries base de la mostra equilibrada'
def main():
 with (PROV/'analisi-trajectories-base-equilibrada.tsv').open(encoding='utf-8',newline='') as h:rows=list(csv.DictReader(h,delimiter='\t'))
 by=defaultdict(list)
 for r in rows:by[r['id_persona']].append(r)
 n=0
 for p in sorted((ROOT/'persones').glob('pa-*.md')):
  text=p.read_text(encoding='utf-8')
  if MARKER in text:text=text.split(MARKER,1)[0].rstrip()+'\n\n'
  items=by.get(p.stem,[])
  def med(k,point):
   vals=[float(r[k]) for r in items if r['punt']==point and r.get(k)];return f'{median(vals):.2f}' if vals else '—'
  if items:
   nt=len(items)//5;label='token' if nt==1 else 'tokens'; section=f"{MARKER}\n\nEn **{nt} {label}** amb coincidència textual small/base, les medianes instrumentals entre el primer i l'últim punt són F0 **{med('f0_hz','1')} → {med('f0_hz','5')} Hz**, F1 **{med('f1_hz','1')} → {med('f1_hz','5')} Hz**, F2 **{med('f2_hz','1')} → {med('f2_hz','5')} Hz** i F3 **{med('f3_hz','1')} → {med('f3_hz','5')} Hz**.\n\nLa trajectòria és exploratòria i sensible a coarticulació, durada, microfonia i segmentació; no és una decisió auditiva. La taula és `../proveniencia/analisi-trajectories-base-equilibrada.tsv`.\n"
  else:section=f"{MARKER}\n\nNo hi ha tokens small/base per mesurar trajectòries en aquesta fitxa.\n"
  p.write_text(text+'\n'+section,encoding='utf-8');n+=1
 print(f'OK: {n} informes actualitzats')
if __name__=='__main__':main()
