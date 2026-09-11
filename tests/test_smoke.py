"""La cadena d'eines funciona i el paquet és importable."""

from cervell import __version__


def test_el_paquet_declara_versio() -> None:
    assert __version__ == "0.1.0"
