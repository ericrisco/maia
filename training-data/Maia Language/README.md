# Maia Language

Maia Language preserves authentic contemporary Andorran Catalan. It selects
human material from `docs/parla/`; Knowledge prose, translations and synthetic
assistant responses are not linguistic sources.

## Build and inspect

From the repository root:

```sh
uv run python 'training-data/Maia Language/scripts/extract_speech.py'
uv run python training-data/scripts/validate_datasets.py
```

A piece is eligible only when its metadata has `veu: originaria`,
`epoca: contemporania` and `apte_llengua: true`. The extraction command records
eligible and excluded pieces, authentic segments, uncertainty spans, candidate
turns and deterministic split assignments under `work/` and `reports/`.
Generated `train.jsonl`, `validation.jsonl` and `test.jsonl` live under
`output/`; the split seed is `maia-training-data-v1`. The global validator
checks exact source spans, source eligibility, uncertainty filtering, public
schema and that a source piece, speaker group or conversation does not cross
splits.

## Current corpus limitation

There are 38 eligible pieces in the current corpus, but none has explicitly
labelled interviewer and respondent turns. The extractor therefore emits zero
chat pairs and empty split files. It does not infer a user question from a
monologue, rhetorical question or narration. Add genuinely labelled human
dialogue to the source corpus before expecting non-empty output.

Uncertain transcript spans are retained in the audit ledger and excluded from
candidate turns when they overlap those turns. The human assistant text must
match its source span exactly. Only traceable spacing, punctuation,
capitalization or source-verified transcription typo normalization is permitted.

The speech source cards currently report redistribution as `pendent`. This
status is recorded, not treated as redistribution permission. Check the
source's licence and terms before sharing any derived dataset. Generated files
are local and ignored by Git. See the [parent README](../README.md).
