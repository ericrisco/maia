"""Afegeix context ASR i mesures instrumentals a les sessions de candidats."""
from __future__ import annotations
import csv,json
from pathlib import Path
ROOT=Path(__file__).parents[1]; PROV=ROOT/'proveniencia'
SPECS=[('sessio-03.tsv','lead-rtva-004-joan-mico','joan-mico'),('sessio-04.tsv','lead-cg-001-xavier-espot','xavier-espot')]
def read(p):
 with p.open(encoding='utf-8',newline='') as h:return list(csv.DictReader(h,delimiter='\t'))
def secs(v):
 h,m,s=v.replace(',','.').split(':');return int(h)*3600+int(m)*60+float(s)
def segments(p):
 data=json.loads(p.read_text(encoding='utf-8'))
 out=[]
 for i,x in enumerate(data.get('transcription',[]),1):
  text=x.get('text','').strip()
  if text and text!='#':out.append({'n':i,'start':secs(x['timestamps']['from']),'end':secs(x['timestamps']['to']),'text':text})
 return out
def main():
 for session,folder,stem in SPECS:
  cand=PROV/'candidats'/folder; rows=read(PROV/'sessions'/session)
  small=segments(cand/'asr'/f'{stem}.json'); base=segments(cand/'asr'/f'{stem}-base.json')
  prov={r['segment']:r for r in read(cand/'segments-speaker-provisional.tsv')}
  acoustic={r['clip']:r for r in read(cand/'analisi-acustica.tsv')}; formants={r['clip']:r for r in read(cand/'formants.tsv')}
  out=[]
  for row in rows:
   clip=row['clip'].split(f'candidats/{folder}/',1)[-1]
   # session clip paths include candidate prefix; manifest clips are relative to candidate.
   manifest_clip=clip
   try: segno=int(next(x for x in read(cand/'formes-clips.tsv') if x['clip']==manifest_clip)['segment'])
   except StopIteration: segno=0
   sr=next((x for x in small if x['n']==segno),{})
   br=min(base,key=lambda x:abs(x['start']-sr.get('start',0))) if base and sr else {}
   ar=acoustic.get(manifest_clip,{ }); fr=formants.get(manifest_clip,{ }); pr=prov.get(str(segno),{})
   row.update({'text_small':sr.get('text',''),'text_base':br.get('text',''),'rol_provisional':pr.get('rol_provisional',''),'motiu_rol':pr.get('motiu',''),'f0_median_hz':ar.get('f0_median_hz',''),'f0_iqr_hz':ar.get('f0_iqr_hz',''),'pausa_mediana_s':ar.get('pausa_mediana_s',''),'f1_hz':fr.get('f1_hz',''),'f2_hz':fr.get('f2_hz',''),'f3_hz':fr.get('f3_hz',''),'estat_instrumental':'suport automàtic; pendent d’audició'})
   out.append(row)
  fields=list(out[0])
  with (PROV/'sessions'/session).open('w',encoding='utf-8',newline='') as h:
   w=csv.DictWriter(h,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(out)
  print(session,len(out))
if __name__=='__main__':main()
