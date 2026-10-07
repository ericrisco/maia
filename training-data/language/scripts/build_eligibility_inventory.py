#!/usr/bin/env python3
"""Inventory speech sources without treating metadata eligibility as reuse approval."""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[3]
DOCS = ROOT / 'docs' / 'parla'
FONTS = ROOT / 'docs' / 'fonts'
DATA = ROOT / 'training-data' / 'language'
WORK = DATA / 'work'
REPORTS = DATA / 'reports'


def read_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding='utf-8', errors='replace')
    match = re.match(r'\A---\s*\n(.*?)\n---(?:\s*\n|\Z)', text, re.DOTALL)
    if not match:
        return {}
    value = yaml.safe_load(match.group(1))
    return value if isinstance(value, dict) else {}


def as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def main() -> None:
    paths = sorted(DOCS.rglob('*.md'))
    entries: list[dict[str, Any]] = []
    errors: list[str] = []
    eligibility_counts: Counter[str] = Counter()
    rights_counts: Counter[str] = Counter()
    transcript_counts: Counter[str] = Counter()
    for path in paths:
        relative = path.relative_to(ROOT).as_posix()
        metadata = read_frontmatter(path)
        if not metadata:
            entries.append({
                'path': relative,
                'type': 'unparsed',
                'title': '',
                'metadata_eligible': False,
                'eligibility_reason': 'No YAML frontmatter; review as navigation or non-record content.',
                'rights_status': 'not_applicable',
                'transcript_status': 'not_applicable',
                'conversation_status': 'not_reviewed',
            })
            continue

        tags = as_list(metadata.get('tags'))
        voice_ok = metadata.get('veu') == 'originaria'
        era_ok = metadata.get('epoca') == 'contemporania'
        language_ok = metadata.get('apte_llengua') is True
        metadata_eligible = metadata.get('type') == 'parla' and voice_ok and era_ok and language_ok
        failed = []
        if metadata.get('type') != 'parla':
            failed.append('type is not parla')
        if not voice_ok:
            failed.append('veu is not originaria')
        if not era_ok:
            failed.append('epoca is not contemporania')
        if not language_ok:
            failed.append('apte_llengua is not true')
        eligibility = 'metadata_candidate' if metadata_eligible else ('excluded_by_corpus_flags' if metadata.get('type') == 'parla' else 'not_a_speech_record')
        eligibility_counts[eligibility] += 1

        font_ids = as_list(metadata.get('font'))
        font_details = []
        for font_id in font_ids:
            font_path = FONTS / f'{font_id}.md'
            font_meta = read_frontmatter(font_path) if font_path.is_file() else {}
            redistribution = str(font_meta.get('redistribucio') or 'unknown').strip().lower()
            if redistribution == 'si' or redistribution.startswith('si,'):
                rights = 'source_allows_redistribution_piece_check_required'
            elif redistribution == 'citacio':
                rights = 'citation_only'
            elif redistribution == 'pendent':
                rights = 'pending'
            else:
                rights = 'unknown'
            font_details.append({
                'font_id': font_id,
                'font_path': font_path.relative_to(ROOT).as_posix() if font_path.is_file() else '',
                'license': str(font_meta.get('llicencia') or ''),
                'redistribution': redistribution,
                'rights_status': rights,
            })
        if not font_details:
            rights_status = 'missing_source'
        elif any(item['rights_status'] in {'pending', 'unknown', 'citation_only'} for item in font_details):
            rights_status = 'pending_or_restricted'
        else:
            rights_status = 'piece_level_review_required'
        is_speech_record = metadata.get('type') == 'parla'
        if is_speech_record:
            rights_counts[rights_status] += 1

        if 'transcripcio-incerta' in tags:
            transcript_status = 'uncertain_and_unverified' if 'transcripcio-no-verificada' in tags else 'uncertain'
        elif 'transcripcio-no-verificada' in tags:
            transcript_status = 'unverified'
        else:
            transcript_status = 'not_marked_uncertain_but_not_verified'
        if is_speech_record:
            transcript_counts[transcript_status] += 1
        entries.append({
            'path': relative,
            'type': str(metadata.get('type') or ''),
            'title': str(metadata.get('title') or ''),
            'voice': str(metadata.get('veu') or ''),
            'era': str(metadata.get('epoca') or ''),
            'apte_llengua': metadata.get('apte_llengua'),
            'speaker': str(metadata.get('speaker') or ''),
            'source_ids': font_ids,
            'source_details': font_details,
            'metadata_eligible': metadata_eligible,
            'eligibility_status': eligibility,
            'eligibility_reason': '; '.join(failed),
            'rights_status': rights_status,
            'transcript_status': transcript_status,
            'tags': tags,
            'conversation_status': 'not_reviewed',
        })

    total = len(entries)
    candidates = sum(row.get('metadata_eligible', False) for row in entries)
    preliminary_candidates = sum(
        row.get('metadata_eligible', False)
        and row.get('rights_status') == 'source_allows_redistribution_piece_check_required'
        and row.get('transcript_status') == 'not_marked_uncertain_but_not_verified'
        for row in entries
    )
    WORK.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    (WORK / 'eligibility-inventory.json').write_text(
        json.dumps({
            'source_root': 'docs/parla/',
            'file_count': total,
            'metadata_candidate_count': candidates,
            'preliminary_candidate_count_before_manual_piece_review': preliminary_candidates,
            'entries': entries,
        }, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    lines = [
        '# Inventari de Maia Language', '',
        'Aquest inventari aplica els tres filtres del corpus, però no converteix una peça en candidata d’entrenament automàticament. Els drets s’han de comprovar per peça i les transcripcions s’han de verificar contra l’àudio. Les transcripcions automàtiques marcades com a incertes no entren al dataset.', '',
        f'- Fitxers Markdown inspeccionats: **{total}**.',
        f'- Peces que passen `veu: originaria`, `epoca: contemporania` i `apte_llengua: true`: **{candidates}**.',
        f'- Peces que passen filtres de transcripció i tenen una font que permet redistribució a nivell de sèrie (encara pendents de revisió per peça): **{preliminary_candidates}**.',
        f'- Converses Language generades: **0**. No s’ha inventat cap torn ni s’ha tractat una transcripció no verificada com a parla validada.',
        '', '## Estats dels drets i transcripcions', '',
        '| Drets | Peces |', '|---|---:|',
    ]
    lines.extend(f'| `{key}` | {value} |' for key, value in sorted(rights_counts.items()))
    lines += ['', '| Transcripció | Peces |', '|---|---:|']
    lines.extend(f'| `{key}` | {value} |' for key, value in sorted(transcript_counts.items()))
    lines += ['', '## Acció necessària', '',
              'Revisar els drets de cada peça i escoltar l’àudio per verificar la transcripció. Després cal determinar si hi ha torns humans suficients per a un diàleg fidel. Si no n’hi ha, la peça no es força dins d’un format `user`/`assistant`.']
    (REPORTS / 'eligibility-summary.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')

    print(f'Inventoried {total} Markdown files; {candidates} pass corpus metadata filters.')
    speech_count = sum(row.get('type') == 'parla' for row in entries)
    print(f'Speech records: {speech_count}; rights status: {dict(rights_counts)}')
    print(f'Transcript status for speech records: {dict(transcript_counts)}')


if __name__ == '__main__':
    main()
