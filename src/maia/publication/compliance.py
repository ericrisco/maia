"""The legal gate before publication — PLAN M6.01, a hard gate.

*"Legal cleanup (M6.01, hard gate): script verifies 0 examples with `no-redistribute` grounding, 0
attributed political opinions, CC-BY-SA attributions present. Final PO manual review."*

This is the last automated thing between the project and a public artifact it cannot take back, so
every check fails closed. Three of the four are mechanical; the interesting one is not.

**Restricted grounding: zero, and unverifiable counts as restricted.** M2.11 already withholds these
from the dataset drop; this re-checks at the boundary, because a hard gate that trusts an earlier
step is a hard gate in name only. An example whose grounding is *not in the corpus supplied* cannot
be shown to be clean, and "we could not check" has never been a licence here (D-0024, D-0032).

**Attributed political opinions: the hard one, and deliberately over-broad.** The Diari de Sessions
is public official text, and a parliamentary speech *attributed to the councillor who gave it* is
exactly what the plan forbids republishing as training data. Detecting opinion is not a job for a
regular expression, so this does not try: it flags **attribution near stance vocabulary**, accepts
that it will over-flag, and hands the list to the PO review the plan requires anyway. The asymmetry
is the point — under-flagging publishes a named politician's position, over-flagging costs an
afternoon.

**CC-BY-SA attribution: present, per source.** Viquipèdia derivatives require it, so the
attribution section is what makes the release lawful rather than convenient. A missing one is not a
formatting problem. The licence itself comes from :mod:`maia.licensing`: this gate once required
the card to name a *different* licence than the upload declared, and neither side noticed because
each was checked against itself.

Its verdict is **advisory to the PO and blocking to the pipeline**: `passed` gates the upload, and
the report says in words that a green result is not the PO's approval.
"""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field

from maia.licensing import DATASET_LICENSE_LABEL, states_dataset_licence
from maia.schemas import CorpusDocument, DatasetExample, License, Source

#: Licences whose derivatives must be credited in the dataset card.
SHARE_ALIKE = frozenset({License.CC_BY_SA_3_0})

#: Vocabulary that marks a *stance* rather than a fact. Broad on purpose — see the module docstring.
#:
#: **Both grammatical persons, and the third one is the one that matters here.** The first version
#: of this list was written from the Diari, where members speak for themselves ("jo considero
#: que…"), so every entry was first-person. But what this gate reviews is not the Diari — it is
#: *generated* examples, and a model writing about a politician writes in the third person: "el cap
#: de Govern considera que la reforma és necessària". That sentence attributes a political position
#: to a head of government in office, and the first-person list let it straight through.
STANCE_WORDS = (
    # ── first person: quoted or paraphrased speech ──
    "crec",
    "creiem",
    "opino",
    "opinem",
    "considero",
    "considerem",
    "defenso",
    "defensem",
    "rebutjo",
    "rebutgem",
    "condemno",
    "condemnem",
    "exigim",
    "exigeixo",
    "inacceptable",
    "irresponsable",
    "vergonyós",
    "escandalós",
    "el nostre grup",
    "el meu grup",
    "aquesta majoria",
    "aquest govern",
    "votarem",
    "votaré",
    "no donarem suport",
    # ── third person: how a generated example talks *about* somebody ──
    "creu que",
    "creuen que",
    "opina",
    "opinen",
    "considera",
    "consideren",
    "defensa",
    "defensen",
    "rebutja",
    "rebutgen",
    "condemna",
    "condemnen",
    "exigeix",
    "exigeixen",
    "sosté",
    "sostenen",
    "es mostra",
    "es mostren",
    "està a favor",
    "està en contra",
    "votarà",
    "votaran",
    "no donarà suport",
    "no donaran suport",
    "partidari",
    "partidària",
    "contrari a",
    "contrària a",
)

#: Patterns that attribute speech to a named person or role, in Andorran parliamentary style.
ATTRIBUTION = re.compile(
    r"(?:"
    r"\b(?:el|la)\s+(?:senyor|senyora|conseller|consellera|síndic|síndica|ministre|ministra|"
    r"cònsol)\b"
    r"|\bcap\s+de\s+govern\b"
    r"|\bsegons\s+(?:el|la)\s+\w+"
    r"|\b(?:va\s+dir|afirma|declara|sosté|manifesta)\b"
    r")",
    re.IGNORECASE,
)

#: How close attribution and stance must be, in characters. A whole example is too coarse: a factual
#: answer can mention a councillor and, paragraphs later, quote a manifesto.
PROXIMITY = 240


def fold(text: str) -> str:
    """Lowercase and strip accents, for matching."""
    decomposed = unicodedata.normalize("NFD", text.lower())
    return "".join(char for char in decomposed if not unicodedata.combining(char))


_FOLDED_STANCE = tuple(fold(word) for word in STANCE_WORDS)


@dataclass(frozen=True)
class Finding:
    """One thing that must be resolved before publication."""

    kind: str
    example_id: str
    detail: str


def restricted_grounding(
    examples: Sequence[DatasetExample], corpus: Mapping[str, CorpusDocument]
) -> list[Finding]:
    """Examples grounded in text that may not be redistributed, or in text nobody can check.

    Re-checked here even though M2.11 already withholds them: a hard gate that trusts an earlier
    step is a hard gate in name only.
    """
    findings: list[Finding] = []
    for example in examples:
        for ident in example.grounding_ids:
            document = corpus.get(ident)
            if document is None:
                findings.append(
                    Finding(
                        "unverifiable-grounding",
                        str(example.id),
                        f"grounding {ident[:16]}… is not in the corpus supplied, so this example "
                        "cannot be shown to be publishable",
                    )
                )
            elif not document.license.is_public():
                findings.append(
                    Finding(
                        "restricted-grounding",
                        str(example.id),
                        f"grounded in {document.license.value} text ({ident[:16]}…)",
                    )
                )
    return findings


def attributed_opinions(examples: Sequence[DatasetExample]) -> list[Finding]:
    """Examples that attribute a stance to a named person or role.

    Deliberately over-broad, and it stops at the first hit per example: the output is a review
    queue, not a count, and a second finding in the same example tells the reviewer nothing new.
    """
    findings: list[Finding] = []
    for example in examples:
        text = "\n".join(message.content for message in example.messages)
        folded = fold(text)
        for match in ATTRIBUTION.finditer(text):
            start = max(0, match.start() - PROXIMITY)
            window = folded[start : match.end() + PROXIMITY]
            hit = next((word for word in _FOLDED_STANCE if word in window), None)
            if hit is not None:
                findings.append(
                    Finding(
                        "attributed-opinion",
                        str(example.id),
                        f"{match.group(0)!r} within {PROXIMITY} characters of {hit!r} — "
                        "needs PO review before publication",
                    )
                )
                break
    return findings


def sources_needing_attribution(
    examples: Sequence[DatasetExample], corpus: Mapping[str, CorpusDocument]
) -> set[Source]:
    """Which sources the published dataset must credit.

    Only the sources actually **cited** by what is being published: crediting one the dataset does
    not draw on is noise, and omitting one it does draw on is the licence problem.
    """
    cited = {ident for example in examples for ident in example.grounding_ids}
    found: set[Source] = set()
    for ident in cited:
        document = corpus.get(ident)
        if document is not None and document.license in SHARE_ALIKE:
            found.add(document.source)
    return found


def missing_attributions(
    examples: Sequence[DatasetExample],
    corpus: Mapping[str, CorpusDocument],
    card: str,
) -> list[Finding]:
    """Share-alike sources the dataset card fails to credit.

    Not a formatting problem: the CC-BY-SA attribution is what makes shipping the derivative
    lawful rather than merely convenient.
    """
    lowered = card.lower()
    return [
        Finding(
            "missing-attribution",
            f"<{source.value}>",
            f"{source.value} is share-alike and is cited by this dataset, but the card does not "
            f"credit it; the attribution is what makes the {DATASET_LICENSE_LABEL} release lawful",
        )
        for source in sorted(
            sources_needing_attribution(examples, corpus), key=lambda item: item.value
        )
        if source.value not in lowered
    ]


def missing_licence_statement(card: str) -> list[Finding]:
    """Whether the card states the dataset's own licence.

    A card that credits every source and never says what *this* is licensed under leaves the
    downstream user without the one fact they need.
    """
    if states_dataset_licence(card):
        return []
    return [
        Finding(
            "missing-licence",
            "<card>",
            f"the card does not state the dataset licence ({DATASET_LICENSE_LABEL}), so a "
            "downstream user cannot tell what they may do with it",
        )
    ]


@dataclass
class ComplianceReport:
    """The M6.01 verdict."""

    examples: int = 0
    findings: list[Finding] = field(default_factory=list)
    card_checked: bool = False
    corpus_supplied: bool = False

    def of_kind(self, kind: str) -> list[Finding]:
        """Findings of one kind."""
        return [finding for finding in self.findings if finding.kind == kind]

    @property
    def blocking(self) -> list[Finding]:
        """Findings that stop publication outright.

        Attributed opinions are **not** here: they are the PO's to rule on, and a regular expression
        should not block a release on a guess about intent. Everything else is mechanical and
        blocks.
        """
        return [finding for finding in self.findings if finding.kind != "attributed-opinion"]

    @property
    def needs_review(self) -> list[Finding]:
        """Findings the PO must look at before the release goes out."""
        return self.of_kind("attributed-opinion")

    @property
    def passed(self) -> bool:
        """Whether the pipeline may proceed.

        Requires the corpus **and** the card: a gate run without its inputs verified nothing, and
        this is the one gate whose failure is irreversible.
        """
        return self.corpus_supplied and self.card_checked and not self.blocking


def check(
    examples: Sequence[DatasetExample],
    *,
    corpus: Mapping[str, CorpusDocument] | None = None,
    card: str | None = None,
) -> ComplianceReport:
    """Run every M6.01 check.

    Both inputs are optional in the signature and **required to pass**: this reports what it could
    not check rather than refusing to run, so a partial run stays useful during development while
    never reading as a green gate.
    """
    report = ComplianceReport(
        examples=len(examples),
        corpus_supplied=corpus is not None,
        card_checked=card is not None,
    )
    if corpus is not None:
        report.findings.extend(restricted_grounding(examples, corpus))
    report.findings.extend(attributed_opinions(examples))
    if card is not None:
        report.findings.extend(missing_licence_statement(card))
        if corpus is not None:
            report.findings.extend(missing_attributions(examples, corpus, card))
    return report


def render(report: ComplianceReport) -> str:
    """The gate's verdict, and what a green one does not mean."""
    mark = "✓ PASS" if report.passed else "✗ BLOCKED"
    lines = [f"{mark} — M6.01 legal gate over {report.examples} example(s)"]

    if not report.corpus_supplied:
        lines.append(
            "  ✗ no corpus supplied, so grounding licences were NOT CHECKED — a §3.2 example "
            "carries no licence of its own (D-0024)"
        )
    if not report.card_checked:
        lines.append("  ✗ no dataset card supplied, so attributions were NOT CHECKED")

    for kind, label in (
        ("restricted-grounding", "grounded in no-redistribute text"),
        ("unverifiable-grounding", "grounding not in the corpus supplied"),
        ("missing-attribution", "share-alike source not credited"),
        ("missing-licence", "dataset licence not stated"),
    ):
        found = report.of_kind(kind)
        lines.append(f"  {'✓' if not found else '✗'} {label}: {len(found)}")
        for finding in found[:3]:
            lines.append(f"      {finding.example_id[:12]}… {finding.detail}")

    review = report.needs_review
    lines.append(f"  {'✓' if not review else '⚠'} attributed opinions to review: {len(review)}")
    for finding in review[:5]:
        lines.append(f"      {finding.example_id[:12]}… {finding.detail}")
    if review:
        lines.append(
            "      flagged over-broadly on purpose: detecting opinion is not a job for a regular "
            "expression, and under-flagging would publish a named politician's position"
        )
    lines.append(
        "  a green result is NOT the PO's approval: M6.01 requires a final manual review, and this "
        "gate only says nothing mechanical is left to find"
    )
    return "\n".join(lines)


def attribution_section(sources: Iterable[Source]) -> str:
    """The card's attribution block, so a required credit cannot be omitted by accident."""
    listed = sorted({source.value for source in sources})
    if not listed:
        return ""
    lines = [
        "## Attributions",
        "",
        "This dataset derives from the sources below. Share-alike sources are credited as their "
        f"licence requires; the dataset itself is released under **{DATASET_LICENSE_LABEL}**, "
        "which share-alike obliges rather than merely permits.",
        "",
    ]
    lines += [f"- `{source}`" for source in listed]
    return "\n".join(lines)
