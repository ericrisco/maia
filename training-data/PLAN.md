# Pla: converses de Maia Knowledge que sonen humanes

## Objectiu

Crear converses en català que ensenyin a Maia a respondre dubtes reals sobre Andorra. La unitat de treball és una curiositat humana resolta en conversa, no una secció del corpus convertida en pregunta.

## Què fallava en les preguntes anteriors

Preguntes com «Què explica aquesta secció?» o «Què indica aquesta fila?» només les faria algú que ja tingués la fitxa al davant. Les respostes com «I dos topònims que en surten:» són fragments, no respostes. Aquest patró ensenya a repetir títols i notes internes, no a ajudar una persona.

Per evitar-ho, no esmentem fitxes, seccions, taules, files, corpus ni documents dins la conversa. La persona pregunta pel tema directament. Cada resposta resol el que li acaben de preguntar i s'entén tota sola.

## Flux per a cada conversa

1. **Triar una curiositat concreta.** Abans de redactar, anotar per a ús editorial què vol entendre la persona: una regla, una diferència, una conseqüència, una data o un límit del que se sap.
2. **Llegir la font sencera i el context.** Comprovar la fitxa de Maia, les fonts originals disponibles i els matisos. No convertir un resum provisional en una certesa.
3. **Escriure el primer torn com ho preguntaria una persona.** Ha de funcionar sense haver vist cap document. Evitar preguntes que només demanen «què és X?» si la curiositat real és més concreta.
4. **Respondre de seguida i amb sentit complet.** Donar la informació que resol el dubte i el context mínim que la fa entendre. No començar una llista per deixar-la a mitges.
5. **Fer conversa, no una pregunta de fitxa.** La tanda de calibratge tindrà converses de dos o més torns d'usuari quan el tema ho permeti. Cada seguiment ha de néixer de la resposta anterior: demanar una conseqüència, aclarir una distinció o comprovar una deducció. No s'allarga un fil amb preguntes artificials; una pregunta factual simple pot quedar resolta en un sol torn.
6. **Llegir la conversa sense les fonts.** En veu alta, comprovar si sembla una conversa possible. Si sona com un examen, una consulta a una taula o una transcripció de notes, reescriure-la.
7. **Registrar la procedència per separat.** Cada afirmació factual ha de poder tornar a una font. Les llicències i condicions de les fonts externes es documenten abans d'incorporar-ne material.

## Com sonen les preguntes humanes

Poden sortir d'una confusió («No ho acabo d'entendre…»), d'una deducció («Això vol dir que…?»), d'una discrepància («Per què aquí surt un dia i allà un altre?»), d'una comparació o d'una conseqüència pràctica. No cal afegir fórmules col·loquials si no hi encaixen.

Una pregunta bona és específica sense dependre de vocabulari editorial. No conté la resposta sencera ni obliga l'assistent a endevinar de quin tema es parla.

### Patrons que cal rebutjar

- «Què explica la secció…?», «què indica aquesta fila?» o «què diu la fitxa…?»: pressuposen que la persona està llegint el material de recerca.
- Preguntes que només demanen repetir un títol, un encapçalament o una etiqueta.
- Respostes que comencen amb «I dues coses…», dos punts, una llista sense pregunta o un pronom sense antecedent.
- Segon torn que repeteix el primer amb altres paraules o canvia de tema sense motiu.
- Col·loquialismes afegits només per fer veure que la pregunta és humana.

Abans d'escriure, formula en una línia privada la curiositat: «què vol entendre aquesta persona?». Després redacta la pregunta sense mirar el títol de la fitxa. Si només es pot formular fent referència a la fitxa, busca una altra curiositat o no generis el registre.

## Com responen les converses

- La primera frase contesta la pregunta.
- Els fets, els relats tradicionals i les interpretacions es distingeixen amb claredat.
- Una premissa equivocada es corregeix amb tacte i amb la dada correcta.
- Si la font no resol una qüestió, s'explica què se sap i què queda obert, sense inventar una resposta plausible.
- La resposta és completa però proporcionada. No recita tot el document.
- No acaba amb dos punts, un encapçalament o una promesa de continuar.

## Revisió abans d'acceptar cada registre

- Una persona podria fer la pregunta sense haver llegit Maia?
- La primera resposta resol el dubte inicial?
- Cada seguiment té una raó conversacional clara?
- Cada resposta conté una idea completa i respon al torn immediatament anterior?
- El fil manté el tema i no repeteix la mateixa pregunta amb altres paraules?
- Es poden verificar les afirmacions? Es preserven els dubtes reals de la font?
- Llegit en veu alta, sona com una conversa i no com un examen o una fitxa?

Si alguna resposta és «no», el registre encara és un esborrany.

## Cobertura íntegra del brain

La font de Knowledge és tot `maia/docs/temes/`, no una selecció de temes populars. L'inventari `knowledge/work/coverage.csv` inclou cada fitxer Markdown, també els índexs i documents que acabin justificant-se com a no entrenables. Cap fitxer es considera cobert només perquè n'hàgim llegit el títol.

Per cada article cal revisar les seccions, paràgrafs, llistes, taules i enllaços rellevants. Cada dada o idea entrenable ha de quedar representada en una o més converses; si no s'inclou, l'inventari n'ha de registrar el motiu. El progrés es marca per fitxer i per conversa, amb procedència. Els índexs serveixen per trobar relacions i no per generar preguntes sobre l'índex mateix.

La font de Language és tot `maia/docs/parla/`. `language/work/coverage.csv` enumera totes les peces Markdown; cadascuna s'ha d'avaluar per autenticitat, transcripció, drets i elegibilitat. Una peça pendent no és una peça aprovada. No es generen respostes sintètiques per omplir buits.

La cobertura només es pot donar per acabada quan tots els elements dels dos inventaris tenen estat revisat, inclòs o exclòs amb motiu, i els registres tenen procedència comprovable.

## Fases

1. **Calibratge:** revisar els exemples de `knowledge/review/calibration.jsonl` i ajustar la guia d'estil abans de continuar la cobertura. Aquests exemples són una mostra editorial, no s'afegeixen automàticament a les exportacions.
2. **Construcció:** avançar tema per tema. Per cada tanda, preparar preguntes, respostes i procedència; després revisar-les abans d'afegir la següent.
3. **Cobertura:** comparar els registres amb els coneixements de cada font i identificar què falta, sense multiplicar paraphrases.
4. **Exportació:** només després de revisar exactitud, naturalitat, cobertura, deduplicació i drets de les fonts. Separar train, validation i test per tema o font per reduir filtracions.

La primera tanda és deliberadament petita. No és una afirmació que el corpus estigui cobert ni que l'estil ja estigui tancat.
