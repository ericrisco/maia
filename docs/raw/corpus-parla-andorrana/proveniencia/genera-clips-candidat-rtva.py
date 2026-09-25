"""Extreu clips curts de les formes Joan-probable per a escolta manual."""
from __future__ import annotations
import csv,wave,re
from pathlib import Path
from collections import OrderedDict
ROOT=Path(__file__).parents[1]
CAND=ROOT/'proveniencia'/'candidats'/'lead-rtva-001'

def slug(v): return re.sub(r'[^a-z0-9]+','-',v.lower()).strip('-')

def main():
 rows=list(csv.DictReader((CAND/'formes-joan-provisional.tsv').open(encoding='utf-8'),delimiter='\t'))
 consensus={r['forma']:r for r in csv.DictReader((CAND/'formes-consens.tsv').open(encoding='utf-8'),delimiter='\t')}
 chosen=OrderedDict()
 for row in rows:
  chosen.setdefault(row['forma'],row)
 clips_dir=CAND/'clips'; clips_dir.mkdir(exist_ok=True)
 with wave.open(str(CAND/'audio.wav'),'rb') as src:
  params=src.getparams(); rate=src.getframerate(); frames=src.readframes(src.getnframes())
 manifest=[]
 for form,row in chosen.items():
  start=max(0.0,float(row['inici_s'])-1.0); end=float(row['final_s'])+1.0
  a=int(start*rate); b=min(len(frames)//(params.sampwidth*params.nchannels),int(end*rate))
  data=frames[a*params.sampwidth*params.nchannels:b*params.sampwidth*params.nchannels]
  filename=f"joan__{slug(form)}__{float(row['inici_s']):.2f}.wav"; out=clips_dir/filename
  with wave.open(str(out),'wb') as dst:
   dst.setparams(params); dst.writeframes(data)
  c=consensus.get(form,{}); small=int(c.get('small','0')); base=int(c.get('base','0'))
  manifest.append({'forma':form,'segment':row['segment'],'inici_forma_s':row['inici_s'],'final_forma_s':row['final_s'],'clip':f'clips/{filename}','inici_clip_s':f'{start:.3f}','final_clip_s':f'{end:.3f}','small':small,'base':base,'prioritat':'A-consens-ASR' if small and base else 'B-un-model-ASR','estat':'pendent d’audició'})
 out=CAND/'formes-joan-clips.tsv'
 with out.open('w',encoding='utf-8',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(manifest[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(manifest)
 lines=['# Clips de formes Joan-probable','',f"S’han extret **{len(manifest)} clips** (finestra d’un segon abans i després) per obrir les formes amb una hipòtesi textual de veu de Joan.",'','| forma | clip | small | base | prioritat |','|---|---|---:|---:|---|']
 for r in manifest: lines.append(f"| `{r['forma']}` | `{r['clip']}` | {r['small']} | {r['base']} | {r['prioritat']} |")
 lines += ['', 'La prioritat ASR no és una decisió auditiva. Cal comprovar que el segment és de Joan, corregir la transcripció i anotar fonètica i prosòdia.']
 (CAND/'quadern-clips-formes.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 report=CAND/'informe.md'; s=report.read_text(encoding='utf-8'); marker='## Següent revisió\n'; addition='## Clips de revisió\n\n`formes-joan-clips.tsv` i `quadern-clips-formes.md` extreuen un clip per a cadascuna de les formes `joan-probable`; les formes presents en els dos ASR queden davant.\n\n';
 if '## Clips de revisió' not in s: report.write_text(s.replace(marker,addition+marker,1),encoding='utf-8')
 print(f'{len(manifest)} clips · {sum(r["prioritat"]=="A-consens-ASR" for r in manifest)} A · {sum(r["prioritat"]=="B-un-model-ASR" for r in manifest)} B')
if __name__=='__main__':main()
