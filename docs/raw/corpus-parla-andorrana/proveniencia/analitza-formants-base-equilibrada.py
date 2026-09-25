"""Mesura F0/F1/F2/F3 en els 70 tokens base que coincideixen amb small."""
from collections import defaultdict
from pathlib import Path
from statistics import median
import csv
import parselmouth
ROOT=Path(__file__).parents[1]; PROV=ROOT/'proveniencia'
def fmt(v): return f'{v:.2f}' if v is not None and v==v else ''
def main():
 with (PROV/'qa-equilibrada-base-token-occurrences.tsv').open(encoding='utf-8',newline='') as h: rows=list(csv.DictReader(h,delimiter='\t'))
 cache={}; out=[]; by_form=defaultdict(list)
 for row in rows:
  path=str(PROV/row['clip'])
  if path not in cache:
   snd=parselmouth.Sound(path); cache[path]=(snd,snd.to_formant_burg(time_step=.005,max_number_of_formants=5,maximum_formant=5500,window_length=.025,pre_emphasis_from=50),snd.to_pitch(time_step=.005,pitch_floor=60,pitch_ceiling=500))
  snd,form,pitch=cache[path]
  center=max(.015,min(snd.duration-.015,(float(row['local_start_s'])+float(row['local_end_s']))/2))
  result=dict(row); result['centre_rel_s']=f'{center:.3f}'
  try: result['f0_hz']=fmt(pitch.get_value_at_time(center))
  except Exception: result['f0_hz']=''
  for n in (1,2,3):
   try: result[f'f{n}_hz']=fmt(form.get_value_at_time(n,center))
   except Exception: result[f'f{n}_hz']=''
  result['estat']='coincidència small/base; mesures instrumentals; pendent d’audició';out.append(result);by_form[row['forma']].append(result)
 fields=['id_persona','forma','clip','occurrence','local_start_s','local_end_s','absolute_start_s','absolute_end_s','prob_min','text','centre_rel_s','f0_hz','f1_hz','f2_hz','f3_hz','estat']
 with (PROV/'analisi-formants-base-equilibrada.tsv').open('w',encoding='utf-8',newline='') as h:
  w=csv.DictWriter(h,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(out)
 summary=[]
 for form,items in sorted(by_form.items()):
  def med(k):
   vals=[float(i[k]) for i in items if i.get(k)];return f'{median(vals):.2f}' if vals else ''
  summary.append({'forma':form,'n_tokens':str(len(items)),'n_parlants':str(len({i['id_persona'] for i in items})),'f0_median_hz':med('f0_hz'),'f1_median_hz':med('f1_hz'),'f2_median_hz':med('f2_hz'),'f3_median_hz':med('f3_hz')})
 with (PROV/'resum-formants-base-equilibrada.tsv').open('w',encoding='utf-8',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(summary[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(summary)
 print(f'{len(out)} tokens mesurats · {len(summary)} formes · F0 {sum(bool(r["f0_hz"]) for r in out)} · F1 {sum(bool(r["f1_hz"]) for r in out)} · F2 {sum(bool(r["f2_hz"]) for r in out)} · F3 {sum(bool(r["f3_hz"]) for r in out)}')
if __name__=='__main__':main()
