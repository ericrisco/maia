"""Mesura trajectòries en cinc punts dels tokens base consensuals."""
from collections import defaultdict
from pathlib import Path
from statistics import median
import csv, parselmouth
ROOT=Path(__file__).parents[1];PROV=ROOT/'proveniencia';POINTS=(.2,.35,.5,.65,.8)
def fmt(v):return f'{v:.2f}' if v is not None and v==v else ''
def measure(form,pitch,intensity,time):
 out={}
 try:out['f0_hz']=fmt(pitch.get_value_at_time(time))
 except Exception:out['f0_hz']=''
 for n in (1,2,3):
  try:out[f'f{n}_hz']=fmt(form.get_value_at_time(n,time))
  except Exception:out[f'f{n}_hz']=''
 try:out['intensity_db']=fmt(intensity.get_value(time))
 except Exception:out['intensity_db']=''
 return out
def main():
 with (PROV/'qa-equilibrada-base-token-occurrences.tsv').open(encoding='utf-8',newline='') as h:rows=list(csv.DictReader(h,delimiter='\t'))
 cache={};out=[];by=defaultdict(list)
 for row in rows:
  path=str(PROV/row['clip'])
  if path not in cache:
   sound=parselmouth.Sound(path);cache[path]=(sound,sound.to_formant_burg(time_step=.005,max_number_of_formants=5,maximum_formant=5500,window_length=.025,pre_emphasis_from=50),sound.to_pitch(time_step=.005,pitch_floor=60,pitch_ceiling=500),sound.to_intensity(minimum_pitch=60))
  sound,form,pitch,intensity=cache[path];start=max(.015,min(sound.duration-.015,float(row['local_start_s'])));end=max(start+.01,min(sound.duration-.015,float(row['local_end_s'])));duration=end-start
  for point,fraction in enumerate(POINTS,1):
   time=start+duration*fraction;result=measure(form,pitch,intensity,time);result.update({'id_persona':row['id_persona'],'forma':row['forma'],'clip':row['clip'],'absolute_start_s':row['absolute_start_s'],'absolute_end_s':row['absolute_end_s'],'prob_min':row['prob_min'],'punt':str(point),'proporcio':f'{fraction:.2f}','temps_rel_s':f'{time:.3f}'})
   out.append(result);by[row['forma']].append(result)
 fields=['id_persona','forma','clip','absolute_start_s','absolute_end_s','prob_min','punt','proporcio','temps_rel_s','f0_hz','f1_hz','f2_hz','f3_hz','intensity_db']
 with (PROV/'analisi-trajectories-base-equilibrada.tsv').open('w',encoding='utf-8',newline='') as h:
  w=csv.DictWriter(h,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(out)
 sf=['forma','n_points','n_tokens','n_parlants','f0_start_median_hz','f0_end_median_hz','f1_start_median_hz','f1_end_median_hz','f2_start_median_hz','f2_end_median_hz','f3_start_median_hz','f3_end_median_hz','intensity_start_median_db','intensity_end_median_db'];summ=[]
 for form,items in sorted(by.items()):
  def med(k,p):
   vals=[float(x[k]) for x in items if x['punt']==p and x.get(k)];return f'{median(vals):.2f}' if vals else ''
  summ.append({'forma':form,'n_points':len(items),'n_tokens':len(items)//5,'n_parlants':len({x['id_persona'] for x in items}),'f0_start_median_hz':med('f0_hz','1'),'f0_end_median_hz':med('f0_hz','5'),'f1_start_median_hz':med('f1_hz','1'),'f1_end_median_hz':med('f1_hz','5'),'f2_start_median_hz':med('f2_hz','1'),'f2_end_median_hz':med('f2_hz','5'),'f3_start_median_hz':med('f3_hz','1'),'f3_end_median_hz':med('f3_hz','5'),'intensity_start_median_db':med('intensity_db','1'),'intensity_end_median_db':med('intensity_db','5')})
 with (PROV/'resum-trajectories-base-equilibrada.tsv').open('w',encoding='utf-8',newline='') as h:
  w=csv.DictWriter(h,fieldnames=sf,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(summ)
 print(f'{len(out)} punts · {len(rows)} tokens · {len(summ)} formes · F0 {sum(bool(x["f0_hz"]) for x in out)} · F1 {sum(bool(x["f1_hz"]) for x in out)} · F2 {sum(bool(x["f2_hz"]) for x in out)} · F3 {sum(bool(x["f3_hz"]) for x in out)}')
if __name__=='__main__':main()
