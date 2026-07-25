"""Tests for 90/5/5 split assignment and the test-split freeze (PLAN M2.08)."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from uuid import UUID, uuid5

import pytest

from maia.schemas import DatasetExample, ExampleType, Split, compute_id
from maia.synth.splits import (
    MAX_DRIFT,
    TARGETS,
    FrozenSplitError,
    SplitReport,
    assign_splits,
    freeze,
    grounding_groups,
    group_key,
    main,
    read_dataset,
    read_freeze,
    render,
)
from maia.synth.validate import check_splits, split_digest, verify_frozen

_NAMESPACE = UUID("6ba7b815-9dad-11d1-80b4-00c04fd430c8")


def passage(index: int) -> str:
    return compute_id(f"Passatge {index} del corpus andorrà.")


def example(
    tag: str,
    *,
    kind: ExampleType = ExampleType.QA,
    grounding: list[int] | None = None,
) -> DatasetExample:
    cites = kind.requires_grounding()
    ids = [passage(index) for index in (grounding if grounding is not None else [0])]
    return DatasetExample.model_validate(
        {
            "id": str(uuid5(_NAMESPACE, tag)),
            "messages": [
                {"role": "user", "content": f"Pregunta {tag}?"},
                {"role": "assistant", "content": f"Resposta {tag}."},
            ],
            "type": kind.value,
            "topic": "institucions/consell-general" if cites else "general_ca/instrucat",
            "grounding_ids": sorted(set(ids)) if cites else [],
            "generator": "claude-opus-5",
            "judge_score": 0.9 if cites else 0.0,
            "split": "train",
        }
    )


def dataset(size: int = 200, *, passages: int = 50) -> list[DatasetExample]:
    """A dataset where every ``size // passages`` examples share one passage."""
    return [example(f"e{index}", grounding=[index % passages]) for index in range(size)]


# ─────────────────────────────────────────────────────────────
# Grouping — the guarantee no content check can provide
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_examples_sharing_a_passage_form_one_group() -> None:
    """Two questions about one paragraph are two views of the same information."""
    examples = [
        example("a", grounding=[1]),
        example("b", grounding=[1]),
        example("c", grounding=[2]),
    ]
    groups = grounding_groups(examples)
    assert [len(group) for group in groups] == [2, 1]
    assert group_key(examples[0]) in groups[0]
    assert group_key(examples[1]) in groups[0]


@pytest.mark.unit
def test_grouping_is_transitive_through_shared_passages() -> None:
    """A cites 1, B cites 1 and 2, C cites 2 — all three travel together."""
    examples = [
        example("a", grounding=[1]),
        example("b", grounding=[1, 2]),
        example("c", grounding=[2]),
    ]
    assert [len(group) for group in grounding_groups(examples)] == [3]


@pytest.mark.unit
def test_ungrounded_examples_are_singletons() -> None:
    """They cite nothing, so they can leak nothing."""
    examples = [
        example("a", kind=ExampleType.GENERAL_CA),
        example("b", kind=ExampleType.GENERAL_CA),
    ]
    assert [len(group) for group in grounding_groups(examples)] == [1, 1]


@pytest.mark.unit
def test_grouping_is_stable_in_input_order() -> None:
    examples = dataset(40, passages=10)
    assert grounding_groups(examples) == grounding_groups(examples)


@pytest.mark.unit
def test_grouping_nothing_yields_nothing() -> None:
    assert grounding_groups([]) == []


# ─────────────────────────────────────────────────────────────
# Assignment
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_every_example_gets_exactly_one_split() -> None:
    assigned, report = assign_splits(dataset(200), seed=1)
    assert len(assigned) == 200
    assert sum(report.counts.values()) == 200
    assert {example.split for example in assigned} == set(TARGETS)


@pytest.mark.unit
def test_the_proportions_land_inside_the_validator_tolerance() -> None:
    _, report = assign_splits(dataset(400, passages=100), seed=1)
    assert report.within_tolerance
    for split, target in TARGETS.items():
        assert abs(report.share(split) - target) <= MAX_DRIFT, split


@pytest.mark.unit
def test_no_group_is_split_across_splits() -> None:
    """The property the whole module exists for."""
    assigned, _ = assign_splits(dataset(300, passages=60), seed=3)
    by_id = {group_key(example): example.split for example in assigned}
    for group in grounding_groups(assigned):
        assert len({by_id[key] for key in group}) == 1, group


@pytest.mark.unit
def test_no_passage_appears_in_two_splits() -> None:
    """Stated the other way round: a passage grounds examples in exactly one split."""
    assigned, _ = assign_splits(dataset(300, passages=60), seed=5)
    owner: dict[str, Split] = {}
    for item in assigned:
        for ident in item.grounding_ids:
            assert owner.setdefault(ident, item.split) is item.split


@pytest.mark.unit
def test_the_assignment_is_reproducible_from_the_seed() -> None:
    first, _ = assign_splits(dataset(200), seed=7)
    again, _ = assign_splits(dataset(200), seed=7)
    other, _ = assign_splits(dataset(200), seed=8)
    assert [item.split for item in first] == [item.split for item in again]
    assert [item.split for item in first] != [item.split for item in other]


@pytest.mark.unit
def test_the_result_passes_the_m2_05_split_check() -> None:
    """The two modules must agree, since they share the targets and the tolerance."""
    assigned, _ = assign_splits(dataset(1_000, passages=250), seed=1)
    assert check_splits(assigned) == []


@pytest.mark.unit
def test_a_single_giant_group_makes_90_5_5_unreachable_and_says_so() -> None:
    """Every example citing one passage collapses into one group, which cannot be divided.

    This is a real risk at scale: if the generator reuses overlapping passages across nodes, the
    transitive closure can swallow the dataset. The report must fail rather than silently return
    a dataset with an empty test split.
    """
    _, report = assign_splits([example(f"e{index}", grounding=[0]) for index in range(100)], seed=1)
    assert report.largest_group == 100
    assert not report.within_tolerance
    rendered = render(report)
    assert "grounding groups are indivisible" in rendered
    assert "✗" in rendered


@pytest.mark.unit
def test_large_groups_are_placed_before_small_ones() -> None:
    """A big group placed last can only overshoot, and the drift is what has to stay small."""
    examples = [example(f"big{index}", grounding=[0]) for index in range(20)]
    examples += [example(f"small{index}", grounding=[index + 1]) for index in range(180)]
    _, report = assign_splits(examples, seed=1)
    assert report.within_tolerance


@pytest.mark.unit
def test_an_empty_dataset_assigns_nothing() -> None:
    assigned, report = assign_splits([], seed=1)
    assert assigned == []
    assert report.total == 0
    assert report.share(Split.TEST) == 0.0
    assert report.largest_group == 0


@pytest.mark.unit
def test_the_report_breaks_down_each_split_by_type() -> None:
    examples = dataset(180, passages=60)
    examples += [example(f"gc{index}", kind=ExampleType.GENERAL_CA) for index in range(20)]
    _, report = assign_splits(examples, seed=1)
    assert report.by_type[Split.TRAIN][ExampleType.QA.value] > 0
    assert sum(report.by_type[Split.TRAIN].values()) == report.counts[Split.TRAIN]


@pytest.mark.unit
def test_a_type_missing_from_the_test_split_is_flagged() -> None:
    """A type present in train but absent from test is unmeasured, which is worth knowing."""
    report = SplitReport(
        total=100,
        counts={Split.TRAIN: 90, Split.VAL: 5, Split.TEST: 5},
        by_type={
            Split.TRAIN: Counter({"qa": 80, "traduccio": 10}),
            Split.VAL: Counter({"qa": 5}),
            Split.TEST: Counter({"qa": 5}),
        },
    )
    rendered = render(report)
    assert "contains no traduccio example(s)" in rendered
    assert rendered.count("contains no traduccio") == 2  # val and test


# ─────────────────────────────────────────────────────────────
# The freeze
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_freeze_records_the_digest_the_ids_and_the_count() -> None:
    assigned, _ = assign_splits(dataset(200), seed=1)
    payload = json.loads(freeze(assigned, version="1"))
    assert payload["split"] == "test"
    assert payload["digest"] == split_digest(assigned, Split.TEST)
    assert payload["count"] == len(payload["ids"]) > 0
    assert payload["ids"] == sorted(payload["ids"])


@pytest.mark.unit
def test_the_freeze_round_trips(tmp_path: Path) -> None:
    assigned, _ = assign_splits(dataset(200), seed=1)
    path = tmp_path / "freeze.json"
    path.write_text(freeze(assigned, version="1"), encoding="utf-8")
    digest, ids = read_freeze(path)
    assert digest == split_digest(assigned, Split.TEST)
    assert len(ids) == sum(1 for item in assigned if item.split is Split.TEST)


@pytest.mark.unit
def test_a_frozen_test_split_is_honoured_not_reshuffled() -> None:
    """Once committed, re-splitting must leave every frozen example in test."""
    first, _ = assign_splits(dataset(300, passages=75), seed=1)
    frozen = [group_key(item) for item in first if item.split is Split.TEST]
    assert frozen

    second, report = assign_splits(dataset(300, passages=75), seed=99, frozen_test_ids=frozen)
    still_test = {group_key(item) for item in second if item.split is Split.TEST}
    assert set(frozen) <= still_test
    assert report.frozen_kept == len(frozen)
    assert "frozen test example(s) kept in place" in render(report)


@pytest.mark.unit
def test_a_frozen_example_never_lands_in_train() -> None:
    first, _ = assign_splits(dataset(300, passages=75), seed=1)
    frozen = [group_key(item) for item in first if item.split is Split.TEST]
    second, _ = assign_splits(dataset(300, passages=75), seed=42, frozen_test_ids=frozen)
    trained = {group_key(item) for item in second if item.split is Split.TRAIN}
    assert not trained.intersection(frozen)


@pytest.mark.unit
def test_the_rest_of_a_frozen_examples_group_goes_to_test_too() -> None:
    """Its group shares grounding with it, so putting those in train is the leak."""
    examples = [example("a", grounding=[1]), example("b", grounding=[1])]
    examples += [example(f"other{index}", grounding=[index + 2]) for index in range(40)]
    assigned, _ = assign_splits(examples, seed=1, frozen_test_ids=[group_key(examples[0])])
    by_id = {group_key(item): item.split for item in assigned}
    assert by_id[group_key(examples[0])] is Split.TEST
    assert by_id[group_key(examples[1])] is Split.TEST


@pytest.mark.unit
def test_the_frozen_digest_still_verifies_after_a_resplit() -> None:
    """The end-to-end guarantee: freeze, re-split with a different seed, digest unchanged."""
    first, _ = assign_splits(dataset(400, passages=100), seed=1)
    digest = split_digest(first, Split.TEST)
    frozen = [group_key(item) for item in first if item.split is Split.TEST]

    second, _ = assign_splits(dataset(400, passages=100), seed=1234, frozen_test_ids=frozen)
    assert verify_frozen(second, digest) is None


@pytest.mark.unit
def test_a_freeze_naming_an_absent_example_is_an_error() -> None:
    """A freeze that names an example the dataset no longer has means the test set was edited."""
    with pytest.raises(FrozenSplitError, match="not in this dataset"):
        assign_splits(dataset(50), seed=1, frozen_test_ids=["missing-id"])


@pytest.mark.unit
@pytest.mark.parametrize(
    ("payload", "message"),
    [
        ({"ids": ["a"]}, "not a test-split freeze"),
        ({"digest": "x"}, "not a test-split freeze"),
        ("nope", "not a test-split freeze"),
        ({"digest": "x", "ids": "a"}, "must be a list of strings"),
        ({"digest": "x", "ids": [1]}, "must be a list of strings"),
        ({"digest": "x", "ids": ["a"], "count": 5}, "edited by hand"),
    ],
)
def test_an_unreadable_freeze_is_refused(tmp_path: Path, payload: object, message: str) -> None:
    """A run that cannot read the freeze must not proceed as though nothing were frozen."""
    path = tmp_path / "freeze.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match=message):
        read_freeze(path)


# ─────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────


def write(path: Path, examples: list[DatasetExample]) -> Path:
    path.write_text("".join(f"{e.model_dump_json()}\n" for e in examples), encoding="utf-8")
    return path


@pytest.mark.unit
def test_cli_assigns_and_writes(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    source = write(tmp_path / "dataset.jsonl", dataset(400, passages=100))
    out = tmp_path / "split" / "dataset.jsonl"
    assert main([str(source), "--out", str(out)]) == 0
    assigned = read_dataset(out)
    assert {item.split for item in assigned} == set(TARGETS)
    assert "✓ splits over 400 example(s)" in capsys.readouterr().out


@pytest.mark.unit
def test_cli_writes_a_freeze_only_when_asked(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Freezing is a deliberate act, not a side effect of splitting."""
    source = write(tmp_path / "dataset.jsonl", dataset(400, passages=100))
    assert main([str(source)]) == 0
    assert "commit it" not in capsys.readouterr().out

    freeze_path = tmp_path / "configs" / "test-split.freeze.json"
    assert main([str(source), "--write-freeze", str(freeze_path)]) == 0
    assert "commit it" in capsys.readouterr().out
    digest, ids = read_freeze(freeze_path)
    assert len(digest) == 64
    assert ids


@pytest.mark.unit
def test_cli_honours_an_existing_freeze(tmp_path: Path) -> None:
    source = write(tmp_path / "dataset.jsonl", dataset(400, passages=100))
    freeze_path = tmp_path / "freeze.json"
    assert main([str(source), "--write-freeze", str(freeze_path), "--seed", "1"]) == 0
    digest, _ = read_freeze(freeze_path)

    out = tmp_path / "resplit.jsonl"
    assert (
        main([str(source), "--freeze", str(freeze_path), "--seed", "777", "--out", str(out)]) == 0
    )
    assert verify_frozen(read_dataset(out), digest) is None


@pytest.mark.unit
def test_cli_fails_when_the_split_cannot_hit_the_targets(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = write(
        tmp_path / "dataset.jsonl", [example(f"e{index}", grounding=[0]) for index in range(100)]
    )
    assert main([str(source)]) == 1
    assert "grounding groups are indivisible" in capsys.readouterr().out


@pytest.mark.unit
def test_cli_reports_a_missing_dataset(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main([str(tmp_path / "absent.jsonl")]) == 1
    assert "no such file" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_reports_a_missing_freeze(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    source = write(tmp_path / "dataset.jsonl", dataset(50))
    assert main([str(source), "--freeze", str(tmp_path / "absent.json")]) == 1
    assert "no such file" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_reports_a_freeze_that_no_longer_matches(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The test split was edited — that must stop the run, not be re-split around."""
    source = write(tmp_path / "dataset.jsonl", dataset(400, passages=100))
    freeze_path = tmp_path / "freeze.json"
    main([str(source), "--write-freeze", str(freeze_path)])
    payload = json.loads(freeze_path.read_text(encoding="utf-8"))
    payload["ids"].append(str(uuid5(_NAMESPACE, "not-in-the-dataset")))
    payload["count"] = len(payload["ids"])
    freeze_path.write_text(json.dumps(payload), encoding="utf-8")

    assert main([str(source), "--freeze", str(freeze_path)]) == 1
    assert "the test split was edited" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_reports_a_corrupt_freeze(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    source = write(tmp_path / "dataset.jsonl", dataset(50))
    freeze_path = tmp_path / "freeze.json"
    freeze_path.write_text('{"nope": true}', encoding="utf-8")
    assert main([str(source), "--freeze", str(freeze_path)]) == 1
    assert "not a test-split freeze" in capsys.readouterr().err
