"""Publishing the dataset to Hugging Face — PLAN M2.11.

M1.09 publishes the corpus and the licence rule there is direct: a document carries a licence, and
a ``no-redistribute`` document never enters a public artifact. The dataset breaks that directness,
because **a §3.2 example has no licence of its own**. What it has is ``grounding_ids``, and the
generator was instructed to answer *from* those passages — so an example grounded in a
``no-redistribute`` document is a derivative of text the project is not allowed to redistribute.

Three consequences, and they are the whole module:

1. **Provenance is licence.** An example's publishability is the licence of the passages it cites.
   :func:`restricted` returns the examples whose grounding includes anything non-public.
2. **Unverifiable provenance is not publishable.** An example citing a passage that is not in the
   corpus supplied cannot be shown to be clean, and "we could not check" is not a licence. Those are
   excluded exactly like restricted ones, and counted separately so the difference is visible.
3. **Without the corpus, a public drop is refused outright.** There is no way to establish
   provenance without it, and a public upload is irreversible in practice — it is cached, mirrored
   and indexed. A private drop needs no such check.

**Excluding examples collides with the frozen test split**, and that collision must not be resolved
quietly. Dropping a restricted example that happens to be in ``test`` changes the test set after it
was frozen (M2.08), which breaks the comparability every Phase 4 number depends on. So the drop
**fails** and says which examples caused it: the fix is a decision (re-freeze, or re-run generation
without those passages), not something a publish step should make on someone's behalf.

Exclusion also moves the §3.2 type shares, so those are re-checked on **what is actually being
published** rather than on what was validated earlier.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from maia.corpus.publish import (
    DatasetHub,
    RestrictedContentError,
    StaleStagingError,
    hf_hub,
)

# Re-exported explicitly for `mypy --strict`; the definition lives in `maia.licensing`.
from maia.licensing import DATASET_LICENSE as DATASET_LICENSE
from maia.schemas import CorpusDocument, DatasetExample, License, Split
from maia.synth.distribution import TYPE_BANDS, Profile, profile
from maia.synth.distribution import render as render_profile
from maia.synth.pilot import dataset_digest
from maia.synth.splits import read_freeze
from maia.synth.validate import split_digest

#: The §3.2 version this drop conforms to.
SCHEMA_VERSION = "3.2"

#: What each §3.2 split is called on the Hub. Ours is ``val``; the Hub's convention — and what
#: ``datasets`` looks for — is ``validation``, so the published name is not simply ``split.value``.
HUB_SPLIT_NAMES = {Split.TRAIN: "train", Split.VAL: "validation", Split.TEST: "test"}

#: One file per split, the layout Hugging Face recognises without configuration.
SPLIT_FILES = {split: f"data/{name}.jsonl" for split, name in HUB_SPLIT_NAMES.items()}

#: Re-exported from :mod:`maia.licensing` — see there for why it is CC-BY-SA-4.0 and why it is
#: defined once.


class FrozenTestSplitError(RuntimeError):
    """Raised when a drop would publish a test split different from the frozen one."""


def licences_of(
    example: DatasetExample, corpus: Mapping[str, CorpusDocument]
) -> tuple[set[str], list[str]]:
    """``(licences of the passages this example cites, ids not found in the corpus)``."""
    found: set[str] = set()
    missing: list[str] = []
    for ident in example.grounding_ids:
        document = corpus.get(ident)
        if document is None:
            missing.append(ident)
        else:
            found.add(document.license.value)
    return found, missing


def restricted(
    examples: Iterable[DatasetExample], corpus: Mapping[str, CorpusDocument]
) -> list[DatasetExample]:
    """Examples grounded in text that may not be redistributed.

    Provenance is licence: the example itself carries none, so its publishability is that of the
    passages it was generated from.
    """
    return [
        example
        for example in examples
        if any(not License(value).is_public() for value in licences_of(example, corpus)[0])
    ]


def untraceable(
    examples: Iterable[DatasetExample], corpus: Mapping[str, CorpusDocument]
) -> list[DatasetExample]:
    """Examples citing passages the supplied corpus does not contain.

    Kept separate from :func:`restricted` because the reason differs: this is not "we know it is
    restricted" but "we cannot show it is not", and only one of those is a data-cleaning problem.
    Both are excluded — "we could not check" is not a licence.
    """
    return [example for example in examples if licences_of(example, corpus)[1]]


@dataclass(frozen=True)
class DatasetManifest:
    """What a dataset drop contains — written alongside the data."""

    repo_id: str
    private: bool
    schema_version: str
    examples: int
    by_split: dict[str, int]
    by_type: dict[str, int]
    test_digest: str
    dataset_digest: str
    excluded_restricted: int = 0
    excluded_untraceable: int = 0
    files: dict[str, int] = field(default_factory=dict)

    @property
    def type_violations(self) -> list[str]:
        """§3.2 shares broken by **what is being published**.

        Withholding examples moves the distribution, so the shares that were validated before
        exclusion are not the shares going out. A public drop that breaks them is publishing a
        dataset the project's own schema calls invalid.
        """
        return [
            f"{kind.value} is {self.by_type.get(kind.value, 0) / self.examples:.1%}, outside "
            f"§3.2's {low:.0%}-{high:.0%}"
            for kind, (low, high) in TYPE_BANDS.items()
            if self.examples and not low <= self.by_type.get(kind.value, 0) / self.examples <= high
        ]

    def to_json(self) -> str:
        """The manifest, for committing beside the data."""
        return json.dumps(
            {
                "repo_id": self.repo_id,
                "private": self.private,
                "schema_version": self.schema_version,
                "examples": self.examples,
                "by_split": dict(sorted(self.by_split.items())),
                "by_type": dict(sorted(self.by_type.items())),
                "test_digest": self.test_digest,
                "dataset_digest": self.dataset_digest,
                "excluded_restricted": self.excluded_restricted,
                "excluded_untraceable": self.excluded_untraceable,
                "type_violations": self.type_violations,
                "files": dict(sorted(self.files.items())),
            },
            ensure_ascii=False,
            indent=2,
        )


def publishable(
    examples: Sequence[DatasetExample],
    corpus: Mapping[str, CorpusDocument] | None,
    *,
    private: bool,
    frozen_test_digest: str | None = None,
) -> tuple[list[DatasetExample], list[DatasetExample], list[DatasetExample]]:
    """Split ``examples`` into ``(publishable, restricted, untraceable)``.

    A private drop publishes everything: the repo is not a public artifact, and the restricted text
    is exactly what makes the private drop useful for RAG.

    Raises:
        RestrictedContentError: for a public drop with no corpus — provenance cannot be established
            and a public upload is irreversible in practice.
        FrozenTestSplitError: if exclusion would change the frozen test split. Publishing a test set
            different from the frozen one breaks the comparability every Phase 4 number rests on,
            and choosing how to resolve that is not a publish step's decision.
    """
    if private:
        return list(examples), [], []
    if corpus is None:
        raise RestrictedContentError(
            "a public drop needs the corpus to establish provenance: a §3.2 example carries no "
            "licence of its own, only the grounding it was generated from, and an unchecked "
            "public upload cannot be taken back"
        )

    blocked = {str(example.id) for example in restricted(examples, corpus)}
    unknown = {str(example.id) for example in untraceable(examples, corpus)}
    excluded = blocked | unknown
    kept = [example for example in examples if str(example.id) not in excluded]

    if frozen_test_digest is not None:
        removed_from_test = sorted(
            str(example.id)
            for example in examples
            if example.split is Split.TEST and str(example.id) in excluded
        )
        if removed_from_test:
            raise FrozenTestSplitError(
                f"{len(removed_from_test)} test example(s) cannot be published "
                f"(e.g. {removed_from_test[0]}), so the published test split would differ from the "
                f"frozen one ({frozen_test_digest[:16]}...) and Phase 4 numbers would no longer be "
                "comparable. Re-freeze deliberately, or re-run generation without those passages"
            )
        actual = split_digest(kept, Split.TEST)
        if actual != frozen_test_digest:
            raise FrozenTestSplitError(
                f"the test split to be published digests to {actual[:16]}... but "
                f"{frozen_test_digest[:16]}... was frozen — the test set changed since M2.08"
            )

    return (
        kept,
        [example for example in examples if str(example.id) in blocked],
        [example for example in examples if str(example.id) in unknown],
    )


def dataset_card(
    manifest: DatasetManifest, measured: Profile, *, name: str = "MAIA dataset"
) -> str:
    """The Hugging Face dataset card (``README.md``).

    The YAML front matter is what makes the dataset browsable and filterable on the Hub; the body is
    M2.09's distribution report, because that is already the evidence and writing a second
    description would let the two disagree.
    """
    front = [
        "---",
        f"license: {DATASET_LICENSE}",
        "language:",
        "  - ca",
        "task_categories:",
        "  - text-generation",
        "  - question-answering",
        "pretty_name: " + name,
        "size_categories:",
        f"  - {_size_category(manifest.examples)}",
        "configs:",
        "  - config_name: default",
        "    data_files:",
    ]
    for split, path in SPLIT_FILES.items():
        if manifest.by_split.get(split.value):
            front += [f"      - split: {HUB_SPLIT_NAMES[split]}", f"        path: {path}"]
    front.append("---")

    body = [
        "",
        f"# {name}",
        "",
        "Instruction dataset in Catalan about Andorra, generated by **grounded distillation**: "
        "every example was produced from real passages of the "
        "[MAIA corpus](https://huggingface.co/datasets) and cites them in `grounding_ids`.",
        "",
        "## Provenance and licensing",
        "",
        f"- Schema: §{manifest.schema_version}. Each example carries its `grounding_ids`, so any "
        "answer can be traced back to the corpus passages it was generated from.",
        "- The **test split is frozen** and its digest is committed: "
        f"`{manifest.test_digest}`. It is never trained on.",
    ]
    if manifest.excluded_restricted or manifest.excluded_untraceable:
        body.append(
            f"- {manifest.excluded_restricted} example(s) were **withheld** from this public drop "
            "because they are grounded in text that may not be redistributed, and "
            f"{manifest.excluded_untraceable} because their grounding could not be verified "
            "against the corpus. This dataset is therefore a subset of the one used internally."
        )
    body += [
        "",
        "## Intended use and limits",
        "",
        "- Built to fine-tune a Catalan model on Andorran institutions, law, geography and "
        "culture.",
        "- The spoken subcorpora were used for **register and lexicon only**, never to imitate an "
        "identifiable person.",
        "- Generated by a frontier model and filtered automatically; a human sample was reviewed "
        "(DoD-F2) but every example was not. Treat it as training data, not as a reference source.",
        "- `no_ho_se` examples deliberately teach the model to decline. They are correct answers.",
        "",
        render_profile(measured, name=manifest.repo_id),
    ]
    return "\n".join([*front, *body])


def _size_category(examples: int) -> str:
    """The Hub's size bucket for ``examples``."""
    for ceiling, label in ((1_000, "n<1K"), (10_000, "1K<n<10K"), (100_000, "10K<n<100K")):
        if examples < ceiling:
            return label
    return "100K<n<1M"


def stage(
    examples: Sequence[DatasetExample],
    staging_dir: Path,
    *,
    repo_id: str,
    private: bool = True,
    corpus: Mapping[str, CorpusDocument] | None = None,
    frozen_test_digest: str | None = None,
    measured: Profile | None = None,
    reuse_dir: bool = False,
) -> DatasetManifest:
    """Write the drop to ``staging_dir`` and return its manifest.

    Raises:
        StaleStagingError: if the directory already holds data from an earlier drop. The hub client
            commits the **whole folder**, so a leftover file from a private drop would ride along
            into a public one — the D-0016 finding, in the same shape.
    """
    staging_dir.mkdir(parents=True, exist_ok=True)
    existing = sorted(
        path
        for path in staging_dir.rglob("*")
        if path.is_file() and path.suffix in {".jsonl", ".json", ".md"}
    )
    if existing and not reuse_dir:
        raise StaleStagingError(
            f"{staging_dir} already holds {len(existing)} file(s) from an earlier drop "
            f"(e.g. {existing[0].name}); the hub commits the whole folder, so those would be "
            "published too. Pass reuse_dir=True to clear it"
        )
    for path in existing:
        path.unlink()

    kept, blocked, unknown = publishable(
        examples, corpus, private=private, frozen_test_digest=frozen_test_digest
    )

    files: dict[str, int] = {}
    for split, relative in SPLIT_FILES.items():
        rows = [example for example in kept if example.split is split]
        if not rows:
            continue
        target = staging_dir / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("".join(f"{row.model_dump_json()}\n" for row in rows), encoding="utf-8")
        files[relative] = len(rows)

    manifest = DatasetManifest(
        repo_id=repo_id,
        private=private,
        schema_version=SCHEMA_VERSION,
        examples=len(kept),
        by_split=dict(Counter(example.split.value for example in kept)),
        by_type=dict(Counter(example.type.value for example in kept)),
        test_digest=split_digest(kept, Split.TEST),
        dataset_digest=dataset_digest(kept),
        excluded_restricted=len(blocked),
        excluded_untraceable=len(unknown),
        files=files,
    )
    (staging_dir / "manifest.json").write_text(manifest.to_json(), encoding="utf-8")
    (staging_dir / "README.md").write_text(
        dataset_card(manifest, measured or profile(kept)), encoding="utf-8"
    )
    return manifest


def verify_staged(staging_dir: Path, manifest: DatasetManifest) -> list[str]:
    """Re-read the staged files and report anything that disagrees with the manifest.

    Also refuses **any** ``.jsonl`` the manifest does not describe: the hub commits the folder, not
    the manifest, so a file nobody accounted for is a file nobody checked.
    """
    problems: list[str] = []
    seen = 0
    for relative, expected in manifest.files.items():
        path = staging_dir / relative
        if not path.is_file():
            problems.append(f"{relative}: staged file is missing")
            continue
        rows = [
            DatasetExample.model_validate_json(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        seen += len(rows)
        if len(rows) != expected:
            problems.append(
                f"{relative}: manifest says {expected} example(s), file holds {len(rows)}"
            )
    if seen != manifest.examples:
        problems.append(f"manifest says {manifest.examples} example(s), staged files hold {seen}")

    described = {staging_dir / relative for relative in manifest.files}
    for path in sorted(staging_dir.rglob("*.jsonl")):
        if path not in described:
            problems.append(
                f"{path.relative_to(staging_dir)}: on disk but not in the manifest — it would be "
                "published unchecked"
            )
    return problems


def upload_dataset(
    examples: Sequence[DatasetExample],
    hub: DatasetHub,
    staging_dir: Path,
    *,
    repo_id: str,
    private: bool = True,
    corpus: Mapping[str, CorpusDocument] | None = None,
    frozen_test_digest: str | None = None,
    measured: Profile | None = None,
    commit_message: str | None = None,
    reuse_dir: bool = False,
) -> DatasetManifest:
    """Stage, verify, then commit the dataset to a Hub repo.

    ``private`` defaults to ``True`` for the same reason as M1.09: a public drop must be asked for
    explicitly *and* survive the provenance check.
    """
    manifest = stage(
        examples,
        staging_dir,
        repo_id=repo_id,
        private=private,
        corpus=corpus,
        frozen_test_digest=frozen_test_digest,
        measured=measured,
        reuse_dir=reuse_dir,
    )
    problems = verify_staged(staging_dir, manifest)
    if problems:
        raise RuntimeError(
            "staged dataset does not verify:\n" + "\n".join(f"  {problem}" for problem in problems)
        )
    if not private and manifest.type_violations:
        raise RestrictedContentError(
            "this public drop breaks §3.2 after withholding restricted examples:\n"
            + "\n".join(f"  {violation}" for violation in manifest.type_violations)
            + "\n  publishing a dataset the project's own schema calls invalid is not a caveat"
        )

    hub.create_repo(repo_id, repo_type="dataset", private=private, exist_ok=True)
    hub.upload_folder(
        repo_id=repo_id,
        folder_path=str(staging_dir),
        repo_type="dataset",
        commit_message=commit_message
        or f"dataset drop: {manifest.examples} examples, schema §{SCHEMA_VERSION}",
    )
    return manifest


def render(manifest: DatasetManifest) -> str:
    """Human-readable summary of a drop."""
    lines = [
        f"repo: {manifest.repo_id} ({'private' if manifest.private else 'PUBLIC'})",
        f"  examples: {manifest.examples}  schema: §{manifest.schema_version}",
        "  by split: " + ", ".join(f"{k}={v}" for k, v in sorted(manifest.by_split.items())),
        f"  test digest: {manifest.test_digest}",
        f"  dataset digest: {manifest.dataset_digest}",
    ]
    if manifest.excluded_restricted:
        lines.append(
            f"  withheld: {manifest.excluded_restricted} example(s) grounded in "
            "no-redistribute text"
        )
    if manifest.excluded_untraceable:
        lines.append(
            f"  withheld: {manifest.excluded_untraceable} example(s) whose grounding is not in "
            "the corpus supplied — provenance unverifiable"
        )
    lines.append("  files: " + ", ".join(f"{k}={v}" for k, v in sorted(manifest.files.items())))
    for violation in manifest.type_violations:
        lines.append(f"  ✗ {violation}")
    return "\n".join(lines)


def read_dataset(path: Path) -> list[DatasetExample]:
    """Read a §3.2 dataset from JSONL."""
    return [
        DatasetExample.model_validate_json(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def read_corpus(paths: Sequence[Path]) -> dict[str, CorpusDocument]:
    """Index §3.1 corpus documents by id."""
    return {
        document.id: document
        for path in paths
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
        for document in [CorpusDocument.model_validate_json(line)]
    }


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point.

    Private by default; ``--public`` needs ``--corpus`` and has to survive the provenance check.
    """
    parser = argparse.ArgumentParser(
        description="Publish the §3.2 dataset to a Hugging Face dataset repo (M2.11). A public "
        "drop withholds every example grounded in no-redistribute text, and refuses to run at all "
        "without the corpus needed to establish that."
    )
    parser.add_argument("dataset", type=Path, help="the §3.2 dataset (JSONL)")
    parser.add_argument("--repo-id", required=True, help="e.g. ericrisco/maia-dataset")
    parser.add_argument("--staging-dir", type=Path, default=Path("build/hf-dataset"))
    parser.add_argument("--corpus", type=Path, nargs="+", help="§3.1 corpus JSONL, for provenance")
    parser.add_argument("--freeze", type=Path, help="configs/test-split.freeze.json")
    parser.add_argument("--public", action="store_true", help="publish publicly (deliberate)")
    parser.add_argument("--reuse-staging-dir", action="store_true", help="clear the staging dir")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="stage and verify without touching the Hub",
    )
    args = parser.parse_args(argv)

    paths = [
        args.dataset,
        *(args.corpus or []),
        *([args.freeze] if args.freeze else []),
    ]
    for path in paths:
        if not path.is_file():
            print(f"error: no such file: {path}", file=sys.stderr)
            return 1

    examples = read_dataset(args.dataset)
    corpus = read_corpus(args.corpus) if args.corpus else None
    frozen: str | None = None

    try:
        if args.freeze:
            frozen, _ = read_freeze(args.freeze)
        if args.dry_run:
            manifest = stage(
                examples,
                args.staging_dir,
                repo_id=args.repo_id,
                private=not args.public,
                corpus=corpus,
                frozen_test_digest=frozen,
                reuse_dir=args.reuse_staging_dir,
            )
            problems = verify_staged(args.staging_dir, manifest)
            if problems:
                print("error: staged dataset does not verify:", file=sys.stderr)
                for problem in problems:
                    print(f"  {problem}", file=sys.stderr)
                return 1
        else:
            manifest = upload_dataset(
                examples,
                hf_hub(),
                args.staging_dir,
                repo_id=args.repo_id,
                private=not args.public,
                corpus=corpus,
                frozen_test_digest=frozen,
                reuse_dir=args.reuse_staging_dir,
            )
    except (
        RestrictedContentError,
        FrozenTestSplitError,
        StaleStagingError,
        RuntimeError,
        ValueError,
    ) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    print(render(manifest))
    if args.dry_run:
        print(f"  dry run: staged in {args.staging_dir}, nothing uploaded")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
