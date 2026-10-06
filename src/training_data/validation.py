"""Validators globals d'esquema, procedència, cobertura i fuites de split."""

from __future__ import annotations

import json
import re
from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from training_data.knowledge import KnowledgeLedger
from training_data.knowledge_coverage import KnowledgeCoverageReport
from training_data.knowledge_generate import ConversationCandidate
from training_data.knowledge_split import KnowledgeSplit
from training_data.language import LanguageLedger
from training_data.language_conversations import SpeechConversationCandidate
from training_data.language_split import LanguageSplit
from training_data.language_uncertainty import _candidate_uncertainties

MARKDOWN = re.compile(
    r"(?:\*\*|__|~~|`|!?\[[^\]]*\]\([^)]*\)|^\s*(?:[-*+]\s|\d{1,2}[.)]\s|\|))",
    re.MULTILINE,
)


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    """Una infracció concreta del contracte d'un dataset."""

    code: str
    message: str
    path: str | None = None
    line: int | None = None


@dataclass(frozen=True, slots=True)
class DatasetValidationReport:
    """Resultat verificable d'un dels dos datasets."""

    dataset: str
    valid: bool
    record_counts: dict[str, int]
    exact_duplicates: int
    issues: tuple[ValidationIssue, ...]


@dataclass(frozen=True, slots=True)
class TrainingDataValidationReport:
    """Estat agregat de Maia Knowledge i Maia Language."""

    valid: bool
    knowledge: DatasetValidationReport
    language: DatasetValidationReport
    knowledge_coverage: float


def _fingerprint(record: Mapping[str, object]) -> tuple[tuple[str, str], ...] | None:
    messages = record.get("messages")
    if not isinstance(messages, list) or len(messages) < 2 or len(messages) % 2:
        return None
    transcript: list[tuple[str, str]] = []
    for index, message in enumerate(messages):
        if not isinstance(message, dict):
            return None
        role = message.get("role")
        content = message.get("content")
        expected_role = "user" if index % 2 == 0 else "assistant"
        if role != expected_role or not isinstance(content, str):
            return None
        transcript.append((expected_role, re.sub(r"\s+", " ", content).strip().casefold()))
    return tuple(transcript)


def _candidate_fingerprints(
    candidates: tuple[ConversationCandidate | SpeechConversationCandidate, ...],
) -> Counter[tuple[tuple[str, str], ...]]:
    fingerprints: Counter[tuple[tuple[str, str], ...]] = Counter()
    for candidate in candidates:
        fingerprint = _fingerprint(candidate.to_public_record())
        if fingerprint is not None:
            fingerprints[fingerprint] += 1
    return fingerprints


def validate_public_splits(paths: dict[str, Path], *, dataset: str) -> DatasetValidationReport:
    """Valida JSONL públic, missatges, text pla i duplicats entre splits."""

    issues: list[ValidationIssue] = []
    counts: dict[str, int] = {}
    seen: dict[tuple[tuple[str, str], ...], tuple[str, int]] = {}
    duplicates = 0
    for split_name, path in paths.items():
        counts[split_name] = 0
        if not path.exists():
            issues.append(ValidationIssue("missing_split", "Split file is missing.", str(path)))
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError as error:
            issues.append(ValidationIssue("unreadable_split", str(error), str(path)))
            continue
        for line_number, line in enumerate(lines, start=1):
            if not line.strip():
                issues.append(
                    ValidationIssue(
                        "empty_jsonl_line", "JSONL contains a blank line.", str(path), line_number
                    )
                )
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                issues.append(ValidationIssue("invalid_json", str(error), str(path), line_number))
                continue
            if not isinstance(record, dict) or set(record) != {"messages"}:
                issues.append(
                    ValidationIssue(
                        "public_schema",
                        "Record must contain only the messages field.",
                        str(path),
                        line_number,
                    )
                )
                continue
            messages = record.get("messages")
            if not isinstance(messages, list) or len(messages) < 2 or len(messages) % 2:
                issues.append(
                    ValidationIssue(
                        "message_count",
                        "Record must contain complete user-assistant turn pairs.",
                        str(path),
                        line_number,
                    )
                )
                continue
            valid_messages = True
            for message_index, message in enumerate(messages):
                role = "user" if message_index % 2 == 0 else "assistant"
                if not isinstance(message, dict) or set(message) != {"role", "content"}:
                    issues.append(
                        ValidationIssue(
                            "message_schema",
                            "Message must contain only role and content.",
                            str(path),
                            line_number,
                        )
                    )
                    valid_messages = False
                    continue
                content = message.get("content")
                if message.get("role") != role:
                    issues.append(
                        ValidationIssue(
                            "message_role", f"Expected {role!r} role.", str(path), line_number
                        )
                    )
                    valid_messages = False
                if not isinstance(content, str) or not content.strip():
                    issues.append(
                        ValidationIssue(
                            "empty_content",
                            "Message content must be non-empty text.",
                            str(path),
                            line_number,
                        )
                    )
                    valid_messages = False
                elif MARKDOWN.search(content):
                    issues.append(
                        ValidationIssue(
                            "markdown_residue",
                            "Public content contains Markdown syntax.",
                            str(path),
                            line_number,
                        )
                    )
                    valid_messages = False
            if not valid_messages:
                continue
            signature = _fingerprint(record)
            if signature is not None:
                previous = seen.get(signature)
                if previous is not None:
                    duplicates += 1
                    issues.append(
                        ValidationIssue(
                            "exact_duplicate",
                            f"Duplicate of {previous[0]} line {previous[1]}.",
                            str(path),
                            line_number,
                        )
                    )
                else:
                    seen[signature] = (str(path), line_number)
            counts[split_name] += 1
    return DatasetValidationReport(dataset, not issues, counts, duplicates, tuple(issues))


def validate_knowledge_dataset(
    paths: dict[str, Path],
    split: KnowledgeSplit,
    ledger: KnowledgeLedger,
    coverage: KnowledgeCoverageReport,
) -> DatasetValidationReport:
    """Verifica que Knowledge respecti esquema, evidències, fonts i split."""

    report = validate_public_splits(paths, dataset="Maia Knowledge")
    issues = list(report.issues)
    evidence = {unit.id: unit for unit in ledger.units}
    records = {"train": split.train, "validation": split.validation, "test": split.test}
    expected_counts: dict[str, int] = {}
    family_splits: dict[str, str] = {}
    expected_public: dict[str, Counter[tuple[tuple[str, str], ...]]] = {}
    for split_name, candidates in records.items():
        expected_counts[split_name] = len(candidates)
        expected_public[split_name] = _candidate_fingerprints(candidates)
        for candidate in candidates:
            previous = family_splits.setdefault(candidate.family_id, split_name)
            if previous != split_name:
                issues.append(
                    ValidationIssue("family_leakage", "A Knowledge family crosses splits.")
                )
            if split.manifest.assignments.get(candidate.family_id) != split_name:
                issues.append(
                    ValidationIssue(
                        "manifest_assignment_mismatch",
                        f"Knowledge family {candidate.family_id!r} differs from the manifest.",
                    )
                )
            for evidence_id in candidate.evidence_ids:
                unit = evidence.get(evidence_id)
                if unit is None:
                    issues.append(
                        ValidationIssue("unknown_evidence", f"Unknown evidence ID: {evidence_id}.")
                    )
                    continue
                if not unit.provenance or any(
                    reference.status != "recorded" for reference in unit.provenance
                ):
                    issues.append(
                        ValidationIssue(
                            "invalid_provenance", f"Unresolved provenance for {evidence_id}."
                        )
                    )
                if unit.volatility_score >= 0.5:
                    issues.append(
                        ValidationIssue(
                            "volatile_evidence", f"Volatile evidence exported: {evidence_id}."
                        )
                    )
    for split_name, path in paths.items():
        if not path.exists():
            continue
        actual: Counter[tuple[str, str]] = Counter()
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(record, dict):
                signature = _fingerprint(record)
                if signature is not None:
                    actual[signature] += 1
        if actual != expected_public.get(split_name, Counter()):
            issues.append(
                ValidationIssue(
                    "split_content_mismatch",
                    f"{split_name} JSONL does not match its internal candidate records.",
                    str(path),
                )
            )
        if len(actual) != expected_counts.get(split_name, 0):
            issues.append(
                ValidationIssue(
                    "split_count_mismatch",
                    f"{split_name} count differs from the split manifest.",
                    str(path),
                )
            )
    if coverage.total_coverage != 1.0:
        issues.append(
            ValidationIssue("incomplete_coverage", "Knowledge evidence is not fully classified.")
        )
    return DatasetValidationReport(
        report.dataset, not issues, report.record_counts, report.exact_duplicates, tuple(issues)
    )


def validate_language_dataset(
    paths: dict[str, Path], split: LanguageSplit, ledger: LanguageLedger
) -> DatasetValidationReport:
    """Verifica text fontal, elegibilitat, incertesa i grups de Language."""

    report = validate_public_splits(paths, dataset="Maia Language")
    issues = list(report.issues)
    pieces = {piece.path: piece for piece in ledger.pieces}
    records = {"train": split.train, "validation": split.validation, "test": split.test}
    expected_public: dict[str, Counter[tuple[str, str]]] = {}
    identifier_splits: dict[tuple[str, str], str] = {}
    for split_name, candidates in records.items():
        expected_public[split_name] = _candidate_fingerprints(candidates)
        for candidate in candidates:
            piece = pieces.get(candidate.source_path)
            if (
                piece is None
                or piece.eligibility != "eligible"
                or piece.voice != "originaria"
                or piece.epoch != "contemporania"
                or piece.language_eligible is not True
            ):
                issues.append(
                    ValidationIssue(
                        "ineligible_language_source",
                        f"Language source is not eligible: {candidate.source_path}.",
                    )
                )
                continue
            if split.manifest.candidate_splits.get(candidate.family_id) != split_name:
                issues.append(
                    ValidationIssue(
                        "manifest_assignment_mismatch",
                        f"Language candidate {candidate.family_id!r} differs from the manifest.",
                    )
                )
            if not piece.provenance or any(
                reference.status != "recorded" for reference in piece.provenance
            ):
                issues.append(
                    ValidationIssue(
                        "invalid_language_provenance",
                        f"Unresolved source card: {candidate.source_path}.",
                    )
                )
            if candidate.user != piece.text[candidate.user_start : candidate.user_end]:
                issues.append(
                    ValidationIssue(
                        "rewritten_user_turn", f"User turn changed: {candidate.family_id}."
                    )
                )
            if (
                candidate.assistant
                != piece.text[candidate.assistant_start : candidate.assistant_end]
            ):
                issues.append(
                    ValidationIssue(
                        "rewritten_assistant_turn",
                        f"Assistant turn changed: {candidate.family_id}.",
                    )
                )
            if _candidate_uncertainties(piece, candidate):
                issues.append(
                    ValidationIssue(
                        "uncertain_language_turn",
                        f"Uncertain span reaches output: {candidate.family_id}.",
                    )
                )
            for kind, identifier in (
                ("piece", candidate.piece_id),
                ("conversation", candidate.conversation_id),
                ("speaker", candidate.speaker_id),
            ):
                if identifier is None:
                    continue
                key = (kind, identifier)
                previous = identifier_splits.setdefault(key, split_name)
                if previous != split_name:
                    issues.append(
                        ValidationIssue(
                            "language_group_leakage",
                            f"{kind} {identifier!r} crosses splits.",
                        )
                    )
    for split_name, path in paths.items():
        if not path.exists():
            continue
        actual: Counter[tuple[str, str]] = Counter()
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(record, dict):
                signature = _fingerprint(record)
                if signature is not None:
                    actual[signature] += 1
        if actual != expected_public.get(split_name, Counter()):
            issues.append(
                ValidationIssue(
                    "split_content_mismatch",
                    f"{split_name} JSONL does not match its source-turn records.",
                    str(path),
                )
            )
    return DatasetValidationReport(
        report.dataset, not issues, report.record_counts, report.exact_duplicates, tuple(issues)
    )


def validate_training_data(
    knowledge: DatasetValidationReport,
    language: DatasetValidationReport,
    *,
    knowledge_coverage: float,
) -> TrainingDataValidationReport:
    """Construeix el resum global amb el valor de cobertura Knowledge."""

    valid = knowledge.valid and language.valid and knowledge_coverage == 1.0
    return TrainingDataValidationReport(valid, knowledge, language, knowledge_coverage)
