# Maia Knowledge

Entrena respostes factuals sobre Andorra a partir de `docs/temes/`. Cada
conversa candidate ha de tenir una raó humana per existir, una resposta
comprovada i procedència separada. Consulta [els exemples](review/EXEMPLES.md)
abans d'afegir registres.

- `review/`: candidats editorials i fonts que els sustenten.
- `work/`: inventari i dades temporals de preparació.
- `output/`: JSONL aprovats per split i atribució; l'exportació actual és parcial.
- `reports/`: cobertura, qualitat, drets i exclusions.
- `scripts/`: inventari i exportació validada de registres aprovats.

Abans d'afegir un exemple, consulta `review/EXEMPLES.md`. Després de cada
conversa aprovada, actualitza `split-assignments.json` si incorpora una font
nova i executa `python3 scripts/export_approved.py`. Les fonts d'una mateixa
conversa han de quedar al mateix split.
