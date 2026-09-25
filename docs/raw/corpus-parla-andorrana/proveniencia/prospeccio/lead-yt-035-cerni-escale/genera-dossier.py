"""Prepara el dossier de prospecció de Cerni Escalé fora del cànon."""
from __future__ import annotations
import csv, hashlib, json, re, subprocess
from collections import Counter
from datetime import date
from pathlib import Path

ROOT=Path(__file__).parent; ASR=ROOT/'asr'; CLIPS=ROOT/'clips'
SMALL=json.loads((ASR/'cerni-escale-small-nocontext.json').read_text())
BASE=json.loads((ASR/'cerni-escale-base-nocontext.json').read_text())
FORMS_SOURCE=Path(__file__).parents[2]/'candidats/lead-rtva-008-mireia-pedescoll/formes-consens.tsv'
EXTRA=[
 ('Cerni Escalé','persones'),('Concòrdia','política'),('eleccions','institucions'),('Consell General','institucions'),('política','política'),('Banc Mundial','institucions'),('Nacions Unides','institucions'),('Sierra Leone','toponim'),('Unió Europea','institucions'),('acord d’associació','institucions'),('Catalunya','toponim'),('França','toponim'),('Espanya','toponim'),('llengua catalana','sociolingüística'),('català','sociolingüística'),('andorrà','gentilici'),('immobiliari','economia'),('creixement','economia'),('muntanya','territori'),('orri','cultura'),('formatges','cultura'),('turistes','societat'),('copríncep','institucions'),('comunitat','societat'),('habitatge','societat'),('joventut','societat'),('sostenibilitat','economia'),('territori','territori'),('aigua','territori'),('comarques','territori'),('integració','societat'),('referèndum','institucions'),('fronteres','territori'),('educació','societat'),('serveis','institucions'),('llengües','sociolingüística'),
]

def rows(d): return d.get('transcription',[])
def plain(t): return re.sub(r'\s+',' ',re.sub(r'\[_[^]]+\]','',t or '')).strip()
def rx(form): return re.compile(r'(?i)(?<!\w)'+re.escape(form)+r'(?!\w)')
def count(text,form): return len(rx(form).findall(text))
def first_hit(data,form):
    for seg in rows(data):
        text=plain(seg.get('text',''))
        if rx(form).search(text): return seg,text
    return None,''
def conf(seg):
    vals=[float(t['p']) for t in (seg or {}).get('tokens',[]) if t.get('p') is not None and not str(t.get('text','')).startswith('[_')]
    return (min(vals),sum(vals)/len(vals)) if vals else ('','')
def write_tsv(path,items,fields):
    with path.open('w',encoding='utf-8',newline='') as h:
        w=csv.DictWriter(h,fieldnames=fields,delimiter='\t');w.writeheader();w.writerows(items)
def main():
    CLIPS.mkdir(exist_ok=True)
    small_text=' '.join(plain(s.get('text','')) for s in rows(SMALL)); base_text=' '.join(plain(s.get('text','')) for s in rows(BASE))
    forms=[]; seen=set()
    with FORMS_SOURCE.open(encoding='utf-8',newline='') as h:
        for r in csv.DictReader(h,delimiter='\t'):
            f=r['forma']
            if f not in seen: forms.append((f,r.get('categoria','')));seen.add(f)
    for f,c in EXTRA:
        if f not in seen: forms.append((f,c));seen.add(f)
    form_rows=[]; queue=[]
    for idx,(form,cat) in enumerate(forms,1):
        sseg,sctx=first_hit(SMALL,form); bseg,bctx=first_hit(BASE,form)
        loc='small' if sseg else ('base' if bseg else '')
        seg=sseg or bseg; smn=count(small_text,form); bmn=count(base_text,form)
        clip=''; start=end=''
        if seg:
            start=int(seg['offsets']['from']);end=int(seg['offsets']['to']); cs=max(0,start-2000); ce=end+2000
            slug=re.sub(r'[^a-z0-9]+','-',form.lower()).strip('-') or f'forma-{idx}'
            clip=f'lead-yt-035__{idx:02d}__{slug}.wav'; out=CLIPS/clip
            if not out.exists():
                subprocess.run(['ffmpeg','-y','-ss',f'{cs/1000:.3f}','-i',str(ROOT/'audio.wav'),'-t',f'{(ce-cs)/1000:.3f}','-ac','1','-ar','16000','-c:a','pcm_s16le',str(out),'-loglevel','error'],check=True)
        scm,smean=conf(sseg); bcm,bmean=conf(bseg)
        form_rows.append({'forma':form,'categoria':cat,'small':str(smn),'base':str(bmn),'consens':'sí' if smn and bmn else 'no','model_localitzador':loc,'context_small':sctx,'context_base':bctx,'prob_min_segment_small':f'{scm:.4f}' if isinstance(scm,float) else '','prob_mean_segment_small':f'{smean:.4f}' if isinstance(smean,float) else '','prob_min_segment_base':f'{bcm:.4f}' if isinstance(bcm,float) else '','prob_mean_segment_base':f'{bmean:.4f}' if isinstance(bmean,float) else '','clip':clip,'inici_ms':str(start),'final_ms':str(end),'estat':'ASR textual; atribució i audició pendents'})
        if clip: queue.append({'candidate':'lead-yt-035-cerni-escale','forma':form,'clip':f'clips/{clip}','veu_confirmada':'pendent','forma_confirmada':'pendent','variant_transcrita':'pendent','trets_fonetica':'pendent','prosodia':'pendent','nota_audicio':'pendent','estat_audicio':'pendent'})
    write_tsv(ROOT/'formes.tsv',form_rows,list(form_rows[0]))
    write_tsv(ROOT/'cua-audicio.tsv',queue,list(queue[0]))
    def sha(p):
        h=hashlib.sha256();
        with p.open('rb') as f:
            for b in iter(lambda:f.read(1032*1032),b''):h.update(b)
        return h.hexdigest()
    info=json.loads((ROOT/'source.info.json').read_text()); info['data_consulta']=str(date.today());info['asr_small']='asr/cerni-escale-small-nocontext.json';info['asr_base']='asr/cerni-escale-base-nocontext.json';info['forms_count']=len(form_rows);info['clips_count']=len(queue);info['hashes']={x:sha(ROOT/x) for x in ['source-page.html','legal-page.html','source-original.mp4','audio.wav']};(ROOT/'source.info.json').write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n')
    def stats(d): return len(rows(d)),(rows(d)[-1]['offsets']['to'] if rows(d) else 0)
    ss,sd=stats(SMALL);bs,bd=stats(BASE);low=[t for s in rows(SMALL) for t in s.get('tokens',[]) if t.get('p',1)<.55 and re.search(r'\w',t.get('text',''))];rep=sum(1 for a,b in zip(rows(SMALL),rows(SMALL)[1:]) if plain(a.get('text')) and plain(a.get('text'))==plain(b.get('text')));top=', '.join(f'{w} ({n})' for w,n in Counter(re.findall(r"\b[\wàèéíòóúïüç']+\b",small_text.lower())).most_common(20))
    (ROOT/'informe.md').write_text(f'''# Expedient de prospecció — Cerni Escalé\n\n## Estat\n\n`lead-yt-035-cerni-escale` és una font candidata fora del recompte i dels grafs canònics. El vídeo del canal CFEM presenta una entrevista amb Cerni Escalé, cap de llista nacional de Concòrdia a les eleccions al Consell General; la fitxa es manté candidata fins a la revisió de veu i context. L'enregistrament conté preguntes de l'entrevistador i la veu principal de Cerni Escalé; cap clip s'atribueix automàticament a Cerni Escalé.\n\n## Procedència i fitxers\n\n- Font: [YouTube — Eleccions a Andorra: entrevista amb Cerni Escalé](https://www.youtube.com/watch?v=eRcBWJzHdyo).\n- Pàgina conservada: `source-page.html`; termes: `legal-page.html` i [`terms.md`](terms.md).\n- Flux original local: `source-original.mp4` (derivat local de recerca).\n- WAV de treball: `audio.wav`, mono, 16 kHz, {info['audio_wav']['duration_seconds']:.2f} s.\n- Hashes i metadades: `source.info.json`.\n\n## Transcripcions\n\nLa passada small sense context acumulat té {ss} segments fins a {sd/1000:.2f} s; la passada base independent té {bs} segments fins a {bd/1000:.2f} s. La small conté {len(low)} tokens per sota de 0,55 i {rep} repeticions consecutives exactes. Les dues sortides són ASR de treball i s'han de contrastar amb l'àudio.\n\n## Inventari i anàlisi provisional\n\n`formes.tsv` conserva {len(form_rows)} formes: les 35 formes comparables del paquet i {len(forms)-35} candidats polítics, institucionals, territorials i sociolingüístics detectats en aquesta font. `clips/` conté {len(queue)} clips locals; `cua-audicio.tsv` manté veu, variant, fonètica, prosòdia i nota en `pendent`.\n\nEls candidats locals inclouen `Concòrdia`, `eleccions`, `Consell General`, `Banc Mundial`, `Nacions Unides`, `Unió Europea`, `acord d'associació`, `llengua catalana`, `immobiliari`, `orri`, `formatges` i `habitatge`. Són formes localitzades textualment per ASR, no variants dialectals confirmades.\n\nSeqüències lèxiques més repetides en la passada small (no són trets dialectals): {top}\n\nNo es publica cap tret fonètic, prosòdic ni dialectal com a confirmat. Qualsevol incorporació al cànon exigeix escolta clip per clip, atribució de veu i revisió dels termes d'ús.\n''',encoding='utf-8')
    print(f'OK dossier Cerni Escalé: {len(form_rows)} formes · {len(queue)} clips · {ss}/{bs} segments small/base')
if __name__=='__main__': main()
