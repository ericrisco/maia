"""Afegeix context automàtic als 35 clips candidats de la sessió 01."""
from __future__ import annotations
import csv,json
from pathlib import Path
ROOT=Path(__file__).parents[1]; PROV=ROOT/'proveniencia'
SPECS={
 'lead-rtva-001':('formes-joan-clips.tsv','joan-verdu'),
 'lead-rtva-002-ian-moya':('formes-clips.tsv','ian-moya'),
 'lead-rtva-003-dj-neura':('formes-clips.tsv','dj-neura'),
}
def read(p):
 with p.open(encoding='utf-8',newline='') as h:return list(csv.DictReader(h,delimiter='\t'))
def secs(v):
 h,m,s=v.replace(',','.').split(':');return int(h)*3600+int(m)*60+float(s)
def segs(p):
 out=[]
 for i,x in enumerate(json.loads(p.read_text(encoding='utf-8')).get('transcription',[]),1):
  t=x.get('text','').strip()
  if t and t!='#':out.append({'n':i,'start':secs(x['timestamps']['from']),'end':secs(x['timestamps']['to']),'text':t})
 return out
def main():
 session=PROV/'sessions'/'sessio-01.tsv'; rows=read(session); cache={}
 for folder,(manifest_name,stem) in SPECS.items():
  cand=PROV/'candidats'/folder; manifest=read(cand/manifest_name); by_clip={r['clip']:r for r in manifest}; small=segs(cand/'asr'/f'{stem}.json'); base=segs(cand/'asr'/f'{stem}-base.json'); prov={r['segment']:r for r in read(cand/'segments-speaker-provisional.tsv')}; acoustic={r['clip']:r for r in read(cand/'analisi-acustica.tsv')}; formants={r['clip']:r for r in read(cand/'formants.tsv')}
  cache[folder]=(by_clip,small,base,prov,acoustic,formants)
 out=[]
 for row in rows:
  folder=row['id_global'].split('::',1)[0] if row['id_global'].startswith('lead-') else ''
  if folder not in cache:out.append(row);continue
  by_clip,small,base,prov,acoustic,formants=cache[folder]; clip=row['clip'].split(f'candidats/{folder}/',1)[-1]; manifest=by_clip.get(clip,{})
  try:segno=int(manifest.get('segment','0'))
  except:segno=0
  sr=next((x for x in small if x['n']==segno),{});br=min(base,key=lambda x:abs(x['start']-sr.get('start',0))) if base and sr else {}; pr=prov.get(str(segno),{}); ar=acoustic.get(clip,{}); fr=formants.get(clip,{})
  row.update({'text_small':sr.get('text',''),'text_base':br.get('text',''),'rol_provisional':pr.get('rol_provisional',''),'motiu_rol':pr.get('motiu',''),'f0_median_hz':ar.get('f0_median_hz',''),'f0_iqr_hz':ar.get('f0_iqr_hz',''),'pausa_mediana_s':ar.get('pausa_mediana_s',''),'f1_hz':fr.get('f1_hz',''),'f2_hz':fr.get('f2_hz',''),'f3_hz':fr.get('f3_hz',''),'estat_instrumental':'suport automàtic; pendent d’audició'})
  out.append(row)
 fields=list(out[0]); extra=['text_small','text_base','rol_provisional','motiu_rol','f0_median_hz','f0_iqr_hz','pausa_mediana_s','f1_hz','f2_hz','f3_hz','estat_instrumental']; fields += [x for x in extra if x not in fields]
 with session.open('w',encoding='utf-8',newline='') as h:
  w=csv.DictWriter(h,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(out)
 print('sessio-01',sum(bool(r.get('text_small')) for r in out),'files candidats enriquides')
if __name__=='__main__':main()
