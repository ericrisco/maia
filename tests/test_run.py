"""Tests for full-scale, resumable generation (PLAN M2.07)."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path

import pytest

from maia.schemas import CorpusDocument, ExampleType, License, Registre, Source, compute_id
from maia.synth.pools import Partition
from maia.synth.run import (
    DEFAULT_MAX_USD,
    MAX_CONSECUTIVE_FAILURES,
    PRICES,
    SAFETY_MARGIN,
    Attempt,
    CharacterEstimate,
    Price,
    RunReport,
    Spend,
    attempts_by_key,
    coverage,
    deficit,
    ledger_path_for,
    main,
    passage_seed,
    plan_run,
    read_ledger,
    read_partial,
    render,
    run_generation,
)
from maia.synth.taxonomy import Taxonomy

MODEL = "claude-opus-5"


def document(index: int) -> CorpusDocument:
    text = (
        f"El Consell General es compon de vint-i-vuit consellers generals. Passatge {index} amb "
        f"prou text per servir de font a la generació d'exemples sobre les institucions del "
        f"Principat, incloent-hi el detall número {index} que el distingeix dels altres."
    )
    return CorpusDocument.model_validate(
        {
            "id": compute_id(text),
            "text": text,
            "source": Source.JURIDIC.value,
            "url": f"https://www.portaljuridicandorra.ad/llei/{index}",
            "fetched_at": "2026-07-25T10:00:00+00:00",
            "license": License.PUBLIC_OFFICIAL.value,
            "registre": Registre.ESTANDARD.value,
            "lang": "ca",
        }
    )


DOCUMENTS = [document(index) for index in range(24)]


def taxonomy(nodes: int = 2) -> Taxonomy:
    return Taxonomy.model_validate(
        {
            "version": "test",
            "approved": True,
            "approved_by": "PO",
            "nodes": [
                {
                    "id": f"institucions/node-{index}",
                    "label": f"Node {index}",
                    "keywords": ["consell", "general", "consellers"],
                    "weight": 1.0,
                }
                for index in range(nodes)
            ],
        }
    )


def partition() -> Partition:
    return Partition(train=frozenset(doc.id for doc in DOCUMENTS), bench=frozenset())


PARTITION = partition()
DIGEST = PARTITION.digest


@dataclass
class ScriptedGenerator:
    """The injected model.

    Its answers are derived **from the prompt**, which is the property that matters here: a real
    model given different passages writes different examples, and a real model given the identical
    prompt writes much the same thing. A fake that ignored the prompt could not tell a resumed run
    that made progress from one that stalled — the exact bug this module exists to prevent.
    """

    calls: int = 0
    prompts: list[str] = field(default_factory=list)
    fail_with: type[Exception] | None = None
    fail_after: int = 0
    per_call: int = 2

    def complete(self, prompt: str) -> str:
        self.calls += 1
        self.prompts.append(prompt)
        if self.fail_with is not None and self.calls > self.fail_after:
            raise self.fail_with("the model was unavailable")
        tag = hashlib.blake2b(prompt.encode(), digest_size=6).hexdigest()
        # §3.2 requires a multiturn example to have more than one exchange.
        extra = "multiturn" in prompt
        return json.dumps(
            [
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": f"Pregunta {tag}.{index} sobre el Consell General?",
                        },
                        {
                            "role": "assistant",
                            "content": f"Resposta {tag}.{index}: vint-i-vuit consellers.",
                        },
                        *(
                            [
                                {"role": "user", "content": f"I qui els presideix, {tag}?"},
                                {"role": "assistant", "content": "El síndic general."},
                            ]
                            if extra
                            else []
                        ),
                    ]
                }
                for index in range(self.per_call)
            ],
            ensure_ascii=False,
        )


def go(
    tmp_path: Path,
    generator: ScriptedGenerator,
    *,
    total: int = 8,
    max_usd: float = DEFAULT_MAX_USD,
    max_requests: int | None = None,
    out: Path | None = None,
    nodes: int = 2,
) -> tuple[RunReport, Path]:
    target = out or tmp_path / "dataset.jsonl"
    report = run_generation(
        generator,
        taxonomy(nodes),
        DOCUMENTS,
        PARTITION,
        out=target,
        frozen_digest=DIGEST,
        total=total,
        generator_name=MODEL,
        model=MODEL,
        seed=1,
        max_usd=max_usd,
        max_requests=max_requests,
    )
    return report, target


# ─────────────────────────────────────────────────────────────
# Planning and the deficit
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_plan_allocates_the_whole_total_exactly() -> None:
    plan = plan_run(taxonomy(4), 1_000)
    assert sum(plan.values()) == 1_000


@pytest.mark.unit
def test_the_plan_is_deterministic() -> None:
    assert plan_run(taxonomy(3), 500) == plan_run(taxonomy(3), 500)


@pytest.mark.unit
def test_coverage_reads_the_partial_dataset_as_the_checkpoint(tmp_path: Path) -> None:
    """No side-car progress file that can disagree with the data."""
    _, out = go(tmp_path, ScriptedGenerator())
    counts = coverage(read_partial(out))
    assert sum(counts.values()) == len(read_partial(out))
    assert all(node.startswith("institucions/") for node, _ in counts)


@pytest.mark.unit
def test_the_deficit_is_what_is_still_owed() -> None:
    plan = {("a", ExampleType.QA): 10, ("b", ExampleType.QA): 5}
    done = {("a", ExampleType.QA): 4}
    assert deficit(plan, done) == {("a", ExampleType.QA): 6, ("b", ExampleType.QA): 5}


@pytest.mark.unit
def test_over_production_is_ignored_not_clawed_back() -> None:
    plan = {("a", ExampleType.QA): 10}
    assert deficit(plan, {("a", ExampleType.QA): 40}) == {}


# ─────────────────────────────────────────────────────────────
# Resuming — the point of the module
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_run_appends_and_flushes_so_a_crash_costs_one_request(tmp_path: Path) -> None:
    """The output file is written as the run goes, not at the end."""
    generator = ScriptedGenerator(fail_with=RuntimeError, fail_after=2)
    report, out = go(tmp_path, generator, total=40)
    assert out.is_file()
    assert report.produced > 0
    assert report.failures > 0
    # Everything written before the failures is still there.
    assert len(read_partial(out)) == report.produced


@pytest.mark.unit
def test_resuming_continues_rather_than_starting_over(tmp_path: Path) -> None:
    first, out = go(tmp_path, ScriptedGenerator(), total=40, max_requests=2)
    assert not first.complete
    after_first = len(read_partial(out))
    assert after_first > 0

    second, _ = go(tmp_path, ScriptedGenerator(), total=40, max_requests=2, out=out)
    assert second.resumed_from == after_first
    assert second.produced > 0
    assert len(read_partial(out)) == after_first + second.produced


@pytest.mark.unit
def test_a_resumed_run_samples_different_passages_and_makes_progress(tmp_path: Path) -> None:
    """The trap: same seed, same passages, colliding UUID5 ids, budget spent for nothing.

    The passage draw is offset by the attempt count from the ledger, so the second attempt at a
    pair looks at a different part of the corpus.
    """
    first_generator = ScriptedGenerator()
    _, out = go(tmp_path, first_generator, total=40, max_requests=1)
    first_prompt = first_generator.prompts[0]

    second_generator = ScriptedGenerator()
    report, _ = go(tmp_path, second_generator, total=40, max_requests=1, out=out)
    assert report.produced > 0, "a resumed run that produces nothing has stalled"
    assert second_generator.prompts[0] != first_prompt


@pytest.mark.unit
def test_the_attempt_seed_moves_with_the_attempt_number() -> None:
    base = passage_seed(1, "institucions/a", ExampleType.QA, 0)
    assert passage_seed(1, "institucions/a", ExampleType.QA, 1) != base
    assert passage_seed(1, "institucions/a", ExampleType.QA, 0) == base
    assert passage_seed(2, "institucions/a", ExampleType.QA, 0) != base
    assert passage_seed(1, "institucions/b", ExampleType.QA, 0) != base
    assert passage_seed(1, "institucions/a", ExampleType.RESUM, 0) != base


@pytest.mark.unit
def test_the_attempt_seed_is_stable_across_processes() -> None:
    """`hash()` over a string is salted per process, so a resumed run would draw differently for
    reasons unrelated to the attempt number."""
    assert passage_seed(20260725, "institucions/consell-general", ExampleType.QA, 0) == (
        passage_seed(20260725, "institucions/consell-general", ExampleType.QA, 0)
    )
    # A fixed expectation, so a change of derivation is a visible change.
    assert passage_seed(1, "n", ExampleType.QA, 0) == 10_611_945_639_798_062_293


@pytest.mark.unit
def test_an_already_covered_target_does_nothing(tmp_path: Path) -> None:
    generator = ScriptedGenerator()
    _, out = go(tmp_path, generator, total=4)
    calls = generator.calls

    again = ScriptedGenerator()
    report, _ = go(tmp_path, again, total=4, out=out)
    assert again.calls == 0
    assert "already covered" in report.stopped_early
    assert calls > 0


@pytest.mark.unit
def test_duplicate_examples_are_not_written_twice(tmp_path: Path) -> None:
    """Two calls returning identical content produce identical UUID5 ids."""

    @dataclass
    class Repeating:
        calls: int = 0

        def complete(self, prompt: str) -> str:
            self.calls += 1
            return json.dumps(
                [
                    {
                        "messages": [
                            {"role": "user", "content": "Sempre la mateixa pregunta?"},
                            {"role": "assistant", "content": "Sempre la mateixa resposta."},
                        ]
                    }
                ],
                ensure_ascii=False,
            )

    report, out = go(tmp_path, Repeating(), total=8, nodes=1)  # type: ignore[arg-type]
    lines = read_partial(out)
    assert len({example.id for example in lines}) == len(lines)
    assert report.duplicates > 0
    assert "not written twice" in render(report)


@pytest.mark.unit
def test_the_ledger_records_every_request(tmp_path: Path) -> None:
    report, out = go(tmp_path, ScriptedGenerator(), total=8)
    ledger = read_ledger(ledger_path_for(out))
    assert len(ledger) == report.requests
    assert all(entry.input_tokens > 0 for entry in ledger)
    assert all(entry.node.startswith("institucions/") for entry in ledger)


@pytest.mark.unit
def test_the_ledger_survives_a_round_trip() -> None:
    entry = Attempt(
        node="institucions/a",
        example_type="qa",
        asked=5,
        kept=4,
        input_tokens=1_200,
        output_tokens=300,
        usd=0.0135,
        error="RefusalError: declined",
    )
    assert Attempt.from_json(entry.to_json()) == entry


@pytest.mark.unit
@pytest.mark.parametrize("line", ["not json", "{}", '{"node": "a"}', "[1, 2]"])
def test_an_unreadable_ledger_line_is_refused(line: str) -> None:
    """A ledger that cannot be read cannot be resumed from, and guessing would repeat spend."""
    with pytest.raises(ValueError, match="not a ledger entry"):
        Attempt.from_json(line)


@pytest.mark.unit
def test_attempt_counts_come_from_the_ledger() -> None:
    ledger = [
        Attempt("a", "qa", 1, 1, 1, 1, 0.0),
        Attempt("a", "qa", 1, 0, 1, 0, 0.0, error="boom"),
        Attempt("b", "resum", 1, 1, 1, 1, 0.0),
    ]
    assert attempts_by_key(ledger) == {
        ("a", ExampleType.QA): 2,
        ("b", ExampleType.RESUM): 1,
    }


@pytest.mark.unit
def test_a_ledger_entry_for_an_unknown_type_is_skipped_not_fatal() -> None:
    """Forward compatibility: a ledger written by a build that knew more types still reads."""
    assert attempts_by_key([Attempt("a", "some_future_type", 1, 1, 1, 1, 0.0)]) == {}


@pytest.mark.unit
def test_reading_a_run_that_has_not_started_yields_nothing(tmp_path: Path) -> None:
    assert read_partial(tmp_path / "absent.jsonl") == []
    assert read_ledger(tmp_path / "absent.ledger.jsonl") == []


# ─────────────────────────────────────────────────────────────
# Money
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_price_table_matches_the_published_rates() -> None:
    assert PRICES[MODEL] == Price(input_usd=5.0, output_usd=25.0)
    assert PRICES["claude-haiku-4-5"].input_usd == 1.0


@pytest.mark.unit
def test_cost_is_per_million_tokens() -> None:
    assert Price(input_usd=5.0, output_usd=25.0).cost(1_000_000, 1_000_000) == pytest.approx(30.0)
    assert Price(input_usd=5.0, output_usd=25.0).cost(1_000, 0) == pytest.approx(0.005)


@pytest.mark.unit
def test_an_unpriced_model_refuses_to_run(tmp_path: Path) -> None:
    """Reporting a spend of zero would be worse than refusing."""
    with pytest.raises(ValueError, match="no published price"):
        run_generation(
            ScriptedGenerator(),
            taxonomy(),
            DOCUMENTS,
            PARTITION,
            out=tmp_path / "dataset.jsonl",
            frozen_digest=DIGEST,
            total=4,
            generator_name="mystery",
            model="mystery-model-9",
            seed=1,
        )


@pytest.mark.unit
def test_a_run_stops_at_the_budget_ceiling(tmp_path: Path) -> None:
    generator = ScriptedGenerator()
    report, _ = go(tmp_path, generator, total=400, max_usd=0.001)
    assert "budget ceiling reached" in report.stopped_early
    assert not report.complete
    assert generator.calls <= 1


@pytest.mark.unit
def test_the_ceiling_is_applied_with_a_safety_margin() -> None:
    """An under-estimate that walks past the budget is the failure mode worth guarding."""
    spend = Spend(price=PRICES[MODEL])
    spend.record(input_tokens=1_000_000, output_tokens=0)  # $5.00
    assert spend.usd == pytest.approx(5.0)
    assert not spend.would_exceed(10.0, 1.0)
    # 5 + 3 = 8 is under 10, but 8 x 1.25 = 10 sits exactly on the ceiling and is still allowed.
    assert not spend.would_exceed(10.0, 3.0)
    # 5 + 3.1 = 8.1, still under 10 — but 8.1 x 1.25 = 10.125 is over it.
    assert spend.would_exceed(10.0, 3.1)
    assert SAFETY_MARGIN == 1.25


@pytest.mark.unit
def test_spend_is_carried_over_from_the_ledger_when_resuming(tmp_path: Path) -> None:
    """Otherwise every resume restarts the budget at zero and the total spend is unbounded."""
    _, out = go(tmp_path, ScriptedGenerator(), total=40, max_requests=2)
    first_spend = sum(entry.usd for entry in read_ledger(ledger_path_for(out)))
    assert first_spend > 0

    report, _ = go(tmp_path, ScriptedGenerator(), total=40, max_requests=1, out=out)
    assert report.spend_usd > first_spend


@pytest.mark.unit
def test_the_report_says_the_cost_is_estimated(tmp_path: Path) -> None:
    report, _ = go(tmp_path, ScriptedGenerator(), total=4)
    assert "ESTIMATED from character counts" in render(report)


@pytest.mark.unit
def test_the_default_counter_is_characters_over_four() -> None:
    counter = CharacterEstimate()
    assert counter.count("x" * 400) == 100
    assert counter.count("") == 0
    assert counter.count("xx") == 1  # never zero for non-empty text


@pytest.mark.unit
def test_a_custom_counter_is_used_when_given(tmp_path: Path) -> None:
    @dataclass
    class Doubling:
        seen: int = 0

        def count(self, text: str) -> int:
            self.seen += 1
            return len(text)

    counter = Doubling()
    run_generation(
        ScriptedGenerator(),
        taxonomy(1),
        DOCUMENTS,
        PARTITION,
        out=tmp_path / "dataset.jsonl",
        frozen_digest=DIGEST,
        total=4,
        generator_name=MODEL,
        model=MODEL,
        seed=1,
        counter=counter,
    )
    assert counter.seen > 0


# ─────────────────────────────────────────────────────────────
# Surviving failure
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_one_bad_request_does_not_end_the_run(tmp_path: Path) -> None:
    @dataclass
    class FlakyOnce:
        calls: int = 0

        def complete(self, prompt: str) -> str:
            self.calls += 1
            if self.calls == 1:
                raise TimeoutError("connection reset")
            return json.dumps(
                [
                    {
                        "messages": [
                            {"role": "user", "content": f"Pregunta {self.calls}?"},
                            {"role": "assistant", "content": f"Resposta {self.calls}."},
                        ]
                    }
                ],
                ensure_ascii=False,
            )

    generator = FlakyOnce()
    report, _ = go(tmp_path, generator, total=8)  # type: ignore[arg-type]
    assert generator.calls > 1
    assert report.failures == 1
    assert report.produced > 0
    assert "TimeoutError" in render(report)


@pytest.mark.unit
def test_a_run_where_everything_fails_stops_instead_of_spending_the_budget(
    tmp_path: Path,
) -> None:
    generator = ScriptedGenerator(fail_with=RuntimeError, fail_after=0)
    report, _ = go(tmp_path, generator, total=4_000)
    assert "consecutive failures" in report.stopped_early
    assert generator.calls == MAX_CONSECUTIVE_FAILURES
    assert report.produced == 0


@pytest.mark.unit
def test_a_success_resets_the_consecutive_failure_count(tmp_path: Path) -> None:
    @dataclass
    class Alternating:
        calls: int = 0

        def complete(self, prompt: str) -> str:
            self.calls += 1
            if self.calls % 2:
                raise RuntimeError("flaky")
            return json.dumps(
                [
                    {
                        "messages": [
                            {"role": "user", "content": f"Pregunta {self.calls}?"},
                            {"role": "assistant", "content": f"Resposta {self.calls}."},
                        ]
                    }
                ],
                ensure_ascii=False,
            )

    generator = Alternating()
    report, _ = go(tmp_path, generator, total=60)  # type: ignore[arg-type]
    assert generator.calls > MAX_CONSECUTIVE_FAILURES
    assert "consecutive failures" not in report.stopped_early


@pytest.mark.unit
def test_a_refusal_is_recorded_like_any_other_failure(tmp_path: Path) -> None:
    from maia.synth.generate import RefusalError

    report, _ = go(tmp_path, ScriptedGenerator(fail_with=RefusalError, fail_after=0), total=4)
    assert report.failures > 0
    assert "RefusalError" in report.errors[0]


# ─────────────────────────────────────────────────────────────
# The gates M2.03 refuses to start without
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_contaminated_partition_refuses_to_run(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError):
        run_generation(
            ScriptedGenerator(),
            taxonomy(),
            DOCUMENTS,
            PARTITION,
            out=tmp_path / "dataset.jsonl",
            frozen_digest="0" * 64,
            total=4,
            generator_name=MODEL,
            model=MODEL,
            seed=1,
        )


@pytest.mark.unit
def test_an_unapproved_taxonomy_refuses_to_run(tmp_path: Path) -> None:
    """Otherwise the API budget is spent on the wrong topics."""
    unapproved = Taxonomy.model_validate(
        {
            "version": "test",
            "approved": False,
            "nodes": [
                {"id": "a/b", "label": "T", "keywords": ["consell"], "weight": 1.0},
            ],
        }
    )
    with pytest.raises(RuntimeError):
        run_generation(
            ScriptedGenerator(),
            unapproved,
            DOCUMENTS,
            PARTITION,
            out=tmp_path / "dataset.jsonl",
            frozen_digest=DIGEST,
            total=4,
            generator_name=MODEL,
            model=MODEL,
            seed=1,
        )


@pytest.mark.unit
def test_a_node_without_enough_passages_is_recorded_not_generated(tmp_path: Path) -> None:
    thin = Partition(train=frozenset({DOCUMENTS[0].id}), bench=frozenset())
    report = run_generation(
        ScriptedGenerator(),
        taxonomy(1),
        DOCUMENTS[:1],
        thin,
        out=tmp_path / "dataset.jsonl",
        frozen_digest=thin.digest,
        total=8,
        generator_name=MODEL,
        model=MODEL,
        seed=1,
    )
    assert any("fewer than the" in reason for reason in report.rejected)


# ─────────────────────────────────────────────────────────────
# Reporting
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_finished_run_reports_complete(tmp_path: Path) -> None:
    report, _ = go(tmp_path, ScriptedGenerator(per_call=20), total=4)
    assert report.complete
    assert "✓ complete" in render(report)


@pytest.mark.unit
def test_an_unfinished_run_says_how_to_continue() -> None:
    report = RunReport(target=100, produced=10, requests=5)
    rendered = render(report)
    assert "… incomplete" in rendered
    assert "the output file is the checkpoint" in rendered


@pytest.mark.unit
def test_a_run_stopped_early_says_why_instead(tmp_path: Path) -> None:
    report = RunReport(target=100, produced=10, stopped_early="budget ceiling reached")
    assert "stopped early: budget ceiling reached" in render(report)
    assert "run again to continue" not in render(report)


@pytest.mark.unit
def test_the_request_ceiling_is_reported(tmp_path: Path) -> None:
    report, _ = go(tmp_path, ScriptedGenerator(), total=400, max_requests=2)
    assert "request ceiling reached (2)" in report.stopped_early


# ─────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────


def write_inputs(tmp_path: Path) -> tuple[Path, Path, Path]:
    corpus = tmp_path / "corpus.jsonl"
    corpus.write_text("".join(f"{doc.model_dump_json()}\n" for doc in DOCUMENTS), encoding="utf-8")
    tax = tmp_path / "taxonomy.yaml"
    tax.write_text(
        "version: test\napproved: true\napproved_by: PO\nnodes:\n"
        + "".join(
            f"  - id: institucions/node-{index}\n"
            f"    label: Node {index}\n"
            f"    keywords: [consell, general]\n"
            f"    weight: 1.0\n"
            for index in range(2)
        ),
        encoding="utf-8",
    )
    pools = tmp_path / "partition.json"
    pools.write_text(
        json.dumps(
            {
                "pool_train": sorted(PARTITION.train),
                "pool_bench": sorted(PARTITION.bench),
                "digest": DIGEST,
            }
        ),
        encoding="utf-8",
    )
    return corpus, tax, pools


@pytest.mark.unit
def test_cli_plan_only_never_calls_the_api(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    corpus, tax, pools = write_inputs(tmp_path)
    code = main(
        [
            "--corpus",
            str(corpus),
            "--taxonomy",
            str(tax),
            "--partition",
            str(pools),
            "--frozen-digest",
            DIGEST,
            "--out",
            str(tmp_path / "dataset.jsonl"),
            "--total",
            "100",
            "--plan-only",
        ]
    )
    assert code == 0
    printed = capsys.readouterr().out
    assert "plan: 100 example(s)" in printed
    assert "still owed: 100" in printed


@pytest.mark.unit
def test_cli_plan_only_accounts_for_what_is_already_on_disk(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    corpus, tax, pools = write_inputs(tmp_path)
    _, out = go(tmp_path, ScriptedGenerator(), total=8)
    main(
        [
            "--corpus",
            str(corpus),
            "--taxonomy",
            str(tax),
            "--partition",
            str(pools),
            "--frozen-digest",
            DIGEST,
            "--out",
            str(out),
            "--total",
            "8",
            "--plan-only",
        ]
    )
    printed = capsys.readouterr().out
    assert "already on disk: " in printed
    assert "already on disk: 0\n" not in printed


@pytest.mark.unit
def test_cli_reports_a_missing_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert (
        main(
            [
                "--corpus",
                str(tmp_path / "absent.jsonl"),
                "--taxonomy",
                str(tmp_path / "t.yaml"),
                "--partition",
                str(tmp_path / "p.json"),
                "--frozen-digest",
                DIGEST,
                "--out",
                str(tmp_path / "o.jsonl"),
            ]
        )
        == 1
    )
    assert "no such file" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_reports_a_bad_digest(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    corpus, tax, pools = write_inputs(tmp_path)
    assert (
        main(
            [
                "--corpus",
                str(corpus),
                "--taxonomy",
                str(tax),
                "--partition",
                str(pools),
                "--frozen-digest",
                "0" * 64,
                "--out",
                str(tmp_path / "dataset.jsonl"),
            ]
        )
        == 1
    )
    assert "error:" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_runs_against_an_injected_client(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """The API client is blocked-by-resource, so the seam is patched — not the logic."""
    corpus, tax, pools = write_inputs(tmp_path)
    monkeypatch.setattr("maia.synth.generate.anthropic_client", lambda *a, **k: object())
    monkeypatch.setattr(
        "maia.synth.generate.AnthropicGenerator.complete",
        lambda self, prompt: ScriptedGenerator(per_call=20).complete(prompt),
    )
    code = main(
        [
            "--corpus",
            str(corpus),
            "--taxonomy",
            str(tax),
            "--partition",
            str(pools),
            "--frozen-digest",
            DIGEST,
            "--out",
            str(tmp_path / "dataset.jsonl"),
            "--total",
            "4",
        ]
    )
    assert code == 0
    assert "✓ complete" in capsys.readouterr().out


@pytest.mark.unit
def test_cli_passes_the_glossary_through(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """The glossary is what makes the prompts require Andorran lexicon (M2.02)."""
    corpus, tax, pools = write_inputs(tmp_path)
    glossary = Path(__file__).resolve().parents[1] / "configs" / "glossari-andorra.yaml"
    seen: list[str] = []

    def recording(self: object, prompt: str) -> str:
        seen.append(prompt)
        return ScriptedGenerator(per_call=20).complete(prompt)

    monkeypatch.setattr("maia.synth.generate.anthropic_client", lambda *a, **k: object())
    monkeypatch.setattr("maia.synth.generate.AnthropicGenerator.complete", recording)
    code = main(
        [
            "--corpus",
            str(corpus),
            "--taxonomy",
            str(tax),
            "--partition",
            str(pools),
            "--frozen-digest",
            DIGEST,
            "--glossary",
            str(glossary),
            "--out",
            str(tmp_path / "dataset.jsonl"),
            "--total",
            "4",
        ]
    )
    assert code == 0
    assert seen
    assert "comú" in seen[0]
