# Maia Knowledge — laboratori de converses humanes

Aquest directori és una mostra editorial del format nou. No és encara part de
`output/` ni del dataset d'entrenament. Les converses estan en revisió humana i
les fonts d'aquests exemples tenen la reutilització per a entrenament pendent.

## Estructura

- `conversations.jsonl`: una conversa coherent per línia; només conté `messages`.
- `provenance.jsonl`: font, límit factual, estat de drets i revisió de cada línia.

La traça editorial no s'inclou als missatges que rebria el model.

## Comprovació ràpida

Cada conversa comença amb una necessitat comprensible sense obrir la fitxa.
Els seguiments reprenen una idea de la resposta anterior i demanen una cosa
nova. Les respostes resolen el dubte abans d'afegir context. El diàleg es pot
llegir en veu alta sense parlar de seccions, taules, files ni del corpus.

Aquests exemples serveixen per discutir l'estil. Abans d'aprovar-los cal
revisar fidelitat, naturalitat i drets. No s'han de copiar a `output/` mentre
l'estat de drets sigui pendent.

`Maia Language` no hereta aquest patró de generació: només pot preservar torns
humans que ja existeixin a les fonts elegibles. No s'inventen preguntes per
fabricar conversa.
