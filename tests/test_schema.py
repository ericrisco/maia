"""L'esquema és la font de veritat, i la derivació d'aptitud és una regla, no un criteri."""

from pathlib import Path

import pytest

from cervell.schema import Epoca, Veu, derive_aptitude, load

SCHEMA = Path(__file__).resolve().parents[1] / "schema" / "corpus.toml"


@pytest.mark.parametrize(
    ("veu", "epoca", "esperat"),
    [
        (Veu.ORIGINARIA, Epoca.CONTEMPORANIA, True),
        (Veu.ORIGINARIA, Epoca.HISTORICA, False),
        (Veu.COMPILADA, Epoca.CONTEMPORANIA, False),
        (Veu.COMPILADA, Epoca.HISTORICA, False),
    ],
)
def test_taula_de_veritat_completa(veu: Veu, epoca: Epoca, esperat: bool) -> None:
    """Les quatre combinacions. Només originaria + contemporania és apta."""
    assert derive_aptitude(veu, epoca) is esperat


def test_esquema_declara_els_camps_obligatoris() -> None:
    schema = load(SCHEMA)
    obligatoris = {n for n, f in schema.fields.items() if f.required}
    assert {
        "type",
        "title",
        "tema",
        "veu",
        "epoca",
        "apte_llengua",
        "font",
        "timestamp",
    } <= obligatoris


def test_esquema_declara_els_enums_tancats() -> None:
    schema = load(SCHEMA)
    assert schema.enums["veu"] == ["originaria", "compilada"]
    assert schema.enums["epoca"] == ["contemporania", "historica"]
    assert schema.enums["redistribucio"] == ["si", "no", "pendent"]


def test_esquema_declara_les_catorze_regles_amb_severitat() -> None:
    schema = load(SCHEMA)
    assert len(schema.rules) == 14
    assert {f"R{n:03d}" for n in range(1, 15)} == set(schema.rules)
    assert schema.rules["R005"].severity == "warning", "R005 avisa, no bloqueja (constitució §24)"
    assert schema.rules["R001"].severity == "error"


def test_tota_regla_porta_missatge() -> None:
    schema = load(SCHEMA)
    assert all(r.message.strip() for r in schema.rules.values())
