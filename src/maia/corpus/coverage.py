"""Corpus coverage report — PLAN M1.10.

The F1 exit artifact: *"coverage report by source (docs, tokens, licenses)"*, which the PO
reads to decide whether Phase 1 is done. It answers, from the corpus itself:

* **Is there enough text?** Against the 5-15 M token target.
* **Where does it come from?** Documents, characters, words and estimated tokens per source,
  with each source's share of the whole — a corpus that is 90 % Viquipèdia is not the
  Andorran corpus this project needs, and only a per-source breakdown shows that.
* **How much of it can be published?** Tokens split by licence, with ``no-redistribute``
  called out separately. This is the number that bounds what the public dataset can draw on,
  as opposed to what the private RAG index may use.
* **Is the spoken subcorpus real?** ``andorra_parlat`` documents and distinct speakers, which
  is the F1 criterion for the Diari de Sessions subcorpus.
* **Is the legal subcorpus complete?** Articles per law, ranks covered, and the consolidation
  date each law was captured at — F1 asks for *all P0 laws in text refós*, and a law present
  with three articles is a scraping failure that a document count alone would hide.

**Token counts are estimates.** A true count needs the Gemma tokenizer, which needs a gated
download (blocked-by-resource), so the default counter divides characters by
:data:`CHARS_PER_TOKEN` and every field is named ``estimated_tokens`` to keep that honest.
:data:`TokenCounter` is the seam: pass the real tokenizer's ``len(encode(text))`` and the
report becomes exact without anything else changing. Words are reported alongside so the
estimate can be sanity-checked by eye.

The report also runs two integrity checks on the artifact rather than trusting its producer:
duplicate ids (consolidation should have removed them) and documents whose id does not match
their text.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import Counter
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

from maia.corpus.consolidate import ConsolidationReport, read_documents
from maia.schemas import CorpusDocument, License, Registre, compute_id

#: Characters per token for Catalan under a multilingual SentencePiece tokenizer. A working
#: figure, not a measurement — see the module docstring and the wiki gaps entry.
CHARS_PER_TOKEN = 3.7

#: The corpus volume target (PRD §4, Fase 1): ample, because the corpus grounds RAG and the
#: synthetic dataset rather than being pre-training data.
TARGET_MIN_TOKENS = 5_000_000
TARGET_MAX_TOKENS = 15_000_000

#: Counts the tokens in a piece of text. Swap in a real tokenizer to make the report exact.
TokenCounter = Callable[[str], int]


def estimate_tokens(text: str) -> int:
    """Estimate the token count of ``text`` from its length."""
    return round(len(text) / CHARS_PER_TOKEN)


def count_words(text: str) -> int:
    """Whitespace-delimited word count — reported so the token estimate can be checked."""
    return len(text.split())


class Tokenizer(Protocol):
    """Anything that encodes text to tokens — ``transformers`` tokenizers satisfy this."""

    def encode(self, text: str, add_special_tokens: bool = ...) -> Sequence[int]:
        """Encode ``text`` into token ids."""


def tokenizer_counter(tokenizer: Tokenizer) -> TokenCounter:
    """Turn a real tokenizer into a :data:`TokenCounter`, making the report exact.

    The tokenizer is passed in rather than constructed here, so this module never imports
    ``transformers`` and needs no gated download to be tested. Getting the real Gemma
    tokenizer is the blocked-by-resource part (it needs ``HF_TOKEN`` and access to the gated
    repo), and it belongs to the caller::

        from transformers import AutoTokenizer

        counter = tokenizer_counter(AutoTokenizer.from_pretrained(GEMMA_MODEL_ID))
        report = build_report(documents, count_tokens=counter)
    """

    def count(text: str) -> int:
        return len(tokenizer.encode(text, add_special_tokens=False))

    return count


@dataclass(frozen=True)
class Volume:
    """A quantity of text, counted four ways."""

    documents: int = 0
    characters: int = 0
    words: int = 0
    estimated_tokens: int = 0

    def plus(self, doc: CorpusDocument, tokens: int) -> Volume:
        """This volume with ``doc`` added."""
        return Volume(
            documents=self.documents + 1,
            characters=self.characters + len(doc.text),
            words=self.words + count_words(doc.text),
            estimated_tokens=self.estimated_tokens + tokens,
        )

    def as_dict(self) -> dict[str, int]:
        return {
            "documents": self.documents,
            "characters": self.characters,
            "words": self.words,
            "estimated_tokens": self.estimated_tokens,
        }


@dataclass(frozen=True)
class LawCoverage:
    """One law's presence in the corpus."""

    citation: str
    rang: str
    articles: int
    consolidacio_data: str


@dataclass
class CoverageReport:
    """Everything the F1 gate asks about the corpus."""

    total: Volume = field(default_factory=Volume)
    by_source: dict[str, Volume] = field(default_factory=dict)
    by_license: dict[str, Volume] = field(default_factory=dict)
    by_registre: dict[str, Volume] = field(default_factory=dict)
    #: Interventions per speaker (Diari de Sessions only).
    speakers: Counter[str] = field(default_factory=Counter)
    #: Articles captured per law, keyed by the law's citation.
    laws: list[LawCoverage] = field(default_factory=list)
    #: Document lengths in characters, for the distribution summary.
    lengths: list[int] = field(default_factory=list)
    #: Integrity findings on the artifact itself.
    duplicate_ids: list[str] = field(default_factory=list)
    mismatched_ids: list[str] = field(default_factory=list)

    @property
    def publishable(self) -> Volume:
        """Volume that may enter public artifacts."""
        return _merge(
            volume for name, volume in self.by_license.items() if License(name).is_public()
        )

    @property
    def grounding_only(self) -> Volume:
        """Volume that is ``no-redistribute`` — RAG and grounding, never published."""
        return self.by_license.get(License.NO_REDISTRIBUTE.value, Volume())

    @property
    def target_status(self) -> str:
        """``below`` / ``within`` / ``above`` the 5-15 M token target."""
        tokens = self.total.estimated_tokens
        if tokens < TARGET_MIN_TOKENS:
            return "below"
        return "within" if tokens <= TARGET_MAX_TOKENS else "above"

    @property
    def integrity_ok(self) -> bool:
        """True when the artifact holds no duplicate and no mismatched ids."""
        return not self.duplicate_ids and not self.mismatched_ids

    @property
    def length_summary(self) -> dict[str, int]:
        """Min / median / p90 / max document length in characters."""
        if not self.lengths:
            return {"min": 0, "median": 0, "p90": 0, "max": 0}
        ordered = sorted(self.lengths)
        index = min(len(ordered) - 1, round(0.9 * (len(ordered) - 1)))
        return {
            "min": ordered[0],
            "median": round(statistics.median(ordered)),
            "p90": ordered[index],
            "max": ordered[-1],
        }

    def share(self, source: str) -> float:
        """``source``'s share of the corpus by estimated tokens, 0.0-1.0."""
        if not self.total.estimated_tokens:
            return 0.0
        return self.by_source[source].estimated_tokens / self.total.estimated_tokens


def _merge(volumes: Iterable[Volume]) -> Volume:
    total = Volume()
    for volume in volumes:
        total = Volume(
            documents=total.documents + volume.documents,
            characters=total.characters + volume.characters,
            words=total.words + volume.words,
            estimated_tokens=total.estimated_tokens + volume.estimated_tokens,
        )
    return total


def build_report(
    documents: Iterable[CorpusDocument],
    *,
    count_tokens: TokenCounter = estimate_tokens,
) -> CoverageReport:
    """Compute the coverage report over ``documents``."""
    report = CoverageReport()
    seen: set[str] = set()
    # llei citation (or rang, for the Constitution) → articles seen and the consolidation date
    legal: dict[str, tuple[str, set[str], str]] = {}

    for doc in documents:
        tokens = count_tokens(doc.text)
        report.total = report.total.plus(doc, tokens)
        report.lengths.append(len(doc.text))

        for bucket, key in (
            (report.by_source, doc.source.value),
            (report.by_license, doc.license.value),
            (report.by_registre, doc.registre.value),
        ):
            bucket[key] = bucket.get(key, Volume()).plus(doc, tokens)

        if doc.speaker is not None:
            report.speakers[doc.speaker] += 1

        if doc.id in seen:
            report.duplicate_ids.append(doc.id)
        seen.add(doc.id)
        if doc.id != compute_id(doc.text):
            report.mismatched_ids.append(doc.id)

        if doc.legal is not None:
            # The Constitution has no `llei` number, so it is keyed by its rank instead.
            key = doc.legal.llei or doc.legal.rang.value
            rang, articles, _ = legal.get(key, (doc.legal.rang.value, set(), ""))
            articles.add(doc.legal.article)
            legal[key] = (rang, articles, doc.legal.consolidacio_data.isoformat())

    report.laws = [
        LawCoverage(citation=key, rang=rang, articles=len(articles), consolidacio_data=stamp)
        for key, (rang, articles, stamp) in sorted(legal.items())
    ]
    return report


def to_json(report: CoverageReport) -> str:
    """The report as JSON, for CI and for the dataset card (M6.03)."""
    return json.dumps(
        {
            "total": report.total.as_dict(),
            "target": {
                "min_tokens": TARGET_MIN_TOKENS,
                "max_tokens": TARGET_MAX_TOKENS,
                "status": report.target_status,
            },
            "by_source": {
                name: {**volume.as_dict(), "share": round(report.share(name), 4)}
                for name, volume in sorted(report.by_source.items())
            },
            "by_license": {
                name: volume.as_dict() for name, volume in sorted(report.by_license.items())
            },
            "by_registre": {
                name: volume.as_dict() for name, volume in sorted(report.by_registre.items())
            },
            "publishable": report.publishable.as_dict(),
            "grounding_only": report.grounding_only.as_dict(),
            "speakers": dict(sorted(report.speakers.items())),
            "laws": [
                {
                    "citation": law.citation,
                    "rang": law.rang,
                    "articles": law.articles,
                    "consolidacio_data": law.consolidacio_data,
                }
                for law in report.laws
            ],
            "document_length_chars": report.length_summary,
            "integrity": {
                "ok": report.integrity_ok,
                "duplicate_ids": report.duplicate_ids,
                "mismatched_ids": report.mismatched_ids,
            },
        },
        ensure_ascii=False,
        indent=2,
    )


def _thousands(value: int) -> str:
    return f"{value:,}".replace(",", " ")


def to_markdown(report: CoverageReport) -> str:
    """The report as markdown — what the PO reads to validate F1."""
    total = report.total
    status = {"below": "⚠ below target", "within": "✓ within target", "above": "above target"}[
        report.target_status
    ]
    lines = [
        "# Corpus coverage report (M1.10)",
        "",
        f"**{_thousands(total.documents)} documents** · "
        f"{_thousands(total.characters)} characters · "
        f"{_thousands(total.words)} words · "
        f"**≈{_thousands(total.estimated_tokens)} tokens** — {status} "
        f"({_thousands(TARGET_MIN_TOKENS)}\u2013{_thousands(TARGET_MAX_TOKENS)}).",
        "",
        "> Token counts are **estimates** "
        f"({CHARS_PER_TOKEN} chars/token); a true count needs the Gemma tokenizer.",
        "",
        "## By source",
        "",
        "| source | docs | words | ≈tokens | share |",
        "| --- | --: | --: | --: | --: |",
    ]
    for name, volume in sorted(
        report.by_source.items(), key=lambda item: -item[1].estimated_tokens
    ):
        lines.append(
            f"| `{name}` | {_thousands(volume.documents)} | {_thousands(volume.words)} "
            f"| {_thousands(volume.estimated_tokens)} | {report.share(name):.1%} |"
        )

    lines += [
        "",
        "## By licence",
        "",
        "| licence | docs | ≈tokens | publishable |",
        "| --- | --: | --: | :-: |",
    ]
    for name, volume in sorted(report.by_license.items()):
        mark = "yes" if License(name).is_public() else "**no**"
        lines.append(
            f"| `{name}` | {_thousands(volume.documents)} "
            f"| {_thousands(volume.estimated_tokens)} | {mark} |"
        )
    lines += [
        "",
        f"**Publishable:** {_thousands(report.publishable.documents)} docs, "
        f"≈{_thousands(report.publishable.estimated_tokens)} tokens. "
        f"**Grounding-only:** {_thousands(report.grounding_only.documents)} docs, "
        f"≈{_thousands(report.grounding_only.estimated_tokens)} tokens "
        "(never in a public artifact).",
        "",
        "## By register",
        "",
        "| register | docs | ≈tokens |",
        "| --- | --: | --: |",
    ]
    for name, volume in sorted(report.by_registre.items()):
        lines.append(
            f"| `{name}` | {_thousands(volume.documents)} | {_thousands(volume.estimated_tokens)} |"
        )

    spoken = report.by_registre.get(Registre.ANDORRA_PARLAT.value, Volume())
    lines += [
        "",
        "## Spoken subcorpus (Diari de Sessions)",
        "",
        f"{_thousands(spoken.documents)} interventions from "
        f"**{len(report.speakers)} distinct speakers** "
        f"(whitelist applied upstream, M1.04/M1.05).",
    ]
    if report.speakers:
        lines += ["", "| speaker | interventions |", "| --- | --: |"]
        lines += [
            f"| {speaker} | {count} |"
            for speaker, count in sorted(report.speakers.items(), key=lambda kv: (-kv[1], kv[0]))
        ]

    lines += ["", "## Juridical subcorpus", ""]
    if report.laws:
        lines += [
            "| norm | rank | articles | consolidated |",
            "| --- | --- | --: | --- |",
        ]
        lines += [
            f"| {law.citation} | `{law.rang}` | {law.articles} | {law.consolidacio_data} |"
            for law in report.laws
        ]
        lines += [
            "",
            "> F1 requires **all P0 laws in text refós**. A law present with only a handful of "
            "articles is a capture failure, not coverage.",
        ]
    else:
        lines.append("_No legal documents in this corpus._")

    summary = report.length_summary
    lines += [
        "",
        "## Document length (characters)",
        "",
        f"min {_thousands(summary['min'])} · median {_thousands(summary['median'])} · "
        f"p90 {_thousands(summary['p90'])} · max {_thousands(summary['max'])}",
        "",
        "## Integrity",
        "",
    ]
    if report.integrity_ok:
        lines.append("✓ No duplicate ids, and every id matches its text.")
    else:
        lines.append(
            f"⚠ {len(report.duplicate_ids)} duplicate id(s), "
            f"{len(report.mismatched_ids)} id(s) not matching their text."
        )
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point. Exit 0 unless the corpus fails validation or an integrity check."""
    parser = argparse.ArgumentParser(
        description="Build the F1 corpus coverage report (docs, tokens, licences, by source)."
    )
    parser.add_argument("inputs", type=Path, nargs="+", help="consolidated JSONL corpus files")
    parser.add_argument("--markdown", type=Path, help="write the markdown report here")
    parser.add_argument("--json", type=Path, dest="json_path", help="write the JSON report here")
    parser.add_argument(
        "--require-target",
        action="store_true",
        help="exit 1 if the estimated token count is below the 5 M target",
    )
    args = parser.parse_args(argv)

    missing = [path for path in args.inputs if not path.is_file()]
    if missing:
        for path in missing:
            print(f"error: no such file: {path}", file=sys.stderr)
        return 1

    read = ConsolidationReport()
    documents = read_documents(args.inputs, read)
    if read.invalid:
        print(f"error: {len(read.invalid)} line(s) failed §3.1 validation", file=sys.stderr)
        for error in read.invalid[:20]:
            print(f"  ✗ line {error.line}: {error.reason}", file=sys.stderr)
        return 1

    report = build_report(documents)
    markdown = to_markdown(report)
    if args.markdown:
        args.markdown.parent.mkdir(parents=True, exist_ok=True)
        args.markdown.write_text(markdown, encoding="utf-8")
    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(to_json(report) + "\n", encoding="utf-8")
    if not args.markdown and not args.json_path:
        print(markdown, end="")
    else:
        print(
            f"{report.total.documents} documents, "
            f"≈{report.total.estimated_tokens} tokens ({report.target_status} target)"
        )

    if not report.integrity_ok:
        print(
            f"error: integrity check failed — {len(report.duplicate_ids)} duplicate id(s), "
            f"{len(report.mismatched_ids)} mismatched id(s)",
            file=sys.stderr,
        )
        return 1
    if args.require_target and report.target_status == "below":
        print(
            f"error: ≈{report.total.estimated_tokens} tokens is below the "
            f"{TARGET_MIN_TOKENS} target",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
