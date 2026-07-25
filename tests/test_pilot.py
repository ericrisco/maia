"""Tests for the 500-example pilot gate (PLAN M2.06)."""

from __future__ import annotations

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
    compute_id,
)
from maia.synth.pilot import (
    CANDIDATE_THRESHOLDS,
    MIN_ANDORRAN_RATE,
    MIN_CATALAN_RATE,
    MIN_FACTUAL_RATE,
    MIN_SUPPORT,
    IncompleteReviewError,
    Label,
    Rate,
    ReviewedExample,
    calibrate,
    conversation_of,
    draw_pilot,
    from_csv,
    main,
    render,
    score,
    to_csv,
    to_markdown,
)

PASSAGE = "El Consell General es compon de 28 consellers generals."
GROUNDING = compute_id(PASSAGE)
_NAMESPACE = UUID("6ba7b814-9dad-11d1-80b4-00c04fd430c8")


def document(text: str = PASSAGE) -> CorpusDocument:
    return CorpusDocument.model_validate(
        {
            "id": compute_id(text),
            "text": text,
            "source": Source.JURIDIC.value,
            "url": "https://www.portaljuridicandorra.ad/llei/exemple",
            "fetched_at": "2026-07-25T10:00:00+00:00",
            "license": License.PUBLIC_OFFICIAL.value,
            "registre": Registre.ESTANDARD.value,
            "lang": "ca",
        }
    )


CORPUS = {document().id: document()}


def example(
    tag: str = "a",
    *,
    kind: ExampleType = ExampleType.QA,
    score_value: float = 0.9,
    grounded: bool | None = None,
) -> DatasetExample:
    """A §3.2 example with a stable id, so a seeded draw is reproducible across runs."""
    cites = kind.requires_grounding() if grounded is None else grounded
    return DatasetExample.model_validate(
        {
            "id": str(uuid5(_NAMESPACE, f"{kind.value}|{tag}")),
            "messages": [
                {"role": "user", "content": f"Pregunta {tag}?"},
                {"role": "assistant", "content": f"Resposta {tag}."},
            ],
            "type": kind.value,
            "topic": "institucions/consell-general" if cites else "general_ca/instrucat",
            "grounding_ids": [GROUNDING] if cites else [],
            "generator": "claude-opus-5",
            "judge_score": score_value,
            "split": "train",
        }
    )


def reviewed(
    tag: str = "a",
    *,
    kind: ExampleType = ExampleType.QA,
    score_value: float = 0.9,
    factual: Label = Label.YES,
    catalan: Label = Label.YES,
    andorran: Label = Label.YES,
) -> ReviewedExample:
    return ReviewedExample(
        example=example(tag, kind=kind, score_value=score_value),
        passages=(PASSAGE,),
        factual=factual,
        catalan=catalan,
        andorran=andorran,
    )


# ─────────────────────────────────────────────────────────────
# Drawing the pilot
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_whole_dataset_is_taken_when_it_is_smaller_than_the_pilot() -> None:
    examples = [example(str(index)) for index in range(5)]
    assert len(draw_pilot(examples, CORPUS, size=500, seed=1)) == 5


@pytest.mark.unit
def test_the_draw_is_stratified_so_no_type_escapes_the_gate() -> None:
    """A uniform draw over a mostly-qa dataset says nothing about whether no_ho_se declines."""
    examples = [example(f"qa{index}") for index in range(200)]
    examples += [example(f"nhs{index}", kind=ExampleType.NO_HO_SE) for index in range(5)]
    examples += [example("trad", kind=ExampleType.TRADUCCIO)]
    drawn = draw_pilot(examples, CORPUS, size=20, seed=1)
    kinds = {item.example.type for item in drawn}
    assert ExampleType.NO_HO_SE in kinds
    assert ExampleType.TRADUCCIO in kinds
    assert len(drawn) == 20


@pytest.mark.unit
def test_the_draw_is_reproducible_from_the_seed() -> None:
    """A gate whose sample cannot be reproduced is not evidence."""
    examples = [example(str(index)) for index in range(100)]
    first = [item.example.id for item in draw_pilot(examples, CORPUS, size=10, seed=7)]
    again = [item.example.id for item in draw_pilot(examples, CORPUS, size=10, seed=7)]
    other = [item.example.id for item in draw_pilot(examples, CORPUS, size=10, seed=8)]
    assert first == again
    assert first != other


@pytest.mark.unit
def test_the_draw_does_not_depend_on_input_order() -> None:
    examples = [example(str(index)) for index in range(60)]
    forwards = {item.example.id for item in draw_pilot(examples, CORPUS, size=10, seed=3)}
    backwards = {
        item.example.id for item in draw_pilot(list(reversed(examples)), CORPUS, size=10, seed=3)
    }
    assert forwards == backwards


@pytest.mark.unit
def test_each_row_carries_its_grounding_passage() -> None:
    """ "Is this factually correct?" is unanswerable without the passage."""
    drawn = draw_pilot([example()], CORPUS, seed=1)
    assert drawn[0].passages == (PASSAGE,)


@pytest.mark.unit
def test_a_missing_passage_is_marked_not_silently_omitted() -> None:
    """A reviewer must never mark something factual against no evidence."""
    drawn = draw_pilot([example()], {}, seed=1)
    assert "MISSING FROM CORPUS" in drawn[0].passages[0]


@pytest.mark.unit
def test_without_a_corpus_no_passages_are_invented() -> None:
    assert draw_pilot([example()], None, seed=1)[0].passages == ()


@pytest.mark.unit
def test_general_ca_is_not_asked_to_sound_andorran() -> None:
    """Scoring it against that bar would penalise it for doing its job."""
    drawn = draw_pilot([example(kind=ExampleType.GENERAL_CA)], CORPUS, seed=1)
    assert drawn[0].andorran is Label.NA
    assert drawn[0].factual is Label.PENDING


@pytest.mark.unit
def test_rows_are_grouped_by_type_for_the_reviewer() -> None:
    examples = [
        example("z", kind=ExampleType.RESUM),
        example("a", kind=ExampleType.QA),
        example("b", kind=ExampleType.QA),
    ]
    drawn = draw_pilot(examples, CORPUS, seed=1)
    assert [item.example.type.value for item in drawn] == ["qa", "qa", "resum"]


# ─────────────────────────────────────────────────────────────
# The review sheet
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_sheet_round_trips_including_the_conversation_newlines() -> None:
    sample = draw_pilot([example("a"), example("b")], CORPUS, seed=1)
    restored = from_csv(to_csv(sample, seed=1))
    assert [item.example.id for item in restored] == [item.example.id for item in sample]
    assert [item.example.type for item in restored] == [item.example.type for item in sample]
    assert [item.example.judge_score for item in restored] == [0.9, 0.9]
    assert restored[0].passages == (PASSAGE,)


@pytest.mark.unit
def test_the_sheet_records_the_seed_and_the_bars() -> None:
    written = to_csv(draw_pilot([example()], CORPUS, seed=42), seed=42)
    assert "seed 42" in written
    assert "95%" in written and "98%" in written


@pytest.mark.unit
def test_pending_is_the_default_so_nothing_is_pre_answered() -> None:
    written = to_csv(draw_pilot([example()], CORPUS, seed=1), seed=1)
    assert from_csv(written)[0].factual is Label.PENDING


@pytest.mark.unit
def test_multiple_passages_survive_the_round_trip() -> None:
    two = document("Un altre passatge del corpus.")
    corpus = {**CORPUS, two.id: two}
    grounded = DatasetExample.model_validate(
        {
            "id": str(uuid5(_NAMESPACE, "two")),
            "messages": [
                {"role": "user", "content": "Pregunta?"},
                {"role": "assistant", "content": "Resposta."},
            ],
            "type": ExampleType.QA.value,
            "topic": "institucions/consell-general",
            "grounding_ids": sorted({GROUNDING, two.id}),
            "generator": "claude-opus-5",
            "judge_score": 0.9,
            "split": "train",
        }
    )
    sample = draw_pilot([grounded], corpus, seed=1)
    assert len(from_csv(to_csv(sample, seed=1))[0].passages) == 2


@pytest.mark.unit
def test_an_empty_sheet_reads_as_nothing() -> None:
    assert from_csv("") == []


@pytest.mark.unit
def test_a_sheet_missing_a_column_is_refused() -> None:
    with pytest.raises(ValueError, match="missing column"):
        from_csv("id,type\nx,qa\n")


@pytest.mark.unit
@pytest.mark.parametrize("bad", ["si", "y", "TRUE", "maybe"])
def test_an_unrecognised_label_is_refused(bad: str) -> None:
    """A typo must not quietly become a yes."""
    sheet = to_csv(draw_pilot([example()], CORPUS, seed=1), seed=1)
    with pytest.raises(ValueError, match="unrecognised label"):
        from_csv(sheet.replace(",pending,pending,", f",{bad},pending,"))


@pytest.mark.unit
def test_labels_are_read_case_insensitively_and_trimmed() -> None:
    sheet = to_csv(draw_pilot([example()], CORPUS, seed=1), seed=1)
    assert from_csv(sheet.replace(",pending,pending,pending,", ",  YES ,no,na,"))[0].factual is (
        Label.YES
    )


@pytest.mark.unit
def test_a_row_that_is_not_a_readable_example_is_refused() -> None:
    sheet = to_csv(draw_pilot([example()], CORPUS, seed=1), seed=1)
    with pytest.raises(ValueError, match="not a readable review row"):
        from_csv(sheet.replace(",qa,", ",not-a-type,"))


@pytest.mark.unit
def test_the_markdown_companion_shows_the_passages_and_the_bars() -> None:
    written = to_markdown(draw_pilot([example()], CORPUS, seed=1), seed=1)
    assert PASSAGE in written
    assert "Grounding passages" in written
    assert "95%" in written
    assert "| type | sampled |" in written


@pytest.mark.unit
def test_the_companion_warns_when_a_grounded_example_has_no_passages() -> None:
    written = to_markdown(draw_pilot([example()], None, seed=1), seed=1)
    assert "factual review is not possible" in written


@pytest.mark.unit
def test_the_companion_says_when_a_type_cites_nothing_by_construction() -> None:
    written = to_markdown(
        draw_pilot([example(kind=ExampleType.GENERAL_CA)], CORPUS, seed=1), seed=1
    )
    assert "cites no passages by construction" in written
    assert "exempt - not judged" in written


@pytest.mark.unit
def test_the_conversation_is_rendered_with_roles() -> None:
    assert "USER: Pregunta a?" in conversation_of(example())
    assert "ASSISTANT: Resposta a." in conversation_of(example())


# ─────────────────────────────────────────────────────────────
# Scoring the gate
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_clean_pilot_passes_on_every_axis() -> None:
    result = score([reviewed(str(index)) for index in range(50)])
    assert result.passed
    assert result.factual.rate == 1.0
    assert "✓ PASS" in render(result)


@pytest.mark.unit
def test_a_half_finished_review_can_never_read_as_a_pass() -> None:
    """The one way this gate could quietly fail."""
    with pytest.raises(IncompleteReviewError, match="still pending"):
        score([reviewed("a"), reviewed("b", factual=Label.PENDING)])


@pytest.mark.unit
def test_an_empty_pilot_is_refused() -> None:
    with pytest.raises(ValueError, match="the pilot is empty"):
        score([])


@pytest.mark.unit
def test_the_factual_bar_is_dod_f2s() -> None:
    """94 % is a fail, 96 % is a pass, at DoD-F2's ≥95 %."""
    fail = [reviewed(str(i), factual=Label.NO if i < 6 else Label.YES) for i in range(100)]
    ok = [reviewed(str(i), factual=Label.NO if i < 4 else Label.YES) for i in range(100)]
    assert not score(fail).factual.passed
    assert score(ok).factual.passed
    assert MIN_FACTUAL_RATE == 0.95


@pytest.mark.unit
def test_the_catalan_bar_is_stricter_than_the_factual_one() -> None:
    borderline = [reviewed(str(i), catalan=Label.NO if i < 3 else Label.YES) for i in range(100)]
    result = score(borderline)
    assert result.factual.passed
    assert not result.catalan.passed
    assert MIN_CATALAN_RATE == 0.98
    assert not result.passed


@pytest.mark.unit
def test_the_andorran_question_has_its_own_bar() -> None:
    poor = [reviewed(str(i), andorran=Label.NO if i < 60 else Label.YES) for i in range(100)]
    result = score(poor)
    assert result.factual.passed and result.catalan.passed
    assert not result.andorran.passed
    assert not result.passed
    assert MIN_ANDORRAN_RATE == 0.50


@pytest.mark.unit
def test_the_three_axes_are_independent() -> None:
    """A factually wrong answer and a badly written one are different problems."""
    result = score(
        [
            reviewed("a", factual=Label.NO, catalan=Label.YES, andorran=Label.YES),
            reviewed("b", factual=Label.YES, catalan=Label.NO, andorran=Label.YES),
        ]
    )
    assert result.factual.yes == 1
    assert result.catalan.yes == 1
    assert result.andorran.yes == 2


@pytest.mark.unit
def test_not_applicable_answers_are_excluded_from_the_denominator() -> None:
    result = score([reviewed("a"), reviewed("b", andorran=Label.NA)])
    assert result.andorran.asked == 1
    assert result.andorran.not_applicable == 1
    assert result.andorran.rate == 1.0
    assert "1 n/a" in render(result)


@pytest.mark.unit
def test_a_question_nobody_was_asked_does_not_pass_by_default() -> None:
    assert not Rate(yes=0, no=0, not_applicable=5, bar=0.95).passed
    assert Rate(yes=0, no=0, not_applicable=5, bar=0.95).rate == 0.0


@pytest.mark.unit
def test_failures_are_broken_down_by_type() -> None:
    result = score(
        [
            reviewed("a", kind=ExampleType.TRADUCCIO, factual=Label.NO),
            *[reviewed(str(index)) for index in range(10)],
        ]
    )
    assert result.by_type["traduccio"] == (0, 1)
    assert "traduccio: 1/1 not factual" in render(result)


@pytest.mark.unit
def test_notes_on_failed_examples_are_surfaced() -> None:
    flagged = ReviewedExample(
        example=example("bad"),
        factual=Label.NO,
        catalan=Label.YES,
        andorran=Label.YES,
        note="inventa una data",
    )
    result = score([flagged, *[reviewed(str(index)) for index in range(10)]])
    assert result.notes[0][1] == "inventa una data"
    assert "inventa una data" in render(result)


@pytest.mark.unit
def test_the_summary_says_the_po_ok_is_still_required() -> None:
    """M2.06 is a PO-blocking gate; the numbers only say whether they stand in its way."""
    assert "PO OK is still required" in render(score([reviewed()]))


# ─────────────────────────────────────────────────────────────
# Calibrating the threshold — the point of the pilot
# ─────────────────────────────────────────────────────────────


def curve_sample() -> list[ReviewedExample]:
    """40 examples where the judge separates cleanly: 0.80+ is factual, below 0.20 is not.

    The calibrated threshold is therefore **0.20**, not 0.80 — the lowest point that admits every
    correct example and no incorrect one. A calibration that returned 0.80 would satisfy the bar
    while discarding nothing it needed to, which is the mistake this function exists to catch.
    """
    good = [
        reviewed(f"g{index}", score_value=0.80 + index / 200, factual=Label.YES)
        for index in range(25)
    ]
    bad = [
        reviewed(f"b{index}", score_value=0.10 + index / 200, factual=Label.NO)
        for index in range(15)
    ]
    return good + bad


@pytest.mark.unit
def test_the_lowest_threshold_clearing_the_bar_is_chosen() -> None:
    """Lowest, because any higher threshold discards good examples for no gain in quality."""
    calibration = calibrate(curve_sample())
    assert calibration.achievable
    assert calibration.threshold == 0.20
    assert calibration.factual_rate == 1.0
    assert calibration.support == 25
    # Every higher threshold also clears the bar but keeps fewer examples.
    assert all(rate == 1.0 for point, rate, _ in calibration.curve if point >= 0.20)


@pytest.mark.unit
def test_the_calibration_reports_how_much_it_retains() -> None:
    calibration = calibrate(curve_sample())
    assert calibration.retained == pytest.approx(25 / 40)
    assert "retaining 62.5%" in calibration.summary


@pytest.mark.unit
def test_a_threshold_resting_on_too_few_examples_is_not_evidence() -> None:
    """A rate of 100 % on four examples is arithmetic, not evidence."""
    tiny = [reviewed(f"g{index}", score_value=0.95, factual=Label.YES) for index in range(4)]
    tiny += [reviewed(f"b{index}", score_value=0.10, factual=Label.NO) for index in range(4)]
    assert not calibrate(tiny).achievable
    assert calibrate(tiny, min_support=3).achievable
    assert MIN_SUPPORT == 20


@pytest.mark.unit
def test_a_judge_that_cannot_gate_the_dataset_says_so() -> None:
    """Returning the best of a bad set would look like a calibration and be a fiction."""
    noisy = [
        reviewed(f"x{index}", score_value=0.9, factual=Label.YES if index % 2 else Label.NO)
        for index in range(40)
    ]
    calibration = calibrate(noisy)
    assert not calibration.achievable
    assert calibration.threshold is None
    assert "cannot gate this dataset" in calibration.summary
    assert "keep human review in the loop" in calibration.summary


@pytest.mark.unit
def test_exempt_examples_are_excluded_from_the_curve() -> None:
    """They carry judge_score 0.0 by construction, so including them would flatter every
    threshold with a wall of unjudged zeros."""
    sample = curve_sample()
    sample += [
        reviewed(f"gc{index}", kind=ExampleType.GENERAL_CA, score_value=0.0, factual=Label.YES)
        for index in range(30)
    ]
    calibration = calibrate(sample)
    assert calibration.judged == 40
    assert calibration.excluded_exempt == 30
    assert calibration.threshold == 0.20


@pytest.mark.unit
def test_unanswered_examples_take_no_part_in_the_calibration() -> None:
    sample = [*curve_sample(), reviewed("na", factual=Label.NA)]
    assert calibrate(sample).judged == 40


@pytest.mark.unit
def test_the_agreement_rate_shows_whether_the_judge_is_worth_anything() -> None:
    perfect = calibrate(curve_sample())
    assert perfect.agreement == 1.0

    inverted = [reviewed(f"g{i}", score_value=0.95, factual=Label.NO) for i in range(20)]
    inverted += [reviewed(f"b{i}", score_value=0.10, factual=Label.YES) for i in range(20)]
    assert calibrate(inverted).agreement == 0.0


@pytest.mark.unit
def test_the_curve_is_reported_for_every_usable_threshold() -> None:
    calibration = calibrate(curve_sample())
    assert calibration.curve
    thresholds = [point[0] for point in calibration.curve]
    assert thresholds == sorted(thresholds)
    assert all(0.0 <= point[1] <= 1.0 for point in calibration.curve)
    # Support falls as the threshold rises.
    supports = [point[2] for point in calibration.curve]
    assert supports == sorted(supports, reverse=True)


@pytest.mark.unit
def test_a_threshold_above_every_score_contributes_no_curve_point() -> None:
    sample = [reviewed(f"g{index}", score_value=0.5, factual=Label.YES) for index in range(25)]
    calibration = calibrate(sample)
    assert max(point[0] for point in calibration.curve) == 0.5
    assert calibration.threshold == 0.0


@pytest.mark.unit
def test_calibrating_nothing_is_not_achievable() -> None:
    calibration = calibrate([])
    assert not calibration.achievable
    assert calibration.agreement == 0.0
    assert calibration.judged == 0
    assert calibration.curve == ()


@pytest.mark.unit
def test_the_candidate_thresholds_span_the_whole_range() -> None:
    assert CANDIDATE_THRESHOLDS[0] == 0.0
    assert CANDIDATE_THRESHOLDS[-1] == 1.0
    assert len(CANDIDATE_THRESHOLDS) == 21


@pytest.mark.unit
def test_the_summary_carries_the_calibration_and_the_agreement() -> None:
    rendered = render(score(curve_sample()))
    assert "threshold: threshold 0.20" in rendered
    assert "judge/human agreement at 0.70: 100.0%" in rendered


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
def test_cli_draw_writes_both_artifacts(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    dataset = write_dataset(tmp_path / "dataset.jsonl", [example(str(i)) for i in range(30)])
    corpus = write_corpus(tmp_path / "corpus.jsonl")
    out = tmp_path / "review" / "pilot.csv"
    assert (
        main(["draw", str(dataset), "--corpus", str(corpus), "--out", str(out), "--size", "10"])
        == 0
    )
    assert len(from_csv(out.read_text(encoding="utf-8"))) == 10
    assert PASSAGE in out.with_suffix(".md").read_text(encoding="utf-8")
    assert "wrote 10 example(s)" in capsys.readouterr().out


@pytest.mark.unit
def test_cli_draw_warns_when_no_corpus_is_given(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Without passages the factual column cannot honestly be filled."""
    dataset = write_dataset(tmp_path / "dataset.jsonl", [example()])
    assert main(["draw", str(dataset), "--out", str(tmp_path / "pilot.csv")]) == 0
    assert "factual column cannot honestly be filled" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_draw_flags_missing_passages(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    dataset = write_dataset(tmp_path / "dataset.jsonl", [example()])
    empty = tmp_path / "corpus.jsonl"
    empty.write_text("", encoding="utf-8")
    assert (
        main(["draw", str(dataset), "--corpus", str(empty), "--out", str(tmp_path / "p.csv")]) == 0
    )
    assert "missing from the corpus" in capsys.readouterr().out


@pytest.mark.unit
def test_cli_draw_reports_a_missing_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["draw", str(tmp_path / "absent.jsonl")]) == 1
    assert "no such file" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_score_passes_a_clean_sheet(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    sheet = tmp_path / "pilot.csv"
    sheet.write_text(to_csv([reviewed(str(i)) for i in range(30)], seed=1), encoding="utf-8")
    assert main(["score", str(sheet)]) == 0
    printed = capsys.readouterr().out
    assert "✓ PASS" in printed
    assert "threshold" in printed


@pytest.mark.unit
def test_cli_score_reports_the_calibration_curve_on_a_mixed_sheet(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """37.5 % of this pilot is factually wrong, so the gate fails — and the calibration still says
    where the threshold belongs, which is the actionable half of the answer."""
    sheet = tmp_path / "pilot.csv"
    sheet.write_text(to_csv(curve_sample(), seed=1), encoding="utf-8")
    assert main(["score", str(sheet)]) == 1
    printed = capsys.readouterr().out
    assert "✗ FAIL" in printed
    assert "threshold 0.20" in printed


@pytest.mark.unit
def test_cli_score_fails_a_sheet_below_the_bars(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    sheet = tmp_path / "pilot.csv"
    sheet.write_text(
        to_csv([reviewed(str(i), factual=Label.NO) for i in range(30)], seed=1), encoding="utf-8"
    )
    assert main(["score", str(sheet)]) == 1
    assert "✗ FAIL" in capsys.readouterr().out


@pytest.mark.unit
def test_cli_score_refuses_a_half_finished_sheet(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    sheet = tmp_path / "pilot.csv"
    sheet.write_text(to_csv(draw_pilot([example()], CORPUS, seed=1), seed=1), encoding="utf-8")
    assert main(["score", str(sheet)]) == 1
    assert "still pending review" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_score_reports_a_missing_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["score", str(tmp_path / "absent.csv")]) == 1
    assert "no such file" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_score_reports_a_bad_label(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    sheet = tmp_path / "pilot.csv"
    sheet.write_text(
        to_csv(draw_pilot([example()], CORPUS, seed=1), seed=1).replace(
            ",pending,pending,pending,", ",si,yes,yes,"
        ),
        encoding="utf-8",
    )
    assert main(["score", str(sheet)]) == 1
    assert "unrecognised label" in capsys.readouterr().err
