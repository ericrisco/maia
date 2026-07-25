"""Tests for the dataset distribution report (PLAN M2.09)."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from uuid import UUID, uuid5

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
from maia.synth.distribution import (
    TARGET_SIZE,
    TYPE_BANDS,
    Lengths,
    Profile,
    main,
    profile,
    read_corpus,
    read_dataset,
    render,
    sources_of,
    text_of,
)
from maia.synth.glossary import Glossary
from maia.synth.taxonomy import Taxonomy

_NAMESPACE = UUID("6ba7b816-9dad-11d1-80b4-00c04fd430c8")


def document(index: int, source: Source = Source.JURIDIC) -> CorpusDocument:
    text = f"El comú de la parròquia gestiona el territori. Passatge {index}."
    return CorpusDocument.model_validate(
        {
            "id": compute_id(text),
            "text": text,
            "source": source.value,
            "url": f"https://www.portaljuridicandorra.ad/{index}",
            "fetched_at": "2026-07-25T10:00:00+00:00",
            "license": License.PUBLIC_OFFICIAL.value,
            "registre": Registre.ESTANDARD.value,
            "lang": "ca",
        }
    )


LEGAL = [document(index) for index in range(4)]
SPOKEN = [document(index + 100, Source.CONSELL_DIARI_SESSIONS) for index in range(2)]
CORPUS = {doc.id: doc for doc in [*LEGAL, *SPOKEN]}


def example(
    tag: str,
    *,
    kind: ExampleType = ExampleType.QA,
    node: str = "institucions/comuns",
    split: Split = Split.TRAIN,
    score: float = 0.9,
    grounding: list[CorpusDocument] | None = None,
    response: str = "El comú gestiona el territori de la parròquia.",
    turns: int = 2,
) -> DatasetExample:
    cites = kind.requires_grounding()
    messages = [
        {"role": "user", "content": f"Què fa el comú? ({tag})"},
        {"role": "assistant", "content": response},
    ]
    if turns > 2:
        messages += [
            {"role": "user", "content": "I el cònsol major?"},
            {"role": "assistant", "content": "Presideix el comú."},
        ]
    return DatasetExample.model_validate(
        {
            "id": str(uuid5(_NAMESPACE, tag)),
            "messages": messages,
            "type": kind.value,
            "topic": node if cites else "general_ca/instrucat",
            "grounding_ids": sorted({doc.id for doc in (grounding or LEGAL[:1])}) if cites else [],
            "generator": "claude-opus-5",
            "judge_score": score if cites else 0.0,
            "split": split.value,
        }
    )


def taxonomy(node_ids: list[str]) -> Taxonomy:
    return Taxonomy.model_validate(
        {
            "version": "test",
            "approved": True,
            "approved_by": "PO",
            "nodes": [
                {"id": node, "label": node, "keywords": ["comú"], "weight": 1.0}
                for node in node_ids
            ],
        }
    )


GLOSSARY = Glossary.model_validate(
    {
        "version": "test",
        "entries": [
            {"term": "comú", "category": "institucional", "gloss": "Govern de la parròquia."},
            {"term": "esquellots", "category": "cultural", "gloss": "Costum popular."},
        ],
    }
)


def dataset(size: int = 100) -> list[DatasetExample]:
    """A dataset with §3.2-compliant type shares and 90/5/5 splits."""
    examples: list[DatasetExample] = []
    for index in range(size):
        position = index % 100
        if position < 8:
            kind = ExampleType.NO_HO_SE
        elif position < 25:
            kind = ExampleType.GENERAL_CA
        else:
            kind = ExampleType.QA
        if position < 90:
            split = Split.TRAIN
        elif position < 95:
            split = Split.VAL
        else:
            split = Split.TEST
        examples.append(
            example(
                f"e{index}",
                kind=kind,
                split=split,
                grounding=[LEGAL[index % len(LEGAL)]],
            )
        )
    return examples


# ─────────────────────────────────────────────────────────────
# Basic measurement
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_types_splits_and_nodes_are_counted() -> None:
    measured = profile(dataset(100))
    assert measured.total == 100
    assert measured.by_type[ExampleType.QA.value] == 75
    assert measured.by_type[ExampleType.NO_HO_SE.value] == 8
    assert measured.by_split[Split.TRAIN.value] == 90
    assert measured.share_of_type(ExampleType.GENERAL_CA) == pytest.approx(0.17)
    assert measured.share_of_split(Split.TEST) == pytest.approx(0.05)


@pytest.mark.unit
def test_an_empty_dataset_measures_to_zero_not_an_error() -> None:
    measured = profile([])
    assert measured.total == 0
    assert measured.share_of_type(ExampleType.QA) == 0.0
    assert measured.share_of_split(Split.TRAIN) == 0.0
    assert measured.lengths == Lengths()


@pytest.mark.unit
def test_lengths_are_summarised_with_percentiles() -> None:
    lengths = Lengths.of([10, 20, 30, 40, 100])
    assert lengths.count == 5
    assert lengths.total == 200
    assert lengths.mean == 40.0
    assert lengths.p50 == 30
    assert lengths.p95 == 100
    assert lengths.longest == 100
    assert lengths.shortest == 10


@pytest.mark.unit
def test_lengths_of_nothing_are_all_zero() -> None:
    assert Lengths.of([]) == Lengths()


@pytest.mark.unit
def test_lengths_of_one_value_are_that_value() -> None:
    lengths = Lengths.of([42])
    assert lengths.p50 == lengths.p95 == lengths.longest == lengths.shortest == 42


@pytest.mark.unit
def test_lengths_are_reported_per_type() -> None:
    measured = profile(
        [
            example("short", response="Curt."),
            example("long", response="Una resposta considerablement més llarga que l'altra."),
            example("gc", kind=ExampleType.GENERAL_CA),
        ]
    )
    assert measured.lengths_by_type[ExampleType.QA.value].count == 2
    assert measured.lengths_by_type[ExampleType.GENERAL_CA.value].count == 1


@pytest.mark.unit
def test_turns_are_counted() -> None:
    measured = profile([example("a"), example("b", kind=ExampleType.MULTITURN, turns=4)])
    assert measured.turns == {2: 1, 4: 1}


@pytest.mark.unit
def test_the_text_of_an_example_is_every_message() -> None:
    text = text_of(example("a"))
    assert "Què fa el comú?" in text
    assert "El comú gestiona" in text


# ─────────────────────────────────────────────────────────────
# Taxonomy coverage — a node that produced nothing
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_node_that_produced_nothing_is_named() -> None:
    """A twelfth of the approved subject matter being absent is invisible to every §3.2 check."""
    measured = profile(
        [example("a", node="institucions/comuns")],
        taxonomy=taxonomy(["institucions/comuns", "historia/pareatges", "cultura/falles"]),
    )
    assert measured.empty_nodes == ["cultura/falles", "historia/pareatges"]
    assert not measured.publishable
    assert any("produced no examples" in finding for finding in measured.findings)
    assert "produced nothing" in render(measured)


@pytest.mark.unit
def test_full_node_coverage_is_not_a_finding() -> None:
    measured = profile(
        [example("a", node="institucions/comuns"), example("b", node="cultura/falles")],
        taxonomy=taxonomy(["institucions/comuns", "cultura/falles"]),
    )
    assert measured.empty_nodes == []
    assert not any("produced no examples" in finding for finding in measured.findings)


@pytest.mark.unit
def test_without_a_taxonomy_nothing_is_claimed_about_nodes() -> None:
    """What is not supplied is not reported — never assumed clean."""
    measured = profile([example("a")])
    assert measured.empty_nodes == []
    assert len(measured.by_node) == 1


# ─────────────────────────────────────────────────────────────
# Grounding by corpus source — was M1's work actually used?
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_grounding_is_attributed_to_corpus_sources() -> None:
    measured = profile([example("a", grounding=[LEGAL[0], SPOKEN[0]])], corpus=CORPUS)
    assert measured.by_source[Source.JURIDIC.value] == 1
    assert measured.by_source[Source.CONSELL_DIARI_SESSIONS.value] == 1
    assert measured.grounding_citations == 2
    assert measured.distinct_passages == 2


@pytest.mark.unit
def test_a_source_never_cited_is_a_finding() -> None:
    """M1 spent five milestones on the spoken subcorpus; if nothing cites it, it is not here."""
    measured = profile([example("a", grounding=[LEGAL[0]])], corpus=CORPUS)
    assert measured.unused_sources == [Source.CONSELL_DIARI_SESSIONS.value]
    assert not measured.publishable
    assert "never cited" in render(measured)


@pytest.mark.unit
def test_a_grounding_id_absent_from_the_corpus_is_a_finding() -> None:
    """Those examples cannot be traced to a source."""
    measured = profile([example("a", grounding=[LEGAL[0]])], corpus={SPOKEN[0].id: SPOKEN[0]})
    assert measured.unknown_passages == 1
    assert any("not in the corpus supplied" in finding for finding in measured.findings)


@pytest.mark.unit
def test_without_a_corpus_no_source_claims_are_made() -> None:
    measured = profile([example("a")])
    assert measured.by_source == {}
    assert measured.unused_sources == []
    assert measured.unknown_passages == 0


@pytest.mark.unit
def test_the_sources_of_a_corpus_are_reported() -> None:
    assert sources_of(CORPUS.values()) == {Source.JURIDIC, Source.CONSELL_DIARI_SESSIONS}


# ─────────────────────────────────────────────────────────────
# Judging — telling "scored zero" from "never judged"
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_an_unjudged_grounded_example_is_distinguished_from_an_exempt_one() -> None:
    """judge_score = 0.0 means two different things; only one of them is fine."""
    measured = profile(
        [
            example("judged", score=0.9),
            example("never", score=0.0),
            example("exempt", kind=ExampleType.GENERAL_CA),
            example("style", kind=ExampleType.ESTIL_ANDORRA),
        ],
        corpus=CORPUS,
    )
    assert measured.judged == 1
    assert measured.exempt == 2
    assert len(measured.unjudged_grounded) == 1
    assert any("never judged" in finding for finding in measured.findings)
    assert "never judged" in render(measured)


@pytest.mark.unit
def test_the_mean_score_covers_only_judged_examples() -> None:
    measured = profile(
        [
            example("a", score=1.0),
            example("b", score=0.8),
            example("exempt", kind=ExampleType.GENERAL_CA),
        ]
    )
    assert measured.mean_score == pytest.approx(0.9)


@pytest.mark.unit
def test_scores_are_bucketed() -> None:
    measured = profile(
        [
            example("a", score=0.95),
            example("b", score=0.85),
            example("c", score=0.75),
            example("d", score=0.6),
            example("e", score=0.2),
        ]
    )
    assert measured.score_buckets == {
        "0.9-1.0": 1,
        "0.8-0.9": 1,
        "0.7-0.8": 1,
        "0.5-0.7": 1,
        "<0.5": 1,
    }
    assert "score distribution" in render(measured)


@pytest.mark.unit
def test_a_fully_unjudged_dataset_reports_a_zero_mean_not_a_crash() -> None:
    measured = profile([example("a", kind=ExampleType.GENERAL_CA)])
    assert measured.mean_score == 0.0
    assert measured.judged == 0


# ─────────────────────────────────────────────────────────────
# Andorran lexicon reach
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_lexicon_reach_is_measured_not_assumed() -> None:
    """M2.03 requires the glossary; whether the output contains it is a measurement."""
    with_term = example("with", response="El comú gestiona la parròquia.")
    without = example("without", response="Una resposta sense cap terme del glossari.")
    # The default prompt mentions the glossary term, so the second example needs a clean one too.
    without = without.model_copy(
        update={
            "messages": [
                without.messages[0].model_copy(update={"content": "Explica-ho, si us plau."}),
                without.messages[1],
            ]
        }
    )
    measured = profile([with_term, without], glossary=GLOSSARY)
    assert measured.glossary_hits == 1
    assert measured.glossary_terms_seen == 1
    assert measured.glossary_terms_total == 2
    assert "Andorran lexicon" in render(measured)


@pytest.mark.unit
def test_a_term_that_never_appears_is_reflected_in_the_count() -> None:
    measured = profile([example("a", response="El comú.")], glossary=GLOSSARY)
    assert measured.glossary_terms_seen == 1  # `esquellots` never appears
    assert "1/2 terms appear" in render(measured)


@pytest.mark.unit
def test_without_a_glossary_no_lexicon_claim_is_made() -> None:
    measured = profile([example("a")])
    assert measured.glossary_terms_total == 0
    assert "Andorran lexicon" not in render(measured)


# ─────────────────────────────────────────────────────────────
# The publishability verdict
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_dataset_of_the_right_size_and_shape_is_publishable() -> None:
    measured = Profile(
        total=12_000,
        by_type=Counter({"qa": 9_000, "no_ho_se": 960, "general_ca": 2_040}),
        by_split=Counter({"train": 10_800, "val": 600, "test": 600}),
    )
    assert measured.size_ok
    assert measured.type_violations == []
    assert measured.split_violations == []
    assert measured.publishable
    assert "✓ publishable" in render(measured)


@pytest.mark.unit
def test_a_type_outside_its_band_blocks_publication() -> None:
    measured = profile(
        [example(f"e{index}") for index in range(100)],  # 100 % qa: no no_ho_se, no general_ca
    )
    assert len(measured.type_violations) == 2
    assert not measured.publishable
    assert "✗ not publishable" in render(measured)
    assert "## Findings" in render(measured)


@pytest.mark.unit
def test_a_split_outside_tolerance_blocks_publication() -> None:
    measured = profile([example(f"e{index}", split=Split.TRAIN) for index in range(100)])
    assert any("val" in violation for violation in measured.split_violations)
    assert not measured.publishable


@pytest.mark.unit
def test_a_dataset_outside_the_dod_size_range_blocks_publication() -> None:
    measured = profile(dataset(100))
    assert not measured.size_ok
    assert any("outside DoD-F2's" in finding for finding in measured.findings)
    assert TARGET_SIZE == (10_000, 15_000)


@pytest.mark.unit
def test_the_bands_are_the_ones_3_2_constrains() -> None:
    assert TYPE_BANDS[ExampleType.NO_HO_SE] == (0.06, 0.10)
    assert TYPE_BANDS[ExampleType.GENERAL_CA] == (0.15, 0.20)


# ─────────────────────────────────────────────────────────────
# The rendered report
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_report_is_markdown_with_the_sections_the_dataset_card_needs() -> None:
    measured = profile(
        dataset(100), taxonomy=taxonomy(["institucions/comuns"]), corpus=CORPUS, glossary=GLOSSARY
    )
    report = render(measured, name="maia-dataset.jsonl")
    assert report.startswith("# Dataset distribution — maia-dataset.jsonl")
    for heading in (
        "## Types",
        "## Splits",
        "## Grounding",
        "## Judging",
        "## Coverage",
        "## Shape",
    ):
        assert heading in report
    assert "| type | count | share | §3.2 | mean chars |" in report


@pytest.mark.unit
def test_the_report_marks_each_constrained_type() -> None:
    report = render(profile(dataset(100)))
    assert "| `no_ho_se` |" in report
    assert "| `qa` | 75 | 75.0% | — |" in report


@pytest.mark.unit
def test_a_clean_report_has_no_findings_section() -> None:
    measured = Profile(
        total=12_000,
        by_type=Counter({"qa": 9_000, "no_ho_se": 960, "general_ca": 2_040}),
        by_split=Counter({"train": 10_800, "val": 600, "test": 600}),
    )
    assert "## Findings" not in render(measured)


@pytest.mark.unit
def test_the_report_lists_generators_and_total_characters() -> None:
    report = render(profile(dataset(20)))
    assert "`claude-opus-5`" in report
    assert "characters in total" in report


# ─────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────


def write_dataset(path: Path, examples: list[DatasetExample]) -> Path:
    path.write_text("".join(f"{e.model_dump_json()}\n" for e in examples), encoding="utf-8")
    return path


def write_corpus(path: Path, documents: list[CorpusDocument]) -> Path:
    path.write_text("".join(f"{d.model_dump_json()}\n" for d in documents), encoding="utf-8")
    return path


def write_taxonomy(path: Path, node_ids: list[str]) -> Path:
    path.write_text(
        "version: test\napproved: true\napproved_by: PO\nnodes:\n"
        + "".join(
            f"  - id: {node}\n    label: {node}\n    keywords: [comú]\n    weight: 1.0\n"
            for node in node_ids
        ),
        encoding="utf-8",
    )
    return path


@pytest.mark.unit
def test_cli_prints_and_writes_the_report(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = write_dataset(tmp_path / "dataset.jsonl", dataset(100))
    out = tmp_path / "reports" / "distribution.md"
    # 100 examples is outside the DoD size range, so the exit code is 1 — but the report is
    # still written, because a failing dataset is exactly when someone needs to read it.
    assert main([str(source), "--out", str(out)]) == 1
    assert "# Dataset distribution" in capsys.readouterr().out
    assert out.read_text(encoding="utf-8").startswith("# Dataset distribution")


@pytest.mark.unit
def test_cli_uses_every_optional_input(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    source = write_dataset(tmp_path / "dataset.jsonl", dataset(100))
    corpus = write_corpus(tmp_path / "corpus.jsonl", [*LEGAL, *SPOKEN])
    tax = write_taxonomy(tmp_path / "taxonomy.yaml", ["institucions/comuns", "cultura/falles"])
    glossary = Path(__file__).resolve().parents[1] / "configs" / "glossari-andorra.yaml"
    assert (
        main(
            [
                str(source),
                "--corpus",
                str(corpus),
                "--taxonomy",
                str(tax),
                "--glossary",
                str(glossary),
            ]
        )
        == 1
    )
    printed = capsys.readouterr().out
    assert "produced nothing" in printed
    assert "never cited" in printed
    assert "Andorran lexicon" in printed


@pytest.mark.unit
def test_cli_exits_zero_on_a_publishable_dataset(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = write_dataset(tmp_path / "dataset.jsonl", dataset(10_000))
    assert main([str(source)]) == 0
    assert "✓ publishable" in capsys.readouterr().out


@pytest.mark.unit
def test_cli_reports_a_missing_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main([str(tmp_path / "absent.jsonl")]) == 1
    assert "no such file" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_reports_an_unapproved_taxonomy_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = write_dataset(tmp_path / "dataset.jsonl", dataset(20))
    broken = tmp_path / "taxonomy.yaml"
    broken.write_text("version: test\nnodes: []\n", encoding="utf-8")
    assert main([str(source), "--taxonomy", str(broken)]) == 1
    assert "error:" in capsys.readouterr().err


@pytest.mark.unit
def test_reading_a_dataset_and_corpus_round_trips(tmp_path: Path) -> None:
    source = write_dataset(tmp_path / "dataset.jsonl", dataset(10))
    corpus = write_corpus(tmp_path / "corpus.jsonl", LEGAL)
    assert len(read_dataset(source)) == 10
    assert set(read_corpus([corpus])) == {doc.id for doc in LEGAL}
