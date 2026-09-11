"""El contracte es genera des de l'esquema. Si divergissin, el criteri #9 seria mentida."""

from pathlib import Path

from cervell.render import contract
from cervell.schema import load

SCHEMA = Path(__file__).resolve().parents[1] / "schema" / "corpus.toml"


def test_es_determinista() -> None:
    """Mateix esquema, mateix byte. Sense això no es pot comparar amb el commitejat."""
    s = load(SCHEMA)
    assert contract(s) == contract(s)


def test_declara_tots_els_camps_obligatoris() -> None:
    s = load(SCHEMA)
    text = contract(s)
    for name, spec in s.fields.items():
        if spec.required:
            assert f"`{name}`" in text, f"el contracte no documenta el camp {name}"


def test_explica_la_derivacio() -> None:
    """Qui llegeixi el contracte ha de poder calcular apte_llengua sense preguntar."""
    text = contract(load(SCHEMA))
    assert "apte_llengua" in text
    assert "originaria" in text and "contemporania" in text


def test_llista_totes_les_regles_amb_la_seva_severitat() -> None:
    s = load(SCHEMA)
    text = contract(s)
    for rid, rule in s.rules.items():
        assert rid in text, f"el contracte no esmenta {rid}"
        assert rule.message in text


def test_distingeix_avis_de_error() -> None:
    """R005 avisa i no bloqueja: qui llegeix el contracte ho ha de saber."""
    text = contract(load(SCHEMA))
    assert "R005" in text
    linia = next(ln for ln in text.splitlines() if "R005" in ln)
    assert "avís" in linia.lower() or "avis" in linia.lower()
