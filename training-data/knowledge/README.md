# Maia Knowledge

Maia Knowledge converts documented information about Andorra into auditable
chat examples. Its source is `docs/temes/`, including the Markdown content and
its metadata, links, lists and tables. It does not use `docs/raw/` as a source.

## Build and inspect

From the repository root:

```sh
uv run python training-data/knowledge/scripts/extract_inventory.py
uv run python training-data/knowledge/scripts/generate_candidates.py
uv run python training-data/scripts/validate_datasets.py
```

The inventory command writes the evidence ledger and extraction report to
`work/` and `reports/`. The generation command creates source-bound candidates,
coverage and deduplication reports, a deterministic 80/10/10 split manifest,
and three JSONL files under `output/`. The seed is
`maia-training-data-v1`. Global validation checks these outputs against a fresh
in-memory rebuild; details are written to `reports/validation.json`.

## Quality and provenance

Answers quote or summarize inventoried evidence and retain internal evidence
IDs. Those IDs and all other pipeline metadata are excluded from public JSONL.
Exact duplicate conversations are removed. Related evidence groups stay in one
split. Markdown formatting is converted to plain text; substituted strikethrough
text and structural-only content are omitted. Conflicting claims are not
arbitrarily reconciled. Unknowns remain stated. Volatile facts such as current
officeholders, prices, schedules and legislation are excluded from fine-tuning.

Every source's available source-card and redistribution information remains in
the local provenance ledger and reports. A `pendent` or `no` redistribution
status is recorded as-is; it is not permission to redistribute the source or
dataset. Review provenance before any external use.

The default generator is deterministic and makes no model or network calls.
Generated examples are marked for human wording review; a successful structural
validation does not certify factual or editorial quality. Review the local
coverage, exclusion and validation reports before using a build.

Generated work files, reports and JSONL are ignored by Git. See the
[parent README](../README.md) for shared setup and dataset boundaries.
