"""Corpus → parquet → private Hugging Face dataset — PLAN M1.09.

Takes the consolidated corpus (M1.08) and stages it for upload: one **parquet** file per
source under ``data/``, a manifest describing exactly what is in the drop, and a commit to a
**private** HF dataset repo. Parquet rather than JSONL because the corpus is a data contract:
an explicit, typed, columnar schema (:func:`corpus_schema`) means a consumer cannot silently
read a mistyped column, and HF's dataset viewer loads it natively.

Two safety controls, both enforced in code rather than by procedure:

* **A no-redistribute document can never be staged into a public repo.** The corpus legally
  *may* contain restricted text (BOPA as grounding, press, RTVA), and this drop is private
  precisely so it can. :func:`upload_corpus` therefore refuses to run against a
  non-private repo whenever restricted documents are present, naming them. This is the wall
  between "grounding-only" and "published" that F6/M6.01 checks at the far end — checking it
  here too means a mistake costs a failed command, not a retraction.
* **Every document is re-validated against §3.1 on the way in.** Consolidation produces
  valid documents, but this is the last step before an artifact leaves the machine, and it is
  cheap to prove rather than assume.

The upload itself is **blocked-by-resource**: it needs an ``HF_TOKEN`` with write scope and
network. :class:`DatasetHub` is the seam — :func:`hf_hub` wires the real
``huggingface_hub.HfApi``, and the tests drive a recording fake, so staging, schema, manifest
and every refusal are verified offline.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

import pyarrow as pa
import pyarrow.parquet as pq

from maia.corpus.consolidate import ConsolidationReport, read_documents
from maia.corpus.validate import ValidationReport
from maia.schemas import CorpusDocument, License

#: Bumped whenever :func:`corpus_schema` changes shape — consumers pin against it.
SCHEMA_VERSION = "3.1"

#: Where the parquet files live inside the dataset repo. HF's loader treats every parquet
#: under this prefix as one ``train`` split; the per-source split stays visible as a column
#: *and* as a filename, so a source can be dropped from the drop by deleting one file.
DATA_PREFIX = "data"

MANIFEST_NAME = "corpus_manifest.json"


def corpus_schema() -> pa.Schema:
    """The explicit parquet schema for §3.1 documents.

    Written out rather than inferred: inference would type an all-null ``speaker`` column as
    null, an empty ``topic`` list as null-of-null, and a corpus without legal documents would
    get a different schema from one with them — so two drops would not concatenate.
    """
    legal = pa.struct(
        [
            pa.field("rang", pa.string(), nullable=False),
            pa.field("article", pa.string(), nullable=False),
            pa.field("consolidacio_data", pa.date32(), nullable=False),
            pa.field("llei", pa.string(), nullable=True),
        ]
    )
    return pa.schema(
        [
            pa.field("id", pa.string(), nullable=False),
            pa.field("text", pa.string(), nullable=False),
            pa.field("source", pa.string(), nullable=False),
            pa.field("url", pa.string(), nullable=False),
            pa.field("fetched_at", pa.timestamp("us", tz="UTC"), nullable=False),
            pa.field("lang", pa.string(), nullable=False),
            pa.field("topic", pa.list_(pa.string()), nullable=False),
            pa.field("license", pa.string(), nullable=False),
            pa.field("registre", pa.string(), nullable=False),
            pa.field("speaker", pa.string(), nullable=True),
            pa.field("legal", legal, nullable=True),
        ],
        metadata={"maia_schema_version": SCHEMA_VERSION},
    )


def to_record(doc: CorpusDocument) -> dict[str, object]:
    """One §3.1 document as a parquet row."""
    return {
        "id": doc.id,
        "text": doc.text,
        "source": doc.source.value,
        "url": str(doc.url),
        "fetched_at": doc.fetched_at,
        "lang": doc.lang,
        "topic": list(doc.topic),
        "license": doc.license.value,
        "registre": doc.registre.value,
        "speaker": doc.speaker,
        "legal": (
            None
            if doc.legal is None
            else {
                "rang": doc.legal.rang.value,
                "article": doc.legal.article,
                "consolidacio_data": doc.legal.consolidacio_data,
                "llei": doc.legal.llei,
            }
        ),
    }


def write_parquet(documents: Iterable[CorpusDocument], path: Path) -> int:
    """Write documents to one parquet file. Returns the row count."""
    records = [to_record(doc) for doc in documents]
    table = pa.Table.from_pylist(records, schema=corpus_schema())
    path.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(table, path, compression="zstd")
    return int(table.num_rows)


def read_parquet(path: Path) -> list[CorpusDocument]:
    """Read a corpus parquet file back into §3.1 documents.

    The round-trip is the point: it proves the drop is readable and still schema-valid, which
    is the F1 exit criterion ("validator green, 0 errors") stated about the *uploaded* thing.
    """
    table = pq.read_table(path)
    return [CorpusDocument.model_validate(row) for row in table.to_pylist()]


@dataclass(frozen=True)
class Manifest:
    """What a drop contains — committed alongside the parquet."""

    repo_id: str
    private: bool
    schema_version: str
    documents: int
    by_source: dict[str, int]
    by_license: dict[str, int]
    files: dict[str, int] = field(default_factory=dict)

    @property
    def no_redistribute(self) -> int:
        """Documents that must never reach a public artifact."""
        return self.by_license.get(License.NO_REDISTRIBUTE.value, 0)

    def to_json(self) -> str:
        return json.dumps(
            {
                "repo_id": self.repo_id,
                "private": self.private,
                "schema_version": self.schema_version,
                "documents": self.documents,
                "by_source": dict(sorted(self.by_source.items())),
                "by_license": dict(sorted(self.by_license.items())),
                "files": dict(sorted(self.files.items())),
                "no_redistribute": self.no_redistribute,
            },
            ensure_ascii=False,
            indent=2,
        )


class DatasetHub(Protocol):
    """The slice of ``huggingface_hub.HfApi`` this module needs."""

    def create_repo(self, repo_id: str, *, repo_type: str, private: bool, exist_ok: bool) -> object:
        """Create (or accept the existence of) a dataset repo."""

    def upload_folder(
        self, *, repo_id: str, folder_path: str, repo_type: str, commit_message: str
    ) -> object:
        """Commit a local folder into the repo."""


class RestrictedContentError(RuntimeError):
    """Raised when a drop containing ``no-redistribute`` text targets a public repo."""


def restricted(documents: Iterable[CorpusDocument]) -> list[CorpusDocument]:
    """The documents in ``documents`` that may never enter a public artifact."""
    return [doc for doc in documents if not doc.license.is_public()]


def stage(
    documents: Sequence[CorpusDocument],
    staging_dir: Path,
    *,
    repo_id: str,
    private: bool = True,
) -> Manifest:
    """Write the parquet files and manifest that :func:`upload_corpus` will commit.

    Raises:
        RestrictedContentError: if ``private`` is false and any document is
            ``no-redistribute``. The corpus is allowed to hold restricted text — the private
            drop exists so it can — but it must never be staged for a public repo.
        ValueError: if ``documents`` is empty. An empty commit would look like a successful
            upload while publishing nothing.
    """
    if not documents:
        raise ValueError("refusing to stage an empty corpus")

    blocked = restricted(documents)
    if blocked and not private:
        sources = ", ".join(sorted({doc.source.value for doc in blocked}))
        raise RestrictedContentError(
            f"{len(blocked)} no-redistribute document(s) from {sources} cannot go to a "
            f"public repo ({repo_id}); they are grounding-only (ANEXO §8)"
        )

    grouped: dict[str, list[CorpusDocument]] = {}
    for doc in documents:
        grouped.setdefault(doc.source.value, []).append(doc)

    files: dict[str, int] = {}
    for source, docs in sorted(grouped.items()):
        relative = f"{DATA_PREFIX}/{source}.parquet"
        files[relative] = write_parquet(docs, staging_dir / relative)

    manifest = Manifest(
        repo_id=repo_id,
        private=private,
        schema_version=SCHEMA_VERSION,
        documents=len(documents),
        by_source=dict(Counter(doc.source.value for doc in documents)),
        by_license=dict(Counter(doc.license.value for doc in documents)),
        files=files,
    )
    (staging_dir / MANIFEST_NAME).write_text(manifest.to_json() + "\n", encoding="utf-8")
    return manifest


def verify_staged(staging_dir: Path, manifest: Manifest) -> ValidationReport:
    """Read every staged parquet back and re-validate it against §3.1.

    This is the F1 exit criterion applied to the artifact rather than to the input: whatever
    is about to be committed is proven readable and conformant first.
    """
    report = ValidationReport()
    for relative in sorted(manifest.files):
        for doc in read_parquet(staging_dir / relative):
            report.total += 1
            report.valid += 1
            report.by_source[doc.source.value] += 1
            report.by_license[doc.license.value] += 1
    return report


def upload_corpus(
    documents: Sequence[CorpusDocument],
    hub: DatasetHub,
    staging_dir: Path,
    *,
    repo_id: str,
    private: bool = True,
    commit_message: str | None = None,
) -> Manifest:
    """Stage, verify, then commit the corpus to a dataset repo.

    ``private`` defaults to ``True``: the M1.09 drop is private by design, and a public drop
    has to be asked for explicitly *and* survive the restricted-content check.
    """
    manifest = stage(documents, staging_dir, repo_id=repo_id, private=private)
    report = verify_staged(staging_dir, manifest)
    if report.valid != manifest.documents:
        raise RuntimeError(
            f"staged corpus does not round-trip: wrote {manifest.documents} documents, "
            f"read back {report.valid}"
        )

    hub.create_repo(repo_id, repo_type="dataset", private=private, exist_ok=True)
    hub.upload_folder(
        repo_id=repo_id,
        folder_path=str(staging_dir),
        repo_type="dataset",
        commit_message=commit_message
        or f"corpus drop: {manifest.documents} documents, schema §{SCHEMA_VERSION}",
    )
    return manifest


def hf_hub(token: str | None = None) -> DatasetHub:
    """The real Hugging Face client (blocked-by-resource: needs ``HF_TOKEN`` + network).

    Imported lazily so the rest of the module — and all of its tests — need no HF session.
    """
    from huggingface_hub import HfApi

    api: DatasetHub = HfApi(token=token)
    return api


def render(manifest: Manifest) -> str:
    """Human-readable summary of a drop."""
    lines = [
        f"repo: {manifest.repo_id} ({'private' if manifest.private else 'PUBLIC'})",
        f"  documents: {manifest.documents}  schema: §{manifest.schema_version}",
        "  by source: " + ", ".join(f"{k}={v}" for k, v in sorted(manifest.by_source.items())),
        "  files: " + ", ".join(f"{k} ({v})" for k, v in sorted(manifest.files.items())),
    ]
    if manifest.no_redistribute:
        lines.append(
            f"  ⚠ no-redistribute (grounding-only, never public): {manifest.no_redistribute}"
        )
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point. Exit 0 on a successful drop, 1 on any refusal or failure."""
    parser = argparse.ArgumentParser(
        description="Stage a consolidated corpus as parquet and upload it to a private "
        "Hugging Face dataset repo."
    )
    parser.add_argument("inputs", type=Path, nargs="+", help="consolidated JSONL corpus files")
    parser.add_argument("--repo-id", required=True, help="e.g. ericrisco/maia-corpus")
    parser.add_argument("--staging-dir", type=Path, required=True, help="local staging directory")
    parser.add_argument(
        "--public",
        action="store_true",
        help="target a PUBLIC repo — refused if the corpus holds no-redistribute documents",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="stage and verify locally without contacting Hugging Face",
    )
    args = parser.parse_args(argv)

    missing = [path for path in args.inputs if not path.is_file()]
    if missing:
        for path in missing:
            print(f"error: no such file: {path}", file=sys.stderr)
        return 1

    report = ConsolidationReport()
    documents = read_documents(args.inputs, report)
    if report.invalid:
        print(f"error: {len(report.invalid)} input line(s) failed §3.1 validation", file=sys.stderr)
        for error in report.invalid[:20]:
            print(f"  ✗ line {error.line}: {error.reason}", file=sys.stderr)
        return 1

    private = not args.public
    try:
        if args.dry_run:
            manifest = stage(documents, args.staging_dir, repo_id=args.repo_id, private=private)
            verify_staged(args.staging_dir, manifest)
        else:
            manifest = upload_corpus(
                documents, hf_hub(), args.staging_dir, repo_id=args.repo_id, private=private
            )
    except (RestrictedContentError, ValueError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(render(manifest))
    if args.dry_run:
        print("  (dry run — nothing uploaded)")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
