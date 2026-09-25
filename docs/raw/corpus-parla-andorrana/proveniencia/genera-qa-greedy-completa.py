"""Tercera descodificació greedy dels 656 clips de la cua mestra."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import csv,hashlib,re,subprocess,unicodedata
ROOT=Path(__file__).parents[1];PROV=ROOT/'proveniencia';OUT=PROV/'qa-clips-greedy-full';MODEL=Path('/Users/ericrisco/.codex/local-maia-models/ggml-small.bin')
def norm(s):
 s=unicodedata.normalize('NFD',s.lower());return ''.join(c for c in s if unicodedata.category(c)!='Mn')
def slug(s):return re.sub(r'[^a-z0-9]+','-',norm(s)).strip('-')
def run(r):
 prefix=OUT/f"{r['id_persona']}__{slug(r['forma'])}__{r['interval_escolta'].replace('.', '_').replace('-', '_')}";txt=prefix.with_suffix('.txt');log=prefix.with_suffix('.log')
 if not txt.exists():
  cmd=['whisper-cli','-m',str(MODEL),'-l','ca','-t','8','-mc','0','-bs','1','-bo','1','-nf','-otxt','-of',str(prefix),str(PROV/r['clip'])]
  with log.open('w',encoding='utf-8') as h:
   result=subprocess.run(cmd,stdout=h,stderr=subprocess.STDOUT)
  if result.returncode:raise RuntimeError(f'greedy ha fallat {r["id_persona"]} {r["forma"]}')
 text=txt.read_text(encoding='utf-8',errors='replace').strip().replace('\n',' ');target=norm(r['forma']);match=bool(re.search(r'(?<!\w)'+re.escape(target).replace(r'\ ',r'\s+')+r'(?!\w)',norm(text)))
 return {'id_persona':r['id_persona'],'forma':r['forma'],'interval_escolta':r['interval_escolta'],'clip':r['clip'],'sha256':hashlib.sha256((PROV/r['clip']).read_bytes()).hexdigest(),'text_greedy':text,'greedy_txt':f'qa-clips-greedy-full/{txt.name}','forma_en_greedy':'sí' if match else 'no'}
def main():
 with (PROV/'clips-audicio.tsv').open(encoding='utf-8',newline='') as h:rows=list(csv.DictReader(h,delimiter='\t'))
 OUT.mkdir(exist_ok=True);results={}
 with ThreadPoolExecutor(max_workers=8) as ex:
  fs={ex.submit(run,r):(r['id_persona'],r['forma']) for r in rows}
  for f in as_completed(fs):results[fs[f]]=f.result()
 fields=['id_persona','forma','interval_escolta','clip','sha256','greedy_txt','text_greedy','forma_en_greedy']
 with (PROV/'qa-clips-greedy-full.tsv').open('w',encoding='utf-8',newline='') as h:
  w=csv.DictWriter(h,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();[w.writerow(results[(r['id_persona'],r['forma'])]) for r in rows]
 print(f'{len(rows)} clips greedy · {sum(r["forma_en_greedy"]=="sí" for r in results.values())} coincidències')
if __name__=='__main__':main()
