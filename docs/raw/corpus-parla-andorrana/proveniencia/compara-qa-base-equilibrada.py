"""Compara la transcripció small de la mostra amb la passada base."""
from collections import Counter, defaultdict
from pathlib import Path
import csv

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
SRC = PROV / "qa-equilibrada-base.tsv"
OUT = PROV / "qa-equilibrada-consens.tsv"

def main():
    with SRC.open(encoding='utf-8',newline='') as h: rows=list(csv.DictReader(h,delimiter='\t'))
    fields=['ordre','id_persona','forma','clip','prob_small','text_small','text_base','forma_en_base','categoria','decisio_audicio']
    out=[]
    for i,row in enumerate(rows,1):
        base=row['forma_en_base']=='sí'
        out.append({'ordre':i,'id_persona':row['id_persona'],'forma':row['forma'],'clip':row['clip'],'prob_small':row['prob_small'],'text_small':row['text_small'],'text_base':row['text_base'],'forma_en_base':row['forma_en_base'],'categoria':'A-doble-coincidencia' if base else 'B-small-only','decisio_audicio':''})
    with OUT.open('w',encoding='utf-8',newline='') as h:
        w=csv.DictWriter(h,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(out)
    print('OK',len(out),'files',Counter(r['categoria'] for r in out))

if __name__=='__main__':main()
