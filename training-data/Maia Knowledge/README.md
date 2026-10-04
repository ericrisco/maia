# Maia Knowledge

This dataset teaches documented knowledge about Andorra. Its primary source is
`docs/temes/`. Answers must be supported by the corpus and its provenance
records. Conflicts and gaps stay explicit. Facts with an expiry date are
reported but kept out of fine-tuning.

- `scripts/` holds Knowledge pipeline entry points.
- `work/` holds local intermediate records.
- `output/` holds `train.jsonl`, `validation.jsonl` and `test.jsonl` when built.
- `reports/` holds local coverage and quality reports.

Generated files are ignored by Git. See the parent README for the boundary
between this dataset and Maia Language.
