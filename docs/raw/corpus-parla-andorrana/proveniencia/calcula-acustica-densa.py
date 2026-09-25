
"""Calcula descriptors acústicos densos para prioritzar l'escolta humana.

No són mesures dialectals: resumeixen energia, pauses, creuament per zero i
distribució espectral de cada WAV per seleccionar fragments comparables.
"""
from __future__ import annotations
import csv, subprocess
from pathlib import Path
import numpy as np
ROOT=Path(__file__).parents[1]
RATE=16000; FRAME=640; HOP=320; FFT=2048; THRESH=10**(-35/20)
def frames(path):
 p=subprocess.Popen(["ffmpeg","-hide_banner","-loglevel","error","-i",str(path),"-ac","1","-ar",str(RATE),"-f","s16le","-"],stdout=subprocess.PIPE)
 carry=np.empty(0,np.float32); assert p.stdout is not None
 while True:
  chunk=p.stdout.read(RATE*2)
  if not chunk: break
  a=np.frombuffer(chunk,dtype="<i2").astype(np.float32)/32768
  data=np.concatenate((carry,a))
  stop=((len(data)-FRAME)//HOP+1)*HOP if len(data)>=FRAME else 0
  for start in range(0,stop,HOP): yield data[start:start+FRAME]
  carry=data[stop:]
 p.wait()
 if p.returncode: raise RuntimeError(path)
def pitch(f):
 sp=np.abs(np.fft.rfft(f*np.hanning(len(f)),n=FFT)); lo=int(70*FFT/RATE); hi=int(350*FFT/RATE); band=sp[lo:hi+1]
 if not len(band) or float(np.max(band))<=0:return None
 i=int(np.argmax(band))+lo
 if 0<i<len(sp)-1:
  l,pk,r=sp[i-1:i+2]; den=l-2*pk+r; i+=0.5*(l-r)/den if den else 0
 return i*RATE/FFT
def measure(pid,status):
 rms=[]; zcr=[]; f0=[]; centroid=[]; voiced=[]
 for i,f in enumerate(frames(ROOT/"audios"/pid/"audio.wav")):
  e=float(np.sqrt(np.mean(f*f))); rms.append(e); zcr.append(float(np.mean(f[:-1]*f[1:]<0))); voiced.append(e>=THRESH)
  if i%5==0:
   q=np.abs(np.fft.rfft(f*np.hanning(len(f)),n=FFT)); fre=np.fft.rfftfreq(FFT,1/RATE); centroid.append(float((fre*q).sum()/q.sum()) if q.sum() else 0)
   if e>=THRESH:
    x=pitch(f)
    if x is not None:f0.append(x)
 v=np.asarray(voiced,dtype=bool); runs=[]; pauses=[]; start=None
 for i,on in enumerate(v):
  if on and start is None:start=i
  if not on and start is not None:runs.append((start,i));start=None
 if start is not None:runs.append((start,len(v)))
 for a,b in zip(runs,runs[1:]):pauses.append((b[0]-a[1])*HOP/RATE)
 return {"id_persona":pid,"estat":status,"rms_p10_db":f"{20*np.log10(max(np.percentile(rms,10),1e-9)):.2f}","rms_p90_db":f"{20*np.log10(max(np.percentile(rms,90),1e-9)):.2f}","zcr_p10":f"{np.percentile(zcr,10):.4f}","zcr_p90":f"{np.percentile(zcr,90):.4f}","f0_iqr_hz":f"{(np.percentile(f0,75)-np.percentile(f0,25)) if f0 else 0:.2f}","f0_sd_hz":f"{np.std(f0) if f0 else 0:.2f}","centroid_median_hz":f"{np.median(centroid) if centroid else 0:.2f}","centroid_p90_hz":f"{np.percentile(centroid,90) if centroid else 0:.2f}","segments_veu":str(len(runs)),"durada_veu_mediana_s":f"{np.median([(b-a)*HOP/RATE for a,b in runs]) if runs else 0:.2f}","pausa_veu_mediana_s":f"{np.median(pauses) if pauses else 0:.2f}","mostres_f0":str(len(f0))}
def main():
 status={}
 with (ROOT/"persones.tsv").open(encoding="utf-8",newline="") as h:
  for r in csv.DictReader(h,delimiter="\t"):status[r["id_persona"]]=r["estat"]
 rows=[measure(pid,status[pid]) for pid in sorted(status)]
 out=ROOT/"proveniencia"/"analisi-acustica-densa.tsv"
 with out.open("w",encoding="utf-8",newline="") as h:
  w=csv.DictWriter(h,fieldnames=list(rows[0]),delimiter="\t",lineterminator="\n");w.writeheader();w.writerows(rows)
 print(f"{len(rows)} àudios · {out}")
if __name__=="__main__":main()

