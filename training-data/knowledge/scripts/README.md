# Eines de Maia Knowledge

`build_coverage_inventory.py` inventaria totes les fitxes Markdown de
`docs/temes/` i genera el manifest de treball i l'informe de cobertura per tema.
El recompte de fitxes citades és només orientatiu; no prova que tots els fets
d'una fitxa estiguin coberts. L'script inventaria, però no redacta preguntes.

`export_approved.py` comprova que cada conversa exportable tingui una aprovació
editorial i de drets, que comparteixi split amb les seves fonts, i que el JSONL
només exposi `messages`. Escriu els tres splits, el resum i l'atribució.
Assigna les fonts noves a `../split-assignments.json` abans de regenerar.
