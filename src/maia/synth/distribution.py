"""The dataset distribution report — PLAN M2.09.

M2.05's validator answers *is this dataset valid?* — a yes/no over §3.2's invariants. This module
answers a different question: **what is actually in it?** The two are not the same, and the gap
between them is where a valid-but-useless dataset lives.

Four things nothing else in the pipeline looks at:

* **Taxonomy nodes with no examples.** The PO approved 64 nodes; if 12 of them produced nothing —
  because their keywords match no corpus passage, or their requests kept failing — the dataset is
  valid, the type shares are green, and a twelfth of the approved subject matter is simply absent.
  :attr:`Profile.empty_nodes` names them.
* **Corpus sources never used as grounding.** M1 spent five milestones building the legal and spoken
  subcorpora. If no example cites a single ``juridic`` document, that work is not in the dataset and
  no §3.2 check would say so.
* **Unjudged examples.** ``judge_score = 0.0`` means both "the judge scored it zero" and "nobody
  judged it" (M2.03 writes the placeholder). The exempt types are *supposed* to sit at zero
  (D-0018); a **grounded** example at zero is one the judge never reached, and counting it as a
  quality signal would be wrong.
* **Andorran lexicon reach.** M2.02 built a glossary and M2.03 requires its use. Whether the
  finished dataset actually contains those words is a measurement, not an assumption.

The report renders as Markdown on purpose: it is the evidence for DoD-F2 and the body of the M2.11
dataset card, so it should be readable where those live rather than only in a terminal.
"""

from __future__ import annotations

import argparse
import statistics
import sys
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from math import ceil
from pathlib import Path

from maia.schemas import CorpusDocument, DatasetExample, ExampleType, Source, Split
from maia.synth.general_ca import andorra_matcher, mentions_andorra
from maia.synth.glossary import Glossary, load_glossary
from maia.synth.judge import is_exempt
from maia.synth.taxonomy import Taxonomy, load_taxonomy
from maia.synth.validate import SPLIT_TARGETS, SPLIT_TOLERANCE

#: §3.2's constrained shares, checked here so the report says whether the dataset is publishable.
TYPE_BANDS: dict[ExampleType, tuple[float, float]] = {
    ExampleType.NO_HO_SE: (0.06, 0.10),
    ExampleType.GENERAL_CA: (0.15, 0.20),
}

#: DoD-F2's size range for Phase 2.
TARGET_SIZE = (10_000, 15_000)

#: Percentiles reported for length distributions.
PERCENTILES = (50, 95)


def text_of(example: DatasetExample) -> str:
    """Every message of one example, for length statistics."""
    return "\n".join(message.content for message in example.messages)


@dataclass
class Lengths:
    """Length statistics for one population, in characters."""

    count: int = 0
    total: int = 0
    mean: float = 0.0
    p50: int = 0
    p95: int = 0
    longest: int = 0
    shortest: int = 0

    @classmethod
    def of(cls, values: Sequence[int]) -> Lengths:
        """Summarise ``values``. An empty population is all zeros, not an error."""
        if not values:
            return cls()
        ordered = sorted(values)
        return cls(
            count=len(ordered),
            total=sum(ordered),
            mean=statistics.fmean(ordered),
            p50=_percentile(ordered, 50),
            p95=_percentile(ordered, 95),
            longest=ordered[-1],
            shortest=ordered[0],
        )


def _percentile(ordered: Sequence[int], percentile: int) -> int:
    """Nearest-rank percentile of an already-sorted sequence.

    ``ceil``, not ``round``: Python rounds halves to even, so ``round(2.5) == 2`` would make the
    median of five values the second one instead of the third.

    ``ordered`` is never empty — :meth:`Lengths.of` returns before calling this.
    """
    index = min(len(ordered) - 1, max(0, ceil(percentile / 100 * len(ordered)) - 1))
    return ordered[index]


@dataclass
class Profile:
    """What is actually in a dataset."""

    total: int = 0
    by_type: Counter[str] = field(default_factory=Counter)
    by_split: Counter[str] = field(default_factory=Counter)
    by_node: Counter[str] = field(default_factory=Counter)
    by_source: Counter[str] = field(default_factory=Counter)
    by_generator: Counter[str] = field(default_factory=Counter)
    turns: Counter[int] = field(default_factory=Counter)
    lengths: Lengths = field(default_factory=Lengths)
    lengths_by_type: dict[str, Lengths] = field(default_factory=dict)
    judged: int = 0
    unjudged_grounded: list[str] = field(default_factory=list)
    exempt: int = 0
    score_buckets: Counter[str] = field(default_factory=Counter)
    mean_score: float = 0.0
    grounding_citations: int = 0
    distinct_passages: int = 0
    unknown_passages: int = 0
    empty_nodes: list[str] = field(default_factory=list)
    unused_sources: list[str] = field(default_factory=list)
    glossary_hits: int = 0
    glossary_terms_seen: int = 0
    glossary_terms_total: int = 0

    def share_of_type(self, kind: ExampleType) -> float:
        """Share of the dataset held by ``kind``."""
        return self.by_type.get(kind.value, 0) / self.total if self.total else 0.0

    def share_of_split(self, split: Split) -> float:
        """Share of the dataset held by ``split``."""
        return self.by_split.get(split.value, 0) / self.total if self.total else 0.0

    @property
    def type_violations(self) -> list[str]:
        """§3.2 shares the dataset breaks."""
        return [
            f"{kind.value} is {self.share_of_type(kind):.1%}, outside {low:.0%}-{high:.0%}"
            for kind, (low, high) in TYPE_BANDS.items()
            if not low <= self.share_of_type(kind) <= high
        ]

    @property
    def split_violations(self) -> list[str]:
        """Split proportions outside the validator's tolerance."""
        return [
            f"{split.value} is {self.share_of_split(split):.1%}, target {target:.0%} "
            f"(±{SPLIT_TOLERANCE:.0%})"
            for split, target in SPLIT_TARGETS.items()
            if abs(self.share_of_split(split) - target) > SPLIT_TOLERANCE
        ]

    @property
    def size_ok(self) -> bool:
        """Whether the dataset is inside DoD-F2's size range."""
        return TARGET_SIZE[0] <= self.total <= TARGET_SIZE[1]

    @property
    def findings(self) -> list[str]:
        """Everything worth blocking publication over."""
        found = [*self.type_violations, *self.split_violations]
        if not self.size_ok:
            found.append(
                f"{self.total} examples is outside DoD-F2's {TARGET_SIZE[0]:,}-{TARGET_SIZE[1]:,}"
            )
        if self.empty_nodes:
            found.append(
                f"{len(self.empty_nodes)} approved taxonomy node(s) produced no examples: "
                + ", ".join(self.empty_nodes[:5])
            )
        if self.unused_sources:
            found.append(
                "corpus source(s) never cited as grounding: " + ", ".join(self.unused_sources)
            )
        if self.unjudged_grounded:
            found.append(
                f"{len(self.unjudged_grounded)} grounded example(s) have judge_score 0.0 and were "
                "never judged (M2.05 did not reach them)"
            )
        if self.unknown_passages:
            found.append(
                f"{self.unknown_passages} grounding id(s) are not in the corpus supplied — those "
                "examples cannot be traced to a source"
            )
        return found

    @property
    def publishable(self) -> bool:
        """Whether nothing found here should stop an upload."""
        return not self.findings


def profile(
    examples: Sequence[DatasetExample],
    *,
    taxonomy: Taxonomy | None = None,
    corpus: Mapping[str, CorpusDocument] | None = None,
    glossary: Glossary | None = None,
) -> Profile:
    """Measure a dataset.

    Every input beyond ``examples`` is optional, and each one unlocks a class of finding: the
    taxonomy reveals nodes that produced nothing, the corpus reveals unused sources and untraceable
    grounding, the glossary measures Andorran lexicon reach. What is not supplied is simply not
    reported — never assumed clean.
    """
    result = Profile(total=len(examples))
    scores: list[float] = []
    by_type_lengths: dict[str, list[int]] = {}
    passages: set[str] = set()

    for example in examples:
        result.by_type[example.type.value] += 1
        result.by_split[example.split.value] += 1
        result.by_node[example.topic] += 1
        result.by_generator[example.generator] += 1
        result.turns[len(example.messages)] += 1
        length = len(text_of(example))
        by_type_lengths.setdefault(example.type.value, []).append(length)

        result.grounding_citations += len(example.grounding_ids)
        passages.update(example.grounding_ids)

        if is_exempt(example):
            result.exempt += 1
        elif example.judge_score > 0.0:
            result.judged += 1
            scores.append(example.judge_score)
            result.score_buckets[_bucket(example.judge_score)] += 1
        else:
            # Grounded and still at the placeholder: nobody judged it.
            result.unjudged_grounded.append(str(example.id))

    result.lengths = Lengths.of([len(text_of(example)) for example in examples])
    result.lengths_by_type = {
        kind: Lengths.of(values) for kind, values in sorted(by_type_lengths.items())
    }
    result.mean_score = statistics.fmean(scores) if scores else 0.0
    result.distinct_passages = len(passages)

    if taxonomy is not None:
        result.empty_nodes = sorted(
            node.id for node in taxonomy.nodes if not result.by_node.get(node.id)
        )
    if corpus is not None:
        result.unknown_passages = sum(1 for ident in passages if ident not in corpus)
        for ident in passages:
            document = corpus.get(ident)
            if document is not None:
                result.by_source[document.source.value] += 1
        present = {document.source.value for document in corpus.values()}
        result.unused_sources = sorted(present - set(result.by_source))
    if glossary is not None:
        result.glossary_terms_total = len(glossary.entries)
        result.glossary_hits, result.glossary_terms_seen = _lexicon_reach(examples, glossary)
    return result


def _bucket(score: float) -> str:
    """Which decile-ish band a judge score falls in."""
    if score >= 0.9:
        return "0.9-1.0"
    if score >= 0.8:
        return "0.8-0.9"
    if score >= 0.7:
        return "0.7-0.8"
    if score >= 0.5:
        return "0.5-0.7"
    return "<0.5"


def _lexicon_reach(examples: Iterable[DatasetExample], glossary: Glossary) -> tuple[int, int]:
    """``(examples containing Andorran lexicon, distinct glossary entries seen)``.

    Reuses M2.04's matcher, which is the same source of truth in the opposite direction: there it
    rejects Andorran content from the anti-forgetting mix, here it confirms the Andorran half
    actually contains what M2.03 asked for.
    """
    per_entry = [
        (entry, andorra_matcher(Glossary(version=glossary.version, entries=[entry])))
        for entry in glossary.entries
    ]
    whole = andorra_matcher(glossary)
    hits = 0
    seen: set[str] = set()
    for example in examples:
        text = text_of(example)
        if mentions_andorra(text, whole):
            hits += 1
            for entry, matcher in per_entry:
                if entry.term not in seen and mentions_andorra(text, matcher):
                    seen.add(entry.term)
    return hits, len(seen)


def render(profile_: Profile, *, name: str = "dataset") -> str:
    """The report, as Markdown — it is the DoD-F2 evidence and the M2.11 dataset card body."""
    status = "✓ publishable" if profile_.publishable else "✗ not publishable"
    lines = [
        f"# Dataset distribution — {name}",
        "",
        f"**{profile_.total:,} examples** · {status}",
        "",
    ]

    lines += [
        "## Types",
        "",
        "| type | count | share | §3.2 | mean chars |",
        "| --- | --: | --: | :-: | --: |",
    ]
    for kind, count in sorted(profile_.by_type.items()):
        # The schema validated these, so the enum lookup cannot fail.
        band = TYPE_BANDS.get(ExampleType(kind))
        share = count / profile_.total if profile_.total else 0.0
        mark = "—" if band is None else ("✓" if band[0] <= share <= band[1] else "✗")
        mean = profile_.lengths_by_type.get(kind, Lengths()).mean
        lines.append(f"| `{kind}` | {count:,} | {share:.1%} | {mark} | {mean:,.0f} |")
    lines.append("")

    lines += ["## Splits", "", "| split | count | share | target |", "| --- | --: | --: | --: |"]
    for split, target in SPLIT_TARGETS.items():
        count = profile_.by_split.get(split.value, 0)
        lines.append(
            f"| `{split.value}` | {count:,} | {profile_.share_of_split(split):.1%} | {target:.0%} |"
        )
    lines.append("")

    lines += [
        "## Grounding",
        "",
        f"- {profile_.grounding_citations:,} citation(s) over "
        f"{profile_.distinct_passages:,} distinct corpus passage(s)",
    ]
    if profile_.by_source:
        lines.append("- passages by source:")
        lines += [
            f"  - `{source}`: {count:,}"
            for source, count in sorted(profile_.by_source.items(), key=lambda item: -item[1])
        ]
    if profile_.unused_sources:
        lines.append(
            "- ⚠ **never cited**: "
            + ", ".join(f"`{source}`" for source in profile_.unused_sources)
            + " — that subcorpus is not in the dataset"
        )
    lines.append("")

    lines += [
        "## Judging",
        "",
        f"- {profile_.judged:,} judged, mean score {profile_.mean_score:.2f}",
        f"- {profile_.exempt:,} exempt by type (`general_ca`, `estil_andorra` cite no passages)",
    ]
    if profile_.unjudged_grounded:
        lines.append(
            f"- ⚠ **{len(profile_.unjudged_grounded):,} grounded example(s) never judged** "
            "(`judge_score` is still the 0.0 placeholder, not a verdict)"
        )
    if profile_.score_buckets:
        lines.append("- score distribution:")
        lines += [
            f"  - {bucket}: {count:,}"
            for bucket, count in sorted(profile_.score_buckets.items(), reverse=True)
        ]
    lines.append("")

    lines += [
        "## Coverage",
        "",
        f"- {len(profile_.by_node):,} taxonomy node(s) represented",
    ]
    if profile_.empty_nodes:
        lines.append(
            f"- ⚠ **{len(profile_.empty_nodes)} approved node(s) produced nothing**: "
            + ", ".join(f"`{node}`" for node in profile_.empty_nodes)
        )
    if profile_.glossary_terms_total:
        lines.append(
            f"- Andorran lexicon: {profile_.glossary_hits:,} example(s) "
            f"({profile_.glossary_hits / profile_.total:.1%}) use at least one glossary term; "
            f"{profile_.glossary_terms_seen}/{profile_.glossary_terms_total} terms appear"
        )
    lines.append("")

    lines += [
        "## Shape",
        "",
        f"- length: mean {profile_.lengths.mean:,.0f} chars, "
        f"p50 {profile_.lengths.p50:,}, p95 {profile_.lengths.p95:,}, "
        f"max {profile_.lengths.longest:,}, min {profile_.lengths.shortest:,}",
        f"- {profile_.lengths.total:,} characters in total",
        "- turns per example: "
        + ", ".join(f"{turns}→{count:,}" for turns, count in sorted(profile_.turns.items())),
        "- generators: "
        + ", ".join(
            f"`{name_}` {count:,}" for name_, count in sorted(profile_.by_generator.items())
        ),
        "",
    ]

    if profile_.findings:
        lines += ["## Findings", ""]
        lines += [f"- ✗ {finding}" for finding in profile_.findings]
        lines.append("")
    return "\n".join(lines)


def read_dataset(path: Path) -> list[DatasetExample]:
    """Read a §3.2 dataset from JSONL."""
    return [
        DatasetExample.model_validate_json(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def read_corpus(paths: Sequence[Path]) -> dict[str, CorpusDocument]:
    """Index §3.1 corpus documents by id."""
    return {
        document.id: document
        for path in paths
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
        for document in [CorpusDocument.model_validate_json(line)]
    }


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point. Exit non-zero when a finding should stop publication."""
    parser = argparse.ArgumentParser(
        description="Profile a §3.2 dataset (M2.09): type and split shares, grounding coverage by "
        "corpus source, taxonomy nodes that produced nothing, unjudged examples, Andorran lexicon "
        "reach. Renders Markdown for the DoD-F2 evidence and the M2.11 dataset card."
    )
    parser.add_argument("dataset", type=Path, help="the §3.2 dataset (JSONL)")
    parser.add_argument("--taxonomy", type=Path, help="configs/taxonomy.yaml, to find empty nodes")
    parser.add_argument("--corpus", type=Path, nargs="+", help="§3.1 corpus JSONL, for sources")
    parser.add_argument("--glossary", type=Path, help="configs/glossari-andorra.yaml")
    parser.add_argument("--out", type=Path, help="write the Markdown report here")
    args = parser.parse_args(argv)

    paths = [
        args.dataset,
        *(args.corpus or []),
        *([args.taxonomy] if args.taxonomy else []),
        *([args.glossary] if args.glossary else []),
    ]
    for path in paths:
        if not path.is_file():
            print(f"error: no such file: {path}", file=sys.stderr)
            return 1

    try:
        measured = profile(
            read_dataset(args.dataset),
            taxonomy=load_taxonomy(args.taxonomy) if args.taxonomy else None,
            corpus=read_corpus(args.corpus) if args.corpus else None,
            glossary=load_glossary(args.glossary) if args.glossary else None,
        )
    except (ValueError, RuntimeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    report = render(measured, name=args.dataset.name)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(report, encoding="utf-8")
    print(report)
    return 0 if measured.publishable else 1


def sources_of(corpus: Iterable[CorpusDocument]) -> set[Source]:
    """Which §3.1 sources a corpus contains — the denominator for unused-source reporting."""
    return {document.source for document in corpus}


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
