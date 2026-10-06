# Pla per construir els datasets de Maia

## Objectiu

Crear dos datasets separats i traçables a partir de `docs/`:

- **Knowledge**: respostes conversacionals sobre el coneixement d’Andorra a `docs/temes/`.
- **Language**: llengua andorrana contemporània extreta de parla humana elegible a `docs/parla/`.

No convertim cada paràgraf en una pregunta. El criteri és si una persona tindria aquell dubte en una conversa real.

## Procés per a cada conversa Knowledge

1. Llegir la font sencera i comprovar les afirmacions al text i les fonts que cita.
2. Anotar internament quin dubte humà resol la conversa: entendre una contradicció, aclarir una conseqüència, distingir conceptes o saber què permet una norma.
3. Escriure la pregunta sense referències a una fitxa, apartat, taula o «fila». Afegir només el context que necessitaria algú que no veu el document.
4. Respondre la pregunta directament, amb les dades i els límits necessaris. Evitar fragments, llistes de camps i xifres sense subjecte.
5. Afegir un seguiment només quan neixi de la resposta i plantegi una curiositat nova. No forçar converses llargues: dues parelles de torns són una bona mida inicial, no una quota universal.
6. Llegir el diàleg com una conversa seguida. Si sona a examen, consulta d’índex o plantilla, reescriure’l o descartar-lo.
7. Guardar la conversa neta al JSONL i la procedència, evidència i drets en fitxers separats.
8. Mantenir-la com a esborrany fins que passi revisió humana i drets.

## Senyals de preguntes humanes

Una pregunta bona expressa una intenció: «com quadren aquestes dues dades?», «què canviaria si…?», «vol dir que…?» o «quina diferència hi ha?». El context pot venir del torn anterior. No s’inventa una situació personal quan no ajuda a entendre el fet.

Rebutjar preguntes que només funcionen davant d’un document concret, com ara «què explica la secció…?» o «què indica aquesta fila?». Rebutjar també preguntes vagues com «què més?» i variacions de plantilla que demanen la mateixa resposta.

## Converses multitorn

La primera resposta ha de resoldre el dubte inicial. El seguiment ha de ser una reacció plausible a aquesta resposta i ha d’obtenir informació nova: una distinció, una conseqüència o un límit. Cap torn no ha de dependre d’una font invisible. La conversa es pot tancar abans si no hi ha una continuació natural.

## Quality gate

Abans d’acceptar un registre, revisar:

- **Naturalitat**: algú ho preguntaria amb aquest motiu i aquest context?
- **Resposta**: comença per contestar i s’entén sense la fitxa?
- **Fidelitat**: cada fet surt de la font; les atribucions i incerteses es conserven?
- **Multitorn**: el seguiment neix del torn anterior i no repeteix la resposta?
- **Separació**: el missatge només conté la conversa, sense IDs ni notes internes?
- **Procedència i drets**: es pot tornar a la prova i està clara la condició de reutilització?
- **Duplicació**: aporta un intent o un fet nou respecte dels registres existents?

Decisions: `acceptar`, `reescriure` o `descartar`. Un exemple editorialment bo encara no és exportable si els drets no estan clars.

## Passos

1. Revisar junts els quatre exemples de `knowledge/review/conversations.jsonl`; retocar el to segons el que soni natural.
2. Fer un pilot petit en un sol tema i revisar-lo abans d’ampliar el volum.
3. Avançar per temes; per cada unitat d’evidència, crear una conversa útil, justificar-ne l’exclusió o deixar explícit per què no dona per fer-ne una. Cobertura no vol dir fabricar preguntes.
4. Afegir comparacions i síntesis entre fitxes quan les relacions estiguin documentades.
5. Deduplicar i separar train/validation/test per tema/font, perquè reformulacions del mateix fet no caiguin en conjunts diferents.
6. Treballar Language en una via separada; no inventar torns humans ni imitar una veu andorrana amb text generat.
7. Exportar només registres revisats, traçables i compatibles amb els drets de cada font.

## Estat actual i següent pas

La lectura estructural de `docs/temes/` ha inventariat 1.477 fitxes i 87.339 unitats d’evidència. Aquestes unitats no són preguntes ni registres entrenables. El primer pas ara és revisar i ajustar els quatre diàlegs pilot abans de crear més registres.

La via Language té 45 entrades, 40 peces de parla, 38 que passen els filtres bàsics i 8.449 fragments marcats com a incerts. No s’hi han trobat torns explícits i les condicions de redistribució continuen pendents; per tant, no hi ha encara sortida d’entrenament.
