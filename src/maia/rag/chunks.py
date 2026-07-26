"""The §3.3 RAG chunk, and how documents become chunks — PLAN M5.01.

*"Chunking: **1 chunk = 1 article** for laws (the natural legal retrieval/citation unit); ~512
tokens with 64 overlap for everything else. RAG chunk schema (§3.3): ``{id, doc_id, text,
embedding_model, metadata: inherits Corpus §3.1}``."*

Three decisions live here, and the third is a compliance one that is easy to miss.

**A legal document is already one chunk.** M1.06 split consolidated law by article, so a `juridic`
document *is* an article — splitting it again by token count would cut a citation in half and give a
chunk that answers *"article 5 says…"* with the second half of article 5. :func:`chunk_document`
never splits a document carrying `legal` metadata, however long, and reports the oversized ones
instead of quietly mangling them.

**Overlap exists so a sentence spanning a boundary is retrievable from either side**, which means
a chunk must be *contiguous* text from its document — never a window that skips. The obvious
implementation (slice by index, step by ``size - overlap``) is right; the obvious *bug* is an
overlap at or above the size, which either makes no progress or silently drops text, so it is
refused.

**The chunk carries its licence, and that is what makes the RAG index safe to build.** The index
legitimately contains `no-redistribute` text — that is the whole point of RAG owning facts (D-0011)
— but a *cited* answer that quotes it publishes it. The chunk inherits §3.1's licence so the serving
layer can cite a restricted chunk without quoting it, and :func:`citable` is the predicate that
decides. Losing the licence here would make that impossible downstream and nothing would notice.
"""

from __future__ import annotations

import hashlib
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from typing import Protocol

from pydantic import BaseModel, ConfigDict, Field

from maia.schemas import CorpusDocument, Legal, License, Registre, Source

#: The plan's target chunk size, in tokens.
TARGET_TOKENS = 512

#: The plan's overlap, in tokens.
OVERLAP_TOKENS = 64

#: Softcatalà's recommendation for Catalan.
DEFAULT_EMBEDDING_MODEL = "intfloat/multilingual-e5-large"

#: Characters per token for the default estimate. Catalan runs a little longer than English per
#: token; this is the same order-of-magnitude figure M2.07 uses and is labelled an estimate wherever
#: it shows.
CHARS_PER_TOKEN = 4


class TokenCounter(Protocol):
    """Counts tokens. The seam for the embedding model's own tokenizer."""

    def count(self, text: str) -> int:
        """How many tokens ``text`` is."""


@dataclass(frozen=True)
class CharacterEstimate:
    """Characters over :data:`CHARS_PER_TOKEN`. Crude, and named so.

    Good enough to decide chunk boundaries — a chunk 20 % off target still retrieves — and wrong
    enough that the real tokenizer should replace it before a production index is built.
    """

    chars_per_token: int = CHARS_PER_TOKEN

    def count(self, text: str) -> int:
        """Estimated token count."""
        return max(1, len(text) // self.chars_per_token) if text.strip() else 0


class RagChunk(BaseModel):
    """§3.3: one retrievable unit, with §3.1's metadata inherited.

    ``extra="forbid"`` for the same reason the corpus schema forbids it: a field nobody declared is
    a field nobody validates, and the index is what the served answers are grounded in.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str = Field(min_length=64, max_length=64, pattern=r"^[0-9a-f]{64}$")
    doc_id: str = Field(min_length=64, max_length=64, pattern=r"^[0-9a-f]{64}$")
    text: str = Field(min_length=1)
    embedding_model: str = Field(min_length=1)
    #: Position within the source document, so a mid-document chunk can be located and its
    #: neighbours fetched.
    ordinal: int = Field(ge=0)
    #: Inherited from §3.1. Licence is load-bearing — see the module docstring.
    source: Source
    url: str
    license: License
    registre: Registre
    lang: str = "ca"
    legal: Legal | None = None

    @property
    def restricted(self) -> bool:
        """Whether this chunk's text may not be redistributed."""
        return not self.license.is_public()

    @property
    def citation(self) -> dict[str, str]:
        """What a served answer may show as its source.

        The **reference**, never the text: a restricted chunk can be cited (its URL and article are
        public facts) without quoting the passage it holds.
        """
        reference = {"url": self.url}
        if self.legal is not None:
            reference["article"] = self.legal.article
            reference["consolidacio_data"] = self.legal.consolidacio_data.isoformat()
            if self.legal.llei:
                reference["llei"] = self.legal.llei
        return reference


def citable(chunk: RagChunk, *, public: bool) -> bool:
    """Whether ``chunk``'s **text** may be quoted in this context.

    A restricted chunk is always usable as grounding and always citable as a reference; only its
    text is withheld from a public answer. Getting this backwards either way is a real failure:
    withholding the reference makes answers unverifiable, quoting the text breaks D-0011.
    """
    return not public or not chunk.restricted


def chunk_id(doc_id: str, ordinal: int, text: str) -> str:
    """A content-addressed chunk id.

    Over ``(doc_id, ordinal, text)``, so re-chunking the same document reproduces the same ids and a
    re-index does not duplicate the collection — the same property M2.03 relies on for examples.
    """
    hasher = hashlib.sha256()
    hasher.update(doc_id.encode("utf-8"))
    hasher.update(f"|{ordinal}|".encode())
    hasher.update(text.encode("utf-8"))
    return hasher.hexdigest()


@dataclass
class ChunkReport:
    """What chunking produced, and what it refused to do."""

    documents: int = 0
    chunks: int = 0
    legal_whole: int = 0
    oversized_legal: list[tuple[str, int]] = field(default_factory=list)
    empty: list[str] = field(default_factory=list)

    @property
    def mean_chunks(self) -> float:
        """Chunks per document."""
        return self.chunks / self.documents if self.documents else 0.0


def split_text(
    text: str,
    counter: TokenCounter,
    *,
    target: int = TARGET_TOKENS,
    overlap: int = OVERLAP_TOKENS,
) -> list[str]:
    """Split ``text`` into overlapping, **contiguous** windows of about ``target`` tokens.

    Contiguous because overlap exists so a sentence spanning a boundary is retrievable from either
    side; a window that skipped text would leave that sentence in neither.

    Raises:
        ValueError: if ``overlap`` is not smaller than ``target``. Equal makes no progress and
            larger silently drops text between windows — the same bug in two directions.
    """
    if target <= 0:
        raise ValueError("target must be positive")
    if overlap < 0:
        raise ValueError("overlap cannot be negative")
    if overlap >= target:
        raise ValueError(
            f"overlap {overlap} is not smaller than target {target}: equal makes no progress, and "
            "larger drops the text between windows"
        )
    if not text.strip():
        return []
    if counter.count(text) <= target:
        return [text]

    # Work in characters, converting the token budget through the counter's own ratio so a real
    # tokenizer changes the boundaries rather than being ignored.
    per_token = len(text) / max(1, counter.count(text))
    window = max(1, int(target * per_token))
    step = max(1, int((target - overlap) * per_token))
    # ``while True`` rather than ``while start < len(text)``: the loop always exits at the window
    # that reaches the end, so a second condition would be a branch nothing can take.
    chunks: list[str] = []
    start = 0
    while True:
        piece = text[start : start + window]
        if piece.strip():
            chunks.append(piece)
        if start + window >= len(text):
            return chunks
        start += step


def chunk_document(
    document: CorpusDocument,
    *,
    counter: TokenCounter | None = None,
    embedding_model: str = DEFAULT_EMBEDDING_MODEL,
    target: int = TARGET_TOKENS,
    overlap: int = OVERLAP_TOKENS,
) -> list[RagChunk]:
    """Turn one §3.1 document into §3.3 chunks.

    A document carrying ``legal`` metadata is **never split**: M1.06 already made it one article,
    and the article is the natural retrieval and citation unit. Splitting it by token count would
    cut a citation in half and give a chunk that answers *"article 5 says…"* with the second half
    of article 5.
    """
    tokens = counter or CharacterEstimate()
    pieces = (
        [document.text]
        if document.legal is not None
        else split_text(document.text, tokens, target=target, overlap=overlap)
    )
    return [
        RagChunk(
            id=chunk_id(document.id, ordinal, piece),
            doc_id=document.id,
            text=piece,
            embedding_model=embedding_model,
            ordinal=ordinal,
            source=document.source,
            url=str(document.url),
            license=document.license,
            registre=document.registre,
            lang=document.lang,
            legal=document.legal,
        )
        for ordinal, piece in enumerate(pieces)
    ]


def chunk_corpus(
    documents: Iterable[CorpusDocument],
    *,
    counter: TokenCounter | None = None,
    embedding_model: str = DEFAULT_EMBEDDING_MODEL,
    target: int = TARGET_TOKENS,
    overlap: int = OVERLAP_TOKENS,
) -> tuple[list[RagChunk], ChunkReport]:
    """Chunk a whole corpus, reporting what was left whole and what was refused."""
    tokens = counter or CharacterEstimate()
    report = ChunkReport()
    chunks: list[RagChunk] = []
    for document in documents:
        report.documents += 1
        if not document.text.strip():
            report.empty.append(document.id)
            continue
        produced = chunk_document(
            document,
            counter=tokens,
            embedding_model=embedding_model,
            target=target,
            overlap=overlap,
        )
        if document.legal is not None:
            report.legal_whole += 1
            size = tokens.count(document.text)
            if size > target:
                report.oversized_legal.append((document.id, size))
        chunks.extend(produced)
        report.chunks += len(produced)
    return chunks, report


def render(report: ChunkReport, *, target: int = TARGET_TOKENS) -> str:
    """Human-readable summary of a chunking run."""
    lines = [
        f"chunked {report.documents} document(s) into {report.chunks} chunk(s) "
        f"({report.mean_chunks:.1f} each)",
        f"  {report.legal_whole} legal document(s) kept whole — one article is one chunk, and "
        "splitting one would cut a citation in half",
    ]
    if report.oversized_legal:
        lines.append(
            f"  ⚠ {len(report.oversized_legal)} article(s) exceed the {target}-token target and "
            "were kept whole anyway; they may be truncated by the embedding model:"
        )
        for doc_id, size in sorted(report.oversized_legal, key=lambda item: -item[1])[:5]:
            lines.append(f"    {doc_id[:16]}…: ~{size} tokens")
    if report.empty:
        lines.append(f"  {len(report.empty)} document(s) had no text and produced no chunk")
    lines.append(
        "  token counts are ESTIMATED from characters unless a real tokenizer was supplied"
    )
    return "\n".join(lines)


def restricted_share(chunks: Sequence[RagChunk]) -> float:
    """Share of the index that may not be quoted publicly.

    Worth knowing before serving: a high share means many answers will be able to cite a source
    without showing it, which is correct behaviour and looks evasive to a user.
    """
    return sum(1 for chunk in chunks if chunk.restricted) / len(chunks) if chunks else 0.0
