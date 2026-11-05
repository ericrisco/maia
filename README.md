# maia

An open model specialised in Andorra, built from Gemma 4, and the open corpus of Andorran knowledge behind it:
history, language, institutions, customs and speech, each document with its provenance.

**Experimental: these are not final models.** They recall far more of the facts they were taught, but they still make
things up. Read [how maia was trained](https://ericrisco.github.io/maia-bench/training.html) before trusting a figure.

| | |
|---|---|
| Models | [`gemma-maia-12b`](https://huggingface.co/ericrisco/gemma-maia-12b), [`gemma-maia-e4b`](https://huggingface.co/ericrisco/gemma-maia-e4b) |
| Training data | [`maia-training-data`](https://huggingface.co/datasets/ericrisco/maia-training-data) |
| Benchmark | [maia-bench](https://ericrisco.github.io/maia-bench/) ([code](https://github.com/ericrisco/maia-bench)) |
| Training guide | [`training/README.md`](training/README.md) |

## Results

| | Gemma 4 E4B → maia E4B | Gemma 4 12B → maia 12B |
|---|---|---|
| Facts recalled, on 338 questions in unseen wording | 7 % → 36 % | 12 % → 47 % |
| maia-bench, 926 questions | 30.3 % → 32.9 % | 37.4 % → 43.3 % (inflated) |

The 12B benchmark gain is inflated, because its multiple-choice practice resembles benchmark questions. On questions
with no similar practice question, the gain is +0.8 points, 95 % CI [−2.6, +4.1], which is not significant.

## What is here

| Path | What it is |
|---|---|
| `docs/` | The corpus. It opens directly as an Obsidian vault. |
| `docs/temes/` | Compiled knowledge, by domain. |
| `docs/parla/` | Speech transcripts and candidates, with provenance and verification status per file. |
| `docs/fonts/` | One record per source: owner, licence and redistribution. |
| `training-data/` | The conversations and facts the models train on, and the scripts that generate them. |
| `scripts/exporta_dataset.py` | Builds the training export from `training-data/datasets/`. |
| `training/` | Training, evaluation and publishing on Google Cloud. |
| `src/cervell/` | The tool that validates the corpus and generates its contract and index. |
| `schema/corpus.toml` | The source of truth for fields, enums and rules. |

Corpus content, the Catalan field names and the training data are in Catalan, which is the point of the project.

## The distinction behind the corpus

Every document declares **who produced the text** and **which period its language is from**:

```yaml
veu: originaria | compilada        # verbatim Andorran, or written by an agent
epoca: contemporania | historica   # today's language, or another time's
apte_llengua                       # derived: true if originaria and contemporania
```

A text about Andorra is not the same as a text in Andorran Catalan. The derivation is a rule, so it is not argued
document by document.

## Corpus status

Initial collection closed on 24 September 2026, with 1,347 articles, 618 source records and 40 speech documents in the
editorial inventory. Closing collection does not certify that all the material is fit for training. See the
[closing record](docs/raw/estat-projecte/tancament-obtencio-v1.md) and the
[curation map](docs/raw/curacio/mapa-inicial.md).

## Usage

```bash
uv sync
uv run cervell check docs/    # validates the whole corpus
uv run pytest                 # the test suite
```

The input contract in `docs/CONTRACT.md` is generated from `schema/corpus.toml`. Do not edit it by hand: what a person
reads and what the machine checks come from the same source, so they cannot diverge.

## Licence

To be determined. Each corpus source declares its own in its record.
