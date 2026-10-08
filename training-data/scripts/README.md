# Scripts de Training Data

Executa aquestes ordres des de l’arrel de `maia/`.

- `python3 training-data/scripts/inventory.py` regenera els CSV de cobertura de Knowledge i Language. Conserva els estats i els comentaris que ja existeixen.
- `python3 training-data/scripts/parse_corpus.py` llegeix totes les fitxes Knowledge i crea `knowledge/reports/parser-coverage.md`. El parser conserva les unitats Markdown en ordre i no crea preguntes.
- `python3 -m unittest discover -s training-data/scripts -p 'test_*.py'` executa les proves del parser amb una mostra estructural i una fitxa real.

Les marques epistemològiques detectades pel parser són pistes de cerca; cal revisar el text original abans de redactar una resposta.
