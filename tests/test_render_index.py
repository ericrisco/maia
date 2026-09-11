"""L'índex es llegeix sense obrir cap document. Criteri #8."""

from pathlib import Path

from cervell.model import load_corpus
from cervell.render import index

DOCS = Path(__file__).resolve().parents[1] / "docs"


def test_es_determinista() -> None:
    c = load_corpus(DOCS)
    assert index(c) == index(c)


def test_llista_tots_els_documents() -> None:
    c = load_corpus(DOCS)
    text = index(c)
    for d in c.docs:
        assert d.path.name in text, f"{d.path.name} no surt a l'índex"


def test_cada_fila_porta_tema_veu_epoca_i_aptitud() -> None:
    """Sense obrir cap document s'ha de poder saber què és cada cosa."""
    c = load_corpus(DOCS)
    text = index(c)
    assert "Tema" in text and "Veu" in text and "Època" in text and "Apte" in text


def test_un_corpus_buit_genera_index_valid(tmp_path: Path) -> None:
    text = index(load_corpus(tmp_path))
    assert text.strip(), "fins i tot buit, l'índex ha de dir alguna cosa"
