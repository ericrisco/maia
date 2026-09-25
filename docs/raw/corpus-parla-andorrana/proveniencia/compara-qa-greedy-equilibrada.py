"""Compara small, base i greedy dels 100 clips equilibrats."""
from collections import Counter
from pathlib import Path
import csv
ROOT=Path(__file__).parents[1];PROV=ROOT/'proveniencia'
def read(n):
 with (PROV/n).open(encoding='utf-8',newline='') as h:return list(csv.DictReader(h,delimiter='\t'))
def main():
 small={(r['id_persona'],r['forma'],r['clip']):r for r in read('qa-equilibrada-consens.tsv')};greedy={(r['id_persona'],r['forma'],r['clip']):r for r in read('qa-equilibrada-greedy.tsv')}
 out=[]
 for k,r in small.items():
  vals={'small':True,'base':r['categoria']=='A-doble-coincidencia','greedy':greedy[k]['forma_en_greedy']=='sí'};n=sum(vals.values());cat=('A-tres-models' if n==3 else 'B-dos-models' if n==2 else 'C-un-model' if n==1 else 'D-cap-model')
  out.append({'id_persona':r['id_persona'],'forma':r['forma'],'clip':r['clip'],'small':'sí','base':'sí' if vals['base'] else 'no','greedy':'sí' if vals['greedy'] else 'no','categoria':cat,'text_small':r['text_small'],'text_base':r['text_base'],'text_greedy':greedy[k]['text_greedy'],'decisio_audicio':''})
 fields=list(out[0])
 with (PROV/'qa-equilibrada-triple.tsv').open('w',encoding='utf-8',newline='') as h:
  w=csv.DictWriter(h,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(out)
 counts=Counter(r['categoria'] for r in out);lines=['# Comparació de tres descodificacions — mostra equilibrada','',f"La mostra conté **{len(out)} clips**. La tercera passada és greedy del model small; cap categoria substitueix l'escolta.",'','| Categoria | Clips |','|---|---:|']
 for c in ('A-tres-models','B-dos-models','C-un-model','D-cap-model'):lines.append(f'| {c} | {counts[c]} |')
 lines += ['', '## Casos que requereixen escolta prioritària','']
 for r in out:
  if r['categoria']!='A-tres-models':lines.append(f"- **{r['id_persona']} · {r['forma']}** ({r['categoria']}) · [{Path(r['clip']).name}](clips/{Path(r['clip']).name}) · small=`{r['text_small']}` · base=`{r['text_base']}` · greedy=`{r['text_greedy']}`")
 (PROV/'informe-qa-equilibrada-triple.md').write_text('\n'.join(lines)+'\n',encoding='utf-8');print(counts)
if __name__=='__main__':main()
