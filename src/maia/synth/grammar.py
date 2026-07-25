"""LanguageTool Catalan check — PLAN M2.05, filter 3 of 3.

DoD-F2 wants **≥98 % correct Catalan** in the human sample, and a frontier model writing Catalan
still produces castellanismes, wrong prepositions and missing accents. LanguageTool's ``ca`` rules
catch the mechanical ones cheaply, before a human reads anything.

**The Andorran-lexicon conflict is the reason this module is not a thin HTTP wrapper.**
LanguageTool implements standard Catalan, in the ``ca-ES`` / ``ca-ES-valencia`` variants. There is
no Andorran variant. So the very lexicon M2.03 spent a milestone *requiring* — ``comú``, ``cònsol``,
``síndic``, ``quart``, ``borda`` — is what a spellchecker flags as unknown or as a wrong word
choice. Left alone, filter 3 would systematically delete the examples filters 1 and 2 worked to
produce, and the drop counter would report them as bad Catalan. So spelling and word-choice
matches whose text is in the [glossary](../../../configs/glossari-andorra.yaml) are
**ignored, and counted separately** as :attr:`GrammarReport.andorran_lexicon` — visible, not
silently swallowed, because that count is also the evidence the register injection worked.

Grammatical rules are *not* exempted: an Andorran word in a sentence with a bad preposition is
still a sentence with a bad preposition.

Running LanguageTool is **blocked-by-resource** (an HTTP service, local or hosted).
:class:`GrammarService` is the seam; :func:`languagetool_service` is the live wiring and
:func:`parse_matches` reads its public JSON response shape.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from typing import Protocol

from maia.schemas import DatasetExample
from maia.synth.glossary import Glossary, fold

#: Issues per 1,000 characters at or above which the example is dropped. One typo in a paragraph
#: is not worth losing a grounded example; a sentence with an error every few words is.
DEFAULT_MAX_DENSITY = 4.0

#: The public LanguageTool endpoint. Rate-limited — a local container is the intended deployment.
DEFAULT_ENDPOINT = "https://api.languagetool.org/v2/check"

#: LanguageTool's Catalan language code.
LANGUAGE = "ca-ES"

#: Rule categories that flag a *word* rather than a construction, and are therefore the ones an
#: Andorran term trips. Only these are eligible for the glossary exemption.
LEXICAL_CATEGORIES = frozenset({"TYPOS", "CASING", "CAT_ELA_GEMINADA", "MORFOLOGIK_RULE"})


@dataclass(frozen=True)
class Match:
    """One LanguageTool finding."""

    rule_id: str
    category: str
    message: str
    text: str
    offset: int = 0

    @property
    def is_lexical(self) -> bool:
        """Whether this flags a word choice or spelling, rather than a construction."""
        return self.category.upper() in LEXICAL_CATEGORIES or self.rule_id.upper().startswith(
            "MORFOLOGIK"
        )


class GrammarService(Protocol):
    """A LanguageTool ``/v2/check`` endpoint. Blocked-by-resource."""

    def check(self, text: str, language: str = LANGUAGE) -> list[Match]:
        """Return every match LanguageTool reports for ``text``."""


def andorran_terms(glossary: Glossary | None) -> frozenset[str]:
    """Every accent-folded glossary surface form, for the lexical exemption."""
    if glossary is None:
        return frozenset()
    return frozenset(fold(form) for entry in glossary.entries for form in entry.forms)


def is_andorran_lexicon(match: Match, terms: frozenset[str]) -> bool:
    """Whether ``match`` is LanguageTool objecting to Andorran vocabulary.

    Requires *both* that the rule is lexical and that the flagged text is a glossary term: a
    grammatical rule firing near an Andorran word is a real finding, not a false positive.
    """
    return match.is_lexical and fold(match.text.strip()) in terms


def text_of(example: DatasetExample) -> str:
    """The text checked for one example — the assistant turns only.

    The user turns are the *prompt* side. Their Catalan matters for realism, but a clumsy question
    is a legitimate thing to train on answering, while a clumsy answer is what the model learns to
    write. Judging both would drop examples for the quality of their questions.
    """
    return "\n\n".join(
        message.content for message in example.messages if message.role == "assistant"
    )


def density(matches: Sequence[Match], text: str) -> float:
    """Matches per 1,000 characters. ``0.0`` for empty text — nothing to be wrong about."""
    return len(matches) * 1_000 / len(text) if text else 0.0


@dataclass
class GrammarReport:
    """What the Catalan check examined, excused and dropped."""

    examined: int = 0
    checked: int = 0
    dropped: int = 0
    matches: int = 0
    andorran_lexicon: int = 0
    by_rule: dict[str, int] = field(default_factory=dict)
    worst: list[tuple[str, float]] = field(default_factory=list)

    @property
    def kept(self) -> int:
        """How many examples survive."""
        return self.examined - self.dropped

    def record(self, match: Match) -> None:
        """Count one counted (non-exempt) match."""
        self.matches += 1
        self.by_rule[match.rule_id] = self.by_rule.get(match.rule_id, 0) + 1


@dataclass(frozen=True)
class CatalanCheck:
    """Runs LanguageTool over the assistant turns, excusing Andorran lexicon."""

    service: GrammarService
    glossary: Glossary | None = None
    max_density: float = DEFAULT_MAX_DENSITY
    language: str = LANGUAGE

    def counted_matches(self, text: str) -> tuple[list[Match], int]:
        """``(matches that count, number excused as Andorran lexicon)``."""
        terms = andorran_terms(self.glossary)
        counted: list[Match] = []
        excused = 0
        for match in self.service.check(text, self.language):
            if is_andorran_lexicon(match, terms):
                excused += 1
            else:
                counted.append(match)
        return counted, excused

    def run(self, examples: Sequence[DatasetExample]) -> tuple[list[DatasetExample], GrammarReport]:
        """Drop examples whose assistant turns exceed ``max_density`` issues per 1,000 chars."""
        report = GrammarReport(examined=len(examples))
        survivors: list[DatasetExample] = []
        for example in examples:
            text = text_of(example)
            if not text.strip():
                survivors.append(example)
                continue
            report.checked += 1
            counted, excused = self.counted_matches(text)
            report.andorran_lexicon += excused
            for match in counted:
                report.record(match)
            found = density(counted, text)
            if found > self.max_density:
                report.dropped += 1
                report.worst.append((str(example.id), found))
                continue
            survivors.append(example)
        report.worst.sort(key=lambda item: (-item[1], item[0]))
        return survivors, report


def render(report: GrammarReport) -> str:
    """Human-readable summary."""
    lines = [
        f"Catalan check: {report.kept}/{report.examined} kept ({report.dropped} dropped), "
        f"{report.checked} checked, {report.matches} issue(s)"
    ]
    if report.andorran_lexicon:
        lines.append(
            f"  {report.andorran_lexicon} match(es) excused as Andorran lexicon — LanguageTool "
            "has no Andorran variant, so the glossary M2.03 requires is what it flags"
        )
    if report.by_rule:
        top = sorted(report.by_rule.items(), key=lambda item: (-item[1], item[0]))[:5]
        lines.append("  top rules: " + ", ".join(f"{rule}={count}" for rule, count in top))
    for example_id, found in report.worst[:5]:
        lines.append(f"    dropped {example_id} at {found:.1f} issues/1k chars")
    return "\n".join(lines)


def parse_matches(payload: object) -> list[Match]:
    """Read LanguageTool's ``/v2/check`` JSON response.

    Raises:
        ValueError: if the payload is not the documented shape. A service that changed or an
            error body returned as 200 would otherwise read as "no problems found", quietly
            turning the Catalan check into a no-op that reports success.
    """
    if not isinstance(payload, dict) or not isinstance(payload.get("matches"), list):
        raise ValueError(
            f"not a LanguageTool /v2/check response: expected a 'matches' list, got "
            f"{sorted(payload) if isinstance(payload, dict) else type(payload).__name__}"
        )
    matches: list[Match] = []
    for raw in payload["matches"]:
        if not isinstance(raw, dict):
            raise ValueError(f"match is not an object: {raw!r}")
        rule = raw.get("rule") if isinstance(raw.get("rule"), dict) else {}
        assert isinstance(rule, dict)
        category = rule.get("category") if isinstance(rule.get("category"), dict) else {}
        assert isinstance(category, dict)
        offset = raw.get("offset")
        matches.append(
            Match(
                rule_id=str(rule.get("id", "UNKNOWN")),
                category=str(category.get("id", "UNKNOWN")),
                message=str(raw.get("message", "")),
                text=_flagged_text(raw),
                offset=offset if isinstance(offset, int) else 0,
            )
        )
    return matches


_WHITESPACE = re.compile(r"\s+")


def _flagged_text(raw: dict[str, object]) -> str:
    """The exact text a match flags, from ``context.text`` and the match offsets."""
    context = raw.get("context")
    if not isinstance(context, dict):
        return ""
    text = context.get("text")
    offset = context.get("offset")
    length = context.get("length")
    if not isinstance(text, str) or not isinstance(offset, int) or not isinstance(length, int):
        return ""
    return _WHITESPACE.sub(" ", text[offset : offset + length])


def languagetool_service(
    endpoint: str = DEFAULT_ENDPOINT, *, timeout: float = 30.0
) -> GrammarService:
    """A live LanguageTool client (blocked-by-resource: needs the service reachable).

    ``requests`` is imported locally so the module and its tests need no network.
    """
    import requests

    @dataclass(frozen=True)
    class _HttpService:
        url: str

        def check(self, text: str, language: str = LANGUAGE) -> list[Match]:
            response = requests.post(
                self.url, data={"text": text, "language": language}, timeout=timeout
            )
            response.raise_for_status()
            return parse_matches(response.json())

    return _HttpService(endpoint)


def rule_histogram(matches: Iterable[Match]) -> dict[str, int]:
    """Count matches by rule id — which mistakes the generator actually makes."""
    counts: dict[str, int] = {}
    for match in matches:
        counts[match.rule_id] = counts.get(match.rule_id, 0) + 1
    return counts
