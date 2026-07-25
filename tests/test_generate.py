"""Tests for the grounded generation engine (PLAN M2.03).

The frontier LLM is blocked-by-resource; :class:`ScriptedGenerator` stands in for it, so
planning, sampling, prompting, parsing, budgeting and every refusal are verified offline.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from random import Random

import pytest
import yaml

from maia.schemas import (
    CorpusDocument,
    ExampleType,
    License,
    Registre,
    Source,
    Split,
)
from maia.synth.generate import (
    MIN_PASSAGES,
    TYPE_MIX,
    AnthropicGenerator,
    Budget,
    GenerationRequest,
    RefusalError,
    anthropic_client,
    build_prompt,
    generate_batch,
    generate_node,
    largest_remainder,
    main,
    node_quota,
    parse_response,
    plan_types,
    render,
    sample_passages,
    style_excerpts,
    type_instruction,
)
from maia.synth.glossary import Glossary
from maia.synth.pools import ContaminationError, Partition, split_corpus
from maia.synth.taxonomy import NotApprovedError, Taxonomy, TaxonomyNode

STAMP = datetime(2026, 8, 1, tzinfo=UTC)


def document(
    text: str,
    *,
    source: Source = Source.GOVERN,
    license: License = License.PUBLIC_OFFICIAL,
    registre: Registre = Registre.ESTANDARD,
) -> CorpusDocument:
    return CorpusDocument(
        text=text,
        source=source,
        url=f"https://www.example.ad/{abs(len(text))}-{source.value}",  # type: ignore[arg-type]
        fetched_at=STAMP,
        lang="ca",
        license=license,
        registre=registre,
    )


def falles_corpus(count: int = 12, **kwargs: object) -> list[CorpusDocument]:
    return [
        document(f"Les falles del solstici es fan a la parròquia, edició {index}.", **kwargs)  # type: ignore[arg-type]
        for index in range(count)
    ]


NODE = TaxonomyNode.model_validate(
    {"id": "cultura/falles-solstici", "label": "Les falles", "keywords": ["falles"]}
)


def taxonomy_of(*nodes: TaxonomyNode, approved: bool = True) -> Taxonomy:
    return Taxonomy.model_validate(
        {
            "version": "test",
            "approved": approved,
            "approved_by": "Eric Risco" if approved else "",
            "nodes": [node.model_dump() for node in nodes],
        }
    )


def all_train(documents: list[CorpusDocument]) -> Partition:
    return Partition(frozenset(doc.id for doc in documents), frozenset())


class ScriptedGenerator:
    """Returns canned responses in order, recording the prompts it was given."""

    def __init__(self, *responses: str) -> None:
        self.responses = list(responses)
        self.prompts: list[str] = []

    def complete(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return self.responses[min(len(self.prompts) - 1, len(self.responses) - 1)]


class ShapeAwareGenerator:
    """A fake that answers with the shape the prompt asked for.

    Reads the ``TIPUS:`` line and returns two turns for ``multiturn``, one otherwise — so a
    batch spanning several types is not rejected for reasons that are the fake's fault.
    """

    def __init__(self, count: int = 2) -> None:
        self.count = count
        self.prompts: list[str] = []

    def complete(self, prompt: str) -> str:
        self.prompts.append(prompt)
        turns = 2 if "TIPUS: multiturn" in prompt else 1
        return json.dumps(
            [
                {
                    "messages": [
                        message
                        for turn in range(turns)
                        for message in (
                            {"role": "user", "content": f"Pregunta {index}.{turn}?"},
                            {"role": "assistant", "content": f"Resposta {index}.{turn}."},
                        )
                    ]
                }
                for index in range(self.count)
            ]
        )


def response(count: int = 2) -> str:
    return json.dumps(
        [
            {
                "messages": [
                    {"role": "user", "content": f"Què són les falles? ({index})"},
                    {"role": "assistant", "content": f"Una tradició del solstici ({index})."},
                ]
            }
            for index in range(count)
        ]
    )


# ─────────────────────────────────────────────────────────────
# Planning the mix
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_type_mix_sums_to_one_and_excludes_general_ca() -> None:
    # general_ca is the AINA anti-forgetting mix (M2.04), not something generated from the corpus.
    assert sum(TYPE_MIX.values()) == pytest.approx(1.0)
    assert ExampleType.GENERAL_CA not in TYPE_MIX


@pytest.mark.unit
@pytest.mark.parametrize("count", [1, 7, 13, 100, 999])
def test_planning_allocates_exactly_the_requested_count(count: int) -> None:
    """Largest-remainder, so the total is exact.

    §3.2's distribution constraints are checked to the percentage point, and rounding drift
    across 64 nodes would be enough to fail them.
    """
    assert sum(plan_types(count).values()) == count


@pytest.mark.unit
def test_planning_nothing_allocates_nothing() -> None:
    assert plan_types(0) == {}
    assert plan_types(-5) == {}


@pytest.mark.unit
def test_no_ho_se_lands_in_its_band_once_general_ca_dilutes_it() -> None:
    """The reason no_ho_se is 10 % here but 8 % in §3.2.

    M2.04 adds 15-20 % general_ca on top of this, so 10 % of the generated portion becomes
    ~8.25 % of the finished dataset — inside §3.2's 6-10 % band.
    """
    generated_share = plan_types(10_000)[ExampleType.NO_HO_SE] / 10_000
    for general_ca_share in (0.15, 0.175, 0.20):
        final = generated_share * (1 - general_ca_share)
        assert 0.06 <= final <= 0.10, general_ca_share


@pytest.mark.unit
def test_node_quota_follows_weight_and_sums_exactly() -> None:
    heavy = TaxonomyNode.model_validate({**NODE.model_dump(), "id": "a/heavy", "weight": 3.0})
    light = TaxonomyNode.model_validate({**NODE.model_dump(), "id": "b/light", "weight": 1.0})
    quota = node_quota(taxonomy_of(heavy, light), 100)
    assert sum(quota.values()) == 100
    assert quota["a/heavy"] > quota["b/light"] * 2


@pytest.mark.unit
def test_node_quota_of_nothing_is_empty() -> None:
    assert node_quota(taxonomy_of(NODE), 0) == {}


# ─────────────────────────────────────────────────────────────
# Sampling passages
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_sampling_finds_passages_matching_the_node_keywords() -> None:
    documents = [*falles_corpus(8), document("Un text sobre res en concret.")]
    picked = sample_passages(
        NODE, documents, all_train(documents), example_type=ExampleType.QA, rng=Random(1)
    )
    assert len(picked) == 8
    assert all("falles" in doc.text for doc in picked)


@pytest.mark.unit
def test_sampling_never_leaves_pool_train() -> None:
    """The B1 → M2 guarantee, checked at the sampler."""
    documents = falles_corpus(10)
    partition = Partition(
        frozenset(doc.id for doc in documents[:4]), frozenset(doc.id for doc in documents[4:])
    )
    picked = sample_passages(NODE, documents, partition, example_type=ExampleType.QA, rng=Random(1))
    assert {doc.id for doc in picked} <= partition.train


@pytest.mark.unit
def test_rag_style_never_samples_restricted_text() -> None:
    """D-0014, enforced at generation rather than detected at validation.

    rag_style embeds the passage as its context, so grounding it on no-redistribute text
    republishes it. Preventing it here costs nothing; catching it after a €30-60 run costs the run.
    """
    documents = [
        *falles_corpus(6, license=License.NO_REDISTRIBUTE, source=Source.PREMSA),
        *falles_corpus(6),
    ]
    partition = all_train(documents)
    restricted = sample_passages(
        NODE, documents, partition, example_type=ExampleType.RAG_STYLE, rng=Random(1)
    )
    assert all(doc.license.is_public() for doc in restricted)
    # Other types may ground on it — paraphrase is explicitly allowed.
    paraphrase = sample_passages(
        NODE, documents, partition, example_type=ExampleType.QA, rng=Random(1)
    )
    assert any(not doc.license.is_public() for doc in paraphrase)


@pytest.mark.unit
def test_sampling_diversifies_across_sources() -> None:
    """A node grounded entirely in one source generates examples that all sound like it."""
    documents = [
        *falles_corpus(30, source=Source.VIQUIPEDIA),
        *falles_corpus(3, source=Source.CULTURA),
        *falles_corpus(3, source=Source.JURIDIC),
    ]
    picked = sample_passages(
        NODE, documents, all_train(documents), example_type=ExampleType.QA, rng=Random(1)
    )
    sources = {doc.source.value for doc in picked}
    assert sources == {"viquipedia", "cultura", "juridic"}


@pytest.mark.unit
def test_sampling_respects_the_maximum() -> None:
    documents = falles_corpus(50)
    picked = sample_passages(
        NODE,
        documents,
        all_train(documents),
        example_type=ExampleType.QA,
        rng=Random(1),
        max_passages=7,
    )
    assert len(picked) == 7


@pytest.mark.unit
def test_sampling_is_deterministic_for_a_seed() -> None:
    documents = falles_corpus(30)
    partition = all_train(documents)
    first = sample_passages(NODE, documents, partition, example_type=ExampleType.QA, rng=Random(3))
    second = sample_passages(NODE, documents, partition, example_type=ExampleType.QA, rng=Random(3))
    assert [d.id for d in first] == [d.id for d in second]


@pytest.mark.unit
def test_sampling_a_node_nothing_matches_returns_nothing() -> None:
    documents = [document("Un text sobre economia digital.")]
    assert (
        sample_passages(
            NODE, documents, all_train(documents), example_type=ExampleType.QA, rng=Random(1)
        )
        == []
    )


# ─────────────────────────────────────────────────────────────
# Style few-shots
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_style_excerpts_come_only_from_spoken_registers() -> None:
    spoken = document(
        "Doncs miri, jo hi vaig cada any i sempre és igual d'emocionant, ves.",
        source=Source.CONSELL_DIARI_SESSIONS,
        registre=Registre.ANDORRA_PARLAT,
    )
    oral = document(
        "Bon dia a tothom i benvinguts al programa d'avui.",
        source=Source.RTVA,
        license=License.NO_REDISTRIBUTE,
        registre=Registre.ANDORRA_PARLAT_ORAL,
    )
    written = document("El Govern ha aprovat el pressupost per a l'exercici vinent.")
    corpus = [spoken, oral, written]
    excerpts = style_excerpts(corpus, all_train(corpus), count=5, rng=Random(1))
    # `oral` is RTVA and therefore no-redistribute, so only the publishable spoken turn survives.
    assert len(excerpts) == 1
    assert written.text not in excerpts
    assert "Doncs miri" in excerpts[0]


@pytest.mark.unit
def test_style_excerpts_are_trimmed() -> None:
    long_turn = document(
        "paraula " * 500,
        source=Source.CONSELL_DIARI_SESSIONS,
        registre=Registre.ANDORRA_PARLAT,
    )
    assert (
        len(style_excerpts([long_turn], all_train([long_turn]), count=1, rng=Random(1))[0]) <= 400
    )


@pytest.mark.unit
def test_no_spoken_documents_means_no_excerpts() -> None:
    written = [document("Text escrit estàndard.")]
    assert style_excerpts(written, all_train(written), count=3, rng=Random(1)) == []


# ─────────────────────────────────────────────────────────────
# The prompt
# ─────────────────────────────────────────────────────────────


def request_for(example_type: ExampleType = ExampleType.QA, **kwargs: object) -> GenerationRequest:
    documents = falles_corpus(6)
    payload: dict[str, object] = {
        "node": NODE,
        "example_type": example_type,
        "count": 5,
        "passages": tuple(documents),
    }
    payload.update(kwargs)
    return GenerationRequest(**payload)  # type: ignore[arg-type]


@pytest.mark.unit
def test_the_prompt_carries_the_passages_and_the_rules() -> None:
    prompt = build_prompt(request_for())
    assert "Les falles" in prompt
    assert "cultura/falles-solstici" in prompt
    assert "REGLES INVIOLABLES" in prompt
    assert "No afegeixis cap dada que no hi sigui" in prompt
    assert prompt.count("[PASSATGE") == 6
    # The passages come last, where the model must look.
    assert prompt.index("REGLES INVIOLABLES") < prompt.index("[PASSATGE 1]")


@pytest.mark.unit
def test_every_type_has_an_instruction() -> None:
    # A type with no instruction would ask the model for nothing in particular.
    for example_type in ExampleType:
        assert type_instruction(example_type)


@pytest.mark.unit
def test_the_no_ho_se_prompt_forbids_inventing_the_answer() -> None:
    prompt = build_prompt(request_for(ExampleType.NO_HO_SE))
    assert "BOPA" in prompt
    assert "No inventis mai la dada" in prompt


@pytest.mark.unit
def test_the_rag_style_prompt_asks_for_the_context_in_the_question() -> None:
    prompt = build_prompt(request_for(ExampleType.RAG_STYLE))
    assert "ha d'incloure el passatge com a context" in prompt


@pytest.mark.unit
def test_the_glossary_and_style_are_included_when_given() -> None:
    prompt = build_prompt(
        request_for(
            glossary_lines=("- comú: l'òrgan de govern d'una parròquia",),
            style_excerpts=("Doncs miri, ves.",),
        )
    )
    assert "LÈXIC ANDORRÀ" in prompt
    assert "comú" in prompt
    assert "REGISTRE ANDORRÀ" in prompt
    assert "Doncs miri, ves." in prompt


@pytest.mark.unit
def test_the_prompt_omits_empty_sections() -> None:
    prompt = build_prompt(request_for())
    assert "LÈXIC ANDORRÀ" not in prompt
    assert "REGISTRE ANDORRÀ" not in prompt


@pytest.mark.unit
def test_the_prompt_asks_for_strict_json() -> None:
    assert '"messages"' in build_prompt(request_for())


# ─────────────────────────────────────────────────────────────
# Parsing
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_well_formed_response_becomes_examples() -> None:
    result = parse_response(response(3), request_for(), generator="claude-opus-5")
    assert len(result.examples) == 3
    assert result.rejected == []
    example = result.examples[0]
    assert example.type is ExampleType.QA
    assert example.topic == "cultura/falles-solstici"
    assert example.generator == "claude-opus-5"
    assert example.split is Split.TRAIN
    assert len(example.grounding_ids) == 6


@pytest.mark.unit
def test_grounding_is_the_passages_that_were_actually_sent() -> None:
    """The anti-hallucination link: every example records what it was generated from."""
    request = request_for()
    result = parse_response(response(1), request, generator="g")
    assert result.examples[0].grounding_ids == [p.id for p in request.passages]


@pytest.mark.unit
def test_judge_score_starts_at_zero_meaning_unjudged() -> None:
    result = parse_response(response(1), request_for(), generator="g")
    assert result.examples[0].judge_score == 0.0


@pytest.mark.unit
def test_a_json_fence_is_tolerated() -> None:
    fenced = f"```json\n{response(2)}\n```"
    assert len(parse_response(fenced, request_for(), generator="g").examples) == 2


@pytest.mark.unit
def test_a_non_json_response_is_rejected_with_a_reason() -> None:
    result = parse_response("Ho sento, no puc.", request_for(), generator="g")
    assert result.examples == []
    assert "was not JSON" in result.rejected[0]


@pytest.mark.unit
def test_a_json_object_instead_of_an_array_is_rejected() -> None:
    result = parse_response('{"messages": []}', request_for(), generator="g")
    assert "expected a JSON array" in result.rejected[0]


@pytest.mark.unit
def test_a_malformed_item_is_rejected_not_repaired() -> None:
    """A silently patched example is one nobody wrote and nobody reviewed."""
    payload = json.dumps(
        [
            {
                "messages": [
                    {"role": "user", "content": "Bé?"},
                    {"role": "assistant", "content": "Sí."},
                ]
            },
            {"nota": "sense messages"},
            {"messages": [{"role": "assistant", "content": "Comença malament."}]},
        ]
    )
    result = parse_response(payload, request_for(), generator="g")
    assert len(result.examples) == 1
    assert len(result.rejected) == 2
    assert "has no 'messages'" in result.rejected[0]


@pytest.mark.unit
def test_a_response_violating_the_type_shape_is_rejected() -> None:
    # A single-turn payload for type=multiturn breaks §3.2, so it must not be accepted.
    result = parse_response(response(1), request_for(ExampleType.MULTITURN), generator="g")
    assert result.examples == []
    assert result.rejected


@pytest.mark.unit
def test_ids_are_derived_from_content_so_a_rerun_does_not_duplicate() -> None:
    request = request_for()
    first = parse_response(response(2), request, generator="g")
    second = parse_response(response(2), request, generator="g")
    assert [e.id for e in first.examples] == [e.id for e in second.examples]


@pytest.mark.unit
def test_different_content_gets_different_ids() -> None:
    request = request_for()
    result = parse_response(response(3), request, generator="g")
    assert len({e.id for e in result.examples}) == 3


# ─────────────────────────────────────────────────────────────
# Budget
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_budget_stops_on_requests_or_examples() -> None:
    budget = Budget(max_requests=2, max_examples=100)
    assert budget.can_continue()
    budget.record(5)
    budget.record(5)
    assert not budget.can_continue()

    budget = Budget(max_requests=100, max_examples=6)
    budget.record(6)
    assert not budget.can_continue()
    assert budget.remaining_examples == 0


@pytest.mark.unit
def test_remaining_examples_never_goes_negative() -> None:
    budget = Budget(max_requests=10, max_examples=5)
    budget.record(9)
    assert budget.remaining_examples == 0


# ─────────────────────────────────────────────────────────────
# One node, and the whole batch
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_generate_node_sends_the_prompt_and_parses_the_reply() -> None:
    generator = ScriptedGenerator(response(2))
    result = generate_node(generator, request_for(), generator_name="claude-opus-5")
    assert len(result.examples) == 2
    assert "REGLES INVIOLABLES" in generator.prompts[0]


@pytest.mark.unit
def test_a_batch_covers_the_taxonomy_and_respects_the_budget() -> None:
    documents = falles_corpus(20)
    partition = all_train(documents)
    taxonomy = taxonomy_of(NODE)
    budget = Budget(max_requests=3, max_examples=50)
    result = generate_batch(
        ShapeAwareGenerator(2),
        taxonomy,
        documents,
        partition,
        frozen_digest=partition.digest,
        total=100,
        budget=budget,
        generator_name="claude-opus-5",
        seed=1,
    )
    assert budget.requests == 3
    assert len(result.examples) == 6
    assert any("budget exhausted" in reason for reason in result.rejected)


@pytest.mark.unit
def test_a_batch_requests_several_types_per_node() -> None:
    documents = falles_corpus(20)
    partition = all_train(documents)
    generator = ShapeAwareGenerator(1)
    generate_batch(
        generator,
        taxonomy_of(NODE),
        documents,
        partition,
        frozen_digest=partition.digest,
        total=100,
        budget=Budget(max_requests=20, max_examples=200),
        generator_name="g",
        seed=1,
    )
    requested = {prompt.split("TIPUS: ")[1].split(" ")[0] for prompt in generator.prompts}
    assert len(requested) >= 5
    assert "no_ho_se" in requested
    assert "general_ca" not in requested  # comes from AINA in M2.04, not from the corpus


@pytest.mark.unit
def test_a_batch_refuses_a_partition_that_moved_after_the_freeze() -> None:
    documents = falles_corpus(12)
    partition = all_train(documents)
    with pytest.raises(ContaminationError, match="after the B1 freeze"):
        generate_batch(
            ScriptedGenerator(response(1)),
            taxonomy_of(NODE),
            documents,
            partition,
            frozen_digest="0" * 64,
            total=10,
            budget=Budget(max_requests=5, max_examples=10),
            generator_name="g",
            seed=1,
        )


@pytest.mark.unit
def test_a_batch_refuses_an_unapproved_taxonomy() -> None:
    """M2.01's gate, enforced where the money is spent."""
    documents = falles_corpus(12)
    partition = all_train(documents)
    with pytest.raises(NotApprovedError):
        generate_batch(
            ScriptedGenerator(response(1)),
            taxonomy_of(NODE, approved=False),
            documents,
            partition,
            frozen_digest=partition.digest,
            total=10,
            budget=Budget(max_requests=5, max_examples=10),
            generator_name="g",
            seed=1,
        )


@pytest.mark.unit
def test_a_node_with_too_few_passages_reports_every_grounded_type() -> None:
    documents = falles_corpus(MIN_PASSAGES - 1)
    partition = all_train(documents)
    result = generate_batch(
        ScriptedGenerator(response(1)),
        taxonomy_of(NODE),
        documents,
        partition,
        frozen_digest=partition.digest,
        total=20,
        budget=Budget(max_requests=20, max_examples=50),
        generator_name="g",
        seed=1,
    )
    skipped = [r for r in result.rejected if "needed to ground it" in r]
    assert skipped
    # No grounded example can have been produced from a corpus that cannot ground one.
    grounded = {t for t in ExampleType if t.requires_grounding()}
    assert all(example.type not in grounded for example in result.examples)


@pytest.mark.unit
def test_the_batch_passes_the_glossary_into_the_prompt() -> None:
    documents = falles_corpus(12)
    partition = all_train(documents)
    glossary = Glossary.model_validate(
        {
            "version": "t",
            "entries": [
                {
                    "term": "falla",
                    "category": "cultural",
                    "gloss": "Torxa encesa del solstici d'estiu.",
                }
            ],
        }
    )
    generator = ScriptedGenerator(response(1))
    generate_batch(
        generator,
        taxonomy_of(NODE),
        documents,
        partition,
        frozen_digest=partition.digest,
        total=10,
        budget=Budget(max_requests=1, max_examples=10),
        generator_name="g",
        glossary=glossary,
        seed=1,
    )
    assert "LÈXIC ANDORRÀ" in generator.prompts[0]


@pytest.mark.unit
def test_render_summarises_and_truncates() -> None:
    documents = falles_corpus(MIN_PASSAGES - 1)
    partition = all_train(documents)
    nodes = [
        TaxonomyNode.model_validate({**NODE.model_dump(), "id": f"cultura/node-{index}"})
        for index in range(30)
    ]
    budget = Budget(max_requests=100, max_examples=500)
    result = generate_batch(
        ScriptedGenerator(response(1)),
        taxonomy_of(*nodes),
        documents,
        partition,
        frozen_digest=partition.digest,
        total=300,
        budget=budget,
        generator_name="g",
        seed=1,
    )
    rendered = render(result, budget)
    assert "rejection(s)" in rendered
    assert "and" in rendered and "more" in rendered


# ─────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────


@pytest.fixture
def workspace(tmp_path: Path) -> dict[str, Path]:
    documents = [
        *falles_corpus(12),
        # More than one spoken document: a source with a single document has all of it held
        # back for the benchmark, so it would never reach a prompt as a style few-shot.
        *(
            document(
                f"Doncs miri, les falles són una cosa que la canalla espera tot l'any, ves. ({i})",
                source=Source.CONSELL_DIARI_SESSIONS,
                registre=Registre.ANDORRA_PARLAT,
            )
            for i in range(4)
        ),
    ]
    corpus_path = tmp_path / "corpus.jsonl"
    corpus_path.write_text(
        "".join(f"{doc.model_dump_json()}\n" for doc in documents), encoding="utf-8"
    )

    taxonomy_path = tmp_path / "taxonomy.yaml"
    taxonomy_path.write_text(
        yaml.safe_dump(
            {
                "version": "t",
                "approved": True,
                "approved_by": "Eric Risco",
                "nodes": [NODE.model_dump()],
            }
        ),
        encoding="utf-8",
    )

    partition = split_corpus(documents, bench_share=0.15, seed=1)
    partition_path = tmp_path / "pools.json"
    partition_path.write_text(partition.to_json(), encoding="utf-8")

    return {
        "corpus": corpus_path,
        "taxonomy": taxonomy_path,
        "partition": partition_path,
        "digest": Path(partition.digest),
    }


@pytest.mark.unit
def test_cli_dry_run_prints_the_prompt_without_calling_the_api(
    workspace: dict[str, Path], capsys: pytest.CaptureFixture[str]
) -> None:
    exit_code = main(
        [
            "--corpus",
            str(workspace["corpus"]),
            "--taxonomy",
            str(workspace["taxonomy"]),
            "--partition",
            str(workspace["partition"]),
            "--frozen-digest",
            str(workspace["digest"]),
            "--dry-run",
        ]
    )
    assert exit_code == 0
    out = capsys.readouterr().out
    assert "REGLES INVIOLABLES" in out
    assert "[PASSATGE 1]" in out
    assert "REGISTRE ANDORRÀ" in out  # the spoken document became a style few-shot


@pytest.mark.unit
def test_cli_refuses_a_stale_frozen_digest(
    workspace: dict[str, Path], capsys: pytest.CaptureFixture[str]
) -> None:
    exit_code = main(
        [
            "--corpus",
            str(workspace["corpus"]),
            "--taxonomy",
            str(workspace["taxonomy"]),
            "--partition",
            str(workspace["partition"]),
            "--frozen-digest",
            "0" * 64,
            "--dry-run",
        ]
    )
    assert exit_code == 1
    assert "B1 freeze" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_reports_a_missing_file(
    workspace: dict[str, Path], capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    exit_code = main(
        [
            "--corpus",
            str(tmp_path / "absent.jsonl"),
            "--taxonomy",
            str(workspace["taxonomy"]),
            "--partition",
            str(workspace["partition"]),
            "--frozen-digest",
            str(workspace["digest"]),
            "--dry-run",
        ]
    )
    assert exit_code == 1
    assert "no such file" in capsys.readouterr().err


# ─────────────────────────────────────────────────────────────
# The Anthropic wiring (an API key and spend are blocked-by-resource)
# ─────────────────────────────────────────────────────────────


@dataclass
class FakeBlock:
    type: str
    text: str = ""


@dataclass
class FakeMessage:
    content: list[FakeBlock]
    stop_reason: str | None = "end_turn"


@dataclass
class FakeMessages:
    """Records the request the real Messages API would have received."""

    reply: FakeMessage
    calls: list[dict[str, object]] = field(default_factory=list)

    def create(self, **kwargs: object) -> FakeMessage:
        self.calls.append(kwargs)
        return self.reply


@dataclass
class FakeClient:
    messages: FakeMessages


def fake_client(*blocks: FakeBlock, stop_reason: str | None = "end_turn") -> FakeClient:
    return FakeClient(FakeMessages(FakeMessage(list(blocks), stop_reason)))


@pytest.mark.unit
def test_the_anthropic_generator_joins_text_blocks_and_skips_the_rest() -> None:
    # Thinking is on by default on Claude Opus 5, so the response carries non-text blocks.
    client = fake_client(
        FakeBlock("thinking"), FakeBlock("text", "[{"), FakeBlock("text", '"messages": []}]')
    )
    generator = AnthropicGenerator(client, model="claude-opus-5")
    assert generator.complete("prompt") == '[{"messages": []}]'


@pytest.mark.unit
def test_the_generator_sends_the_documented_request() -> None:
    client = fake_client(FakeBlock("text", "[]"))
    AnthropicGenerator(client, model="claude-opus-5").complete("el prompt")
    sent = client.messages.calls[0]
    assert sent["model"] == "claude-opus-5"
    assert sent["messages"] == [{"role": "user", "content": "el prompt"}]
    # Non-streaming, and thinking counts against the same budget as the response text — a
    # tight max_tokens truncates the JSON array and the parser then rejects the whole batch.
    assert sent["max_tokens"] == 16_000


@pytest.mark.unit
def test_fallbacks_are_on_by_default_and_can_be_turned_off() -> None:
    """Opus 5's classifiers can decline benign adjacent work; a fallback saves the batch."""
    client = fake_client(FakeBlock("text", "[]"))
    AnthropicGenerator(client).complete("p")
    assert client.messages.calls[0]["fallbacks"] == "default"
    assert client.messages.calls[0]["betas"] == ["server-side-fallback-2026-07-01"]

    plain = fake_client(FakeBlock("text", "[]"))
    AnthropicGenerator(plain, use_fallbacks=False).complete("p")
    assert "fallbacks" not in plain.messages.calls[0]


@pytest.mark.unit
def test_a_refusal_raises_rather_than_looking_like_an_empty_batch() -> None:
    """A decline is HTTP 200 with an empty content array.

    Read unconditionally, it would look like a node that simply produced nothing — the batch
    would continue and the gap would only surface in the M2.09 distribution report.
    """
    client = fake_client(stop_reason="refusal")
    with pytest.raises(RefusalError, match="declined"):
        AnthropicGenerator(client, model="claude-opus-5").complete("prompt")


@pytest.mark.unit
def test_max_tokens_is_overridable() -> None:
    client = fake_client(FakeBlock("text", "[]"))
    AnthropicGenerator(client, max_tokens=4096).complete("p")
    assert client.messages.calls[0]["max_tokens"] == 4096


@pytest.mark.unit
def test_the_real_client_can_be_built_without_contacting_anything() -> None:
    # Constructing the SDK client is offline; the key is only used when a call is made.
    assert hasattr(anthropic_client(api_key="sk-ant-not-a-real-key"), "messages")


@pytest.mark.unit
def test_cli_live_path_generates_through_the_injected_client(
    workspace: dict[str, Path], capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    # The only blocked-by-resource part of the live path is the authenticated client.
    client = fake_client(FakeBlock("text", response(2)))
    monkeypatch.setattr("maia.synth.generate.anthropic_client", lambda: client)
    out_path = workspace["corpus"].parent / "dataset.jsonl"
    exit_code = main(
        [
            "--corpus",
            str(workspace["corpus"]),
            "--taxonomy",
            str(workspace["taxonomy"]),
            "--partition",
            str(workspace["partition"]),
            "--frozen-digest",
            str(workspace["digest"]),
            "--total",
            "10",
            "--max-requests",
            "1",
            "--out",
            str(out_path),
        ]
    )
    assert exit_code == 0
    assert "generated 2 example(s)" in capsys.readouterr().out
    assert len(out_path.read_text(encoding="utf-8").splitlines()) == 2


@pytest.mark.unit
def test_largest_remainder_is_exact_and_deterministic() -> None:
    """The shared allocator behind both plan_types and node_quota.

    They used to be two near-identical copies; unifying them removed the duplication and the
    branches only one of the two ever reached.
    """
    thirds = {"a": 1 / 3, "b": 1 / 3, "c": 1 / 3}
    allocation = largest_remainder(thirds, 100, lambda key: key)
    assert sum(allocation.values()) == 100
    # 33.33 each: floors to 99, and the single leftover unit goes to the first tie-break key.
    assert allocation == {"a": 34, "b": 33, "c": 33}
    assert largest_remainder(thirds, 100, lambda key: key) == allocation


@pytest.mark.unit
@pytest.mark.parametrize("total", [0, -3])
def test_largest_remainder_allocates_nothing_for_no_total(total: int) -> None:
    assert largest_remainder({"a": 1.0}, total, lambda key: key) == {}


@pytest.mark.unit
def test_largest_remainder_allocates_nothing_for_no_shares() -> None:
    assert largest_remainder({}, 100, lambda key: key) == {}


@pytest.mark.unit
def test_node_quota_distributes_the_leftover_unit() -> None:
    nodes = [
        TaxonomyNode.model_validate({**NODE.model_dump(), "id": f"cultura/node-{index}"})
        for index in range(3)
    ]
    quota = node_quota(taxonomy_of(*nodes), 100)
    assert sum(quota.values()) == 100
    assert sorted(quota.values()) == [33, 33, 34]


@pytest.mark.unit
def test_cli_dry_run_includes_the_glossary_when_given(
    workspace: dict[str, Path], tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    glossary_path = tmp_path / "glossari.yaml"
    glossary_path.write_text(
        yaml.safe_dump(
            {
                "version": "t",
                "entries": [
                    {
                        "term": "falla",
                        "category": "cultural",
                        "gloss": "Torxa encesa del solstici d'estiu.",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    assert (
        main(
            [
                "--corpus",
                str(workspace["corpus"]),
                "--taxonomy",
                str(workspace["taxonomy"]),
                "--partition",
                str(workspace["partition"]),
                "--frozen-digest",
                str(workspace["digest"]),
                "--glossary",
                str(glossary_path),
                "--dry-run",
            ]
        )
        == 0
    )
    assert "LÈXIC ANDORRÀ" in capsys.readouterr().out


@pytest.mark.unit
def test_cli_reports_a_refusal_to_start_rather_than_spending(
    workspace: dict[str, Path],
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An unapproved taxonomy must stop the run before any API spend."""
    monkeypatch.setattr("maia.synth.generate.anthropic_client", lambda: fake_client())
    unapproved = tmp_path / "taxonomy.yaml"
    unapproved.write_text(
        yaml.safe_dump({"version": "t", "approved": False, "nodes": [NODE.model_dump()]}),
        encoding="utf-8",
    )
    exit_code = main(
        [
            "--corpus",
            str(workspace["corpus"]),
            "--taxonomy",
            str(unapproved),
            "--partition",
            str(workspace["partition"]),
            "--frozen-digest",
            str(workspace["digest"]),
        ]
    )
    assert exit_code == 1
    assert "not approved" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_without_out_still_reports(
    workspace: dict[str, Path], capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        "maia.synth.generate.anthropic_client", lambda: fake_client(FakeBlock("text", response(1)))
    )
    exit_code = main(
        [
            "--corpus",
            str(workspace["corpus"]),
            "--taxonomy",
            str(workspace["taxonomy"]),
            "--partition",
            str(workspace["partition"]),
            "--frozen-digest",
            str(workspace["digest"]),
            "--total",
            "5",
            "--max-requests",
            "1",
        ]
    )
    assert exit_code == 0
    assert "generated 1 example(s)" in capsys.readouterr().out


@pytest.mark.unit
def test_the_taxonomy_schema_is_what_makes_node_quota_safe() -> None:
    # node_quota divides by the weight sum with no guard; the schema is the guarantee.
    with pytest.raises(ValueError):
        TaxonomyNode.model_validate({**NODE.model_dump(), "weight": 0.0})
    with pytest.raises(ValueError):
        taxonomy_of()  # a taxonomy needs at least one node


@pytest.mark.unit
def test_style_excerpts_never_carry_pool_bench_or_restricted_text() -> None:
    """The invisible leak an adversarial review found.

    An excerpt is pasted into the prompt but never recorded in ``grounding_ids``, so no
    downstream validator can see it. Every prompt in a batch was carrying up to 400 characters
    of ``pool_bench`` RTVA text — ``no-redistribute``, under an instruction to imitate it —
    breaking the B1 anti-contamination guarantee and the licence rule at once.
    """
    bench = document(
        "NOMÉS PER AL BENCHMARK: el pressupost del Comú és de quaranta-dos milions.",
        source=Source.RTVA,
        license=License.NO_REDISTRIBUTE,
        registre=Registre.ANDORRA_PARLAT_ORAL,
    )
    restricted = document(
        "Dins de pool_train però no publicable, no ha de sortir al prompt.",
        source=Source.RTVA,
        license=License.NO_REDISTRIBUTE,
        registre=Registre.ANDORRA_PARLAT_ORAL,
    )
    publishable = document(
        "Doncs miri, jo hi vaig cada any i sempre és igual d'emocionant, ves.",
        source=Source.CONSELL_DIARI_SESSIONS,
        registre=Registre.ANDORRA_PARLAT,
    )
    corpus = [bench, restricted, publishable]
    partition = Partition(frozenset({restricted.id, publishable.id}), frozenset({bench.id}))
    excerpts = style_excerpts(corpus, partition, count=5, rng=Random(1))
    assert excerpts == [publishable.text]


@pytest.mark.unit
def test_a_batch_never_puts_pool_bench_text_in_a_prompt() -> None:
    passages = falles_corpus(12)
    bench = document(
        "NOMÉS BENCHMARK: dada reservada per a AndBench, mai a un prompt.",
        source=Source.RTVA,
        license=License.NO_REDISTRIBUTE,
        registre=Registre.ANDORRA_PARLAT_ORAL,
    )
    documents = [*passages, bench]
    partition = Partition(frozenset(d.id for d in passages), frozenset({bench.id}))
    generator = ShapeAwareGenerator(1)
    generate_batch(
        generator,
        taxonomy_of(NODE),
        documents,
        partition,
        frozen_digest=partition.digest,
        total=20,
        budget=Budget(max_requests=3, max_examples=20),
        generator_name="g",
        seed=1,
    )
    assert generator.prompts
    assert not any("NOMÉS BENCHMARK" in prompt for prompt in generator.prompts)
