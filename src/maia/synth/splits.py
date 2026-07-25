"""Assigning the 90/5/5 splits and freezing the test set — PLAN M2.08.

*"splits 90/5/5; **test split never trained** and frozen (hash in repo)."*

M2.05's validator already **checks** splits (`check_splits`) and already knows how to freeze one
(`split_digest`, `verify_frozen`). What was missing is the thing that decides which example goes
where, and doing that by shuffling would quietly break the guarantee the freeze exists to protect.

**Examples that share a grounding passage must not be split apart.** The generator produces 5-20
examples per request from the *same* passages. Two of them are different questions about the same
paragraph; put one in ``train`` and one in ``test`` and the model is evaluated on a paragraph it was
trained on. `check_splits` cannot see this — it looks for identical *content* in two splits, and
these differ. So the unit of assignment is not the example, it is the **group**: the transitive
closure of examples linked by a shared ``grounding_id``, built with the same union-find as M1.05 and
M2.05. Ungrounded examples (``general_ca``, ``estil_andorra``) have nothing to leak and are assigned
individually.

Grouping and exact 90/5/5 pull against each other — a group is indivisible, so the sizes land near
the target rather than on it. :data:`MAX_DRIFT` matches the validator's tolerance and
:attr:`SplitReport.within_tolerance` says whether the result would pass it.

**A frozen test split is honoured, not re-shuffled.** Once a digest is committed, re-splitting must
leave every frozen example in ``test`` and must never move a frozen example into ``train`` — that is
the whole point of freezing it. :func:`assign_splits` takes the frozen ids and pins them, and
:func:`freeze` writes the file that gets committed.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from random import Random

from maia.corpus.dedup import UnionFind
from maia.schemas import DatasetExample, ExampleType, Split
from maia.synth.validate import SPLIT_TARGETS, SPLIT_TOLERANCE, split_digest

#: The plan's proportions, reused from the validator so the two cannot disagree.
TARGETS = SPLIT_TARGETS

#: How far a split may sit from its target. Groups are indivisible, so exactness is not available;
#: this is the validator's own tolerance, so anything within it passes M2.05 too.
MAX_DRIFT = SPLIT_TOLERANCE

#: Filename convention for the committed freeze.
DEFAULT_FREEZE = Path("configs/test-split.freeze.json")


class FrozenSplitError(RuntimeError):
    """Raised when an assignment would move an example out of a frozen test split."""


def group_key(example: DatasetExample) -> str:
    """The union-find key for one example."""
    return str(example.id)


def grounding_groups(examples: Sequence[DatasetExample]) -> list[list[str]]:
    """Group example ids by shared grounding passage, transitively.

    Two examples generated from one passage are two views of the same information. Splitting them
    is leakage that no content-equality check can see, so they travel together.

    Ungrounded examples form singleton groups: they cite nothing, so they can leak nothing.
    """
    forest = UnionFind()
    first_for_passage: dict[str, str] = {}
    order = [group_key(example) for example in examples]
    for example in examples:
        key = group_key(example)
        forest.find(key)
        for passage in example.grounding_ids:
            anchor = first_for_passage.setdefault(passage, key)
            forest.union(anchor, key)
    rank = {key: index for index, key in enumerate(order)}
    groups = [sorted(members, key=lambda key: rank[key]) for members in forest.groups().values()]
    return sorted(groups, key=lambda members: rank[members[0]])


@dataclass
class SplitReport:
    """What the assignment produced."""

    total: int = 0
    groups: int = 0
    largest_group: int = 0
    frozen_kept: int = 0
    counts: dict[Split, int] = field(default_factory=dict)
    by_type: dict[Split, Counter[str]] = field(default_factory=dict)

    def share(self, split: Split) -> float:
        """Realised share of one split."""
        return self.counts.get(split, 0) / self.total if self.total else 0.0

    def drift(self, split: Split) -> float:
        """How far one split sits from its target."""
        return self.share(split) - TARGETS[split]

    @property
    def within_tolerance(self) -> bool:
        """Whether every split is inside :data:`MAX_DRIFT` — i.e. would pass M2.05."""
        return all(abs(self.drift(split)) <= MAX_DRIFT for split in TARGETS)

    @property
    def worst(self) -> tuple[Split, float]:
        """The split furthest from its target."""
        return max(((split, self.drift(split)) for split in TARGETS), key=lambda item: abs(item[1]))


def assign_splits(
    examples: Sequence[DatasetExample],
    *,
    seed: int,
    frozen_test_ids: Iterable[str] = (),
) -> tuple[list[DatasetExample], SplitReport]:
    """Assign every example to ``train`` / ``val`` / ``test``, keeping groups intact.

    Groups are shuffled reproducibly, then placed largest-first into whichever split is furthest
    below its quota. Largest-first because a big group placed last can only overshoot, and the
    drift is what has to stay small.

    Raises:
        FrozenSplitError: if a frozen id is not in ``examples``. A freeze that names an example the
            dataset no longer contains means the test set was edited, and silently re-splitting
            around the gap would hide it.
    """
    frozen = set(frozen_test_ids)
    known = {group_key(example) for example in examples}
    lost = frozen - known
    if lost:
        raise FrozenSplitError(
            f"{len(lost)} frozen test example(s) are not in this dataset (e.g. {sorted(lost)[0]}) "
            "— the test split was edited; re-freezing is a deliberate act, not a side effect"
        )

    groups = grounding_groups(examples)
    report = SplitReport(
        total=len(examples),
        groups=len(groups),
        largest_group=max((len(group) for group in groups), default=0),
    )

    assignment: dict[str, Split] = {}
    placed = dict.fromkeys(TARGETS, 0)

    # A group holding any frozen example goes to test whole: the frozen ones must stay, and the
    # rest of their group shares grounding with them, so putting those in train is the leak.
    remaining: list[list[str]] = []
    for group in groups:
        if frozen.intersection(group):
            for key in group:
                assignment[key] = Split.TEST
            placed[Split.TEST] += len(group)
            report.frozen_kept += len(frozen.intersection(group))
        else:
            remaining.append(group)

    rng = Random(seed)
    rng.shuffle(remaining)
    remaining.sort(key=len, reverse=True)

    for group in remaining:
        target = min(TARGETS, key=lambda split: placed[split] - TARGETS[split] * len(examples))
        for key in group:
            assignment[key] = target
        placed[target] += len(group)

    assigned = [
        example.model_copy(update={"split": assignment[group_key(example)]}) for example in examples
    ]
    report.counts = dict(placed)
    report.by_type = {
        split: Counter(example.type.value for example in assigned if example.split is split)
        for split in TARGETS
    }
    return assigned, report


def freeze(examples: Iterable[DatasetExample], *, version: str) -> str:
    """The freeze file's contents: the digest, the ids, and how many there are.

    The ids are committed alongside the digest so a later mismatch can say *which* examples moved
    rather than only that something did.
    """
    test = sorted(str(example.id) for example in examples if example.split is Split.TEST)
    return json.dumps(
        {
            "version": version,
            "split": Split.TEST.value,
            "count": len(test),
            "digest": split_digest(examples, Split.TEST),
            "ids": test,
        },
        indent=2,
    )


def read_freeze(path: Path) -> tuple[str, list[str]]:
    """Read a freeze file. Returns ``(digest, ids)``.

    Raises:
        ValueError: if the file is not a freeze. A run that cannot read the freeze must not proceed
            as though nothing were frozen.
    """
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or "digest" not in payload or "ids" not in payload:
        raise ValueError(f"{path}: not a test-split freeze (needs 'digest' and 'ids')")
    ids = payload["ids"]
    if not isinstance(ids, list) or not all(isinstance(item, str) for item in ids):
        raise ValueError(f"{path}: 'ids' must be a list of strings")
    if len(ids) != payload.get("count", len(ids)):
        raise ValueError(
            f"{path}: says count={payload['count']} but lists {len(ids)} id(s) — the file was "
            "edited by hand"
        )
    return str(payload["digest"]), ids


def render(report: SplitReport) -> str:
    """Human-readable summary of an assignment."""
    status = "✓" if report.within_tolerance else "✗"
    lines = [
        f"{status} splits over {report.total} example(s) in {report.groups} grounding group(s) "
        f"(largest {report.largest_group})"
    ]
    for split in (Split.TRAIN, Split.VAL, Split.TEST):
        mark = "✓" if abs(report.drift(split)) <= MAX_DRIFT else "✗"
        lines.append(
            f"  {mark} {split.value}: {report.counts.get(split, 0)} "
            f"({report.share(split):.1%}, target {TARGETS[split]:.0%}, "
            f"drift {report.drift(split):+.1%})"
        )
    if report.frozen_kept:
        lines.append(f"  {report.frozen_kept} frozen test example(s) kept in place")
    if not report.within_tolerance:
        split, drift = report.worst
        lines.append(
            f"  ✗ {split.value} is {abs(drift):.1%} from target, over the {MAX_DRIFT:.0%} "
            "tolerance — grounding groups are indivisible, so a few very large groups can make "
            "90/5/5 unreachable; check the largest group above"
        )
    for split in (Split.VAL, Split.TEST):
        missing = sorted(
            kind.value
            for kind in ExampleType
            if report.by_type.get(Split.TRAIN, Counter()).get(kind.value)
            and not report.by_type.get(split, Counter()).get(kind.value)
        )
        if missing:
            lines.append(
                f"  ⚠ {split.value} contains no {', '.join(missing)} example(s), so that type is "
                "unmeasured there"
            )
    return "\n".join(lines)


def read_dataset(path: Path) -> list[DatasetExample]:
    """Read a §3.2 dataset from JSONL."""
    return [
        DatasetExample.model_validate_json(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point. Exit non-zero when the assignment would not pass M2.05's tolerance."""
    parser = argparse.ArgumentParser(
        description="Assign 90/5/5 splits keeping grounding groups intact (M2.08), and write the "
        "freeze file that commits the test split."
    )
    parser.add_argument("dataset", type=Path, help="the §3.2 dataset (JSONL)")
    parser.add_argument("--out", type=Path, help="write the split dataset here")
    parser.add_argument(
        "--freeze",
        type=Path,
        help=f"read an existing freeze and honour it (conventionally {DEFAULT_FREEZE})",
    )
    parser.add_argument(
        "--write-freeze",
        type=Path,
        help="write a new freeze file for the resulting test split — a deliberate act",
    )
    parser.add_argument("--version", default="1", help="version recorded in the freeze file")
    parser.add_argument("--seed", type=int, default=20260725)
    args = parser.parse_args(argv)

    for path in (args.dataset, *([args.freeze] if args.freeze else ())):
        if not path.is_file():
            print(f"error: no such file: {path}", file=sys.stderr)
            return 1

    examples = read_dataset(args.dataset)
    frozen_ids: list[str] = []
    try:
        if args.freeze:
            _, frozen_ids = read_freeze(args.freeze)
        assigned, report = assign_splits(examples, seed=args.seed, frozen_test_ids=frozen_ids)
    except (ValueError, FrozenSplitError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(
            "".join(f"{example.model_dump_json()}\n" for example in assigned), encoding="utf-8"
        )
    if args.write_freeze:
        args.write_freeze.parent.mkdir(parents=True, exist_ok=True)
        args.write_freeze.write_text(freeze(assigned, version=args.version), encoding="utf-8")
        print(f"wrote freeze to {args.write_freeze} — commit it")

    print(render(report))
    return 0 if report.within_tolerance else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
