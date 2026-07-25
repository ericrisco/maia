"""Grounded generation engine — PLAN M2.03.

Distillation from a frontier LLM where **the generator always receives real corpus passages as
context**. That is the anti-hallucination measure the whole of Phase 2 rests on: the model is
not asked what it knows about Andorra, it is asked to write instruction/response pairs *from
passages it is given*, and every example records which passages (§3.2 ``grounding_ids``).

The order of operations is the design:

1. **Verify the pool partition** before anything else (:mod:`maia.synth.pools`). Generation that
   samples ``pool_bench`` contaminates the benchmark, and that failure is silent.
2. **Require the taxonomy to be approved** (M2.01). The node list decides what the model knows.
3. **Plan the mix** — how many examples of which type, per node, from the taxonomy weights and
   §3.2's distribution constraints. ``general_ca`` is deliberately *not* planned here: it is
   unrelated to Andorra and comes from AINA in M2.04.
4. **Sample passages** per node, from ``pool_train`` only, diversified across sources.
5. **Build a Catalan prompt** carrying the passages, the glossary and Andorran-register
   few-shots, and asking for a strict JSON shape.
6. **Parse and validate** into §3.2 examples, rejecting anything malformed with a reason rather
   than repairing it.

Two couplings are enforced here rather than left to the validator:

* **``rag_style`` never samples a ``no-redistribute`` passage.** That type embeds the passage as
  its context, so grounding it on restricted text republishes it (D-0014). Preventing it at
  sampling time costs nothing; detecting it after a €30-60 generation run costs the run.
* **Every sampled id is re-checked against ``pool_train``** with
  :func:`~maia.synth.pools.assert_train_only`, so the guarantee survives a future change to the
  sampler.

The frontier LLM is **blocked-by-resource** (needs an API key and spend). :class:`TextGenerator`
is the seam; everything above — planning, sampling, prompting, parsing, budgeting — is exercised
offline against a scripted fake.

**``judge_score`` is left at 0.0 by generation**: it means *not yet judged*, and M2.05's
LLM-as-judge overwrites it. A dataset where every score is still 0.0 has not been through the
judge — §3.2 cannot distinguish that from "judged terrible", which is noted in the wiki gaps.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from random import Random
from typing import Protocol, TypeVar, cast
from uuid import UUID, uuid5

from maia.schemas import CorpusDocument, DatasetExample, ExampleType, Registre, Split
from maia.synth.glossary import Category, Glossary, load_glossary
from maia.synth.pools import Partition, assert_train_only, load_partition
from maia.synth.taxonomy import Taxonomy, TaxonomyNode, load_taxonomy, require_approved

#: Passages per generation request (the plan's 5-20).
MIN_PASSAGES = 5
MAX_PASSAGES = 20

#: How the corpus-grounded share of the dataset splits across types. ``general_ca`` is absent
#: on purpose — it is the AINA anti-forgetting mix (M2.04), not something generated from the
#: corpus. ``no_ho_se`` is sized so that after M2.04 dilutes everything it lands near §3.2's 8 %.
TYPE_MIX: dict[ExampleType, float] = {
    ExampleType.QA: 0.34,
    ExampleType.EXPLICACIO: 0.16,
    ExampleType.RAG_STYLE: 0.16,
    ExampleType.MULTITURN: 0.10,
    ExampleType.RESUM: 0.08,
    ExampleType.NO_HO_SE: 0.10,
    ExampleType.TRADUCCIO: 0.03,
    ExampleType.ESTIL_ANDORRA: 0.03,
}

#: Namespace for deriving example ids, so a re-run produces the same ids for the same content.
_ID_NAMESPACE = UUID("6ba7b812-9dad-11d1-80b4-00c04fd430c8")

#: Few-shot style excerpts are trimmed to this length — they are there for register, not content.
STYLE_EXCERPT_CHARS = 400


class TextGenerator(Protocol):
    """The frontier LLM. Blocked-by-resource: needs an API key and spend."""

    def complete(self, prompt: str) -> str:
        """Return the model's completion for ``prompt``."""


class ContentBlock(Protocol):
    """One block of a model response. ``text`` is only read on ``type == "text"`` blocks."""

    @property
    def type(self) -> str:
        """The block kind — ``text``, ``thinking``, ``tool_use``…"""

    @property
    def text(self) -> str:
        """The block's text. Only meaningful on a text block."""


class ResponseMessage(Protocol):
    """The slice of an Anthropic ``Message`` this module reads."""

    @property
    def stop_reason(self) -> str | None:
        """Why generation stopped. ``"refusal"`` must be checked before reading content."""

    @property
    def content(self) -> Sequence[ContentBlock]:
        """The response blocks."""


class MessagesResource(Protocol):
    """The ``client.messages`` surface this module calls."""

    def create(
        self,
        *,
        model: str,
        max_tokens: int,
        messages: Sequence[dict[str, str]],
        **extra: object,
    ) -> ResponseMessage:
        """Create one message."""


class MessagesClient(Protocol):
    """An Anthropic client, narrowed to what this module uses."""

    @property
    def messages(self) -> MessagesResource:
        """The Messages API resource."""


@dataclass
class Budget:
    """Per-batch cost control. Phase 2 targets €30-60 of API in total."""

    max_requests: int
    max_examples: int
    requests: int = 0
    examples: int = 0

    def can_continue(self) -> bool:
        """Whether another request is within budget."""
        return self.requests < self.max_requests and self.examples < self.max_examples

    def record(self, examples: int) -> None:
        """Account for one completed request."""
        self.requests += 1
        self.examples += examples

    @property
    def remaining_examples(self) -> int:
        """Examples still allowed."""
        return max(0, self.max_examples - self.examples)


@dataclass(frozen=True)
class GenerationRequest:
    """Everything one call to the frontier LLM needs."""

    node: TaxonomyNode
    example_type: ExampleType
    count: int
    passages: tuple[CorpusDocument, ...]
    glossary_lines: tuple[str, ...] = ()
    style_excerpts: tuple[str, ...] = ()

    @property
    def grounding_ids(self) -> list[str]:
        """The §3.2 grounding of every example this request produces."""
        return [passage.id for passage in self.passages]


_Key = TypeVar("_Key")


def largest_remainder(
    shares: dict[_Key, float], total: int, order: Callable[[_Key], str]
) -> dict[_Key, int]:
    """Allocate ``total`` whole units across ``shares``, summing **exactly**.

    Each key gets the floor of its share, then the leftover units go to the largest fractional
    parts. ``order`` breaks ties deterministically, so the same inputs always allocate the same
    way.

    Exactness is the point rather than a nicety: §3.2's distribution constraints are checked to
    the percentage point, and rounding drift across 64 taxonomy nodes would be enough to fail
    them on a dataset that is otherwise correct.
    """
    if total <= 0 or not shares:
        return {}
    exact = {key: total * share for key, share in shares.items()}
    allocation = {key: int(value) for key, value in exact.items()}
    remainder = total - sum(allocation.values())
    ranked = sorted(exact.items(), key=lambda item: (-(item[1] % 1), order(item[0])))
    for key, _ in ranked[:remainder]:
        allocation[key] += 1
    return allocation


def plan_types(count: int, mix: dict[ExampleType, float] | None = None) -> dict[ExampleType, int]:
    """Split ``count`` examples across types by :data:`TYPE_MIX`, summing exactly."""
    allocated = largest_remainder(mix or TYPE_MIX, count, lambda kind: kind.value)
    return {kind: value for kind, value in allocated.items() if value}


def node_quota(taxonomy: Taxonomy, total: int) -> dict[str, int]:
    """Split ``total`` examples across nodes by taxonomy weight, summing exactly.

    No divide-by-zero guard is needed: the taxonomy schema requires at least one node and each
    node's ``weight`` to be greater than zero, so the sum is always positive.
    """
    weights = {node.id: node.weight for node in taxonomy.nodes}
    weight_sum = sum(weights.values())
    shares = {node_id: weight / weight_sum for node_id, weight in weights.items()}
    return largest_remainder(shares, total, lambda node_id: node_id)


def sample_passages(
    node: TaxonomyNode,
    documents: Sequence[CorpusDocument],
    partition: Partition,
    *,
    example_type: ExampleType,
    rng: Random,
    max_passages: int = MAX_PASSAGES,
) -> list[CorpusDocument]:
    """Pick this node's grounding passages from ``pool_train``.

    Candidates are documents whose text mentions one of the node's keywords. They are then taken
    **round-robin across sources**, so a node does not end up grounded entirely in Viquipèdia
    when institutional and legal passages were also available — grounding diversity is what
    stops the generated examples from all sounding like one source.

    ``rag_style`` requests exclude ``no-redistribute`` passages: that type embeds the passage as
    its context, so grounding it on restricted text republishes it (D-0014). Preventing it here
    costs nothing; catching it after the generation run costs the run.
    """
    needles = [keyword.casefold() for keyword in node.keywords]
    embeds_text = example_type.embeds_source_text()

    by_source: dict[str, list[CorpusDocument]] = {}
    for document in documents:
        if not partition.allows(document.id):
            continue
        if embeds_text and not document.license.is_public():
            continue
        haystack = document.text.casefold()
        if any(needle in haystack for needle in needles):
            by_source.setdefault(document.source.value, []).append(document)

    for group in by_source.values():
        group.sort(key=lambda document: document.id)
        rng.shuffle(group)

    picked: list[CorpusDocument] = []
    sources = sorted(by_source)
    while len(picked) < max_passages and any(by_source[source] for source in sources):
        for source in sources:
            if by_source[source] and len(picked) < max_passages:
                picked.append(by_source[source].pop())
    return picked


def style_excerpts(documents: Iterable[CorpusDocument], *, count: int, rng: Random) -> list[str]:
    """Andorran-register few-shots, drawn from the spoken subcorpora.

    Register injection by example rather than instruction: telling a model to "write like an
    Andorran" does far less than showing it Andorrans talking. Excerpts are trimmed because they
    are there for register, not content — and D7 forbids cloning any individual's voice, so they
    are drawn across speakers rather than from one.
    """
    spoken = [
        document.text
        for document in documents
        if document.registre in {Registre.ANDORRA_PARLAT, Registre.ANDORRA_PARLAT_ORAL}
    ]
    if not spoken:
        return []
    spoken.sort()
    rng.shuffle(spoken)
    return [text[:STYLE_EXCERPT_CHARS].strip() for text in spoken[:count]]


_TYPE_INSTRUCTIONS: dict[ExampleType, str] = {
    ExampleType.QA: "Preguntes concretes amb respostes breus i exactes.",
    ExampleType.EXPLICACIO: "Preguntes obertes amb explicacions desenvolupades i ordenades.",
    ExampleType.MULTITURN: (
        "Converses de dos o tres torns, on cada pregunta continua la resposta anterior. "
        "Alterna sempre usuari i assistent, i acaba amb l'assistent."
    ),
    ExampleType.RESUM: "Peticions de resum del passatge, amb resums fidels i sense afegits.",
    ExampleType.TRADUCCIO: (
        "Peticions de traducció al català d'una frase en castellà o francès sobre el tema, "
        "amb la traducció correcta."
    ),
    ExampleType.NO_HO_SE: (
        "Preguntes que els passatges NO permeten respondre (dades que canvien: imports, "
        "terminis, percentatges, articles concrets). La resposta ha de dir honestament que no "
        "consta i on cal consultar-ho (el text vigent al BOPA). No inventis mai la dada."
    ),
    ExampleType.RAG_STYLE: (
        "La pregunta de l'usuari inclou el passatge com a context; la resposta el fa servir i "
        "el cita. És el format que el model trobarà en producció amb RAG."
    ),
    ExampleType.ESTIL_ANDORRA: (
        "Peticions de reescriptura d'un text en català general al registre andorrà, mantenint "
        "el significat i canviant només el lèxic i el gir."
    ),
    ExampleType.GENERAL_CA: (
        "NO es genera aquí: és la barreja anti-oblit de català general (AINA, M2.04)."
    ),
}


def type_instruction(example_type: ExampleType) -> str:
    """The per-type instruction added to the prompt.

    Raises:
        KeyError: for a type with no instruction — which would mean the prompt silently asked
            for nothing in particular, and the batch came back as an unusable mix.
    """
    return _TYPE_INSTRUCTIONS[example_type]


def build_prompt(request: GenerationRequest) -> str:
    """The Catalan generation prompt.

    The passages come last and are clearly delimited, because that is where the model must look;
    the rules come first so they are still in view. The output shape is a strict JSON array so
    the response can be parsed rather than interpreted.
    """
    passages = "\n\n".join(
        f"[PASSATGE {index}] (font: {passage.source.value})\n{passage.text}"
        for index, passage in enumerate(request.passages, start=1)
    )
    lines = [
        "Ets un expert en Andorra i en llengua catalana. Has de redactar exemples "
        "d'entrenament per a un model de llenguatge andorrà.",
        "",
        f"TEMA: {request.node.label} ({request.node.id})",
        f"NOMBRE D'EXEMPLES: {request.count}",
        f"TIPUS: {request.example_type.value} — {type_instruction(request.example_type)}",
        "",
        "REGLES INVIOLABLES:",
        "1. Basa't NOMÉS en els passatges de sota. No afegeixis cap dada que no hi sigui.",
        "2. Si els passatges no contenen la resposta, no te la inventis.",
        "3. Escriu en català d'Andorra, natural i correcte. No calquis el castellà.",
        "4. Varia la formulació de les preguntes; no repeteixis la mateixa estructura.",
        "5. No esmentis els passatges ni diguis «segons el text»; escriu com un expert.",
    ]
    if request.example_type is ExampleType.RAG_STYLE:
        lines.append(
            "6. Per a aquest tipus, la pregunta de l'usuari ha d'incloure el passatge com a "
            "context i la resposta ha de citar-lo explícitament."
        )
    if request.glossary_lines:
        lines += [
            "",
            "LÈXIC ANDORRÀ (fes-lo servir amb naturalitat quan encaixi; no forcis):",
            *request.glossary_lines,
        ]
    if request.style_excerpts:
        lines += ["", "REGISTRE ANDORRÀ (imita el to, no el contingut):"]
        lines += [f"«{excerpt}»" for excerpt in request.style_excerpts]
    lines += [
        "",
        "FORMAT DE SORTIDA — només un array JSON, sense text abans ni després:",
        '[{"messages": [{"role": "user", "content": "..."}, '
        '{"role": "assistant", "content": "..."}]}]',
        "",
        "PASSATGES:",
        "",
        passages,
    ]
    return "\n".join(lines)


@dataclass
class GenerationResult:
    """What one request produced, and what was thrown away."""

    examples: list[DatasetExample] = field(default_factory=list)
    rejected: list[str] = field(default_factory=list)

    def extend(self, other: GenerationResult) -> None:
        """Absorb another result."""
        self.examples.extend(other.examples)
        self.rejected.extend(other.rejected)


def _strip_fence(raw: str) -> str:
    """Drop a ```json fence if the model wrapped its answer in one."""
    text = raw.strip()
    if not text.startswith("```"):
        return text
    body = text.split("\n", 1)[1] if "\n" in text else ""
    return body.rsplit("```", 1)[0].strip()


def parse_response(
    raw: str,
    request: GenerationRequest,
    *,
    generator: str,
    split: Split = Split.TRAIN,
) -> GenerationResult:
    """Turn a model response into §3.2 examples.

    Malformed items are **rejected with a reason, never repaired**. A silently patched example is
    an example nobody wrote and nobody reviewed, and the whole dataset's credibility rests on
    every example having been produced by the process that is documented.

    Ids are derived from the content with UUID5, so re-running generation over the same passages
    does not duplicate the dataset — and §3.2's split-leakage check would catch it if it did.
    """
    result = GenerationResult()
    try:
        payload = json.loads(_strip_fence(raw))
    except json.JSONDecodeError as exc:
        result.rejected.append(f"{request.node.id}: response was not JSON ({exc.msg})")
        return result
    if not isinstance(payload, list):
        result.rejected.append(
            f"{request.node.id}: expected a JSON array, got {type(payload).__name__}"
        )
        return result

    for index, item in enumerate(payload, start=1):
        locator = f"{request.node.id}#{index}"
        if not isinstance(item, dict) or "messages" not in item:
            result.rejected.append(f"{locator}: item has no 'messages'")
            continue
        fingerprint = json.dumps(item["messages"], ensure_ascii=False, sort_keys=True)
        try:
            example = DatasetExample.model_validate(
                {
                    "id": str(uuid5(_ID_NAMESPACE, f"{request.node.id}|{fingerprint}")),
                    "messages": item["messages"],
                    "type": request.example_type.value,
                    "topic": request.node.id,
                    "grounding_ids": request.grounding_ids,
                    "generator": generator,
                    # 0.0 means "not yet judged"; M2.05's judge overwrites it.
                    "judge_score": 0.0,
                    "split": split.value,
                }
            )
        except ValueError as exc:
            first = str(exc).splitlines()[-1].strip() if str(exc) else "invalid"
            result.rejected.append(f"{locator}: {first}")
            continue
        result.examples.append(example)
    return result


def generate_node(
    generator: TextGenerator,
    request: GenerationRequest,
    *,
    generator_name: str,
    split: Split = Split.TRAIN,
) -> GenerationResult:
    """Run one request against the frontier LLM."""
    return parse_response(
        generator.complete(build_prompt(request)),
        request,
        generator=generator_name,
        split=split,
    )


def generate_batch(
    generator: TextGenerator,
    taxonomy: Taxonomy,
    documents: Sequence[CorpusDocument],
    partition: Partition,
    *,
    frozen_digest: str,
    total: int,
    budget: Budget,
    generator_name: str,
    glossary: Glossary | None = None,
    seed: int,
    split: Split = Split.TRAIN,
) -> GenerationResult:
    """Generate a batch across the whole taxonomy, in budget.

    Refuses to start unless the partition matches ``frozen_digest`` and the taxonomy is
    approved. Both checks are cheap and both failures are otherwise silent: a contaminated
    benchmark reports flattering numbers, and an unapproved taxonomy spends the API budget on
    the wrong topics.
    """
    from maia.synth.pools import verify_partition

    verify_partition(partition, frozen_digest)
    require_approved(taxonomy)

    rng = Random(seed)
    excerpts = tuple(style_excerpts(documents, count=3, rng=rng))
    result = GenerationResult()

    for node_id, node_total in sorted(node_quota(taxonomy, total).items()):
        node = taxonomy.node(node_id)
        for example_type, count in sorted(
            plan_types(node_total).items(), key=lambda item: item[0].value
        ):
            if not budget.can_continue():
                result.rejected.append(
                    f"{node_id}: skipped, batch budget exhausted "
                    f"({budget.requests} requests, {budget.examples} examples)"
                )
                return result
            passages = sample_passages(
                node, documents, partition, example_type=example_type, rng=rng
            )
            if len(passages) < MIN_PASSAGES:
                result.rejected.append(
                    f"{node_id} ({example_type.value}): only {len(passages)} passage(s) in "
                    f"pool_train, fewer than the {MIN_PASSAGES} needed to ground it"
                )
                continue
            assert_train_only(partition, [passage.id for passage in passages])

            lines = tuple(glossary.prompt_lines(_categories_for(node)) if glossary else ())
            request = GenerationRequest(
                node=node,
                example_type=example_type,
                count=min(count, budget.remaining_examples),
                passages=tuple(passages),
                glossary_lines=lines,
                style_excerpts=excerpts,
            )
            produced = generate_node(generator, request, generator_name=generator_name, split=split)
            budget.record(len(produced.examples))
            result.extend(produced)
    return result


def _categories_for(node: TaxonomyNode) -> list[Category] | None:
    """Glossary categories worth putting in this node's prompt.

    A node about geography does not need the whole institutional lexicon in its context window;
    matching the node's branch to a glossary category keeps the prompt focused (and cheaper).
    ``None`` means "all of it", for branches with no obvious counterpart.
    """
    mapping = {
        "institucions": [Category.INSTITUCIONAL, Category.ADMINISTRATIU],
        "legal": [Category.JURIDIC, Category.INSTITUCIONAL],
        "geografia": [Category.GEOGRAFIC],
        "cultura": [Category.CULTURAL, Category.QUOTIDIA],
        "gastronomia": [Category.CULTURAL],
        "economia": [Category.ADMINISTRATIU, Category.INSTITUCIONAL],
    }
    return mapping.get(node.branch)


def render(result: GenerationResult, budget: Budget) -> str:
    """Human-readable summary of a batch."""
    lines = [
        f"generated {len(result.examples)} example(s) in {budget.requests} request(s); "
        f"{len(result.rejected)} rejection(s)",
    ]
    for reason in result.rejected[:20]:
        lines.append(f"  ⚠ {reason}")
    if len(result.rejected) > 20:
        lines.append(f"  … and {len(result.rejected) - 20} more")
    return "\n".join(lines)


class RefusalError(RuntimeError):
    """Raised when the model declined the request.

    A refusal arrives as a **successful HTTP 200** with ``stop_reason == "refusal"`` and an
    empty or partial ``content``, so code that reads ``content[0]`` unconditionally would
    silently treat a decline as an empty batch. Raising makes it visible instead.
    """


@dataclass(frozen=True)
class AnthropicGenerator:
    """The frontier generator, wired to the Anthropic Messages API.

    The **client is injected, not constructed here** — the same inversion used for the corpus
    tokenizer (M1.10) and the HF hub (M1.09). Getting an authenticated client is the
    blocked-by-resource part and belongs to the caller; everything this class does with it is
    testable against a stand-in::

        from anthropic import Anthropic

        generator = AnthropicGenerator(Anthropic(), model="claude-opus-5")

    ``max_tokens`` defaults to 16000 rather than the SDK minimum: this is a non-streaming
    request, thinking is on by default on Claude Opus 5, and ``max_tokens`` caps thinking *and*
    response text together — a tight budget truncates the JSON array mid-example, which the
    parser then rejects wholesale.

    ``fallbacks="default"`` is on by default. Claude Opus 5's safety classifiers can decline a
    request, and benign adjacent work sometimes trips them; the parameter re-runs a declined
    request on Anthropic's recommended fallback server-side rather than losing the batch.
    """

    client: MessagesClient
    model: str = "claude-opus-5"
    max_tokens: int = 16_000
    use_fallbacks: bool = True

    def complete(self, prompt: str) -> str:
        """Send one prompt and return the model's text.

        Raises:
            RefusalError: if the model declined. Checked *before* reading ``content``.
        """
        extra: dict[str, object] = (
            {"betas": ["server-side-fallback-2026-07-01"], "fallbacks": "default"}
            if self.use_fallbacks
            else {}
        )
        message = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=[{"role": "user", "content": prompt}],
            **extra,
        )
        if message.stop_reason == "refusal":
            raise RefusalError(
                f"{self.model} declined this generation request; "
                "check the taxonomy node and its passages"
            )
        return "".join(block.text for block in message.content if block.type == "text")


def anthropic_client(api_key: str | None = None) -> MessagesClient:
    """Build a real Anthropic client (blocked-by-resource: needs an API key and spend).

    Imported locally so the module and its tests need no key. The cast narrows the SDK's
    content-block union to the two fields :class:`AnthropicGenerator` actually reads.
    """
    from anthropic import Anthropic

    return cast(MessagesClient, Anthropic(api_key=api_key))


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point. ``--dry-run`` prints one prompt instead of calling the API."""
    parser = argparse.ArgumentParser(
        description="Generate grounded synthetic examples from the corpus (M2.03). The API call "
        "is blocked-by-resource; --dry-run exercises everything up to it."
    )
    parser.add_argument("--corpus", type=Path, nargs="+", required=True)
    parser.add_argument("--taxonomy", type=Path, required=True)
    parser.add_argument("--partition", type=Path, required=True)
    parser.add_argument("--frozen-digest", required=True, help="the B1 partition freeze")
    parser.add_argument("--glossary", type=Path)
    parser.add_argument("--out", type=Path, help="write examples here as JSONL")
    parser.add_argument("--total", type=int, default=1000)
    parser.add_argument("--max-requests", type=int, default=200)
    parser.add_argument("--seed", type=int, default=20260725)
    parser.add_argument("--model", default="claude-opus-5")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print the first prompt that would be sent and stop",
    )
    args = parser.parse_args(argv)

    paths = [*args.corpus, args.taxonomy, args.partition]
    if args.glossary:
        paths.append(args.glossary)
    for path in paths:
        if not path.is_file():
            print(f"error: no such file: {path}", file=sys.stderr)
            return 1

    documents = [
        CorpusDocument.model_validate_json(line)
        for path in args.corpus
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    try:
        taxonomy = load_taxonomy(args.taxonomy)
        partition = load_partition(args.partition, expected_digest=args.frozen_digest)
        glossary = load_glossary(args.glossary) if args.glossary else None
    except (ValueError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.dry_run:
        rng = Random(args.seed)
        node = taxonomy.nodes[0]
        passages = sample_passages(node, documents, partition, example_type=ExampleType.QA, rng=rng)
        request = GenerationRequest(
            node=node,
            example_type=ExampleType.QA,
            count=5,
            passages=tuple(passages),
            glossary_lines=tuple(glossary.prompt_lines(_categories_for(node)) if glossary else ()),
            style_excerpts=tuple(style_excerpts(documents, count=2, rng=rng)),
        )
        print(build_prompt(request))
        return 0

    budget = Budget(max_requests=args.max_requests, max_examples=args.total)
    try:
        result = generate_batch(
            AnthropicGenerator(anthropic_client(), model=args.model),
            taxonomy,
            documents,
            partition,
            frozen_digest=args.frozen_digest,
            total=args.total,
            budget=budget,
            generator_name=args.model,
            glossary=glossary,
            seed=args.seed,
        )
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(
            "".join(f"{example.model_dump_json()}\n" for example in result.examples),
            encoding="utf-8",
        )
    print(render(result, budget))
    return 0 if result.examples else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
