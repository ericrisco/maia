# MAIA — Model Andorrà d'Intel·ligència Artificial

> The first open-source LLM specialized in Andorra: a **Gemma 4 12B** QLoRA fine-tune that
> answers in normative Catalan with Andorran lexicon, toponymy and institutions, paired with a
> **RAG** system for verifiable, changing facts. Published open on Hugging Face.

**Pattern:** light QLoRA teaches *how to speak* (style, register, stable knowledge); RAG supplies
*what is true right now* (laws, figures, institutions) — following AINA/BSC Salamandra-EADOP.
Measured against its sibling benchmark **AndBench**.

## Status

Milestone **M0 — Foundations** (of M0–M6). See the execution roadmap and per-phase Definition of
Done in the project wiki (harness, out of git).

## Repository layout

```
maia/
├── pyproject.toml            # uv · Python 3.11 · ruff · mypy (strict) · pytest
├── .pre-commit-config.yaml   # ruff (lint+format) + mypy
├── configs/                  # versioned YAML, one per env / per run
├── src/maia/
│   ├── scraping/   # one module per source (diari_sessions, bopa, viquipedia…)
│   ├── corpus/     # cleaning, dedup, tagging, Pydantic schema validation
│   ├── synth/      # taxonomy, grounded generation, filters, LLM-as-judge
│   ├── training/   # Unsloth QLoRA configs + launch scripts
│   ├── evaluation/ # AndBench wrappers, ai-eval-catalan, 4-config matrix
│   ├── rag/        # ingest, chunk-by-article for laws, retrieval
│   └── serving/    # OpenAI-compatible FastAPI + vLLM, Ollama Modelfile
├── tests/                    # pytest — mandatory for every parser and data filter
├── docs/                     # cards, runbooks, openapi.json
└── data/                     # NEVER committed
```

## Development

```bash
uv sync                       # create the env + install dev tools (Python 3.11)
uv run pre-commit install     # enable the local hook
```

Local gate (same checks CI runs), each standalone so a failure can't be masked:

```bash
uv run ruff format --check .
uv run ruff check .
uv run mypy
uv run pytest                 # fast: unit tests. Full suite: uv run pytest -m "unit or integration"
```

## Principles

- **Type hints mandatory** in `src/`; mypy strict. **Tests mandatory** for every parser and data
  filter (the project's #1 source of silent bugs).
- **Reproducibility:** every training run launched from a versioned `configs/` YAML + seed; the
  test split is frozen and hashed, never trained on.
- **License gate:** nothing marked no-redistribute enters public artifacts — such sources are read
  for grounding/contrast only; the public dataset references laws by URL, not literal text.
- **No legal-advisor framing** (system-prompt + model-card disclaimers).
- **Git authorship is always Eric**; conventional commits; PR to protected `main`.

## License

Code: [Apache-2.0](LICENSE). Published dataset: CC-BY (per-source licenses documented in the
dataset card).
