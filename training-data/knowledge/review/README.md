# Revisió de Maia Knowledge

`conversations.jsonl` té una conversa candidata per línia. `provenance.jsonl`
té una fila per candidat amb evidència, fonts, drets i estat editorial. Tots dos
fitxers es relacionen mitjançant `example_id`.

Un candidat no és una dada d'entrenament. Només els registres revisats i
aprovats es poden exportar; el JSONL final conté únicament `messages`.
