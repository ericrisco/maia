"""Indexing and retrieval — PLAN M5.02-M5.03.

*"Qdrant + LlamaIndex + `multilingual-e5-large` embeddings. System prompt: identity, instruction to
cite retrieved sources and to answer "no ho sé" out of context. The legal index has a quarterly
reindexation runbook."*

Four things decided here, two of which are the reason this module is not a thin Qdrant wrapper.

**`multilingual-e5-large` needs its prefixes, and getting them wrong is silent.** E5 models are
trained with ``query:`` and ``passage:`` prefixes, and embedding a question as a passage (or the
reverse) degrades retrieval **without any error** — the vectors stay valid, just measured in the
wrong space. :func:`query_text` and :func:`passage_text` are the only places either prefix is
written, and :func:`check_prefixes` asserts an index was built with the right one.

**The system prompt is data, not a string literal in a handler.** It carries three obligations the
plan states — identity, cite the retrieved sources, answer *"no ho sé"* out of context — and the
third is what M2's whole ``no_ho_se`` type trained for. A prompt assembled ad hoc in the API layer
would drift from what the model was trained to do; :func:`system_prompt` builds it, and
:func:`missing_obligations` is what a contract test can assert against.

**A restricted chunk is retrieved, cited, and not quoted.** M5.01 put the licence on the chunk; this
is where it is used. :func:`context_block` renders the passages for the prompt and, for a public
answer, replaces restricted text with its reference — so the model can say *"segons l'article 5…"*
without the transcript containing text the project may not redistribute (D-0011, D-0037).

**Reindexing is a diff, not a rebuild.** The legal index is reindexed quarterly because consolidated
law changes; :func:`plan_reindex` reports what to add, replace and delete, because a blind rebuild
loses nothing but costs an embedding pass over the whole corpus, and — worse — a *partial* rebuild
that only adds silently leaves superseded articles in the index answering as current law.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Protocol

from maia.rag.chunks import DEFAULT_EMBEDDING_MODEL, RagChunk

#: E5's required prefixes. Not decoration: the model was trained with them.
QUERY_PREFIX = "query: "
PASSAGE_PREFIX = "passage: "

#: The collection the chunks live in.
DEFAULT_COLLECTION = "maia-corpus"

#: How many passages the served prompt carries by default.
DEFAULT_TOP_K = 5

#: What the plan requires the system prompt to establish.
IDENTITY = (
    "Ets MAIA, un assistent especialitzat en Andorra: institucions, dret, geografia, història i "
    "cultura del Principat. Respons en català."
)
CITE_RULE = (
    "Fonamenta cada afirmació en els passatges de context que reps i cita'n la font. Si una "
    "afirmació no surt dels passatges, no la facis."
)
UNKNOWN_RULE = (
    "Si els passatges no contenen la resposta, digues clarament que no ho saps o que no consta. "
    "No inventis dades, dates, xifres ni articles."
)

#: The three obligations, for :func:`missing_obligations`.
OBLIGATIONS = ("identity", "cite", "unknown")


class VectorStore(Protocol):
    """The slice of Qdrant used here. Blocked-by-resource: a running instance."""

    def upsert(self, collection: str, points: Sequence[Mapping[str, object]]) -> None:
        """Insert or replace points by id."""

    def delete(self, collection: str, ids: Sequence[str]) -> None:
        """Remove points by id."""

    def search(
        self, collection: str, vector: Sequence[float], *, limit: int
    ) -> list[Mapping[str, object]]:
        """Nearest points, best first, each carrying its payload."""


class Embedder(Protocol):
    """An embedding model. Blocked-by-resource: downloads weights."""

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        """Embed every text, in order."""


class PrefixError(RuntimeError):
    """Raised when text was embedded with the wrong E5 prefix."""


def query_text(question: str) -> str:
    """A question, prefixed for E5.

    The only place ``query:`` is written. Embedding a question as a passage degrades retrieval with
    no error at all — the vectors are valid, just measured in the wrong space.
    """
    return f"{QUERY_PREFIX}{question.strip()}"


def passage_text(chunk: RagChunk) -> str:
    """A chunk, prefixed for E5. The only place ``passage:`` is written."""
    return f"{PASSAGE_PREFIX}{chunk.text}"


def check_prefixes(texts: Iterable[str], *, expect: str) -> None:
    """Assert every text carries ``expect``.

    Raises:
        PrefixError: naming the first offender. This exists because the failure it catches produces
            a working index that retrieves badly, which is far harder to notice than a crash.
    """
    for text in texts:
        if not text.startswith(expect):
            raise PrefixError(
                f"expected the {expect.strip()!r} prefix but got {text[:40]!r}; embedding a query "
                "as a passage (or the reverse) degrades retrieval with no error"
            )


def to_point(chunk: RagChunk, vector: Sequence[float]) -> dict[str, object]:
    """One Qdrant point: the chunk's id, its vector, and its §3.1 metadata as the payload.

    The **licence travels into the payload**, so the serving layer can decide what to quote
    without a second lookup — see D-0037.
    """
    return {
        "id": chunk.id,
        "vector": list(vector),
        "payload": {
            "doc_id": chunk.doc_id,
            "text": chunk.text,
            "ordinal": chunk.ordinal,
            "source": chunk.source.value,
            "url": chunk.url,
            "license": chunk.license.value,
            "registre": chunk.registre.value,
            "lang": chunk.lang,
            "embedding_model": chunk.embedding_model,
            **({"legal": chunk.legal.model_dump(mode="json")} if chunk.legal else {}),
        },
    }


@dataclass
class IndexReport:
    """What an indexing run wrote."""

    chunks: int = 0
    batches: int = 0
    restricted: int = 0
    model: str = DEFAULT_EMBEDDING_MODEL

    @property
    def restricted_share(self) -> float:
        """Share of the index that may be cited but not quoted publicly."""
        return self.restricted / self.chunks if self.chunks else 0.0


def index_chunks(
    chunks: Sequence[RagChunk],
    embedder: Embedder,
    store: VectorStore,
    *,
    collection: str = DEFAULT_COLLECTION,
    batch_size: int = 64,
) -> IndexReport:
    """Embed and upsert every chunk.

    Raises:
        ValueError: if a chunk was built for a different embedding model than the one indexing it,
            or if the embedder returns the wrong number of vectors. A mixed-model collection returns
            neighbours from two incompatible spaces and looks like poor retrieval quality.
    """
    if batch_size <= 0:
        raise ValueError("batch_size must be positive")
    report = IndexReport(chunks=len(chunks))
    for chunk in chunks:
        if chunk.embedding_model != report.model:
            raise ValueError(
                f"chunk {chunk.id[:16]}… was built for {chunk.embedding_model!r} but this index "
                f"uses {report.model!r}; a mixed-model collection returns neighbours from two "
                "incompatible spaces and reads as poor retrieval quality"
            )
        if chunk.restricted:
            report.restricted += 1

    for start in range(0, len(chunks), batch_size):
        batch = chunks[start : start + batch_size]
        texts = [passage_text(chunk) for chunk in batch]
        check_prefixes(texts, expect=PASSAGE_PREFIX)
        vectors = embedder.embed(texts)
        if len(vectors) != len(batch):
            raise ValueError(
                f"embedder returned {len(vectors)} vectors for {len(batch)} chunk(s) — refusing to "
                "pair chunks with vectors that may not be theirs"
            )
        store.upsert(
            collection,
            [to_point(chunk, vector) for chunk, vector in zip(batch, vectors, strict=True)],
        )
        report.batches += 1
    return report


@dataclass(frozen=True)
class Hit:
    """One retrieved chunk with its score."""

    chunk_id: str
    score: float
    text: str
    url: str
    license: str
    legal: Mapping[str, object] | None = None

    @property
    def restricted(self) -> bool:
        """Whether this hit's text may not be quoted publicly."""
        return self.license == "no-redistribute"

    @property
    def citation(self) -> dict[str, str]:
        """The reference a served answer may show."""
        reference = {"url": self.url}
        if self.legal:
            for key in ("article", "consolidacio_data", "llei"):
                value = self.legal.get(key)
                if value:
                    reference[key] = str(value)
        return reference


def _as_float(value: object) -> float:
    """A score, or ``0.0`` when the store did not report one."""
    return float(value) if isinstance(value, int | float) and not isinstance(value, bool) else 0.0


def to_hit(point: Mapping[str, object]) -> Hit:
    """Read one Qdrant result.

    Raises:
        ValueError: if the payload lacks what a citation needs. A hit that cannot be attributed
            cannot be used, and silently dropping the attribution is how an unsourced answer gets
            served as a sourced one.
    """
    payload = point.get("payload")
    if not isinstance(payload, Mapping):
        raise ValueError(f"result {point.get('id')!r} has no payload")
    missing = [key for key in ("text", "url", "license") if not payload.get(key)]
    if missing:
        raise ValueError(
            f"result {point.get('id')!r} is missing {', '.join(missing)}; a hit that cannot be "
            "attributed cannot be served as a sourced answer"
        )
    legal = payload.get("legal")
    return Hit(
        chunk_id=str(point.get("id", "")),
        score=_as_float(point.get("score")),
        text=str(payload["text"]),
        url=str(payload["url"]),
        license=str(payload["license"]),
        legal=legal if isinstance(legal, Mapping) else None,
    )


def retrieve(
    question: str,
    embedder: Embedder,
    store: VectorStore,
    *,
    collection: str = DEFAULT_COLLECTION,
    top_k: int = DEFAULT_TOP_K,
) -> list[Hit]:
    """Retrieve the ``top_k`` chunks for one question."""
    if not question.strip():
        raise ValueError("an empty question retrieves nothing meaningful")
    if top_k <= 0:
        raise ValueError("top_k must be positive")
    text = query_text(question)
    check_prefixes([text], expect=QUERY_PREFIX)
    vectors = embedder.embed([text])
    if len(vectors) != 1:
        raise ValueError(f"embedder returned {len(vectors)} vectors for one question")
    return [to_hit(point) for point in store.search(collection, vectors[0], limit=top_k)]


def system_prompt(*, extra: str = "") -> str:
    """The served system prompt.

    Assembled here rather than written in the API handler, so it cannot drift from what M2 trained
    the model to do — the *"no ho sé"* obligation is the whole reason that example type exists.
    """
    parts = [IDENTITY, CITE_RULE, UNKNOWN_RULE]
    if extra.strip():
        parts.append(extra.strip())
    return "\n\n".join(parts)


def missing_obligations(prompt: str) -> list[str]:
    """Which of the plan's three obligations a prompt fails to state.

    The predicate a contract test asserts on, so a well-meaning edit that drops the *"no ho sé"*
    instruction fails a test instead of quietly changing how the model behaves out of context.
    """
    missing = []
    if "MAIA" not in prompt:
        missing.append("identity")
    if "cita" not in prompt.lower():
        missing.append("cite")
    if "no ho saps" not in prompt.lower() and "no consta" not in prompt.lower():
        missing.append("unknown")
    return missing


def context_block(hits: Sequence[Hit], *, public: bool = True) -> str:
    """Render retrieved passages for the prompt.

    For a public answer a restricted passage is replaced by its **reference**: the model can still
    say *"segons l'article 5 de la Llei…"* while the transcript never contains text the project may
    not redistribute. The alternative — dropping the passage — would make the model answer *"no ho
    sé"* about something the corpus knows, which is a worse failure than a citation without a quote.
    """
    if not hits:
        return "(cap passatge recuperat)"
    blocks: list[str] = []
    for index, hit in enumerate(hits, start=1):
        reference = ", ".join(f"{key}={value}" for key, value in hit.citation.items())
        if citable_hit(hit, public=public):
            blocks.append(f"[{index}] ({reference})\n{hit.text}")
        else:
            blocks.append(
                f"[{index}] ({reference})\n"
                "(text de llicència restringida: cita la font, no en reprodueixis el contingut)"
            )
    return "\n\n".join(blocks)


def citable_hit(hit: Hit, *, public: bool) -> bool:
    """Whether this hit's text may be quoted — the :func:`citable` rule, for a retrieved hit."""
    return not public or not hit.restricted


@dataclass
class ReindexPlan:
    """What a quarterly reindex should change."""

    added: list[str] = field(default_factory=list)
    replaced: list[str] = field(default_factory=list)
    deleted: list[str] = field(default_factory=list)
    unchanged: int = 0

    @property
    def touched(self) -> int:
        """Points the reindex writes or removes."""
        return len(self.added) + len(self.replaced) + len(self.deleted)


def plan_reindex(current: Sequence[RagChunk], indexed: Mapping[str, str]) -> ReindexPlan:
    """Diff freshly chunked text against what the index holds. ``indexed`` maps chunk id to doc id.

    A diff rather than a rebuild for one reason that matters: an **add-only** refresh leaves
    superseded articles in the index, still answering as current law. Consolidated text changes, so
    the deletions are the part of a quarterly reindex that cannot be skipped.
    """
    plan = ReindexPlan()
    fresh = {chunk.id: chunk for chunk in current}
    for chunk_id in fresh:
        if chunk_id not in indexed:
            plan.added.append(chunk_id)
        else:
            plan.unchanged += 1
    # Ids are content-addressed (M5.01), so a changed article yields a new id and its old one has to
    # go: same document, different chunk id.
    fresh_docs = {chunk.doc_id for chunk in current}
    for chunk_id, doc_id in indexed.items():
        if chunk_id in fresh:
            continue
        if doc_id in fresh_docs:
            plan.replaced.append(chunk_id)
        else:
            plan.deleted.append(chunk_id)
    plan.added.sort()
    plan.replaced.sort()
    plan.deleted.sort()
    return plan


def apply_reindex(
    plan: ReindexPlan,
    current: Sequence[RagChunk],
    embedder: Embedder,
    store: VectorStore,
    *,
    collection: str = DEFAULT_COLLECTION,
) -> IndexReport:
    """Write the plan: index what is new, then remove what it supersedes.

    Deletions happen **after** the writes, so an interrupted reindex leaves the index with both
    versions rather than with neither — stale-and-present is recoverable, missing is not.
    """
    fresh = {chunk.id: chunk for chunk in current}
    report = index_chunks(
        [fresh[chunk_id] for chunk_id in plan.added],
        embedder,
        store,
        collection=collection,
    )
    stale = [*plan.replaced, *plan.deleted]
    if stale:
        store.delete(collection, stale)
    return report


def render_index(report: IndexReport) -> str:
    """Human-readable summary of an indexing run."""
    lines = [
        f"indexed {report.chunks} chunk(s) in {report.batches} batch(es) with {report.model}",
    ]
    if report.restricted:
        lines.append(
            f"  {report.restricted} ({report.restricted_share:.0%}) carry restricted text: "
            "retrievable and citable, with their text withheld from public answers"
        )
    return "\n".join(lines)


def render_reindex(plan: ReindexPlan) -> str:
    """Human-readable summary of a quarterly reindex."""
    lines = [
        f"reindex: +{len(plan.added)} new, ~{len(plan.replaced)} superseded, "
        f"-{len(plan.deleted)} removed, {plan.unchanged} unchanged",
    ]
    if plan.replaced:
        lines.append(
            f"  {len(plan.replaced)} chunk(s) belong to documents that changed; leaving them would "
            "keep superseded articles answering as current law"
        )
    if not plan.touched:
        lines.append("  nothing to do: the index already matches the corpus")
    return "\n".join(lines)
