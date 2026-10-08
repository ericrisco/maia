# Revisió de Maia Knowledge

`records.jsonl` és la font de veritat. Cada registre conté la conversa i la procedència al mateix objecte, perquè una font no es pugui desalinear d'una conversa. El format final d'entrenament conté només `{"messages":[...]}`.

Abans d’afegir registres, consulta [`EXEMPLES.md`](EXEMPLES.md): hi ha converses de referència i casos rebutjats. La pregunta inicial ha de plantejar un dubte que s’entengui sense la fitxa; els seguiments han d’aparèixer de manera natural a partir de la resposta. No afegeixis un torn només per complir una llargada mínima.

## Estats

- `draft`: pendent de revisió.
- `approved_sample`: exemple per calibrar el criteri; no s'exporta ni compta com a cobertura.
- `approved`: revisat, amb drets i evidència comprovats; es pot exportar.
- `rejected`: descartat.

`conversations.jsonl` el genera `validate_knowledge_review.py`. Només conté els missatges dels registres `approved`. No l'edites directament.

Abans d'aprovar un registre, llegeix el diàleg sense la fitxa, aplica totes les preguntes de [`EXEMPLES.md`](EXEMPLES.md) i comprova les fonts, l'atribució, els drets i els límits documentats al mateix registre. Un seguiment artificial és motiu suficient per reescriure o descartar.
