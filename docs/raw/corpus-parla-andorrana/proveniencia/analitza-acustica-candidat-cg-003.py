"""Calcula descriptors acústics orientatius per als clips de Roser Suñé."""
from __future__ import annotations
import csv, wave
from pathlib import Path
import numpy as np
ROOT=Path(__file__).parents[1]; CAND=ROOT/'proveniencia'/'candidats'/'lead-cg-003-roser-sune'; RATE=16000; FRAME=640; HOP=320; FFT=2048; THRESH=10**(-35/20)
def read_values(path):
 with wave.open(str(path),'rb') as a:
  ch,rate=a.getnchannels(),a.getframerate(); raw=a.readframes(a.getnframes())
 v=np.frombuffer(raw,dtype='<i2').astype(np.float32)/32768
 if ch>1:v=v.reshape(-1,ch).mean(axis=1)
 if rate!=RATE:raise ValueError(rate)
 return v
def pitch(frame):
 s=np.abs(np.fft.rfft(frame*np.hanning(len(frame)),n=FFT)); lo=int(70*FFT/RATE); hi=int(350*FFT/RATE); band=s[lo:hi+1]
 if not len(band) or not np.max(band):return None
 return (np.argmax(band)+lo)*RATE/FFT
def q(a,p):return float(np.percentile(a,p)) if len(a) else 0.0
def measure(row):
 v=read_values(CAND/row['clip']); fs=[v[i:i+FRAME] for i in range(0,max(0,len(v)-FRAME+1),HOP)] or [np.pad(v,(0,max(0,FRAME-len(v))))[:FRAME]]
 e=np.asarray([np.sqrt(np.mean(f*f)) for f in fs]); z=np.asarray([np.mean(f[:-1]*f[1:]<0) for f in fs]); voiced=e>=THRESH; f0=[]; cent=[]; freqs=np.fft.rfftfreq(FFT,1/RATE)
 for i,f in enumerate(fs):
  if i%2==0:
   sp=np.abs(np.fft.rfft(f*np.hanning(len(f)),n=FFT)); cent.append(float((freqs*sp).sum()/sp.sum()) if sp.sum() else 0)
   if voiced[i]:
    p=pitch(f)
    if p is not None:f0.append(p)
 runs=[]; start=None
 for i,x in enumerate(voiced):
  if x and start is None:start=i
  if not x and start is not None:runs.append((start,i));start=None
 if start is not None:runs.append((start,len(voiced)))
 pauses=[(b[0]-a[1])*HOP/RATE for a,b in zip(runs,runs[1:])]; db=lambda x:20*np.log10(max(float(x),1e-9))
 return {'forma':row['forma'],'segment':row['segment'],'clip':row['clip'],'inici_forma_s':row['inici_forma_s'],'final_forma_s':row['final_forma_s'],'durada_s':f'{len(v)/RATE:.3f}','veu_proporcio':f'{np.mean(voiced):.4f}','rms_p10_db':f'{db(q(e,10)):.2f}','rms_p50_db':f'{db(q(e,50)):.2f}','rms_p90_db':f'{db(q(e,90)):.2f}','zcr_p10':f'{q(z,10):.4f}','zcr_p90':f'{q(z,90):.4f}','f0_median_hz':f'{q(f0,50):.2f}','f0_iqr_hz':f'{q(f0,75)-q(f0,25):.2f}','centroid_median_hz':f'{q(cent,50):.2f}','centroid_p90_hz':f'{q(cent,90):.2f}','segments_veu':str(len(runs)),'pausa_mediana_s':f'{q(pauses,50):.3f}','mostres_f0':str(len(f0)),'estat':'descriptor orientatiu; pendent d’audició'}
def main():
 rows=[]
 with (CAND/'formes-clips.tsv').open(encoding='utf-8',newline='') as h:
  for r in csv.DictReader(h,delimiter='\t'):rows.append(measure(r))
 with (CAND/'analisi-acustica.tsv').open('w',encoding='utf-8',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
 lines=['# Perfil acústic — Roser Suñé','','Les mesures són descriptors instrumentals dels clips seleccionats. No substitueixen l’escolta ni permeten atribuir una variant dialectal.','', '| forma | durada | F0 mediana | F0 IQR | veu | pausa mediana |','|---|---:|---:|---:|---:|---:|']
 lines += [f"| `{r['forma']}` | {r['durada_s']} s | {r['f0_median_hz']} Hz | {r['f0_iqr_hz']} Hz | {r['veu_proporcio']} | {r['pausa_mediana_s']} s |" for r in rows]
 (CAND/'analisi-acustica.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 report=CAND/'informe.md'; s=report.read_text(encoding='utf-8'); marker='## Revisió preparada\n'; block='## Perfil acústic instrumental\n\n`analisi-acustica.tsv` i `analisi-acustica.md` conserven durada, proporció de veu, F0, energia, centroid espectral i pauses dels clips seleccionats. Són descriptors exploratoris; no substitueixen l’audició ni confirmen trets dialectals.\n\n';
 if '## Perfil acústic instrumental' not in s:report.write_text(s.replace(marker,block+marker,1),encoding='utf-8')
 print(f'{len(rows)} clips')
if __name__=='__main__':main()
