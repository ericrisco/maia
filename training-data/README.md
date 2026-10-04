# Maia Training Data

This directory contains two independent chat fine-tuning datasets. Both are
derived only from the versioned `docs/` corpus. Their source eligibility,
provenance and transformations stay separate.

## Regenerate

Run from the repository root with Python 3.12 and the project dependencies
installed through `uv`:

```sh
uv run python training-data/knowledge/scripts/extract_inventory.py
uv run python training-data/knowledge/scripts/generate_candidates.py
uv run python training-data/language/scripts/extract_speech.py
uv run python training-data/scripts/validate_datasets.py
```

The commands read `docs/` and write local intermediate files and reports under
each dataset's `work/` and `reports/` directories. The generators write
`train.jsonl`, `validation.jsonl` and `test.jsonl` under each `output/`
directory. The final public JSONL schema contains only a `messages` array with
one non-empty `user` message followed by one non-empty `assistant` message.

`validate_datasets.py` rebuilds the ledgers in memory and checks public schema,
plain text, duplicates, provenance, eligibility, evidence coverage, uncertainty
filters and split leakage. It writes a detailed local report to
`knowledge/reports/validation.json` and exits non-zero on failure. Generated
JSONL, reports and work files are ignored by Git; only code, documentation and
empty-directory placeholders are versioned.

## Dataset boundaries

- [Maia Knowledge](knowledge/README.md) uses documented material from
  `docs/temes/`. Every answer is traceable to evidence. Conflicts remain
  unresolved, unknowns stay explicit, and volatile facts are excluded from
  fine-tuning.
- [Maia Language](language/README.md) uses eligible original,
  contemporary Andorran speech from `docs/parla/`. It preserves human wording
  and does not synthesize dialogue.

The Language output is currently empty: 38 corpus pieces meet the metadata
eligibility rules, but the source contains no explicitly labelled speaker turns
that can safely be converted into user/assistant pairs. The pipeline does not
turn monologue or rhetorical questions into invented dialogue.

The source cards for the speech pieces currently mark redistribution as
`pendent`. Provenance is recorded in local reports and this status is not a
grant of redistribution permission. The Knowledge pipeline likewise records
source-card and redistribution status for audit.
