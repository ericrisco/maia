"""Andorran lexicon glossary — PLAN M2.02.

The words a general Catalan model gets wrong or has never seen: *síndic*, *cònsol*, *batlle*,
*quart*, *borda*, *canalla*. The plan asks for an *automatic* glossary of Andorran lexicon
"absent from general Catalan", used two ways — required in generation prompts so the dataset
uses these words naturally, and measured afterwards so "we required it" becomes a number.

Three pieces, and the split between them is the honest part:

* :func:`extract_candidates` is **contrastive and automatic**. Given Andorran documents and a
  general-Catalan reference, it ranks terms by how much more they occur on the Andorran side.
  It cannot decide *on its own* what counts as an Andorranism, because that needs a reference
  corpus this project does not have yet (AINA's general Catalan arrives with the M2.04
  anti-forgetting mix) — so it produces **candidates for review**, not conclusions.
* ``configs/glossari-andorra.yaml`` is a **curated seed**, shipped unapproved, holding the
  terms that are Andorranisms beyond argument. It is what M2.03 can start from before the
  reference corpus exists.
* :func:`check_usage` closes the loop. "Require its natural use" is only meaningful if it is
  measured: this reports which glossary terms actually reached the generated dataset and which
  never did, which is the input to M2.09's distribution report.

Matching is **accent- and case-insensitive over word boundaries**, and multi-word terms are
matched as phrases. That matters more than it sounds: *comú* and *comu* must be the same term,
and a substring match would find *cònsol* inside *consolidació*.
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from collections import Counter
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Self

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from maia.schemas import CorpusDocument, DatasetExample

#: A term must occur at least this often on the Andorran side to be a candidate.
DEFAULT_MIN_COUNT = 5
#: …and at least this many times more often than in general Catalan.
DEFAULT_MIN_RATIO = 3.0

_WORD = re.compile(r"[^\W\d_]+", re.UNICODE)


class Category(StrEnum):
    """Which part of Andorran life a term belongs to.

    The categories mirror the taxonomy's ``lexic`` branch, so a glossary gap and a taxonomy
    gap can be read against each other.
    """

    INSTITUCIONAL = "institucional"
    JURIDIC = "juridic"
    ADMINISTRATIU = "administratiu"
    GEOGRAFIC = "geografic"
    CULTURAL = "cultural"
    QUOTIDIA = "quotidia"


def fold(text: str) -> str:
    """Lowercase and strip accents — the comparison form for every match in this module.

    Without it *comú* and *comu* are different terms, and the Andorran corpus contains both.
    """
    decomposed = unicodedata.normalize("NFD", text.lower())
    return "".join(char for char in decomposed if not unicodedata.combining(char))


class GlossaryEntry(BaseModel):
    """One Andorran term."""

    model_config = ConfigDict(extra="forbid")

    term: str = Field(min_length=2)
    category: Category
    #: A one-line explanation. Goes into the generation prompt, so it must be usable as-is.
    gloss: str = Field(min_length=5)
    #: The general-Catalan word that would be used instead, when one exists. Empty means the
    #: concept itself is Andorran and has no equivalent — which is the interesting case.
    equivalent: str = ""
    #: Other surface forms (plural, feminine, common shortening) that count as this term.
    variants: list[str] = Field(default_factory=list)
    notes: str = ""

    @model_validator(mode="after")
    def _check_forms(self) -> Self:
        for form in self.forms:
            if not form.strip():
                raise ValueError(f"term {self.term!r} has an empty variant")
        folded = [fold(form) for form in self.forms]
        if len(set(folded)) != len(folded):
            # Easy hand-edit slip: `term: Escudella` with `variants: [escudella]`. Matching is
            # accent- and case-insensitive, so those are the same form.
            raise ValueError(
                f"term {self.term!r} repeats a form in its variants (matching ignores case "
                "and accents)"
            )
        if self.equivalent and fold(self.equivalent) == fold(self.term):
            raise ValueError(f"term {self.term!r} lists itself as its general-Catalan equivalent")
        return self

    @property
    def forms(self) -> list[str]:
        """Every surface form that counts as this term."""
        return [self.term, *self.variants]

    def pattern(self) -> re.Pattern[str]:
        """A word-boundary pattern over the folded forms.

        Word boundaries are what stop *cònsol* from matching inside *consolidació*, and
        multi-word terms are matched as phrases with flexible whitespace.
        """
        alternatives = sorted((fold(form) for form in self.forms), key=len, reverse=True)
        joined = "|".join(re.escape(form).replace(r"\ ", r"\s+") for form in alternatives)
        return re.compile(rf"\b(?:{joined})\b")


class Glossary(BaseModel):
    """The whole term list, with the same approval gate as the taxonomy."""

    model_config = ConfigDict(extra="forbid")

    version: str = Field(min_length=1)
    approved: bool = False
    approved_by: str = ""
    notes: str = ""
    entries: list[GlossaryEntry] = Field(min_length=1)

    @model_validator(mode="after")
    def _check_unique(self) -> Self:
        counts = Counter(fold(form) for entry in self.entries for form in entry.forms)
        duplicates = sorted(form for form, count in counts.items() if count > 1)
        if duplicates:
            raise ValueError(f"terms or variants appear more than once: {', '.join(duplicates)}")
        if self.approved and not self.approved_by:
            raise ValueError("approved=true requires approved_by")
        return self

    @property
    def by_category(self) -> dict[str, list[GlossaryEntry]]:
        """Entries grouped by category, in file order."""
        grouped: dict[str, list[GlossaryEntry]] = {}
        for entry in self.entries:
            grouped.setdefault(entry.category.value, []).append(entry)
        return grouped

    def prompt_lines(self, categories: Iterable[Category] | None = None) -> list[str]:
        """The glossary as prompt material for the generator.

        One line per term, with its gloss and its general-Catalan equivalent where there is
        one — the equivalent is the useful half, because it tells the generator which word
        *not* to reach for.
        """
        wanted = set(categories) if categories is not None else None
        lines: list[str] = []
        for entry in self.entries:
            if wanted is not None and entry.category not in wanted:
                continue
            line = f"- {entry.term}: {entry.gloss}"
            if entry.equivalent:
                line += f" (en català general: {entry.equivalent})"
            lines.append(line)
        return lines


def load_glossary(path: str | Path) -> Glossary:
    """Read and validate ``configs/glossari-andorra.yaml``."""
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"{path}: expected a YAML mapping, got {type(raw).__name__}")
    try:
        return Glossary.model_validate(raw)
    except ValidationError as exc:
        details = "; ".join(
            f"{'.'.join(str(part) for part in error['loc']) or '<root>'}: {error['msg']}"
            for error in exc.errors()
        )
        raise ValueError(f"{path}: {details}") from exc


@dataclass(frozen=True)
class Candidate:
    """A term that looks Andorran, for review."""

    term: str
    andorran_count: int
    general_count: int
    ratio: float


def _word_counts(texts: Iterable[str]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for text in texts:
        counts.update(_WORD.findall(fold(text)))
    return counts


def extract_candidates(
    andorran: Iterable[CorpusDocument],
    general: Iterable[CorpusDocument],
    *,
    min_count: int = DEFAULT_MIN_COUNT,
    min_ratio: float = DEFAULT_MIN_RATIO,
    limit: int = 200,
) -> list[Candidate]:
    """Rank words that are far more frequent in Andorran text than in general Catalan.

    Frequencies are normalized by corpus size, so an Andorran corpus ten times smaller than
    the reference does not make every word look Andorran. A word absent from the reference
    gets the largest possible ratio, which is the case we most want at the top.

    This produces **candidates**, not conclusions: deciding that a frequent word is genuinely
    an Andorranism rather than an artifact of what the corpus happens to be about is a
    judgement, and it is the PO's.
    """
    andorran_counts = _word_counts(document.text for document in andorran)
    general_counts = _word_counts(document.text for document in general)
    andorran_total = sum(andorran_counts.values()) or 1
    general_total = sum(general_counts.values()) or 1

    candidates: list[Candidate] = []
    for term, count in andorran_counts.items():
        if count < min_count or len(term) < 3:
            continue
        andorran_rate = count / andorran_total
        general_rate = general_counts.get(term, 0) / general_total
        ratio = andorran_rate / general_rate if general_rate else float("inf")
        if ratio >= min_ratio:
            candidates.append(Candidate(term, count, general_counts.get(term, 0), ratio))

    candidates.sort(
        key=lambda c: (-c.ratio if c.ratio != float("inf") else -1e18, -c.andorran_count, c.term)
    )
    return candidates[:limit]


@dataclass
class UsageReport:
    """Which glossary terms reached the dataset, and which did not."""

    examples: int = 0
    counts: Counter[str] = field(default_factory=Counter)
    #: Terms whose general-Catalan equivalent was used instead of the Andorran one.
    equivalents_used: Counter[str] = field(default_factory=Counter)

    @property
    def used(self) -> list[str]:
        """Terms that appeared at least once."""
        return sorted(term for term, count in self.counts.items() if count)

    @property
    def unused(self) -> list[str]:
        """Terms that never appeared — the gap "require natural use" is meant to close."""
        return sorted(term for term, count in self.counts.items() if not count)

    @property
    def coverage(self) -> float:
        """Share of glossary terms that reached the dataset."""
        return len(self.used) / len(self.counts) if self.counts else 0.0


def check_usage(examples: Iterable[DatasetExample], glossary: Glossary) -> UsageReport:
    """Measure how much of the glossary the generated dataset actually uses.

    Also counts, per term, how often the **general-Catalan equivalent** was used instead. A
    dataset that says *alcalde* where an Andorran would say *cònsol* has failed at exactly the
    thing this glossary exists for, and the term count alone would not show it.
    """
    report = UsageReport()
    patterns = {entry.term: entry.pattern() for entry in glossary.entries}
    equivalents = {
        entry.term: re.compile(rf"\b{re.escape(fold(entry.equivalent))}\b")
        for entry in glossary.entries
        if entry.equivalent
    }
    for term in patterns:
        report.counts[term] = 0

    for example in examples:
        report.examples += 1
        text = fold(" ".join(message.content for message in example.messages))
        for term, pattern in patterns.items():
            report.counts[term] += len(pattern.findall(text))
        for term, pattern in equivalents.items():
            report.equivalents_used[term] += len(pattern.findall(text))
    return report


def render_glossary(glossary: Glossary, path: Path) -> str:
    """Human-readable summary of a glossary file."""
    status = "approved" if glossary.approved else "⚠ NOT APPROVED (M2.02 feeds a PO gate)"
    lines = [
        f"glossary: {path} — {len(glossary.entries)} terms [{status}]",
        "  "
        + ", ".join(
            f"{category}={len(entries)}"
            for category, entries in sorted(glossary.by_category.items())
        ),
    ]
    without_equivalent = [e.term for e in glossary.entries if not e.equivalent]
    lines.append(
        f"  {len(without_equivalent)} term(s) with no general-Catalan equivalent "
        "(the concept itself is Andorran)"
    )
    return "\n".join(lines)


def render_usage(report: UsageReport) -> str:
    """Human-readable usage summary."""
    lines = [
        f"glossary usage over {report.examples} example(s): "
        f"{len(report.used)}/{len(report.counts)} terms used ({report.coverage:.0%})",
    ]
    if report.unused:
        lines.append(f"  never used: {', '.join(report.unused[:30])}")
        if len(report.unused) > 30:
            lines.append(f"  … and {len(report.unused) - 30} more")
    swapped = {term: count for term, count in report.equivalents_used.items() if count}
    if swapped:
        lines.append(
            "  ⚠ general-Catalan equivalent used instead: "
            + ", ".join(f"{term}({count})" for term, count in sorted(swapped.items()))
        )
    return "\n".join(lines)


def _read_corpus(paths: Iterable[Path]) -> list[CorpusDocument]:
    return [
        CorpusDocument.model_validate_json(line)
        for path in paths
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _read_dataset(path: Path) -> list[DatasetExample]:
    return [
        DatasetExample.model_validate_json(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def main(argv: Sequence[str] | None = None) -> int:
    """CLI: ``check`` a glossary file, ``candidates`` from a corpus pair, ``usage`` on a dataset."""
    parser = argparse.ArgumentParser(
        description="Validate the Andorran glossary, propose candidate terms from a corpus, "
        "or measure how much of the glossary a generated dataset uses."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    check = sub.add_parser("check", help="validate a glossary file")
    check.add_argument("path", type=Path, help="configs/glossari-andorra.yaml")

    candidates = sub.add_parser("candidates", help="propose terms from a corpus contrast")
    candidates.add_argument("--andorran", type=Path, nargs="+", required=True)
    candidates.add_argument("--general", type=Path, nargs="+", required=True)
    candidates.add_argument("--limit", type=int, default=50)

    usage = sub.add_parser("usage", help="measure glossary usage in a dataset")
    usage.add_argument("path", type=Path, help="configs/glossari-andorra.yaml")
    usage.add_argument("--dataset", type=Path, required=True)

    args = parser.parse_args(argv)
    paths = [args.path] if hasattr(args, "path") else []
    paths += getattr(args, "andorran", []) or []
    paths += getattr(args, "general", []) or []
    if getattr(args, "dataset", None) is not None:
        paths.append(args.dataset)
    for path in paths:
        if not path.is_file():
            print(f"error: no such file: {path}", file=sys.stderr)
            return 1

    if args.command == "candidates":
        proposals = extract_candidates(
            _read_corpus(args.andorran), _read_corpus(args.general), limit=args.limit
        )
        print(f"{len(proposals)} candidate term(s), most Andorran-looking first:")
        for candidate in proposals:
            ratio = "only here" if candidate.ratio == float("inf") else f"{candidate.ratio:.1f}x"
            print(f"  {candidate.term}  ({candidate.andorran_count} occurrences, {ratio})")
        return 0

    try:
        glossary = load_glossary(args.path)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.command == "usage":
        print(render_usage(check_usage(_read_dataset(args.dataset), glossary)))
        return 0

    print(render_glossary(glossary, args.path))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
