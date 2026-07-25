"""Tests for the anti-forgetting mix (PLAN M2.04)."""

from __future__ import annotations

import json
from pathlib import Path
from random import Random
from uuid import uuid4

import pytest

from maia.schemas import DatasetExample, ExampleType, Split, compute_id
from maia.synth.general_ca import (
    CORE_ANDORRAN_TERMS,
    DEFAULT_TARGET_SHARE,
    GENERAL_CA_RANGE,
    Instruction,
    MixReport,
    _pattern,
    andorra_matcher,
    fingerprints_of,
    main,
    mentions_andorra,
    mix,
    plan_general_ca,
    read_jsonl_source,
    render,
    select,
    to_example,
)
from maia.synth.glossary import Glossary

GROUNDING = compute_id("Un passatge del corpus.")

# Realistic general-Catalan instructions with nothing Andorran in them.
GENERAL = [
    Instruction(
        "Explica què és la fotosíntesi.",
        "És el procés amb què les plantes transformen la llum del sol en energia química, "
        "amb l'ajuda de l'aigua i el diòxid de carboni que prenen de l'entorn.",
        "instrucat",
    ),
    Instruction(
        "Com es fa una truita de patates?",
        "Es pelen i es tallen les patates ben fines, es fregeixen a poc a poc amb oli i "
        "després es barregen amb els ous batuts abans de quallar-ho tot a la paella.",
        "instrucat",
    ),
    Instruction(
        "Qui va escriure La plaça del Diamant?",
        "La va escriure Mercè Rodoreda, i és una de les novel·les més llegides de la "
        "literatura catalana del segle XX.",
        "instrucat",
    ),
    Instruction(
        "Quina diferència hi ha entre un virus i un bacteri?",
        "Els bacteris són organismes vius d'una sola cèl·lula que es poden reproduir sols, "
        "mentre que els virus necessiten infectar una cèl·lula per multiplicar-se.",
        "instrucat",
    ),
]


def example(*, split: Split = Split.TRAIN, nonce: int = 0) -> DatasetExample:
    return DatasetExample.model_validate(
        {
            "id": str(uuid4()),
            "messages": [
                {"role": "user", "content": f"Què són les falles? ({nonce})"},
                {"role": "assistant", "content": f"Una tradició del solstici. ({nonce})"},
            ],
            "type": "qa",
            "topic": "cultura/falles-solstici",
            "grounding_ids": [GROUNDING],
            "generator": "claude-opus-5",
            "judge_score": 0.9,
            "split": split.value,
        }
    )


def generated(count: int) -> list[DatasetExample]:
    return [example(nonce=index) for index in range(count)]


def many_general(count: int) -> list[Instruction]:
    return [
        Instruction(
            f"{base.prompt} (variant {index})",
            f"{base.response} Aquesta és la variació número {index} de la resposta.",
            "instrucat",
        )
        for index in range(count)
        for base in [GENERAL[index % len(GENERAL)]]
    ]


# ─────────────────────────────────────────────────────────────
# The Andorra-relatedness filter — the point of the whole module
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
@pytest.mark.parametrize(
    "text",
    [
        "Quantes parròquies té Andorra?",
        "El Consell General aprova els pressupostos.",
        "Vaig pujar al Comapedrosa l'estiu passat.",
        "El santuari de Meritxell és molt visitat.",
        "La Valira travessa toda la vall.",
        "Els andorrans voten cada quatre anys.",
    ],
)
def test_andorra_related_instructions_are_detected(text: str) -> None:
    """These are exactly what must NOT enter the anti-forgetting mix.

    The mix exists to preserve what the base model knew *outside* Andorra; Andorran content in
    it shrinks the real mix below what the report claims, and smuggles unvetted Andorran facts
    into the weights outside the grounded pipeline.
    """
    assert mentions_andorra(text, andorra_matcher())


@pytest.mark.unit
def test_general_catalan_is_not_flagged() -> None:
    matcher = andorra_matcher()
    for instruction in GENERAL:
        assert not mentions_andorra(instruction.text, matcher), instruction.prompt


@pytest.mark.unit
def test_the_glossary_extends_the_matcher() -> None:
    """The same source of truth, used in reverse.

    If a term is Andorran enough for M2.03 to *require*, it is Andorran enough to exclude here.
    """
    plain = andorra_matcher()
    assert not mentions_andorra("Vaig veure els esquellots al poble.", plain)

    glossary = Glossary.model_validate(
        {
            "version": "t",
            "entries": [
                {
                    "term": "esquellots",
                    "category": "cultural",
                    "gloss": "Costum de fer soroll amb esquelles.",
                }
            ],
        }
    )
    assert mentions_andorra("Vaig veure els esquellots al poble.", andorra_matcher(glossary))


@pytest.mark.unit
def test_matching_is_accent_and_case_insensitive() -> None:
    matcher = andorra_matcher()
    for text in (
        "ANDORRA LA VELLA",
        "andorra la vella",
        "Sant Julià de Lòria",
        "sant julia de loria",
    ):
        assert mentions_andorra(text, matcher), text


@pytest.mark.unit
def test_a_term_inside_a_longer_word_is_not_a_match() -> None:
    # Word boundaries: "principat" must not fire on "principatment" and friends.
    assert not mentions_andorra("El principatment no és una paraula.", andorra_matcher())


@pytest.mark.unit
def test_the_core_terms_cover_the_seven_parishes() -> None:
    folded = set(CORE_ANDORRAN_TERMS)
    for parish in (
        "canillo",
        "encamp",
        "ordino",
        "la massana",
        "sant julià de lòria",
        "escaldes-engordany",
    ):
        assert parish in folded, parish


# ─────────────────────────────────────────────────────────────
# Sizing the mix
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
@pytest.mark.parametrize("count", [100, 1_000, 8_000, 12_750])
def test_the_planned_count_lands_in_the_band(count: int) -> None:
    added = plan_general_ca(count)
    share = added / (count + added)
    low, high = GENERAL_CA_RANGE
    assert low <= share <= high, share


@pytest.mark.unit
def test_the_planned_count_tracks_the_requested_share() -> None:
    assert plan_general_ca(1_000, 0.15) < plan_general_ca(1_000, 0.20)


@pytest.mark.unit
@pytest.mark.parametrize("share", [0.10, 0.149, 0.201, 0.5])
def test_aiming_outside_the_band_is_refused(share: float) -> None:
    # Aiming outside §3.2 would produce a dataset the validator rejects.
    with pytest.raises(ValueError, match=r"outside §3\.2"):
        plan_general_ca(1_000, share)


@pytest.mark.unit
@pytest.mark.parametrize("count", [0, -5])
def test_planning_against_nothing_is_refused(count: int) -> None:
    with pytest.raises(ValueError, match="must be positive"):
        plan_general_ca(count)


@pytest.mark.unit
def test_planning_is_exactly_as_permissive_as_the_arithmetic_allows() -> None:
    """At small totals, rounding a share is not the same as satisfying a range.

    For every total, the planner must either return a count that lands in band or refuse — and it
    must refuse *only* when brute force confirms no whole number would have worked. Some small
    totals are genuinely impossible (with 6 generated, 1 gives 14.3 % and 2 gives 25 %), so the
    boundary is not a simple threshold and must not be hard-coded.
    """
    low, high = GENERAL_CA_RANGE
    for count in range(1, 120):
        feasible = [n for n in range(1, count + 1) if low <= n / (count + n) <= high]
        try:
            added = plan_general_ca(count)
        except ValueError as error:
            assert not feasible, (count, feasible)
            assert "too small to mix" in str(error)
            continue
        assert feasible, (count, added)
        assert low <= added / (count + added) <= high, (count, added)


@pytest.mark.unit
def test_an_impossible_total_is_refused_rather_than_reported_out_of_band() -> None:
    # 6 generated: one addition is 14.3 %, two is 25 %. Returning either would report a share
    # §3.2 rejects, so say so instead.
    with pytest.raises(ValueError, match="too small to mix"):
        plan_general_ca(6)


# ─────────────────────────────────────────────────────────────
# Conversion to §3.2
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_conversion_produces_an_ungrounded_general_ca_example() -> None:
    converted = to_example(GENERAL[0])
    assert converted.type is ExampleType.GENERAL_CA
    # §3.2 enforces this: general_ca is unrelated to Andorra, so citing corpus passages would be
    # a contradiction — and the schema refuses it.
    assert converted.grounding_ids == []
    assert converted.topic == "general_ca/instrucat"
    assert converted.messages[0].content == GENERAL[0].prompt
    assert converted.messages[1].content == GENERAL[0].response


@pytest.mark.unit
def test_conversion_is_idempotent_for_the_same_content() -> None:
    assert to_example(GENERAL[0]).id == to_example(GENERAL[0]).id
    assert to_example(GENERAL[0]).id != to_example(GENERAL[1]).id


@pytest.mark.unit
def test_the_split_is_selectable() -> None:
    assert to_example(GENERAL[0], split=Split.VAL).split is Split.VAL


# ─────────────────────────────────────────────────────────────
# Selection and its drop accounting
# ─────────────────────────────────────────────────────────────


def _select(
    source: list[Instruction], *, wanted: int, exclude: set[str] | None = None
) -> tuple[list[Instruction], MixReport]:
    report = MixReport()
    chosen = select(
        source,
        wanted=wanted,
        matcher=andorra_matcher(),
        exclude=exclude or set(),
        rng=Random(1),
        report=report,
    )
    return chosen, report


@pytest.mark.unit
def test_selection_takes_what_it_needs_and_counts_the_rest() -> None:
    andorran = Instruction(
        "Quantes parròquies té Andorra?", "Set, i cada una té el seu comú.", "instrucat"
    )
    spanish = Instruction(
        "¿Qué es la fotosíntesis?",
        "Es el proceso por el que las plantas transforman la luz del sol en energía química "
        "con la ayuda del agua y del dióxido de carbono que toman del entorno.",
        "instrucat",
    )
    empty = Instruction("   ", "", "instrucat")
    chosen, report = _select([*GENERAL, andorran, spanish, empty], wanted=2)
    assert len(chosen) == 2
    assert report.considered == 7
    assert report.drops["andorra-related"] == 1
    assert report.drops["not-catalan"] == 1
    assert report.drops["empty"] == 1


@pytest.mark.unit
def test_selection_dedups_within_the_source() -> None:
    chosen, report = _select([GENERAL[0], GENERAL[0], GENERAL[1]], wanted=10)
    assert len(chosen) == 2
    assert report.drops["duplicate-in-source"] == 1


@pytest.mark.unit
def test_selection_dedups_against_the_generated_half() -> None:
    """The mix must never re-teach something the Andorran half already covers."""
    already = to_example(GENERAL[0])
    chosen, report = _select(GENERAL, wanted=10, exclude=fingerprints_of([already]))
    assert GENERAL[0] not in chosen
    assert report.drops["already-in-dataset"] == 1


@pytest.mark.unit
def test_selection_is_reproducible_from_a_seed() -> None:
    source = many_general(60)
    first, _ = _select(source, wanted=10)
    second, _ = _select(source, wanted=10)
    assert [i.fingerprint for i in first] == [i.fingerprint for i in second]


@pytest.mark.unit
def test_selection_does_not_depend_on_source_order() -> None:
    source = many_general(60)
    forwards, _ = _select(source, wanted=10)
    backwards, _ = _select(list(reversed(source)), wanted=10)
    assert {i.fingerprint for i in forwards} == {i.fingerprint for i in backwards}


@pytest.mark.unit
def test_a_source_with_nothing_usable_yields_nothing() -> None:
    chosen, report = _select([Instruction("Quantes parròquies té Andorra?", "Set.", "x")], wanted=5)
    assert chosen == []
    assert report.accepted == 0


# ─────────────────────────────────────────────────────────────
# The mix
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_healthy_mix_lands_in_band() -> None:
    base = generated(200)
    examples, report = mix(base, many_general(200), seed=1)
    assert report.in_band
    assert report.share == pytest.approx(DEFAULT_TARGET_SHARE, abs=0.01)
    assert len(examples) == len(base) + report.accepted
    added = [e for e in examples if e.type is ExampleType.GENERAL_CA]
    assert len(added) == report.accepted
    assert all(e.grounding_ids == [] for e in added)


@pytest.mark.unit
def test_the_generated_half_is_preserved_untouched() -> None:
    base = generated(50)
    examples, _ = mix(base, many_general(100), seed=1)
    assert examples[: len(base)] == base


@pytest.mark.unit
def test_a_short_source_is_reported_not_hidden() -> None:
    """A mix that could not be filled is a finding, not a silent shortfall.

    The realised share is out of band, so the CLI fails — otherwise Phase 3 would train on a
    dataset whose anti-forgetting mix is a fraction of what the report claims.
    """
    examples, report = mix(generated(500), GENERAL, seed=1)
    assert report.short > 0
    assert not report.in_band
    assert "short" in render(report)
    assert len(examples) == 500 + report.accepted


@pytest.mark.unit
def test_the_mix_rejects_andorran_rows_from_the_source() -> None:
    poisoned = [
        *many_general(100),
        Instruction("Qui és el cap de Govern d'Andorra?", "El cap del Govern andorrà.", "x"),
    ]
    examples, report = mix(generated(100), poisoned, seed=1)
    assert report.drops.get("andorra-related") == 1
    assert not any(
        "Andorra" in e.messages[0].content for e in examples if e.type is ExampleType.GENERAL_CA
    )


@pytest.mark.unit
def test_the_mix_uses_the_glossary_when_given() -> None:
    glossary = Glossary.model_validate(
        {
            "version": "t",
            "entries": [
                {"term": "esquellots", "category": "cultural", "gloss": "Costum del poble."}
            ],
        }
    )
    poisoned = [
        *many_general(60),
        Instruction(
            "Què són els esquellots?",
            "Un costum popular de fer soroll amb esquelles davant la casa d'uns nuvis.",
            "x",
        ),
    ]
    _, report = mix(generated(60), poisoned, glossary=glossary, seed=1)
    assert report.drops.get("andorra-related") == 1


@pytest.mark.unit
def test_the_share_is_configurable_within_the_band() -> None:
    _, low = mix(generated(400), many_general(200), target_share=0.15, seed=1)
    _, high = mix(generated(400), many_general(200), target_share=0.20, seed=1)
    assert low.accepted < high.accepted
    assert low.in_band and high.in_band


# ─────────────────────────────────────────────────────────────
# Reading upstream files
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_common_aina_shapes_are_all_accepted(tmp_path: Path) -> None:
    path = tmp_path / "aina.jsonl"
    path.write_text(
        "\n".join(
            [
                json.dumps({"instruction": "Pregunta A", "output": "Resposta A"}),
                json.dumps({"prompt": "Pregunta B", "response": "Resposta B"}),
                json.dumps(
                    {
                        "messages": [
                            {"role": "user", "content": "Pregunta C"},
                            {"role": "assistant", "content": "Resposta C"},
                        ]
                    }
                ),
                "",
            ]
        ),
        encoding="utf-8",
    )
    read = read_jsonl_source(path)
    assert [i.prompt for i in read] == ["Pregunta A", "Pregunta B", "Pregunta C"]
    assert all(i.origin == "aina" for i in read)


@pytest.mark.unit
def test_an_aina_input_field_is_folded_into_the_prompt(tmp_path: Path) -> None:
    path = tmp_path / "aina.jsonl"
    path.write_text(
        json.dumps(
            {"instruction": "Resumeix el text", "input": "Un text llarg.", "output": "Curt."}
        )
        + "\n",
        encoding="utf-8",
    )
    assert read_jsonl_source(path)[0].prompt == "Resumeix el text\n\nUn text llarg."


@pytest.mark.unit
def test_an_unrecognised_row_raises_naming_the_line(tmp_path: Path) -> None:
    # A silently skipped row would quietly shrink the mix.
    path = tmp_path / "aina.jsonl"
    path.write_text(json.dumps({"question": "x", "answer": "y"}) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match=r"aina\.jsonl:1: unrecognised shape"):
        read_jsonl_source(path)


@pytest.mark.unit
@pytest.mark.parametrize(
    "row",
    [
        {"messages": ["Pregunta", "Resposta"]},
        {"messages": [{"content": 1}, {"content": 2}]},
        {"messages": [{"role": "user", "content": "Només un torn"}]},
        {"instruction": "Pregunta", "output": 7},
    ],
)
def test_a_malformed_row_raises_rather_than_being_skipped(
    tmp_path: Path, row: dict[str, object]
) -> None:
    path = tmp_path / "aina.jsonl"
    path.write_text(json.dumps(row) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="unrecognised shape"):
        read_jsonl_source(path)


@pytest.mark.unit
def test_blank_lines_between_rows_are_skipped(tmp_path: Path) -> None:
    path = tmp_path / "aina.jsonl"
    path.write_text(
        json.dumps({"prompt": "a", "response": "b"})
        + "\n\n   \n"
        + json.dumps({"prompt": "c", "response": "d"})
        + "\n",
        encoding="utf-8",
    )
    assert [i.prompt for i in read_jsonl_source(path)] == ["a", "c"]


@pytest.mark.unit
def test_an_empty_term_set_never_matches() -> None:
    """Defence for an editable constant.

    Both halves of the matcher are non-empty as long as :data:`CORE_ANDORRAN_TERMS` stays as it
    is — but an empty alternation matches the empty string, so an edit that emptied one half
    would silently reject every instruction in the corpus.
    """
    assert _pattern(set()).search("qualsevol text") is None
    assert _pattern(set()).search("") is None


@pytest.mark.unit
def test_the_origin_can_be_named(tmp_path: Path) -> None:
    path = tmp_path / "x.jsonl"
    path.write_text(json.dumps({"prompt": "a", "response": "b"}) + "\n", encoding="utf-8")
    assert read_jsonl_source(path, origin="instrucat")[0].origin == "instrucat"


# ─────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────


def _write_dataset(path: Path, examples: list[DatasetExample]) -> Path:
    path.write_text("".join(f"{e.model_dump_json()}\n" for e in examples), encoding="utf-8")
    return path


def _write_aina(path: Path, instructions: list[Instruction]) -> Path:
    path.write_text(
        "".join(
            json.dumps({"instruction": i.prompt, "output": i.response}) + "\n" for i in instructions
        ),
        encoding="utf-8",
    )
    return path


@pytest.mark.unit
def test_cli_mixes_and_writes(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    dataset = _write_dataset(tmp_path / "dataset.jsonl", generated(200))
    aina = _write_aina(tmp_path / "aina.jsonl", many_general(200))
    out = tmp_path / "mixed.jsonl"
    assert main([str(dataset), "--aina", str(aina), "--out", str(out)]) == 0
    printed = capsys.readouterr().out
    assert "in band" in printed
    lines = out.read_text(encoding="utf-8").splitlines()
    assert len(lines) > 200
    types = {DatasetExample.model_validate_json(line).type for line in lines}
    assert ExampleType.GENERAL_CA in types


@pytest.mark.unit
def test_cli_fails_when_the_share_is_out_of_band(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    dataset = _write_dataset(tmp_path / "dataset.jsonl", generated(500))
    aina = _write_aina(tmp_path / "aina.jsonl", GENERAL)
    assert main([str(dataset), "--aina", str(aina)]) == 1
    assert "OUT OF BAND" in capsys.readouterr().out


@pytest.mark.unit
def test_cli_uses_the_shipped_glossary(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    glossary = Path(__file__).resolve().parents[1] / "configs" / "glossari-andorra.yaml"
    dataset = _write_dataset(tmp_path / "dataset.jsonl", generated(100))
    poisoned = [
        *many_general(100),
        Instruction(
            "Què fa el cònsol major?",
            "Presideix el comú i el representa davant les altres institucions del país.",
            "x",
        ),
    ]
    aina = _write_aina(tmp_path / "aina.jsonl", poisoned)
    assert main([str(dataset), "--aina", str(aina), "--glossary", str(glossary)]) == 0
    assert "andorra-related=1" in capsys.readouterr().out


@pytest.mark.unit
def test_cli_reports_a_bad_target_share(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    dataset = _write_dataset(tmp_path / "dataset.jsonl", generated(100))
    aina = _write_aina(tmp_path / "aina.jsonl", many_general(50))
    assert main([str(dataset), "--aina", str(aina), "--target-share", "0.5"]) == 1
    assert "outside §3.2" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_reports_a_missing_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main([str(tmp_path / "absent.jsonl"), "--aina", str(tmp_path / "a.jsonl")]) == 1
    assert "no such file" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_reports_an_unrecognised_aina_row(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    dataset = _write_dataset(tmp_path / "dataset.jsonl", generated(100))
    aina = tmp_path / "aina.jsonl"
    aina.write_text(json.dumps({"q": "x"}) + "\n", encoding="utf-8")
    assert main([str(dataset), "--aina", str(aina)]) == 1
    assert "unrecognised shape" in capsys.readouterr().err
