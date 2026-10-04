from __future__ import annotations

from training_data.text import markdown_to_plain_text


def test_markdown_formatting_and_link_destinations_are_removed() -> None:
    source = "- **La vila** manté [la tradició](../temes/(fitxa).md) amb `cendra`."

    normalized = markdown_to_plain_text(source)

    assert normalized == "La vila manté la tradició amb cendra."


def test_replaced_strikethrough_claims_are_removed_and_table_rows_are_readable() -> None:
    source = "~~La data antiga.~~ La data revisada és el 2026."
    row = "| **Data** | 2026 |"

    assert markdown_to_plain_text(source) == "La data revisada és el 2026."
    assert markdown_to_plain_text(row, block_kind="table_row") == "Data — 2026"


def test_markdown_only_input_does_not_create_nonempty_content() -> None:
    assert markdown_to_plain_text("~~text obsolet~~").strip() == ""
    assert markdown_to_plain_text("text parcial~~").strip() == ""
