# Maia Knowledge

Converses naturals basades en `docs/temes/`. El coneixement es traça internament, però els fitxers d’entrenament contenen només `messages`. El pilot està a `review/conversations.jsonl`; cap pilot no és publicable fins que la revisió humana i els drets estiguin resolts.

- `work/`: ledgers interns regenerables.
- `reports/`: inventari i cobertura.
- `review/`: diàlegs, procedència i criteris editorials.
- `output/`: reservat per a exports aprovats.

Després d’editar les converses, regenera la cobertura amb `python3 training-data/scripts/build_knowledge_review_coverage.py`.
