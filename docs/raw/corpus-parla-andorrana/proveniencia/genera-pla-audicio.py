
from pathlib import Path
import csv
ROOT=Path(__file__).parents[1]
def main():
 rows=[]
 with (ROOT/"proveniencia/cua-audicio.tsv").open(encoding="utf-8",newline="") as h:
  for r in csv.DictReader(h,delimiter="\t"):
   score=(4 if r["consens_dos_asr"]=="sí" else 0)+(3 if r["coincidencia_temporal_asr"]=="sí" else 0)+(2 if r["prioritat_asr"]=="alta" else 0)
   r["prioritat_global"]=str(score)
   rows.append(r)
 rows.sort(key=lambda r:(-int(r["prioritat_global"]),r["id_persona"],r["forma"]))
 out=ROOT/"proveniencia/pla-audicio.tsv"
 with out.open("w",encoding="utf-8",newline="") as h:
  fields=list(rows[0]); w=csv.DictWriter(h,fieldnames=fields,delimiter="\t",lineterminator="\n");w.writeheader();w.writerows(rows)
 summary={}
 for r in rows:
  summary.setdefault(r["id_persona"],[]).append(r)
 md=["# Pla de revisió auditiva","", "La cua ordena els intervals segons consens entre ASR, coincidència temporal i prioritat de confiança. No hi ha cap veredicte humà encara.", ""]
 for pid,items in sorted(summary.items()):
  top=items[:3]
  md.append(f"## {pid}")
  md.append(" ; ".join(f"{x['forma']} ({x['prioritat_global']})" for x in top))
  md.append("")
 (ROOT/"proveniencia/pla-audicio.md").write_text("\n".join(md),encoding="utf-8")
 print(f"{len(rows)} intervals · {out}")
if __name__=="__main__":main()

