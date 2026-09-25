"""Crea una hipòtesi de torns per a una entrevista sense diarització."""
from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).parents[1]
CAND=ROOT/'proveniencia'/'candidats'/'lead-rtva-001'
FORMS=['a nivell','a veure','aleshores','aviam','bé','bueno','clar','crec','de fet','diguem','doncs','evidentment','és a dir','llavors','no?','o sigui','per tant','perquè','tirar endavant','vull dir','ensenyança']
QUESTION_RE=re.compile(r"\?|^(?:què|com|per què|perquè|suposo|imagino|et |t'|vas |tornarà|m'has|tens |ara que|digues|no\?)",re.I)
JOAN_RE=re.compile(r"\b(?:jo|em|ens|som|estic|estem|tinc|vaig|vull|puc|poder|hem|anem|sabem|sé|m'agrada|m'he|nosaltres)\b",re.I)

def sec(v):
 h,m,s=v.replace(',','.').split(':'); return int(h)*3600+int(m)*60+float(s)

def classify(text):
 q=bool(QUESTION_RE.search(text)); j=bool(JOAN_RE.search(text))
 if q and j: return 'mixt-indeterminat','pregunta i primera persona en el mateix segment',0.35
 if q: return 'entrevistador-probable','interrogació o fórmula de pregunta',0.78
 if j: return 'joan-probable','primera persona o resposta declarativa',0.60
 return 'indeterminat','cap indici textual suficient',0.30

def main():
 data=json.loads((CAND/'asr'/'joan-verdu.json').read_text(encoding='utf-8'))
 rows=[]
 for i,seg in enumerate(data['transcription'],1):
  text=seg.get('text','').strip()
  if not text: continue
  label,evidence,score=classify(text)
  rows.append({'segment':i,'inici_s':f'{sec(seg["timestamps"]["from"]):.3f}','final_s':f'{sec(seg["timestamps"]["to"]):.3f}','speaker_hipotesi':label,'confiança_regla':f'{score:.2f}','evidencia_regla':evidence,'text_asr':text,'estat':'hipòtesi; pendent d’audició'})
 out=CAND/'segments-speaker-provisional.tsv'
 with out.open('w',encoding='utf-8',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
 occ=[]
 for row in rows:
  if row['speaker_hipotesi']!='joan-probable': continue
  for form in FORMS:
   if re.search(rf'(?<![\wà-ÿ]){re.escape(form)}(?![\wà-ÿ])',row['text_asr'],re.I):
    occ.append({'forma':form,'segment':row['segment'],'inici_s':row['inici_s'],'final_s':row['final_s'],'text_asr':row['text_asr'],'estat':'Joan probable per regla; pendent d’audició'})
 with (CAND/'formes-joan-provisional.tsv').open('w',encoding='utf-8',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(occ[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(occ)
 counts=Counter(row['speaker_hipotesi'] for row in rows)
 form_counts=Counter(row['forma'] for row in occ)
 report=CAND/'segmentacio-veus.md'
 lines=['# Segmentació provisional de veus','', 'La segmentació usa només pistes textuals de l’ASR (interrogacions, fórmules de pregunta i primera persona). No és diarització acústica ni assignació confirmada de Joan.', '', f"- Segments: {len(rows)}."]
 for label,count in counts.items(): lines.append(f'- `{label}`: {count} segments.')
 lines += ['', '## Formes en segments Joan-probable', '']
 for form,count in form_counts.most_common(): lines.append(f'- `{form}`: {count}.')
 lines += ['', 'Els fitxers `segments-speaker-provisional.tsv` i `formes-joan-provisional.tsv` serveixen per ordenar l’escolta; totes les etiquetes s’han de corregir o confirmar manualment.']
 report.write_text('\n'.join(lines)+'\n',encoding='utf-8')
 candidate=CAND/'informe.md'; s=candidate.read_text(encoding='utf-8'); marker='## Següent revisió\n'; addition='## Segmentació textual provisional\n\n`segments-speaker-provisional.tsv` marca torns probables a partir de preguntes i primera persona; `formes-joan-provisional.tsv` restringeix els marcadors als segments `joan-probable`. És una hipòtesi de navegació, no una anotació de veu.\n\n';
 if '## Segmentació textual provisional' not in s: candidate.write_text(s.replace(marker,addition+marker,1),encoding='utf-8')
 print(f'{len(rows)} segments · {counts} · {len(occ)} formes en Joan-probable')
if __name__=='__main__':main()
