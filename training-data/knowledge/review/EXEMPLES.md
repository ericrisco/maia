# Exemples de conversa per a Maia Knowledge

Aquests són **exemples editorials escrits per definir l'estil**. No són converses recollides de persones, no són registres aprovats i no s'han d'exportar com si fossin llengua humana espontània. Les fonts només justifiquen els fets de les respostes.

Les converses tenen llargades diferents. El seguiment apareix perquè la resposta anterior fa sorgir una pregunta concreta. No cal copiar-ne el patró ni el nombre de torns.

## 1. Una llegenda i el que se'n pot afirmar

```json
{"messages":[{"role":"user","content":"Com va aparèixer la imatge de Meritxell?"},{"role":"assistant","content":"Segons la llegenda, un pastor la va trobar sota una gavernera florida el dia de Reis. Se la va endur a Canillo, però l'endemà la imatge havia tornat al lloc de la troballa."},{"role":"user","content":"I per què no la van deixar a Canillo?"},{"role":"assistant","content":"El relat diu que també la van deixar a Encamp, però la imatge tornava sempre al mateix indret. Van entendre que volia quedar-s'hi i hi van construir el santuari."},{"role":"user","content":"Això és només llegenda o hi ha alguna data documentada?"},{"role":"assistant","content":"La troballa forma part de la llegenda. Una dada institucional posterior sí que consta: el Consell General la va declarar patrona i protectora del Principat el 24 d'octubre de 1873."}]}
```

**Per què funciona:** la primera pregunta demana un relat conegut. El primer seguiment surt de l'intent de portar la imatge a una altra parròquia. L'últim separa el relat llegendari del fet institucional, sense presentar la llegenda com a història verificada.

Font de fets: `docs/temes/cultura/llegendes/la-troballa-de-meritxell.md`. La mostra no està aprovada per exportar.

## 2. Una festa vista des del punt de vista de qui hi va

```json
{"messages":[{"role":"user","content":"A les caramelles de Sant Julià, la coral canta en un escenari o va pels carrers?"},{"role":"assistant","content":"Va pels carrers. La Coral Rocafort s'atura sota balcons i en places per cantar; el recorregut complet dura unes tres hores."},{"role":"user","content":"Tres hores? Això també ho fan així a les altres parròquies?"},{"role":"assistant","content":"Les caramelles es fan a totes les parròquies, però el recorregut complet de tres hores només es manté a Sant Julià."}]}
```

**Per què funciona:** la primera pregunta parteix d'una imatge fàcil d'entendre. El seguiment compara una característica que la primera resposta acaba de revelar. La resposta no enumera tota la història de les caramelles.

Fonts de fets: `docs/temes/costums/caramelles/les-caramelles.md` i `docs/raw/web/costums/govern-caramelles-ordino-sant-julia-2026.txt`. La font de premsa o institucional no s'exporta automàticament; cal revisar-ne els drets.

## 3. Una paraula que porta a una pregunta nova

```json
{"messages":[{"role":"user","content":"Per què la dansa de la Marratxa es diu així?"},{"role":"assistant","content":"Pel recipient d'aigua perfumada que els dansaires duien a les mans als orígens de la dansa. «Marratxa», «morratxa» i «almorratxa» són variants del nom."},{"role":"user","content":"Encara en porten un quan ballen?"},{"role":"assistant","content":"No. El recipient ja no forma part del ball, però el nom s'ha conservat."}]}
```

**Per què funciona:** la resposta resol l'etimologia i el mateix detall fa natural preguntar si l'objecte encara hi és. No afegim un torn de data o de lloc només per allargar la conversa.

Font de fets: `docs/temes/costums/danses/la-marratxa.md`. La font declarada al corpus té drets i atribució que cal revisar abans d'exportar.

## Exemples que descartem

- «Què explica la secció “El relat” de la fitxa?» demana navegar per un document, no resol un dubte sobre Andorra.
- «Què indica aquesta fila?» depèn d'una taula que qui pregunta no té per què veure.
- «Quins són el lloc, la data, els participants i els objectes?» acumula preguntes com un examen.
- «I des de quan?» afegit a qualsevol resposta és un qüestionari, no una continuació automàtica.
- Una resposta de poques paraules que completa una frase tallada no és útil només perquè sigui literalment correcta.

Abans d'afegir registres a `conversations.jsonl`, segueix la guia de [disseny de preguntes](QUESTION-DESIGN.md). Desa la procedència per separat a `provenance.jsonl`.
