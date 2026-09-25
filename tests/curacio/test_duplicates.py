"""Contractes per a plantilles i candidats de quasi-duplicat."""

from pathlib import Path

from curacio.duplicates import mark_near_duplicates, mark_templates
from curacio.model import Block, Chunk, CuratedDoc


def _chunk(doc_id: str, text: str) -> Chunk:
    return Chunk(f"{doc_id}#c1", "secció", [], text, 0.0)


def test_plantilla_de_paragraf_detectada_dins_de_chunks_mes_llargs() -> None:
    template = (
        "Aquest avís editorial llarg apareix en diversos documents del corpus i explica "
        "com s'ha de llegir la informació registrada en aquesta fitxa institucional."
    )
    documents = []
    for index in range(3):
        doc_id = f"doc-{index}"
        block = Block("#b1", "cos", "secció", template, text=template)
        chunk = Chunk(f"{doc_id}#c1", "secció", [block], f"Text propi {index}.\n\n{template}", 0.0)
        documents.append(
            CuratedDoc(
                doc_id,
                Path(f"{doc_id}.md"),
                {},
                "sha",
                [block],
                [chunk],
                [],
                source_paragraphs=[f"Text propi {index}.", template],
            )
        )

    assert mark_templates(documents) == (1, 3)
    assert all(doc.chunks[0].template and doc.chunks[0].decision == "excloure" for doc in documents)


def test_quasi_duplicats_es_marquin_i_un_text_diferent_no() -> None:
    words = [f"token{index}" for index in range(500)]
    near = words.copy()
    near[250] = "canvi"
    chunks = [
        _chunk("a", " ".join(words)),
        _chunk("b", " ".join(near)),
        _chunk("c", "un contingut independent i curt"),
    ]

    mark_near_duplicates(chunks)

    assert chunks[0].decision == chunks[1].decision == "pendent"
    assert chunks[2].decision == "incloure"


def test_no_compara_chunks_del_mateix_document() -> None:
    text = " ".join(f"token{index}" for index in range(100))
    chunks = [_chunk("mateix", text), _chunk("mateix", text)]

    mark_near_duplicates(chunks)

    assert all(chunk.decision == "incloure" for chunk in chunks)
