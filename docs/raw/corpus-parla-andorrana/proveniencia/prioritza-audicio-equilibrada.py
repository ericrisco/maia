"""Ordena els 100 clips equilibrats per força de l'evidència automàtica."""
from collections import defaultdict
from pathlib import Path
import csv
ROOT=Path(__file__).parents[1]; PROV=ROOT/'proveniencia'; OUT=PROV/'prioritat-audicio-equilibrada.tsv'; MD=PROV/'quadern-audicio-equilibrada-prioritzat.md'
def read(n):
 with (PROV/n).open(encoding='utf-8',newline='') as h:return list(csv.DictReader(h,delimiter='\t'))
def main():
 sample=read('cua-audicio-small-equilibrada.tsv');cons={(r['id_persona'],r['forma'],r['clip']):r for r in read('qa-equilibrada-consens.tsv')}; form={(r['id_persona'],r['forma'],r['clip']):r for r in read('analisi-formants-base-equilibrada.tsv')}
 ranked=[]
 for r in sample:
  c=cons[(r['id_persona'],r['forma'],r['clip'])]; prob=float(r['prob_min']); dual=c['categoria']=='A-doble-coincidencia'
  if dual and prob>=.8: pri='A-doble-i-confiança-alta'; rank=1
  elif dual: pri='B-doble-i-confiança-baixa'; rank=2
  else: pri='C-divergència-small-base'; rank=3
  reason='small i base coincideixen; probabilitat small >= 0,80' if rank==1 else ('small i base coincideixen; probabilitat small < 0,80' if rank==2 else 'la forma només apareix al small; comparar amb l’àudio')
  row=dict(r);row.update({'categoria_base':c['categoria'],'prioritat':pri,'rang':rank,'justificacio':reason,'text_base':c['text_base'],'f0_base':form.get((r['id_persona'],r['forma'],r['clip']),{}).get('f0_hz',''),'f1_base':form.get((r['id_persona'],r['forma'],r['clip']),{}).get('f1_hz',''),'f2_base':form.get((r['id_persona'],r['forma'],r['clip']),{}).get('f2_hz',''),'f3_base':form.get((r['id_persona'],r['forma'],r['clip']),{}).get('f3_hz',''),'decisio_auditiva':'','variant_transcrita':'','trets_fonetica':'','observacions_prosodia':'','nota_audicio':''})
  ranked.append(row)
 ranked.sort(key=lambda r:(int(r['rang']),-float(r['prob_min']),r['id_persona'],float(r['absolute_start_s'])))
 for i,r in enumerate(ranked,1):r['ordre']=i
 fields=['ordre','rang','prioritat','categoria_base','id_persona','forma','clip','absolute_start_s','absolute_end_s','prob_min','text','text_base','f0_hz','f1_hz','f2_hz','f3_hz','f0_base','f1_base','f2_base','f3_base','justificacio','decisio_auditiva','variant_transcrita','trets_fonetica','observacions_prosodia','nota_audicio']
 with OUT.open('w',encoding='utf-8',newline='') as h:
  w=csv.DictWriter(h,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(ranked)
 groups=defaultdict(list)
 for r in ranked:groups[r['prioritat']].append(r)
 lines=['# Quadern d’audició prioritzat — mostra equilibrada','', 'Ordre de revisió dels 100 clips segons el doble ASR i la confiança. Les categories són prioritats de treball, no decisions lingüístiques.', '']
 for pri in ('A-doble-i-confiança-alta','B-doble-i-confiança-baixa','C-divergència-small-base'):
  lines += [f'## {pri}', '']
  for r in groups[pri]:
   name=Path(r['clip']).name
   lines.append(f"- **{r['id_persona']} · {r['forma']}** · [{name}](clips/{name}) · {r['absolute_start_s']}–{r['absolute_end_s']} s · p={r['prob_min']} · small: `{r['text']}` · base: `{r['text_base']}`")
  lines.append('')
 lines += ['## Camps humans','', 'Per a cada fila: decisió (`sí`, `no` o `incerta`), variant escoltada, trets fonètics, prosòdia i nota justificativa.']
 MD.write_text('\n'.join(lines),encoding='utf-8')
 from collections import Counter
 print(f"{len(ranked)} clips · {Counter(r['prioritat'] for r in ranked)}")
if __name__=='__main__':main()
