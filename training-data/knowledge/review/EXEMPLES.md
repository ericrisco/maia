# Exemples i convencions per a Knowledge

La font de veritat factual és `docs/temes/`. Llegiu la fitxa completa abans de
redactar. El text final d'entrenament va a `conversations.jsonl`; la font i els
drets queden a `provenance.jsonl`.

## Forma

- Cada registre és una conversa `user`/`assistant` amb dos o més intercanvis.
- La primera resposta resol la pregunta original i s'entén sola.
- El seguiment neix d'allò que acaba de dir l'assistent i obre una curiositat
  relacionada.
- Cada resposta és una frase completa en català natural; cap dada sense
  context, cap títol de secció, cap fila de taula sense explicar.
- Si el corpus no sap la resposta, el diàleg ho diu amb precisió i no omple el
  buit amb una conjectura.

## Exemple: una aparent contradicció

```json
{"messages":[{"role":"user","content":"Una cosa: si el 70% diu que la religió els importa poc, com pot ser que gairebé la meitat es consideri religiosa?"},{"role":"assistant","content":"No és necessàriament contradictori: són dues preguntes diferents. En l'estudi del CRES publicat el 2013, el 70% deia que el fet religiós era poc o gens important, però el 48% es considerava religiós."},{"role":"user","content":"I els que no es consideraven religiosos es comptaven com a ateus?"},{"role":"assistant","content":"No. L'estudi separava les dues respostes: un 37,5% es considerava «no religiós» i un 14,2% «ateu convençut»."}]}
```

La persona intenta entendre dues xifres que semblen xocar; el seguiment
comprova una distinció que la primera resposta encara no ha explicat.

## Evitar

- «Què explica la secció X?» o «Què indica aquesta fila?» — demanen navegar
  pel document, no entendre el tema.
- «Resumeix la fitxa» — no té una necessitat concreta i convida a una resposta
  de plantilla.
- «I què més?» com a seguiment — no diu quin dubte nou té la persona.
- Respostes com «14,2%» o «el 2014» sense explicar a què es refereixen.
- Tres o quatre paraules canviades sobre el mateix fet per augmentar el volum.

Els exemples són pilots editorials. Abans de publicar-los com a entrenament,
cal validar exactitud, naturalitat, traçabilitat i llicència.
