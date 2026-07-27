"""Tests for the RAG demo UI (PLAN M5.07, DoD-F5).

Gradio is an optional dependency and is not installed in CI. The rules worth testing live in the
pure functions; :func:`build_ui` is exercised against a stand-in module injected into
``sys.modules``, which also checks that the toggle is actually wired to the handler.
"""

from __future__ import annotations

import sys
import types
from typing import Any

import pytest

from maia.serving.demo import (
    DISCLAIMER,
    EXAMPLES,
    RAG_OFF_WARNING,
    HttpChatClient,
    answer,
    build_ui,
    main,
    render_sources,
)

LEGAL_SOURCE = {
    "url": "https://portaljuridicandorra.ad/llei/12-2004",
    "llei": "Llei 12/2004",
    "article": "Article 5",
    "consolidacio_data": "2024-03-01",
    "text_withheld": False,
}


class FakeClient:
    """A :class:`ChatClient` that records how it was called."""

    def __init__(self, reply: str = "Resposta.", sources: list[dict[str, Any]] | None = None):
        self.reply = reply
        self.sources = sources if sources is not None else [LEGAL_SOURCE]
        self.calls: list[bool] = []

    def ask(self, question: str, *, rag: bool) -> tuple[str, list[dict[str, Any]]]:
        self.calls.append(rag)
        return self.reply, self.sources


class BoomClient:
    def __init__(self, message: str) -> None:
        self.message = message

    def ask(self, question: str, *, rag: bool) -> tuple[str, list[dict[str, Any]]]:
        raise RuntimeError(self.message)


# ── the toggle ───────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_turning_rag_off_warns_that_citable_detail_is_not_in_the_weights() -> None:
    """The reason this toggle is a safety control and not a demo trick. D8 keeps article numbers,
    amounts and deadlines *deliberately* out of the weights, so RAG-off is the model answering from
    memory it was specifically not given — fluently, and wrong in the way that matters most."""
    off = answer(FakeClient(), "Quin és el tipus general de l'IGI?", rag=False)
    assert off.warning == RAG_OFF_WARNING
    assert "D8" in off.warning
    assert "fora dels pesos" in off.warning

    on = answer(FakeClient(), "Quin és el tipus general de l'IGI?", rag=True)
    assert on.warning == ""


@pytest.mark.unit
def test_rag_off_hides_the_sources_box_rather_than_emptying_it() -> None:
    """An empty "Fonts" panel invites the reader to conclude the model searched and found nothing,
    which is the opposite of what happened."""
    off = answer(FakeClient(), "pregunta", rag=False)
    assert off.sources_markdown == ""
    assert off.ok


@pytest.mark.unit
def test_the_toggle_reaches_the_client() -> None:
    client = FakeClient()
    answer(client, "p", rag=True)
    answer(client, "p", rag=False)
    assert client.calls == [True, False]


# ── citations ────────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_legal_citation_keeps_its_law_and_article() -> None:
    """A citation without an article number is not one anyone can follow."""
    rendered = render_sources([LEGAL_SOURCE])
    assert "Llei 12/2004 — Article 5" in rendered
    assert "(https://portaljuridicandorra.ad/llei/12-2004)" in rendered
    assert "text consolidat a 2024-03-01" in rendered


@pytest.mark.unit
def test_a_withheld_passage_reads_as_a_citation_not_as_evasion() -> None:
    """D-0037/38: a no-redistribute passage is cited but never quoted into the prompt, so the
    answer built on it is thinner. Unexplained, the model looks like it is dodging."""
    rendered = render_sources([{**LEGAL_SOURCE, "text_withheld": True}])
    assert "llicència" in rendered
    assert "no reproduït" in rendered


@pytest.mark.unit
def test_a_source_with_only_a_url_still_renders() -> None:
    rendered = render_sources([{"url": "https://govern.ad/x"}])
    assert "[https://govern.ad/x](https://govern.ad/x)" in rendered


@pytest.mark.unit
def test_a_source_with_no_url_does_not_render_a_broken_link() -> None:
    assert render_sources([{"llei": "Constitució"}]) == "**Fonts:**\n\n1. Constitució"


@pytest.mark.unit
def test_no_sources_says_so() -> None:
    assert "Cap font" in render_sources([])


# ── failure is the normal state of a serverless demo ─────────────────────────


@pytest.mark.unit
@pytest.mark.parametrize(
    ("raised", "expected"),
    [
        ("401 Unauthorized", "MAIA_API_KEY"),
        ("429 rate limit exceeded", "espera un minut"),
        ("Read timed out", "~20 s"),
        ("Connection refused", "desplegat"),
        ("something nobody predicted", "inesperat"),
    ],
)
def test_every_transport_failure_becomes_a_sentence(raised: str, expected: str) -> None:
    """On serverless these are normal states, not exceptional ones. A traceback in the UI is the
    demo failing twice."""
    reply = answer(BoomClient(raised), "pregunta", rag=True)
    assert not reply.ok
    assert expected in reply.answer
    assert reply.sources_markdown == ""


@pytest.mark.unit
def test_the_timeout_message_explains_the_cold_start() -> None:
    """The single most likely thing to go wrong in front of an audience, and the one the viewer
    will otherwise read as the model being broken."""
    reply = answer(BoomClient("Read timed out"), "pregunta", rag=True)
    assert "arrencar el contenidor" in reply.answer


@pytest.mark.unit
def test_an_empty_question_is_refused_before_spending_a_gpu_call() -> None:
    client = FakeClient()
    reply = answer(client, "   ", rag=True)
    assert not reply.ok
    assert client.calls == []


@pytest.mark.unit
def test_a_failure_still_carries_the_rag_off_warning() -> None:
    """The warning is about the configuration, not about the answer: it must not disappear because
    the request happened to fail."""
    assert answer(BoomClient("boom"), "p", rag=False).warning == RAG_OFF_WARNING


# ── the UI shell ─────────────────────────────────────────────────────────────


class _Widget:
    """Every Gradio component the demo uses, recording what it was given."""

    def __init__(self, **kwargs: Any) -> None:
        self.kwargs = kwargs
        self.clicked: dict[str, Any] = {}

    def click(self, fn: Any, **kwargs: Any) -> None:
        self.clicked = {"fn": fn, **kwargs}


class _Blocks:
    def __init__(self, **kwargs: Any) -> None:
        self.kwargs = kwargs

    def __enter__(self) -> _Blocks:
        return self

    def __exit__(self, *exc: object) -> None:
        return None


def _fake_gradio(monkeypatch: pytest.MonkeyPatch) -> tuple[types.ModuleType, list[_Widget]]:
    made: list[_Widget] = []

    def component(**kwargs: Any) -> _Widget:
        widget = _Widget(**kwargs)
        made.append(widget)
        return widget

    module = types.ModuleType("gradio")
    module.Blocks = _Blocks  # type: ignore[attr-defined]
    for name in ("Markdown", "Checkbox", "Textbox", "Button", "Examples"):
        setattr(module, name, lambda *args, **kwargs: component(args=args, **kwargs))
    module.update = lambda **kwargs: {"update": kwargs}  # type: ignore[attr-defined]
    module._made = made  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "gradio", module)
    return module, made


@pytest.mark.unit
def test_build_ui_wires_the_toggle_to_the_handler(monkeypatch: pytest.MonkeyPatch) -> None:
    _, made = _fake_gradio(monkeypatch)
    client = FakeClient()
    build_ui(client)

    handler = next(w.clicked["fn"] for w in made if w.clicked)
    text, sources, update = handler("Què és una llei qualificada?", True)
    assert text == client.reply
    assert "Llei 12/2004" in sources
    assert update["update"]["visible"] is False

    text, sources, update = handler("Què és una llei qualificada?", False)
    assert sources == ""
    assert update["update"]["visible"] is True
    assert update["update"]["value"] == RAG_OFF_WARNING


@pytest.mark.unit
def test_the_disclaimer_is_always_on_screen(monkeypatch: pytest.MonkeyPatch) -> None:
    """The model card carries the same limitation, and the demo is where a viewer would otherwise
    form an impression and act on it."""
    _, made = _fake_gradio(monkeypatch)
    build_ui(FakeClient())
    shown = " ".join(str(w.kwargs.get("args", "")) for w in made)
    assert DISCLAIMER in shown
    assert all(example in shown for example in EXAMPLES[:1])


@pytest.mark.unit
def test_a_missing_gradio_says_how_to_install_it(monkeypatch: pytest.MonkeyPatch) -> None:
    """An ImportError traceback is not an answer to "why does the demo not start"."""
    monkeypatch.setitem(sys.modules, "gradio", None)
    with pytest.raises(RuntimeError, match="uv add"):
        build_ui(FakeClient())


# ── the HTTP client and the CLI ──────────────────────────────────────────────


@pytest.mark.unit
def test_the_http_client_sends_the_toggle_and_the_key(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, Any] = {}

    class _Response:
        @staticmethod
        def raise_for_status() -> None:
            return None

        @staticmethod
        def json() -> dict[str, Any]:
            return {
                "choices": [{"message": {"content": "resposta"}}],
                "sources": [LEGAL_SOURCE],
            }

    fake_requests = types.ModuleType("requests")
    fake_requests.post = lambda url, **kwargs: (  # type: ignore[attr-defined]
        captured.update(url=url, **kwargs),
        _Response(),
    )[1]
    monkeypatch.setitem(sys.modules, "requests", fake_requests)

    text, sources = HttpChatClient("https://endpoint/", "k3y").ask("pregunta", rag=False)
    assert text == "resposta"
    assert sources == [LEGAL_SOURCE]
    assert captured["url"] == "https://endpoint/v1/chat/completions"
    assert captured["json"]["rag"] is False
    assert captured["headers"]["Authorization"] == "Bearer k3y"
    assert captured["timeout"] == 60.0


@pytest.mark.unit
def test_the_cli_refuses_to_start_without_a_key(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.delenv("MAIA_API_KEY", raising=False)
    assert main([]) == 1
    assert "MAIA_API_KEY" in capsys.readouterr().err


@pytest.mark.unit
def test_the_cli_launches_against_the_configured_url(monkeypatch: pytest.MonkeyPatch) -> None:
    """The key comes from the environment, never from argv, where it would land in shell history."""
    monkeypatch.setenv("MAIA_API_KEY", "secret")
    launched: dict[str, Any] = {}

    class _Ui:
        @staticmethod
        def launch(**kwargs: Any) -> None:
            launched.update(kwargs)

    monkeypatch.setattr("maia.serving.demo.build_ui", lambda client, **kw: _Ui())
    assert main(["--url", "https://x", "--share"]) == 0
    assert launched == {"share": True}
