"""The RAG demo UI — PLAN M5.07, *"UI demo (Gradio / Open WebUI) with RAG on/off toggle and
visible cited sources"*, and the last functional item of DoD-F5.

This is the only part of MAIA that most people will ever touch, which changes what the code has to
get right. Three things, none of them about widgets.

**The RAG toggle is a safety control, not a demo trick.** Decision D8 keeps citable detail — article
numbers, amounts, deadlines, tax rates — *deliberately out of the weights*, because they change and
the model must look them up. So RAG-off is not "the same model without citations": it is the model
answering legal questions from parametric memory it was specifically not given. It will still
answer, fluently, and it will be wrong in exactly the way that matters. Turning the toggle off
therefore raises a visible warning, and that warning is asserted in the tests. A toggle whose only
effect is that the sources box goes empty teaches the viewer the opposite of the truth.

**A withheld source must read as a citation, not as evasion.** Under D-0037/38 a `no-redistribute`
passage is cited but never quoted into the prompt, so the answer built on it is thinner. Without an
explanation the model looks like it is dodging; with one, the viewer learns something true about how
the system handles licensing. :func:`render_sources` marks those explicitly.

**The failure modes are the demo.** An expired key, a rate limit, a cold start that times out — on
serverless these are the *normal* states of a demo endpoint, not exceptional ones. Every one is
turned into a sentence in Catalan that says what happened and what to do. A traceback in the UI is
the demo failing twice.

Gradio is imported lazily inside :func:`build_ui`: it is a heavy optional dependency, the pure
functions below carry all the behaviour worth testing, and CI must not need it to check the rules.
"""

from __future__ import annotations

import argparse
import os
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Protocol

#: Shown whenever retrieval is off. The point of D8 is that the model was *not* given citable
#: detail, so this is the state where a fluent answer is most likely to be confidently wrong.
RAG_OFF_WARNING = (
    "⚠️ **RAG desactivat.** El model respon només amb el que va aprendre durant l'entrenament. "
    "Els detalls citables (números d'article, imports, terminis, tipus impositius) es van deixar "
    "**fora dels pesos a propòsit** (D8) perquè canvien: sense RAG, MAIA pot inventar-los amb tota "
    "la seguretat del món. Activa el RAG per obtenir respostes amb fonts."
)

#: Shown always. The model card carries the same limitation; a demo that omits it is the one place
#: a viewer would form the wrong impression and act on it.
DISCLAIMER = (
    "MAIA no ofereix assessorament jurídic. Per a qualsevol qüestió amb conseqüències legals, "
    "consulta el text consolidat oficial i un professional."
)

_WITHHELD_NOTE = (
    "text no reproduït (llicència): la font es cita però el seu contingut no s'ha fet servir"
)


class ChatClient(Protocol):
    """The seam onto the M5.05 API. Blocked-by-resource: a running endpoint."""

    def ask(self, question: str, *, rag: bool) -> tuple[str, list[dict[str, Any]]]:
        """Return ``(answer, sources)``.

        Raises whatever the transport raises; :func:`answer` turns that into a sentence.
        """


@dataclass(frozen=True)
class Reply:
    """What the UI shows for one question."""

    answer: str
    sources_markdown: str
    warning: str

    @property
    def ok(self) -> bool:
        """False when the answer is an error message rather than a model response."""
        return not self.answer.startswith("❌")


def render_sources(sources: Sequence[dict[str, Any]]) -> str:
    """Citations as Markdown, with withheld passages marked.

    A legal citation without its article number is not a citation anyone can follow, so `llei` and
    `article` are rendered when present rather than collapsed into the URL.
    """
    if not sources:
        return "_Cap font citada._"

    lines = ["**Fonts:**", ""]
    for index, source in enumerate(sources, start=1):
        url = str(source.get("url", ""))
        label_parts = [str(source[key]) for key in ("llei", "article") if source.get(key)]
        label = " — ".join(label_parts) if label_parts else url
        line = f"{index}. [{label}]({url})" if url else f"{index}. {label}"
        if consolidated := source.get("consolidacio_data"):
            line += f" · text consolidat a {consolidated}"
        if source.get("text_withheld"):
            line += f" · _{_WITHHELD_NOTE}_"
        lines.append(line)
    return "\n".join(lines)


def answer(client: ChatClient, question: str, *, rag: bool) -> Reply:
    """One turn of the demo. Never raises: every failure becomes a sentence the viewer can read."""
    if not question.strip():
        return Reply("❌ Escriu una pregunta.", "", "")

    warning = "" if rag else RAG_OFF_WARNING
    try:
        text, sources = client.ask(question, rag=rag)
    except Exception as exc:  # the UI must survive anything the transport raises
        return Reply(f"❌ {_explain(exc)}", "", warning)

    # Sources are hidden rather than empty when RAG is off: an empty "Fonts" box invites the reader
    # to conclude the model simply found nothing this time.
    return Reply(text, render_sources(sources) if rag else "", warning)


def _explain(exc: Exception) -> str:
    """A transport failure, in Catalan, with what to do about it.

    Matched on the text of the error because the client is a seam and its exception types are not
    this module's to depend on.
    """
    detail = str(exc)
    lowered = detail.lower()
    if "401" in detail or "unauthorized" in lowered or "api key" in lowered:
        return "La clau d'API no és vàlida o ha caducat. Revisa MAIA_API_KEY."
    if "429" in detail or "rate limit" in lowered:
        return (
            "Límit de peticions superat. L'endpoint és serverless i el límit protegeix el "
            "pressupost: espera un minut."
        )
    if "timeout" in lowered or "timed out" in lowered:
        return (
            "L'endpoint no ha respost a temps. Si feia estona que no s'utilitzava, la primera "
            "petició ha d'arrencar el contenidor i carregar el model (fins a ~20 s): torna-ho a "
            "provar."
        )
    if "connection" in lowered or "refused" in lowered:
        return "No s'ha pogut connectar amb l'endpoint. Comprova que està desplegat."
    return f"Error inesperat de l'endpoint: {detail}"


#: Questions that show what the system is for. The first two need retrieval and are where RAG-off
#: visibly invents; the third is a lexical question the weights should answer on their own.
EXAMPLES = (
    "Què és una llei qualificada i en què es diferencia d'una llei ordinària?",
    "Quins són els òrgans judicials d'Andorra i en quin ordre?",
    "Què vol dir «cal fer la feina abans de plegar»?",
)


def build_ui(client: ChatClient, *, title: str = "MAIA — demo") -> Any:
    """Build the Gradio Blocks app.

    Gradio is imported here rather than at module scope: it is a heavy optional dependency and
    every rule this module enforces is tested against the pure functions above, without it.

    Raises:
        RuntimeError: with an installable instruction, rather than an ImportError traceback.
    """
    try:
        import gradio as gr
    except ImportError as exc:
        raise RuntimeError("gradio is not installed: `uv add --optional demo gradio`") from exc

    with gr.Blocks(title=title) as ui:
        gr.Markdown(f"# {title}\n\n{DISCLAIMER}")
        rag_toggle = gr.Checkbox(value=True, label="RAG (fonts del corpus andorrà)")
        warning_box = gr.Markdown(visible=False)
        question_box = gr.Textbox(label="Pregunta", lines=2)
        answer_box = gr.Markdown(label="Resposta")
        sources_box = gr.Markdown()
        gr.Examples(list(EXAMPLES), inputs=question_box)

        def _turn(question: str, rag: bool) -> tuple[str, str, Any]:
            reply = answer(client, question, rag=rag)
            return (
                reply.answer,
                reply.sources_markdown,
                gr.update(value=reply.warning, visible=bool(reply.warning)),
            )

        gr.Button("Pregunta", variant="primary").click(
            _turn,
            inputs=[question_box, rag_toggle],
            outputs=[answer_box, sources_box, warning_box],
        )
    return ui


class HttpChatClient:
    """A :class:`ChatClient` over the M5.05 API. Blocked-by-resource: a deployed endpoint."""

    def __init__(self, base_url: str, api_key: str, *, timeout: float = 60.0) -> None:
        self.base_url = base_url.rstrip("/")
        self._api_key = api_key
        self.timeout = timeout

    def ask(self, question: str, *, rag: bool) -> tuple[str, list[dict[str, Any]]]:
        """POST one chat completion and pull out the answer and its citations."""
        import requests

        response = requests.post(
            f"{self.base_url}/v1/chat/completions",
            json={
                "model": "maia-12b-it",
                "messages": [{"role": "user", "content": question}],
                "rag": rag,
            },
            headers={"Authorization": f"Bearer {self._api_key}"},
            timeout=self.timeout,
        )
        response.raise_for_status()
        payload = response.json()
        return payload["choices"][0]["message"]["content"], payload.get("sources", [])


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point: launch the demo against a deployed endpoint."""
    parser = argparse.ArgumentParser(
        description="Launch the MAIA RAG demo (M5.07). Needs a deployed M5.05 endpoint; the API "
        "key is read from MAIA_API_KEY and is never passed on the command line, where it would "
        "land in the shell history."
    )
    parser.add_argument("--url", default=os.environ.get("MAIA_API_URL", "http://localhost:8000"))
    parser.add_argument("--share", action="store_true", help="expose a public Gradio link")
    args = parser.parse_args(argv)

    key = os.environ.get("MAIA_API_KEY", "")
    if not key:
        print("error: MAIA_API_KEY is not set", file=sys.stderr)
        return 1

    build_ui(HttpChatClient(args.url, key)).launch(share=args.share)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
