"""Language filter — PLAN M1.08, step 2.

The corpus must be Catalan. Andorran sources leak Spanish, French, Portuguese and English:
institutional sites publish multilingual pages, press quotes foreign sources, and scraped
navigation drags in language switchers. A document in the wrong language poisons both the
RAG index and the grounding of the synthetic dataset.

Detection is by **function-word profile**. The closed-class words of a language (articles,
prepositions, conjunctions, auxiliaries) are the most frequent tokens in any prose, so a
few hundred characters is enough to score them, and — crucially — they are the words that
differ between neighbouring Romance languages: *amb*/*con*, *però*/*pero*, *això*/*esto*.

The profiles below are written **generously and with deliberate overlap**, then
:data:`_DISCRIMINATIVE` keeps only the words unique to a single language. That inversion is
the whole trick: hand-curating non-overlapping lists is exactly the kind of job a human gets
subtly wrong, and one shared high-frequency word (Catalan *del*, *les* and *que* are also
Spanish or French) is enough to make Catalan prose score as Spanish. Deriving the
discriminative set by construction means a mistake in the lists can only cost sensitivity,
never correctness.

Two Catalan-only orthographic signals reinforce the word profile: apostrophed elisions
(*l'aigua*, *d'Andorra*, *s'ha*) and the *ela geminada* (``l·l``).

:func:`detect_language` has the shape of a model call and the pipeline takes it as an
**injected seam** — if the M1.10 coverage report shows misclassification, a statistical
detector can replace it without the pipeline changing.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

#: High-frequency function words per language. Overlap between these lists is intentional
#: and is removed below; the only requirement is that each list be *complete enough* that a
#: word shared with Catalan is actually listed under Catalan too.
_RAW_PROFILES: dict[str, str] = {
    "ca": """
        de la el els les un una del dels al als en amb per però com més no es se és són ha
        han hi ho li seu seva seus seves aquest aquesta aquests aquestes això aquell aquella
        què qui quan on també molt tot tota tots totes ja sense sobre sota entre cada altres
        altre altra després abans avui demà ahir aquí allà fins dins mentre doncs així
        perquè nosaltres vosaltres ells elles era eren hem heu vers malgrat durant segons
        qualsevol quelcom tanmateix que
    """,
    "es": """
        de la el los las un una del al en con por para pero como más no se es son ha han hay
        su sus este esta estos estas esto aquel aquella qué quien cuando donde también muy
        todo toda todos todas ya sin sobre bajo entre cada otros otro otra después antes hoy
        mañana ayer aquí allí hasta desde mientras entonces así porque nosotros vosotros
        ellos ellas era eran hemos según durante hacia aunque algo cualquier que
    """,
    "fr": """
        de la le les des du un une au aux en avec par pour mais comme plus ne pas se est
        sont ont il elle ils elles ce cette cet ces qui quand où aussi très tout toute tous
        toutes déjà sans sur sous entre chaque autres autre après avant demain hier ici là
        jusqu depuis pendant alors ainsi parce nous vous était étaient avons selon vers bien
        quelque dans son sa ses leur leurs on que
    """,
    "pt": """
        de da do das dos o os as um uma ao aos em com por para mas como mais não se é são há
        têm temos seu sua seus suas este esta estes estas isto aquele aquela quem quando onde
        também muito todo toda todos todas já sem sobre sob entre cada outros outro outra
        depois antes hoje amanhã ontem aqui ali até desde enquanto então assim porque nós
        vocês eles elas era eram segundo durante embora algo qualquer pelo pela que
    """,
    "en": """
        the of and to in that is are was were be been being have has had with for from by on
        at as this these those which who when where how also more very there not without
        about under between each other others after before today tomorrow yesterday here all
        any according during towards although something would could should his her their our
        your they them it but or if then thus
    """,
}


def _words(blob: str) -> frozenset[str]:
    # Single characters are excluded: "i", "a", "o" and "e" are function words in several of
    # these languages at once and also appear as list bullets and roman numerals.
    return frozenset(word for word in blob.split() if len(word) > 1)


_ALL_PROFILES: dict[str, frozenset[str]] = {
    lang: _words(blob) for lang, blob in _RAW_PROFILES.items()
}

#: Words unique to one language — everything shared is dropped, by construction.
_DISCRIMINATIVE: dict[str, frozenset[str]] = {
    lang: frozenset(
        word
        for word in words
        if not any(word in other for name, other in _ALL_PROFILES.items() if name != lang)
    )
    for lang, words in _ALL_PROFILES.items()
}

_WORD = re.compile(r"[^\W\d_]+", re.UNICODE)

#: Apostrophed elision — "l'aigua", "d'Andorra", "s'ha". Absent from Spanish.
_ELISION = re.compile(r"\b[ldsmntLDSMNT]['\u2019]\s*[^\W\d_]", re.UNICODE)
#: Ela geminada — unique to Catalan orthography.
_ELA_GEMINADA = re.compile(r"l·l", re.IGNORECASE)


@dataclass(frozen=True)
class LanguageVerdict:
    """The detected language and how clearly it won.

    Attributes:
        language: best-scoring language code, or ``"und"`` when there is nothing to score.
        confidence: the winner's share of all profile hits, 0.0-1.0.
        runner_up: the second-best language, or ``"und"`` when nothing else scored.
        runner_up_share: the runner-up's share of the hits — the *amount of foreign signal*
            in the text, which is what distinguishes a Catalan article from a page that is
            half Catalan and half Spanish. Both can name Catalan the winner; only this tells
            them apart, because a mixture tilts towards whichever language has the richer
            profile rather than towards neither.
        margin: ``confidence - runner_up_share``, kept because it is the conventional way to
            report a detector's decisiveness.
    """

    language: str
    confidence: float
    runner_up: str = "und"
    runner_up_share: float = 0.0

    @property
    def margin(self) -> float:
        """How far ahead of the runner-up the winner is."""
        return self.confidence - self.runner_up_share


def _tokens(text: str) -> list[str]:
    folded = unicodedata.normalize("NFC", text.lower())
    return [token for token in _WORD.findall(folded) if len(token) > 1]


def detect_language(text: str) -> LanguageVerdict:
    """Score ``text`` against each function-word profile and return the winner."""
    tokens = _tokens(text)
    if not tokens:
        return LanguageVerdict("und", 0.0)

    scores = {
        lang: sum(token in profile for token in tokens) for lang, profile in _DISCRIMINATIVE.items()
    }

    # Catalan-only orthography, weighted like a handful of function words. Capped so that one
    # apostrophe-heavy line cannot outvote the word profile.
    scores["ca"] += min(len(_ELISION.findall(text)), 10) + 3 * min(
        len(_ELA_GEMINADA.findall(text)), 5
    )

    total = sum(scores.values())
    if total == 0:
        return LanguageVerdict("und", 0.0)

    ranked = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    (best, best_score), (second, second_score) = ranked[0], ranked[1]
    return LanguageVerdict(
        language=best,
        confidence=best_score / total,
        runner_up=second if second_score else "und",
        runner_up_share=second_score / total,
    )


def is_catalan(text: str, *, min_confidence: float = 0.6, max_foreign_share: float = 0.25) -> bool:
    """True if ``text`` is Catalan clearly enough to enter the corpus.

    Catalan must win *and* the runner-up must stay small. The second condition is the one
    that matters in practice: a page that is half Catalan and half Spanish still names
    Catalan the winner — a mixture tilts towards whichever language has the richer profile,
    not towards neither — so only the size of the foreign signal rejects it. Mixed-language
    documents are worth rejecting because they pollute both the RAG index and the grounding.
    """
    verdict = detect_language(text)
    return (
        verdict.language == "ca"
        and verdict.confidence >= min_confidence
        and verdict.runner_up_share <= max_foreign_share
    )
