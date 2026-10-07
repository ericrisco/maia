# Revisió de Maia Knowledge

`conversations.jsonl` té una conversa candidata per línia. `provenance.jsonl`
té una fila per candidat amb evidència, fonts, drets i estat editorial. Tots dos
fitxers es relacionen mitjançant `example_id`.

Un candidat no és una dada d'entrenament. Només els registres revisats i
aprovats es poden exportar; el JSONL final conté únicament `messages`.

Els lots anteriors s'han apartat a `../archive/previous-batch-2026-10/`,
`../archive/rejected-batch-2026-10/` i
`../archive/rejected-conversation-patterns-2026-10/`. Aquest darrer conserva
31 converses retirades en el reset editorial: encara feien referència a la
«fitxa» o al «corpus» o repetien iniciadors construïts. Cap lot arxivat no
entra a l'exportació activa. No es reincorporen automàticament: cada conversa
s'ha de tornar a redactar i revisar amb `../EXEMPLES.md` i `../../PLAN.md`.
