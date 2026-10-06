from __future__ import annotations

import json
from pathlib import Path

from training_data.knowledge_deduplicate import (
    deduplicate_knowledge_candidates,
    write_knowledge_deduplication,
)
from training_data.knowledge_generate import ConversationCandidate, write_knowledge_candidates


def _candidate(
    family_id: str, evidence_ids: tuple[str, ...], user: str, assistant: str
) -> ConversationCandidate:
    return ConversationCandidate(
        family_id=family_id,
        evidence_ids=evidence_ids,
        user=user,
        assistant=assistant,
        review_status="needs_review",
    )


def test_exact_duplicates_merge_without_losing_distinct_evidence() -> None:
    candidates = (
        _candidate("family-a", ("evidence-a",), "Què és la festa?", "És una celebració local."),
        _candidate("family-b", ("evidence-b",), "Què és la festa?", "És una celebració local."),
        _candidate("family-c", ("evidence-c",), "Quan se celebra?", "Al mes de juliol."),
    )

    result = deduplicate_knowledge_candidates(candidates)

    assert len(result.candidates) == 2
    merged = next(
        candidate for candidate in result.candidates if candidate.user == "Què és la festa?"
    )
    assert merged.evidence_ids == ("evidence-a", "evidence-b")
    assert merged.family_id.startswith("exact:")
    assert result.report.exact_duplicate_groups == 1
    assert result.report.exact_records_removed == 1


def test_near_duplicate_family_is_reported_without_removing_candidates(tmp_path: Path) -> None:
    candidates = (
        _candidate(
            "family-a",
            ("evidence-a", "evidence-b"),
            "Quan se celebra la festa?",
            "Se celebra al juliol.",
        ),
        _candidate(
            "family-b",
            ("evidence-b", "evidence-a"),
            "En quin mes és la festa?",
            "La festa és al juliol.",
        ),
        _candidate("family-c", ("evidence-c",), "Què és la festa?", "És una celebració local."),
    )

    result = deduplicate_knowledge_candidates(candidates)

    assert len(result.candidates) == len(candidates)
    family = next(
        family
        for family in result.report.near_duplicate_families
        if set(family.candidate_ids) >= {"family-a", "family-b"}
    )
    assert family.evidence_ids == ("evidence-a", "evidence-b")
    assert len({candidate.family_id for candidate in result.candidates[:2]}) == 1
    assert result.report.near_duplicate_family_count == 1

    write_knowledge_candidates(
        result.candidates,
        work=tmp_path,
        deduplicated_candidates=result.candidates,
    )
    work_records = [
        json.loads(line)
        for line in (tmp_path / "deduplicated-candidates.jsonl").read_text().splitlines()
    ]
    assert len(work_records) == len(candidates)
    assert len({record["family_id"] for record in work_records[:2]}) == 1
    report_path = write_knowledge_deduplication(result.report, reports=tmp_path / "reports")
    assert json.loads(report_path.read_text())["near_duplicate_family_count"] == 1


def test_distinct_followups_are_not_treated_as_exact_duplicates() -> None:
    first = ConversationCandidate(
        family_id="family-a",
        evidence_ids=("evidence-a",),
        user="La Passa és un ball?",
        assistant="No, és una cercavila.",
        review_status="human_reviewed",
        follow_ups=(("Quan es fa?", "Al migdia del dilluns de la festa major."),),
    )
    second = ConversationCandidate(
        family_id="family-b",
        evidence_ids=("evidence-b",),
        user="La Passa és un ball?",
        assistant="No, és una cercavila.",
        review_status="human_reviewed",
        follow_ups=(("Qui va al davant?", "Les parelles que es casaran aquell any."),),
    )

    result = deduplicate_knowledge_candidates((first, second))

    assert len(result.candidates) == 2
    assert result.report.exact_records_removed == 0
