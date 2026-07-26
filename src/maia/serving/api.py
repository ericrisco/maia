"""The inference API — PLAN M5.04, §4 of the technical annex.

*"FastAPI in front of vLLM, **OpenAI-compatible** so standard clients can point at it… The
FastAPI-generated **OpenAPI** is the canonical spec; the exported JSON is committed at
`docs/openapi.json`, and contract tests run against it."*

OpenAI-compatibility is a contract with software nobody here controls, which decides most of the
shape: the request and response models mirror the fields the OpenAI SDK sends and reads, including
the ones this service does not use, because a client that sends `temperature` must not get a 422.

Three decisions are MAIA's own.

**`sources` is a top-level response field, not prose in the answer.** *"RAG responses include
`sources: [{url, llei?, article?, consolidacio_data?}]`"* — a client that wants to show citations
should not have to parse them out of Catalan text. The field is additive, so an OpenAI client
ignores it and a MAIA client reads it.

**A restricted passage is cited in `sources` and never quoted in the prompt.** The rule from D-0037
and D-0038 reaches the boundary here: the response can attribute an answer to `no-redistribute` text
without the served transcript containing it. This is the last place that can go wrong, and it is the
place where getting it wrong is public.

**`/health` reports the index, not just the process.** A service whose model is loaded and whose
Qdrant collection is empty answers every question with *"no ho sé"* while returning 200 — a green
health check on a broken system is worse than a red one, so the index is part of the answer.

vLLM and Qdrant are **blocked-by-resource**; :class:`ChatBackend` and the retrieval seams from M5.02
are injected through :func:`create_app`, so the whole contract is testable with `TestClient` and no
GPU.
"""

from __future__ import annotations

import time
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Annotated, Literal, Protocol

from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

from maia.rag.index import (
    DEFAULT_COLLECTION,
    DEFAULT_TOP_K,
    Embedder,
    Hit,
    VectorStore,
    context_block,
    retrieve,
    system_prompt,
)

#: The model id this service answers as, in OpenAI's ``model`` field.
SERVED_MODEL = "maia-12b"

#: Requests per minute per key. Deliberately low: the demo runs on serverless GPU, where an
#: unthrottled endpoint is a cost incident rather than a performance one.
RATE_LIMIT_PER_MINUTE = 20


class ChatBackend(Protocol):
    """vLLM behind an OpenAI-compatible surface. Blocked-by-resource: a GPU and loaded weights."""

    def complete(
        self, messages: Sequence[dict[str, str]], *, max_tokens: int, temperature: float
    ) -> str:
        """Generate an assistant turn."""

    @property
    def ready(self) -> bool:
        """Whether the model is loaded and can serve."""


class Message(BaseModel):
    """One chat message, in OpenAI's shape."""

    model_config = ConfigDict(extra="forbid")

    role: Literal["system", "user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    """``POST /v1/chat/completions``, OpenAI-compatible.

    The unused fields are here on purpose: an OpenAI client sends them, and rejecting a request for
    carrying ``top_p`` would break the compatibility that is the whole point. They are accepted and,
    where this service cannot honour them, ignored — which is what an OpenAI-compatible proxy does.
    """

    model_config = ConfigDict(extra="forbid")

    model: str = SERVED_MODEL
    messages: list[Message] = Field(min_length=1)
    max_tokens: Annotated[int, Field(ge=1, le=4_096)] = 512
    temperature: Annotated[float, Field(ge=0.0, le=2.0)] = 0.3
    top_p: Annotated[float, Field(ge=0.0, le=1.0)] = 1.0
    stream: bool = False
    #: MAIA's own parameter, defaulting to on as the plan specifies.
    rag: bool = True

    @property
    def question(self) -> str:
        """The text retrieval is run against: the last user turn.

        The last, not the concatenation: retrieving on the whole history drags every earlier topic
        into the query vector, and a follow-up question retrieves for the conversation rather than
        for itself.
        """
        for message in reversed(self.messages):
            if message.role == "user":
                return message.content
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="no user message to answer",
        )


class Source(BaseModel):
    """One citation. ``llei``/``article``/``consolidacio_data`` are legal-only."""

    model_config = ConfigDict(extra="forbid")

    url: str
    llei: str | None = None
    article: str | None = None
    consolidacio_data: str | None = None
    #: Whether the passage's text was withheld from the prompt. Reported so a client can explain a
    #: thinner answer rather than looking evasive.
    text_withheld: bool = False


class Choice(BaseModel):
    """OpenAI's choice envelope."""

    model_config = ConfigDict(extra="forbid")

    index: int = 0
    message: Message
    finish_reason: Literal["stop", "length"] = "stop"


class ChatResponse(BaseModel):
    """``POST /v1/chat/completions`` response, OpenAI-compatible plus ``sources``."""

    model_config = ConfigDict(extra="forbid")

    id: str
    object: Literal["chat.completion"] = "chat.completion"
    created: int
    model: str
    choices: list[Choice]
    #: MAIA's addition: an OpenAI client ignores it, a MAIA client reads it.
    sources: list[Source] = Field(default_factory=list)


class SearchRequest(BaseModel):
    """``POST /rag/search`` — retrieval without generation, for debugging."""

    model_config = ConfigDict(extra="forbid")

    query: str = Field(min_length=1)
    top_k: Annotated[int, Field(ge=1, le=50)] = DEFAULT_TOP_K


class SearchHit(BaseModel):
    """One retrieved chunk, as the debug endpoint returns it."""

    model_config = ConfigDict(extra="forbid")

    chunk_id: str
    score: float
    text: str | None
    source: Source


class SearchResponse(BaseModel):
    """``POST /rag/search`` response."""

    model_config = ConfigDict(extra="forbid")

    query: str
    hits: list[SearchHit]


class Health(BaseModel):
    """``GET /health`` — model **and** index."""

    model_config = ConfigDict(extra="forbid")

    status: Literal["ok", "degraded"]
    model: str
    model_ready: bool
    index_ready: bool
    indexed_chunks: int
    detail: str = ""


def to_source(hit: Hit, *, public: bool) -> Source:
    """One citation from a hit, marking whether its text was withheld."""
    reference = hit.citation
    return Source(
        url=reference["url"],
        llei=reference.get("llei"),
        article=reference.get("article"),
        consolidacio_data=reference.get("consolidacio_data"),
        text_withheld=public and hit.restricted,
    )


@dataclass
class RateLimiter:
    """A fixed-window limiter, per key.

    Fixed window rather than a sliding one: this protects a *cost* budget on serverless GPU, where
    being twice as generous for one second at a window boundary does not matter, and a simpler
    limiter has fewer ways to be wrong.
    """

    limit: int = RATE_LIMIT_PER_MINUTE
    window_seconds: float = 60.0
    clock: object = None
    _counts: dict[tuple[str, int], int] = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        self._counts = {}

    def _now(self) -> float:
        return time.monotonic() if self.clock is None else float(self.clock())  # type: ignore[operator]

    def allow(self, key: str) -> bool:
        """Whether ``key`` may make another request in the current window."""
        bucket = (key, int(self._now() // self.window_seconds))
        self._counts[bucket] = self._counts.get(bucket, 0) + 1
        return self._counts[bucket] <= self.limit


@dataclass
class Deps:
    """Everything the app needs, injected so the contract is testable without a GPU."""

    backend: ChatBackend
    embedder: Embedder
    store: VectorStore
    api_key: str
    collection: str = DEFAULT_COLLECTION
    public: bool = True
    limiter: RateLimiter | None = None
    indexed_chunks: int = 0

    def __post_init__(self) -> None:
        if not self.api_key:
            raise ValueError(
                "an API key is required even for the demo: the endpoint runs on serverless GPU, so "
                "an open one is a cost incident waiting to happen"
            )
        if self.limiter is None:
            self.limiter = RateLimiter()


def create_app(deps: Deps) -> FastAPI:
    """Build the service.

    Every backend is injected, so the OpenAPI contract and every rule below are exercised by
    ``TestClient`` with no GPU, no Qdrant and no network.
    """
    app = FastAPI(
        title="MAIA inference API",
        version="1.0.0",
        description=(
            "OpenAI-compatible chat completions over MAIA, with Andorran-corpus RAG. Responses "
            "carry a `sources` array; passages under a no-redistribute licence are cited but not "
            "quoted."
        ),
    )

    def authorise(authorization: str | None = Header(default=None)) -> None:
        """Bearer auth plus the rate limit, declared on the routes that need it.

        The key is compared in constant time: a short-circuiting comparison leaks its prefix to
        anyone who can time the endpoint.
        """
        import hmac

        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="a bearer token is required",
                headers={"WWW-Authenticate": "Bearer"},
            )
        presented = authorization.removeprefix("Bearer ").strip()
        if not hmac.compare_digest(presented, deps.api_key):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid API key")
        assert deps.limiter is not None  # set in __post_init__
        if not deps.limiter.allow(presented):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"rate limit is {deps.limiter.limit} requests per minute",
            )

    @app.get("/health", response_model=Health)
    def health() -> Health:
        """Model **and** index.

        A loaded model with an empty collection answers every question with *"no ho sé"* while
        returning 200, so a health check that only looked at the process would be green on a broken
        system.
        """
        index_ready = deps.indexed_chunks > 0
        ready = deps.backend.ready and index_ready
        detail = ""
        if not deps.backend.ready:
            detail = "the model is not loaded"
        elif not index_ready:
            detail = (
                "the model is loaded but the index is empty, so every answer would be "
                '"no ho sé" — this is not a healthy service'
            )
        return Health(
            status="ok" if ready else "degraded",
            model=SERVED_MODEL,
            model_ready=deps.backend.ready,
            index_ready=index_ready,
            indexed_chunks=deps.indexed_chunks,
            detail=detail,
        )

    @app.post("/rag/search", response_model=SearchResponse, dependencies=[Depends(authorise)])
    def search(request: SearchRequest) -> SearchResponse:
        """Retrieval without generation.

        Restricted text is ``null`` rather than absent, so a client can tell *"this chunk exists and
        you may not see its text"* from *"there is no such chunk"*.
        """
        hits = retrieve(
            request.query,
            deps.embedder,
            deps.store,
            collection=deps.collection,
            top_k=request.top_k,
        )
        return SearchResponse(
            query=request.query,
            hits=[
                SearchHit(
                    chunk_id=hit.chunk_id,
                    score=hit.score,
                    text=None if deps.public and hit.restricted else hit.text,
                    source=to_source(hit, public=deps.public),
                )
                for hit in hits
            ],
        )

    @app.post(
        "/v1/chat/completions", response_model=ChatResponse, dependencies=[Depends(authorise)]
    )
    def chat(request: ChatRequest) -> ChatResponse:
        """OpenAI-compatible chat completions, with RAG on by default."""
        if request.stream:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="streaming is not implemented; send stream=false",
            )
        hits: list[Hit] = []
        messages: list[dict[str, str]] = [{"role": "system", "content": system_prompt()}]
        if request.rag:
            hits = retrieve(
                request.question,
                deps.embedder,
                deps.store,
                collection=deps.collection,
                top_k=DEFAULT_TOP_K,
            )
            messages.append(
                {
                    "role": "system",
                    "content": "Context recuperat:\n\n" + context_block(hits, public=deps.public),
                }
            )
        messages.extend(
            {"role": message.role, "content": message.content} for message in request.messages
        )
        answer = deps.backend.complete(
            messages, max_tokens=request.max_tokens, temperature=request.temperature
        )
        return ChatResponse(
            id=f"chatcmpl-{int(time.time() * 1000)}",
            created=int(time.time()),
            model=SERVED_MODEL,
            choices=[Choice(message=Message(role="assistant", content=answer))],
            sources=[to_source(hit, public=deps.public) for hit in hits],
        )

    return app


def export_openapi(app: FastAPI) -> dict[str, object]:
    """The canonical spec, for committing at ``docs/openapi.json``.

    The plan makes the generated OpenAPI authoritative, so it is exported from the app rather than
    maintained by hand — a hand-written spec is a second source of truth that drifts.
    """
    schema: dict[str, object] = app.openapi()
    return schema
