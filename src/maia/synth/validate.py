"""Dataset validator (ANEXO §3.2) — blocks all of Phase 2.

The §3.2 analogue of :mod:`maia.corpus.validate`: nothing enters the training set that does
not conform. Per-example shape is the schema's job
(:class:`~maia.schemas.DatasetExample`); this module enforces the four things that are only
visible **across** the whole dataset, and that the wiki states as hard constraints:

* **Distribution.** ``no_ho_se`` ≈ 8 % ± 2 and ``general_ca`` 15-20 %. These are not style
  preferences: the first is how the model learns to decline instead of inventing, and the
  second is the anti-forgetting mix. A dataset that drifts out of range trains a different
  model than the one designed, and nothing downstream would notice.
* **Splits.** 90/5/5 within tolerance, and — the important one — **no example may appear in
  more than one split**. Leakage between train and test silently inflates every Phase 4
  number, which is the failure that makes an evaluation worthless rather than merely wrong.
* **The frozen test split.** :func:`split_digest` hashes the test examples so the hash can be
  committed; :func:`verify_frozen` re-checks it. The test split becomes part of the benchmark,
  so it must be provably the same set that was frozen.
* **Licence.** ``no-redistribute`` corpus documents may ground a *paraphrase* but their text
  may never be republished. See :func:`check_licence` for how that ambiguity is handled — and
  why ``rag_style`` is the one unambiguous violation.

Grounding ids are also checked against the corpus when one is supplied: an example citing a
document that does not exist is not grounded in anything, whatever it claims.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from pydantic import ValidationError

from maia.schemas import CorpusDocument, DatasetExample, ExampleType, Split
from maia.synth.taxonomy import load_taxonomy

#: ``no_ho_se`` share: ≈8 % ± 2 (§3.2).
NO_HO_SE_RANGE = (0.06, 0.10)
#: ``general_ca`` share: 15-20 %, the anti-forgetting mix (§3.2).
GENERAL_CA_RANGE = (0.15, 0.20)
#: Target split proportions, 90/5/5.
SPLIT_TARGETS = {Split.TRAIN: 0.90, Split.VAL: 0.05, Split.TEST: 0.05}
#: How far a split may drift from its target before it is a finding.
SPLIT_TOLERANCE = 0.02

#: Phase 2 targets 10,000-15,000 examples.
TARGET_MIN_EXAMPLES = 10_000
TARGET_MAX_EXAMPLES = 15_000


@dataclass(frozen=True)
class Finding:
    """One problem with the dataset. ``locator`` is a line number or an example id."""

    locator: str
    reason: str


@dataclass
class DatasetReport:
    """Outcome of validating a dataset file."""

    total: int = 0
    valid: int = 0
    invalid: list[Finding] = field(default_factory=list)
    constraint_failures: list[Finding] = field(default_factory=list)
    licence_failures: list[Finding] = field(default_factory=list)
    licence_warnings: list[Finding] = field(default_factory=list)
    by_type: Counter[str] = field(default_factory=Counter)
    by_split: Counter[str] = field(default_factory=Counter)
    by_topic: Counter[str] = field(default_factory=Counter)
    test_digest: str = ""
    #: Checks that could not run (e.g. no corpus supplied). Reported, never silent.
    skipped: list[str] = field(default_factory=list)

    @property
    def within_target(self) -> bool:
        """Whether the dataset is inside DoD-F2's 10-15k example range."""
        return TARGET_MIN_EXAMPLES <= self.valid <= TARGET_MAX_EXAMPLES

    @property
    def ok(self) -> bool:
        """True when every example conforms and every hard constraint holds."""
        return (
            self.total > 0
            and not self.invalid
            and not self.constraint_failures
            and not self.licence_failures
        )

    def share(self, example_type: ExampleType) -> float:
        """This type's share of the dataset."""
        return self.by_type.get(example_type.value, 0) / self.valid if self.valid else 0.0


def validate_line(raw: str, line_no: int) -> tuple[DatasetExample | None, Finding | None]:
    """Validate one JSONL line against §3.2."""
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        return None, Finding(str(line_no), f"invalid JSON: {exc.msg}")
    if not isinstance(data, dict):
        return None, Finding(str(line_no), f"expected a JSON object, got {type(data).__name__}")
    try:
        return DatasetExample.model_validate(data), None
    except ValidationError as exc:
        parts = [
            f"{'.'.join(str(x) for x in error['loc']) or '<root>'}: {error['msg']}"
            for error in exc.errors()
        ]
        return None, Finding(str(line_no), "; ".join(parts))


def check_distribution(examples: Sequence[DatasetExample]) -> list[Finding]:
    """Check the ``no_ho_se`` and ``general_ca`` proportions."""
    findings: list[Finding] = []
    if not examples:
        return [Finding("<dataset>", "the dataset is empty")]

    counts = Counter(example.type.value for example in examples)
    for example_type, (low, high) in (
        (ExampleType.NO_HO_SE, NO_HO_SE_RANGE),
        (ExampleType.GENERAL_CA, GENERAL_CA_RANGE),
    ):
        share = counts.get(example_type.value, 0) / len(examples)
        if not low <= share <= high:
            findings.append(
                Finding(
                    "<distribution>",
                    f"{example_type.value} is {share:.1%} of the dataset, outside "
                    f"{low:.0%}-{high:.0%}",
                )
            )
    return findings


def check_splits(examples: Sequence[DatasetExample]) -> list[Finding]:
    """Check split proportions and, crucially, that no example is in two splits.

    An id appearing in both train and test silently inflates every Phase 4 number. It is
    checked here rather than trusted because it cannot be seen in any single example.
    """
    findings: list[Finding] = []
    if not examples:
        return findings

    # Keyed on the *content*, not only the id. Generation derives ids with UUID5 scoped to the
    # taxonomy node, so two nodes with overlapping keywords produce different ids for a
    # byte-identical conversation — an adversarial review showed such a pair landing in train
    # and test with the check reporting clean.
    seen: dict[str, tuple[str, Split]] = {}
    for example in examples:
        fingerprint = hashlib.sha256(
            json.dumps(
                [[m.role.value, m.content] for m in example.messages], ensure_ascii=False
            ).encode("utf-8")
        ).hexdigest()
        for key in (f"id:{example.id}", f"text:{fingerprint}"):
            previous = seen.get(key)
            if previous is not None and previous[1] is not example.split:
                findings.append(
                    Finding(
                        str(example.id),
                        f"the same {'id' if key.startswith('id:') else 'conversation'} appears "
                        f"in both {previous[1].value} and {example.split.value} — "
                        "train/test leakage",
                    )
                )
            seen[key] = (str(example.id), example.split)

    counts = Counter(example.split.value for example in examples)
    for split, target in SPLIT_TARGETS.items():
        share = counts.get(split.value, 0) / len(examples)
        if abs(share - target) > SPLIT_TOLERANCE:
            findings.append(
                Finding(
                    "<splits>",
                    f"{split.value} is {share:.1%}, more than {SPLIT_TOLERANCE:.0%} from the "
                    f"{target:.0%} target",
                )
            )
    return findings


def check_grounding(examples: Sequence[DatasetExample], corpus_ids: set[str]) -> list[Finding]:
    """Check every ``grounding_id`` exists in the corpus.

    An example citing a document that is not there is not grounded in anything, whatever it
    claims — and since grounding is the anti-hallucination measure, an unresolvable citation
    means the anti-hallucination measure did not apply to that example.
    """
    return [
        Finding(str(example.id), f"grounding_id {grounding_id} is not in the corpus")
        for example in examples
        for grounding_id in example.grounding_ids
        if grounding_id not in corpus_ids
    ]


def check_topics(examples: Sequence[DatasetExample], node_ids: set[str]) -> list[Finding]:
    """Check every ``topic`` is a real taxonomy node.

    §3.2 defines ``topic`` as *"taxonomy node"*. Without this the field is free text: a dataset
    with invented or misspelt topics validates green, and the M1.10-style coverage question
    ("which nodes did we actually cover?") silently answers itself with garbage. The blocker
    noted in the wiki gaps — "cannot check until M2.01 lands `configs/taxonomy.yaml`" — was
    removed when M2.01 shipped.
    """
    return [
        Finding(str(example.id), f"topic {example.topic!r} is not a taxonomy node")
        for example in examples
        if example.topic not in node_ids
    ]


def check_licence(
    examples: Sequence[DatasetExample], restricted_ids: set[str]
) -> tuple[list[Finding], list[Finding]]:
    """Check §3.2's licence rule. Returns ``(failures, warnings)``.

    The rule — *"no grounding_id with license = no-redistribute in examples that quote literal
    text"* — turns on whether an example quotes or paraphrases, and that is not decidable from
    the record alone. So it is split:

    * **Failures** — ``rag_style`` examples grounded on a restricted document. This type
      *embeds the passage as its context by construction*, so it necessarily republishes the
      text. No judgement needed.
    * **Warnings** — every other type grounded on a restricted document. Paraphrasing
      restricted knowledge is explicitly allowed ("the public dataset paraphrases their
      knowledge"), so these cannot be failed automatically; they are the review list for the
      M6.01 legal-cleanup gate.

    Erring the other way — failing every restricted grounding — would block the legitimate
    paraphrase the compliance article permits, and the honest answer is to surface the set
    rather than guess at it.
    """
    failures: list[Finding] = []
    warnings: list[Finding] = []
    for example in examples:
        hits = [gid for gid in example.grounding_ids if gid in restricted_ids]
        if not hits:
            continue
        detail = f"grounds on {len(hits)} no-redistribute document(s)"
        if example.type.embeds_source_text():
            failures.append(
                Finding(
                    str(example.id),
                    f"type={example.type.value} {detail}: this type carries the passage "
                    "verbatim as context, so it republishes restricted text",
                )
            )
        else:
            warnings.append(
                Finding(str(example.id), f"type={example.type.value} {detail} — review at M6.01")
            )
    return failures, warnings


def split_digest(examples: Iterable[DatasetExample], split: Split = Split.TEST) -> str:
    """A stable digest of one split — what gets committed to freeze the test set.

    Order-independent (ids are sorted first), so re-serialising the dataset does not change
    the hash, and content-sensitive, so editing an example does.
    """
    hasher = hashlib.sha256()
    payload = sorted(
        example.model_dump_json(exclude={"split"}) for example in examples if example.split is split
    )
    for line in payload:
        hasher.update(line.encode("utf-8"))
        hasher.update(b"\n")
    return hasher.hexdigest()


def verify_frozen(
    examples: Iterable[DatasetExample], expected: str, split: Split = Split.TEST
) -> Finding | None:
    """Check a split still matches its committed digest. ``None`` when it does."""
    actual = split_digest(examples, split)
    if actual == expected:
        return None
    return Finding(
        f"<{split.value}>",
        f"split digest is {actual} but {expected} was frozen — the {split.value} split changed",
    )


def validate_dataset(
    examples: Sequence[DatasetExample],
    *,
    corpus_ids: set[str] | None = None,
    restricted_ids: set[str] | None = None,
    node_ids: set[str] | None = None,
    report: DatasetReport | None = None,
) -> DatasetReport:
    """Run every cross-dataset check over already-parsed examples.

    ``corpus_ids`` / ``restricted_ids`` of ``None`` mean *no corpus was supplied*, so the
    grounding and licence checks cannot run. That is recorded on the report as
    :attr:`DatasetReport.skipped` and rendered — a green line that silently skipped the licence
    wall proves nothing.
    """
    report = report if report is not None else DatasetReport()
    report.valid = len(examples)
    for example in examples:
        report.by_type[example.type.value] += 1
        report.by_split[example.split.value] += 1
        report.by_topic[example.topic] += 1

    report.constraint_failures.extend(check_distribution(examples))
    report.constraint_failures.extend(check_splits(examples))
    if corpus_ids is not None:
        report.constraint_failures.extend(check_grounding(examples, corpus_ids))
    else:
        report.skipped.append("grounding resolution (no --corpus supplied)")
    if restricted_ids is None:
        report.skipped.append("licence check (no --corpus supplied)")
    if node_ids is not None:
        report.constraint_failures.extend(check_topics(examples, node_ids))
    else:
        report.skipped.append("taxonomy coverage (no --taxonomy supplied)")
    if restricted_ids is not None:
        failures, warnings = check_licence(examples, restricted_ids)
        report.licence_failures.extend(failures)
        report.licence_warnings.extend(warnings)
    report.test_digest = split_digest(examples)
    return report


def read_dataset(path: Path, report: DatasetReport) -> list[DatasetExample]:
    """Read and §3.2-validate every non-blank line of a JSONL dataset file."""
    examples: list[DatasetExample] = []
    with path.open(encoding="utf-8") as handle:
        for line_no, raw in enumerate(handle, start=1):
            if not raw.strip():
                continue
            report.total += 1
            example, finding = validate_line(raw, line_no)
            if finding is not None:
                report.invalid.append(finding)
                continue
            assert example is not None
            examples.append(example)
    return examples


def read_corpus_ids(paths: Iterable[Path]) -> tuple[set[str], set[str]]:
    """Read a corpus and return ``(all ids, no-redistribute ids)``."""
    all_ids: set[str] = set()
    restricted: set[str] = set()
    for path in paths:
        with path.open(encoding="utf-8") as handle:
            for raw in handle:
                if not raw.strip():
                    continue
                document = CorpusDocument.model_validate(json.loads(raw))
                all_ids.add(document.id)
                if not document.license.is_public():
                    restricted.add(document.id)
    return all_ids, restricted


def render(report: DatasetReport, path: Path) -> str:
    """Human-readable summary."""
    lines = [
        f"dataset: {path}",
        f"  examples: {report.total}  valid: {report.valid}  invalid: {len(report.invalid)}",
    ]
    if report.by_type:
        lines.append(
            "  by type: "
            + ", ".join(
                f"{name}={count} ({count / report.valid:.1%})"
                for name, count in sorted(report.by_type.items())
            )
        )
    if report.by_split:
        lines.append(
            "  by split: " + ", ".join(f"{k}={v}" for k, v in sorted(report.by_split.items()))
        )
    if report.by_topic:
        lines.append(f"  taxonomy nodes covered: {len(report.by_topic)}")
    if report.valid:
        lines.append(f"  test split digest: {report.test_digest}")
    for skipped in report.skipped:
        lines.append(f"  ⚠ NOT CHECKED: {skipped}")
    for label, findings in (
        ("✗ invalid", report.invalid),
        ("✗ constraint", report.constraint_failures),
        ("✗ licence", report.licence_failures),
        ("⚠ licence", report.licence_warnings),
    ):
        for finding in findings[:20]:
            lines.append(f"  {label} {finding.locator}: {finding.reason}")
        if len(findings) > 20:
            lines.append(f"  … and {len(findings) - 20} more {label.split()[-1]} findings")
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point. Exit 0 when the dataset fully conforms, 1 otherwise."""
    parser = argparse.ArgumentParser(
        description="Validate a JSONL dataset against the §3.2 schema and its distribution, "
        "split, grounding and licence constraints."
    )
    parser.add_argument("path", type=Path, help="the JSONL dataset file")
    parser.add_argument(
        "--corpus",
        type=Path,
        nargs="*",
        default=[],
        help="corpus JSONL file(s): enables grounding and licence checks",
    )
    parser.add_argument(
        "--taxonomy",
        type=Path,
        help="configs/taxonomy.yaml: enables the check that every topic is a real node",
    )
    parser.add_argument(
        "--frozen-test-digest",
        help="fail unless the test split still matches this committed digest",
    )
    parser.add_argument(
        "--require-target",
        action="store_true",
        help=f"also fail unless the dataset holds {TARGET_MIN_EXAMPLES}-{TARGET_MAX_EXAMPLES} "
        "examples (DoD-F2's first clause)",
    )
    parser.add_argument(
        "--skip-distribution",
        action="store_true",
        help="report the distribution without failing on it (for a pilot batch, M2.06, which "
        "is too small for the proportions to be meaningful)",
    )
    args = parser.parse_args(argv)

    for path in [args.path, *args.corpus, *([args.taxonomy] if args.taxonomy else [])]:
        if not path.is_file():
            print(f"error: no such file: {path}", file=sys.stderr)
            return 1

    report = DatasetReport()
    examples = read_dataset(args.path, report)
    corpus_ids, restricted_ids = read_corpus_ids(args.corpus) if args.corpus else (None, set())
    node_ids = load_taxonomy(args.taxonomy).ids if args.taxonomy else None
    validate_dataset(
        examples,
        corpus_ids=corpus_ids,
        restricted_ids=restricted_ids,
        node_ids=node_ids,
        report=report,
    )

    if args.skip_distribution:
        report.constraint_failures = [
            finding
            for finding in report.constraint_failures
            if finding.locator not in {"<distribution>", "<splits>"}
        ]

    frozen_finding = (
        verify_frozen(examples, args.frozen_test_digest) if args.frozen_test_digest else None
    )
    if frozen_finding is not None:
        report.constraint_failures.append(frozen_finding)

    print(render(report, args.path))
    if args.require_target and not report.within_target:
        print(
            f"error: {report.valid} examples is outside DoD-F2's "
            f"{TARGET_MIN_EXAMPLES}-{TARGET_MAX_EXAMPLES} range",
            file=sys.stderr,
        )
        return 1
    return 0 if report.ok else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
