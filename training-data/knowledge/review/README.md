# Revisió de Maia Knowledge

`conversations.jsonl` té una conversa candidata per línia. `provenance.jsonl`
té una fila per candidat amb evidència, fonts, drets i estat editorial. Tots dos
fitxers es relacionen mitjançant `example_id`.

Un candidat no és una dada d'entrenament. Només els registres revisats i
aprovats es poden exportar; el JSONL final conté únicament `messages`.

El lot anterior s'ha apartat a `../archive/previous-batch-2026-10/`. No es
reincorpora automàticament: cada conversa s'ha de tornar a redactar i revisar
amb `../EXEMPLES.md` i `../../PLAN.md`.
