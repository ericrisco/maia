
from pathlib import Path
import csv
from collections import defaultdict,Counter
from itertools import combinations
ROOT=Path(__file__).parents[1]
def parse(s):
 out=[]
 for part in (s or "").split(";"):
  if "=" in part:
   k,v=part.rsplit("=",1)
   try: out.append((k,int(v)))
   except ValueError: pass
 return out
def main():
 active={}; speaker_features=defaultdict(dict)
 with (ROOT/"persones.tsv").open(encoding="utf-8",newline="") as h:
  status={r["id_persona"]:r["estat"] for r in csv.DictReader(h,delimiter="\t")}
 with (ROOT/"proveniencia/analisi-linguistica.tsv").open(encoding="utf-8",newline="") as h:
  for r in csv.DictReader(h,delimiter="\t"):
   if r["estat"]=="quarantena-asr": continue
   for cat,col in [("discurs",r["marcadors"]),("territorial",r["formes_territorials"])]:
    for f,n in parse(col): speaker_features[r["id_persona"]][f]=(cat,n)
 with (ROOT/"proveniencia/evidencia-gramatica.tsv").open(encoding="utf-8",newline="") as h:
  counts=Counter((r["id_persona"],r["categoria"],r["forma"]) for r in csv.DictReader(h,delimiter="\t"))
 for (pid,category,form),n in counts.items():
  if status.get(pid)=="quarantena-asr": continue
  if pid not in speaker_features:
   speaker_features[pid]={}
  feature=f"{category}={form}"
  speaker_features[pid][feature]=("gramatica",n)
 counts=defaultdict(list)
 for pid,features in speaker_features.items():
  for f,(cat,n) in features.items(): counts[(cat,f)].append((pid,n))
 traits=[]
 for (cat,f),vals in sorted(counts.items()):
  if len(vals)>=3:
   traits.append({"categoria":cat,"forma":f,"parlants":",".join(x[0] for x in vals),"comptatge_total":str(sum(x[1] for x in vals)),"nota":"recompte ASR; revisió auditiva pendent"})
 out=ROOT/"grafo"/"trets-linguistics.tsv"
 with out.open("w",encoding="utf-8",newline="") as h:
  w=csv.DictWriter(h,fieldnames=list(traits[0]),delimiter="\t",lineterminator="\n");w.writeheader();w.writerows(traits)
 edges={}
 for a,b in combinations(sorted(speaker_features),2):
  shared=sorted(set(speaker_features[a])&set(speaker_features[b]))
  if len(shared)>=3:
   edges[(a,b)]={"id_a":a,"id_b":b,"formes_compartides":str(len(shared)),"formes":";".join(shared),"nota":"semblança textual ASR ampliada; no és classificació dialectal"}
 out2=ROOT/"grafo"/"arestes-linguistics.tsv"
 with out2.open("w",encoding="utf-8",newline="") as h:
  rows=list(edges.values()); w=csv.DictWriter(h,fieldnames=list(rows[0]),delimiter="\t",lineterminator="\n");w.writeheader();w.writerows(rows)
 print(f"{len(traits)} trets · {len(edges)} arestes · {len(speaker_features)} veus actives")
if __name__=="__main__":main()
