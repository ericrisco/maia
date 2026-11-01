"""Validate the Andorran canon-facts augmentation JSONL files."""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import Counter
from datetime import date
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

from rewrite_canon_answers import CONTEXT_FRAMES, FALSE_QUESTION_STEMS

ROOT = Path(__file__).resolve().parents[2]
FACTS_PATH = ROOT / "training-data/facts/canon-facts.jsonl"
EXAMPLES_PATH = ROOT / "training-data/datasets/canon-augmentat.jsonl"
CONTRAST_GROUPS_PATH = ROOT / "training-data/facts/canon-contrast-groups.jsonl"
PROBE_PATH = ROOT / "training-data/facts/canon-facts-probe.jsonl"
BASIC_DATASET_PATH = ROOT / "training-data/datasets/canon-basic.jsonl"
EXPECTED_TOPICS = {
    "economia-llengua-societat-gastronomia",
    "historia",
    "persones-esports-present",
    "simbols-costums-cultura",
    "territori-institucions",
}
FACT_FIELDS = {"fact_id", "fact", "source_ids", "topic"}
ROW_FIELDS = {"id", "type", "fact_id", "messages", "documents", "verificat"}
FORBIDDEN_PHRASES = ("segons el document", "el text diu", "segons el text")
ANSWER_BOILERPLATE = (
    "La dada és aquesta",
    "La resposta breu és",
    "Pel que fa a",
    "La informació clau és",
)
QUESTION_BOILERPLATE = (
    "Em recordes",
    "Em pots precisar",
    "Respon breument aquesta pregunta",
    "Dit d'una altra manera",
    "En una consulta pràctica",
    *FALSE_QUESTION_STEMS,
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


def known_source_ids() -> set[str]:
    """Accept thematic source IDs and verified source-row IDs from canon-basic."""
    found = font_ids()
    for row in read_jsonl(BASIC_DATASET_PATH):
        source_id = row.get("id")
        if isinstance(source_id, str):
            found.add(source_id)
    return found


def validate_facts(scope: str | None = None) -> list[dict[str, Any]]:
    facts = read_jsonl(FACTS_PATH)
    if not facts:
        raise ValueError("facts file must not be empty")
    if scope is not None and scope not in EXPECTED_TOPICS:
        raise ValueError(f"unknown topic {scope!r}; expected one of {sorted(EXPECTED_TOPICS)}")
    seen_ids: set[str] = set()
    seen_facts: set[str] = set()
    topic_counts: Counter[str] = Counter()
    known_sources = known_source_ids()
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
            if source_id not in known_sources:
                raise ValueError(f"fact line {index}: unknown allowed source id {source_id!r}")
    if scope is None and set(topic_counts) != EXPECTED_TOPICS:
        raise ValueError(f"all five topics must be represented, found {dict(topic_counts)}")
    if scope is not None and topic_counts[scope] == 0:
        raise ValueError(f"topic {scope!r} has no facts")
    print(f"facts: {len(facts)} unique; topic counts: {dict(sorted(topic_counts.items()))}")
    return facts


def normalized_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).casefold()
    return re.sub(r"[^\w]+", " ", text, flags=re.UNICODE).strip()


TOPIC_STOPWORDS = {
    "a",
    "abans",
    "al",
    "als",
    "amb",
    "andorra",
    "aquell",
    "aquesta",
    "aquestes",
    "aquests",
    "aquí",
    "com",
    "contra",
    "de",
    "del",
    "dels",
    "des",
    "després",
    "durant",
    "el",
    "els",
    "en",
    "entre",
    "era",
    "eren",
    "és",
    "esta",
    "fan",
    "fins",
    "foi",
    "ha",
    "han",
    "has",
    "hi",
    "i",
    "la",
    "les",
    "li",
    "llavors",
    "lo",
    "més",
    "molts",
    "na",
    "no",
    "o",
    "on",
    "per",
    "perquè",
    "però",
    "quan",
    "que",
    "quin",
    "quina",
    "quines",
    "quins",
    "qui",
    "s",
    "se",
    "segons",
    "ser",
    "seu",
    "seva",
    "sobre",
    "son",
    "són",
    "sota",
    "tant",
    "tenia",
    "tenien",
    "un",
    "una",
    "unes",
    "uns",
    "va",
    "van",
    "veure",
    "via",
    "país",
    "païs",
    "andorrà",
    "andorrana",
    "andorrans",
    "andorranes",
}


def topic_terms(text: str) -> set[str]:
    return {
        token
        for token in normalized_text(text).split()
        if len(token) >= 3 and token not in TOPIC_STOPWORDS and not token.isdigit()
    }


def row_user_question(row: dict[str, Any]) -> str:
    messages = row.get("messages", [])
    if not isinstance(messages, list):
        return ""
    return next(
        (message.get("content", "") for message in messages if message.get("role") == "user"),
        "",
    )


def row_answer(row: dict[str, Any]) -> str:
    messages = row.get("messages", [])
    if not isinstance(messages, list):
        return ""
    return next(
        (
            message.get("content", "")
            for message in reversed(messages)
            if message.get("role") == "assistant"
        ),
        "",
    )


def row_fact_ids(row: dict[str, Any]) -> list[str]:
    values = row.get("contrast_fact_ids")
    if isinstance(values, list) and values:
        fact_ids = [value for value in values if isinstance(value, str)]
    else:
        fact_id = row.get("fact_id")
        fact_ids = [fact_id] if isinstance(fact_id, str) else []
    fact_id = row.get("fact_id")
    related_fact_id = row.get("related_fact_id")
    if isinstance(related_fact_id, str) and related_fact_id not in fact_ids:
        fact_ids.append(related_fact_id)
    if isinstance(fact_id, str) and fact_id not in fact_ids:
        fact_ids.insert(0, fact_id)
    return fact_ids


def validate_question_topics(
    facts: list[dict[str, Any]],
    examples: list[dict[str, Any]],
    groups: list[dict[str, Any]],
    scope: str | None = None,
) -> int:
    """Require every factual question to repeat a specific subject from its fact or group."""
    fact_map = {fact["fact_id"]: fact for fact in facts}
    group_map = {group.get("group_id"): group for group in groups}
    checked = 0
    for index, row in enumerate(examples, start=1):
        messages = row.get("messages", [])
        questions = [
            message.get("content", "")
            for message in messages
            if isinstance(message, dict) and message.get("role") == "user"
        ]
        if not questions:
            raise ValueError(f"row {index}: missing user question")
        ids = row_fact_ids(row)
        row_topic = fact_map.get(ids[0], {}).get("topic") if ids else None
        if not row_topic and row.get("group_id") in group_map:
            row_topic = group_map[row["group_id"]].get("topic")
        if scope and row_topic != scope:
            continue
        if row.get("type") == "abstencio":
            anchor_id = row.get("anchor_fact_id")
            ids = [anchor_id] if isinstance(anchor_id, str) else []
            if not ids:
                if scope:
                    # Legacy pilot abstentions have no fact anchor; revise them with the topic lot.
                    continue
                # Pilot abstentions predate anchor_fact_id; find an explicit subject lexically.
                question_terms = set.union(*(topic_terms(question) for question in questions))
                candidates = set.union(*(topic_terms(fact["fact"]) for fact in facts))
                candidates.difference_update({"andorra", "país", "andorrà", "andorrana"})
                if not question_terms.intersection(candidates):
                    raise ValueError(f"row {index}: question does not identify its topic or entity")
                checked += len(questions)
                continue
        if not ids or any(fact_id not in fact_map for fact_id in ids):
            raise ValueError(
                f"row {index}: cannot identify the factual topic without valid fact IDs"
            )
        primary_ids = row.get("contrast_fact_ids")
        if not isinstance(primary_ids, list) or not primary_ids:
            primary_ids = [ids[0]]
        for question_index, question in enumerate(questions):
            question_ids = primary_ids
            if question_index > 0:
                related_id = row.get("related_fact_id")
                if isinstance(related_id, str):
                    question_ids = [related_id]
            candidates: set[str] = set()
            for fact_id in question_ids:
                if fact_id in fact_map:
                    candidates.update(topic_terms(fact_map[fact_id]["fact"]))
            group = group_map.get(row.get("group_id"))
            if group:
                candidates.update(topic_terms(str(group.get("entity_class", ""))))
                candidates.update(topic_terms(str(group.get("data_type", ""))))
            if question_index > 0 and not row.get("related_fact_id"):
                assistant_answers = [
                    message.get("content", "")
                    for message in messages
                    if isinstance(message, dict) and message.get("role") == "assistant"
                ]
                if question_index < len(assistant_answers):
                    candidates.update(topic_terms(assistant_answers[question_index]))
            candidates.difference_update({"andorra", "país", "andorrà", "andorrana"})
            if not topic_terms(question).intersection(candidates):
                raise ValueError(f"row {index}: question does not identify its topic or entity")
            checked += 1
    return checked


def validate_contrast_coverage(
    facts: list[dict[str, Any]],
    groups: list[dict[str, Any]],
    examples: list[dict[str, Any]],
    probe: list[dict[str, Any]],
) -> dict[str, int]:
    """Check contrast-group members, all required example patterns, names, and probe coverage."""
    fact_ids = {fact["fact_id"] for fact in facts}
    seen_groups: set[str] = set()
    by_group: dict[str, list[dict[str, Any]]] = {}
    for row in examples:
        group_id = row.get("group_id")
        if isinstance(group_id, str):
            by_group.setdefault(group_id, []).append(row)
    for index, group in enumerate(groups, start=1):
        group_id = group.get("group_id")
        members = group.get("members")
        if not isinstance(group_id, str) or not group_id or group_id in seen_groups:
            raise ValueError(f"contrast group {index}: missing or duplicate group_id")
        seen_groups.add(group_id)
        if group.get("topic") not in EXPECTED_TOPICS:
            raise ValueError(f"contrast group {group_id}: invalid topic")
        if not isinstance(group.get("entity_class"), str) or not group["entity_class"].strip():
            raise ValueError(f"contrast group {group_id}: entity_class must be non-empty text")
        if not isinstance(group.get("data_type"), str) or not group["data_type"].strip():
            raise ValueError(f"contrast group {group_id}: data_type must be non-empty text")
        if not isinstance(members, list) or len(members) < 2:
            raise ValueError(f"contrast group {group_id}: needs at least two members")
        member_ids = {member.get("fact_id") for member in members if isinstance(member, dict)}
        if (
            len(member_ids) != len(members)
            or len(member_ids) < 2
            or not member_ids.issubset(fact_ids)
            or any(
                not isinstance(member, dict)
                or not isinstance(member.get("entity_name"), str)
                or not member["entity_name"].strip()
                for member in members
            )
        ):
            raise ValueError(f"contrast group {group_id}: references missing or duplicate facts")
        if any(fact_id not in fact_ids or fact_id is None for fact_id in member_ids):
            raise ValueError(f"contrast group {group_id}: references missing or duplicate facts")
        if any(
            fact_id not in {fact["fact_id"] for fact in facts if fact["topic"] == group["topic"]}
            for fact_id in member_ids
        ):
            raise ValueError(f"contrast group {group_id}: members must belong to the group's topic")
        group_examples = group.get("examples")
        if not isinstance(group_examples, list) or len(group_examples) < 3:
            raise ValueError(f"contrast group {group_id}: needs at least 3 examples")
        if len(group_examples) > 6 and len(members) <= 6:
            raise ValueError(
                f"contrast group {group_id}: groups of up to 6 members may have at most 6 examples"
            )
        kinds = {example.get("kind") for example in group_examples if isinstance(example, dict)}
        required = {"successio", "discriminacio", "premissa-falsa"}
        if not required.issubset(kinds):
            raise ValueError(f"contrast group {group_id}: missing contrast patterns")
        rows = by_group.get(group_id, [])
        if len(rows) != len(group_examples):
            raise ValueError(
                f"contrast group {group_id}: group file and training row counts differ"
            )
        row_kinds = {row.get("contrast_kind") for row in rows}
        if not required.issubset(row_kinds):
            raise ValueError(f"contrast group {group_id}: training rows miss contrast patterns")
        row_by_kind: dict[str, list[dict[str, Any]]] = {}
        for row in rows:
            row_by_kind.setdefault(str(row.get("contrast_kind")), []).append(row)
        for group_example in group_examples:
            if not isinstance(group_example, dict):
                raise ValueError(f"contrast group {group_id}: examples must be objects")
            kind = group_example.get("kind")
            matching = row_by_kind.get(str(kind), [])
            if not matching:
                raise ValueError(f"contrast group {group_id}: missing training row for {kind!r}")
            question = group_example.get("question")
            answer = group_example.get("answer")
            if (
                isinstance(question, str)
                and isinstance(answer, str)
                and not any(
                    normalized_text(row_user_question(row)) == normalized_text(question)
                    and normalized_text(row_answer(row)) == normalized_text(answer)
                    and set(row_fact_ids(row)) == set(group_example.get("fact_ids", []))
                    for row in matching
                )
            ):
                raise ValueError(
                    f"contrast group {group_id}: group example does not match its training row"
                )
        for row in rows:
            row_members = set(row_fact_ids(row))
            if not row_members.issubset(member_ids) or row.get("fact_id") not in row_members:
                raise ValueError(
                    f"contrast group {group_id}: training row references unrelated facts"
                )
            answer = normalized_text(row_answer(row))
            entities = {
                member.get("entity_name")
                for member in members
                if isinstance(member, dict) and member.get("fact_id") in row_members
            }
            if any(
                not isinstance(entity, str) or normalized_text(entity) not in answer
                for entity in entities
            ):
                raise ValueError(
                    f"contrast group {group_id}: answer omits a member's full entity name"
                )
        group_probes = [item for item in probe if item.get("fact_id") in member_ids]
        probe_count = len({normalized_text(item.get("question", "")) for item in group_probes})
        if probe_count < 2:
            raise ValueError(f"contrast group {group_id}: needs at least 2 probe questions")
    return {"groups": len(groups), "contrast_rows": sum(len(rows) for rows in by_group.values())}


def validate_probe_separation(
    probe: list[dict[str, Any]],
    examples: list[dict[str, Any]],
    facts: list[dict[str, Any]] | None = None,
    scope: str | None = None,
    dataset_questions: list[str] | None = None,
) -> float:
    """Require probe questions to be well-formed and dissimilar to every training question."""
    train_questions = [
        message.get("content", "")
        for row in examples
        for message in row.get("messages", [])
        if message.get("role") == "user" and isinstance(message.get("content"), str)
    ]
    train_questions.extend(
        question for question in dataset_questions or [] if isinstance(question, str)
    )
    seen: set[str] = set()
    max_similarity = 0.0
    fact_map = {fact["fact_id"]: fact for fact in facts or []}
    for index, item in enumerate(probe, start=1):
        if set(item) != {"fact_id", "question", "expect"}:
            raise ValueError(f"probe row {index}: fields must be fact_id, question, expect")
        if (
            not isinstance(item["fact_id"], str)
            or not isinstance(item["question"], str)
            or not item["question"].strip()
        ):
            raise ValueError(f"probe row {index}: fact_id and question must be non-empty strings")
        if scope and fact_map.get(item["fact_id"], {}).get("topic") != scope:
            continue
        expectations = item["expect"]
        if (
            not isinstance(expectations, list)
            or not expectations
            or any(
                not isinstance(group, list)
                or not group
                or any(not isinstance(value, str) or not value.strip() for value in group)
                for group in expectations
            )
        ):
            raise ValueError(
                f"probe row {index}: expect must be a list of non-empty string alternatives"
            )
        normalized = normalized_text(item["question"])
        if normalized in seen:
            raise ValueError(f"probe row {index}: duplicate probe question")
        seen.add(normalized)
        for training_question in train_questions:
            similarity = SequenceMatcher(
                None, normalized, normalized_text(training_question)
            ).ratio()
            max_similarity = max(max_similarity, similarity)
            if similarity >= 0.8:
                raise ValueError(
                    f"probe question similarity {similarity:.3f} is not below 0.8: "
                    f"{item['question']!r} is too close to {training_question!r}"
                )
    return max_similarity


def validate_examples(facts: list[dict[str, Any]], scope: str | None = None) -> dict[str, Any]:
    """Validate augmentation, contrast coverage, and independent-probe separation."""
    examples = read_jsonl(EXAMPLES_PATH)
    groups = read_jsonl(CONTRAST_GROUPS_PATH)
    probe = read_jsonl(PROBE_PATH)
    fact_map = {fact["fact_id"]: fact for fact in facts}
    group_map = {group.get("group_id"): group for group in groups}
    base_types = {"directa", "reversa", "parafrasi", "context", "dues-voltes", "premissa-falsa"}
    contrast_types = {"contrast-successio", "contrast-discriminacio", "premissa-falsa"}
    allowed_fields = ROW_FIELDS | {
        "group_id",
        "contrast_kind",
        "contrast_fact_ids",
        "related_fact_id",
        "anchor_fact_id",
    }
    seen_ids: set[str] = set()
    seen_pairs: set[str] = set()
    counts: Counter[str] = Counter()
    base_by_fact: Counter[str] = Counter()
    questions_by_fact: dict[str, set[str]] = {}
    answer_texts_by_fact: dict[str, list[str]] = {}
    unique_answers_by_fact: dict[str, set[str]] = {}
    prefix_counts: Counter[tuple[str, str]] = Counter()
    abstention_answers: set[str] = set()
    for index, row in enumerate(examples, start=1):
        if not set(row).issubset(allowed_fields) or not ROW_FIELDS.issubset(row):
            raise ValueError(f"row {index}: unexpected or missing fields")
        row_id = row["id"]
        row_type = row["type"]
        fact_id = row["fact_id"]
        messages = row["messages"]
        documents = row["documents"]
        if not isinstance(row_id, str) or row_id in seen_ids:
            raise ValueError(f"row {index}: invalid or duplicate id {row_id!r}")
        seen_ids.add(row_id)
        if not isinstance(row_type, str) or row_type not in base_types | contrast_types | {
            "abstencio"
        }:
            raise ValueError(f"row {index}: unknown type {row_type!r}")
        counts[row_type] += 1
        try:
            date.fromisoformat(row["verificat"])
        except (TypeError, ValueError) as error:
            raise ValueError(f"row {index}: verificat must be an ISO date") from error
        if not isinstance(messages, list) or any(
            not isinstance(message, dict) for message in messages
        ):
            raise ValueError(f"row {index}: messages must be an array of objects")
        expected_roles = (
            ["system", "user", "assistant", "user", "assistant"]
            if row_type == "dues-voltes"
            else ["system", "user", "assistant"]
        )
        if [message.get("role") for message in messages] != expected_roles:
            raise ValueError(f"row {index}: invalid role sequence")
        if any(not isinstance(message.get("content"), str) for message in messages):
            raise ValueError(f"row {index}: message content must be text")
        if not isinstance(documents, list):
            raise ValueError(f"row {index}: documents must be a list")
        if not row.get("group_id") and any(
            key in row for key in ("contrast_kind", "contrast_fact_ids")
        ):
            raise ValueError(f"row {index}: contrast metadata requires group_id")
        if row_type == "abstencio":
            if fact_id is not None or documents:
                raise ValueError(f"row {index}: abstentions need null fact_id and no documents")
            abstention_answers.add(normalized_text(row_answer(row)))
        else:
            if fact_id not in fact_map:
                raise ValueError(f"row {index}: missing fact reference {fact_id!r}")
            if not documents or any(
                not isinstance(doc, str)
                or not doc.startswith("docs/temes/")
                or not (ROOT / doc).is_file()
                for doc in documents
            ):
                raise ValueError(
                    f"row {index}: factual documents must be existing docs/temes files"
                )
            if row.get("group_id"):
                if row["group_id"] not in group_map:
                    raise ValueError(f"row {index}: unknown contrast group {row['group_id']!r}")
                if row_type not in contrast_types or not isinstance(row.get("contrast_kind"), str):
                    raise ValueError(f"row {index}: contrast row needs a contrast type and kind")
                expected_type = {
                    "successio": "contrast-successio",
                    "discriminacio": "contrast-discriminacio",
                    "premissa-falsa": "premissa-falsa",
                }.get(row["contrast_kind"])
                if row_type != expected_type:
                    raise ValueError(f"row {index}: contrast_kind does not match row type")
            elif row_type not in base_types:
                raise ValueError(f"row {index}: contrast type requires group_id")
            if not row.get("group_id"):
                base_by_fact[fact_id] += 1
                questions_by_fact.setdefault(fact_id, set()).add(
                    normalized_text(row_user_question(row))
                )
                primary_answer = next(
                    message["content"]
                    for message in messages
                    if isinstance(message, dict) and message.get("role") == "assistant"
                )
                unique_answers_by_fact.setdefault(fact_id, set()).add(
                    normalized_text(primary_answer)
                )
                answer_texts_by_fact.setdefault(fact_id, []).append(primary_answer)
        for message in messages:
            content = message["content"]
            if message["role"] == "user":
                if re.search(r"·[^—]*—", content):
                    raise ValueError(f"row {index}: user turn contains a topic label delimiter")
                if any(phrase in content.casefold() for phrase in FORBIDDEN_PHRASES):
                    raise ValueError(f"row {index}: forbidden source-reference wording")
                for prefix in (*QUESTION_BOILERPLATE, *CONTEXT_FRAMES):
                    if content.casefold().startswith(prefix.casefold()):
                        prefix_counts[("question", prefix)] += 1
                for prefix in FALSE_QUESTION_STEMS:
                    if content.count(prefix) > 1:
                        raise ValueError(f"row {index}: repeated false-premise question stem")
            elif message["role"] == "assistant":
                if re.search(r"\b\d{1,2}[-/]\d{1,2}[-/]\d{4}\b", content):
                    raise ValueError(f"row {index}: dates must use Catalan month names")
                if row_type != "premissa-falsa":
                    for prefix in ANSWER_BOILERPLATE:
                        if content.casefold().startswith(prefix.casefold()):
                            prefix_counts[("answer", prefix)] += 1
                sentence_count = len(
                    [part for part in re.split(r"(?<=[.!?])\s+", content) if part.strip()]
                )
                if sentence_count < 1 or sentence_count > 3:
                    raise ValueError(f"row {index}: answer has {sentence_count} sentences")
        answer = row_answer(row).strip()
        if not answer:
            raise ValueError(f"row {index}: empty assistant answer")
        if row_type == "dues-voltes":
            if row.get("related_fact_id"):
                related_id = row["related_fact_id"]
                if (
                    related_id not in fact_map
                    or fact_map[related_id]["topic"] != fact_map[fact_id]["topic"]
                ):
                    raise ValueError(f"row {index}: second-turn fact must be in the same topic")
                if not set(documents).intersection(
                    document
                    for candidate in examples
                    if candidate.get("fact_id") == related_id
                    for document in candidate.get("documents", [])
                ):
                    raise ValueError(f"row {index}: documents do not support the second-turn fact")
            elif date.fromisoformat(row["verificat"]) >= date(2026, 11, 1):
                raise ValueError(f"row {index}: new dialogue needs related_fact_id")
            second_question = messages[3]["content"]
            if any(term in second_question.casefold() for term in ("resum", "resumeix", "resumir")):
                raise ValueError(f"row {index}: second turn must ask a related fact, not a summary")
            if normalized_text(messages[1]["content"]) == normalized_text(second_question):
                raise ValueError(f"row {index}: second question must differ from the first")
        abstention_patterns = (
            r"no en tinc (?:cap )?constància|no ho sé|no em consta",
            r"no tinc (?:cap )?(?:informació|dades)|no tinc prou informació",
            r"no puc (?:confirmar|precisar|afirmar)",
            r"no disposo (?:d’aquesta informació|d’informació)",  # noqa: RUF001
            r"no en sé el nom|no puc donar-te aquesta mida|no en tinc cap registre",
            r"no en tinc cap referència fiable|aquesta dada no la puc confirmar",
            r"no puc precisar-ho|no ho puc afirmar|no ho puc verificar",
            r"no sé quin|no sé quina|no tinc aquesta dada confirmada|no em consta el resultat",
        )
        if row_type == "abstencio" and not re.search(
            "|".join(abstention_patterns), answer.casefold()
        ):
            raise ValueError(f"row {index}: abstention must state lack of knowledge")
        pair = json.dumps(messages, ensure_ascii=False, sort_keys=True)
        if pair in seen_pairs:
            raise ValueError(f"row {index}: duplicate conversation")
        seen_pairs.add(pair)
        if row_type != "abstencio" and row.get("group_id"):
            group = group_map[row["group_id"]]
            members = {
                member["fact_id"]: member
                for member in group.get("members", [])
                if isinstance(member, dict) and isinstance(member.get("fact_id"), str)
            }
            involved = row_fact_ids(row)
            if not involved or any(fact not in members for fact in involved):
                raise ValueError(f"row {index}: contrast row has invalid member references")
            normalized_answer = normalized_text(answer)
            if any(
                not members[fact].get("entity_name")
                or normalized_text(members[fact]["entity_name"]) not in normalized_answer
                for fact in involved
            ):
                raise ValueError(f"row {index}: contrast answer must name every full entity")

    checked_fact_ids = {
        fact_id
        for fact_id, fact in fact_map.items()
        if scope is None or fact.get("topic") == scope
    }
    if any(base_by_fact.get(fact_id, 0) != 11 for fact_id in checked_fact_ids):
        bad = {
            fact_id: base_by_fact.get(fact_id, 0)
            for fact_id in checked_fact_ids
            if base_by_fact.get(fact_id, 0) != 11
        }
        raise ValueError(f"every fact needs exactly 11 base rows: {bad}")
    if any(len(questions_by_fact.get(fact_id, set())) != 11 for fact_id in checked_fact_ids):
        raise ValueError("base questions must be unique within every checked fact")
    if any(len(unique_answers_by_fact.get(fact_id, set())) < 5 for fact_id in checked_fact_ids):
        raise ValueError("each checked fact needs at least 5 distinct answer structures")
    grouped_entities: dict[str, set[str]] = {}
    for group in groups:
        for member in group.get("members", []):
            if (
                isinstance(member, dict)
                and isinstance(member.get("fact_id"), str)
                and isinstance(member.get("entity_name"), str)
            ):
                grouped_entities.setdefault(member["fact_id"], set()).add(member["entity_name"])
    for index, row in enumerate(examples, start=1):
        if row.get("type") == "abstencio":
            continue
        if scope and fact_map.get(row.get("fact_id"), {}).get("topic") != scope:
            continue
        messages = row.get("messages", [])
        if row.get("group_id"):
            checked_answers = [
                (row_fact_ids(row), row_answer(row)),
            ]
        else:
            checked_answers = []
            assistant_messages = [
                message.get("content", "")
                for message in messages
                if message.get("role") == "assistant"
            ]
            primary_fact_id = row.get("fact_id")
            if assistant_messages and isinstance(primary_fact_id, str):
                checked_answers.append(([primary_fact_id], assistant_messages[0]))
            related_fact_id = row.get("related_fact_id")
            if len(assistant_messages) > 1 and isinstance(related_fact_id, str):
                checked_answers.append(([related_fact_id], assistant_messages[1]))
        for fact_ids, answer_message in checked_answers:
            for fact_id in fact_ids:
                for entity in grouped_entities.get(fact_id, set()):
                    if not entity[:1].isupper():
                        continue
                    if normalized_text(entity) not in normalized_text(answer_message):
                        raise ValueError(
                            f"row {index} ({row_id}, {fact_id}): answer about a contrast fact omits full entity name {entity!r}"
                        )
    max_answer_similarity = 0.0
    for fact_id, answers in answer_texts_by_fact.items():
        if scope and fact_map[fact_id].get("topic") != scope:
            continue
        fact_phrase = normalized_text(fact_map[fact_id]["fact"])
        if sum(fact_phrase in normalized_text(answer) for answer in answers) > 1:
            raise ValueError(f"fact {fact_id}: literal fact phrase occurs in more than one answer")
        for index, first in enumerate(answers):
            for second in answers[index + 1 :]:
                similarity = SequenceMatcher(
                    None, normalized_text(first), normalized_text(second)
                ).ratio()
                max_answer_similarity = max(max_answer_similarity, similarity)
                if similarity >= 0.8:
                    raise ValueError(
                        f"fact {fact_id}: answer similarity {similarity:.3f} must be below 0.8: {first!r} vs {second!r}"
                    )
    overused_prefixes = {key: value for key, value in prefix_counts.items() if value > 3}
    if overused_prefixes:
        raise ValueError(
            f"question/answer prefixes occur more than three times: {overused_prefixes}"
        )
    total_rows = len(examples)
    factual_rows = total_rows - counts["abstencio"]
    dialogue_ratio = counts["dues-voltes"] / max(1, factual_rows)
    false_ratio = counts["premissa-falsa"] / max(1, factual_rows)
    abstention_ratio = counts["abstencio"] / total_rows
    if scope is None:
        if not 0.08 <= dialogue_ratio <= 0.12:
            raise ValueError(
                f"two-turn dialogue share must be near 10 percent; found {dialogue_ratio:.2%}"
            )
        if not 0.08 <= false_ratio <= 0.12:
            raise ValueError(f"false-premise share must be near 10 percent; found {false_ratio:.2%}")
        if not 0.045 <= abstention_ratio <= 0.055:
            raise ValueError(
                f"abstention share must be approximately 5 percent; found {abstention_ratio:.2%}"
            )

    thematic_questions = validate_question_topics(facts, examples, groups, scope=scope)
    probe_by_fact = {fact["fact_id"]: fact for fact in facts}
    for index, item in enumerate(probe, start=1):
        if item.get("fact_id") not in probe_by_fact:
            raise ValueError(f"probe row {index}: unknown fact_id {item.get('fact_id')!r}")
    probe_topic_counts = Counter(probe_by_fact[item["fact_id"]]["topic"] for item in probe)
    if scope:
        if probe_topic_counts[scope] < 2:
            raise ValueError(f"probe needs at least 2 questions for topic {scope!r}")
    else:
        if set(probe_topic_counts) != EXPECTED_TOPICS:
            raise ValueError(
                f"probe must represent all five topics, found {dict(probe_topic_counts)}"
            )
        if len(probe) < 200:
            raise ValueError(f"full probe needs approximately 200 questions, found {len(probe)}")
    probe_rows = [
        {
            "type": "probe",
            "fact_id": item["fact_id"],
            "messages": [{"role": "user", "content": item["question"]}],
        }
        for item in probe
    ]
    thematic_questions += validate_question_topics(facts, probe_rows, groups, scope=scope)
    scoped_groups = [group for group in groups if scope is None or group.get("topic") == scope]
    group_metrics = validate_contrast_coverage(facts, scoped_groups, examples, probe)
    basic_questions = [
        row_user_question(row) for row in read_jsonl(BASIC_DATASET_PATH) if row_user_question(row)
    ]
    max_probe_similarity = validate_probe_separation(
        probe, examples, facts, scope=scope, dataset_questions=basic_questions
    )

    print(
        f"examples: {len(examples)}; base facts: {len(fact_map)}; "
        f"rows by type: {dict(sorted(counts.items()))}"
    )
    if scope:
        print(f"validation scope: topic {scope}; metrics cover the accumulated corpus")
    print(
        f"answer diversity: min={min(map(len, unique_answers_by_fact.values()))}/11; "
        f"max character similarity={max_answer_similarity:.3f} (<0.8)"
    )
    print(
        f"topic-explicit questions: {thematic_questions}; "
        f"contrast groups: {group_metrics['groups']}; "
        f"contrast rows: {group_metrics['contrast_rows']}"
    )
    print(
        f"probe: {len(probe)} questions; "
        f"max similarity with training={max_probe_similarity:.3f} (<0.8)"
    )
    print(f"probe coverage by topic: {dict(sorted(probe_topic_counts.items()))}")
    print(
        f"dialogues: {counts['dues-voltes']}/{factual_rows} ({dialogue_ratio:.2%}); "
        f"false premises: {counts['premissa-falsa']}/{factual_rows} ({false_ratio:.2%}); "
        f"abstentions: {counts['abstencio']}/{total_rows} ({abstention_ratio:.2%})"
    )
    return {
        "rows": total_rows,
        "facts": len(fact_map),
        "groups": group_metrics["groups"],
        "probe": len(probe),
        "topic_questions": thematic_questions,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--facts-only", action="store_true")
    group.add_argument("--examples-only", action="store_true")
    group.add_argument("--all", action="store_true")
    group.add_argument("--theme", choices=sorted(EXPECTED_TOPICS))
    args = parser.parse_args()
    try:
        facts = validate_facts(args.theme)
        if not args.facts_only:
            validate_examples(facts, scope=args.theme)
    except (OSError, ValueError, json.JSONDecodeError, KeyError, TypeError) as error:
        print(f"validation failed: {error}", file=sys.stderr)
        return 1
    print("validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
