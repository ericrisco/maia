"""Data contracts: corpus (ANEXO §3.1) and dataset (ANEXO §3.2).

This module is the single source of truth for the shape of every corpus document and every
synthetic training example — the contract between Data Engineering (producers:
scrapers/cleaners, the generation engine) and ML Engineering (consumers: dataset generation,
RAG ingest, fine-tuning). Changing it is a breaking change: PR + team notice.
`maia.corpus.validate` enforces §3.1 over any corpus file, `maia.synth.validate` enforces
§3.2 plus its distribution constraints over any dataset file.
"""

from __future__ import annotations

import hashlib
import re
import unicodedata
from datetime import date
from enum import StrEnum
from typing import Self
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, HttpUrl, model_validator

_WHITESPACE = re.compile(r"\s+")

#: A §3.1 document id: the lowercase hex sha256 that `compute_id` produces.
_SHA256_HEX = re.compile(r"[0-9a-f]{64}")


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


# ─────────────────────────────────────────────────────────────
# Dataset contract (ANEXO §3.2)
# ─────────────────────────────────────────────────────────────
#
# The output contract of Phase 2 and the input contract of Phase 3. It lives beside §3.1
# because the two are one agreement between Data Engineering and ML Engineering, and because
# a dataset example references corpus ids — keeping them together makes that link explicit.


class ExampleType(StrEnum):
    """What kind of training example this is (§3.2).

    The mix is deliberate and its proportions are checked: ``no_ho_se`` teaches the model to
    decline rather than invent (~8 %), ``general_ca`` is unrelated general Catalan carried to
    mitigate catastrophic forgetting (15-20 %), and ``rag_style`` aligns training with how the
    model is actually served — context plus question, answer citing the context.
    """

    QA = "qa"
    EXPLICACIO = "explicacio"
    MULTITURN = "multiturn"
    RESUM = "resum"
    TRADUCCIO = "traduccio"
    NO_HO_SE = "no_ho_se"
    RAG_STYLE = "rag_style"
    ESTIL_ANDORRA = "estil_andorra"
    GENERAL_CA = "general_ca"

    def requires_grounding(self) -> bool:
        """Whether this type must cite the corpus passages it was generated from.

        Grounding is *the* anti-hallucination measure: the generator always receives real
        corpus passages, so an example that cites none was not grounded in anything. Two types
        are exempt by construction — ``general_ca`` is deliberately unrelated to Andorra, and
        ``estil_andorra`` rewrites a text into Andorran register rather than answering from
        sources.
        """
        return self not in {ExampleType.GENERAL_CA, ExampleType.ESTIL_ANDORRA}

    def embeds_source_text(self) -> bool:
        """Whether an example of this type carries corpus text verbatim in its messages.

        ``rag_style`` does by construction: the passage *is* the context. That makes it the one
        type where grounding on a ``no-redistribute`` document is unambiguously a licence
        violation rather than a paraphrase.
        """
        return self is ExampleType.RAG_STYLE


class Split(StrEnum):
    """Train/val/test partition. The test split is frozen and never trained on."""

    TRAIN = "train"
    VAL = "val"
    TEST = "test"


class Role(StrEnum):
    """Chat role. Only these two — a system prompt belongs to serving, not to the data."""

    USER = "user"
    ASSISTANT = "assistant"


class Message(BaseModel):
    """One turn of a conversation (§3.2)."""

    model_config = ConfigDict(extra="forbid")

    role: Role
    content: str = Field(min_length=1)


class DatasetExample(BaseModel):
    """One synthetic training example (ANEXO §3.2).

    ``id`` is a UUID rather than a content hash (unlike §3.1): two examples may legitimately
    have identical text — the same question generated for two taxonomy nodes — and collapsing
    them would silently change the distribution the constraints check.
    """

    model_config = ConfigDict(extra="forbid")

    id: UUID
    messages: list[Message] = Field(min_length=2)
    type: ExampleType
    topic: str = Field(min_length=1)
    grounding_ids: list[str] = Field(default_factory=list)
    generator: str = Field(min_length=1)
    judge_score: float = Field(ge=0.0, le=1.0)
    split: Split

    @model_validator(mode="after")
    def _check_invariants(self) -> Self:
        roles = [message.role for message in self.messages]
        if roles[0] is not Role.USER:
            raise ValueError("a conversation must open with a user message")
        if roles[-1] is not Role.ASSISTANT:
            raise ValueError("a conversation must end with an assistant message")
        expected = [Role.USER if index % 2 == 0 else Role.ASSISTANT for index in range(len(roles))]
        if roles != expected:
            raise ValueError("messages must alternate user/assistant")

        turns = len(self.messages) // 2
        if self.type is ExampleType.MULTITURN and turns < 2:
            raise ValueError("type=multiturn needs at least two user/assistant turns")
        if self.type is not ExampleType.MULTITURN and turns != 1:
            raise ValueError(f"type={self.type.value} must be a single turn; use multiturn")

        if self.type.requires_grounding() and not self.grounding_ids:
            raise ValueError(
                f"type={self.type.value} must cite the corpus passages it was grounded on"
            )
        if self.type is ExampleType.GENERAL_CA and self.grounding_ids:
            raise ValueError(
                "type=general_ca is the anti-forgetting mix, unrelated to Andorra: it must not "
                "cite corpus grounding"
            )
        if len(set(self.grounding_ids)) != len(self.grounding_ids):
            raise ValueError("grounding_ids must not repeat")
        for grounding_id in self.grounding_ids:
            if not _SHA256_HEX.fullmatch(grounding_id):
                raise ValueError(
                    f"grounding_id {grounding_id!r} is not a §3.1 document id "
                    "(64 lowercase hex characters)"
                )
        return self
