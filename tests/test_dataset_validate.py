"""Tests for the §3.2 dataset validator and its cross-dataset constraints."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID, uuid4

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
from maia.synth.validate import (
    GENERAL_CA_RANGE,
    NO_HO_SE_RANGE,
    DatasetReport,
    check_distribution,
    check_grounding,
    check_licence,
    check_splits,
    main,
    read_corpus_ids,
    read_dataset,
    render,
    split_digest,
    validate_dataset,
    validate_line,
    verify_frozen,
)

PASSAGE = "Les falles són una tradició del solstici d'estiu a diverses parròquies."
RESTRICTED_PASSAGE = "Un article de premsa sobre el pressupost del Comú d'Encamp."
GROUNDING = compute_id(PASSAGE)
RESTRICTED_GROUNDING = compute_id(RESTRICTED_PASSAGE)


def example(
    *,
    example_type: ExampleType = ExampleType.QA,
    split: Split = Split.TRAIN,
    grounding: list[str] | None = None,
    topic: str = "cultura/falles",
    identifier: UUID | None = None,
) -> DatasetExample:
    grounded = example_type.requires_grounding()
    if grounding is None:
        grounding = [GROUNDING] if grounded else []
    messages = [
        {"role": "user", "content": "Què són les falles?"},
        {"role": "assistant", "content": "Una tradició del solstici d'estiu."},
    ]
    if example_type is ExampleType.MULTITURN:
        messages += [
            {"role": "user", "content": "I on se celebren?"},
            {"role": "assistant", "content": "A diverses parròquies del Principat."},
        ]
    return DatasetExample.model_validate(
        {
            "id": str(identifier or uuid4()),
            "messages": messages,
            "type": example_type.value,
            "topic": topic,
            "grounding_ids": grounding,
            "generator": "claude-opus-5",
            "judge_score": 0.9,
            "split": split.value,
        }
    )


def dataset(
    *,
    total: int = 100,
    no_ho_se: int = 8,
    general_ca: int = 17,
) -> list[DatasetExample]:
    """A dataset with a healthy distribution and a 90/5/5 split."""
    examples: list[DatasetExample] = []
    kinds = (
        [ExampleType.NO_HO_SE] * no_ho_se
        + [ExampleType.GENERAL_CA] * general_ca
        + [ExampleType.QA] * (total - no_ho_se - general_ca)
    )
    for index, kind in enumerate(kinds):
        if index < round(total * 0.90):
            split = Split.TRAIN
        elif index < round(total * 0.95):
            split = Split.VAL
        else:
            split = Split.TEST
        examples.append(example(example_type=kind, split=split))
    return examples


def corpus_document(text: str, *, license: License = License.PUBLIC_OFFICIAL) -> CorpusDocument:
    return CorpusDocument(
        text=text,
        source=Source.GOVERN if license.is_public() else Source.PREMSA,
        url="https://www.govern.ad/x",  # type: ignore[arg-type]
        fetched_at=datetime(2026, 8, 1, tzinfo=UTC),
        lang="ca",
        license=license,
        registre=Registre.ESTANDARD,
    )


# ─────────────────────────────────────────────────────────────
# Line validation
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_valid_line_parses() -> None:
    parsed, finding = validate_line(example().model_dump_json(), 1)
    assert finding is None
    assert parsed is not None


@pytest.mark.unit
@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("{not json}", "invalid JSON"),
        ("[1, 2]", "expected a JSON object"),
        ('{"id": "x"}', "id"),
    ],
)
def test_bad_lines_are_reported_not_guessed(raw: str, expected: str) -> None:
    parsed, finding = validate_line(raw, 7)
    assert parsed is None
    assert finding is not None
    assert finding.locator == "7"
    assert expected in finding.reason


# ─────────────────────────────────────────────────────────────
# Distribution
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_healthy_distribution_passes() -> None:
    assert check_distribution(dataset()) == []


@pytest.mark.unit
@pytest.mark.parametrize("count", [3, 15])
def test_no_ho_se_outside_its_band_fails(count: int) -> None:
    """~8 % ± 2 is how the model learns to decline instead of inventing.

    Drift here trains a different model than the one designed, and nothing downstream would
    notice — so it is a hard constraint rather than a note.
    """
    findings = check_distribution(dataset(no_ho_se=count))
    assert any("no_ho_se" in finding.reason for finding in findings)


@pytest.mark.unit
@pytest.mark.parametrize("count", [5, 30])
def test_general_ca_outside_its_band_fails(count: int) -> None:
    findings = check_distribution(dataset(general_ca=count))
    assert any("general_ca" in finding.reason for finding in findings)


@pytest.mark.unit
def test_the_band_edges_are_inclusive() -> None:
    low, high = NO_HO_SE_RANGE
    assert check_distribution(dataset(no_ho_se=round(low * 100))) == []
    assert check_distribution(dataset(no_ho_se=round(high * 100))) == []
    low, high = GENERAL_CA_RANGE
    assert check_distribution(dataset(general_ca=round(low * 100))) == []
    assert check_distribution(dataset(general_ca=round(high * 100))) == []


@pytest.mark.unit
def test_an_empty_dataset_is_a_finding() -> None:
    findings = check_distribution([])
    assert findings and "empty" in findings[0].reason


# ─────────────────────────────────────────────────────────────
# Splits — the leakage check
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_healthy_split_passes() -> None:
    assert check_splits(dataset()) == []


@pytest.mark.unit
def test_the_same_id_in_two_splits_is_leakage() -> None:
    """The failure that makes an evaluation worthless rather than merely wrong.

    It cannot be seen in any single example, so it is checked across the dataset.
    """
    shared = uuid4()
    examples = [
        *dataset(),
        example(split=Split.TRAIN, identifier=shared),
        example(split=Split.TEST, identifier=shared),
    ]
    findings = check_splits(examples)
    assert any("leakage" in finding.reason for finding in findings)
    assert any(finding.locator == str(shared) for finding in findings)


@pytest.mark.unit
def test_a_skewed_split_fails() -> None:
    examples = [example(split=Split.TRAIN) for _ in range(50)]
    examples += [example(split=Split.TEST) for _ in range(50)]
    findings = check_splits(examples)
    assert any("test is 50.0%" in finding.reason for finding in findings)


@pytest.mark.unit
def test_no_examples_means_no_split_findings() -> None:
    assert check_splits([]) == []


# ─────────────────────────────────────────────────────────────
# Grounding resolution
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_grounding_ids_must_exist_in_the_corpus() -> None:
    # An unresolvable citation means the anti-hallucination measure did not apply.
    findings = check_grounding([example()], corpus_ids=set())
    assert findings and "is not in the corpus" in findings[0].reason


@pytest.mark.unit
def test_resolvable_grounding_passes() -> None:
    assert check_grounding([example()], corpus_ids={GROUNDING}) == []


@pytest.mark.unit
def test_ungrounded_types_need_no_corpus() -> None:
    assert check_grounding([example(example_type=ExampleType.GENERAL_CA)], corpus_ids=set()) == []


# ─────────────────────────────────────────────────────────────
# The licence rule
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_rag_style_on_restricted_content_is_a_failure() -> None:
    """The one unambiguous violation: rag_style carries the passage verbatim as its context.

    So grounding it on a no-redistribute document necessarily republishes restricted text — no
    judgement about quoting versus paraphrasing is needed.
    """
    failures, warnings = check_licence(
        [example(example_type=ExampleType.RAG_STYLE, grounding=[RESTRICTED_GROUNDING])],
        {RESTRICTED_GROUNDING},
    )
    assert len(failures) == 1
    assert "republishes restricted text" in failures[0].reason
    assert warnings == []


@pytest.mark.unit
def test_other_types_on_restricted_content_are_warnings() -> None:
    """Paraphrasing restricted knowledge is explicitly allowed, so these cannot be failed.

    Failing them would block the paraphrase the compliance article permits; the honest
    treatment is to surface the review list for M6.01.
    """
    failures, warnings = check_licence(
        [example(example_type=ExampleType.QA, grounding=[RESTRICTED_GROUNDING])],
        {RESTRICTED_GROUNDING},
    )
    assert failures == []
    assert len(warnings) == 1
    assert "review at M6.01" in warnings[0].reason


@pytest.mark.unit
def test_publishable_grounding_raises_nothing() -> None:
    failures, warnings = check_licence([example()], {RESTRICTED_GROUNDING})
    assert failures == []
    assert warnings == []


@pytest.mark.unit
def test_no_restricted_ids_means_no_licence_findings() -> None:
    failures, warnings = check_licence(
        [example(example_type=ExampleType.RAG_STYLE, grounding=[RESTRICTED_GROUNDING])], set()
    )
    assert failures == []
    assert warnings == []


# ─────────────────────────────────────────────────────────────
# Freezing the test split
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_digest_is_order_independent() -> None:
    # Re-serialising the dataset must not change the committed hash.
    examples = dataset()
    assert split_digest(examples) == split_digest(list(reversed(examples)))


@pytest.mark.unit
def test_the_digest_ignores_examples_outside_the_split() -> None:
    examples = dataset()
    extra = [*examples, example(split=Split.TRAIN)]
    assert split_digest(examples) == split_digest(extra)


@pytest.mark.unit
def test_editing_a_test_example_changes_the_digest() -> None:
    examples = dataset()
    before = split_digest(examples)
    test_index = next(i for i, ex in enumerate(examples) if ex.split is Split.TEST)
    examples[test_index] = example(split=Split.TEST, topic="cultura/altre-node")
    assert split_digest(examples) != before


@pytest.mark.unit
def test_verify_frozen_accepts_a_matching_digest() -> None:
    examples = dataset()
    assert verify_frozen(examples, split_digest(examples)) is None


@pytest.mark.unit
def test_verify_frozen_reports_a_changed_split() -> None:
    finding = verify_frozen(dataset(), "0" * 64)
    assert finding is not None
    assert "the test split changed" in finding.reason


@pytest.mark.unit
def test_a_split_can_be_frozen_independently() -> None:
    examples = dataset()
    assert split_digest(examples, Split.VAL) != split_digest(examples, Split.TEST)


# ─────────────────────────────────────────────────────────────
# The whole validator
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_healthy_dataset_reports_ok() -> None:
    report = validate_dataset(dataset(), corpus_ids={GROUNDING}, report=DatasetReport(total=100))
    assert report.ok
    assert report.valid == 100
    assert report.by_split == {"train": 90, "val": 5, "test": 5}
    assert report.share(ExampleType.NO_HO_SE) == pytest.approx(0.08)
    assert report.test_digest


@pytest.mark.unit
def test_the_report_counts_taxonomy_coverage() -> None:
    examples = [example(topic=f"node/{index}") for index in range(4)]
    report = validate_dataset(examples)
    assert len(report.by_topic) == 4
    assert "taxonomy nodes covered: 4" in render(report, Path("x.jsonl"))


@pytest.mark.unit
def test_a_licence_failure_makes_the_report_not_ok() -> None:
    examples = [
        *dataset(),
        example(example_type=ExampleType.RAG_STYLE, grounding=[RESTRICTED_GROUNDING]),
    ]
    report = validate_dataset(
        examples, restricted_ids={RESTRICTED_GROUNDING}, report=DatasetReport(total=len(examples))
    )
    assert not report.ok
    assert report.licence_failures


@pytest.mark.unit
def test_a_licence_warning_alone_does_not_fail() -> None:
    examples = [*dataset(), example(grounding=[RESTRICTED_GROUNDING])]
    report = validate_dataset(
        examples, restricted_ids={RESTRICTED_GROUNDING}, report=DatasetReport(total=len(examples))
    )
    assert report.licence_warnings
    assert not report.licence_failures
    assert "⚠ licence" in render(report, Path("x.jsonl"))


@pytest.mark.unit
def test_render_truncates_long_finding_lists() -> None:
    examples = [example(grounding=[compute_id(f"passatge {i}")]) for i in range(30)]
    report = validate_dataset(examples, corpus_ids=set(), report=DatasetReport(total=30))
    rendered = render(report, Path("x.jsonl"))
    # 30 unresolvable groundings plus the distribution/split findings: only 20 are printed.
    assert len(report.constraint_failures) > 20
    assert "more constraint findings" in rendered


# ─────────────────────────────────────────────────────────────
# Reading files
# ─────────────────────────────────────────────────────────────


def _dataset_file(path: Path, examples: list[DatasetExample]) -> Path:
    path.write_text("".join(f"{e.model_dump_json()}\n" for e in examples), encoding="utf-8")
    return path


def _corpus_file(path: Path, documents: list[CorpusDocument]) -> Path:
    path.write_text("".join(f"{d.model_dump_json()}\n" for d in documents), encoding="utf-8")
    return path


@pytest.mark.unit
def test_read_dataset_skips_blanks_and_reports_bad_lines(tmp_path: Path) -> None:
    path = tmp_path / "dataset.jsonl"
    path.write_text(f"{example().model_dump_json()}\n\n{{bad}}\n", encoding="utf-8")
    report = DatasetReport()
    examples = read_dataset(path, report)
    assert len(examples) == 1
    assert report.total == 2
    assert len(report.invalid) == 1


@pytest.mark.unit
def test_read_corpus_ids_separates_restricted_documents(tmp_path: Path) -> None:
    path = tmp_path / "corpus.jsonl"
    documents = [
        corpus_document(PASSAGE),
        corpus_document(RESTRICTED_PASSAGE, license=License.NO_REDISTRIBUTE),
    ]
    # Blank lines between records must be skipped, not parsed.
    path.write_text(
        "\n".join(d.model_dump_json() for d in documents).replace("\n", "\n\n") + "\n",
        encoding="utf-8",
    )
    all_ids, restricted = read_corpus_ids([path])
    assert all_ids == {GROUNDING, RESTRICTED_GROUNDING}
    assert restricted == {RESTRICTED_GROUNDING}


# ─────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_cli_passes_a_healthy_dataset(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = _dataset_file(tmp_path / "dataset.jsonl", dataset())
    assert main([str(path)]) == 0
    out = capsys.readouterr().out
    assert "valid: 100" in out
    assert "test split digest:" in out


@pytest.mark.unit
def test_cli_fails_a_skewed_distribution(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = _dataset_file(tmp_path / "dataset.jsonl", dataset(no_ho_se=30))
    assert main([str(path)]) == 1
    assert "no_ho_se" in capsys.readouterr().out


@pytest.mark.unit
def test_cli_skip_distribution_is_for_the_pilot(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    # M2.06's 500-example pilot is too small for the proportions to mean anything.
    path = _dataset_file(tmp_path / "pilot.jsonl", [example() for _ in range(10)])
    assert main([str(path)]) == 1
    assert main([str(path), "--skip-distribution"]) == 0


@pytest.mark.unit
def test_cli_checks_grounding_and_licence_against_a_corpus(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    corpus = _corpus_file(
        tmp_path / "corpus.jsonl",
        [
            corpus_document(PASSAGE),
            corpus_document(RESTRICTED_PASSAGE, license=License.NO_REDISTRIBUTE),
        ],
    )
    offender = example(example_type=ExampleType.RAG_STYLE, grounding=[RESTRICTED_GROUNDING])
    path = _dataset_file(tmp_path / "dataset.jsonl", [*dataset(), offender])
    assert main([str(path), "--corpus", str(corpus)]) == 1
    assert "republishes restricted text" in capsys.readouterr().out


@pytest.mark.unit
def test_cli_verifies_the_frozen_test_digest(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    examples = dataset()
    path = _dataset_file(tmp_path / "dataset.jsonl", examples)
    digest = split_digest(examples)
    assert main([str(path), "--frozen-test-digest", digest]) == 0
    assert main([str(path), "--frozen-test-digest", "0" * 64]) == 1
    assert "the test split changed" in capsys.readouterr().out


@pytest.mark.unit
def test_cli_fails_on_invalid_lines(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "dataset.jsonl"
    path.write_text("{bad}\n", encoding="utf-8")
    assert main([str(path)]) == 1
    assert "invalid JSON" in capsys.readouterr().out


@pytest.mark.unit
def test_cli_reports_a_missing_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main([str(tmp_path / "absent.jsonl")]) == 1
    assert "no such file" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_reports_a_missing_corpus(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = _dataset_file(tmp_path / "dataset.jsonl", dataset())
    assert main([str(path), "--corpus", str(tmp_path / "absent.jsonl")]) == 1
    assert "no such file" in capsys.readouterr().err


@pytest.mark.unit
def test_the_report_json_shape_is_stable() -> None:
    # The report feeds M2.09's distribution report, so its counters are part of the interface.
    report = validate_dataset(dataset(), report=DatasetReport(total=100))
    payload = json.loads(
        json.dumps({"by_type": dict(report.by_type), "digest": report.test_digest})
    )
    assert payload["by_type"]["no_ho_se"] == 8
    assert len(payload["digest"]) == 64
