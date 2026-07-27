"""Tests for the Andorran lexicon glossary (PLAN M2.02)."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import pytest
import yaml

from maia.schemas import (
    CorpusDocument,
    DatasetExample,
    License,
    Registre,
    Source,
    compute_id,
)
from maia.synth.glossary import (
    Category,
    Glossary,
    GlossaryEntry,
    check_usage,
    extract_candidates,
    fold,
    load_glossary,
    main,
    render_glossary,
    render_usage,
)

SHIPPED = Path(__file__).resolve().parents[1] / "configs" / "glossari-andorra.yaml"
GROUNDING = compute_id("Un passatge del corpus.")


def entry(term: str, **overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "term": term,
        "category": "institucional",
        "gloss": f"Definició de {term} prou llarga.",
    }
    payload.update(overrides)
    return payload


def glossary(entries: list[dict[str, object]], **overrides: object) -> Glossary:
    payload: dict[str, object] = {"version": "test", "entries": entries}
    payload.update(overrides)
    return Glossary.model_validate(payload)


def document(text: str, index: int) -> CorpusDocument:
    return CorpusDocument(
        text=text,
        source=Source.GOVERN,
        url=f"https://www.govern.ad/{index}",  # type: ignore[arg-type]
        fetched_at=datetime(2026, 8, 1, tzinfo=UTC),
        lang="ca",
        license=License.PUBLIC_OFFICIAL,
        registre=Registre.ESTANDARD,
    )


def example(user: str, assistant: str) -> DatasetExample:
    return DatasetExample.model_validate(
        {
            "id": str(uuid4()),
            "messages": [
                {"role": "user", "content": user},
                {"role": "assistant", "content": assistant},
            ],
            "type": "qa",
            "topic": "institucions/comuns-i-consols",
            "grounding_ids": [GROUNDING],
            "generator": "claude-opus-5",
            "judge_score": 0.9,
            "split": "train",
        }
    )


# ─────────────────────────────────────────────────────────────
# Folding — the basis of every match
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_folding_removes_case_and_accents() -> None:
    # Without this, comú and comu are different terms — and the corpus contains both.
    assert fold("Comú") == fold("comu") == "comu"
    assert fold("SÍNDIC") == "sindic"
    assert fold("l·l") == "l·l"  # the interpunct is not a combining mark


# ─────────────────────────────────────────────────────────────
# The shipped seed
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_shipped_seed_loads() -> None:
    loaded = load_glossary(SHIPPED)
    assert len(loaded.entries) > 30
    assert set(loaded.by_category) == {category.value for category in Category}


@pytest.mark.unit
def test_the_shipped_seed_is_approved_and_says_who_approved_it() -> None:
    """Approved as a *working seed* (D-0043) so generation is not blocked. The approver string
    records that this was an engineering review — native-speaker validation has not happened, and
    a bare `true` here would erase that distinction."""
    loaded = load_glossary(SHIPPED)
    assert loaded.approved is True
    assert "Eric Risco" in loaded.approved_by


@pytest.mark.unit
def test_the_shipped_seed_carries_the_load_bearing_terms() -> None:
    terms = {fold(form) for entry_ in load_glossary(SHIPPED).entries for form in entry_.forms}
    # The words a general Catalan model gets wrong, named in the plan.
    for expected in ("sindic", "consol", "batlle", "comu", "quart", "borda", "canalla"):
        assert expected in terms, expected


@pytest.mark.unit
def test_the_shipped_seed_names_the_traps() -> None:
    """The `equivalent` field is the useful half: it says which word *not* to reach for."""
    by_term = {entry_.term: entry_ for entry_ in load_glossary(SHIPPED).entries}
    assert by_term["cònsol major"].equivalent == "alcalde"
    assert by_term["comú"].equivalent == "ajuntament"
    assert by_term["parròquia"].equivalent == "municipi"


# ─────────────────────────────────────────────────────────────
# Entry validation
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_variant_that_repeats_the_term_is_rejected() -> None:
    # The slip the shipped seed originally had: `term: Escudella`, `variants: [escudella]`.
    with pytest.raises(ValueError, match="repeats a form in its variants"):
        GlossaryEntry.model_validate(entry("Escudella", variants=["escudella"]))


@pytest.mark.unit
def test_a_blank_variant_is_rejected() -> None:
    with pytest.raises(ValueError, match="empty variant"):
        GlossaryEntry.model_validate(entry("comú", variants=["  "]))


@pytest.mark.unit
def test_a_term_cannot_be_its_own_equivalent() -> None:
    with pytest.raises(ValueError, match="lists itself"):
        GlossaryEntry.model_validate(entry("comú", equivalent="Comu"))


@pytest.mark.unit
def test_a_gloss_must_be_usable_as_prompt_material() -> None:
    with pytest.raises(ValueError):
        GlossaryEntry.model_validate({"term": "comú", "category": "institucional", "gloss": "x"})


@pytest.mark.unit
def test_an_unknown_category_is_rejected() -> None:
    with pytest.raises(ValueError):
        GlossaryEntry.model_validate(entry("comú", category="inventada"))


@pytest.mark.unit
def test_forms_includes_the_term_and_its_variants() -> None:
    parsed = GlossaryEntry.model_validate(entry("comú", variants=["comuns"]))
    assert parsed.forms == ["comú", "comuns"]


# ─────────────────────────────────────────────────────────────
# Glossary validation
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_form_claimed_by_two_entries_is_rejected() -> None:
    with pytest.raises(ValueError, match="appear more than once"):
        glossary([entry("comú"), entry("comuns", variants=["comú"])])


@pytest.mark.unit
def test_approval_requires_a_name() -> None:
    with pytest.raises(ValueError, match="requires approved_by"):
        glossary([entry("comú")], approved=True)


@pytest.mark.unit
def test_prompt_lines_include_the_equivalent_when_there_is_one() -> None:
    lines = glossary([entry("comú", equivalent="ajuntament"), entry("Sindicatura")]).prompt_lines()
    assert "(en català general: ajuntament)" in lines[0]
    assert "(en català general" not in lines[1]


@pytest.mark.unit
def test_prompt_lines_can_be_filtered_by_category() -> None:
    loaded = glossary([entry("comú"), entry("borda", category="geografic")])
    lines = loaded.prompt_lines([Category.GEOGRAFIC])
    assert len(lines) == 1
    assert "borda" in lines[0]


# ─────────────────────────────────────────────────────────────
# Matching
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_term_is_not_matched_inside_a_longer_word() -> None:
    """The reason patterns use word boundaries: *cònsol* lives inside *consolidació*."""
    pattern = GlossaryEntry.model_validate(entry("cònsol")).pattern()
    assert pattern.search(fold("El cònsol major va dir"))
    assert not pattern.search(fold("El text consolidat de la llei"))


@pytest.mark.unit
def test_matching_ignores_case_and_accents() -> None:
    pattern = GlossaryEntry.model_validate(entry("comú")).pattern()
    for text in ("El COMÚ d'Encamp", "el comu d'encamp", "El Comú"):
        assert pattern.search(fold(text)), text


@pytest.mark.unit
def test_a_multi_word_term_matches_across_flexible_whitespace() -> None:
    pattern = GlossaryEntry.model_validate(entry("síndic general")).pattern()
    assert pattern.search(fold("el síndic general va obrir la sessió"))
    assert pattern.search(fold("el síndic\n  general va obrir"))
    assert not pattern.search(fold("el síndic de greuges"))


@pytest.mark.unit
def test_variants_match_too() -> None:
    pattern = GlossaryEntry.model_validate(entry("comú", variants=["comuns"])).pattern()
    assert pattern.search(fold("els comuns de les parròquies"))


# ─────────────────────────────────────────────────────────────
# Contrastive extraction
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_word_only_in_the_andorran_side_ranks_top() -> None:
    andorran = [
        document("El cònsol major del comú va signar el ban parroquial.", i) for i in range(6)
    ]
    general = [
        document("L'alcalde de la ciutat va signar el document municipal.", i) for i in range(6)
    ]
    candidates = extract_candidates(andorran, general, min_count=5)
    terms = [candidate.term for candidate in candidates]
    assert "consol" in terms
    assert candidates[0].general_count == 0


@pytest.mark.unit
def test_shared_words_are_not_candidates() -> None:
    andorran = [document("El cònsol va signar el document.", i) for i in range(6)]
    general = [document("L'alcalde va signar el document.", i) for i in range(6)]
    terms = [c.term for c in extract_candidates(andorran, general, min_count=5)]
    assert "signar" not in terms
    assert "document" not in terms


@pytest.mark.unit
def test_frequencies_are_normalized_by_corpus_size() -> None:
    """A small Andorran corpus must not make every one of its words look Andorran."""
    andorran = [document("El cònsol i el batlle van parlar.", i) for i in range(6)]
    general = [document("El batlle i el jutge van parlar molt sovint aquí.", i) for i in range(200)]
    terms = [c.term for c in extract_candidates(andorran, general, min_count=5)]
    assert "consol" in terms
    assert "batlle" not in terms  # equally frequent on both sides once normalized


@pytest.mark.unit
def test_rare_and_short_words_are_skipped() -> None:
    andorran = [document("El cònsol major va signar.", i) for i in range(6)]
    andorran.append(document("Una paraula raríssima: quixotesc.", 99))
    candidates = extract_candidates(andorran, [document("Res.", 0)], min_count=5)
    terms = [c.term for c in candidates]
    assert "quixotesc" not in terms  # occurs once
    assert all(len(term) >= 3 for term in terms)


@pytest.mark.unit
def test_the_limit_is_honoured() -> None:
    vocabulary = " ".join(f"mot{chr(97 + i // 26)}{chr(97 + i % 26)}x" for i in range(40))
    andorran = [document(vocabulary, j) for j in range(6)]
    assert len(extract_candidates(andorran, [document("Res.", 0)], min_count=5, limit=5)) == 5


@pytest.mark.unit
def test_digits_are_not_lexicon() -> None:
    # The tokenizer is letters-only on purpose: "1993" is a fact for the taxonomy to cover,
    # not a word for the glossary. It also means "paraula1" and "paraula2" are one term.
    andorran = [document("La reforma de 1866 i la Constitució de 1993.", i) for i in range(6)]
    terms = [c.term for c in extract_candidates(andorran, [document("Res.", 0)], min_count=5)]
    assert "1866" not in terms
    assert "1993" not in terms
    assert "reforma" in terms


@pytest.mark.unit
def test_extraction_from_empty_corpora_yields_nothing() -> None:
    assert extract_candidates([], []) == []


# ─────────────────────────────────────────────────────────────
# Usage measurement — closing the loop
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_usage_counts_terms_that_reached_the_dataset() -> None:
    loaded = glossary([entry("comú", equivalent="ajuntament"), entry("Raonador")])
    examples = [
        example("Qui governa la parròquia?", "El comú, encapçalat pel cònsol major."),
        example("I qui defensa el ciutadà?", "El Raonador del Ciutadà."),
    ]
    report = check_usage(examples, loaded)
    assert report.examples == 2
    assert report.counts["comú"] == 1
    assert report.counts["Raonador"] == 1
    assert report.coverage == 1.0
    assert report.unused == []
    rendered = render_usage(report)
    assert "2/2 terms used (100%)" in rendered
    assert "never used" not in rendered


@pytest.mark.unit
def test_unused_terms_are_the_gap_the_requirement_exists_to_close() -> None:
    loaded = glossary([entry("comú"), entry("esquellots", category="cultural")])
    report = check_usage([example("Qui governa?", "El comú.")], loaded)
    assert report.used == ["comú"]
    assert report.unused == ["esquellots"]
    assert report.coverage == 0.5
    assert "never used: esquellots" in render_usage(report)


@pytest.mark.unit
def test_using_the_general_catalan_equivalent_instead_is_flagged() -> None:
    """A dataset that says *alcalde* where an Andorran says *cònsol* has failed at the one
    thing this glossary exists for — and the term count alone would not show it."""
    loaded = glossary([entry("cònsol major", equivalent="alcalde")])
    report = check_usage([example("Qui presideix el comú?", "L'alcalde de la parròquia.")], loaded)
    assert report.counts["cònsol major"] == 0
    assert report.equivalents_used["cònsol major"] == 1
    assert "equivalent used instead" in render_usage(report)


@pytest.mark.unit
def test_multiple_occurrences_are_all_counted() -> None:
    loaded = glossary([entry("comú")])
    report = check_usage([example("El comú?", "El comú d'Encamp i el comú d'Ordino.")], loaded)
    assert report.counts["comú"] == 3


@pytest.mark.unit
def test_usage_over_no_examples_is_zero_coverage() -> None:
    report = check_usage([], glossary([entry("comú")]))
    assert report.coverage == 0.0
    assert report.unused == ["comú"]


@pytest.mark.unit
def test_render_usage_truncates_a_long_unused_list() -> None:
    loaded = glossary([entry(f"terme{index}") for index in range(40)])
    assert "more" in render_usage(check_usage([], loaded))


# ─────────────────────────────────────────────────────────────
# Loading and rendering
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_non_mapping_file_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "g.yaml"
    path.write_text("- a\n- b\n", encoding="utf-8")
    with pytest.raises(ValueError, match="expected a YAML mapping"):
        load_glossary(path)


@pytest.mark.unit
def test_a_schema_error_names_the_problem(tmp_path: Path) -> None:
    path = tmp_path / "g.yaml"
    path.write_text(
        yaml.safe_dump({"version": "t", "entries": [{"term": "x", "category": "institucional"}]}),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="gloss"):
        load_glossary(path)


@pytest.mark.unit
def test_render_counts_terms_without_an_equivalent() -> None:
    loaded = glossary([entry("comú", equivalent="ajuntament"), entry("Sindicatura")])
    rendered = render_glossary(loaded, Path("g.yaml"))
    assert "2 terms" in rendered
    assert "1 term(s) with no general-Catalan equivalent" in rendered


# ─────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_cli_check_validates_the_shipped_seed(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["check", str(SHIPPED)]) == 0
    assert "[approved]" in capsys.readouterr().out


@pytest.mark.unit
def test_cli_candidates_contrasts_two_corpora(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    andorran = tmp_path / "andorran.jsonl"
    general = tmp_path / "general.jsonl"
    andorran.write_text(
        "".join(
            f"{document('El cònsol major del comú va signar el ban.', i).model_dump_json()}\n"
            for i in range(6)
        ),
        encoding="utf-8",
    )
    general.write_text(
        "".join(
            f"{document('L alcalde va signar el document municipal.', i).model_dump_json()}\n"
            for i in range(6)
        ),
        encoding="utf-8",
    )
    assert main(["candidates", "--andorran", str(andorran), "--general", str(general)]) == 0
    out = capsys.readouterr().out
    assert "candidate term(s)" in out
    assert "only here" in out


@pytest.mark.unit
def test_cli_usage_measures_a_dataset(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    dataset = tmp_path / "dataset.jsonl"
    dataset.write_text(
        f"{example('Qui governa?', 'El comú.').model_dump_json()}\n", encoding="utf-8"
    )
    assert main(["usage", str(SHIPPED), "--dataset", str(dataset)]) == 0
    assert "terms used" in capsys.readouterr().out


@pytest.mark.unit
def test_cli_reports_a_missing_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["check", str(tmp_path / "absent.yaml")]) == 1
    assert "no such file" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_reports_a_broken_glossary(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "g.yaml"
    path.write_text("- not a mapping\n", encoding="utf-8")
    assert main(["check", str(path)]) == 1
    assert "expected a YAML mapping" in capsys.readouterr().err
