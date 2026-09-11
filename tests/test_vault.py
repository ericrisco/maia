"""La bóveda d'Obsidian: propietats visibles i una vista que filtra per aptitud."""

from pathlib import Path

import yaml

DOCS = Path(__file__).resolve().parents[1] / "docs"


def test_les_tres_vistes_son_yaml_valid() -> None:
    for name in ("Corpus.base", "Parla.base", "Fonts.base"):
        parsed = yaml.safe_load((DOCS / name).read_text(encoding="utf-8"))
        assert "views" in parsed, f"{name} no declara cap vista"


def test_una_vista_filtra_per_aptitud_linguistica() -> None:
    """Criteri #7 de l'spec: ha d'existir una vista que filtri per apte_llengua."""
    parsed = yaml.safe_load((DOCS / "Corpus.base").read_text(encoding="utf-8"))
    filtres = [str(v.get("filters", "")) for v in parsed["views"]]
    assert any("apte_llengua" in f for f in filtres)


def test_la_configuracio_forca_enllacos_markdown() -> None:
    """Els wikilinks trenquen la conformitat OKF."""
    cfg = yaml.safe_load((DOCS / ".obsidian" / "app.json").read_text(encoding="utf-8"))
    assert cfg["useMarkdownLinks"] is True
    assert cfg["newLinkFormat"] == "relative"
