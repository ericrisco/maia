"""E0: inventari determinista del snapshot d'entrada."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from cervell.model import Corpus, Doc


def git_blob_sha(data: bytes) -> str:
    """SHA-1 compatible amb l'identificador d'un blob de Git."""
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def doc_id_for(root: Path, doc: Doc) -> str:
    """Retorna la ruta relativa a la bóveda sense l'extensió Markdown."""
    return doc.path.relative_to(root).with_suffix("").as_posix()


def build_manifest(root: Path, corpus: Corpus) -> tuple[list[dict[str, str]], str]:
    """Construeix manifest i hash del snapshot sense dependre de Git o del rellotge."""
    records: list[dict[str, str]] = []
    for doc in sorted(corpus.docs, key=lambda item: doc_id_for(root, item)):
        raw = doc.path.read_bytes()
        records.append(
            {
                "doc_id": doc_id_for(root, doc),
                "ruta": doc.path.relative_to(root).as_posix(),
                "type": str(doc.data.get("type", "")),
                "sha": git_blob_sha(raw),
            }
        )
    canonical = "".join(f"{r['doc_id']}\t{r['sha']}\n" for r in records).encode("utf-8")
    maia_sha = hashlib.sha256(canonical).hexdigest()
    return records, maia_sha


def manifest_jsonl(records: list[dict[str, str]], maia_sha: str) -> str:
    """Serialitza cada entrada amb claus estables i salt de línia final."""
    lines: list[str] = []
    for record in records:
        value: dict[str, Any] = {
            "doc_id": record["doc_id"],
            "ruta": record["ruta"],
            "type": record["type"],
            "sha": record["sha"],
            "maia_sha": maia_sha,
        }
        lines.append(json.dumps(value, ensure_ascii=False, sort_keys=False, separators=(",", ":")))
    return "\n".join(lines) + ("\n" if lines else "")
