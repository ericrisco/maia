#!/usr/bin/env python3
"""Exporta variants de dades per a l'entrenament de Maia."""

from __future__ import annotations

import collections
import hashlib
import json
import random
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "training-data" / "datasets"
OUT = ROOT / "export"
SEED = 20261026


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def reserved(path: str) -> bool:
    return path in RESERVED


def git_reservations(name: str) -> set[str]:
    try:
        raw = subprocess.check_output(
            ["git", "show", f"origin/benchmark:benchmark/reserva/{name}"],
            cwd=ROOT,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        fail(f"no es pot llegir la reserva del benchmark ({name}): {exc}")
    return {line.strip() for line in raw.splitlines() if line.strip() and not line.lstrip().startswith("#")}


RESERVED = git_reservations("fitxes.txt") | git_reservations("parla.txt")


def load_all() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for path in sorted(DATA.glob("*.jsonl")):
        with path.open(encoding="utf-8") as stream:
            for line_no, line in enumerate(stream, 1):
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError as exc:
                    fail(f"JSON invàlid a {path.name}:{line_no}: {exc}")
                if not isinstance(obj, dict):
                    fail(f"línia no és un objecte a {path.name}:{line_no}")
                obj["_source_file"] = path.name
                entries.append(obj)
    return entries


def article_docs(row: dict[str, Any]) -> set[str]:
    return {d for d in row.get("documents", []) if isinstance(d, str) and d.startswith("docs/temes/")}


def validation_articles(rows: list[dict[str, Any]]) -> set[str]:
    """Mostreja aproximadament el 5% sense separar articles connectats."""
    articles = sorted({a for row in rows for a in article_docs(row)})
    parent = {a: a for a in articles}

    def find(a: str) -> str:
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a: str, b: str) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for row in rows:
        docs = sorted(article_docs(row))
        for other in docs[1:]:
            union(docs[0], other)
    components: dict[str, list[str]] = collections.defaultdict(list)
    for article in articles:
        components[find(article)].append(article)

    # La component gran no es pot tallar sense que el mateix article quedi a
    # train i valid. Cerquem per programació dinàmica un conjunt de components
    # proper al 5%, sense dividir-ne cap.
    ordered = sorted(
        components.values(),
        key=lambda group: hashlib.sha256((str(SEED) + "\0" + min(group)).encode()).digest(),
    )
    target = max(1, round(len(articles) * 0.05))
    sizes = [len(group) for group in ordered]
    reachable: dict[int, list[int]] = {0: []}
    for index, size in enumerate(sizes):
        for total, chosen in list(reachable.items()):
            new_total = total + size
            if new_total <= target and new_total not in reachable:
                reachable[new_total] = chosen + [index]
    best = max(reachable)
    selected = [article for i in reachable[best] for article in ordered[i]]
    return set(selected)


def is_reserved(row: dict[str, Any]) -> bool:
    return any(reserved(doc) for doc in row.get("documents", []) if isinstance(doc, str))


def clean_messages(row: dict[str, Any]) -> list[dict[str, str]]:
    messages = row.get("messages")
    if not isinstance(messages, list):
        fail(f"messages invàlid a {row.get('id')}")
    cleaned = [m for m in messages if not (m.get("role") == "system" and m.get("content") == "")]
    if not cleaned:
        fail(f"conversa buida a {row.get('id')}")
    for i, message in enumerate(cleaned):
        if not isinstance(message, dict) or not isinstance(message.get("role"), str) or not isinstance(message.get("content"), str):
            fail(f"missatge invàlid a {row.get('id')}")
        if not message["content"].strip():
            fail(f"missatge buit a {row.get('id')}")
        expected = "user" if i % 2 == 0 else "assistant"
        if message["role"] != expected:
            fail(f"torns no alternen a {row.get('id')}")
    if cleaned[0]["role"] != "user" or cleaned[-1]["role"] != "assistant":
        fail(f"ordre de torns invàlid a {row.get('id')}")
    return [{"role": m["role"], "content": m["content"]} for m in cleaned]


def approx_words(row: dict[str, Any]) -> int:
    if isinstance(row.get("text"), str):
        return len(row["text"].split())
    return sum(len(m["content"].split()) for m in clean_messages(row))


def identity(row: dict[str, Any]) -> str:
    messages = row.get("messages")
    if isinstance(messages, list):
        messages = [m for m in messages if not (isinstance(m, dict) and m.get("role") == "system" and m.get("content") == "")]
    return json.dumps(messages if messages is not None else row.get("text", ""), ensure_ascii=False, sort_keys=True)


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")


def report_variant(name: str, train: list[dict[str, Any]], valid: list[dict[str, Any]], source_rows: list[dict[str, Any]], excluded: int) -> str:
    all_rows = source_rows
    licenses = collections.Counter(str(r.get("redistribucio", "no declarat")) for r in all_rows)
    turns = sum(len(clean_messages(r)) for r in all_rows)
    words = sum(approx_words(r) for r in all_rows)
    longest = sorted(all_rows, key=approx_words, reverse=True)[:3]
    dist = ", ".join(f"{k}: {v}" for k, v in sorted(licenses.items())) or "cap"
    top = "\n".join(f"  - {r.get('id', r.get('base_id', '?'))}: {approx_words(r)} paraules" for r in longest) or "  - cap"
    return (
        f"## {name}\n\n"
        f"- Converses: train {len(train)}, valid {len(valid)}\n"
        f"- Tornatges totals: {turns}\n"
        f"- Tokens aproximats: {words * 1.6:.0f} ({words} paraules × 1,6)\n"
        f"- Redistribució: {dist}\n"
        f"- Entrades excloses per reserva: {excluded}\n"
        f"- Tres converses més llargues:\n{top}\n"
    )


def main() -> None:
    rows = load_all()
    all_knowledge = [r for r in rows if not r.get("_source_file", "").startswith("parla-")]
    all_real = [r for r in rows if r.get("_source_file", "").startswith("parla-") and not r.get("_source_file", "").startswith("parla-sintetic-")]
    all_synthetics = [r for r in rows if r.get("_source_file", "").startswith("parla-sintetic-")]
    excluded_by_kind = {
        "K": sum(is_reserved(r) for r in all_knowledge),
        "KP": sum(is_reserved(r) for r in all_knowledge + [r for r in all_real if r.get("type") == "xat"]),
        "KPS": sum(is_reserved(r) for r in all_knowledge + [r for r in all_real if r.get("type") == "xat"] + all_synthetics),
    }
    kept = [r for r in rows if not is_reserved(r)]

    # Assignació per components d'articles: totes les converses que comparteixen
    # qualsevol article queden al mateix costat de la partició.
    valid_articles = validation_articles(kept)
    article_components_valid = valid_articles
    train_rows: list[dict[str, Any]] = []
    valid_rows: list[dict[str, Any]] = []
    for row in kept:
        docs = article_docs(row)
        target = valid_rows if docs and docs <= article_components_valid else train_rows
        target.append(row)

    # La partició cobreix cada article completament en un únic costat.
    article_side: dict[str, set[str]] = collections.defaultdict(set)
    for side, group in (("train", train_rows), ("valid", valid_rows)):
        for row in group:
            for doc in article_docs(row):
                article_side[doc].add(side)
    leaks = [a for a, sides in article_side.items() if len(sides) > 1]
    if leaks:
        fail(f"articles presents a train i valid: {leaks[:5]}")
    if any(is_reserved(r) for r in train_rows + valid_rows):
        fail("una entrada reservada ha arribat a l'export")

    knowledge = [r for r in kept if not r.get("_source_file", "").startswith("parla-")]
    real = [r for r in kept if r.get("_source_file", "").startswith("parla-") and not r.get("_source_file", "").startswith("parla-sintetic-")]
    synthetics = [r for r in kept if r.get("_source_file", "").startswith("parla-sintetic-") and r.get("apte") is True]
    real_xat = [r for r in real if r.get("type") == "xat"]
    real_text = [r for r in real if r.get("type") == "text" and isinstance(r.get("text"), str)]

    variants: dict[str, tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]] = {}
    for name, subset in (("K", knowledge), ("KP", knowledge + real_xat), ("KPS", knowledge + real_xat + synthetics)):
        # Cada còpia repetida conserva el costat de la conversa font.
        by_identity = {identity(r): r for r in valid_rows}
        train_out: list[dict[str, Any]] = []
        valid_out: list[dict[str, Any]] = []
        source_for_report: list[dict[str, Any]] = []
        for row in subset:
            is_valid = identity(row) in by_identity
            # Les converses xat de parla real es tripliquen només a train.
            copies = 1 if is_valid or row.get("type") != "xat" else 3
            target = valid_out if is_valid else train_out
            target.extend({"messages": clean_messages(row)} for _ in range(copies))
            source_for_report.extend([row] * copies)
        allowed_duplicates = {identity(r) for r in real_xat if identity(r) not in by_identity}
        validate_conversations(train_out, valid_out, allowed_duplicates)
        variants[name] = (train_out, valid_out, source_for_report)
        write_jsonl(OUT / name / "train.jsonl", train_out)
        write_jsonl(OUT / name / "valid.jsonl", valid_out)
        if name in {"KP", "KPS"}:
            write_jsonl(OUT / name / "text.jsonl", [{"text": r["text"]} for r in real_text])

    # Revisió de duplicats a les fonts, abans de la repetició intencional ×3.
    source_conversations = knowledge + real_xat + synthetics
    seen: set[str] = set()
    for row in source_conversations:
        key = identity(row)
        if key in seen:
            fail(f"conversa duplicada a les fonts: {row.get('id')}")
        seen.add(key)

    sections = ["# Informe d'exportació\n", f"Reserva benchmark: {len(RESERVED)} identificadors.\n"]
    for name, (train, valid, source_rows) in variants.items():
        sections.append(report_variant(name, train, valid, source_rows, excluded_by_kind[name]))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "INFORME.md").write_text("\n".join(sections), encoding="utf-8")


def validate_conversations(train: list[dict[str, Any]], valid: list[dict[str, Any]], allowed_duplicates: set[str]) -> None:
    train_counts = collections.Counter(identity(r) for r in train)
    duplicates = [(key, n, key in allowed_duplicates) for key, n in train_counts.items() if n > 1 and (n != 3 or key not in allowed_duplicates)]
    if duplicates:
        fail(f"converses duplicades a train fora de la triplicació de Parla xat: {[(n, allowed) for _, n, allowed in duplicates[:5]]}")
    valid_counts = collections.Counter(identity(r) for r in valid)
    if any(n > 1 for n in valid_counts.values()):
        fail("converses duplicades a valid")


if __name__ == "__main__":
    main()
