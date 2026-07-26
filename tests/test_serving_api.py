"""Contract tests for the inference API (PLAN M5.04, annex §4)."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from maia.serving.api import (
    RATE_LIMIT_PER_MINUTE,
    SERVED_MODEL,
    ChatRequest,
    Deps,
    Message,
    RateLimiter,
    create_app,
    export_openapi,
)

KEY = "maia-test-key"
AUTH = {"Authorization": f"Bearer {KEY}"}
TEXT = "El comú de la parròquia gestiona el territori."
RESTRICTED_TEXT = "Transcripció de ràdio que no es pot redistribuir."


@dataclass
class FakeBackend:
    answer: str = "Vint-i-vuit consellers generals."
    ready: bool = True
    seen: list[Sequence[Mapping[str, str]]] = field(default_factory=list)

    def complete(
        self, messages: Sequence[dict[str, str]], *, max_tokens: int, temperature: float
    ) -> str:
        self.seen.append(list(messages))
        return self.answer


class FakeEmbedder:
    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        return [[0.1, 0.2, 0.3, 0.4] for _ in texts]


def point(
    *, text: str = TEXT, licence: str = "public-official", legal: bool = True
) -> dict[str, object]:
    payload: dict[str, object] = {
        "text": text,
        "url": "https://www.portaljuridicandorra.ad/llei/exemple",
        "license": licence,
    }
    if legal:
        payload["legal"] = {
            "article": "5",
            "consolidacio_data": "2024-03-01",
            "llei": "Llei 9/2003",
        }
    return {"id": "a" * 64, "score": 0.88, "payload": payload}


@dataclass
class FakeStore:
    results: list[Mapping[str, object]] = field(default_factory=lambda: [point()])
    limits: list[int] = field(default_factory=list)

    def upsert(self, collection: str, points: Sequence[Mapping[str, object]]) -> None:
        pass

    def delete(self, collection: str, ids: Sequence[str]) -> None:
        pass

    def search(
        self, collection: str, vector: Sequence[float], *, limit: int
    ) -> list[Mapping[str, object]]:
        self.limits.append(limit)
        return self.results[:limit]


def client(**overrides: object) -> tuple[TestClient, Deps]:
    settings = {
        "backend": FakeBackend(),
        "embedder": FakeEmbedder(),
        "store": FakeStore(),
        "api_key": KEY,
        "indexed_chunks": 1_000,
        **overrides,
    }
    deps = Deps(**settings)  # type: ignore[arg-type]
    return TestClient(create_app(deps)), deps


# ─────────────────────────────────────────────────────────────
# OpenAI compatibility
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_three_contract_endpoints_exist() -> None:
    _, deps = client()
    spec = export_openapi(create_app(deps))
    paths = spec["paths"]
    assert isinstance(paths, dict)
    assert sorted(paths) == ["/health", "/rag/search", "/v1/chat/completions"]


@pytest.mark.unit
def test_an_openai_shaped_request_is_accepted() -> None:
    api, _ = client()
    response = api.post(
        "/v1/chat/completions",
        headers=AUTH,
        json={
            "model": SERVED_MODEL,
            "messages": [{"role": "user", "content": "Quants consellers hi ha?"}],
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["object"] == "chat.completion"
    assert body["choices"][0]["message"]["role"] == "assistant"
    assert body["model"] == SERVED_MODEL


@pytest.mark.unit
def test_parameters_this_service_cannot_honour_do_not_break_the_client() -> None:
    """A client that sends top_p must not get a 422 — that is what compatibility means."""
    api, _ = client()
    response = api.post(
        "/v1/chat/completions",
        headers=AUTH,
        json={
            "messages": [{"role": "user", "content": "Hola?"}],
            "temperature": 0.7,
            "top_p": 0.9,
            "max_tokens": 128,
        },
    )
    assert response.status_code == 200


@pytest.mark.unit
def test_streaming_is_refused_explicitly_rather_than_ignored() -> None:
    """Silently returning a non-stream response to stream=true hangs the client."""
    api, _ = client()
    response = api.post(
        "/v1/chat/completions",
        headers=AUTH,
        json={"messages": [{"role": "user", "content": "Hola?"}], "stream": True},
    )
    assert response.status_code == 400
    assert "streaming is not implemented" in response.json()["detail"]


@pytest.mark.unit
def test_an_unknown_field_is_rejected() -> None:
    api, _ = client()
    response = api.post(
        "/v1/chat/completions",
        headers=AUTH,
        json={"messages": [{"role": "user", "content": "Hola?"}], "nonsense": 1},
    )
    assert response.status_code == 422


@pytest.mark.unit
def test_retrieval_runs_on_the_last_user_turn_not_the_whole_history() -> None:
    """Retrieving on the concatenation drags every earlier topic into the query vector."""
    request = ChatRequest(
        messages=[
            Message(role="user", content="Parla'm de les falles."),
            Message(role="assistant", content="Són una tradició del solstici."),
            Message(role="user", content="I el Consell General?"),
        ]
    )
    assert request.question == "I el Consell General?"


@pytest.mark.unit
def test_a_request_with_no_user_turn_is_refused() -> None:
    api, _ = client()
    response = api.post(
        "/v1/chat/completions",
        headers=AUTH,
        json={"messages": [{"role": "assistant", "content": "Hola!"}]},
    )
    assert response.status_code == 400
    assert "no user message" in response.json()["detail"]


# ─────────────────────────────────────────────────────────────
# sources is a field, not prose
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_rag_answer_carries_structured_sources() -> None:
    """A client should not have to parse citations out of Catalan text."""
    api, _ = client()
    body = api.post(
        "/v1/chat/completions",
        headers=AUTH,
        json={"messages": [{"role": "user", "content": "Què diu l'article 5?"}]},
    ).json()
    assert body["sources"] == [
        {
            "url": "https://www.portaljuridicandorra.ad/llei/exemple",
            "llei": "Llei 9/2003",
            "article": "5",
            "consolidacio_data": "2024-03-01",
            "text_withheld": False,
        }
    ]


@pytest.mark.unit
def test_rag_can_be_turned_off_and_then_there_are_no_sources() -> None:
    api, deps = client()
    body = api.post(
        "/v1/chat/completions",
        headers=AUTH,
        json={"messages": [{"role": "user", "content": "Hola?"}], "rag": False},
    ).json()
    assert body["sources"] == []
    assert isinstance(deps.store, FakeStore)
    assert deps.store.limits == []


@pytest.mark.unit
def test_rag_is_on_by_default() -> None:
    api, deps = client()
    api.post(
        "/v1/chat/completions", headers=AUTH, json={"messages": [{"role": "user", "content": "Q?"}]}
    )
    assert isinstance(deps.store, FakeStore)
    assert deps.store.limits


@pytest.mark.unit
def test_the_system_prompt_and_the_context_reach_the_backend() -> None:
    api, deps = client()
    api.post(
        "/v1/chat/completions", headers=AUTH, json={"messages": [{"role": "user", "content": "Q?"}]}
    )
    assert isinstance(deps.backend, FakeBackend)
    sent = deps.backend.seen[0]
    assert sent[0]["role"] == "system"
    assert "MAIA" in sent[0]["content"]
    assert "Context recuperat" in sent[1]["content"]
    assert TEXT in sent[1]["content"]
    assert sent[-1]["content"] == "Q?"


# ─────────────────────────────────────────────────────────────
# Restricted text at the public boundary
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_restricted_text_is_cited_but_never_sent_in_the_prompt() -> None:
    """The last place this can go wrong, and the place where getting it wrong is public."""
    store = FakeStore(results=[point(text=RESTRICTED_TEXT, licence="no-redistribute")])
    api, deps = client(store=store)
    body = api.post(
        "/v1/chat/completions",
        headers=AUTH,
        json={"messages": [{"role": "user", "content": "Q?"}]},
    ).json()
    assert body["sources"][0]["text_withheld"] is True
    assert body["sources"][0]["article"] == "5"
    assert isinstance(deps.backend, FakeBackend)
    assert RESTRICTED_TEXT not in json.dumps(deps.backend.seen[0], ensure_ascii=False)


@pytest.mark.unit
def test_a_private_deployment_may_use_the_restricted_text() -> None:
    store = FakeStore(results=[point(text=RESTRICTED_TEXT, licence="no-redistribute")])
    api, deps = client(store=store, public=False)
    body = api.post(
        "/v1/chat/completions",
        headers=AUTH,
        json={"messages": [{"role": "user", "content": "Q?"}]},
    ).json()
    assert body["sources"][0]["text_withheld"] is False
    assert isinstance(deps.backend, FakeBackend)
    assert RESTRICTED_TEXT in json.dumps(deps.backend.seen[0], ensure_ascii=False)


@pytest.mark.unit
def test_search_returns_null_text_for_restricted_chunks() -> None:
    """So a client can tell "you may not see this" from "there is no such chunk"."""
    store = FakeStore(results=[point(text=RESTRICTED_TEXT, licence="no-redistribute")])
    api, _ = client(store=store)
    body = api.post("/rag/search", headers=AUTH, json={"query": "Q?"}).json()
    assert body["hits"][0]["text"] is None
    assert body["hits"][0]["source"]["text_withheld"] is True
    assert body["hits"][0]["chunk_id"]


@pytest.mark.unit
def test_search_returns_the_text_of_public_chunks() -> None:
    api, _ = client()
    body = api.post("/rag/search", headers=AUTH, json={"query": "Q?", "top_k": 3}).json()
    assert body["hits"][0]["text"] == TEXT
    assert body["query"] == "Q?"


@pytest.mark.unit
def test_search_honours_top_k() -> None:
    api, deps = client()
    api.post("/rag/search", headers=AUTH, json={"query": "Q?", "top_k": 7})
    assert isinstance(deps.store, FakeStore)
    assert deps.store.limits == [7]


@pytest.mark.unit
def test_an_empty_search_query_is_rejected() -> None:
    api, _ = client()
    assert api.post("/rag/search", headers=AUTH, json={"query": ""}).status_code == 422


# ─────────────────────────────────────────────────────────────
# Health reports the index
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_health_is_ok_when_the_model_and_the_index_are_both_ready() -> None:
    api, _ = client()
    body = api.get("/health").json()
    assert body["status"] == "ok"
    assert body["model_ready"] and body["index_ready"]
    assert body["indexed_chunks"] == 1_000


@pytest.mark.unit
def test_an_empty_index_is_degraded_even_with_a_loaded_model() -> None:
    """A green check on a system that answers everything "no ho sé" is worse than a red one."""
    api, _ = client(indexed_chunks=0)
    body = api.get("/health").json()
    assert body["status"] == "degraded"
    assert body["model_ready"] and not body["index_ready"]
    assert "not a healthy service" in body["detail"]


@pytest.mark.unit
def test_an_unloaded_model_is_degraded() -> None:
    api, _ = client(backend=FakeBackend(ready=False))
    body = api.get("/health").json()
    assert body["status"] == "degraded"
    assert "the model is not loaded" in body["detail"]


@pytest.mark.unit
def test_health_needs_no_api_key() -> None:
    """A probe that needs a secret is a probe that will be configured wrong."""
    api, _ = client()
    assert api.get("/health").status_code == 200


# ─────────────────────────────────────────────────────────────
# Auth and rate limiting
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_request_without_a_token_is_rejected() -> None:
    api, _ = client()
    response = api.post(
        "/v1/chat/completions", json={"messages": [{"role": "user", "content": "Q?"}]}
    )
    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"


@pytest.mark.unit
def test_a_wrong_token_is_rejected() -> None:
    api, _ = client()
    response = api.post(
        "/v1/chat/completions",
        headers={"Authorization": "Bearer wrong"},
        json={"messages": [{"role": "user", "content": "Q?"}]},
    )
    assert response.status_code == 401


@pytest.mark.unit
def test_a_malformed_authorisation_header_is_rejected() -> None:
    api, _ = client()
    assert (
        api.post("/rag/search", headers={"Authorization": KEY}, json={"query": "Q?"}).status_code
        == 401
    )


@pytest.mark.unit
def test_a_service_without_an_api_key_refuses_to_be_built() -> None:
    """An open endpoint on serverless GPU is a cost incident waiting to happen."""
    with pytest.raises(ValueError, match="cost incident"):
        Deps(backend=FakeBackend(), embedder=FakeEmbedder(), store=FakeStore(), api_key="")


@pytest.mark.unit
def test_requests_beyond_the_limit_are_throttled() -> None:
    api, _ = client(limiter=RateLimiter(limit=2, clock=lambda: 0.0))
    payload = {"messages": [{"role": "user", "content": "Q?"}]}
    assert api.post("/v1/chat/completions", headers=AUTH, json=payload).status_code == 200
    assert api.post("/v1/chat/completions", headers=AUTH, json=payload).status_code == 200
    third = api.post("/v1/chat/completions", headers=AUTH, json=payload)
    assert third.status_code == 429
    assert "requests per minute" in third.json()["detail"]


@pytest.mark.unit
def test_the_window_resets() -> None:
    # One clock read per request.
    ticks = iter([0.0, 120.0])
    api, _ = client(limiter=RateLimiter(limit=1, clock=lambda: next(ticks)))
    payload = {"messages": [{"role": "user", "content": "Q?"}]}
    assert api.post("/v1/chat/completions", headers=AUTH, json=payload).status_code == 200
    assert api.post("/v1/chat/completions", headers=AUTH, json=payload).status_code == 200


@pytest.mark.unit
def test_the_default_limit_is_conservative() -> None:
    """This protects a cost budget, not a latency one."""
    assert RATE_LIMIT_PER_MINUTE == 20
    limiter = RateLimiter(clock=lambda: 0.0)
    assert all(limiter.allow("k") for _ in range(RATE_LIMIT_PER_MINUTE))
    assert not limiter.allow("k")


@pytest.mark.unit
def test_limits_are_per_key() -> None:
    limiter = RateLimiter(limit=1, clock=lambda: 0.0)
    assert limiter.allow("first")
    assert limiter.allow("second")
    assert not limiter.allow("first")


# ─────────────────────────────────────────────────────────────
# The canonical spec
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_exported_spec_documents_the_sources_field(tmp_path: Path) -> None:
    """The generated OpenAPI is authoritative, so `sources` has to be in it."""
    _, deps = client()
    spec = export_openapi(create_app(deps))
    components = spec["components"]
    assert isinstance(components, dict)
    schemas = components["schemas"]
    assert "sources" in schemas["ChatResponse"]["properties"]
    assert "rag" in schemas["ChatRequest"]["properties"]
    assert "text_withheld" in schemas["Source"]["properties"]
    # It round-trips as JSON, which is what gets committed at docs/openapi.json.
    path = tmp_path / "openapi.json"
    path.write_text(json.dumps(spec, indent=2), encoding="utf-8")
    reloaded = json.loads(path.read_text(encoding="utf-8"))
    assert reloaded["info"]["title"] == "MAIA inference API"


@pytest.mark.unit
def test_the_committed_spec_matches_the_app() -> None:
    """`docs/openapi.json` is the canonical spec, so it must not drift from the code.

    Without this the committed file becomes documentation of a service that no longer exists — which
    is worse than no file, because clients are generated from it.
    """
    committed = Path(__file__).resolve().parents[1] / "docs" / "openapi.json"
    assert committed.is_file(), "run the export in the M5.04 PR description to regenerate it"
    _, deps = client(api_key="placeholder")
    current = export_openapi(create_app(deps))
    assert json.loads(committed.read_text(encoding="utf-8")) == current, (
        "docs/openapi.json is stale; regenerate it — it is the spec clients are generated from"
    )
