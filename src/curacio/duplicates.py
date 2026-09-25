"""E7: agrupació de plantilles i quasi-duplicats reproduïble."""

from __future__ import annotations

import re
import unicodedata
from collections import Counter, defaultdict

from curacio.chunking import word_count
from curacio.model import Chunk, CuratedDoc

NEAR_DUPLICATE_THRESHOLD = 0.90


def normalized_text(text: str) -> str:
    """Case-folds, strips accents and collapses whitespace for comparison only."""
    folded = unicodedata.normalize("NFKD", text.casefold())
    plain = "".join(char for char in folded if not unicodedata.combining(char))
    return " ".join(re.findall(r"[a-z0-9]+", plain))


def shingles(text: str, size: int = 5) -> set[tuple[str, ...]]:
    """Returns unique five-token shingles; short texts use one whole-text shingle."""
    tokens = normalized_text(text).split()
    if len(tokens) < size:
        return {tuple(tokens)} if tokens else set()
    return {tuple(tokens[index : index + size]) for index in range(len(tokens) - size + 1)}


def mark_templates(documents: list[CuratedDoc]) -> tuple[int, int]:
    """Marks long exact source paragraphs shared by three documents as templates."""
    occurrences: dict[str, set[str]] = defaultdict(set)
    for document in documents:
        for paragraph in document.source_paragraphs:
            normalized = normalized_text(paragraph)
            if word_count(normalized) >= 12:
                occurrences[normalized].add(document.doc_id)
    templates = {
        text for text, source_documents in occurrences.items() if len(source_documents) >= 3
    }
    affected_documents: set[str] = set()
    for document in documents:
        matching_paragraphs = {
            normalized_text(paragraph)
            for paragraph in document.source_paragraphs
            if normalized_text(paragraph) in templates
        }
        if not matching_paragraphs:
            continue
        affected_documents.add(document.doc_id)
        for block in document.blocks:
            block_text = normalized_text(block.raw)
            if any(paragraph in block_text for paragraph in matching_paragraphs):
                block.template = True
                if block.decision != "excloure":
                    block.decision = "excloure"
                    block.reason = "conté un paràgraf plantilla repetit en tres documents o més"
                for chunk in document.chunks:
                    if block in chunk.blocks:
                        chunk.template = True
                        chunk.decision = "excloure"
                        chunk.reason = "conté un paràgraf plantilla repetit en tres documents o més"
    return len(templates), len(affected_documents)


def mark_near_duplicates(chunks: list[Chunk]) -> None:
    """Flags exact high-overlap pairs using shared-shingle candidate generation."""
    sets = [shingles(chunk.text) for chunk in chunks]
    postings: dict[tuple[str, ...], list[int]] = defaultdict(list)
    for index, values in enumerate(sets):
        for value in values:
            postings[value].append(index)
    shared_counts: Counter[tuple[int, int]] = Counter()
    for indices in postings.values():
        for offset, left_index in enumerate(indices):
            left_doc = chunks[left_index].id.split("#", maxsplit=1)[0]
            for right_index in indices[offset + 1 :]:
                if left_doc != chunks[right_index].id.split("#", maxsplit=1)[0]:
                    shared_counts[left_index, right_index] += 1
    for (left_index, right_index), shared in shared_counts.items():
        left = chunks[left_index]
        right = chunks[right_index]
        union_size = len(sets[left_index]) + len(sets[right_index]) - shared
        if union_size and shared / union_size >= NEAR_DUPLICATE_THRESHOLD:
            for chunk in (left, right):
                if chunk.decision == "incloure":
                    chunk.decision = "pendent"
                    chunk.reason = (
                        f"quasi-duplicat Jaccard de shingles ≥ {NEAR_DUPLICATE_THRESHOLD:.2f}"
                    )
