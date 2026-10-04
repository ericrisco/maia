from __future__ import annotations

from pathlib import Path

import pytest

from training_data.inventory import scan_tree
from training_data.parser import MarkdownParseError, parse_markdown

FIXTURES = Path(__file__).parents[1] / "fixtures" / "training_data"


def test_parser_preserves_frontmatter_body_structure_and_links() -> None:
    source = (FIXTURES / "markdown_all_features.md").read_text(encoding="utf-8")

    document = parse_markdown("docs/temes/proves.md", source)

    assert document.path == "docs/temes/proves.md"
    expected_body = source.split("\n---\n", maxsplit=1)[1]
    assert document.body == expected_body
    assert "corregida s'ha marcat com a resolta" in document.body
    assert "buit registrat" in document.body
    assert document.metadata["type"] == "article"
    assert document.metadata["title"] == "Fitxa de prova del parser"
    assert document.metadata["description"] == "Un exemple sense dades reals."
    assert document.metadata["tema"] == "proves/parser"
    assert document.metadata["veu"] == "compilada"
    assert document.metadata["epoca"] == "contemporania"
    assert document.metadata["apte_llengua"] is False
    assert document.metadata["font"] == "font-de-prova"
    assert document.metadata["timestamp"]
    assert document.metadata["tags"] == ["prova", "estructura"]

    kinds = [block.kind for block in document.structure]
    assert "heading" in kinds
    assert "paragraph" in kinds
    assert "list_item" in kinds
    assert "table_row" in kinds
    assert "blockquote" in kinds
    assert "code_block" in kinds
    assert any(
        block.kind == "code_block" and "codi indentat" in block.text for block in document.structure
    )
    assert not any(
        block.kind == "heading" and "dins d'un bloc de codi" in block.text
        for block in document.structure
    )
    table_rows = [block for block in document.structure if block.kind == "table_row"]
    assert any(block.cells == ("estat", "corregit i resolt") for block in table_rows)

    links = {(link.kind, link.target, link.internal) for link in document.links}
    assert ("markdown", "../fitxa.md", True) in links
    assert ("markdown", "https://example.invalid/font", False) in links
    assert ("wikilink", "fitxa-relacionada", True) in links
    assert all(target != "codi.md" for _, target, _ in links)


def test_parser_accepts_markdown_without_frontmatter() -> None:
    source = (FIXTURES / "readme_without_frontmatter.md").read_text(encoding="utf-8")

    document = parse_markdown("docs/raw/README.md", source)

    assert document.metadata == {}
    assert document.body == source
    assert document.structure[0].kind == "heading"


def test_parser_reads_representative_thematic_and_speech_records() -> None:
    repository = Path(__file__).resolve().parents[2]
    samples = (
        Path("docs/temes/costums/calendari-festiu/calendari-festiu-index-de-fitxes.md"),
        Path("docs/parla/oral/el-contrapas-teo-armengol.md"),
    )

    for relative_path in samples:
        source = (repository / relative_path).read_text(encoding="utf-8")
        document = parse_markdown(relative_path.as_posix(), source)
        assert document.path == relative_path.as_posix()
        assert document.metadata["title"]
        assert document.body
        assert document.structure


def test_parser_reports_invalid_frontmatter_with_path() -> None:
    source = (FIXTURES / "malformed_frontmatter.md").read_text(encoding="utf-8")

    with pytest.raises(MarkdownParseError, match=r"docs/temes/trencat\.md"):
        parse_markdown("docs/temes/trencat.md", source)


def test_inventory_classifies_each_file_once_and_keeps_auxiliary_documents(tmp_path: Path) -> None:
    (tmp_path / "temes").mkdir()
    (tmp_path / "raw").mkdir()
    (tmp_path / ".obsidian").mkdir()
    (tmp_path / "temes" / "fitxa.md").write_text(
        (FIXTURES / "markdown_all_features.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (tmp_path / "temes" / "trencat.md").write_text(
        (FIXTURES / "malformed_frontmatter.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (tmp_path / "CONTRACT.md").write_text(
        (FIXTURES / "generated_contract.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (tmp_path / "raw" / "README.md").write_text(
        (FIXTURES / "readme_without_frontmatter.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (tmp_path / "fonts.pdf").write_bytes(b"%PDF-1.7\x00binary fixture")
    (tmp_path / "Corpus.base").write_text("view metadata", encoding="utf-8")
    (tmp_path / ".obsidian" / "workspace.json").write_text("{}", encoding="utf-8")

    inventory = scan_tree(tmp_path)

    paths = [entry.path for entry in inventory.entries]
    assert paths == sorted(paths)
    assert len(paths) == 7
    assert len(set(paths)) == 7
    by_path = {entry.path: entry for entry in inventory.entries}
    assert by_path["temes/fitxa.md"].disposition == "markdown_read"
    assert by_path["temes/trencat.md"].disposition == "markdown_error"
    assert by_path["temes/trencat.md"].error
    assert by_path["CONTRACT.md"].disposition == "generated_auxiliary"
    assert by_path["CONTRACT.md"].document is not None
    assert by_path["raw/README.md"].disposition == "markdown_read"
    assert by_path["fonts.pdf"].disposition == "non_markdown"
    assert by_path["Corpus.base"].disposition == "generated_auxiliary"
    assert by_path[".obsidian/workspace.json"].disposition == "generated_auxiliary"


def test_inventory_records_invalid_utf8_as_markdown_error(tmp_path: Path) -> None:
    (tmp_path / "invalid.md").write_bytes(b"\xff\xfe\x00")

    inventory = scan_tree(tmp_path)

    assert len(inventory.entries) == 1
    assert inventory.entries[0].disposition == "markdown_error"
    assert "utf-8" in (inventory.entries[0].error or "").casefold()


def test_inventory_accounts_for_every_file_in_the_real_docs_tree() -> None:
    repository = Path(__file__).resolve().parents[2]
    docs = repository / "docs"
    expected = {path.relative_to(docs).as_posix() for path in docs.rglob("*") if not path.is_dir()}

    inventory = scan_tree(docs)
    actual = [entry.path for entry in inventory.entries]
    by_path = {entry.path: entry for entry in inventory.entries}

    assert len(actual) == len(set(actual))
    assert set(actual) == expected
    for relative_path in expected:
        path = docs / relative_path
        if path.suffix.lower() == ".md" and not path.is_symlink():
            assert by_path[relative_path].disposition in {
                "markdown_read",
                "markdown_error",
                "generated_auxiliary",
            }
