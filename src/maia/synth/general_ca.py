"""Anti-forgetting mix — PLAN M2.04.

Fine-tuning on 10k Andorra-specific examples degrades everything the base model knew: it is
called catastrophic forgetting, and the plan's countermeasure is to carry **15-20 % general
Catalan instructions unrelated to Andorra**, drawn from the open AINA datasets.

"Unrelated to Andorra" is the whole point, and it is the one property nothing else in the
pipeline checks. So this module inverts the glossary: the same
``configs/glossari-andorra.yaml`` that M2.03 uses to *require* Andorran lexicon is used here to
**reject** it. An AINA sample that happens to include Andorran content is not merely off-target
— it silently shrinks the anti-forgetting mix to something smaller than the report claims, and
it can smuggle unvetted Andorran facts into the weights outside the grounded pipeline.

Three filters, each with a counted drop reason:

* **Andorra-related** — rejected. Glossary terms plus the core toponyms and institutions no
  glossary would list as *lexicon* (``Andorra``, ``Meritxell``, ``Valira``…).
* **Not Catalan** — rejected, reusing :func:`maia.corpus.language.is_catalan`. AINA is Catalan
  data, but a mixed corpus can carry Spanish rows, and a Spanish row in the anti-forgetting mix
  teaches the model the wrong thing about what Catalan is.
* **Already present** — rejected. Content-hash dedup against the generated examples, so the mix
  never re-teaches something the Andorran half already covers.

:func:`plan_general_ca` then computes **how many** to keep so the finished dataset lands inside
§3.2's 15-20 % band exactly, and :func:`mix` assembles it.

The AINA download is **blocked-by-resource** (network, and the dataset ids are a PO choice).
:class:`InstructionSource` is the seam: :func:`read_jsonl_source` reads a file already fetched,
and the tests drive a list.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from math import ceil, floor
from pathlib import Path
from random import Random
from typing import Protocol
from uuid import UUID, uuid5

from maia.corpus.language import is_catalan
from maia.schemas import DatasetExample, ExampleType, Split
from maia.synth.glossary import Glossary, fold, load_glossary

#: §3.2's band for the anti-forgetting mix.
GENERAL_CA_RANGE = (0.15, 0.20)
#: Where in the band to aim. The midpoint leaves room either side for rounding.
DEFAULT_TARGET_SHARE = 0.175

#: Namespace for deriving ids, so re-running over the same source is idempotent.
_ID_NAMESPACE = UUID("6ba7b813-9dad-11d1-80b4-00c04fd430c8")

#: Andorran proper nouns and institutions that no *lexicon* glossary would list, but whose
#: presence still makes an instruction Andorra-related. The glossary supplies the rest.
CORE_ANDORRAN_TERMS: tuple[str, ...] = (
    "andorra",
    "andorrà",
    "andorrana",
    "andorrans",
    "andorranes",
    "principat",
    "meritxell",
    "valira",
    "comapedrosa",
    "canillo",
    "encamp",
    "ordino",
    "la massana",
    "sant julià de lòria",
    "escaldes-engordany",
    "coprincipat",
    "copríncep",
    "consell general",
    "batllia",
    "bopa",
)

_WORD_BOUNDARY = r"(?:^|(?<=[^\w]))"


@dataclass(frozen=True)
class Instruction:
    """One instruction/response pair from an upstream dataset, before §3.2 conversion."""

    prompt: str
    response: str
    origin: str

    @property
    def text(self) -> str:
        """Both halves, for the language and relatedness filters."""
        return f"{self.prompt}\n{self.response}"

    @property
    def fingerprint(self) -> str:
        """Content hash — the dedup key against the generated half."""
        return hashlib.sha256(fold(self.text).encode("utf-8")).hexdigest()


class InstructionSource(Protocol):
    """An upstream instruction dataset. The AINA download is blocked-by-resource."""

    def __iter__(self) -> Iterable[Instruction]:
        """Yield instruction pairs."""


#: A pattern that can never match, for when one half of the matcher has no terms. An empty
#: alternation would match the empty string and reject the whole corpus.
_NEVER = re.compile(r"(?!)")


@dataclass(frozen=True)
class AndorraMatcher:
    """Andorran terms, split by whether accent-folding them is safe.

    Folding accents is what lets *sant julia de loria* match ``Sant Julià de Lòria`` in text that
    dropped its accents. But Catalan accents are **contrastive**, so folding a single word can
    turn an Andorran term into an everyday one: ``solà`` (a sun-facing slope) folds to ``sola``,
    which fires on *un organisme d'una sola cèl·lula* and would have thrown away a quarter of a
    perfectly good general-Catalan corpus. So single accented words are matched **as written**,
    and everything else is matched folded, where collisions are negligible.
    """

    #: Matched against ``fold(text)`` — unaccented and multi-word terms.
    folded: re.Pattern[str]
    #: Matched against the text as written — single words whose accents carry the distinction.
    exact: re.Pattern[str]

    def find(self, text: str) -> str | None:
        """The first Andorran term in ``text``, or ``None``."""
        for pattern, subject in ((self.exact, text), (self.folded, fold(text))):
            found = pattern.search(subject)
            if found is not None:
                return found.group(0)
        return None


def andorra_matcher(glossary: Glossary | None = None) -> AndorraMatcher:
    """A matcher for Andorran terms, used to **reject** Andorra-related instructions.

    Built from :data:`CORE_ANDORRAN_TERMS` plus every form in the glossary. Deliberately the
    same source of truth M2.03 uses to *require* this lexicon: if a term is Andorran enough to
    demand in the Andorran half, it is Andorran enough to exclude from the anti-forgetting half.
    """
    terms = {term.lower() for term in CORE_ANDORRAN_TERMS}
    if glossary is not None:
        terms.update(form.lower() for entry in glossary.entries for form in entry.forms)
    exact = {term for term in terms if _accent_sensitive(term)}
    return AndorraMatcher(
        folded=_pattern({fold(term) for term in terms - exact}), exact=_pattern(exact)
    )


def _accent_sensitive(term: str) -> bool:
    """Whether ``term`` must keep its accents to stay a reliable Andorra signal.

    True for a single word that loses a contrastive accent when folded — see
    :class:`AndorraMatcher`.
    """
    return fold(term) != term and " " not in term


def _pattern(terms: set[str]) -> re.Pattern[str]:
    """One alternation over ``terms``, longest first so the longest match wins."""
    if not terms:
        return _NEVER
    ordered = sorted(terms, key=len, reverse=True)
    joined = "|".join(re.escape(term).replace(r"\ ", r"\s+") for term in ordered)
    return re.compile(rf"{_WORD_BOUNDARY}(?:{joined})\b", re.IGNORECASE)


def mentions_andorra(text: str, matcher: AndorraMatcher) -> bool:
    """Whether ``text`` is Andorra-related and therefore unusable as anti-forgetting data."""
    return matcher.find(text) is not None


def plan_general_ca(generated: int, target_share: float = DEFAULT_TARGET_SHARE) -> int:
    """How many ``general_ca`` examples to add beside ``generated`` to hit ``target_share``.

    Solving ``n / (generated + n) == share`` gives ``n = generated · share / (1 - share)``. The
    aim is then **clamped into the whole numbers that actually land inside §3.2's band**, because
    rounding a share is not the same as satisfying a range: at small totals the nearest integer
    can sit outside it, and the validator checks the finished dataset, not the intent.

    Raises:
        ValueError: if ``target_share`` is outside §3.2's 15-20 % band, if ``generated`` is not
            positive, or if no whole number of examples can put a corpus this small in band
            (below 5 generated examples, every possible mix overshoots 20 %).
    """
    low, high = GENERAL_CA_RANGE
    if not low <= target_share <= high:
        raise ValueError(f"target_share {target_share} is outside §3.2's {low:.0%}-{high:.0%} band")
    if generated <= 0:
        raise ValueError("generated must be positive")

    smallest = ceil(generated * low / (1 - low))
    largest = floor(generated * high / (1 - high))
    if smallest > largest or largest <= 0:
        raise ValueError(
            f"no whole number of general_ca examples puts {generated} generated example(s) "
            f"inside §3.2's {low:.0%}-{high:.0%} band — the generated half is too small to mix"
        )
    aim = round(generated * target_share / (1 - target_share))
    return min(max(aim, smallest), largest)


def to_example(
    instruction: Instruction, *, split: Split = Split.TRAIN, generator: str | None = None
) -> DatasetExample:
    """Convert one instruction to a §3.2 ``general_ca`` example.

    ``grounding_ids`` is empty and the schema enforces that: ``general_ca`` is unrelated to
    Andorra by construction, so citing corpus passages would be a contradiction.
    """
    return DatasetExample.model_validate(
        {
            "id": str(uuid5(_ID_NAMESPACE, f"{instruction.origin}|{instruction.fingerprint}")),
            "messages": [
                {"role": "user", "content": instruction.prompt},
                {"role": "assistant", "content": instruction.response},
            ],
            "type": ExampleType.GENERAL_CA.value,
            "topic": f"general_ca/{instruction.origin}",
            "grounding_ids": [],
            "generator": generator or instruction.origin,
            # Not judged: the anti-forgetting mix is upstream human/curated data, not generated
            # output, so M2.05's factual-support judge does not apply to it.
            "judge_score": 0.0,
            "split": split.value,
        }
    )


@dataclass
class MixReport:
    """What the mix took, and what each filter dropped."""

    considered: int = 0
    accepted: int = 0
    drops: dict[str, int] = field(default_factory=dict)
    generated: int = 0
    wanted: int = 0

    def drop(self, reason: str) -> None:
        """Record one rejection."""
        self.drops[reason] = self.drops.get(reason, 0) + 1

    @property
    def share(self) -> float:
        """The realised ``general_ca`` share of the finished dataset."""
        total = self.generated + self.accepted
        return self.accepted / total if total else 0.0

    @property
    def in_band(self) -> bool:
        """Whether the realised share satisfies §3.2."""
        low, high = GENERAL_CA_RANGE
        return low <= self.share <= high

    @property
    def short(self) -> int:
        """How many examples the source could not supply."""
        return max(0, self.wanted - self.accepted)


def select(
    source: Iterable[Instruction],
    *,
    wanted: int,
    matcher: AndorraMatcher,
    exclude: set[str],
    rng: Random,
    report: MixReport,
) -> list[Instruction]:
    """Take up to ``wanted`` usable instructions, counting every rejection.

    Candidates are collected, shuffled with ``rng``, then taken — so the selection is
    reproducible from a seed and is not biased towards whatever the source happens to list
    first.
    """
    usable: list[Instruction] = []
    seen: set[str] = set()
    for instruction in source:
        report.considered += 1
        if not instruction.prompt.strip() or not instruction.response.strip():
            report.drop("empty")
            continue
        if mentions_andorra(instruction.text, matcher):
            report.drop("andorra-related")
            continue
        if not is_catalan(instruction.text):
            report.drop("not-catalan")
            continue
        if instruction.fingerprint in exclude:
            report.drop("already-in-dataset")
            continue
        if instruction.fingerprint in seen:
            report.drop("duplicate-in-source")
            continue
        seen.add(instruction.fingerprint)
        usable.append(instruction)

    usable.sort(key=lambda item: item.fingerprint)
    rng.shuffle(usable)
    chosen = usable[:wanted]
    report.accepted = len(chosen)
    return chosen


def fingerprints_of(examples: Iterable[DatasetExample]) -> set[str]:
    """Content hashes of already-present examples, for dedup against the mix."""
    return {
        hashlib.sha256(
            fold("\n".join(message.content for message in example.messages)).encode("utf-8")
        ).hexdigest()
        for example in examples
    }


def mix(
    generated: Sequence[DatasetExample],
    source: Iterable[Instruction],
    *,
    glossary: Glossary | None = None,
    target_share: float = DEFAULT_TARGET_SHARE,
    seed: int,
    split: Split = Split.TRAIN,
) -> tuple[list[DatasetExample], MixReport]:
    """Combine the generated half with an anti-forgetting mix that lands in §3.2's band."""
    report = MixReport(generated=len(generated))
    report.wanted = plan_general_ca(len(generated), target_share)
    chosen = select(
        source,
        wanted=report.wanted,
        matcher=andorra_matcher(glossary),
        exclude=fingerprints_of(generated),
        rng=Random(seed),
        report=report,
    )
    added = [to_example(instruction, split=split) for instruction in chosen]
    return [*generated, *added], report


def read_jsonl_source(path: Path, *, origin: str | None = None) -> list[Instruction]:
    """Read instructions from a JSONL file already fetched from AINA.

    Accepts the common shapes — ``{"instruction", "output"}``, ``{"prompt", "response"}``, or a
    chat ``{"messages": [...]}`` — because the AINA collection is not uniform and normalising at
    the edge beats a converter per dataset.

    Raises:
        ValueError: naming the line whose shape is unrecognised. A silently skipped row would
            quietly shrink the mix.
    """
    name = origin or path.stem
    instructions: list[Instruction] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        row = json.loads(line)
        prompt, response = _fields_of(row)
        if prompt is None or response is None:
            raise ValueError(
                f"{path}:{number}: unrecognised shape; expected instruction/output, "
                f"prompt/response, or messages — got keys {sorted(row)}"
            )
        instructions.append(Instruction(prompt=prompt, response=response, origin=name))
    return instructions


def _fields_of(row: dict[str, object]) -> tuple[str | None, str | None]:
    """Pull the prompt and response out of one upstream row, whatever shape it uses."""
    for prompt_key, response_key in (("instruction", "output"), ("prompt", "response")):
        prompt, response = row.get(prompt_key), row.get(response_key)
        if isinstance(prompt, str) and isinstance(response, str):
            # Some AINA rows carry an extra `input` that belongs with the instruction.
            extra = row.get("input")
            if isinstance(extra, str) and extra.strip():
                prompt = f"{prompt}\n\n{extra}"
            return prompt, response
    messages = row.get("messages")
    if isinstance(messages, list) and len(messages) >= 2:
        first, second = messages[0], messages[1]
        if isinstance(first, dict) and isinstance(second, dict):
            prompt, response = first.get("content"), second.get("content")
            if isinstance(prompt, str) and isinstance(response, str):
                return prompt, response
    return None, None


def render(report: MixReport) -> str:
    """Human-readable summary of a mix."""
    status = "✓ in band" if report.in_band else "✗ OUT OF BAND"
    low, high = GENERAL_CA_RANGE
    lines = [
        f"general_ca: {report.accepted} added to {report.generated} generated "
        f"= {report.share:.1%} [{status}, §3.2 wants {low:.0%}-{high:.0%}]",
        f"  considered {report.considered} instruction(s), wanted {report.wanted}",
    ]
    if report.drops:
        lines.append(
            "  dropped: "
            + ", ".join(f"{reason}={count}" for reason, count in sorted(report.drops.items()))
        )
    if report.short:
        lines.append(
            f"  ⚠ {report.short} short — the source could not supply enough usable Catalan "
            "instructions unrelated to Andorra"
        )
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point. Exit 0 when the realised share satisfies §3.2."""
    parser = argparse.ArgumentParser(
        description="Mix an anti-forgetting share of general Catalan instructions (AINA) into a "
        "generated dataset, rejecting anything Andorra-related."
    )
    parser.add_argument("dataset", type=Path, help="the generated §3.2 dataset (JSONL)")
    parser.add_argument("--aina", type=Path, nargs="+", required=True, help="AINA JSONL file(s)")
    parser.add_argument("--glossary", type=Path, help="configs/glossari-andorra.yaml")
    parser.add_argument("--out", type=Path, help="write the mixed dataset here")
    parser.add_argument("--target-share", type=float, default=DEFAULT_TARGET_SHARE)
    parser.add_argument("--seed", type=int, default=20260725)
    args = parser.parse_args(argv)

    paths = [args.dataset, *args.aina, *([args.glossary] if args.glossary else [])]
    for path in paths:
        if not path.is_file():
            print(f"error: no such file: {path}", file=sys.stderr)
            return 1

    generated = [
        DatasetExample.model_validate_json(line)
        for line in args.dataset.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    try:
        instructions = [
            instruction for path in args.aina for instruction in read_jsonl_source(path)
        ]
        glossary = load_glossary(args.glossary) if args.glossary else None
        examples, report = mix(
            generated,
            instructions,
            glossary=glossary,
            target_share=args.target_share,
            seed=args.seed,
        )
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(
            "".join(f"{example.model_dump_json()}\n" for example in examples), encoding="utf-8"
        )
    print(render(report))
    return 0 if report.in_band else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
