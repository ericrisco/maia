# Exemples editorials de Maia Knowledge

Aquests exemples defineixen el llindar de qualitat per a les converses de revisió. No són plantilles per copiar a cada fitxa.

## No publicar: resposta convertida en fragment de fitxa

Pregunta:

> Què explica la secció «La regla de competència: depèn de qui és demandat» de la fitxa «Podies denunciar un cònsol, però no demandar-lo»?

Resposta inadequada:

> apel·lació al Consell General.

La resposta és un tros d'una regla processal. No explica qui jutja primer ni què s'apel·la. La persona ha de conèixer la fitxa per entendre-la.

## Publicar com a conversa revisada

```json
{"messages":[{"role":"user","content":"Com decidien quin tribunal havia de jutjar un plet entre un comú i un particular?"},{"role":"assistant","content":"Depenia de qui presentava la demanda. Si el particular demandava el comú o el quart, l'afer anava a la jurisdicció política. Si era el comú o el quart qui demandava el particular, l'afer anava als tribunals ordinaris."},{"role":"user","content":"I si el demandat era un quart, qui ho jutjava primer?"},{"role":"assistant","content":"Primer ho jutjava el consell de parròquia. Es podia apel·lar al Consell General."}]}
```

El primer torn dona la regla sencera. El seguiment demana una conseqüència concreta i conserva el context. Cada resposta s'entén tota sola. Els fets provenen de «La regla de competència: depèn de qui és demandat» i «I l'escala interna» de [la fitxa font](../../../docs/temes/institucions/justicia/podies-denunciar-un-consol-pero-no-demandar-lo.md#la-regla-de-competència-depèn-de-qui-és-demandat).

## Registres que cal rebutjar

- Una resposta que comença a mig sintagma o deixa un pronom sense antecedent.
- Una capçalera o un subtítol retornat com si contestés la pregunta.
- Una xifra sense unitat, any, categoria o comparació que n'expliqui el sentit.
- Una resposta que resol una divergència sense que el corpus l'hagi resolta.
- Una seqüència de torns afegits només per fer veure que hi ha multitorn.
- Una conversa que necessiti l'ID intern, el títol exacte o la font invisible per ser entesa.

## Revisió abans d'acceptar

1. La pregunta sona com una consulta real i identifica el tema prou bé?
2. La primera resposta resol la consulta en català clar i complet?
3. Cada seguiment continua la mateixa conversa i aporta un fet diferent?
4. La font sosté cada afirmació i es conserven els seus matisos?
5. El registre cobreix una unitat del mapa de cobertura que encara no està coberta?
