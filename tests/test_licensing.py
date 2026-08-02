"""Tests for the single definition of what MAIA is published under (D-0043, D-0045).

The bug these exist to prevent already happened once: the dataset licence lived in three places,
two were changed and one was not, and the legal gate ended up **requiring** the card to name a
different licence than the upload declared. Nothing failed, because the card generator and the card
checker were wrong in the same direction and each was tested against the other.
"""

from __future__ import annotations

import pytest

from maia.licensing import (
    DATASET_LICENSE,
    DATASET_LICENSE_LABEL,
    MODEL_LICENSE,
    states_dataset_licence,
)
from maia.publication import cards, compliance
from maia.schemas import Source
from maia.synth import publish


@pytest.mark.unit
def test_the_dataset_is_share_alike() -> None:
    """Pinned. The corpus includes CC-BY-SA-3.0 Viquipèdia text and share-alike is viral, so a
    non-share-alike release would grant a permission this project has no authority to grant.
    Confirmed by the PO on 2026-08-02."""
    assert DATASET_LICENSE == "cc-by-sa-4.0"
    assert DATASET_LICENSE_LABEL.lower() == DATASET_LICENSE
    assert MODEL_LICENSE == "apache-2.0"


@pytest.mark.unit
def test_every_module_that_names_the_licence_names_the_same_one() -> None:
    """The three call sites: the card generator, the HF upload, and the legal gate. When these were
    three separate constants they disagreed, and the published artifact would have contradicted
    itself about the one fact a downstream user has to be able to trust."""
    assert cards.DATASET_LICENSE is DATASET_LICENSE
    assert publish.DATASET_LICENSE is DATASET_LICENSE
    assert DATASET_LICENSE_LABEL in compliance.attribution_section([Source.VIQUIPEDIA])


@pytest.mark.unit
def test_the_gate_accepts_the_card_the_generator_produces() -> None:
    """The end-to-end version of the same guarantee, and the assertion that would have caught the
    original bug: a card written by MAIA must satisfy MAIA's own licence check."""
    generated = compliance.attribution_section([Source.VIQUIPEDIA])
    assert states_dataset_licence(generated)
    assert compliance.missing_licence_statement(generated) == []


@pytest.mark.unit
def test_the_gate_rejects_a_card_naming_the_old_licence() -> None:
    """`cc-by-sa-4.0` does not contain `cc-by-4.0` as a substring, but the reverse check would have
    silently passed the wrong licence — so this asserts the direction that matters."""
    findings = compliance.missing_licence_statement("Released under CC-BY-4.0.")
    assert len(findings) == 1
    assert "CC-BY-SA-4.0" in findings[0].detail


@pytest.mark.unit
@pytest.mark.parametrize("text", ["cc-by-sa-4.0", "CC-BY-SA-4.0", "cc by sa 4.0", "x CC BY SA 4.0"])
def test_both_spellings_of_the_licence_count(text: str) -> None:
    """A hand-written card would reasonably use either form; matching lives in one place so the
    gate cannot demand a spelling the generator never emits."""
    assert states_dataset_licence(text)


@pytest.mark.unit
def test_a_card_that_names_no_licence_is_caught() -> None:
    assert not states_dataset_licence("# MAIA dataset\n\nAndorran Catalan instructions.\n")
