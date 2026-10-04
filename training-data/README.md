# Maia Training Data

This directory holds two independent fine-tuning datasets. Keep their sources,
quality rules and generated records separate.

- [Maia Knowledge](Maia%20Knowledge/README.md) teaches documented knowledge
  about Andorra from `docs/temes/`.
- [Maia Language](Maia%20Language/README.md) preserves authentic contemporary
  Andorran Catalan from eligible human material in `docs/parla/`.

Each area has its own `scripts/`, `work/`, `output/` and `reports/` directory.
Generated work files, reports and JSONL outputs stay local and are excluded by
this directory's `.gitignore`. The committed `.gitkeep` files preserve the
empty directory layout when the repository is cloned.

The two datasets do not share training examples. Their source eligibility,
generation and validation rules are documented in the child READMEs.
