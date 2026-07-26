"""Tests for the AndBench contribution and harness adapter (PLAN M4.01-M4.02)."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from uuid import UUID, uuid5

import pytest

from maia.evaluation.andbench import (
    CONTRIBUTED_TRACK,
    PO_QUESTIONS,
    ContaminationError,
    Item,
    RestrictedContributionError,
    Track,
    TrackResult,
    UnknownTrackError,
    contamination,
    contribution,
    groups_are_separated,
    parse_results,
    read_manual,
    render,
    render_contribution,
    run,
    to_item,
    write_contribution,
)
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

_NAMESPACE = UUID("6ba7b81a-9dad-11d1-80b4-00c04fd430c8")


def passage(index: int) -> str:
    return compute_id(f"Passatge {index} del corpus andorrà.")


def document(index: int, licence: License = License.PUBLIC_OFFICIAL) -> CorpusDocument:
    text = f"Passatge {index} del corpus andorrà."
    return CorpusDocument.model_validate(
        {
            "id": compute_id(text),
            "text": text,
            "source": Source.JURIDIC.value,
            "url": f"https://www.portaljuridicandorra.ad/{index}",
            "fetched_at": "2026-07-26T10:00:00+00:00",
            "license": licence.value,
            "registre": Registre.ESTANDARD.value,
            "lang": "ca",
        }
    )


def corpus(*, restricted_indices: set[int] | None = None) -> dict[str, CorpusDocument]:
    """Every passage the fixtures use, public unless named as restricted."""
    blocked = restricted_indices or set()
    documents = [
        document(index, License.NO_REDISTRIBUTE if index in blocked else License.PUBLIC_OFFICIAL)
        for index in [*range(5), *range(100, 103)]
    ]
    return {item.id: item for item in documents}


def example(
    tag: str,
    *,
    split: Split = Split.TEST,
    grounding: int = 0,
    turns: int = 2,
    kind: ExampleType = ExampleType.QA,
) -> DatasetExample:
    messages = [
        {"role": "user", "content": f"Quants consellers hi ha? ({tag})"},
        {"role": "assistant", "content": "Vint-i-vuit consellers generals."},
    ]
    if turns > 2:
        messages += [
            {"role": "user", "content": "I qui els presideix?"},
            {"role": "assistant", "content": "El síndic general."},
        ]
    return DatasetExample.model_validate(
        {
            "id": str(uuid5(_NAMESPACE, tag)),
            "messages": messages,
            "type": kind.value,
            "topic": "institucions/consell-general",
            "grounding_ids": [passage(grounding)],
            "generator": "claude-opus-5",
            "judge_score": 0.9,
            "split": split.value,
        }
    )


def clean_dataset() -> list[DatasetExample]:
    """Train and test grounded in *different* passages, as M2.08 guarantees."""
    return [
        *[example(f"tr{index}", split=Split.TRAIN, grounding=index) for index in range(5)],
        *[example(f"te{index}", split=Split.TEST, grounding=100 + index) for index in range(3)],
    ]


@dataclass
class FakeHarness:
    payload: Mapping[str, Mapping[str, float]] = field(
        default_factory=lambda: {
            "and_coneix": {"score": 0.71, "items": 120},
            "and_llengua": {"score": 0.64, "items": 80},
            "and_cotidia": {"score": 0.58, "items": 60},
            "and_obert": {"score": 0.83, "items": 100, "judge_agreement": 0.9},
        }
    )
    calls: list[tuple[str, tuple[str, ...], str | None]] = field(default_factory=list)

    def evaluate(
        self, model: str, tracks: Sequence[str], *, revision: str | None = None
    ) -> Mapping[str, Mapping[str, float]]:
        self.calls.append((model, tuple(tracks), revision))
        return {name: values for name, values in self.payload.items() if name in set(tracks)}


# ─────────────────────────────────────────────────────────────
# The boundary: MAIA keeps no harness of its own
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_four_tracks_are_andbenchs() -> None:
    assert {track.value for track in Track} == {
        "and_coneix",
        "and_llengua",
        "and_cotidia",
        "and_obert",
    }


@pytest.mark.unit
def test_only_and_obert_is_generative() -> None:
    assert Track.OBERT.generative
    assert not any(track.generative for track in Track if track is not Track.OBERT)
    assert CONTRIBUTED_TRACK is Track.OBERT


@pytest.mark.unit
def test_the_report_says_where_the_scores_come_from() -> None:
    """Because the temptation is to reimplement scoring, and then two projects disagree."""
    rendered = render(parse_results({"and_coneix": {"score": 0.7, "items": 10}}))
    assert "MAIA keeps no harness of its own" in rendered


# ─────────────────────────────────────────────────────────────
# Anti-contamination — what makes the contribution sound
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_split_grounded_in_different_passages_is_clean() -> None:
    assert contamination(clean_dataset()) == []
    assert groups_are_separated(clean_dataset())


@pytest.mark.unit
def test_a_shared_grounding_passage_is_contamination() -> None:
    """Being un-trained is necessary and not sufficient: the passage is what MAIA learned."""
    shared = [
        example("tr", split=Split.TRAIN, grounding=7),
        example("te", split=Split.TEST, grounding=7),
    ]
    assert contamination(shared) == [passage(7)]
    assert not groups_are_separated(shared)


@pytest.mark.unit
def test_contributing_contaminated_items_is_refused() -> None:
    shared = [
        example("tr", split=Split.TRAIN, grounding=7),
        example("te", split=Split.TEST, grounding=7),
    ]
    with pytest.raises(ContaminationError, match="scored on passages it learned from"):
        contribution(shared, corpus=corpus())


@pytest.mark.unit
def test_the_refusal_names_the_fix_as_a_re_split() -> None:
    """Trimming the contribution would hide an unsound split rather than fixing it."""
    shared = [
        example("tr", split=Split.TRAIN, grounding=7),
        example("te", split=Split.TEST, grounding=7),
    ]
    with pytest.raises(ContaminationError, match="Re-split by grounding group"):
        contribution(shared, corpus=corpus())


@pytest.mark.unit
def test_a_clean_dataset_contributes_its_test_split() -> None:
    items = contribution(clean_dataset(), corpus=corpus())
    assert len(items) == 3
    assert all(item.source == "maia" for item in items)


@pytest.mark.unit
def test_the_contributed_split_is_configurable() -> None:
    dataset = [
        example("tr", split=Split.TRAIN, grounding=1),
        example("va", split=Split.VAL, grounding=2),
    ]
    assert len(contribution(dataset, contributed=Split.VAL, corpus=corpus())) == 1


# ─────────────────────────────────────────────────────────────
# Items
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_an_example_becomes_a_question_and_a_reference() -> None:
    item = to_item(example("a"))
    assert item.question.startswith("Quants consellers")
    assert item.reference == "Vint-i-vuit consellers generals."
    assert item.grounding_ids == (passage(0),)


@pytest.mark.unit
def test_a_multiturn_example_cannot_be_contributed() -> None:
    """And-Obert scores one answer against one reference; flattening would invent the reference."""
    with pytest.raises(ValueError, match="would invent the reference"):
        to_item(example("m", turns=4, kind=ExampleType.MULTITURN))


@pytest.mark.unit
def test_an_item_serialises_for_the_andbench_repo() -> None:
    payload = json.loads(to_item(example("a")).to_json())
    assert set(payload) == {"id", "question", "reference", "topic", "grounding_ids", "source"}


@pytest.mark.unit
def test_manual_questions_are_carried_through() -> None:
    manual = [
        Item(
            id="po-1",
            question="Què és un quart?",
            reference="Una divisió territorial.",
            topic="manual",
            grounding_ids=(),
            source="po-manual",
        )
    ]
    items = contribution(clean_dataset(), manual=manual, corpus=corpus())
    assert len(items) == 4
    assert items[-1].source == "po-manual"


@pytest.mark.unit
def test_the_contribution_round_trips_through_jsonl(tmp_path: Path) -> None:
    items = contribution(clean_dataset(), corpus=corpus())
    path = write_contribution(items, tmp_path / "andbench" / "maia.jsonl")
    restored = read_manual(path)
    assert [item.question for item in restored] == [item.question for item in items]


@pytest.mark.unit
def test_a_malformed_manual_question_names_its_line(tmp_path: Path) -> None:
    """A silently dropped question shrinks the benchmark MAIA is measured on."""
    path = tmp_path / "manual.jsonl"
    path.write_text('{"id": "1", "question": "Q?"}\n', encoding="utf-8")
    with pytest.raises(ValueError, match=r"manual\.jsonl:1: not a question item"):
        read_manual(path)


@pytest.mark.unit
def test_blank_lines_in_the_manual_file_are_skipped(tmp_path: Path) -> None:
    path = tmp_path / "manual.jsonl"
    path.write_text('{"id": "1", "question": "Q?", "reference": "A."}\n\n   \n', encoding="utf-8")
    assert len(read_manual(path)) == 1


@pytest.mark.unit
def test_the_summary_counts_both_sources_and_flags_a_short_manual_set() -> None:
    rendered = render_contribution(contribution(clean_dataset(), corpus=corpus()))
    assert "3 from the frozen test split, 0 hand-written" in rendered
    assert f"asks for {PO_QUESTIONS} manual PO questions" in rendered
    assert "checked, not assumed" in rendered


# ─────────────────────────────────────────────────────────────
# The harness adapter
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_running_the_harness_normalises_every_track() -> None:
    harness = FakeHarness()
    results = run(harness, "ericrisco/maia-12b", revision="cand1")
    assert [result.track for result in results] == sorted(Track, key=lambda t: t.value)
    assert harness.calls[0][0] == "ericrisco/maia-12b"
    assert harness.calls[0][2] == "cand1"


@pytest.mark.unit
def test_a_subset_of_tracks_can_be_run() -> None:
    results = run(FakeHarness(), "model", tracks=[Track.OBERT])
    assert [result.track for result in results] == [Track.OBERT]
    assert results[0].detail["judge_agreement"] == 0.9


@pytest.mark.unit
def test_running_no_tracks_is_refused() -> None:
    with pytest.raises(ValueError, match="no tracks to run"):
        run(FakeHarness(), "model", tracks=[])


@pytest.mark.unit
def test_an_unknown_track_raises_rather_than_scoring_zero() -> None:
    """Reporting zero for a typo would look like a failing track, which is a different problem."""
    with pytest.raises(UnknownTrackError, match="is not an AndBench track"):
        parse_results({"and_coneixement": {"score": 0.5, "items": 10}})


@pytest.mark.unit
@pytest.mark.parametrize("values", [{"score": 0.5}, {"items": 10}, {}])
def test_a_result_without_a_score_and_a_count_is_refused(values: dict[str, float]) -> None:
    with pytest.raises(ValueError, match="cannot be compared with anything"):
        parse_results({"and_coneix": values})


@pytest.mark.unit
@pytest.mark.parametrize("score", [-0.1, 1.5])
def test_a_score_outside_the_unit_range_is_refused(score: float) -> None:
    with pytest.raises(ValueError, match=r"outside 0\.0-1\.0"):
        TrackResult(track=Track.OBERT, score=score, items=10)


@pytest.mark.unit
@pytest.mark.parametrize("items", [0, -5])
def test_a_score_over_nothing_is_refused(items: int) -> None:
    with pytest.raises(ValueError, match="is not a score"):
        TrackResult(track=Track.OBERT, score=0.5, items=items)


@pytest.mark.unit
def test_the_report_marks_which_track_is_llm_judged() -> None:
    rendered = render(run(FakeHarness(), "model"), label="cand1")
    assert "AndBench — cand1" in rendered
    assert "| `and_obert` | 0.830 | 100 | LLM-judge |" in rendered
    assert "| `and_coneix` | 0.710 | 120 | MCQ |" in rendered


@pytest.mark.unit
def test_a_full_manual_set_is_not_flagged() -> None:
    manual = [
        Item(
            id=f"po-{index}",
            question=f"Pregunta {index}?",
            reference="Resposta.",
            topic="manual",
            grounding_ids=(),
            source="po-manual",
        )
        for index in range(PO_QUESTIONS)
    ]
    rendered = render_contribution(contribution(clean_dataset(), manual=manual, corpus=corpus()))
    assert f"{PO_QUESTIONS} hand-written" in rendered
    assert "⚠" not in rendered


# ─────────────────────────────────────────────────────────────
# The licence rule — AndBench is a public artifact
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_contributing_without_the_corpus_is_refused() -> None:
    """A §3.2 example carries no licence of its own; only its grounding does (D-0024)."""
    with pytest.raises(RestrictedContributionError, match="needs the corpus"):
        contribution(clean_dataset())


@pytest.mark.unit
def test_an_item_grounded_in_restricted_text_cannot_be_contributed() -> None:
    """Contributing it publishes a derivative of text the project may not redistribute — the same
    rule M2.11 applies to the dataset, applied to the benchmark."""
    with pytest.raises(RestrictedContributionError, match="may not be redistributed"):
        contribution(clean_dataset(), corpus=corpus(restricted_indices={100}))


@pytest.mark.unit
def test_the_refusal_points_at_pool_bench_rather_than_at_trimming() -> None:
    with pytest.raises(RestrictedContributionError, match="Exclude those passages from pool_bench"):
        contribution(clean_dataset(), corpus=corpus(restricted_indices={101}))


@pytest.mark.unit
def test_restricted_text_in_the_train_split_does_not_block_the_contribution() -> None:
    """Only what is being published matters; training on restricted text is allowed (D-0011)."""
    items = contribution(clean_dataset(), corpus=corpus(restricted_indices={0, 1}))
    assert len(items) == 3
