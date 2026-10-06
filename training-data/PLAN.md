# Pla per crear converses útils

## Objectiu

Fer que Maia respongui com un assistent útil sobre Andorra i, per separat, preservar llengua andorrana autèntica. La qualitat d'una conversa importa més que el nombre de registres.

## El problema que aquest pla evita

Una fitxa, un títol o una fila de taula no són una conversa. Preguntes com «què explica la secció…?», «què indica aquesta fila?» o una pregunta genèrica feta només per cobrir una dada depenen del document i no representen el que acostuma a preguntar una persona.

## Maia Knowledge

Font factual: `docs/temes/`, amb les fonts originals i els registres de `docs/fonts/` i `docs/raw/`.

Per crear una conversa:

1. Llegeix el document i comprova la font citada, les correccions, les contradiccions i els buits.
2. Escriu en privat quin dubte pràctic, curiositat o confusió resoldria aquesta informació.
3. Formula la pregunta com la diria algú que no té el document al davant. Dona el context mínim perquè s'entengui.
4. Respon primer el dubte. Afegeix només el context necessari. No copiïs l'estructura de la fitxa.
5. Afegeix un altre torn d'usuari només si la resposta anterior li dona un motiu clar per preguntar una cosa nova. Si no, acaba la conversa.
6. Comprova cada afirmació amb l'evidència. Conserva la incertesa amb paraules normals. No converteixis una llegenda, una inferència o una dada antiga en certesa actual.
7. Llegeix tota la conversa en veu alta. Si sona com un examen, una cerca dins d'un document o un formulari, reescriu-la o descarta-la.
8. Registra separadament les fonts, els fragments de suport, la llicència, l'atribució, la revisió i la decisió d'ús.

No cal que cada conversa sigui multitorn. Una sola pregunta ben resolta és millor que dos seguiments artificials. No inventis una experiència personal per fer una pregunta més viva.

### Prova ràpida

- Ho preguntaria una persona sense veure la fitxa?
- S'entén què vol saber i per què?
- La resposta contesta directament i sona natural?
- El seguiment depèn realment del que s'acaba de dir?
- Cada fet es pot rastrejar fins a una font fiable?
- Els drets permeten l'ús concret previst?

Un «no» a naturalitat o evidència vol dir reescriure o excloure. Un dret pendent vol dir que no s'exporta.

## Maia Language

Font: `docs/parla/`, segons el contracte del corpus i els drets de cada peça. Es conserva parla humana real. No es converteixen monòlegs en preguntes i respostes inventades ni es barregen fragments de parlants diferents per fabricar diàlegs.

Abans d'acceptar material, cal verificar que la transcripció sigui llegible, que l'origen i el parlant siguin prou clars i que els drets cobreixin l'ús previst. Les exclusions i els motius queden registrats.

## Flux de revisió

1. Inventaria el corpus i les fonts sense generar preguntes automàticament.
2. Proposa converses des de dubtes humans identificables.
3. Revisa naturalitat, exactitud, incertesa, duplicats i drets.
4. Desa els candidats i la seva procedència per separat a `review/`.
5. Accepta o exclou cada candidat amb un motiu traçable.
6. Exporta només registres aprovats per al seu destí. Mantén Knowledge i Language separats.
7. Publica recomptes, cobertura, exclusions i limitacions. No presentis cobertura documental com si fos qualitat de conversa.

## Format entrenable

Una línia JSONL per conversa, amb missatges alternats:

```json
{"messages":[{"role":"user","content":"..."},{"role":"assistant","content":"..."}]}
```

Els missatges no contenen identificadors interns, notes de procedència ni estats de revisió. Aquests viuen en fitxers separats.

## Estructura

- `knowledge/review/`: converses factuals candidates i procedència separada.
- `knowledge/work/`: inventari i notes de treball, no dades entrenables.
- `knowledge/output/`: només exportacions aprovades.
- `knowledge/reports/`: cobertura, qualitat, exclusions i drets.
- `language/`: mateixos espais, però només per a llengua humana autèntica.

Els fitxers d'exemple actuals són un pilot d'estil. Cal revisar-los abans de tractar-los com a aprovats.
