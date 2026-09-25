
from pathlib import Path
import csv, math
import numpy as np
ROOT=Path(__file__).parents[1]
FEATURES=["rms_p10_db","rms_p90_db","zcr_p10","zcr_p90","f0_iqr_hz","f0_sd_hz","centroid_median_hz","centroid_p90_hz","durada_veu_mediana_s","pausa_veu_mediana_s"]
def main():
 rows=[]
 with (ROOT/"proveniencia/analisi-acustica-densa.tsv").open(encoding="utf-8",newline="") as h:
  for r in csv.DictReader(h,delimiter="\t"):
   if r["estat"]!="quarantena-asr": rows.append(r)
 x=np.asarray([[float(r[f]) for f in FEATURES] for r in rows],float)
 med=np.nanmedian(x,axis=0); scale=np.nanmedian(np.abs(x-med),axis=0); scale[scale==0]=1
 z=(x-med)/scale
 outrows=[]
 for i,r in enumerate(rows):
  d=np.sqrt(np.sum((z-z[i])**2,axis=1)); order=np.argsort(d)
  for j in order[1:4]:
   a,b=sorted((r["id_persona"],rows[j]["id_persona"]))
   if any(q["id_a"]==a and q["id_b"]==b for q in outrows): continue
   outrows.append({"id_a":a,"id_b":b,"distancia_mad":f"{d[j]:.3f}","features":";".join(FEATURES),"nota":"veïnatge acústic exploratori; no és semblança dialectal"})
 out=ROOT/"grafo/arestes-acustica-densa.tsv"
 with out.open("w",encoding="utf-8",newline="") as h:
  w=csv.DictWriter(h,fieldnames=list(outrows[0]),delimiter="\t",lineterminator="\n");w.writeheader();w.writerows(outrows)
 print(f"{len(rows)} veus · {len(outrows)} arestes · {out}")
if __name__=="__main__":main()

