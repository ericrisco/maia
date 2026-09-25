"""Mesura F0/F1/F2/F3 als clips dels candidats audiovisuals."""
from __future__ import annotations
import csv, math
from pathlib import Path
import parselmouth
ROOT=Path(__file__).parents[1]
CANDIDATES=[('lead-rtva-002-ian-moya','Ian Moya'),('lead-rtva-003-dj-neura','DJ Neura'),('lead-rtva-004-joan-mico','Joan Micó'),('lead-cg-001-xavier-espot','Xavier Espot')]
def fmt(v): return f'{v:.2f}' if v is not None and math.isfinite(v) else ''
def process(folder,label):
 cand=ROOT/'proveniencia'/'candidats'/folder
 rows=list(csv.DictReader((cand/'formes-clips.tsv').open(encoding='utf-8'),delimiter='\t')); out=[]
 for row in rows:
  snd=parselmouth.Sound(str(cand/row['clip']))
  form=snd.to_formant_burg(time_step=.005,max_number_of_formants=5,maximum_formant=5500,window_length=.025,pre_emphasis_from=50)
  pitch=snd.to_pitch(time_step=.005,pitch_floor=60,pitch_ceiling=500)
  center=(float(row['inici_forma_s'])+float(row['final_forma_s']))/2-float(row['inici_clip_s'])
  center=max(.015,min(snd.duration-.015,center))
  result={k:v for k,v in row.items() if k != 'estat'}; result['centre_rel_s']=f'{center:.3f}'
  try: result['f0_hz']=fmt(pitch.get_value_at_time(center))
  except Exception: result['f0_hz']=''
  for n in (1,2,3):
   try: result[f'f{n}_hz']=fmt(form.get_value_at_time(n,center))
   except Exception: result[f'f{n}_hz']=''
  result['estat_mesura']='mesura instrumental; pendent d’audició'; out.append(result)
 fields=[k for k in rows[0] if k != 'estat']+['centre_rel_s','f0_hz','f1_hz','f2_hz','f3_hz','estat_mesura']
 with (cand/'formants.tsv').open('w',encoding='utf-8',newline='') as h:
  w=csv.DictWriter(h,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(out)
 lines=[f'# Mesures instrumentals — clips {label}','', 'Les mesures es prenen al centre temporal de cada clip ASR. Són sensibles al micròfon, la coarticulació, la veu d’altres torns i la segmentació; no són una classificació dialectal.','', '| forma | F0 | F1 | F2 | F3 |','|---|---:|---:|---:|---:|']
 lines += [f"| `{r['forma']}` | {r['f0_hz'] or '—'} | {r['f1_hz'] or '—'} | {r['f2_hz'] or '—'} | {r['f3_hz'] or '—'} |" for r in out]
 lines += ['', 'La taula completa és `formants.tsv`; qualsevol lectura fonètica requereix escolta i confirmació de la veu.']
 (cand/'formants.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 report=cand/'informe.md'; s=report.read_text(encoding='utf-8')
 if '## Mesures formàntiques instrumentals' not in s:
  marker='## Revisió preparada\n'; block=f"## Mesures formàntiques instrumentals\n\n`formants.tsv` i `formants.md` conserven F0/F1/F2/F3 dels {len(out)} clips. Són mesures exploratòries i no permeten inferir el vocalisme de {label} sense audició.\n\n"
  report.write_text(s.replace(marker,block+marker,1),encoding='utf-8')
 return len(out),sum(bool(r['f0_hz']) for r in out),sum(bool(r['f1_hz']) for r in out),sum(bool(r['f2_hz']) for r in out),sum(bool(r['f3_hz']) for r in out)
def main():
 for spec in CANDIDATES: print(spec[1], process(*spec))
if __name__=='__main__':main()
