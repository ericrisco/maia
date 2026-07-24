"""Contract tests for the §3.1 corpus schema — invariants, not just the happy path."""

from __future__ import annotations

from datetime import UTC, date, datetime
from typing import Any

import pytest
from pydantic import ValidationError

from maia.schemas import (
    CorpusDocument,
    License,
    Registre,
    Source,
    compute_id,
    normalize_text,
)


def _doc(**overrides: Any) -> dict[str, Any]:
    """A minimal valid document payload; override any field."""
    base: dict[str, Any] = {
        "text": "Andorra és un microestat als Pirineus.",
        "source": "viquipedia",
        "url": "https://ca.wikipedia.org/wiki/Andorra",
        "fetched_at": "2026-08-01T10:00:00Z",
        "license": "cc-by-sa-3.0",
        "registre": "estandard",
    }
    base.update(overrides)
    return base


@pytest.mark.unit
def test_minimal_document_is_valid_and_id_is_computed() -> None:
    doc = CorpusDocument.model_validate(_doc())
    assert doc.id == compute_id(doc.text)
    assert len(doc.id) == 64  # sha256 hex
    assert doc.lang == "ca"
    assert doc.topic == []


@pytest.mark.unit
def test_provided_matching_id_is_accepted() -> None:
    text = "Un text qualsevol."
    doc = CorpusDocument.model_validate(_doc(text=text, id=compute_id(text)))
    assert doc.id == compute_id(text)


@pytest.mark.unit
def test_provided_wrong_id_is_rejected() -> None:
    with pytest.raises(ValidationError, match="does not match sha256"):
        CorpusDocument.model_validate(_doc(id="deadbeef"))


@pytest.mark.unit
def test_id_is_whitespace_normalized() -> None:
    assert compute_id("hola   món") == compute_id("hola\n\tmón")
    assert normalize_text("  a\n b ") == "a b"


@pytest.mark.unit
def test_extra_fields_forbidden() -> None:
    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        CorpusDocument.model_validate(_doc(unexpected="x"))


@pytest.mark.unit
def test_empty_text_rejected() -> None:
    with pytest.raises(ValidationError):
        CorpusDocument.model_validate(_doc(text=""))


@pytest.mark.unit
@pytest.mark.parametrize("field_name", ["source", "license", "registre"])
def test_unknown_enum_value_rejected(field_name: str) -> None:
    with pytest.raises(ValidationError):
        CorpusDocument.model_validate(_doc(**{field_name: "nonsense"}))


@pytest.mark.unit
def test_naive_datetime_rejected_aware_accepted() -> None:
    with pytest.raises(ValidationError):
        CorpusDocument.model_validate(_doc(fetched_at="2026-08-01T10:00:00"))
    doc = CorpusDocument.model_validate(_doc(fetched_at=datetime(2026, 8, 1, 10, tzinfo=UTC)))
    assert doc.fetched_at.tzinfo is not None


@pytest.mark.unit
def test_bad_url_rejected() -> None:
    with pytest.raises(ValidationError):
        CorpusDocument.model_validate(_doc(url="not-a-url"))


@pytest.mark.unit
def test_speaker_only_for_diari_sessions() -> None:
    with pytest.raises(ValidationError, match="speaker is only allowed"):
        CorpusDocument.model_validate(_doc(source="viquipedia", speaker="Sr. Ministre"))
    doc = CorpusDocument.model_validate(
        _doc(
            source="consell_diari_sessions",
            registre="andorra_parlat",
            license="public-official",
            speaker="Sr. Ministre",
        )
    )
    assert doc.speaker == "Sr. Ministre"


@pytest.mark.unit
def test_legal_only_for_juridic_source() -> None:
    legal = {
        "rang": "qualificada",
        "article": "3",
        "consolidacio_data": "2024-01-15",
    }
    with pytest.raises(ValidationError, match="legal metadata is only allowed"):
        CorpusDocument.model_validate(_doc(source="govern", legal=legal))
    doc = CorpusDocument.model_validate(
        _doc(source="juridic", license="public-official", legal=legal)
    )
    assert doc.legal is not None
    assert doc.legal.rang.value == "qualificada"
    assert doc.legal.consolidacio_data == date(2024, 1, 15)


@pytest.mark.unit
def test_juridic_without_legal_is_allowed() -> None:
    doc = CorpusDocument.model_validate(_doc(source="juridic", license="public-official"))
    assert doc.legal is None


@pytest.mark.unit
def test_legal_requires_its_mandatory_fields() -> None:
    with pytest.raises(ValidationError):
        CorpusDocument.model_validate(
            _doc(source="juridic", license="public-official", legal={"article": "3"})
        )


@pytest.mark.unit
def test_license_is_public_gate() -> None:
    assert License.CC_BY_SA_3_0.is_public()
    assert License.PUBLIC_OFFICIAL.is_public()
    assert License.PUBLIC_DOMAIN.is_public()
    assert not License.NO_REDISTRIBUTE.is_public()


@pytest.mark.unit
def test_json_round_trip() -> None:
    doc = CorpusDocument.model_validate(
        _doc(
            source="consell_diari_sessions",
            registre="andorra_parlat",
            license="public-official",
            speaker="Sr. Ministre",
            topic=["institucions"],
        )
    )
    dumped = doc.model_dump(mode="json")
    assert isinstance(dumped["url"], str)
    reloaded = CorpusDocument.model_validate(dumped)
    assert reloaded == doc


@pytest.mark.unit
def test_enum_members_match_contract() -> None:
    assert {s.value for s in Source} == {
        "viquipedia",
        "govern",
        "cultura",
        "bopa",
        "consell_diari_sessions",
        "comuns",
        "visitandorra",
        "classics",
        "juridic",
    }
    assert {r.value for r in Registre} == {"estandard", "andorra_parlat"}
