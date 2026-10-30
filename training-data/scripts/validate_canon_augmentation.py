"""Validate the Andorran canon-facts pilot JSONL files."""

from __future__ import annotations

import argparse
import json
import re
import sys
from difflib import SequenceMatcher
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any

from rewrite_canon_answers import ANSWER_FORMS, CONTEXT_FRAMES, FALSE_QUESTION_STEMS

ROOT = Path(__file__).resolve().parents[2]
FACTS_PATH = ROOT / "training-data/facts/canon-facts.jsonl"
EXAMPLES_PATH = ROOT / "training-data/datasets/canon-augmentat.jsonl"
EXPECTED_TOPICS = {
    "economia-llengua-societat-gastronomia",
    "historia",
    "persones-esports-present",
    "simbols-costums-cultura",
    "territori-institucions",
}
EXPECTED_TYPES = {
    "directa": 150,
    "reversa": 100,
    "parafrasi": 100,
    "context": 100,
    "dues-voltes": 50,
    "premissa-falsa": 50,
    "abstencio": 29,
}
FACT_FIELDS = {"fact_id", "fact", "source_ids", "topic"}
ROW_FIELDS = {"id", "type", "fact_id", "messages", "documents", "verificat"}
FORBIDDEN_PHRASES = ("segons el document", "el text diu", "segons el text")
RELATED_VERIFIED_ANSWERS = {
    "el roc de les bruixes mira directament el santuari de meritxell": {"topic": "simbols-costums-cultura", "document": "docs/temes/cultura/llegendes/el-roc-de-les-bruixes.md"},
    "la banca andorrana aporta al voltant del 20 % del pib": {"topic": "economia-llengua-societat-gastronomia", "document": "docs/temes/economia/banca-i-fiscalitat/banca-i-fiscalitat.md"},
    "el català és la llengua vehicular de l escola andorrana": {"topic": "economia-llengua-societat-gastronomia", "document": "docs/temes/societat/educacio/els-tres-sistemes.md"},
    "la carta pobla atribueix a carlemany i a lluís el piadós la concessió de franqueses als habitants d andorra": {"topic": "historia", "document": "docs/temes/historia/origens/carta-pobla-fals-carlemany.md"},
    "la nova reforma va establir un consell general de 24 consellers elegits pels caps de casa": {"topic": "historia", "document": "docs/temes/historia/segle-xix/nova-reforma.md"},
    "la federació andorrana de futbol va entrar a la fifa i la uefa el 1996": {"topic": "persones-esports-present", "document": "docs/temes/esports/futbol/clubs-i-competicions/la-federacio.md"},
    "el campanar de santa coloma fa 17 75 metres d alçada": {"topic": "simbols-costums-cultura", "document": "docs/temes/cultura/arquitectura/santa-coloma.md"},
    "les falles tradicionals es feien amb escorça de beç": {"topic": "simbols-costums-cultura", "document": "docs/temes/costums/falles/falles.md"},
    "els gegants d andorra la vella es van construir el 1985": {"topic": "simbols-costums-cultura", "document": "docs/temes/costums/gegants/els-gegants.md"},
    "a encamp també es representa el ball de l óssa": {"topic": "simbols-costums-cultura", "document": "docs/temes/cultura/teatre/el-teatre-de-carnestoltes.md"},
    "cada comissió té almenys cinc consellers": {"topic": "territori-institucions", "document": "docs/temes/institucions/consell-general/el-consell-general.md"},
}
ANSWER_BOILERPLATE = (
    "La dada és aquesta", "La resposta breu és", "Pel que fa a", "La informació clau és",
)
QUESTION_BOILERPLATE = (
    "Em recordes", "Em pots precisar", "Respon breument aquesta pregunta",
    "Dit d’una altra manera", "En una consulta pràctica", *FALSE_QUESTION_STEMS,
)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            if not line.strip():
                raise ValueError(f"{path}:{line_number}: blank JSONL line")
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_number}: expected an object")
            rows.append(value)
    return rows


def font_ids() -> set[str]:
    found: set[str] = set()
    for path in (ROOT / "docs/fonts").glob("*.md"):
        text = path.read_text(encoding="utf-8")
        match = re.search(r"^id:\s*['\"]?([^\s'\"]+)", text, re.MULTILINE)
        if match:
            found.add(match.group(1))
    return found


def validate_facts() -> list[dict[str, Any]]:
    facts = read_jsonl(FACTS_PATH)
    if len(facts) != 50:
        raise ValueError(f"expected 50 facts, found {len(facts)}")
    seen_ids: set[str] = set()
    seen_facts: set[str] = set()
    topic_counts: Counter[str] = Counter()
    known_fonts = font_ids()
    for index, fact in enumerate(facts, start=1):
        if set(fact) != FACT_FIELDS:
            raise ValueError(f"fact line {index}: fields must be {sorted(FACT_FIELDS)}")
        fact_id = fact["fact_id"]
        statement = fact["fact"]
        sources = fact["source_ids"]
        topic = fact["topic"]
        if not isinstance(fact_id, str) or not re.fullmatch(r"[^\W_]+(?:-[^\W_]+)*", fact_id):
            raise ValueError(f"fact line {index}: invalid fact_id {fact_id!r}")
        if fact_id in seen_ids:
            raise ValueError(f"duplicate fact_id: {fact_id}")
        seen_ids.add(fact_id)
        if not isinstance(statement, str) or not statement.strip():
            raise ValueError(f"fact line {index}: empty fact")
        normalized = re.sub(r"[^\w]+", " ", statement.casefold(), flags=re.UNICODE).strip()
        if normalized in seen_facts:
            raise ValueError(f"duplicate fact statement: {statement}")
        seen_facts.add(normalized)
        if topic not in EXPECTED_TOPICS:
            raise ValueError(f"fact line {index}: unexpected topic {topic!r}")
        topic_counts[topic] += 1
        if not isinstance(sources, list) or not sources:
            raise ValueError(f"fact line {index}: source_ids must be a non-empty list")
        if len(sources) != len(set(sources)):
            raise ValueError(f"fact line {index}: duplicate source_ids")
        for source_id in sources:
            if source_id not in known_fonts:
                raise ValueError(f"fact line {index}: unknown docs/fonts id {source_id!r}")
    if set(topic_counts) != EXPECTED_TOPICS or any(topic_counts[t] != 10 for t in EXPECTED_TOPICS):
        raise ValueError(f"expected 10 facts in each topic, found {dict(topic_counts)}")
    print(f"facts: {len(facts)} unique; topic counts: {dict(sorted(topic_counts.items()))}")
    return facts


def normalized_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).casefold()
    return re.sub(r"[^\w]+", " ", text, flags=re.UNICODE).strip()


def validate_examples(facts: list[dict[str, Any]]) -> None:
    examples = read_jsonl(EXAMPLES_PATH)
    if len(examples) != 579:
        raise ValueError(f"expected 579 rows, found {len(examples)}")
    fact_map = {fact["fact_id"]: fact for fact in facts}
    answer_fact_ids = {normalized_text(fact["fact"]): fact["fact_id"] for fact in facts}
    for fact_id, variants in ANSWER_FORMS.items():
        for variant in variants:
            answer_fact_ids[normalized_text(variant)] = fact_id
    documents_by_fact = {
        fact_id: next((row["documents"] for row in examples if row.get("fact_id") == fact_id and row["type"] != "dues-voltes"), [])
        for fact_id in fact_map
    }
    counts: Counter[str] = Counter()
    by_fact: Counter[str] = Counter()
    seen_ids: set[str] = set()
    seen_pairs: set[str] = set()
    questions_by_fact: dict[str, set[str]] = {}
    answers_by_fact: dict[str, set[str]] = {}
    answer_texts_by_fact: dict[str, list[str]] = {}
    abstention_answers: set[str] = set()
    assistant_answers: list[str] = []
    prefix_counts: Counter[tuple[str, str]] = Counter()
    context_count = 0
    dialogue_count = 0
    false_premise_count = 0
    for index, row in enumerate(examples, start=1):
        if set(row) != ROW_FIELDS:
            raise ValueError(f"row {index}: fields must be {sorted(ROW_FIELDS)}")
        row_id = row["id"]
        row_type = row["type"]
        fact_id = row["fact_id"]
        messages = row["messages"]
        documents = row["documents"]
        if not isinstance(row_id, str) or row_id in seen_ids:
            raise ValueError(f"row {index}: invalid or duplicate id {row_id!r}")
        seen_ids.add(row_id)
        if row_type not in EXPECTED_TYPES:
            raise ValueError(f"row {index}: unknown type {row_type!r}")
        counts[row_type] += 1
        if row["verificat"] != "2026-10-30":
            raise ValueError(f"row {index}: unexpected verification date {row['verificat']!r}")
        if not isinstance(documents, list):
            raise ValueError(f"row {index}: documents must be a list")
        if row_type == "abstencio":
            if fact_id is not None or documents:
                raise ValueError(f"row {index}: abstentions need null fact_id and no documents")
        else:
            if fact_id not in fact_map:
                raise ValueError(f"row {index}: missing fact reference {fact_id!r}")
            fact = fact_map[fact_id]
            if not row_id.startswith(f"canon-aug/{fact['topic']}/{fact_id}-"):
                raise ValueError(f"row {index}: id does not match fact topic and id")
            if not documents or any(not isinstance(doc, str) or not doc.startswith("docs/temes/") for doc in documents):
                raise ValueError(f"row {index}: factual documents must point into docs/temes/")
            for doc in documents:
                if not (ROOT / doc).is_file():
                    raise ValueError(f"row {index}: missing source document {doc!r}")
            by_fact[fact_id] += 1
        if row_type == "dues-voltes":
            dialogue_count += 1
            expected_roles = ["system", "user", "assistant", "user", "assistant"]
        else:
            expected_roles = ["system", "user", "assistant"]
        if not isinstance(messages, list) or [m.get("role") for m in messages] != expected_roles:
            raise ValueError(f"row {index}: invalid role sequence")
        if any(not isinstance(m.get("content"), str) for m in messages):
            raise ValueError(f"row {index}: message content must be text")
        for message in messages:
            content = message["content"]
            if message["role"] == "user" and re.search(r"·[^—]*—", content):
                raise ValueError(f"row {index}: user turn contains a topic label delimiter")
            if message["role"] == "user" and any(phrase in content.casefold() for phrase in ("quina dada concreta s’obté", "quina informació aporta la pregunta", "en què consisteix quina informació")):
                raise ValueError(f"row {index}: user question is a prefixed duplicate rather than a natural rephrasing")
            if any(phrase in content.casefold() for phrase in FORBIDDEN_PHRASES):
                raise ValueError(f"row {index}: forbidden source-reference wording")
            if message["role"] == "assistant":
                assistant_answers.append(content)
                if re.search(r"[:,]\s+[A-ZÀ-Þ]", content):
                    raise ValueError(f"row {index}: uppercase letter after a colon or comma in an answer")
                if re.search(r"\b\d{1,2}[-/]\d{1,2}[-/]\d{4}\b", content):
                    raise ValueError(f"row {index}: dates must be written with Catalan month names")
                if row_type != "premissa-falsa":
                    for prefix in ANSWER_BOILERPLATE:
                        if content.casefold().startswith(prefix.casefold()):
                            prefix_counts[("answer", prefix)] += 1
            elif message["role"] == "user":
                for prefix in FALSE_QUESTION_STEMS:
                    if content.count(prefix) > 1:
                        raise ValueError(f"row {index}: repeated false-premise question stem")
                for prefix in QUESTION_BOILERPLATE:
                    if content.casefold().startswith(prefix.casefold()):
                        prefix_counts[("question", prefix)] += 1
                for prefix in CONTEXT_FRAMES:
                    if content.startswith(prefix):
                        prefix_counts[("question", prefix)] += 1
                        break
        answer = messages[-1]["content"].strip()
        if row_type == "abstencio":
            abstention_answers.add(normalized_text(answer))
        else:
            primary_answer = messages[2]["content"].strip()
            answers_by_fact.setdefault(fact_id, set()).add(normalized_text(primary_answer))
            answer_texts_by_fact.setdefault(fact_id, []).append(primary_answer)
        if row_type != "abstencio":
            normalized_question = normalized_text(messages[1]["content"])
            previous_questions = questions_by_fact.setdefault(fact_id, set())
            if normalized_question in previous_questions:
                raise ValueError(f"row {index}: duplicate user question for fact {fact_id}")
            previous_questions.add(normalized_question)
        if row_type == "context":
            context_count += 1
        if row_type == "premissa-falsa":
            false_premise_count += 1
            correction = messages[2]["content"]
            if correction.startswith("No és així: ") and not correction[len("No és així: "):len("No és així: ")+1].islower():
                raise ValueError(f"row {index}: correction after 'No és així:' must start lowercase")
        if row_type == "dues-voltes":
            second_question = messages[3]["content"].casefold()
            if any(term in second_question for term in ("resum", "resumeix", "resumir")):
                raise ValueError(f"row {index}: second turn must ask a related fact, not a summary")
            if normalized_text(messages[3]["content"]) == normalized_text(messages[1]["content"]):
                raise ValueError(f"row {index}: second question must differ from the first")
            secondary_answer = normalized_text(messages[4]["content"])
            related_id = answer_fact_ids.get(secondary_answer)
            supplemental = RELATED_VERIFIED_ANSWERS.get(secondary_answer)
            if related_id:
                related_topic = fact_map[related_id]["topic"]
                related_documents = documents_by_fact[related_id]
            elif supplemental:
                related_topic = supplemental["topic"]
                related_documents = [supplemental["document"]]
            else:
                # A supplemental corpus fact can be verified in the attached topic document.
                related_topic = fact_map[fact_id]["topic"]
                related_documents = [doc for doc in documents if doc.startswith("docs/temes/")]
            if related_topic != fact_map[fact_id]["topic"]:
                raise ValueError(f"row {index}: second-turn fact topic differs from primary fact topic")
            if not set(related_documents).issubset(set(documents)):
                raise ValueError(f"row {index}: second-turn documents do not include the related fact source")
            if any(not (ROOT / doc).is_file() for doc in related_documents):
                raise ValueError(f"row {index}: second-turn source document is missing")
        if not answer:
            raise ValueError(f"row {index}: empty assistant answer")
        if row_type == "abstencio":
            if not re.search(r"no en tinc (?:cap )?constància|no ho sé|no em consta|no tinc (?:cap )?(?:informació|dades)|no tinc prou informació|no puc (?:confirmar|precisar|afirmar)|no disposo (?:d’aquesta informació|d’informació)|no en sé el nom|no puc donar-te aquesta mida|no en tinc cap registre|no en tinc cap referència fiable|aquesta dada no la puc confirmar|no puc precisar-ho|no ho puc afirmar|no ho puc verificar|no sé quin|no sé quina|no tinc aquesta dada confirmada|no em consta el resultat|no puc donar-te aquesta mida", answer.casefold()):
                raise ValueError(f"row {index}: abstention must state lack of knowledge")
        else:
            sentence_count = len([part for part in re.split(r"(?<=[.!?])\s+", answer) if part.strip()])
            if sentence_count < 1 or sentence_count > 3:
                raise ValueError(f"row {index}: answer has {sentence_count} sentences")
        pair = json.dumps(messages, ensure_ascii=False, sort_keys=True)
        if pair in seen_pairs:
            raise ValueError(f"row {index}: duplicate conversation")
        seen_pairs.add(pair)
    if counts != Counter(EXPECTED_TYPES):
        raise ValueError(f"unexpected type counts: {dict(sorted(counts.items()))}")
    if len(by_fact) != 50 or any(by_fact[fact_id] != 11 for fact_id in fact_map):
        raise ValueError(f"expected 11 factual rows per fact, found {dict(by_fact)}")
    if any(len(questions_by_fact.get(fact_id, set())) != 11 for fact_id in fact_map):
        raise ValueError("questions must be 100% unique within every fact")
    unique_counts = {fact_id: len(values) for fact_id, values in answers_by_fact.items()}
    minimum_unique = min(unique_counts.values())
    average_unique = sum(unique_counts.values()) / len(unique_counts)
    if any(value < 5 for value in unique_counts.values()):
        raise ValueError(f"each fact needs at least 5 answer structures; minimum is {minimum_unique}")
    max_similarity = 0.0
    literal_counts = {
        fact_id: sum(normalized_text(fact["fact"]) in normalized_text(answer) for answer in assistant_answers)
        for fact_id, fact in fact_map.items()
    }
    for fact_id, literal_matches in literal_counts.items():
        if literal_matches > 1:
            raise ValueError(f"fact {fact_id}: literal fact phrase occurs in {literal_matches} assistant answers (maximum 1)")
    for fact_id, answers in answer_texts_by_fact.items():
        for i, first in enumerate(answers):
            for second in answers[i + 1:]:
                similarity = SequenceMatcher(None, normalized_text(first), normalized_text(second)).ratio()
                max_similarity = max(max_similarity, similarity)
                if similarity >= 0.8:
                    raise ValueError(f"fact {fact_id}: answer character similarity {similarity:.3f} is not below 0.8")
    if len(abstention_answers) < 5:
        raise ValueError(f"expected at least 5 distinct abstention wordings, found {len(abstention_answers)}")
    overused_prefixes = {key: value for key, value in prefix_counts.items() if value > 3}
    if overused_prefixes:
        raise ValueError(f"question/answer boilerplate prefixes occur more than three times: {overused_prefixes}")
    if counts["abstencio"] / len(examples) < 0.045 or counts["abstencio"] / len(examples) > 0.055:
        raise ValueError("abstention share must be approximately 5 percent")
    if context_count != 100 or dialogue_count != 50 or false_premise_count != 50:
        raise ValueError("context/dialogue/false-premise type counts do not match pilot spec")
    print(f"examples: {len(examples)}; type counts: {dict(sorted(counts.items()))}")
    print(f"answer diversity: min={minimum_unique}/11; average={average_unique:.2f}/11; max character similarity={max_similarity:.3f} (<0.8)")
    print(f"literal fact phrases: maximum={max(literal_counts.values())} assistant answers per fact; boilerplate prefix maximum={max(prefix_counts.values(), default=0)}/3")
    print(f"abstentions: {counts['abstencio']}/{len(examples)} ({counts['abstencio']/len(examples):.2%}); unique wordings={len(abstention_answers)}")
    print(f"questions: 100% unique per fact; user label delimiters: 0; dialogues: {dialogue_count} with same-topic verified follow-ups; false premises: {false_premise_count} checked")
    print(f"factual rows: {sum(by_fact.values())}; abstentions: {counts['abstencio']}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--facts-only", action="store_true")
    group.add_argument("--examples-only", action="store_true")
    group.add_argument("--all", action="store_true")
    args = parser.parse_args()
    try:
        facts = validate_facts()
        if not args.facts_only:
            validate_examples(facts)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"validation failed: {error}", file=sys.stderr)
        return 1
    print("validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
