from pathlib import Path
import csv, subprocess, hashlib, wave
root=Path(__file__).parents[1]
targets={('pa-001','a nivell'),('pa-002','a nivell'),('pa-003','a nivell'),('pa-024','a nivell'),('pa-051','bueno'),('pa-052','bueno')}
rows=list(csv.DictReader((root/'proveniencia/cua-audicio.tsv').open(encoding='utf-8',newline=''),delimiter='\t'))
selected=[]
for row in rows:
    if (row['id_persona'],row['forma']) in targets and (row['id_persona'],row['forma']) not in {(r['id_persona'],r['forma']) for r in selected}:
        selected.append(row)
print('selected',len(selected))
created=[]
for row in selected:
    clip=root/'proveniencia'/row['clip_suggerit']
    src=root/'audios'/row['id_persona']/'audio.wav'
    start,end=row['interval_escolta'].split('-')
    subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-ss',start,'-to',end,'-i',str(src),'-ac','1','-ar','16000','-sample_fmt','s16',str(clip)],check=True)
    with wave.open(str(clip)) as wav:
        duration=wav.getnframes()/wav.getframerate()
    created.append({'forma':row['forma'],'id_persona':row['id_persona'],'interval_escolta':row['interval_escolta'],'interval_base':row['interval_base'],'clip':str(clip.relative_to(root/'proveniencia')),'estat_clip':'existent-extraient-sense-overlap','sha256':hashlib.sha256(clip.read_bytes()).hexdigest(),'duracio_s':f'{duration:.3f}'})
manifest=root/'proveniencia/clips-audicio.tsv'
with manifest.open(encoding='utf-8',newline='') as handle:
    existing=list(csv.DictReader(handle,delimiter='\t'))
fields=list(existing[0])
seen={(row['id_persona'],row['forma']) for row in existing}
existing.extend(row for row in created if (row['id_persona'],row['forma']) not in seen)
with manifest.open('w',encoding='utf-8',newline='') as handle:
    writer=csv.DictWriter(handle,fieldnames=fields,delimiter='\t',lineterminator='\n'); writer.writeheader(); writer.writerows(existing)
print('created',len(created),'manifest',len(existing))
