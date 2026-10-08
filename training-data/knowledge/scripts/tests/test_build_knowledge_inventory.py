import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_knowledge_inventory as inventory


class InventoryParserTests(unittest.TestCase):
    def test_keeps_title_description_and_paragraph_units(self):
        document = inventory.parse_document_text(
            "docs/temes/test.md",
            "---\ntype: article\ntitle: Títol\ndescription: Descripció\ntema: test\nfont: exemple\nveu: compilada\nepoca: contemporania\napte_llengua: false\ntimestamp: 2026-09-18T12:00:00Z\ntags: [a, b]\n---\n# Secció\n\nUn paràgraf amb [enllaç](altre.md).\n",
        )
        self.assertEqual(document["frontmatter_error"], "")
        self.assertEqual(document["metadata"]["type"], "article")
        self.assertEqual(document["metadata"]["title"], "Títol")
        self.assertEqual(document["metadata"]["tema"], "test")
        self.assertEqual(document["metadata"]["font"], "exemple")
        self.assertEqual(document["metadata"]["veu"], "compilada")
        self.assertEqual(document["metadata"]["epoca"], "contemporania")
        self.assertIs(document["metadata"]["apte_llengua"], False)
        self.assertEqual(document["metadata"]["timestamp"], "2026-09-18T12:00:00+00:00")
        self.assertEqual(document["metadata"]["tags"], ["a", "b"])
        self.assertEqual(document["unit_count"], 4)
        self.assertEqual(document["units"][0]["kind"], "metadata_title")
        self.assertEqual(document["units"][1]["kind"], "metadata_description")
        self.assertEqual(document["units"][2]["kind"], "heading")
        self.assertEqual(document["units"][3]["internal_links"], ["altre.md"])

    def test_keeps_each_table_row_as_a_unit(self):
        units = inventory.parse_units(
            "docs/temes/test.md",
            "| Any | Fet |\n|---|---|\n| 1901 | Primer |\n| 1902 | Segon |\n",
        )
        self.assertEqual([unit["kind"] for unit in units], ["table_header", "table_row", "table_row"])
        self.assertEqual(units[1]["cells"], ["1901", "Primer"])

    def test_keeps_lists_quotes_and_code(self):
        units = inventory.parse_units(
            "docs/temes/test.md",
            "- Primer\n  continuació\n\n> Cita\n> segona línia\n\n```text\nexemple\n```\n",
        )
        self.assertEqual([unit["kind"] for unit in units], ["list_item", "blockquote", "code_block"])
        self.assertIn("continuació", units[0]["text"])

    def test_unit_ids_survive_unrelated_insertions(self):
        one = inventory.parse_units("docs/temes/test.md", "Text estable.\n")[0]["unit_id"]
        two = inventory.parse_units("docs/temes/test.md", "Un altre paràgraf.\n\nText estable.\n")[-1]["unit_id"]
        self.assertEqual(one, two)


if __name__ == "__main__":
    unittest.main()
