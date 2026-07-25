"""Corpus data contract (ANEXO §3.1).

This module is the single source of truth for the shape of every corpus document — the
contract between Data Engineering (producers: scrapers/cleaners) and ML Engineering
(consumers: dataset generation, RAG ingest). Changing it is a breaking change: PR + team
notice. `maia.corpus.validate` enforces it at 100 % over any corpus file.
"""

from __future__ import annotations

import hashlib
import re
import unicodedata
from datetime import date
from enum import StrEnum
from typing import Self

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, HttpUrl, model_validator

_WHITESPACE = re.compile(r"\s+")


def normalize_text(text: str) -> str:
    """Canonical normalization used for the document id.

    NFC unicode + whitespace runs (including newlines) collapsed to single spaces +
    stripped. Applied only to derive a stable content id; the stored ``text`` keeps its
    original form.
    """
    return _WHITESPACE.sub(" ", unicodedata.normalize("NFC", text)).strip()


def compute_id(text: str) -> str:
    """SHA-256 of the normalized text — the document id (§3.1)."""
    return hashlib.sha256(normalize_text(text).encode("utf-8")).hexdigest()


class Source(StrEnum):
    """Corpus provenance (§3.1)."""

    VIQUIPEDIA = "viquipedia"
    GOVERN = "govern"
    CULTURA = "cultura"
    BOPA = "bopa"
    CONSELL_DIARI_SESSIONS = "consell_diari_sessions"
    COMUNS = "comuns"
    VISITANDORRA = "visitandorra"
    CLASSICS = "classics"
    JURIDIC = "juridic"
    # Grounding-only sources (M1.13, M1.14). Both are `no-redistribute`: their text never
    # enters a public artifact, only the knowledge paraphrased from it.
    RTVA = "rtva"
    PREMSA = "premsa"


class License(StrEnum):
    """Per-document license — the mandatory compliance control (ANEXO §8)."""

    CC_BY_SA_3_0 = "cc-by-sa-3.0"
    PUBLIC_OFFICIAL = "public-official"
    PUBLIC_DOMAIN = "public-domain"
    NO_REDISTRIBUTE = "no-redistribute"

    def is_public(self) -> bool:
        """True if documents under this license may enter public artifacts.

        ``no-redistribute`` sources (Enciclopèdia.cat, leslleis.com, BOPA-as-collection,
        RTVA/press) are grounding/contrast reads only — never published.
        """
        return self is not License.NO_REDISTRIBUTE


class Registre(StrEnum):
    """Linguistic register — keeps standard Catalan separable from spoken Andorran.

    ``andorra_parlat`` is *transcribed-for-publication* speech (the Diari de Sessions, which
    is edited before printing); ``andorra_parlat_oral`` is genuinely unedited speech (radio,
    M1.13). They are kept apart because the second is closer to how Andorrans actually talk
    and carries transcription error the first does not, so the two are weighted differently
    downstream.
    """

    ESTANDARD = "estandard"
    ANDORRA_PARLAT = "andorra_parlat"
    ANDORRA_PARLAT_ORAL = "andorra_parlat_oral"


class Rang(StrEnum):
    """Rank of an Andorran legal norm."""

    CONSTITUCIO = "constitucio"
    QUALIFICADA = "qualificada"
    ORDINARIA = "ordinaria"
    REGLAMENT = "reglament"


class Legal(BaseModel):
    """Legal metadata — present only on documents from the juridical subcorpus (§3.1)."""

    model_config = ConfigDict(extra="forbid")

    rang: Rang
    article: str = Field(min_length=1)
    consolidacio_data: date
    llei: str | None = None


class CorpusDocument(BaseModel):
    """A single corpus document (ANEXO §3.1).

    ``id`` is derived from the normalized text; omit it when constructing and it is
    computed, provide it (e.g. loading a corpus file) and it is verified for integrity.
    """

    model_config = ConfigDict(extra="forbid")

    id: str = ""
    text: str = Field(min_length=1)
    source: Source
    url: HttpUrl
    fetched_at: AwareDatetime
    lang: str = "ca"
    topic: list[str] = Field(default_factory=list)
    license: License
    registre: Registre
    speaker: str | None = None
    legal: Legal | None = None

    @model_validator(mode="after")
    def _check_invariants(self) -> Self:
        expected_id = compute_id(self.text)
        if self.id and self.id != expected_id:
            raise ValueError(
                f"id does not match sha256 of normalized text "
                f"(got {self.id!r}, expected {expected_id!r})"
            )
        if not self.id:
            self.id = expected_id

        if self.speaker is not None and self.source is not Source.CONSELL_DIARI_SESSIONS:
            raise ValueError("speaker is only allowed for source=consell_diari_sessions")

        if self.legal is not None and self.source is not Source.JURIDIC:
            raise ValueError("legal metadata is only allowed for source=juridic")

        return self
