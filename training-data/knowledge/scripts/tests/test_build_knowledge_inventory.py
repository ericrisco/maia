import sys
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))
import build_knowledge_inventory as inventory  # noqa: E402


class KnowledgeInventoryTests(unittest.TestCase):
    def parse(self, relative_path: str) -> dict:
        return inventory.parse_document(inventory.ROOT / relative_path)

    def test_parses_frontmatter_and_markdown_table_rows(self) -> None:
        document = self.parse("docs/temes/costums/calendari-festiu/calendari-festiu.md")
        self.assertEqual(document["frontmatter_error"], "")
        self.assertEqual(document["type"], "article")
        self.assertGreater(document["unit_counts"]["table_row"], 0)
        headers = [unit for unit in document["units"] if unit["kind"] == "table_header"]
        self.assertTrue(headers)

    def test_preserves_lists_and_internal_links(self) -> None:
        document = self.parse("docs/temes/costums/calendari-festiu/calendari-festiu-index-de-fitxes.md")
        self.assertGreater(document["unit_counts"]["list_item"], 0)
        self.assertTrue(any(link.endswith("calendari-festiu.md") for link in document["internal_links"]))

    def test_preserves_blockquotes_as_separate_units(self) -> None:
        document = self.parse("docs/temes/costums/danses/danses.md")
        self.assertGreater(document["unit_counts"]["blockquote"], 0)

    def test_preserves_code_blocks(self) -> None:
        document = self.parse("docs/temes/institucions/justicia/cinc-respostes-a-la-mateixa-pregunta.md")
        self.assertGreater(document["unit_counts"]["code_block"], 0)


if __name__ == "__main__":
    unittest.main()
