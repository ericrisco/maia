
"""Resume patrons lingüístics observables en les transcripcions ASR.

Les comptabilitats són candidats textuals i no validen variants dialectals.
"""
from __future__ import annotations
import csv,re,unicodedata
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).parents[1]
MARKERS=["bé","bueno","clar","doncs","llavors","aleshores","de fet","és a dir","o sigui","vull dir","a veure","aviam","diguem","evidentment","perquè","per tant","a nivell","no?"]
TERRITORIAL=["andorrà","andorrana","parròquia","comú","comuns","copríncep","coprínceps","veguer","vegueria","comunal","comunals","bordes","ramat","pastura","aiguat","aiguats","santuari","padrí","pagesia","Canillo","Encamp","Ordino","Escaldes","Massana","Sant Julià"]
CLITICS=["em","m","me","ens","el","la","els","les","ho","hi","en","n","se","es"]
def norm(s): return unicodedata.normalize("NFC",s.lower())
def count(t,f): return len(re.findall(r"(?i)(?<!\w)"+re.escape(f)+r"(?!\w)",t))
def main():
 status={}
 with (ROOT/"persones.tsv").open(encoding="utf-8",newline="") as h:
  for r in csv.DictReader(h,delimiter="\t"): status[r["id_persona"]]=r["estat"]
 rows=[]
 for pid in sorted(status):
  text=norm((ROOT/"transcripcions"/f"{pid}.txt").read_text(encoding="utf-8",errors="ignore"))
  words=re.findall(r"[a-zàèéíïòóúüç·']+",text)
  bare=[w.strip("'·") for w in words if w.strip("'·")]
  grams=Counter(tuple(bare[i:i+3]) for i in range(max(0,len(bare)-2)))
  repeated=sum(n-1 for n in grams.values() if n>1)
  marker=";".join(f"{m}={count(text,m)}" for m in MARKERS if count(text,m))
  terr=";".join(f"{m}={count(text,m)}" for m in TERRITORIAL if count(text,m))
  clitic=sum(sum(w==c or w.startswith(c+"'") for w in bare) for c in CLITICS)
  past=sum(1 for i,w in enumerate(bare[:-1]) if w in {"vaig","vas","va","vam","vau","van"} and re.match(r"^[a-zàèéíïòóúüç·']+$",bare[i+1]))
  first=sum(count(text,x) for x in ["jo","jo me","nosaltres","nos","me'n","m'"])
  neg=sum(count(text,x) for x in ["no","mai","tampoc"])
  rows.append({"id_persona":pid,"estat":status[pid],"tokens":str(len(bare)),"tipus_lexics":str(len(set(bare))),"type_token_ratio":f"{len(set(bare))/len(bare):.4f}" if bare else "0","repeticio_3gram":f"{repeated/max(len(grams),1):.4f}","marcadors":marker,"formes_territorials":terr,"pronoms_clitics":str(clitic),"perifrasi_past_aparent":str(past),"primera_persona":str(first),"negacio":str(neg),"nota":"recompte ASR; validar contra àudio"})
 out=ROOT/"proveniencia"/"analisi-linguistica.tsv"
 with out.open("w",encoding="utf-8",newline="") as h:
  w=csv.DictWriter(h,fieldnames=list(rows[0]),delimiter="\t",lineterminator="\n");w.writeheader();w.writerows(rows)
 print(f"{len(rows)} persones · {out}")
if __name__=="__main__":main()

