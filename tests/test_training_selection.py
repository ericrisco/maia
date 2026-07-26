"""Tests for epoch checkpoint selection (PLAN M3.04)."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path

import pytest

from maia.synth.semdedup import Vector
from maia.training.selection import (
    MAX_VARIETY_DROP,
    MIN_SAMPLE,
    OPENING_WORDS,
    Candidate,
    Selection,
    Variety,
    dissimilarity,
    evaluate,
    length_spread,
    openings,
    render,
    select,
    variety,
)


@dataclass
class WordEmbedder:
    """Bag-of-words vectors — identical answers land at cosine 1, distinct ones far apart."""

    dimensions: int = 512
    vocabulary: dict[str, int] = field(default_factory=dict)

    def embed(self, texts: Sequence[str]) -> list[Vector]:
        vectors: list[Vector] = []
        for text in texts:
            vector = [0.0] * self.dimensions
            for word in text.lower().split():
                slot = self.vocabulary.setdefault(word, len(self.vocabulary) % self.dimensions)
                vector[slot] += 1.0
            vectors.append(vector)
        return vectors


VARIED = [
    "El Consell General es compon de vint-i-vuit consellers generals elegits cada quatre anys.",
    "Set parròquies formen el Principat, cadascuna amb el seu comú propi.",
    "La Batllia resol en primera instància; el Tribunal de Corts jutja les causes penals greus.",
    "Meritxell acull el santuari de la patrona, reconstruït després de l'incendi de 1972.",
    "El copríncep episcopal és el bisbe d'Urgell i comparteix la prefectura amb el francès.",
    "Els esquellots eren una cridòria festiva davant la casa d'uns nuvis viudos.",
    "La Valira travessa el país de nord a sud i desemboca al Segre.",
    "El Comapedrosa, amb 2.942 metres, és el cim més alt del territori andorrà.",
    "Andorra la Vella és la capital i seu del Govern des del segle passat.",
    "Els Pareatges de 1278 van fixar la sobirania compartida que encara perdura avui.",
    "El síndic general presideix el Consell i el representa davant les institucions.",
    "La Massana i Ordino conserven bordes de pedra restaurades com a habitatge.",
]

CLONIC = [
    f"El Consell General és una institució andorrana molt important del país número {index}."
    for index in range(12)
]


def measured(answers: Sequence[str]) -> Variety:
    return variety(list(answers), WordEmbedder())


def candidate(epoch: int, accuracy: float, answers: Sequence[str] = tuple(VARIED)) -> Candidate:
    return Candidate(
        epoch=epoch,
        checkpoint=Path(f"build/train/exp/checkpoint-epoch-{epoch}"),
        accuracy=accuracy,
        variety=measured(answers),
    )


@dataclass
class FakeAnswerer:
    by_checkpoint: dict[str, list[str]] = field(default_factory=dict)
    default: list[str] = field(default_factory=lambda: list(VARIED))
    seen: list[Path] = field(default_factory=list)

    def answer(self, checkpoint: Path, questions: Sequence[str]) -> list[str]:
        self.seen.append(checkpoint)
        answers = self.by_checkpoint.get(checkpoint.name, self.default)
        return list(answers[: len(questions)])


@dataclass
class FakeScorer:
    scores: list[float] = field(default_factory=lambda: [0.6, 0.7, 0.8])
    calls: int = 0

    def score(self, answers: Sequence[str], references: Sequence[str]) -> float:
        self.calls += 1
        return self.scores[min(self.calls - 1, len(self.scores) - 1)]


# ─────────────────────────────────────────────────────────────
# Measuring variety — what accuracy cannot see
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_varied_answers_start_differently() -> None:
    assert openings(VARIED) == 1.0


@pytest.mark.unit
def test_clonic_answers_share_an_opening() -> None:
    """A model collapsed into a house style opens the same way every time."""
    assert openings(CLONIC) == pytest.approx(1 / len(CLONIC))
    assert OPENING_WORDS == 4


@pytest.mark.unit
def test_openings_are_case_folded() -> None:
    assert openings(["El consell general és", "el CONSELL General és"]) == 0.5


@pytest.mark.unit
def test_openings_of_nothing_is_zero() -> None:
    assert openings([]) == 0.0
    assert openings(["", "   "]) == 0.0


@pytest.mark.unit
def test_uniform_lengths_score_zero_spread() -> None:
    """A collapsed model answers everything at the same length."""
    assert length_spread(["x" * 100] * 5) == 0.0
    assert length_spread(VARIED) > 0.0


@pytest.mark.unit
def test_length_spread_uses_a_coefficient_not_a_deviation() -> None:
    """So a uniformly *long* model is not mistaken for a varied one."""
    short = ["a" * 10, "b" * 20]
    long = ["a" * 1_000, "b" * 2_000]
    assert length_spread(short) == pytest.approx(length_spread(long))


@pytest.mark.unit
def test_length_spread_needs_two_answers() -> None:
    assert length_spread(["only one"]) == 0.0
    assert length_spread([]) == 0.0


@pytest.mark.unit
def test_identical_answers_are_maximally_similar() -> None:
    """The direct measurement of "clonic"."""
    assert dissimilarity(["exactament el mateix text"] * 5, WordEmbedder()) == pytest.approx(0.0)


@pytest.mark.unit
def test_distinct_answers_are_dissimilar() -> None:
    assert dissimilarity(VARIED, WordEmbedder()) > 0.5


@pytest.mark.unit
def test_dissimilarity_needs_two_answers() -> None:
    assert dissimilarity(["one"], WordEmbedder()) == 0.0
    assert dissimilarity([], WordEmbedder()) == 0.0


@pytest.mark.unit
def test_an_embedder_returning_the_wrong_count_is_refused() -> None:
    @dataclass
    class Truncating:
        def embed(self, texts: Sequence[str]) -> list[Vector]:
            return [[1.0]] * (len(texts) - 1)

    with pytest.raises(ValueError, match="may not be theirs"):
        dissimilarity(["a", "b"], Truncating())


@pytest.mark.unit
def test_variety_is_higher_for_varied_answers_on_every_axis() -> None:
    varied, clonic = measured(VARIED), measured(CLONIC)
    assert varied.distinct_openings > clonic.distinct_openings
    assert varied.dissimilarity > clonic.dissimilarity
    assert varied.score > clonic.score


@pytest.mark.unit
def test_variety_needs_a_sample_to_mean_anything() -> None:
    assert not measured(VARIED[:3]).measurable
    assert measured(VARIED).measurable
    assert MIN_SAMPLE == 10


@pytest.mark.unit
def test_blank_answers_do_not_count_towards_the_sample() -> None:
    assert measured([*VARIED[:5], "", "   ", "\n"]).sample == 5


# ─────────────────────────────────────────────────────────────
# Selection — the best is not always the last
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_highest_scoring_checkpoint_wins_when_variety_holds() -> None:
    selection = select([candidate(1, 0.60), candidate(2, 0.70), candidate(3, 0.80)])
    assert selection.chosen is not None
    assert selection.chosen.epoch == 3
    assert not selection.differs_from_last
    assert selection.rejected_for_variety == []


@pytest.mark.unit
def test_a_collapsed_final_epoch_is_rejected_despite_scoring_highest() -> None:
    """The case the plan calls out: the best is not always the last."""
    selection = select(
        [
            candidate(1, 0.70, VARIED),
            candidate(2, 0.75, VARIED),
            candidate(3, 0.82, CLONIC),  # highest accuracy, collapsed style
        ]
    )
    assert selection.chosen is not None
    assert selection.chosen.epoch == 2
    assert selection.differs_from_last
    assert [item.epoch for item in selection.rejected_for_variety] == [3]


@pytest.mark.unit
def test_the_report_names_the_trade_off_rather_than_hiding_it() -> None:
    selection = select(
        [candidate(1, 0.70, VARIED), candidate(2, 0.75, VARIED), candidate(3, 0.82, CLONIC)]
    )
    rendered = render(selection)
    assert "clonic-answer collapse" in rendered
    assert "not the last one" in rendered
    assert "accuracy alone would have chosen epoch 3" in rendered
    assert "PO's and Tech Lead's call" in rendered


@pytest.mark.unit
def test_a_tie_goes_to_the_earlier_epoch() -> None:
    """Less training for the same result is less overfitting."""
    selection = select([candidate(1, 0.80), candidate(2, 0.80), candidate(3, 0.80)])
    assert selection.chosen is not None
    assert selection.chosen.epoch == 1


@pytest.mark.unit
def test_variety_is_not_used_when_it_cannot_be_measured() -> None:
    """A rule applied on evidence nobody has is worse than no rule."""
    tiny = VARIED[:4]
    selection = select([candidate(1, 0.70, tiny), candidate(2, 0.90, tiny)])
    assert selection.chosen is not None
    assert selection.chosen.epoch == 2
    assert "variety not measured" in selection.reasons[0]
    assert "accuracy alone" in selection.reasons[0]


@pytest.mark.unit
def test_the_variety_threshold_is_configurable() -> None:
    candidates = [candidate(1, 0.70, VARIED), candidate(2, 0.82, CLONIC)]
    strict = select(candidates, max_variety_drop=0.01)
    lenient = select(candidates, max_variety_drop=0.99)
    assert strict.chosen is not None and strict.chosen.epoch == 1
    assert lenient.chosen is not None and lenient.chosen.epoch == 2
    assert MAX_VARIETY_DROP == 0.15


@pytest.mark.unit
def test_no_candidates_chooses_nothing() -> None:
    selection = select([])
    assert selection.chosen is None
    assert selection.best_by_accuracy is None
    assert selection.last is None
    assert not selection.differs_from_last
    assert "no candidates" in render(selection)


@pytest.mark.unit
def test_the_naive_baselines_are_reported_for_comparison() -> None:
    selection = select(
        [candidate(1, 0.70, VARIED), candidate(2, 0.75, VARIED), candidate(3, 0.82, CLONIC)]
    )
    assert selection.best_by_accuracy is not None
    assert selection.best_by_accuracy.epoch == 3
    assert selection.last is not None
    assert selection.last.epoch == 3


@pytest.mark.unit
def test_the_report_tabulates_every_epoch_and_marks_the_choice() -> None:
    rendered = render(select([candidate(1, 0.70), candidate(2, 0.80)]))
    assert "| epoch | accuracy | variety | openings | lengths | distinct |" in rendered
    assert rendered.count("| 1 ") + rendered.count("| 1←") >= 1
    assert "←" in rendered


@pytest.mark.unit
def test_a_selection_without_a_choice_renders_its_reasons() -> None:
    assert "no checkpoint chosen" in render(Selection(chosen=None, reasons=["nothing to do"]))


# ─────────────────────────────────────────────────────────────
# Evaluating the checkpoints
# ─────────────────────────────────────────────────────────────


QUESTIONS = [f"Pregunta {index}?" for index in range(12)]
REFERENCES = [f"Referència {index}." for index in range(12)]


@pytest.mark.unit
def test_every_checkpoint_is_answered_scored_and_measured() -> None:
    answerer, scorer = FakeAnswerer(), FakeScorer()
    checkpoints = [Path(f"checkpoint-epoch-{n}") for n in (1, 2, 3)]
    candidates = evaluate(checkpoints, QUESTIONS, REFERENCES, answerer, scorer, WordEmbedder())
    assert [item.epoch for item in candidates] == [1, 2, 3]
    assert [item.accuracy for item in candidates] == [0.6, 0.7, 0.8]
    assert answerer.seen == checkpoints
    assert all(item.variety.measurable for item in candidates)


@pytest.mark.unit
def test_a_collapsed_checkpoint_is_measured_as_such_end_to_end() -> None:
    answerer = FakeAnswerer(by_checkpoint={"checkpoint-epoch-3": list(CLONIC)})
    checkpoints = [Path(f"checkpoint-epoch-{n}") for n in (1, 2, 3)]
    candidates = evaluate(
        checkpoints, QUESTIONS, REFERENCES, answerer, FakeScorer(), WordEmbedder()
    )
    selection = select(candidates)
    assert selection.chosen is not None
    assert selection.chosen.epoch == 2
    assert selection.differs_from_last


@pytest.mark.unit
def test_no_checkpoints_is_refused() -> None:
    with pytest.raises(ValueError, match="no checkpoints"):
        evaluate([], QUESTIONS, REFERENCES, FakeAnswerer(), FakeScorer(), WordEmbedder())


@pytest.mark.unit
def test_mismatched_questions_and_references_are_refused() -> None:
    """A mismatched pairing produces a score that means nothing and looks like a result."""
    with pytest.raises(ValueError, match="means nothing and looks like a result"):
        evaluate(
            [Path("checkpoint-epoch-1")],
            QUESTIONS,
            REFERENCES[:5],
            FakeAnswerer(),
            FakeScorer(),
            WordEmbedder(),
        )


@pytest.mark.unit
def test_a_checkpoint_answering_the_wrong_number_of_questions_is_refused() -> None:
    answerer = FakeAnswerer(default=list(VARIED[:3]))
    with pytest.raises(ValueError, match="answer\\(s\\) for"):
        evaluate(
            [Path("checkpoint-epoch-1")],
            QUESTIONS,
            REFERENCES,
            answerer,
            FakeScorer(),
            WordEmbedder(),
        )
