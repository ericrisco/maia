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

## Exemple: una situació pràctica

```json
{"messages":[{"role":"user","content":"Som unes quantes famílies i volem inscriure una comunitat religiosa a Andorra. Cal que siguem vint-i-un i tots majors d'edat?"},{"role":"assistant","content":"No. La Llei 2/2025 fixa un mínim de vint persones físiques, andorranes o residents, i només exigeix que almenys una tingui majoria d'edat i plens drets. També han de compartir les mateixes creences religioses i de culte."},{"role":"user","content":"I si no ens inscrivim, vol dir que no podem ni reunir-nos?"},{"role":"assistant","content":"No és això el que diu la llei. La Constitució garanteix la llibertat religiosa i de culte; la inscripció, en canvi, dona personalitat jurídica. Si una entitat religiosa no inscrita actua en nom seu o contreu obligacions amb tercers, tots els membres en responen solidàriament juntament amb l'entitat, amb dret a reclamar a qui hagi actuat en nom seu o n'hagi estat responsable directe."}]}
```

La persona pregunta per un cas concret. El seguiment neix d'un possible dubte
pràctic sobre què canvia quan no s'inscriuen. El límit legal queda explícit.

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
