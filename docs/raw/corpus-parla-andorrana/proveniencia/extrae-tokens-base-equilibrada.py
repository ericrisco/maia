"""Localitza timestamps dels tokens que el model base reconeix a la mostra."""
from pathlib import Path
import csv,json,re,unicodedata
ROOT=Path(__file__).parents[1]; PROV=ROOT/'proveniencia'

def norm(s):
 s=unicodedata.normalize('NFD',s.lower()); return ''.join(c for c in s if unicodedata.category(c)!='Mn')
def words(tokens):
 out=[]
 for tok in tokens:
  text=tok.get('text','')
  if text.startswith(('[_', '<|')) or not re.search(r'\w',text): continue
  item={'text':text.strip(),'p':float(tok.get('p',0)),'from':int(tok['offsets']['from']),'to':int(tok['offsets']['to'])}
  if text.startswith(' ') or not out: out.append(item)
  else:
   out[-1]['text']=(out[-1]['text']+text).strip();out[-1]['p']=min(out[-1]['p'],item['p']);out[-1]['to']=item['to']
 return out
def clip_start(clip):
 m=re.search(r'__([0-9]+(?:\.[0-9]+)?)\.wav$',clip); return float(m.group(1)) if m else 0.0

def main():
 with (PROV/'qa-equilibrada-base.tsv').open(encoding='utf-8',newline='') as h: rows=list(csv.DictReader(h,delimiter='\t'))
 occurrences=[]; summary=[]
 for row in rows:
  payload=json.loads((PROV/row['json_base']).read_text(encoding='utf-8'))
  target=norm(row['forma']); matches=[]
  for seg in payload.get('transcription',[]):
   seq=words(seg.get('tokens',[]))
   for i in range(len(seq)):
    for j in range(i+1,min(len(seq),i+4)+1):
     text=' '.join(str(x['text']) for x in seq[i:j])
     if norm(text)!=target: continue
     local_start=float(seq[i]['from'])/1000; local_end=float(seq[j-1]['to'])/1000
     m={'occurrence':len(matches)+1,'local_start_s':f'{local_start:.3f}','local_end_s':f'{local_end:.3f}','absolute_start_s':f'{clip_start(row["clip"])+local_start:.3f}','absolute_end_s':f'{clip_start(row["clip"])+local_end:.3f}','prob_min':f'{min(float(x["p"]) for x in seq[i:j]):.4f}','text':text}
     matches.append(m); occurrences.append({'id_persona':row['id_persona'],'forma':row['forma'],'clip':row['clip'],**m})
  summary.append({'id_persona':row['id_persona'],'forma':row['forma'],'clip':row['clip'],'n_matches':str(len(matches)),'token_match':'sí' if matches else 'no'})
 fields=['id_persona','forma','clip','n_matches','token_match']
 with (PROV/'qa-equilibrada-base-tokens.tsv').open('w',encoding='utf-8',newline='') as h:
  w=csv.DictWriter(h,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(summary)
 fields2=['id_persona','forma','clip','occurrence','local_start_s','local_end_s','absolute_start_s','absolute_end_s','prob_min','text']
 with (PROV/'qa-equilibrada-base-token-occurrences.tsv').open('w',encoding='utf-8',newline='') as h:
  w=csv.DictWriter(h,fieldnames=fields2,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(occurrences)
 print(f'{len(summary)} clips · {sum(r["token_match"]=="sí" for r in summary)} amb token · {len(occurrences)} ocurrències')
if __name__=='__main__':main()
