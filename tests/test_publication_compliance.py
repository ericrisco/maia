"""Tests for the M6.01 legal gate."""

from __future__ import annotations

from uuid import UUID, uuid5

import pytest

from maia.publication.compliance import (
    PROXIMITY,
    SHARE_ALIKE,
    ComplianceReport,
    attributed_opinions,
    attribution_section,
    check,
    missing_attributions,
    missing_licence_statement,
    render,
    restricted_grounding,
    sources_needing_attribution,
)
from maia.schemas import (
    CorpusDocument,
    DatasetExample,
    ExampleType,
    License,
    Registre,
    Source,
    compute_id,
)

_NAMESPACE = UUID("6ba7b81b-9dad-11d1-80b4-00c04fd430c8")
CARD = "# MAIA dataset\n\nReleased under CC-BY-SA-4.0.\n"


def document(
    text: str, *, licence: License = License.PUBLIC_OFFICIAL, source: Source = Source.JURIDIC
) -> CorpusDocument:
    return CorpusDocument.model_validate(
        {
            "id": compute_id(text),
            "text": text,
            "source": source.value,
            "url": "https://www.portaljuridicandorra.ad/x",
            "fetched_at": "2026-07-26T10:00:00+00:00",
            "license": licence.value,
            "registre": Registre.ESTANDARD.value,
            "lang": "ca",
        }
    )


PUBLIC = document("Passatge públic del corpus andorrà.")
RESTRICTED = document("Passatge restringit.", licence=License.NO_REDISTRIBUTE)
WIKI = document(
    "Passatge de la Viquipèdia.", licence=License.CC_BY_SA_3_0, source=Source.VIQUIPEDIA
)
ABSENT = document("Passatge que no és al corpus.")
CORPUS = {doc.id: doc for doc in (PUBLIC, RESTRICTED, WIKI)}


def example(
    tag: str,
    *,
    answer: str = "Vint-i-vuit consellers generals.",
    question: str = "Quants consellers hi ha?",
    grounding: list[CorpusDocument] | None = None,
) -> DatasetExample:
    return DatasetExample.model_validate(
        {
            "id": str(uuid5(_NAMESPACE, tag)),
            "messages": [
                {"role": "user", "content": question},
                {"role": "assistant", "content": answer},
            ],
            "type": ExampleType.QA.value,
            "topic": "institucions/consell-general",
            "grounding_ids": sorted({doc.id for doc in (grounding or [PUBLIC])}),
            "generator": "claude-opus-5",
            "judge_score": 0.9,
            "split": "train",
        }
    )


# ─────────────────────────────────────────────────────────────
# Restricted grounding: zero, and unverifiable counts
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_public_grounding_is_clean() -> None:
    assert restricted_grounding([example("a")], CORPUS) == []


@pytest.mark.unit
def test_restricted_grounding_is_a_finding() -> None:
    """Re-checked here even though M2.11 withholds them: a gate that trusts is not a gate."""
    findings = restricted_grounding([example("bad", grounding=[RESTRICTED])], CORPUS)
    assert [finding.kind for finding in findings] == ["restricted-grounding"]
    assert "no-redistribute" in findings[0].detail


@pytest.mark.unit
def test_grounding_absent_from_the_corpus_counts_as_unpublishable() -> None:
    """ "We could not check" has never been a licence in this project."""
    findings = restricted_grounding([example("orphan", grounding=[ABSENT])], CORPUS)
    assert [finding.kind for finding in findings] == ["unverifiable-grounding"]
    assert "cannot be shown to be publishable" in findings[0].detail


@pytest.mark.unit
def test_both_kinds_block_publication() -> None:
    report = check(
        [example("bad", grounding=[RESTRICTED]), example("orphan", grounding=[ABSENT])],
        corpus=CORPUS,
        card=CARD,
    )
    assert not report.passed
    assert len(report.blocking) == 2


# ─────────────────────────────────────────────────────────────
# Attributed opinions: deliberately over-broad
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_an_attributed_stance_is_flagged() -> None:
    """Exactly what the plan forbids republishing as training data."""
    findings = attributed_opinions(
        [
            example(
                "opinion",
                answer=(
                    "El conseller general va dir que aquesta situació és inacceptable i que el "
                    "seu grup no donarem suport al pressupost."
                ),
            )
        ]
    )
    assert len(findings) == 1
    assert findings[0].kind == "attributed-opinion"
    assert "needs PO review" in findings[0].detail


@pytest.mark.unit
def test_a_factual_answer_about_an_institution_is_not_flagged() -> None:
    assert (
        attributed_opinions(
            [
                example(
                    "factual",
                    answer=(
                        "El Consell General es compon de vint-i-vuit consellers generals, la "
                        "meitat elegits per circumscripció parroquial."
                    ),
                )
            ]
        )
        == []
    )


@pytest.mark.unit
def test_attribution_without_a_stance_is_not_flagged() -> None:
    """Naming a role is not the problem; naming a role beside a position is."""
    assert (
        attributed_opinions(
            [
                example(
                    "role",
                    answer="El síndic general presideix el Consell i el representa.",
                )
            ]
        )
        == []
    )


@pytest.mark.unit
def test_a_stance_without_attribution_is_not_flagged() -> None:
    assert (
        attributed_opinions(
            [example("stance", answer="Molts ciutadans consideren que cal més habitatge.")]
        )
        == []
    )


@pytest.mark.unit
def test_distance_matters_so_a_long_factual_answer_is_not_flagged() -> None:
    """A factual answer can mention a councillor and, paragraphs later, quote a manifesto."""
    far = (
        "El conseller general presideix la comissió legislativa corresponent. "
        + "Aquesta és una explicació purament descriptiva del funcionament parlamentari. " * 8
        + "Alguns creuen que caldria reformar-ho."
    )
    assert attributed_opinions([example("far", answer=far)]) == []
    assert len(far) > PROXIMITY * 2


@pytest.mark.unit
def test_one_finding_per_example_because_the_output_is_a_review_queue() -> None:
    repeated = "El conseller va dir que és inacceptable. La consellera afirma que és irresponsable."
    assert len(attributed_opinions([example("many", answer=repeated)])) == 1


@pytest.mark.unit
def test_the_flag_is_accent_insensitive() -> None:
    assert attributed_opinions(
        [example("acc", answer="La consellera declara que això és vergonyos i inacceptable.")]
    )


@pytest.mark.unit
def test_attributed_opinions_do_not_block_the_pipeline() -> None:
    """A regular expression should not block a release on a guess about intent."""
    report = check(
        [example("op", answer="El ministre va dir que és inacceptable.")],
        corpus=CORPUS,
        card=CARD,
    )
    assert report.needs_review
    assert report.blocking == []
    assert report.passed


@pytest.mark.unit
def test_the_report_explains_why_it_over_flags() -> None:
    report = check(
        [example("op", answer="El ministre va dir que és inacceptable.")],
        corpus=CORPUS,
        card=CARD,
    )
    rendered = render(report)
    assert "attributed opinions to review: 1" in rendered
    assert "not a job for a regular expression" in rendered
    assert "publish a named politician's position" in rendered


# ─────────────────────────────────────────────────────────────
# Attributions
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_only_share_alike_sources_need_crediting() -> None:
    assert License.CC_BY_SA_3_0 in SHARE_ALIKE
    assert sources_needing_attribution([example("a", grounding=[PUBLIC])], CORPUS) == set()
    assert sources_needing_attribution([example("w", grounding=[WIKI])], CORPUS) == {
        Source.VIQUIPEDIA
    }


@pytest.mark.unit
def test_only_cited_sources_need_crediting() -> None:
    """Crediting a source the dataset does not draw on is noise."""
    assert sources_needing_attribution([example("a", grounding=[PUBLIC])], CORPUS) == set()


@pytest.mark.unit
def test_a_missing_credit_is_a_finding_and_blocks() -> None:
    """The attribution is what makes the release lawful, not a formatting nicety."""
    examples = [example("w", grounding=[WIKI])]
    findings = missing_attributions(examples, CORPUS, CARD)
    assert [finding.kind for finding in findings] == ["missing-attribution"]
    assert not check(examples, corpus=CORPUS, card=CARD).passed


@pytest.mark.unit
def test_a_credited_source_passes() -> None:
    card = CARD + attribution_section([Source.VIQUIPEDIA])
    assert missing_attributions([example("w", grounding=[WIKI])], CORPUS, card) == []
    assert check([example("w", grounding=[WIKI])], corpus=CORPUS, card=card).passed


@pytest.mark.unit
def test_the_generated_section_states_the_dataset_licence() -> None:
    section = attribution_section([Source.VIQUIPEDIA, Source.JURIDIC])
    assert "## Attributions" in section
    assert "CC-BY-SA-4.0" in section
    assert "`viquipedia`" in section


@pytest.mark.unit
def test_an_empty_attribution_section_is_empty() -> None:
    assert attribution_section([]) == ""


@pytest.mark.unit
def test_a_card_without_the_dataset_licence_is_a_finding() -> None:
    """A card that credits every source and never says what this is licensed under is incomplete."""
    findings = missing_licence_statement("# MAIA\n\nUn dataset en català.\n")
    assert [finding.kind for finding in findings] == ["missing-licence"]
    assert "cannot tell what they may do with it" in findings[0].detail


@pytest.mark.unit
@pytest.mark.parametrize("statement", ["CC-BY-SA-4.0", "cc by sa 4.0", "Licensed CC-BY-SA-4.0."])
def test_either_spelling_of_the_licence_counts(statement: str) -> None:
    assert missing_licence_statement(f"# Card\n\n{statement}\n") == []


# ─────────────────────────────────────────────────────────────
# The gate refuses to pass on missing inputs
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_clean_dataset_with_both_inputs_passes() -> None:
    report = check([example("a"), example("b")], corpus=CORPUS, card=CARD)
    assert report.passed
    assert "✓ PASS — M6.01 legal gate over 2 example(s)" in render(report)


@pytest.mark.unit
def test_without_a_corpus_the_gate_cannot_pass() -> None:
    """A §3.2 example carries no licence of its own."""
    report = check([example("a")], card=CARD)
    assert not report.passed
    rendered = render(report)
    assert "no corpus supplied" in rendered
    assert "NOT CHECKED" in rendered


@pytest.mark.unit
def test_without_a_card_the_gate_cannot_pass() -> None:
    report = check([example("a")], corpus=CORPUS)
    assert not report.passed
    assert "no dataset card supplied" in render(report)


@pytest.mark.unit
def test_a_partial_run_is_still_useful_but_never_green() -> None:
    """So the gate stays usable during development without ever reading as a pass."""
    report = check([example("op", answer="El ministre va dir que és inacceptable.")])
    assert report.needs_review
    assert not report.passed


@pytest.mark.unit
def test_a_green_gate_is_not_the_pos_approval() -> None:
    """M6.01 requires a final manual review; this only says nothing mechanical is left."""
    rendered = render(check([example("a")], corpus=CORPUS, card=CARD))
    assert "a green result is NOT the PO's approval" in rendered
    assert "final manual review" in rendered


@pytest.mark.unit
def test_an_empty_report_does_not_pass() -> None:
    assert not ComplianceReport().passed


@pytest.mark.unit
def test_findings_are_grouped_by_kind_in_the_report() -> None:
    report = check(
        [example("bad", grounding=[RESTRICTED]), example("w", grounding=[WIKI])],
        corpus=CORPUS,
        card=CARD,
    )
    rendered = render(report)
    assert "✗ grounded in no-redistribute text: 1" in rendered
    assert "✗ share-alike source not credited: 1" in rendered
    assert "✓ grounding not in the corpus supplied: 0" in rendered
