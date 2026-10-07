#!/usr/bin/env python3
"""Inventory every Markdown file under docs/temes and summarize review coverage."""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / 'training-data' / 'knowledge'
DOCS = ROOT / 'docs' / 'temes'
REVIEW = DATA / 'review'
WORK = DATA / 'work'
REPORTS = DATA / 'reports'
STATUSES = {'not_started', 'in_progress', 'complete', 'no_natural_question', 'excluded_rights'}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    for number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f'{path}:{number}: JSONL invàlid: {exc}') from exc
        if not isinstance(value, dict):
            raise ValueError(f'{path}:{number}: cada línia ha de ser un objecte')
        rows.append(value)
    return rows


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding='utf-8', errors='replace')
    if not text.startswith('---\n'):
        raise ValueError(f'{path.relative_to(ROOT)}: falta el frontmatter inicial')
    parts = text.split('---', 2)
    if len(parts) != 3:
        raise ValueError(f'{path.relative_to(ROOT)}: frontmatter sense tancament')
    block = parts[1]
    result: dict[str, str] = {}
    for key in ('type', 'title', 'tema', 'font'):
        match = re.search(rf'(?m)^{re.escape(key)}:\s*(.*?)\s*$', block)
        if match:
            value = match.group(1).strip()
            if len(value) > 1 and value[0] in "\"'" and value[-1] == value[0]:
                value = value[1:-1]
            result[key] = value
    if 'type' not in result or 'title' not in result:
        raise ValueError(f'{path.relative_to(ROOT)}: falta type o title')
    return result


def validate_messages(row: dict[str, Any], row_number: int) -> None:
    messages = row.get('messages')
    if not isinstance(messages, list) or len(messages) < 2 or len(messages) % 2:
        raise ValueError(f'conversations.jsonl:{row_number}: messages ha de tenir torns user/assistant complets')
    for i, message in enumerate(messages):
        expected = 'user' if i % 2 == 0 else 'assistant'
        if not isinstance(message, dict) or message.get('role') != expected or not str(message.get('content', '')).strip():
            raise ValueError(f'conversations.jsonl:{row_number}: torn {i + 1} incorrecte')


def main() -> None:
    status_path = WORK / 'document-status.json'
    statuses = json.loads(status_path.read_text(encoding='utf-8')) if status_path.exists() else {}
    if not isinstance(statuses, dict):
        raise ValueError('document-status.json ha de ser un objecte indexat per ruta')

    conversations = read_jsonl(REVIEW / 'conversations.jsonl')
    provenance = read_jsonl(REVIEW / 'provenance.jsonl')
    if len(conversations) != len(provenance):
        raise ValueError(f'{len(conversations)} converses però {len(provenance)} registres de procedència')
    ids: set[str] = set()
    records_by_source: dict[str, list[str]] = defaultdict(list)
    for number, (conversation, source_row) in enumerate(zip(conversations, provenance), 1):
        validate_messages(conversation, number)
        record_id = source_row.get('example_id')
        if not isinstance(record_id, str) or not record_id or record_id in ids:
            raise ValueError(f'provenance.jsonl:{number}: example_id absent o duplicat')
        ids.add(record_id)
        sources = source_row.get('source_documents', [])
        if not isinstance(sources, list) or not sources:
            raise ValueError(f'provenance.jsonl:{number}: source_documents buit')
        for source in sources:
            if isinstance(source, str) and source.startswith('docs/temes/'):
                records_by_source[source].append(record_id)

    paths = sorted(DOCS.rglob('*.md'))
    known: set[str] = set()
    inventory: list[dict[str, Any]] = []
    file_totals: Counter[str] = Counter()
    article_totals: Counter[str] = Counter()
    by_topic: dict[str, Counter[str]] = defaultdict(Counter)
    for path in paths:
        relative = path.relative_to(ROOT).as_posix()
        known.add(relative)
        meta = parse_frontmatter(path)
        state = statuses.get(relative, {})
        if not isinstance(state, dict):
            raise ValueError(f'{relative}: estat ha de ser un objecte')
        status = state.get('status') or ('in_progress' if records_by_source.get(relative) else 'not_started')
        if status not in STATUSES:
            raise ValueError(f'{relative}: estat desconegut {status!r}')
        if status == 'complete' and not state.get('completion_note'):
            raise ValueError(f'{relative}: complete necessita completion_note')
        if status == 'no_natural_question' and not state.get('reason'):
            raise ValueError(f'{relative}: no_natural_question necessita reason')
        if status == 'excluded_rights' and not state.get('exclusion_reason'):
            raise ValueError(f'{relative}: excluded_rights necessita exclusion_reason')
        row = {
            'path': relative,
            'title': meta['title'],
            'type': meta['type'],
            'topic': meta.get('tema', ''),
            'source': meta.get('font', ''),
            'status': status,
            'conversation_count': len(set(records_by_source.get(relative, []))),
            'conversation_ids': sorted(set(records_by_source.get(relative, []))),
            'reviewed_units': state.get('reviewed_units', []),
            'open_units': state.get('open_units', []),
            'completion_note': state.get('completion_note', ''),
            'reason': state.get('reason', ''),
            'exclusion_reason': state.get('exclusion_reason', ''),
        }
        inventory.append(row)
        file_totals[status] += 1
        if meta['type'] == 'article':
            article_totals[status] += 1
            by_topic[meta.get('tema', '(sense tema)')][status] += 1

    stale = sorted(set(statuses) - known)
    if stale:
        raise ValueError(f'Rutes obsoletes a document-status.json: {stale}')

    WORK.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    (WORK / 'document-inventory.json').write_text(
        json.dumps({
            'source_root': 'docs/temes/',
            'file_count': len(inventory),
            'article_count': sum(1 for row in inventory if row['type'] == 'article'),
            'conversation_count': len(conversations),
            'file_status_totals': {key: file_totals[key] for key in sorted(STATUSES)},
            'article_status_totals': {key: article_totals[key] for key in sorted(STATUSES)},
            'documents': inventory,
        }, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    labels = {'not_started':'No començats', 'in_progress':'En curs', 'complete':'Completats', 'no_natural_question':'Sense pregunta natural', 'excluded_rights':'Exclosos per drets'}
    lines = [
        '# Cobertura de Maia Knowledge', '',
        'El recompte inclou tots els Markdown de `docs/temes/`, també índexs i altres fitxers. Les exclusions per drets continuen comptant a la cobertura i necessiten una raó documentada. Un article només és complet quan cada unitat útil s’ha revisat i els buits tenen una nota explícita.', '',
        f"- Fitxers Markdown inventariats: **{len(inventory)}**.",
        f"- Fitxes `article`: **{sum(1 for row in inventory if row['type'] == 'article')}**.",
        f'- Converses candidates amb procedència: **{len(conversations)}**.',
        '', '## Estat de tots els fitxers', '', '| Estat | Fitxers |', '|---|---:|',
    ]
    lines.extend(f'| {labels[key]} | {file_totals[key]} |' for key in sorted(STATUSES))
    lines += ['', '## Estat de les fitxes article', '', '| Estat | Articles |', '|---|---:|']
    lines.extend(f'| {labels[key]} | {article_totals[key]} |' for key in sorted(STATUSES))
    lines += ['', '## Estat per tema', '', '| Tema | Articles | No començats | En curs | Complets | Sense pregunta natural |', '|---|---:|---:|---:|---:|---:|']
    for topic, counts in sorted(by_topic.items()):
        lines.append(f"| `{topic}` | {sum(counts.values())} | {counts['not_started']} | {counts['in_progress']} | {counts['complete']} | {counts['no_natural_question']} |")
    (REPORTS / 'coverage-summary.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f"Inventariats {len(inventory)} fitxers ({sum(1 for row in inventory if row['type'] == 'article')} articles)")
    print('Estat articles:', ', '.join(f'{key}={article_totals[key]}' for key in sorted(STATUSES)))
    print(f'Converses amb procedència: {len(conversations)}')


if __name__ == '__main__':
    main()
