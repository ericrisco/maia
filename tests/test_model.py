"""El model carrega el corpus i no jutja. Un document malformat es registra, no peta."""

from pathlib import Path

from cervell.model import load_corpus

DOCS = Path(__file__).resolve().parents[1] / "docs"


def test_corpus_buit_es_valid(tmp_path: Path) -> None:
    """Criteri #10: un corpus buit passa."""
    c = load_corpus(tmp_path)
    assert c.docs == []
    assert c.fonts == {}
    assert c.unparsed == []


def test_document_malformat_es_registra_i_no_llenca(tmp_path: Path) -> None:
    (tmp_path / "temes").mkdir()
    (tmp_path / "temes" / "roto.md").write_text(
        "---\n: no és yaml :\n---\n\n# x\n", encoding="utf-8"
    )
    c = load_corpus(tmp_path)
    assert len(c.unparsed) == 1
    assert "roto.md" in str(c.unparsed[0].path)


def test_carrega_el_corpus_real() -> None:
    c = load_corpus(DOCS)
    assert len(c.docs) >= 20, "el corpus real ha de tenir articles"
    assert len(c.fonts) >= 5, "i les seves fitxes de font"
    assert c.unparsed == [], f"documents no parsejables: {c.unparsed}"


def test_extreu_els_enllacos_interns() -> None:
    c = load_corpus(DOCS)
    amb_enllacos = [d for d in c.docs if d.links]
    assert amb_enllacos, "cap document amb enllaços interns"


def test_tots_els_articles_declaren_veu_i_epoca() -> None:
    c = load_corpus(DOCS)
    for d in c.docs:
        assert d.veu in ("originaria", "compilada"), d.path
        assert d.epoca in ("contemporania", "historica"), d.path
