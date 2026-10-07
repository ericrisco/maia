import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))
import validate_knowledge_review as validator  # noqa: E402


class KnowledgeReviewValidationTests(unittest.TestCase):
    def test_redistribution_gate_uses_explicit_source_rights(self) -> None:
        open_source = validator.font_metadata("docs/fonts/wikipedia-dama-blanca.md", 1)
        restricted_source = validator.font_metadata("docs/fonts/premsa-andorrana.md", 1)
        self.assertTrue(validator.is_redistributable(open_source.get("redistribucio")))
        self.assertFalse(validator.is_redistributable(restricted_source.get("redistribucio")))

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

    def test_accepts_a_single_exchange_when_the_question_is_resolved(self) -> None:
        row = {"messages": [
            {"role": "user", "content": "Què va passar?"},
            {"role": "assistant", "content": "La font no ho diu."},
        ]}
        validator.validate_conversation(row, 1)

    def test_review_record_keeps_messages_and_provenance_in_one_row(self) -> None:
        row = {
            "record_id": "sample-001",
            "review_status": "approved_sample",
            "messages": [
                {"role": "user", "content": "Què és això?"},
                {"role": "assistant", "content": "És una mostra."},
            ],
            "source_documents": ["docs/temes/exemple.md"],
            "source_ids": ["docs/fonts/exemple.md"],
            "source_locations": ["Definició"],
            "claims_supported": ["La mostra té una afirmació."],
            "license": "CC BY-SA 4.0",
            "attribution": "Font de prova.",
            "limits": "Mostra fictícia per a la prova.",
            "split_group": "sample-001",
            "unit_ids": [],
        }
        validator.validate_review_record(row, 1)

    def test_review_record_rejects_split_provenance_fields(self) -> None:
        row = {
            "record_id": "sample-001",
            "review_status": "approved_sample",
            "messages": [
                {"role": "user", "content": "Què és això?"},
                {"role": "assistant", "content": "És una mostra."},
            ],
        }
        with self.assertRaisesRegex(ValueError, "expected exactly"):
            validator.validate_review_record(row, 1)

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
