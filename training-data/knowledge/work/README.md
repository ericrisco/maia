# Treball intern de Knowledge

Conté l’inventari regenerable del corpus: documents, unitats d’evidència, relacions, fonts, problemes de procedència i cobertura per fitxa. `unit-exclusions.jsonl` explica per què s’ometen estructures sense afirmacions entrenables. `manual-unit-exclusions.jsonl` registra exclusions revisades per motius editorials o de procedència; cada línia inclou l’ID de l’evidència i una raó concreta.

Regenera’l amb [`scripts/build_inventory.py`](../scripts/build_inventory.py). La cobertura només compta converses de `review/`; les mostres editorials no compten com a cobertura.
