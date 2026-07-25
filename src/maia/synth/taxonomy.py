"""Generation taxonomy — PLAN M2.01.

The 60-80 node map of what the synthetic dataset must cover, loaded from
``configs/taxonomy.yaml``. Every generated example carries its node in ``topic`` (§3.2), so
the taxonomy is what makes coverage measurable rather than assumed: without it, "we generated
12,000 examples" says nothing about whether the model was taught the judicial hierarchy or
just asked about ski resorts a thousand times.

**The taxonomy is a PO input and must be approved before generation runs.** That is not a
formality — the node list decides what the model knows, and it is far cheaper to argue about
a YAML file than to regenerate 12,000 examples at €30-60 of API. This module therefore does
two things and deliberately not a third:

* It **validates** a taxonomy: the 60-80 count the plan specifies, unique well-formed ids,
  every branch non-empty, and the presence of the branches the plan names — including the
  ``legal`` branch, which exists to teach *concepts* while citable details stay in RAG (D8).
* It **exposes an approval flag**. ``approved: false`` in the file means the generator must
  refuse to run; :func:`require_approved` is the check M2.03 calls.
* It does **not** invent coverage silently. The shipped file is a *draft* derived from the
  branches and examples the Phase-1 plan enumerates, marked unapproved, for the PO to edit.

Each node carries ``keywords`` because generation samples corpus passages per node: the
keywords are how the sampler finds the 5-20 passages that ground that node's examples. A node
whose keywords retrieve nothing is a node that will generate ungrounded examples, so
:func:`check_retrievable` reports that against a real corpus before any generation happens.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Self

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator

from maia.schemas import CorpusDocument, normalize_text

#: The plan's range: 60-80 nodes. Fewer is thin coverage; more spreads the generation budget
#: so thin that each node gets too few examples to teach anything.
MIN_NODES = 60
MAX_NODES = 80

#: Branches the Phase-1 plan names explicitly. Each must be present and non-empty.
REQUIRED_BRANCHES = (
    "historia",
    "institucions",
    "geografia",
    "cultura",
    "legal",
    "gastronomia",
    "economia",
    "lexic",
)

#: A node id: ``branch/slug``, lowercase, digits and hyphens.
_NODE_ID = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*/[a-z0-9]+(?:-[a-z0-9]+)*")


class TaxonomyNode(BaseModel):
    """One topic the dataset must cover."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=3)
    label: str = Field(min_length=1)
    #: Terms used to retrieve this node's grounding passages from the corpus.
    keywords: list[str] = Field(min_length=1)
    #: Relative share of the generation budget. 1.0 is an ordinary node.
    weight: float = Field(default=1.0, gt=0.0, le=5.0)
    notes: str = ""

    @field_validator("keywords", mode="before")
    @classmethod
    def _stringify_scalars(cls, value: object) -> object:
        """Accept the numbers YAML infers from bare years.

        A PO writing ``keywords: [pareatge, 1278]`` is entirely natural, and YAML types that
        ``1278`` as an int. Failing on it would be user-hostile for a file whose whole purpose
        is to be hand-edited, and the coercion is unambiguous.
        """
        if isinstance(value, list):
            return [str(item) if isinstance(item, int | float) else item for item in value]
        return value

    @model_validator(mode="after")
    def _check_id(self) -> Self:
        if not _NODE_ID.fullmatch(self.id):
            raise ValueError(f"node id {self.id!r} must be 'branch/slug' in lowercase with hyphens")
        if any(not keyword.strip() for keyword in self.keywords):
            raise ValueError(f"node {self.id!r} has an empty keyword")
        return self

    @property
    def branch(self) -> str:
        """The branch this node belongs to, from its id."""
        return self.id.split("/", 1)[0]


class Taxonomy(BaseModel):
    """The whole node map, plus the approval flag the generator checks."""

    model_config = ConfigDict(extra="forbid")

    version: str = Field(min_length=1)
    #: False until the PO has reviewed the node list. The generator refuses to run while false.
    approved: bool = False
    approved_by: str = ""
    notes: str = ""
    nodes: list[TaxonomyNode] = Field(min_length=1)

    @model_validator(mode="after")
    def _check_unique_ids(self) -> Self:
        counts = Counter(node.id for node in self.nodes)
        duplicates = sorted(node_id for node_id, n in counts.items() if n > 1)
        if duplicates:
            raise ValueError(f"duplicate node ids: {', '.join(duplicates)}")
        if self.approved and not self.approved_by:
            raise ValueError("approved=true requires approved_by")
        return self

    @property
    def branches(self) -> dict[str, list[TaxonomyNode]]:
        """Nodes grouped by branch, in file order."""
        grouped: dict[str, list[TaxonomyNode]] = {}
        for node in self.nodes:
            grouped.setdefault(node.branch, []).append(node)
        return grouped

    @property
    def ids(self) -> set[str]:
        """Every node id — what §3.2's ``topic`` field must be one of."""
        return {node.id for node in self.nodes}

    def node(self, node_id: str) -> TaxonomyNode:
        """Look up one node.

        Raises:
            KeyError: if there is no such node.
        """
        for candidate in self.nodes:
            if candidate.id == node_id:
                return candidate
        raise KeyError(node_id)


@dataclass(frozen=True)
class Finding:
    """One problem with a taxonomy."""

    locator: str
    reason: str


@dataclass
class TaxonomyReport:
    """Outcome of checking a taxonomy."""

    nodes: int = 0
    branches: dict[str, int] = field(default_factory=dict)
    findings: list[Finding] = field(default_factory=list)
    unretrievable: list[Finding] = field(default_factory=list)
    approved: bool = False

    @property
    def ok(self) -> bool:
        """True when the taxonomy is structurally sound (approval is a separate question)."""
        return not self.findings


class NotApprovedError(RuntimeError):
    """Raised when generation is attempted against an unapproved taxonomy."""


def load_taxonomy(path: str | Path) -> Taxonomy:
    """Read and validate ``configs/taxonomy.yaml``.

    Raises:
        ValueError: if the file is not a mapping, or does not satisfy the schema. The message
            names the problem — a taxonomy that silently loads half its nodes would produce a
            dataset with silent holes.
    """
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"{path}: expected a YAML mapping, got {type(raw).__name__}")
    try:
        return Taxonomy.model_validate(raw)
    except ValidationError as exc:
        details = "; ".join(
            f"{'.'.join(str(part) for part in error['loc']) or '<root>'}: {error['msg']}"
            for error in exc.errors()
        )
        raise ValueError(f"{path}: {details}") from exc


def check_taxonomy(taxonomy: Taxonomy) -> TaxonomyReport:
    """Check the count range and branch coverage the plan specifies."""
    report = TaxonomyReport(
        nodes=len(taxonomy.nodes),
        branches={branch: len(nodes) for branch, nodes in taxonomy.branches.items()},
        approved=taxonomy.approved,
    )

    if not MIN_NODES <= report.nodes <= MAX_NODES:
        report.findings.append(
            Finding(
                "<count>",
                f"{report.nodes} nodes, outside the {MIN_NODES}-{MAX_NODES} range: "
                "fewer is thin coverage, more spreads the generation budget too thin",
            )
        )

    missing = [branch for branch in REQUIRED_BRANCHES if branch not in report.branches]
    if missing:
        report.findings.append(
            Finding("<branches>", f"missing required branch(es): {', '.join(missing)}")
        )
    for branch, count in sorted(report.branches.items()):
        if count < 2:
            report.findings.append(
                Finding(branch, f"only {count} node(s): a branch that thin is not a branch")
            )
    return report


def check_retrievable(
    taxonomy: Taxonomy, documents: Iterable[CorpusDocument], *, min_passages: int = 5
) -> list[Finding]:
    """Report nodes whose keywords retrieve too few corpus passages.

    Generation samples 5-20 passages per node, so a node that retrieves fewer cannot be
    grounded — and §3.2 rejects ungrounded examples, so those nodes would simply produce
    nothing. Finding that out here costs a command; finding it out during generation costs the
    API spend for every other node in the batch.

    Matching is deliberately crude (case-folded substring over the normalized text): the real
    sampler will use embeddings, and this is a *coverage smoke test*, not a retriever.
    """
    corpus = [normalize_text(document.text).casefold() for document in documents]
    findings: list[Finding] = []
    for node in taxonomy.nodes:
        needles = [keyword.casefold() for keyword in node.keywords]
        hits = sum(1 for text in corpus if any(needle in text for needle in needles))
        if hits < min_passages:
            findings.append(
                Finding(
                    node.id,
                    f"keywords retrieve {hits} passage(s), fewer than the {min_passages} "
                    "needed to ground a node",
                )
            )
    return findings


def require_approved(taxonomy: Taxonomy) -> None:
    """Gate the generator on PO approval.

    Raises:
        NotApprovedError: while ``approved`` is false. The node list decides what the model
            knows, and arguing about a YAML file is far cheaper than regenerating 12,000
            examples.
    """
    if not taxonomy.approved:
        raise NotApprovedError(
            "the taxonomy is not approved: set approved: true (with approved_by) in "
            "configs/taxonomy.yaml once the PO has reviewed the node list (M2.01)"
        )


def render(report: TaxonomyReport, path: Path) -> str:
    """Human-readable summary."""
    status = "approved" if report.approved else "⚠ NOT APPROVED (M2.01 is a PO gate)"
    lines = [
        f"taxonomy: {path} — {report.nodes} nodes, {len(report.branches)} branches [{status}]",
        "  " + ", ".join(f"{branch}={count}" for branch, count in sorted(report.branches.items())),
    ]
    for finding in report.findings:
        lines.append(f"  ✗ {finding.locator}: {finding.reason}")
    for finding in report.unretrievable[:20]:
        lines.append(f"  ⚠ {finding.locator}: {finding.reason}")
    if len(report.unretrievable) > 20:
        lines.append(f"  … and {len(report.unretrievable) - 20} more thin nodes")
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point. Exit 0 when the taxonomy is structurally sound."""
    parser = argparse.ArgumentParser(
        description="Validate the generation taxonomy, and optionally check that every node "
        "can be grounded against a corpus."
    )
    parser.add_argument("path", type=Path, help="configs/taxonomy.yaml")
    parser.add_argument(
        "--corpus", type=Path, nargs="*", default=[], help="corpus JSONL to check grounding"
    )
    parser.add_argument(
        "--min-passages",
        type=int,
        default=5,
        help="passages a node must retrieve to be groundable (default 5)",
    )
    parser.add_argument(
        "--require-approved",
        action="store_true",
        help="also fail while the taxonomy is unapproved (what the generator does)",
    )
    args = parser.parse_args(argv)

    for path in [args.path, *args.corpus]:
        if not path.is_file():
            print(f"error: no such file: {path}", file=sys.stderr)
            return 1

    try:
        taxonomy = load_taxonomy(args.path)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    report = check_taxonomy(taxonomy)
    if args.corpus:
        documents = [
            CorpusDocument.model_validate_json(line)
            for path in args.corpus
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        report.unretrievable = check_retrievable(
            taxonomy, documents, min_passages=args.min_passages
        )

    print(render(report, args.path))
    if not report.ok:
        return 1
    if args.require_approved:
        try:
            require_approved(taxonomy)
        except NotApprovedError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
