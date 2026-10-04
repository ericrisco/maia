# Maia Language

This dataset preserves authentic contemporary Andorran Catalan from eligible
human material in `docs/parla/`. A piece is eligible only when it declares
`veu: originaria`, `epoca: contemporania` and `apte_llengua: true`. Assistant
text must come from human speech, with only minimal, traceable normalization.

- `scripts/` holds Language pipeline entry points.
- `work/` holds local intermediate records.
- `output/` holds `train.jsonl`, `validation.jsonl` and `test.jsonl` when built.
- `reports/` holds local source, uncertainty and quality reports.

Generated files are ignored by Git. Maia Language does not use Knowledge prose
as a linguistic source and does not inflate a small speech sample with
synthetic assistant text.
