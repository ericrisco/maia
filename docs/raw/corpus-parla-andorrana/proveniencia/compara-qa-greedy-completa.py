"""Compara small, base i greedy per als 656 clips."""
from collections import Counter,defaultdict
from pathlib import Path
import csv
ROOT=Path(__file__).parents[1];PROV=ROOT/'proveniencia';MARKER='### Tercera descodificació greedy de la cua completa'
def read(n):
 with (PROV/n).open(encoding='utf-8',newline='') as h:return list(csv.DictReader(h,delimiter='\t'))
def replace_section(text,marker,section):
 if marker not in text:return text.rstrip()+'\n'+section
 start=text.index(marker);next_heading=text.find('\n### ',start+len(marker));end=len(text) if next_heading==-1 else next_heading+1
 return text[:start].rstrip()+'\n'+section.rstrip()+'\n\n'+text[end:].lstrip()
def main():
 master=read('clips-audicio.tsv');small={(r['id_persona'],r['forma']):r for r in read('qa-clips.tsv')};base={(r['id_persona'],r['forma']):r for r in read('qa-clips-base.tsv')};greedy={(r['id_persona'],r['forma']):r for r in read('qa-clips-greedy-full.tsv')};rows=[];by=defaultdict(Counter)
 for index,m in enumerate(master,1):
  k=(m['id_persona'],m['forma']);vals={'small':small[k]['forma_en_qa']=='sí','base':base[k]['forma_en_base']=='sí','greedy':greedy[k]['forma_en_greedy']=='sí'};n=sum(vals.values());cat='A-tres-models' if n==3 else 'B-dos-models' if n==2 else 'C-un-model' if n==1 else 'D-cap-model';out={'ordre':str(index),'id_persona':m['id_persona'],'forma':m['forma'],'clip':m['clip'],'small':'sí' if vals['small'] else 'no','base':'sí' if vals['base'] else 'no','greedy':'sí' if vals['greedy'] else 'no','categoria':cat,'text_small':small[k]['text_qa'],'text_base':base[k]['text_base'],'text_greedy':greedy[k]['text_greedy']};rows.append(out);by[m['id_persona']][cat]+=1
 fields=list(rows[0])
 with (PROV/'qa-clips-triple-full.tsv').open('w',encoding='utf-8',newline='') as h:
  w=csv.DictWriter(h,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
 counts=Counter(r['categoria'] for r in rows);lines=['# Comparació de tres descodificacions de la cua completa','',f"La cua conté **{len(rows)} clips**. La tercera passada és greedy del model small; cap categoria substitueix l'escolta humana.",'','| Categoria | Clips |','|---|---:|']
 for c in ('A-tres-models','B-dos-models','C-un-model','D-cap-model'):lines.append(f'| {c} | {counts[c]} |')
 lines += ['', '## Divergències que mereixen escolta prioritària','']
 for r in rows:
  if r['categoria']!='A-tres-models':lines.append(f"- **{r['id_persona']} · {r['forma']}** ({r['categoria']}) · `{r['clip']}` · small=`{r['text_small']}` · base=`{r['text_base']}` · greedy=`{r['text_greedy']}`")
 (PROV/'informe-qa-triple-complet.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 with (ROOT/'persones.tsv').open(encoding='utf-8',newline='') as h: people=[r['id_persona'] for r in csv.DictReader(h,delimiter='\t')]
 for pid in people:
  c=by.get(pid,Counter())
  report=ROOT/'persones'/f'{pid}.md';text=report.read_text(encoding='utf-8');details='; '.join(f'{x}={c[x]}' for x in ('A-tres-models','B-dos-models','C-un-model','D-cap-model') if c[x]) or 'cap clip'
  section=f"\n{MARKER}\n\nLa tercera passada greedy cobreix els 656 clips de la cua: en aquesta fitxa hi ha **{sum(c.values())}** casos ({details}). És evidència ASR i continua pendent d'escolta.\n"
  report.write_text(replace_section(text,MARKER,section),encoding='utf-8')
 print(' '.join(f'{k}={counts[k]}' for k in ('A-tres-models','B-dos-models','C-un-model','D-cap-model')))
if __name__=='__main__':main()
