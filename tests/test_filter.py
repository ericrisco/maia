"""Tests for the M2.05 filter pipeline."""

from __future__ import annotations

import json
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path
from uuid import uuid4

import pytest

from maia.schemas import (
    CorpusDocument,
    DatasetExample,
    ExampleType,
    License,
    Registre,
    Source,
    Split,
    compute_id,
)
from maia.synth import grammar, judge, semdedup
from maia.synth.filter import (
    TYPE_BANDS,
    FilterReport,
    main,
    read_dataset,
    render,
    run_filters,
)

PASSAGE = "El Consell General es compon de 28 consellers generals."
GROUNDING = compute_id(PASSAGE)


def document() -> CorpusDocument:
    return CorpusDocument.model_validate(
        {
            "id": GROUNDING,
            "text": PASSAGE,
            "source": Source.JURIDIC.value,
            "url": "https://www.portaljuridicandorra.ad/llei/exemple",
            "fetched_at": "2026-07-25T10:00:00+00:00",
            "license": License.PUBLIC_OFFICIAL.value,
            "registre": Registre.ESTANDARD.value,
            "lang": "ca",
        }
    )


CORPUS = judge.index_corpus([document()])


def example(
    prompt: str = "Quants consellers generals hi ha?",
    response: str = "Vint-i-vuit consellers generals.",
    *,
    kind: ExampleType = ExampleType.QA,
    split: Split = Split.TRAIN,
) -> DatasetExample:
    grounded = kind.requires_grounding()
    return DatasetExample.model_validate(
        {
            "id": str(uuid4()),
            "messages": [
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": response},
            ],
            "type": kind.value,
            "topic": "institucions/consell-general" if grounded else "general_ca/instrucat",
            "grounding_ids": [GROUNDING] if grounded else [],
            "generator": "claude-opus-5",
            "judge_score": 0.0 if not grounded else 0.9,
            "split": split.value,
        }
    )


#: Distinct vocabulary per example, so the bag-of-words fake embedder does not read a shared
#: template as a near-duplicate. Real embeddings would not, but the fake has no semantics.
_WORDS = (
    "muntanya",
    "riu",
    "poble",
    "carrer",
    "taula",
    "finestra",
    "llibre",
    "camí",
    "pedra",
    "arbre",
    "núvol",
    "vent",
    "aigua",
    "foc",
    "terra",
    "ferro",
    "fusta",
    "paper",
    "vidre",
    "llana",
    "seda",
    "plom",
    "coure",
    "estany",
    "or",
    "plata",
    "bronze",
    "marbre",
    "argila",
    "sorra",
    "gel",
    "neu",
    "pluja",
    "boira",
    "sol",
    "lluna",
    "estrella",
    "planeta",
    "cometa",
    "nebulosa",
    "galàxia",
    "buit",
    "espai",
    "temps",
    "hora",
    "minut",
    "segon",
    "dia",
    "setmana",
    "mes",
    "any",
    "segle",
    "mil·lenni",
    "instant",
    "moment",
    "durada",
    "ritme",
    "compàs",
    "nota",
    "clau",
    "octava",
    "escala",
    "acord",
    "melodia",
    "harmonia",
    "timbre",
    "ressonància",
    "silenci",
    "soroll",
    "eco",
    "veu",
    "cant",
    "crit",
    "xiuxiueig",
    "murmuri",
    "tro",
    "llamp",
    "calamarsa",
    "rosada",
    "gebre",
    "glaç",
    "desglaç",
    "riuada",
    "torrent",
    "cascada",
    "gorg",
    "llac",
    "mar",
    "oceà",
    "onada",
    "marea",
    "escuma",
    "sal",
    "iode",
    "plàncton",
    "corall",
    "alga",
    "peix",
)


def compliant_dataset(size: int = 100) -> list[DatasetExample]:
    """A dataset whose type shares satisfy §3.2 — 8 % no_ho_se, 17 % general_ca."""
    examples: list[DatasetExample] = []
    for index in range(size):
        if index % 100 < 8:
            kind = ExampleType.NO_HO_SE
        elif index % 100 < 25:
            kind = ExampleType.GENERAL_CA
        else:
            kind = ExampleType.QA
        word = _WORDS[index % len(_WORDS)]
        examples.append(
            example(f"Què saps sobre {word}?", f"Una explicació sobre {word}.", kind=kind)
        )
    return examples


@dataclass
class WordEmbedder:
    # Wider than the fixture vocabulary, so distinct words land in distinct slots. A narrower
    # space makes unrelated sentences collide, which is a fake artefact, not real geometry.
    dimensions: int = 512
    vocabulary: dict[str, int] = field(default_factory=dict)

    def embed(self, texts: Sequence[str]) -> list[semdedup.Vector]:
        vectors: list[semdedup.Vector] = []
        for text in texts:
            vector = [0.0] * self.dimensions
            for word in text.lower().split():
                vector[
                    self.vocabulary.setdefault(word, len(self.vocabulary) % self.dimensions)
                ] += 1
            vectors.append(vector)
        return vectors


@dataclass
class ScriptedCompleter:
    score: float = 1.0
    calls: int = 0

    def complete(self, prompt: str) -> str:
        self.calls += 1
        return json.dumps({"score": self.score, "reason": "ok", "unsupported": []})


@dataclass
class ScriptedService:
    matches: list[grammar.Match] = field(default_factory=list)

    def check(self, text: str, language: str = grammar.LANGUAGE) -> list[grammar.Match]:
        return list(self.matches)


# ─────────────────────────────────────────────────────────────
# Nothing wired
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_with_no_filters_wired_every_stage_is_reported_not_run() -> None:
    """Blocked-by-resource is the normal state of this repo, and it must not read as clean."""
    examples = compliant_dataset()
    survivors, report = run_filters(examples)
    assert survivors == examples
    assert report.skipped == ["semantic dedup", "factual-support judge", "Catalan check"]
    rendered = render(report)
    assert rendered.count("NOT RUN") == 3
    assert "nothing was checked" in rendered


@pytest.mark.unit
def test_a_judge_without_a_corpus_is_refused() -> None:
    """It would fail every example for a missing passage and call that a filter run."""
    with pytest.raises(ValueError, match="needs the corpus"):
        run_filters(
            compliant_dataset(), factual_judge=judge.FactualSupportJudge(ScriptedCompleter())
        )


# ─────────────────────────────────────────────────────────────
# Order and composition
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_dedup_runs_before_the_judge_so_duplicates_are_not_paid_for() -> None:
    """A judge call costs money; a cosine does not."""
    duplicated = [example("Quants consellers hi ha?") for _ in range(4)]
    completer = ScriptedCompleter()
    _, report = run_filters(
        duplicated,
        embedder=WordEmbedder(),
        factual_judge=judge.FactualSupportJudge(completer),
        corpus=CORPUS,
        threshold=0.9,
    )
    assert report.dedup is not None and report.dedup.dropped == 3
    assert completer.calls == 1


@pytest.mark.unit
def test_all_three_stages_report_and_compose() -> None:
    examples = compliant_dataset()
    survivors, report = run_filters(
        examples,
        embedder=WordEmbedder(),
        factual_judge=judge.FactualSupportJudge(ScriptedCompleter()),
        corpus=CORPUS,
        catalan=grammar.CatalanCheck(ScriptedService()),
    )
    assert report.skipped == []
    assert report.dedup is not None
    assert report.judged is not None
    assert report.grammar is not None
    assert report.finished == len(survivors)
    assert report.started == len(examples)


@pytest.mark.unit
def test_the_judge_writes_scores_that_survive_the_later_stage() -> None:
    survivors, _ = run_filters(
        [example()],
        factual_judge=judge.FactualSupportJudge(ScriptedCompleter(score=0.85)),
        corpus=CORPUS,
        catalan=grammar.CatalanCheck(ScriptedService()),
    )
    assert survivors[0].judge_score == 0.85


@pytest.mark.unit
def test_the_total_dropped_is_the_sum_of_what_the_stages_removed() -> None:
    examples = [*compliant_dataset(50), example("Quants consellers hi ha?")]
    examples.append(example("Quants consellers hi ha?"))
    _, report = run_filters(examples, embedder=WordEmbedder(), threshold=0.9)
    assert report.dropped == report.started - report.finished
    assert report.dedup is not None
    assert report.dropped == report.dedup.dropped


# ─────────────────────────────────────────────────────────────
# §3.2 compliance after filtering — the point of the orchestrator
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_compliant_dataset_stays_compliant_when_nothing_is_dropped() -> None:
    _, report = run_filters(compliant_dataset())
    assert report.compliant
    assert report.violations == []
    assert "✓ no_ho_se" in render(report)


@pytest.mark.unit
def test_filtering_that_breaks_a_ban_is_a_failure_not_a_caveat() -> None:
    """The judge drops unevenly, so the surviving shares move.

    Here every grounded example fails, so only the exempt types survive and general_ca ends at
    100 % of what is left — far outside §3.2, and with the honesty examples gone entirely.
    Reporting that as a successful filter run would hand Phase 3 a dataset the validator rejects.
    """
    _, report = run_filters(
        compliant_dataset(),
        factual_judge=judge.FactualSupportJudge(ScriptedCompleter(score=0.0)),
        corpus=CORPUS,
    )
    assert not report.compliant
    assert any("general_ca" in violation for violation in report.violations)
    rendered = render(report)
    assert "✗" in rendered
    assert "before filtering →" in rendered


@pytest.mark.unit
def test_the_report_shows_the_share_before_and_after() -> None:
    _, report = run_filters(
        compliant_dataset(),
        factual_judge=judge.FactualSupportJudge(ScriptedCompleter(score=0.0)),
        corpus=CORPUS,
    )
    assert report.shares_before[ExampleType.QA] == pytest.approx(0.75)
    assert ExampleType.QA not in report.shares_after
    assert "17.0% before filtering → 100.0%" in render(report)


@pytest.mark.unit
def test_the_bands_are_the_ones_3_2_constrains() -> None:
    assert TYPE_BANDS[ExampleType.NO_HO_SE] == (0.06, 0.10)
    assert TYPE_BANDS[ExampleType.GENERAL_CA] == (0.15, 0.20)


@pytest.mark.unit
def test_an_empty_dataset_reports_no_shares() -> None:
    _, report = run_filters([])
    assert report.shares_after == {}
    assert "distribution after filtering" not in render(report)


@pytest.mark.unit
def test_a_dataset_missing_a_constrained_type_is_not_compliant() -> None:
    """A dataset of pure qa has no anti-forgetting mix at all, which is a §3.2 violation."""
    report = FilterReport(started=1, finished=1, shares_after={ExampleType.QA: 1.0})
    assert not report.compliant
    assert len(report.violations) == 2


# ─────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────


def write_dataset(path: Path, examples: list[DatasetExample]) -> Path:
    path.write_text("".join(f"{e.model_dump_json()}\n" for e in examples), encoding="utf-8")
    return path


def write_corpus(path: Path) -> Path:
    path.write_text(f"{document().model_dump_json()}\n", encoding="utf-8")
    return path


@pytest.mark.unit
def test_cli_with_nothing_wired_reports_three_stages_not_run(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    dataset = write_dataset(tmp_path / "dataset.jsonl", compliant_dataset())
    assert main([str(dataset)]) == 0
    printed = capsys.readouterr().out
    assert printed.count("NOT RUN") == 3
    assert "100/100 kept" in printed


@pytest.mark.unit
def test_cli_writes_the_survivors(tmp_path: Path) -> None:
    dataset = write_dataset(tmp_path / "dataset.jsonl", compliant_dataset())
    out = tmp_path / "filtered" / "dataset.jsonl"
    assert main([str(dataset), "--out", str(out)]) == 0
    assert len(read_dataset(out)) == 100


@pytest.mark.unit
def test_cli_fails_when_the_surviving_dataset_breaks_3_2(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    dataset = write_dataset(tmp_path / "dataset.jsonl", [example() for _ in range(10)])
    assert main([str(dataset)]) == 1
    assert "✗ no_ho_se" in capsys.readouterr().out


@pytest.mark.unit
def test_cli_reports_a_missing_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main([str(tmp_path / "absent.jsonl")]) == 1
    assert "no such file" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_refuses_the_judge_without_a_corpus(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    dataset = write_dataset(tmp_path / "dataset.jsonl", compliant_dataset())
    assert main([str(dataset), "--judge"]) == 1
    assert "--judge needs --corpus" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_loads_the_corpus_for_the_judge(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The judge's client is blocked-by-resource, so the seam is patched, not the logic."""
    dataset = write_dataset(tmp_path / "dataset.jsonl", compliant_dataset())
    corpus = write_corpus(tmp_path / "corpus.jsonl")
    monkeypatch.setattr("maia.synth.generate.anthropic_client", lambda *a, **k: object())
    monkeypatch.setattr(
        judge.FactualSupportJudge,
        "run",
        lambda self, examples, corpus_index, **kwargs: (
            list(examples),
            judge.JudgeReport(examined=len(examples), judged=len(examples)),
        ),
    )
    assert main([str(dataset), "--corpus", str(corpus), "--judge"]) == 0


@pytest.mark.unit
def test_cli_wires_the_languagetool_url(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    dataset = write_dataset(tmp_path / "dataset.jsonl", compliant_dataset())
    monkeypatch.setattr(
        "maia.synth.grammar.languagetool_service", lambda url, **kwargs: ScriptedService()
    )
    assert main([str(dataset), "--languagetool", "http://localhost:8081/v2/check"]) == 0


@pytest.mark.unit
def test_cli_wires_the_embeddings_url(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    dataset = write_dataset(tmp_path / "dataset.jsonl", compliant_dataset())
    monkeypatch.setattr("maia.synth.semdedup.ollama_embedder", lambda url, **kwargs: WordEmbedder())
    assert main([str(dataset), "--embeddings-url", "http://localhost:11434/api/embed"]) == 0
    assert "semantic dedup:" in capsys.readouterr().out


@pytest.mark.unit
def test_cli_passes_the_glossary_to_the_catalan_check(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    dataset = write_dataset(tmp_path / "dataset.jsonl", compliant_dataset())
    glossary = Path(__file__).resolve().parents[1] / "configs" / "glossari-andorra.yaml"
    service = ScriptedService(
        [grammar.Match(rule_id="MORFOLOGIK_RULE_CA_ES", category="TYPOS", message="", text="comú")]
    )
    monkeypatch.setattr("maia.synth.grammar.languagetool_service", lambda url, **kwargs: service)
    assert main([str(dataset), "--glossary", str(glossary), "--languagetool", "http://x/"]) == 0
    assert "excused as Andorran lexicon" in capsys.readouterr().out


@pytest.mark.unit
def test_cli_reports_an_unverifiable_grounding(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """An example citing a passage the given corpus does not hold is a finding, not a pass."""
    dataset = write_dataset(tmp_path / "dataset.jsonl", compliant_dataset())
    empty_corpus = tmp_path / "corpus.jsonl"
    empty_corpus.write_text("", encoding="utf-8")
    monkeypatch.setattr("maia.synth.generate.anthropic_client", lambda *a, **k: object())
    # No model call is patched, and none happens: the grounding lookup fails first.
    assert main([str(dataset), "--corpus", str(empty_corpus), "--judge"]) == 1
    assert "could not be judged" in capsys.readouterr().out


@pytest.mark.unit
def test_cli_reports_a_filter_that_could_not_run(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A misbehaving service is an error, not an empty result set."""

    @dataclass
    class Truncating:
        def embed(self, texts: Sequence[str]) -> list[semdedup.Vector]:
            return []

    dataset = write_dataset(tmp_path / "dataset.jsonl", compliant_dataset())
    monkeypatch.setattr("maia.synth.semdedup.ollama_embedder", lambda url, **kwargs: Truncating())
    assert main([str(dataset), "--embeddings-url", "http://localhost:11434/api/embed"]) == 1
    assert "refusing to pair examples" in capsys.readouterr().err
