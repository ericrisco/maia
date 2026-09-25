"""Descodifica la mostra equilibrada amb el model base i conserva JSON/TXT."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import csv, re, subprocess, unicodedata

ROOT = Path(__file__).parents[1]
PROV = ROOT / "proveniencia"
MODEL = Path("/Users/ericrisco/.codex/local-maia-models/ggml-base.bin")
OUT = PROV / "qa-equilibrada-base"
TSV = PROV / "qa-equilibrada-base.tsv"

def stem(row):
    return re.sub(r"[^a-zA-Z0-9_\-]+", "_", row["clip"].replace("clips/", "").replace(".wav", ""))

def norm(s):
    s=unicodedata.normalize("NFD",s.lower())
    return "".join(ch for ch in s if unicodedata.category(ch)!="Mn")

def run(row):
    prefix=OUT/stem(row)
    json_path=prefix.with_suffix('.json'); txt_path=prefix.with_suffix('.txt'); log=prefix.with_suffix('.log')
    if not json_path.exists() or not txt_path.exists():
        cmd=["whisper-cli","-m",str(MODEL),"-l","ca","-t","8","-mc","0","-bs","5","-bo","5","-nf","-oj","-ojf","-otxt","-of",str(prefix),str(PROV/row["clip"])]
        with log.open('w',encoding='utf-8') as h:
            result=subprocess.run(cmd,stdout=h,stderr=subprocess.STDOUT)
        if result.returncode:
            raise RuntimeError(f"fallada base {row['id_persona']} {row['forma']}")
    text=txt_path.read_text(encoding='utf-8',errors='replace').strip()
    words=re.findall(r"[\w]+(?:[’']\w+)?", norm(text))
    target=re.findall(r"[\w]+(?:[’']\w+)?", norm(row['forma']))
    found=any(words[i:i+len(target)]==target for i in range(max(0,len(words)-len(target)+1)))
    return {"id_persona":row["id_persona"],"forma":row["forma"],"clip":row["clip"],"prob_small":row["prob_min"],"text_small":row["text"],"text_base":text,"forma_en_base":"sí" if found else "no","json_base":f"qa-equilibrada-base/{json_path.name}","txt_base":f"qa-equilibrada-base/{txt_path.name}","estat":"pendent-audicio"}

def main():
    with (PROV/'cua-audicio-small-equilibrada.tsv').open(encoding='utf-8',newline='') as h:
        rows=list(csv.DictReader(h,delimiter='\t'))
    OUT.mkdir(exist_ok=True)
    result={}
    with ThreadPoolExecutor(max_workers=4) as ex:
        futures={ex.submit(run,row):(row['id_persona'],row['forma'],row['clip']) for row in rows}
        for f in as_completed(futures): result[futures[f]]=f.result()
    fields=['id_persona','forma','clip','prob_small','text_small','text_base','forma_en_base','json_base','txt_base','estat']
    with TSV.open('w',encoding='utf-8',newline='') as h:
        w=csv.DictWriter(h,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader()
        for row in rows:w.writerow(result[(row['id_persona'],row['forma'],row['clip'])])
    matches=sum(r['forma_en_base']=='sí' for r in result.values())
    print(f"{len(rows)} clips base · {matches} coincidències textuals · {len(rows)-matches} divergències")

if __name__=='__main__':main()
