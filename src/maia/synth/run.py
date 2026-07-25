"""Full-scale generation — PLAN M2.07.

M2.03 generates a batch. M2.07 generates **10,000-15,000 examples** for 30-60 EUR of API, which is
hundreds of requests over hours, and that changes what the code has to survive:

* **A crash must not cost the run.** ``generate_batch`` returns everything at the end, so a network
  drop at request 300 throws away 300 requests of spend. Here every request is appended to the
  output file and flushed before the next one starts.
* **Resuming must not duplicate, and must not stall.** The partial dataset **is** the checkpoint:
  ``topic`` holds the taxonomy node id and ids are UUID5 over ``(node, messages)``, so
  :func:`coverage` reconstructs exactly what has been produced per ``(node, type)`` with no
  side-car state file to fall out of sync. What is left is the **deficit**, and only that is asked
  for.
* **A resumed request must sample different passages.** This is the trap. Re-running a
  ``(node, type)`` with the same seed draws the same passages, the model returns much the same
  examples, their UUID5 ids collide with what is already on disk, and the run burns budget making
  no progress. So the passage seed is offset by how many attempts that pair has already had —
  recorded in the ledger — and a resumed attempt looks at different parts of the corpus.
* **One bad request must not end the run**, and a run where *everything* fails must not spend the
  whole budget discovering that. Failures are recorded and tolerated up to
  :data:`MAX_CONSECUTIVE_FAILURES` in a row.

The ledger (``<out>.ledger.jsonl``) is the run's accounting: one line per request with the node,
type, how many examples were asked for and kept, the estimated tokens and cost, and any error. It
is what makes the spend auditable after the fact and what makes attempt counting possible.

**Cost is estimated, not measured.** The Anthropic response carries exact ``usage``, but
``TextGenerator.complete`` returns only text, so this module counts characters through an injected
:class:`TokenCounter` (~4 characters per token) and applies :data:`SAFETY_MARGIN` so an
under-estimate cannot walk past the ceiling. Every report says ``estimated``. Reading real ``usage``
is logged in gaps.md as the way to close this.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from random import Random
from typing import Protocol

from maia.schemas import CorpusDocument, DatasetExample, ExampleType, Split
from maia.synth.generate import (
    MIN_PASSAGES,
    GenerationRequest,
    GenerationResult,
    TextGenerator,
    build_prompt,
    categories_for,
    generate_node,
    node_quota,
    plan_types,
    sample_passages,
    style_excerpts,
)
from maia.synth.glossary import Glossary
from maia.synth.pools import Partition, assert_train_only, verify_partition
from maia.synth.taxonomy import Taxonomy, require_approved

#: PRD §4's API budget for the whole of Phase 2, in USD. The plan states €30-60; the API is priced
#: in dollars, so the conversion is the caller's and ``--max-usd`` is what is enforced.
DEFAULT_MAX_USD = 60.0

#: Applied to the estimated spend before comparing it to the ceiling, because the estimate can be
#: low and overshooting a budget is worse than stopping a little early.
SAFETY_MARGIN = 1.25

#: Consecutive failures after which the run stops. One bad request is weather; ten in a row means
#: something is broken and the rest of the budget would be spent learning nothing.
MAX_CONSECUTIVE_FAILURES = 10

#: Rough characters per token for Catalan text. Only used for the cost estimate.
CHARS_PER_TOKEN = 4


@dataclass(frozen=True)
class Price:
    """Per-million-token prices for one model."""

    input_usd: float
    output_usd: float

    def cost(self, input_tokens: int, output_tokens: int) -> float:
        """Cost in USD of one request."""
        return (input_tokens * self.input_usd + output_tokens * self.output_usd) / 1_000_000


#: Published prices, June 2026. A model absent from this table has no price and the run refuses to
#: start rather than reporting a spend of zero.
PRICES: dict[str, Price] = {
    "claude-opus-5": Price(input_usd=5.0, output_usd=25.0),
    "claude-opus-4-8": Price(input_usd=5.0, output_usd=25.0),
    "claude-sonnet-5": Price(input_usd=3.0, output_usd=15.0),
    "claude-haiku-4-5": Price(input_usd=1.0, output_usd=5.0),
}


class TokenCounter(Protocol):
    """Counts tokens in a string. The seam for a real tokenizer."""

    def count(self, text: str) -> int:
        """How many tokens ``text`` is."""


@dataclass(frozen=True)
class CharacterEstimate:
    """The default counter: characters over :data:`CHARS_PER_TOKEN`.

    Deliberately crude and deliberately named. It exists so the budget can be enforced without a
    tokenizer download, and every report that uses it says ``estimated``.
    """

    chars_per_token: int = CHARS_PER_TOKEN

    def count(self, text: str) -> int:
        """Estimated token count."""
        return max(1, len(text) // self.chars_per_token) if text else 0


@dataclass
class Spend:
    """Running account of what the run has cost."""

    price: Price
    input_tokens: int = 0
    output_tokens: int = 0
    requests: int = 0

    @property
    def usd(self) -> float:
        """Estimated spend so far."""
        return self.price.cost(self.input_tokens, self.output_tokens)

    def record(self, input_tokens: int, output_tokens: int) -> None:
        """Account for one completed request."""
        self.input_tokens += input_tokens
        self.output_tokens += output_tokens
        self.requests += 1

    def would_exceed(self, ceiling: float, next_request: float) -> bool:
        """Whether one more request of ``next_request`` USD would break ``ceiling``.

        The estimate is scaled by :data:`SAFETY_MARGIN` first — an under-estimate that walks past
        the budget is the failure mode worth guarding.
        """
        return (self.usd + next_request) * SAFETY_MARGIN > ceiling


@dataclass(frozen=True)
class Attempt:
    """One ledger line: what a single request asked for and what came back."""

    node: str
    example_type: str
    asked: int
    kept: int
    input_tokens: int
    output_tokens: int
    usd: float
    error: str = ""

    def to_json(self) -> str:
        """One JSONL line."""
        return json.dumps(
            {
                "node": self.node,
                "example_type": self.example_type,
                "asked": self.asked,
                "kept": self.kept,
                "input_tokens": self.input_tokens,
                "output_tokens": self.output_tokens,
                "usd": round(self.usd, 6),
                "error": self.error,
            },
            ensure_ascii=False,
        )

    @classmethod
    def from_json(cls, line: str) -> Attempt:
        """Read one ledger line.

        Raises:
            ValueError: if the line is not a ledger entry. A ledger that cannot be read is a
                ledger that cannot be resumed from, and guessing would repeat spend.
        """
        try:
            payload = json.loads(line)
            return cls(
                node=str(payload["node"]),
                example_type=str(payload["example_type"]),
                asked=int(payload["asked"]),
                kept=int(payload["kept"]),
                input_tokens=int(payload["input_tokens"]),
                output_tokens=int(payload["output_tokens"]),
                usd=float(payload["usd"]),
                error=str(payload.get("error", "")),
            )
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            raise ValueError(f"not a ledger entry: {line[:120]!r} ({error})") from error


Key = tuple[str, ExampleType]


def passage_seed(seed: int, node_id: str, example_type: ExampleType, attempt: int) -> int:
    """A per-attempt seed for the passage draw.

    Derived with ``blake2b`` rather than ``hash()``: ``hash`` over a string is salted per process,
    so a resumed run would draw differently for reasons unrelated to the attempt number and the
    same command would not be reproducible. ``attempt`` is what moves the draw — see the module
    docstring on why a resumed request must not re-read the same passages.
    """
    digest = hashlib.blake2b(
        f"{seed}|{node_id}|{example_type.value}|{attempt}".encode(), digest_size=8
    )
    return int.from_bytes(digest.digest(), "big")


def plan_run(taxonomy: Taxonomy, total: int) -> dict[Key, int]:
    """The target: how many examples of each type each node should end up with.

    Deterministic, and the same allocation M2.03 uses — node weight then :data:`TYPE_MIX`, both by
    largest remainder so the totals are exact.
    """
    plan: dict[Key, int] = {}
    for node_id, node_total in node_quota(taxonomy, total).items():
        for example_type, count in plan_types(node_total).items():
            plan[(node_id, example_type)] = count
    return plan


def coverage(examples: Iterable[DatasetExample]) -> dict[Key, int]:
    """What a partial dataset already holds, per ``(node, type)``.

    ``topic`` carries the taxonomy node id (M2.03 writes it there), so the dataset is its own
    checkpoint — no side-car progress file that can disagree with the data.
    """
    counts: dict[Key, int] = {}
    for example in examples:
        key = (example.topic, example.type)
        counts[key] = counts.get(key, 0) + 1
    return counts


def deficit(plan: dict[Key, int], done: dict[Key, int]) -> dict[Key, int]:
    """What is still owed. Over-production is not clawed back, only ignored."""
    return {
        key: target - done.get(key, 0)
        for key, target in plan.items()
        if target - done.get(key, 0) > 0
    }


def attempts_by_key(ledger: Iterable[Attempt]) -> dict[Key, int]:
    """How many requests each ``(node, type)`` has already had, successful or not.

    This is what stops a resumed run from re-drawing the same passages — see the module docstring.
    """
    counts: dict[Key, int] = {}
    for attempt in ledger:
        try:
            key = (attempt.node, ExampleType(attempt.example_type))
        except ValueError:  # a type this build no longer knows: count it under nothing
            continue
        counts[key] = counts.get(key, 0) + 1
    return counts


def read_ledger(path: Path) -> list[Attempt]:
    """Read a run ledger, or return nothing if there is none yet."""
    if not path.is_file():
        return []
    return [
        Attempt.from_json(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def read_partial(path: Path) -> list[DatasetExample]:
    """Read an in-progress output file, or return nothing if there is none yet."""
    if not path.is_file():
        return []
    return [
        DatasetExample.model_validate_json(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def ledger_path_for(out: Path) -> Path:
    """Where the ledger for ``out`` lives."""
    return out.with_suffix(out.suffix + ".ledger.jsonl")


@dataclass
class RunReport:
    """What a full-scale run did."""

    target: int
    resumed_from: int = 0
    produced: int = 0
    requests: int = 0
    failures: int = 0
    duplicates: int = 0
    rejected: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    spend_usd: float = 0.0
    max_usd: float = DEFAULT_MAX_USD
    stopped_early: str = ""

    @property
    def total(self) -> int:
        """Examples in the output file once the run finishes."""
        return self.resumed_from + self.produced

    @property
    def complete(self) -> bool:
        """Whether the target was reached."""
        return self.total >= self.target


def run_generation(
    generator: TextGenerator,
    taxonomy: Taxonomy,
    documents: Sequence[CorpusDocument],
    partition: Partition,
    *,
    out: Path,
    frozen_digest: str,
    total: int,
    generator_name: str,
    model: str = "claude-opus-5",
    glossary: Glossary | None = None,
    seed: int,
    split: Split = Split.TRAIN,
    max_usd: float = DEFAULT_MAX_USD,
    max_requests: int | None = None,
    counter: TokenCounter | None = None,
) -> RunReport:
    """Generate towards ``total`` examples in ``out``, resuming whatever is already there.

    Appends and flushes after every request, so a crash costs one request rather than the run.

    Raises:
        ValueError: if ``model`` has no published price. A run that cannot price itself cannot
            respect a budget, and reporting a spend of zero would be worse than refusing.
        RuntimeError: if the partition does not match ``frozen_digest`` or the taxonomy is not
            PO-approved — the same two gates M2.03 refuses to start without.
    """
    if model not in PRICES:
        raise ValueError(
            f"no published price for {model!r}; known: {', '.join(sorted(PRICES))} — refusing to "
            "run without being able to account for the spend"
        )
    verify_partition(partition, frozen_digest)
    require_approved(taxonomy)

    tokens = counter or CharacterEstimate()
    ledger = ledger_path_for(out)
    existing = read_partial(out)
    history = read_ledger(ledger)
    attempts = attempts_by_key(history)
    seen = {example.id for example in existing}

    spend = Spend(price=PRICES[model])
    for attempt in history:
        spend.record(attempt.input_tokens, attempt.output_tokens)

    report = RunReport(
        target=total, resumed_from=len(existing), max_usd=max_usd, spend_usd=spend.usd
    )
    remaining = deficit(plan_run(taxonomy, total), coverage(existing))
    if not remaining:
        report.stopped_early = "nothing to do: the target is already covered"
        return report

    out.parent.mkdir(parents=True, exist_ok=True)
    excerpts = tuple(style_excerpts(documents, partition, count=3, rng=Random(seed)))
    consecutive = 0

    with out.open("a", encoding="utf-8") as sink, ledger.open("a", encoding="utf-8") as book:
        for (node_id, example_type), owed in sorted(
            remaining.items(), key=lambda item: (item[0][0], item[0][1].value)
        ):
            if max_requests is not None and report.requests >= max_requests:
                report.stopped_early = f"request ceiling reached ({max_requests})"
                break
            if consecutive >= MAX_CONSECUTIVE_FAILURES:
                report.stopped_early = (
                    f"{consecutive} consecutive failures — stopping rather than spending the "
                    "rest of the budget on a broken run"
                )
                break

            node = taxonomy.node(node_id)
            # Offset the draw by past attempts, so a resumed request looks at different passages
            # and does not reproduce ids already on disk.
            attempt_number = attempts.get((node_id, example_type), 0)
            rng = Random(passage_seed(seed, node_id, example_type, attempt_number))
            passages = sample_passages(
                node, documents, partition, example_type=example_type, rng=rng
            )
            if example_type.requires_grounding() and len(passages) < MIN_PASSAGES:
                report.rejected.append(
                    f"{node_id} ({example_type.value}): only {len(passages)} passage(s) in "
                    f"pool_train, fewer than the {MIN_PASSAGES} needed to ground it"
                )
                continue
            assert_train_only(partition, [passage.id for passage in passages])

            request = GenerationRequest(
                node=node,
                example_type=example_type,
                count=owed,
                passages=tuple(passages),
                glossary_lines=tuple(
                    glossary.prompt_lines(categories_for(node)) if glossary else ()
                ),
                style_excerpts=excerpts,
            )
            prompt = build_prompt(request)
            input_tokens = tokens.count(prompt)
            # Assume the answer is as long as the prompt when checking the ceiling; it is the only
            # honest guess before the call, and erring high is the safe direction.
            if spend.would_exceed(max_usd, spend.price.cost(input_tokens, input_tokens)):
                report.stopped_early = (
                    f"budget ceiling reached: ${spend.usd:.2f} estimated of ${max_usd:.2f} "
                    f"(margin {SAFETY_MARGIN:g}x)"
                )
                break

            produced, error = _attempt(generator, request, generator_name, split)
            output_tokens = sum(
                tokens.count(message.content)
                for example in produced.examples
                for message in example.messages
            )
            cost = spend.price.cost(input_tokens, output_tokens)
            spend.record(input_tokens, output_tokens)
            report.requests += 1

            fresh = [example for example in produced.examples if example.id not in seen]
            report.duplicates += len(produced.examples) - len(fresh)
            for example in fresh:
                sink.write(f"{example.model_dump_json()}\n")
                seen.add(example.id)
            sink.flush()
            report.produced += len(fresh)
            report.rejected.extend(produced.rejected)

            if error:
                report.failures += 1
                report.errors.append(f"{node_id} ({example_type.value}): {error}")
                consecutive += 1
            else:
                consecutive = 0

            book.write(
                Attempt(
                    node=node_id,
                    example_type=example_type.value,
                    asked=owed,
                    kept=len(fresh),
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    usd=cost,
                    error=error,
                ).to_json()
                + "\n"
            )
            book.flush()

    report.spend_usd = spend.usd
    return report


def _attempt(
    generator: TextGenerator,
    request: GenerationRequest,
    generator_name: str,
    split: Split,
) -> tuple[GenerationResult, str]:
    """One request, with its failure turned into a value.

    Every exception is caught on purpose: the run's job is to keep going and record what went
    wrong. A refusal, a timeout, a malformed response and a transport error all cost the same one
    request, and none of them should end a run that has hours of work behind it.
    """
    try:
        return generate_node(generator, request, generator_name=generator_name, split=split), ""
    except Exception as error:  # every failure is a value here — see the docstring
        return GenerationResult(), f"{type(error).__name__}: {error}"


def render(report: RunReport) -> str:
    """Human-readable summary of a run."""
    status = "✓ complete" if report.complete else "… incomplete"
    lines = [
        f"{status} — {report.total}/{report.target} example(s) "
        f"({report.resumed_from} resumed, {report.produced} new) over {report.requests} request(s)",
        f"  spend: ${report.spend_usd:.2f} estimated of ${report.max_usd:.2f} "
        "— ESTIMATED from character counts, not measured from the API's usage",
    ]
    if report.duplicates:
        lines.append(
            f"  {report.duplicates} example(s) already on disk (same content, same UUID5) and "
            "not written twice"
        )
    if report.failures:
        lines.append(f"  {report.failures} failed request(s):")
        lines += [f"    {error}" for error in report.errors[:5]]
    if report.rejected:
        lines.append(f"  {len(report.rejected)} rejected item(s):")
        lines += [f"    {reason}" for reason in report.rejected[:5]]
    if report.stopped_early:
        lines.append(f"  stopped early: {report.stopped_early}")
    if not report.complete and not report.stopped_early:
        lines.append("  run again to continue: the output file is the checkpoint")
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point. Re-running the same command resumes; it never starts over."""
    from maia.synth.generate import AnthropicGenerator, anthropic_client
    from maia.synth.glossary import load_glossary
    from maia.synth.pools import load_partition
    from maia.synth.taxonomy import load_taxonomy

    parser = argparse.ArgumentParser(
        description="Full-scale generation (M2.07). Appends to --out and resumes from it, so "
        "re-running the same command continues rather than starting over."
    )
    parser.add_argument("--corpus", type=Path, nargs="+", required=True)
    parser.add_argument("--taxonomy", type=Path, required=True)
    parser.add_argument("--partition", type=Path, required=True)
    parser.add_argument("--frozen-digest", required=True, help="the B1 partition freeze")
    parser.add_argument("--out", type=Path, required=True, help="JSONL, appended to and resumed")
    parser.add_argument("--glossary", type=Path)
    parser.add_argument("--total", type=int, default=12_000)
    parser.add_argument("--max-usd", type=float, default=DEFAULT_MAX_USD)
    parser.add_argument("--max-requests", type=int)
    parser.add_argument("--seed", type=int, default=20260725)
    parser.add_argument("--model", default="claude-opus-5")
    parser.add_argument(
        "--plan-only",
        action="store_true",
        help="print what the run would ask for and stop, without calling the API",
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

        if args.plan_only:
            print(_render_plan(taxonomy, args.total, args.out))
            return 0

        report = run_generation(
            AnthropicGenerator(anthropic_client(), model=args.model),
            taxonomy,
            documents,
            partition,
            out=args.out,
            frozen_digest=args.frozen_digest,
            total=args.total,
            generator_name=args.model,
            model=args.model,
            glossary=glossary,
            seed=args.seed,
            max_usd=args.max_usd,
            max_requests=args.max_requests,
        )
    except (ValueError, RuntimeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    print(render(report))
    return 0 if report.complete else 1


def _render_plan(taxonomy: Taxonomy, total: int, out: Path) -> str:
    """What a run would ask for, without asking for it."""
    plan = plan_run(taxonomy, total)
    done = coverage(read_partial(out))
    owed = deficit(plan, done)
    lines = [
        f"plan: {sum(plan.values())} example(s) across {len(plan)} (node, type) pair(s)",
        f"  already on disk: {sum(done.values())}",
        f"  still owed: {sum(owed.values())} across {len(owed)} pair(s)",
    ]
    for (node_id, example_type), count in sorted(
        owed.items(), key=lambda item: (-item[1], item[0][0])
    )[:10]:
        lines.append(f"    {node_id} ({example_type.value}): {count}")
    return "\n".join(lines)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
