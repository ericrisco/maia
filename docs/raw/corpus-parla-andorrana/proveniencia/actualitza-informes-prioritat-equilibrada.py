"""Afegeix la prioritat de la cua equilibrada a cada fitxa."""
from collections import defaultdict
from pathlib import Path
import csv
ROOT=Path(__file__).parents[1]; PROV=ROOT/'proveniencia'; SRC=PROV/'prioritat-audicio-equilibrada.tsv'; MARKER='### Prioritat d’audició de la mostra equilibrada'
def main():
 with SRC.open(encoding='utf-8',newline='') as h: rows=list(csv.DictReader(h,delimiter='\t'))
 by=defaultdict(list)
 for r in rows:by[r['id_persona']].append(r)
 n=0
 for p in sorted((ROOT/'persones').glob('pa-*.md')):
  text=p.read_text(encoding='utf-8')
  if MARKER in text:text=text.split(MARKER,1)[0].rstrip()+'\n\n'
  rs=by.get(p.stem,[])
  counts=defaultdict(int)
  for r in rs:counts[r['prioritat']]+=1
  summary=', '.join(f'{k}={counts[k]}' for k in ('A-doble-i-confiança-alta','B-doble-i-confiança-baixa','C-divergència-small-base') if counts[k]) or 'sense clips'
  n_clips=len(rs); clip_label='clip' if n_clips == 1 else 'clips'
  lines=[MARKER,'',f"Aquesta fitxa té {n_clips} {clip_label} a la cua equilibrada: {summary}. L'ordre és una priorització automàtica; la decisió auditiva continua pendent.",'']
  for r in rs:
   lines.append(f"- ordre {r['ordre']} · **{r['forma']}** · prioritat {r['prioritat']} · [{Path(r['clip']).name}](../proveniencia/{r['clip']}) · p={r['prob_min']}")
  lines += ['', 'La justificació i els dos textos són a `../proveniencia/prioritat-audicio-equilibrada.tsv`.', '']
  p.write_text(text+'\n'.join(lines),encoding='utf-8');n+=1
 print(f'OK: {n} informes actualitzats')
if __name__=='__main__':main()
