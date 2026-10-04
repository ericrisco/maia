"""Deduplicació exacta i agrupació reversible de famílies semblants."""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from dataclasses import asdict, dataclass, replace
from pathlib import Path

from training_data.knowledge_generate import ConversationCandidate, ReviewStatus


@dataclass(frozen=True, slots=True)
class NearDuplicateFamily:
    """Candidats diferents que comparteixen una o més evidències font."""

    family_id: str
    candidate_ids: tuple[str, ...]
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class DeduplicationReport:
    """Comptadors de duplicats i evidències preservades després d'agrupar."""

    input_candidates: int
    output_candidates: int
    exact_duplicate_groups: int
    exact_records_removed: int
    near_duplicate_family_count: int
    evidence_ids_before: int
    evidence_ids_after: int
    near_duplicate_families: tuple[NearDuplicateFamily, ...]


@dataclass(frozen=True, slots=True)
class DeduplicationResult:
    """Candidats sense duplicats literals i el report dels grups preservats."""

    candidates: tuple[ConversationCandidate, ...]
    report: DeduplicationReport


def _normalize(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).casefold()
    return re.sub(r"\s+", " ", normalized).strip()


def _fingerprint(user: str, assistant: str) -> str:
    return hashlib.sha256(f"{_normalize(user)}\0{_normalize(assistant)}".encode()).hexdigest()


def _stable_group_id(prefix: str, values: set[str]) -> str:
    payload = "\0".join(sorted(values))
    return f"{prefix}:{hashlib.sha256(payload.encode()).hexdigest()[:16]}"


def deduplicate_knowledge_candidates(
    candidates: tuple[ConversationCandidate, ...],
) -> DeduplicationResult:
    """Fusiona converses idèntiques i agrupa variants amb evidència compartida."""

    grouped: dict[str, list[ConversationCandidate]] = {}
    for candidate in candidates:
        grouped.setdefault(_fingerprint(candidate.user, candidate.assistant), []).append(candidate)

    deduplicated: list[ConversationCandidate] = []
    exact_groups = 0
    for fingerprint, duplicates in grouped.items():
        if len(duplicates) > 1:
            exact_groups += 1
        first = duplicates[0]
        evidence_ids = tuple(
            sorted({item for candidate in duplicates for item in candidate.evidence_ids})
        )
        family_id = (
            _stable_group_id("exact", {fingerprint}) if len(duplicates) > 1 else first.family_id
        )
        review_status: ReviewStatus = (
            "human_reviewed"
            if all(candidate.review_status == "human_reviewed" for candidate in duplicates)
            else "needs_review"
        )
        deduplicated.append(
            replace(
                first,
                family_id=family_id,
                evidence_ids=evidence_ids,
                review_status=review_status,
            )
        )

    evidence_groups: dict[tuple[str, ...], list[int]] = {}
    for index, candidate in enumerate(deduplicated):
        signature = tuple(sorted(candidate.evidence_ids))
        evidence_groups.setdefault(signature, []).append(index)

    near_families: list[NearDuplicateFamily] = []
    for indices in evidence_groups.values():
        if len(indices) < 2:
            continue
        members = [deduplicated[index] for index in indices]
        evidence_ids = tuple(
            sorted({item for candidate in members for item in candidate.evidence_ids})
        )
        family_id = _stable_group_id("near", set(evidence_ids))
        near_families.append(
            NearDuplicateFamily(
                family_id=family_id,
                candidate_ids=tuple(candidate.family_id for candidate in members),
                evidence_ids=evidence_ids,
            )
        )
        for index in indices:
            deduplicated[index] = replace(deduplicated[index], family_id=family_id)

    before_evidence = {item for candidate in candidates for item in candidate.evidence_ids}
    after_evidence = {item for candidate in deduplicated for item in candidate.evidence_ids}
    report = DeduplicationReport(
        input_candidates=len(candidates),
        output_candidates=len(deduplicated),
        exact_duplicate_groups=exact_groups,
        exact_records_removed=len(candidates) - len(deduplicated),
        near_duplicate_family_count=len(near_families),
        evidence_ids_before=len(before_evidence),
        evidence_ids_after=len(after_evidence),
        near_duplicate_families=tuple(near_families),
    )
    return DeduplicationResult(tuple(deduplicated), report)


def write_knowledge_deduplication(report: DeduplicationReport, *, reports: Path) -> Path:
    """Desa els grups exactes i semblants per revisar-los sense perdre evidències."""

    reports.mkdir(parents=True, exist_ok=True)
    path = reports / "deduplication.json"
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(
        json.dumps(asdict(report), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)
    return path
