import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))
import validate_knowledge_review as validator  # noqa: E402


class KnowledgeReviewValidationTests(unittest.TestCase):
    def test_accepts_a_structurally_valid_multiturn_dialogue(self) -> None:
        row = {
            "messages": [
                {"role": "user", "content": "A què es deu aquesta diferència?"},
                {"role": "assistant", "content": "La font no n'explica la causa."},
                {"role": "user", "content": "Passa també l'any següent?"},
                {"role": "assistant", "content": "Sí, les dues sèries encara divergeixen."},
            ]
        }
        validator.validate_conversation(row, 1)

    def test_rejects_a_single_exchange(self) -> None:
        row = {"messages": [
            {"role": "user", "content": "Què va passar?"},
            {"role": "assistant", "content": "La font no ho diu."},
        ]}
        with self.assertRaisesRegex(ValueError, "at least two"):
            validator.validate_conversation(row, 1)

    def test_rejects_role_order_errors(self) -> None:
        row = {"messages": [
            {"role": "assistant", "content": "Resposta."},
            {"role": "user", "content": "Pregunta."},
            {"role": "assistant", "content": "Resposta."},
            {"role": "user", "content": "Seguiment."},
        ]}
        with self.assertRaisesRegex(ValueError, "invalid role"):
            validator.validate_conversation(row, 1)

    def test_reports_jsonl_line_for_invalid_json(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "bad.jsonl"
            path.write_text('{"ok": true}\nnot-json\n', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, r"bad.jsonl:2: invalid JSON"):
                validator.read_jsonl(path)


if __name__ == "__main__":
    unittest.main()
