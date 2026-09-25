"""Afegeix el contrast small/base de la mostra equilibrada a cada fitxa."""
from collections import defaultdict
from pathlib import Path
import csv

ROOT=Path(__file__).parents[1]
PROV=ROOT/'proveniencia'
SRC=PROV/'qa-equilibrada-consens.tsv'
MARKER='### Contrast small/base de la mostra equilibrada'

def main():
    with SRC.open(encoding='utf-8',newline='') as h: rows=list(csv.DictReader(h,delimiter='\t'))
    by=defaultdict(list)
    for r in rows: by[r['id_persona']].append(r)
    n=0
    for report in sorted((ROOT/'persones').glob('pa-*.md')):
        text=report.read_text(encoding='utf-8')
        if MARKER in text: text=text.split(MARKER,1)[0].rstrip()+'\n\n'
        rs=by.get(report.stem,[])
        a=sum(r['categoria']=='A-doble-coincidencia' for r in rs); b=sum(r['categoria']=='B-small-only' for r in rs)
        n_clips=len(rs); clip_label='clip' if n_clips == 1 else 'clips'
        lines=[MARKER,'',f"La mostra equilibrada té **{n_clips} {clip_label}** per a aquesta veu: **{a}** amb coincidència textual small/base i **{b}** només amb coincidència small. Aquesta comparació és ASR i no substitueix l'escolta.", '']
        if rs:
            for r in rs:
                if r['categoria']=='B-small-only':
                    lines.append(f"- **{r['forma']}** · [clip](../proveniencia/{r['clip']}) · divergència small/base · small: `{r['text_small']}` · base: `{r['text_base']}`")
            if not any(r['categoria']=='B-small-only' for r in rs): lines.append('- No hi ha divergències textuals small/base en els clips seleccionats.')
        else:
            lines.append('- Aquesta veu no té clip en la mostra equilibrada; la seva cobertura continua a la cua global.')
        lines += ['', 'El detall complet és `../proveniencia/qa-equilibrada-consens.tsv`; la revisió auditiva queda pendent.', '']
        report.write_text(text+'\n'.join(lines),encoding='utf-8'); n+=1
    print(f'OK: {n} informes actualitzats')

if __name__=='__main__':main()
