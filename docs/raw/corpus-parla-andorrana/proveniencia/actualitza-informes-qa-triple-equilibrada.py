"""Afegeix el resum de la tercera descodificació a les fitxes."""
from collections import Counter, defaultdict
from pathlib import Path
import csv
ROOT = Path(__file__).parents[1]
PROV = ROOT / 'proveniencia'
MARKER = '### Tercera descodificació de la mostra equilibrada'
def main():
    with (PROV / 'qa-equilibrada-triple.tsv').open(encoding='utf-8', newline='') as h:
        rows = list(csv.DictReader(h, delimiter='\t'))
    by = defaultdict(list)
    for row in rows:
        by[row['id_persona']].append(row)
    n = 0
    for report in sorted((ROOT / 'persones').glob('pa-*.md')):
        text = report.read_text(encoding='utf-8')
        if MARKER in text:
            text = text.split(MARKER, 1)[0].rstrip() + '\n\n'
        counts = Counter(row['categoria'] for row in by.get(report.stem, []))
        total = sum(counts.values())
        details = '; '.join(f'{key}={counts[key]}' for key in ('A-tres-models', 'B-dos-models', 'C-un-model', 'D-cap-model') if counts[key]) or 'cap clip'
        clip_label = 'clip' if total == 1 else 'clips'
        section = f"{MARKER}\n\nLa tercera descodificació greedy cobreix **{total} {clip_label}** d'aquesta fitxa: {details}. És una comparació ASR i continua pendent d'escolta.\n"
        report.write_text(text + '\n' + section, encoding='utf-8')
        n += 1
    print(f'OK: {n} informes actualitzats')
if __name__ == '__main__':
    main()
