"""Mesura F0/F1/F2/F3 als clips del candidat RTVA."""
from __future__ import annotations
import csv,math
from pathlib import Path
from statistics import median
import parselmouth
ROOT=Path(__file__).parents[1]; CAND=ROOT/'proveniencia'/'candidats'/'lead-rtva-001'

def fmt(v): return f'{v:.2f}' if v is not None and math.isfinite(v) else ''
def main():
 rows=list(csv.DictReader((CAND/'formes-joan-clips.tsv').open(encoding='utf-8'),delimiter='\t')); out=[]
 for row in rows:
  snd=parselmouth.Sound(str(CAND/row['clip'])); form=snd.to_formant_burg(time_step=.005,max_number_of_formants=5,maximum_formant=5500,window_length=.025,pre_emphasis_from=50); pitch=snd.to_pitch(time_step=.005,pitch_floor=60,pitch_ceiling=500)
  center=(float(row['inici_forma_s'])+float(row['final_forma_s']))/2-float(row['inici_clip_s']); center=max(.015,min(snd.duration-.015,center))
  result={k:v for k,v in row.items() if k != 'estat'}; result['centre_rel_s']=f'{center:.3f}'
  try: result['f0_hz']=fmt(pitch.get_value_at_time(center))
  except Exception: result['f0_hz']=''
  for n in (1,2,3):
   try: result[f'f{n}_hz']=fmt(form.get_value_at_time(n,center))
   except Exception: result[f'f{n}_hz']=''
  result['estat_mesura']='mesura instrumental; pendent d’audició'; out.append(result)
 fields=[k for k in rows[0] if k != 'estat']+['centre_rel_s','f0_hz','f1_hz','f2_hz','f3_hz','estat_mesura']
 with (CAND/'formants.tsv').open('w',encoding='utf-8',newline='') as h:
  w=csv.DictWriter(h,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(out)
 lines=['# Mesures instrumentals — clips Joan Verdú','','Les mesures es prenen al centre temporal del candidat ASR en cada clip. Són sensibles a micròfon, coarticulació, veu de l’entrevistador i segmentació; no són una classificació dialectal.','', '| forma | F0 | F1 | F2 | F3 |','|---|---:|---:|---:|---:|']
 for r in out: lines.append(f"| `{r['forma']}` | {r['f0_hz'] or '—'} | {r['f1_hz'] or '—'} | {r['f2_hz'] or '—'} | {r['f3_hz'] or '—'} |")
 lines += ['', 'La taula completa és `formants.tsv`; qualsevol lectura fonètica requereix escolta i confirmació de la veu.']
 (CAND/'formants.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 report=CAND/'informe.md'; s=report.read_text(encoding='utf-8'); marker='## Següent revisió\n'; addition='## Mesures instrumentals\n\n`formants.tsv` i `formants.md` conserven F0/F1/F2/F3 dels 10 clips curts. Són mesures exploratòries i no permeten inferir el vocalisme de Joan sense audició.\n\n';
 if '## Mesures instrumentals' not in s: report.write_text(s.replace(marker,addition+marker,1),encoding='utf-8')
 print(f'{len(out)} clips · F0 {sum(bool(r["f0_hz"]) for r in out)} · F1 {sum(bool(r["f1_hz"]) for r in out)} · F2 {sum(bool(r["f2_hz"]) for r in out)} · F3 {sum(bool(r["f3_hz"]) for r in out)}')
if __name__=='__main__':main()
