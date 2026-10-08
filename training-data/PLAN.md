# Pla de treball: converses que sonen humanes

## Objectiu

Crear converses de fine-tuning que responguin dubtes reals sobre Andorra. La pregunta ha de tenir sentit per a algú que no conegui les fitxes internes de Maia. La resposta ha de resoldre el dubte amb informació sostinguda pel corpus.

## Com trobar la pregunta

Abans d'escriure, digues en una frase què necessita saber la persona. Busca una situació recognoscible: vol entendre una tradició, aclarir una confusió, preparar una visita, comprovar una dada o saber què es pot afirmar. Escriu la pregunta des d'aquesta necessitat, no des del títol, subtítol, taula o buit d'una fitxa.

Si l'única pregunta que se t'acut és «què explica aquesta secció?» o «què diu aquesta fila?», encara no tens una pregunta d'usuari. Reformula-la amb el context necessari o descarta el fet com a exemple conversacional.

No cal que cada pregunta sigui original o dramàtica. Una pregunta breu i quotidiana és millor que una veu impostada, argot decoratiu o una escena inventada.

## Com escriure els torns

1. Comença amb una pregunta concreta i comprensible per si sola.
2. Respon primer el dubte. Fes servir una veu clara i natural, sense etiquetes ni llistes de camps.
3. Afegeix només el context que ajuda a entendre la resposta.
4. Afegeix un seguiment quan sigui creïble que la resposta provoqui una altra pregunta. El seguiment ha d'aportar una dada o aclariment nou.
5. Tanca quan la necessitat queda resolta. No allarguis el diàleg per assolir una quota de torns.

Cada conversa del conjunt serà multitorn: com a mínim dues preguntes de l'usuari i dues respostes. El seguiment ha de néixer de la resposta anterior; si no es pot trobar un seguiment natural, no es força una conversa només per omplir una quota: es reformula la necessitat inicial o no es crea el registre.

## Respostes i límits

- Separa fets documentats, llegendes, interpretacions i incerteses.
- Si el corpus no resol una pregunta, digues què se sap i què falta. No completis la resposta amb una suposició.
- Una resposta no ha de copiar la fitxa sencera ni deixar una frase a mig fer.
- No afegeixis una dada només perquè apareix a prop de la resposta.
- La primera pregunta no pot dependre de conèixer «la fitxa», «la secció», «la fila» o «el gràfic».
- Les referències i els estats editorials queden fora de `messages`; es guarden a la procedència interna.

## Revisió abans d'acceptar

Llegeix el diàleg sense la font i comprova:

- **Necessitat real:** una persona podria preguntar-ho en una conversa normal?
- **Context:** s'entén què pregunta des del primer torn?
- **Resposta útil:** el primer torn de resposta ja resol el dubte?
- **Fil:** cada seguiment neix de la resposta anterior i afegeix alguna cosa?
- **Fidelitat:** cada afirmació es pot verificar al corpus?
- **Veu:** sona clara i natural, sense imitar oralitat ni omplir amb fórmules?
- **Drets:** la procedència i les condicions de reutilització estan registrades?

Si falla una comprovació, reescriu o descarta el registre. No comptis-lo com a cobertura aprovada.

## Fases

1. Fixar i seguir el criteri de `knowledge/review/EXEMPLES.md`.
2. Inventariar tots els fitxers de `docs/temes/` i `docs/parla/` a `work/coverage.csv`; no donar per cobert cap tema sense inspecció.
3. Afegir les converses a `knowledge/review/conversations.jsonl`, tema a tema i una conversa per línia, amb procedència a `work/provenance.jsonl`.
4. Cada conversa ha de tenir el seu propi commit i push a `main`, després de validar contingut, cobertura, procedència i estructura.
5. Revisar naturalitat, correcció, duplicació, afirmacions omeses i drets abans de passar converses a `knowledge/output/`.
6. Mesurar cobertura per fet i relació útil, no només per document o pel nombre de preguntes.
7. Processar Maia Language separadament, només amb fragments humans elegibles i transcripcions fiables, i preservar el text original.
8. Fer splits quan hi hagi prou registres, agrupant per tema o peça per evitar filtracions entre conjunts.

## Formats

Una línia JSONL és una conversa completa:

```json
{"messages":[{"role":"user","content":"..."},{"role":"assistant","content":"..."},{"role":"user","content":"..."},{"role":"assistant","content":"..."}]}
```

Els exports aprovats contenen només `messages`. Les mostres de calibratge són internes i no s'exporten automàticament. La traçabilitat, els hashes de font i els estats de drets queden separats a `work/provenance.jsonl`.
