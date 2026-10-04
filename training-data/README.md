# Maia training data

This directory contains plain text only: clean knowledge fiches, related-text indexes, speech text, manifests, and topic Q&A records. It must not contain PDFs, audio, images, HTML captures, binaries, or copied source-document prose. It has two destinations:

- `talk/`: text for adapting the model to contemporary spoken Andorran Catalan.
- `knowledge/`: cleaned, reviewed knowledge fiches linked by topic, plus one Q&A dataset per topic for training with RAFT.

The source of truth remains `docs/`. `training-data/` contains clean text fiches derived from the source sheets, not raw PDFs, audio, captures, or verbatim source-document dumps. Fiches link to related fiches inside `knowledge/`. Each Q&A answer is newly written from the evidence. Citations identify source sheets, source records, locations, and URLs; they do not quote the source text.

## Review before creating a record

Before creating or extending a fiche, read the entire source sheet, all its linked sheets, and their registered source records. Investigate every open question using other sheets and sources. Close each point only when evidence supports it. Otherwise record what was checked and why it remains unresolved. Answer only with evidence available in `docs/` or verified source records. Never turn a missing answer into a factual negative.

For each knowledge fiche, prepare these question forms:

1. A question answerable from that sheet.
2. A question that needs that sheet and linked sheets.
3. A question that needs research across the corpus, centered on that sheet.

For less important cultural topics, create three questions per source fiche: one local, one requiring linked fiches, and one requiring wider corpus research. For other topics, use the importance tiers from the project brief: five questions at level 1, three at level 2, and two at level 3. The source tree does not yet label every topic with an importance level; do not guess silently. Record each topic's assigned tier before bulk Q&A production.

Every source sheet, including indexes, must be represented as clean linked text. Q&A should reflect substantive facts and relationships in each sheet; do not omit an index just because it is an index.

## Knowledge fiche frontmatter

Every fiche uses the same plain-text metadata so datasets and cross-links can be checked consistently:

```yaml
type: knowledge-fiche
title: Readable title
description: One-sentence summary.
topic: topic-id
source_doc: docs/temes/topic/source-sheet.md
review_status: complete-with-unresolved
sources:
  - source_id: registered-source-id
    source_doc: docs/fonts/registered-source-id.md
    url: https://example.org/source
    location: page, section, date, or timestamp
    llicencia: exact value recorded in the source card
    redistribucio: si, no, or pendent
related_fiches:
  - knowledge/topic/fichas/related-sheet.md
```

Use `review_status: complete` only when no material question remains open. Use `complete-with-unresolved` when the fiche records what was investigated and why an answer remains unavailable. Related links in the body use relative Markdown links; the metadata list is their stable-ID counterpart.

## Text dataset record

One JSON object per line. Each topic has its own `knowledge/<topic>/dataset.jsonl`. `question_id` is stable and unique. `source_fiche` and `supporting_fiches` point to clean, related fiches under `knowledge/`; `source_doc` preserves the original `docs/` identity. `sources` points to the source record and its exact location.

```json
{"question_id":"topic/doc-slug/local-01","topic":"topic","source_fiche":"knowledge/topic/fichas/doc-slug.md","source_doc":"docs/temes/topic/doc-slug.md","question_kind":"local","question":"Question text.","answer":"Grounded answer, or an explicit statement that it could not be established.","answer_status":"answered","supporting_fiches":[],"sources":[{"source_id":"stable-source-id","source_doc":"docs/fonts/stable-source-id.md","url":"https://example.org/source","location":"page, section, date, or timestamp","llicencia":"exact source-card value","redistribucio":"pendent"}]}
```

`question_kind` is `local`, `related`, or `corpus`. `answer_status` is `answered` or `unresolved`. For `unresolved`, the answer states what could not be determined; `sources` records what was checked. Do not include copied source passages or source documents in a record.

Each topic dataset is a UTF-8 JSONL text file. Use one record per question so each completed question can be committed and pushed independently. Every record must be valid JSON and cite enough evidence to reproduce its answer.
