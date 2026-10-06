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

## Reescriure consultes que depenen de la fitxa

Les preguntes sobre «què explica una secció», «quina fila és aquesta» o «quins
mots surten aquí» solen comprovar si el model ha vist el document, no si sap
respondre una persona. Cal recuperar la intenció humana —entendre una regla,
interpretar una dada o seguir un relat— i donar el context necessari. Aquests
exemples reescriuen casos que havien produït respostes fragmentàries.

### Regla judicial

```json
{"messages":[{"role":"user","content":"Si un particular volia reclamar un deute a un cònsol, necessitava un permís especial?"},{"role":"assistant","content":"Després de la Reforma de 1866, no si era un deute personal del cònsol. L'autorització només calia per reclamar deutes que hagués contret en exercici del càrrec; aleshores se'n demanava llicència al Síndic."},{"role":"user","content":"I reclamar-li penalment també exigia aquest permís?"},{"role":"assistant","content":"No. La distinció que recull la font és entre les reclamacions civils per deutes contrets com a autoritat, que podien requerir llicència, i les persecucions criminals, que no la requerien."}]}
```

La conversa explica la conseqüència pràctica de la regla i manté el període
històric. [Font](../../../docs/temes/institucions/justicia/podies-denunciar-un-consol-pero-no-demandar-lo.md#la-inversió-civil-amb-permís-criminal-sense).

### Usos comunals en terra privada

```json
{"messages":[{"role":"user","content":"Un camp podia ser privat i, alhora, servir de pastura per a tothom?"},{"role":"assistant","content":"Sí. Algunes terres privades estaven gravades amb la peixena: després de la collita, els habitants de la parròquia hi podien passar i fer-hi pasturar els ramats."},{"role":"user","content":"Això limitava què hi podia plantar el propietari?"},{"role":"assistant","content":"Sí. Sense autorització del consell de parròquia, el propietari no podia canviar la rotació dels conreus ni sembrar farratge, perquè aquestes decisions podien impedir la pastura després de la collita."}]}
```

La primera pregunta demana una relació aparentment paradoxal; el seguiment
explora una conseqüència concreta. [Font](../../../docs/temes/territori/geografia-fisica/un-camp-es-comunal-perque-hi-passen-els-ramats.md#la-peixena-i-la-seva-conseqüència).

### Dada d'un gràfic amb context

```json
{"messages":[{"role":"user","content":"El 2014, l'indicador lingüístic donava avantatge al català o al castellà?"},{"role":"assistant","content":"Al català: la sèrie dona un 57,7 per al català i un 56,4 per al castellà."},{"role":"user","content":"I el 2018 continuava igual?"},{"role":"assistant","content":"No. El 2018 el català era a 56,8 i el castellà a 57,6. En aquella publicació, el gràfic dibuixava aquests dos valors al revés, però la sèrie de l'API d'Estadística confirma les xifres del text."}]}
```

La pregunta diu què mesuren els valors i el seguiment preserva la discrepància
entre gràfic i text, amb la resolució posterior. [Font](../../../docs/temes/llengua/politica-linguistica/el-diposit-legal-daquesta-edicio-es-and-000-2019.md#arbitrat-el-18-09-2026-el-text-tenia-raó-i-el-gràfic-no).

### Llegenda de Meritxell

```json
{"messages":[{"role":"user","content":"Per què, segons la llegenda, van construir el santuari de Meritxell allà on és?"},{"role":"assistant","content":"Segons la llegenda, la imatge de la Mare de Déu tornava al lloc on l'havia trobada un pastor, encara que la duguessin a Canillo o a Encamp. La gent ho va interpretar com que volia restar en aquell indret i hi va construir el santuari."},{"role":"user","content":"Què havia trobat el pastor en aquell lloc?"},{"role":"assistant","content":"Una imatge de la Verge sota una gavernera florida en ple hivern, el dia de Reis."}]}
```

La resposta identifica el relat com a llegenda i el seguiment pregunta per un
detall concret que s'hi acaba d'esmentar. [Font](../../../docs/temes/cultura/llegendes/la-troballa-de-meritxell.md#el-relat).

### Tipus d'interès: distingir contractes

```json
{"messages":[{"role":"user","content":"Com s'entén que un decret parli del 3,33 % i també del 5 %?"},{"role":"assistant","content":"El decret del Consell General del 1895 separa dos casos: manté el 3,33 % per als censals i diu que, en la resta, el Consell i el Tribunal de Corts havien acceptat el 5 %. Per tant, els dos tipus no s'aplicaven al mateix contracte."},{"role":"user","content":"Així, el 5 % també era el tipus dels censals?"},{"role":"assistant","content":"No. El text reserva el 3,33 % als censals; el 5 % s'aplicava a la resta dels casos que descriu."}]}
```

El primer torn explica la distinció i el següent comprova si s'ha entès, sense
repetir «tres coses que el corpus registra». [Font](../../../docs/temes/economia/banca-i-fiscalitat/pero-en-tot-lo-demes-al-cinc-per-cent.md#i-aquí-hi-ha-el-document-que-ho-resol).

### Preguntes sobre xifres, llocs o noms

No retorneu una fila com «2014 — verd, 57,7 — morat, 56,4». Expliqueu què
representen els colors, quina llengua correspon a cada valor i com s'interpreta
la comparació. Igualment, no contesteu una pregunta sobre la Marratxa amb «I dos
topònims que en surten:»: expliqueu què signifiquen els topònims només si la
persona n'ha preguntat el sentit i la font els documenta.

## Revisió abans d'acceptar

1. La pregunta sona com una consulta real i identifica el tema prou bé?
2. La primera resposta resol la consulta en català clar i complet?
3. Cada seguiment continua la mateixa conversa i aporta un fet diferent?
4. La font sosté cada afirmació i es conserven els seus matisos?
5. El registre cobreix una unitat del mapa de cobertura que encara no està coberta?
