import unittest

from parse_corpus import ROOT, parse_document, parse_frontmatter, parse_markdown, split_frontmatter


class ParseCorpusTests(unittest.TestCase):
    def test_frontmatter_reads_block_description_tags_and_boolean(self):
        text = '''---
type: article
title: "Prova"
description: >
  Primera línia.
  Segona línia.
apte_llengua: false
tags: [costums, "ball, tradicional"]
---
# Cos
'''
        raw, body = split_frontmatter(text)
        metadata = parse_frontmatter(raw)
        self.assertEqual(body.strip(), "# Cos")
        self.assertEqual(metadata["description"], "Primera línia. Segona línia.")
        self.assertFalse(metadata["apte_llengua"])
        self.assertEqual(metadata["tags"], ["costums", "ball, tradicional"])

    def test_markdown_keeps_order_context_tables_lists_quotes_and_links(self):
        body = '''# Títol
Paràgraf amb [font](../fonts/prova.md).
## Dades
| Any | Festa |
|---|---|
| 1902 | Sant Pere |
- primer punt
> Buit registrat.
'''
        blocks, metrics = parse_markdown(body)
        self.assertEqual([b["kind"] for b in blocks], ["heading", "paragraph", "heading", "table", "list_item", "quote"])
        self.assertEqual(blocks[3]["header"], ["Any", "Festa"])
        self.assertEqual(blocks[3]["rows"], [["1902", "Sant Pere"]])
        self.assertEqual(blocks[4]["heading_context"], ["Títol", "Dades"])
        self.assertEqual(blocks[1]["links"], [{"label": "font", "target": "../fonts/prova.md"}])
        self.assertIn("unknown", blocks[5]["markers"])
        self.assertEqual(metrics["table_rows"], 1)

    def test_real_corpus_document_has_metadata_sections_tables_and_links(self):
        path = ROOT / "docs/temes/institucions/justicia/els-tribunals-tancaven-per-la-fira-dorganya.md"
        parsed = parse_document(path)
        self.assertEqual(parsed["metadata"]["title"], "Els tribunals tancaven per la fira d'Organyà")
        self.assertGreater(parsed["metrics"]["headings"], 5)
        self.assertGreater(parsed["metrics"]["tables"], 0)
        self.assertGreater(parsed["metrics"]["links"], 0)


if __name__ == "__main__":
    unittest.main()
