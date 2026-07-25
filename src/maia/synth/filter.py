"""The M2.05 filter pipeline — semantic dedup, factual-support judge, Catalan check.

*"each filter logs how much it drops"* is the spec's own requirement, and the reason this module
exists rather than three CLIs run by hand: the number that matters is not any single filter's
count but **what came out the other end**, because filtering changes the §3.2 distribution. Drop
6 % of examples and the ``no_ho_se`` share moves; drop them unevenly and it moves out of its ±2 pp
band. So the pipeline reports the type shares before and after, and the CLI fails when the
surviving dataset no longer satisfies §3.2 — filtering a dataset into non-compliance is a failure,
not a success with a caveat.

**Order is deliberate.** Dedup is free and shrinks everything downstream, so it runs first — no
point paying a judge call for an example a duplicate check would have removed. The judge runs
second because it is the expensive one and the only one that *writes* (it fills in
``judge_score``). The Catalan check runs last, on the survivors only.

Every stage is optional, and an omitted stage is reported as ``NOT RUN`` rather than passing
silently — the same rule as :mod:`maia.synth.validate`. All three depend on a
blocked-by-resource service, so a run with none of them wired is the normal state of this repo,
and it must not be mistakable for a clean filter run.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from maia.schemas import CorpusDocument, DatasetExample, ExampleType
from maia.synth import grammar, judge, semdedup
from maia.synth.glossary import Glossary, load_glossary

#: The §3.2 constraints filtering can break. Checked on the *surviving* dataset.
TYPE_BANDS: dict[ExampleType, tuple[float, float]] = {
    ExampleType.NO_HO_SE: (0.06, 0.10),
    ExampleType.GENERAL_CA: (0.15, 0.20),
}


@dataclass
class FilterReport:
    """What the whole pipeline did, stage by stage."""

    started: int = 0
    dedup: semdedup.SemanticDedupReport | None = None
    judged: judge.JudgeReport | None = None
    grammar: grammar.GrammarReport | None = None
    shares_before: dict[ExampleType, float] = field(default_factory=dict)
    shares_after: dict[ExampleType, float] = field(default_factory=dict)
    finished: int = 0

    @property
    def skipped(self) -> list[str]:
        """Stages that did not run — reported, never assumed clean."""
        return [
            name
            for name, report in (
                ("semantic dedup", self.dedup),
                ("factual-support judge", self.judged),
                ("Catalan check", self.grammar),
            )
            if report is None
        ]

    @property
    def dropped(self) -> int:
        """Total examples removed."""
        return self.started - self.finished

    @property
    def violations(self) -> list[str]:
        """§3.2 distribution constraints the *surviving* dataset breaks."""
        broken = []
        for kind, (low, high) in TYPE_BANDS.items():
            share = self.shares_after.get(kind, 0.0)
            if not low <= share <= high:
                was = self.shares_before.get(kind, 0.0)
                broken.append(
                    f"{kind.value} is {share:.1%}, outside §3.2's {low:.0%}-{high:.0%} "
                    f"(was {was:.1%} before filtering)"
                )
        return broken

    @property
    def compliant(self) -> bool:
        """Whether the surviving dataset still satisfies the §3.2 bands."""
        return not self.violations


def run_filters(
    examples: Sequence[DatasetExample],
    *,
    embedder: semdedup.Embedder | None = None,
    factual_judge: judge.FactualSupportJudge | None = None,
    corpus: Mapping[str, CorpusDocument] | None = None,
    catalan: grammar.CatalanCheck | None = None,
    threshold: float = semdedup.DEFAULT_THRESHOLD,
) -> tuple[list[DatasetExample], FilterReport]:
    """Run whichever filters are wired, in order, and report each one's drops.

    Raises:
        ValueError: if a judge is supplied without a corpus. The judge compares answers to their
            grounding passages; without the corpus it has nothing to compare against, and running
            it anyway would fail every example for a missing passage.
    """
    if factual_judge is not None and corpus is None:
        raise ValueError(
            "the factual-support judge needs the corpus its examples cite — pass corpus="
        )
    report = FilterReport(started=len(examples))
    report.shares_before = semdedup.share_by_type(examples)
    survivors = list(examples)

    if embedder is not None:
        survivors, report.dedup = semdedup.deduplicate(survivors, embedder, threshold=threshold)
    if factual_judge is not None:
        assert corpus is not None  # guarded above
        survivors, report.judged = factual_judge.run(survivors, corpus)
    if catalan is not None:
        survivors, report.grammar = catalan.run(survivors)

    report.finished = len(survivors)
    report.shares_after = semdedup.share_by_type(survivors)
    return survivors, report


def render(report: FilterReport) -> str:
    """Human-readable summary of the whole pipeline."""
    lines = [f"filters: {report.finished}/{report.started} kept ({report.dropped} dropped)"]
    if report.dedup is not None:
        lines.append(semdedup.render(report.dedup))
    if report.judged is not None:
        lines.append(judge.render(report.judged))
    if report.grammar is not None:
        lines.append(grammar.render(report.grammar))
    for name in report.skipped:
        lines.append(f"{name}: NOT RUN — blocked-by-resource, nothing was checked")
    if report.shares_after:
        lines.append("§3.2 distribution after filtering:")
        for kind, (low, high) in TYPE_BANDS.items():
            share = report.shares_after.get(kind, 0.0)
            mark = "✓" if low <= share <= high else "✗"
            lines.append(
                f"  {mark} {kind.value}: {report.shares_before.get(kind, 0.0):.1%} before "
                f"filtering → {share:.1%} (§3.2 wants {low:.0%}-{high:.0%})"
            )
    return "\n".join(lines)


def read_dataset(path: Path) -> list[DatasetExample]:
    """Read a §3.2 dataset from JSONL."""
    return [
        DatasetExample.model_validate_json(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point.

    Every filter is off unless its resource is supplied, and the summary says so. Exit is non-zero
    when the surviving dataset breaks a §3.2 band — filtering a dataset into non-compliance is a
    failure, not a success with a caveat.
    """
    parser = argparse.ArgumentParser(
        description="Filter a generated dataset (M2.05): semantic dedup, factual-support judge, "
        "LanguageTool ca. Each filter needs a blocked-by-resource service; those not supplied "
        "are reported as NOT RUN."
    )
    parser.add_argument("dataset", type=Path, help="the generated §3.2 dataset (JSONL)")
    parser.add_argument("--out", type=Path, help="write the surviving dataset here")
    parser.add_argument(
        "--corpus", type=Path, nargs="+", help="§3.1 corpus JSONL, for the judge's grounding"
    )
    parser.add_argument("--glossary", type=Path, help="configs/glossari-andorra.yaml")
    parser.add_argument("--languagetool", help="LanguageTool /v2/check URL, to run the ca check")
    parser.add_argument(
        "--embeddings-url", help="Ollama-compatible /api/embed URL, to run the semantic dedup"
    )
    parser.add_argument("--embeddings-model", default="jina/jina-embeddings-v2-base-es")
    parser.add_argument(
        "--judge",
        action="store_true",
        help="run the factual-support judge (needs ANTHROPIC_API_KEY and --corpus)",
    )
    parser.add_argument("--model", default="claude-opus-5")
    parser.add_argument("--judge-threshold", type=float, default=judge.DEFAULT_THRESHOLD)
    parser.add_argument("--dedup-threshold", type=float, default=semdedup.DEFAULT_THRESHOLD)
    parser.add_argument("--max-density", type=float, default=grammar.DEFAULT_MAX_DENSITY)
    args = parser.parse_args(argv)

    for path in [args.dataset, *(args.corpus or []), *([args.glossary] if args.glossary else [])]:
        if not path.is_file():
            print(f"error: no such file: {path}", file=sys.stderr)
            return 1

    examples = read_dataset(args.dataset)
    corpus = _load_corpus(args.corpus) if args.corpus else None
    glossary: Glossary | None = load_glossary(args.glossary) if args.glossary else None

    embedder = (
        semdedup.ollama_embedder(args.embeddings_url, model=args.embeddings_model)
        if args.embeddings_url
        else None
    )

    factual_judge = None
    if args.judge:
        if corpus is None:
            print("error: --judge needs --corpus", file=sys.stderr)
            return 1
        from maia.synth.generate import AnthropicGenerator, anthropic_client

        factual_judge = judge.FactualSupportJudge(
            AnthropicGenerator(anthropic_client(), model=args.model),
            threshold=args.judge_threshold,
        )

    catalan = None
    if args.languagetool:
        catalan = grammar.CatalanCheck(
            grammar.languagetool_service(args.languagetool),
            glossary=glossary,
            max_density=args.max_density,
        )

    try:
        survivors, report = run_filters(
            examples,
            embedder=embedder,
            factual_judge=factual_judge,
            corpus=corpus,
            catalan=catalan,
            threshold=args.dedup_threshold,
        )
    except (ValueError, KeyError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(
            "".join(f"{example.model_dump_json()}\n" for example in survivors), encoding="utf-8"
        )
    print(render(report))
    return 0 if report.compliant else 1


def _load_corpus(paths: Sequence[Path]) -> dict[str, CorpusDocument]:
    """Index every §3.1 corpus document by id, for the judge's grounding lookup.

    Restricted text is deliberately included: the judge is an internal check, and its prompt is
    never written to a public artifact — the same rule the generator follows (D-0011).
    """
    return judge.index_corpus(
        CorpusDocument.model_validate_json(line)
        for path in paths
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    )
