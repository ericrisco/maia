"""Copia el resum formàntic base de la mostra equilibrada a les fitxes."""
from collections import defaultdict
from pathlib import Path
from statistics import median
import csv
ROOT=Path(__file__).parents[1];PROV=ROOT/'proveniencia';MARKER='### Formants base de coincidències small/base'
def main():
 with (PROV/'analisi-formants-base-equilibrada.tsv').open(encoding='utf-8',newline='') as h: rows=list(csv.DictReader(h,delimiter='\t'))
 by=defaultdict(list)
 for r in rows:by[r['id_persona']].append(r)
 n=0
 for p in sorted((ROOT/'persones').glob('pa-*.md')):
  text=p.read_text(encoding='utf-8')
  if MARKER in text:text=text.split(MARKER,1)[0].rstrip()+'\n\n'
  items=by.get(p.stem,[])
  def med(k):
   vals=[float(r[k]) for r in items if r.get(k)];return f'{median(vals):.2f}' if vals else '—'
  if items:
   n_tokens=len(items); token_label='token' if n_tokens == 1 else 'tokens'
   section=f"{MARKER}\n\nAquesta fitxa té **{n_tokens} {token_label}** on small i base coincideixen textualment. Les medianes instrumentals són F0 **{med('f0_hz')} Hz**, F1 **{med('f1_hz')} Hz**, F2 **{med('f2_hz')} Hz** i F3 **{med('f3_hz')} Hz**. Són mesures acústiques exploratòries del mateix clip i continuen pendents d'audició.\n\nLa taula és `../proveniencia/analisi-formants-base-equilibrada.tsv`; el resum per forma és `../proveniencia/resum-formants-base-equilibrada.tsv`.\n"
  else: section=f"{MARKER}\n\nAquesta fitxa no té tokens amb coincidència small/base dins la mostra equilibrada.\n"
  p.write_text(text+'\n'+section,encoding='utf-8');n+=1
 print(f'OK: {n} informes actualitzats')
if __name__=='__main__':main()
