#!/usr/bin/env python3
"""Inventory all Maia Knowledge Markdown and report per-document conversation coverage."""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[3]
DOCS = ROOT / 'docs' / 'temes'
DATA = ROOT / 'training-data' / 'knowledge'
REVIEW = DATA / 'review'
WORK = DATA / 'work'
REPORTS = DATA / 'reports'
STATUSES = {'not_started', 'in_progress', 'complete', 'no_natural_question', 'excluded_rights'}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    for line_number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f'{path}:{line_number}: invalid JSONL: {exc}') from exc
        if not isinstance(value, dict):
            raise ValueError(f'{path}:{line_number}: each line must be a JSON object')
        rows.append(value)
    return rows


def parse_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding='utf-8', errors='replace')
    if not text.startswith('---'):
        raise ValueError('missing opening frontmatter delimiter')
    match = re.match(r'\A---\s*\n(.*?)\n---(?:\s*\n|\Z)', text, re.DOTALL)
    if not match:
        raise ValueError('missing closing frontmatter delimiter')
    metadata = yaml.safe_load(match.group(1))
    if not isinstance(metadata, dict):
        raise ValueError('frontmatter must be a YAML object')
    if not metadata.get('type') or not metadata.get('title'):
        raise ValueError('frontmatter requires type and title')
    return metadata


def validate_messages(row: dict[str, Any], number: int) -> None:
    if set(row) != {'messages'}:
        raise ValueError(f'conversations.jsonl:{number}: only the messages field is allowed')
    messages = row['messages']
    if not isinstance(messages, list) or len(messages) < 2 or len(messages) % 2:
        raise ValueError(f'conversations.jsonl:{number}: messages must contain complete user/assistant pairs')
    for index, message in enumerate(messages):
        role = 'user' if index % 2 == 0 else 'assistant'
        if not isinstance(message, dict) or set(message) != {'role', 'content'}:
            raise ValueError(f'conversations.jsonl:{number}: message {index + 1} has invalid fields')
        if message.get('role') != role or not isinstance(message.get('content'), str) or not message['content'].strip():
            raise ValueError(f'conversations.jsonl:{number}: message {index + 1} is invalid')


def load_statuses(path: Path) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    if not path.exists():
        return {}, {}
    raw = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(raw, dict):
        raise ValueError('document-status.json must be an object')
    if 'documents' in raw:
        documents = raw['documents']
        metadata = {key: value for key, value in raw.items() if key != 'documents'}
    else:
        documents = raw
        metadata = {}
    if not isinstance(documents, dict) or any(not isinstance(value, dict) for value in documents.values()):
        raise ValueError('document-status.json documents must map paths to objects')
    return documents, metadata


def main() -> None:
    statuses, status_metadata = load_statuses(WORK / 'document-status.json')
    conversations = read_jsonl(REVIEW / 'conversations.jsonl')
    provenance = read_jsonl(REVIEW / 'provenance.jsonl')
    if len(conversations) != len(provenance):
        raise ValueError(f'{len(conversations)} conversations but {len(provenance)} provenance records')

    ids: set[str] = set()
    unique_conversations: set[str] = set()
    records_by_source: dict[str, list[str]] = defaultdict(list)
    for number, (conversation, source_row) in enumerate(zip(conversations, provenance), 1):
        validate_messages(conversation, number)
        conversation_key = json.dumps(conversation, ensure_ascii=False, sort_keys=True)
        if conversation_key in unique_conversations:
            raise ValueError(f'conversations.jsonl:{number}: exact duplicate conversation')
        unique_conversations.add(conversation_key)
        record_id = source_row.get('example_id')
        if not isinstance(record_id, str) or not record_id or record_id in ids:
            raise ValueError(f'provenance.jsonl:{number}: missing or duplicate example_id')
        ids.add(record_id)
        sources = source_row.get('source_documents')
        if not isinstance(sources, list) or not sources:
            raise ValueError(f'provenance.jsonl:{number}: source_documents must be non-empty')
        if not isinstance(source_row.get('license'), str) or not source_row['license'].strip():
            raise ValueError(f'provenance.jsonl:{number}: missing source license/terms')
        if not isinstance(source_row.get('source_ids'), list) or not source_row['source_ids']:
            raise ValueError(f'provenance.jsonl:{number}: missing source_ids')
        claims = source_row.get('claims_supported')
        if not isinstance(claims, list) or not claims or any(not isinstance(claim, str) or not claim.strip() for claim in claims):
            raise ValueError(f'provenance.jsonl:{number}: claims_supported must be non-empty strings')
        if not isinstance(source_row.get('limits'), str) or not source_row['limits'].strip():
            raise ValueError(f'provenance.jsonl:{number}: missing claims limits')
        if not isinstance(source_row.get('split_group'), str) or not source_row['split_group'].strip():
            raise ValueError(f'provenance.jsonl:{number}: missing split_group')
        for source in sources:
            if not isinstance(source, str) or not (ROOT / source).is_file():
                raise ValueError(f'provenance.jsonl:{number}: source path is missing: {source!r}')
            if source.startswith('docs/temes/'):
                records_by_source[source].append(record_id)

    paths = sorted(DOCS.rglob('*.md'))
    known_paths = {path.relative_to(ROOT).as_posix() for path in paths}
    stale_statuses = sorted(set(statuses) - known_paths)
    if stale_statuses:
        raise ValueError(f'document-status.json has stale paths: {stale_statuses}')

    inventory: list[dict[str, Any]] = []
    file_totals: Counter[str] = Counter()
    article_totals: Counter[str] = Counter()
    by_topic: dict[str, Counter[str]] = defaultdict(Counter)
    errors: list[str] = []
    for path in paths:
        relative = path.relative_to(ROOT).as_posix()
        state = statuses.get(relative, {})
        declared_ids = sorted(set(state.get('conversation_ids', [])))
        actual_ids = sorted(set(records_by_source.get(relative, [])))
        if declared_ids and declared_ids != actual_ids:
            raise ValueError(f'{relative}: document-status conversation_ids do not match provenance')
        try:
            metadata = parse_frontmatter(path)
            parse_error = ''
        except (ValueError, yaml.YAMLError) as exc:
            metadata = {}
            parse_error = str(exc)
            errors.append(f'{relative}: {parse_error}')
        status = state.get('status') or ('in_progress' if records_by_source.get(relative) else 'not_started')
        if status not in STATUSES:
            raise ValueError(f'{relative}: unknown status {status!r}')
        if status == 'complete' and (not state.get('completion_note') or state.get('open_units')):
            raise ValueError(f'{relative}: complete requires completion_note and no open_units')
        if status == 'no_natural_question' and not state.get('reason'):
            raise ValueError(f'{relative}: no_natural_question requires reason')
        if status == 'excluded_rights' and not state.get('exclusion_reason'):
            raise ValueError(f'{relative}: excluded_rights requires exclusion_reason')
        file_type = str(metadata.get('type') or 'unparsed')
        topic = str(metadata.get('tema') or '')
        row = {
            'path': relative,
            'title': str(metadata.get('title') or ''),
            'type': file_type,
            'topic': topic,
            'source': str(metadata.get('font') or ''),
            'status': status,
            'conversation_count': len(set(records_by_source.get(relative, []))),
            'conversation_ids': sorted(set(records_by_source.get(relative, []))),
            'reviewed_units': state.get('covered_units', state.get('reviewed_units', [])),
            'open_units': state.get('open_units', []),
            'completion_note': state.get('completion_note', ''),
            'reason': state.get('reason', ''),
            'exclusion_reason': state.get('exclusion_reason', ''),
            'parse_error': parse_error,
        }
        inventory.append(row)
        file_totals[status] += 1
        if file_type == 'article':
            article_totals[status] += 1
            by_topic[topic or '(sense tema)'][status] += 1

    WORK.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    (WORK / 'document-inventory.json').write_text(
        json.dumps({
            'source_root': 'docs/temes/',
            'generated_from_status': status_metadata,
            'file_count': len(inventory),
            'article_count': sum(row['type'] == 'article' for row in inventory),
            'parse_error_count': len(errors),
            'conversation_count': len(conversations),
            'file_status_totals': {key: file_totals[key] for key in sorted(STATUSES)},
            'article_status_totals': {key: article_totals[key] for key in sorted(STATUSES)},
            'documents': inventory,
        }, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    labels = {
        'not_started': 'No començats',
        'in_progress': 'En curs',
        'complete': 'Completats',
        'no_natural_question': 'Sense pregunta natural',
        'excluded_rights': 'Exclosos per drets',
    }
    lines = [
        '# Cobertura de Maia Knowledge', '',
        'L’inventari inclou tots els Markdown de `docs/temes/`, inclosos índexs. Una fitxa només és completa quan totes les unitats útils s’han revisat i les exclusions i buits tenen motiu documentat. Aquest recompte de documents no substitueix la revisió de cobertura semàntica.', '',
        f'- Fitxers Markdown inventariats: **{len(inventory)}**.',
        f'- Fitxes `article`: **{sum(row["type"] == "article" for row in inventory)}**.',
        f'- Fitxers amb frontmatter invàlid: **{len(errors)}**.',
        f'- Converses actives amb procedència: **{len(conversations)}**.',
        '', '## Estat de tots els fitxers', '', '| Estat | Fitxers |', '|---|---:|',
    ]
    lines.extend(f'| {labels[key]} | {file_totals[key]} |' for key in sorted(STATUSES))
    lines += ['', '## Estat de les fitxes article', '', '| Estat | Articles |', '|---|---:|']
    lines.extend(f'| {labels[key]} | {article_totals[key]} |' for key in sorted(STATUSES))
    lines += ['', '## Estat per tema', '', '| Tema | Articles | No començats | En curs | Complets | Sense pregunta natural | Exclosos per drets |', '|---|---:|---:|---:|---:|---:|---:|']
    for topic, counts in sorted(by_topic.items()):
        lines.append(f"| `{topic}` | {sum(counts.values())} | {counts['not_started']} | {counts['in_progress']} | {counts['complete']} | {counts['no_natural_question']} | {counts['excluded_rights']} |")
    if errors:
        lines += ['', '## Errors de frontmatter', '']
        lines.extend(f'- `{error}`' for error in errors)
    in_progress = [row for row in inventory if row['status'] == 'in_progress']
    if in_progress:
        lines += ['', '## Documents en curs', '']
        for row in in_progress:
            lines.append(f"- `{row['path']}` — {row['conversation_count']} converses; {len(row['open_units'])} punts oberts.")
    (REPORTS / 'coverage-summary.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')

    print(f'Inventoried {len(inventory)} Markdown files ({sum(row["type"] == "article" for row in inventory)} articles)')
    print(f'Frontmatter errors: {len(errors)}; active conversations: {len(conversations)}')
    print('Article status: ' + ', '.join(f'{key}={article_totals[key]}' for key in sorted(STATUSES)))


if __name__ == '__main__':
    main()
