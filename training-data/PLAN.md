# Pla de Maia Training Data

## Objectiu

Crear dades de fine-tuning útils per a Maia a partir de `docs/`, amb dos fluxos separats:

- **Maia Knowledge**: converses que ensenyen coneixement documentat sobre Andorra.
- **Maia Language**: mostres basades en llengua humana andorrana contemporània.

El problema que corregim és concret: preguntes com «Què explica aquesta secció?» o «Què indica aquesta fila?» només les faria algú que està mirant la fitxa. No representen una conversa amb una persona que vol entendre Andorra.

## La regla editorial

Abans d'escriure un registre, formula en una frase el dubte que tindria una persona. Si el dubte només existeix perquè hi ha un títol, una fila o una secció al document, no el converteixis en pregunta.

Una bona pregunta pot néixer d'una curiositat, una confusió, una comparació o una afirmació que la persona vol comprovar. Ha de donar prou context per entendre's sense obrir el corpus.

No fabriquis una experiència personal per fer-la sonar humana. «Vaig anar-hi ahir…» només és acceptable si forma part d'una conversa humana real i documentada. La naturalitat ve del dubte i de com s'expressa, no d'inventar biografia, faltes o argot.

## Com escriure cada conversa

1. **Pregunta inicial:** planteja una necessitat plausible amb paraules corrents. Evita repetir el títol de la font com si fos una consulta de cercador.
2. **Resposta:** contesta primer el dubte. Dona el context necessari perquè s'entengui completa. Separa fets, llegendes, interpretacions i incerteses.
3. **Seguiment:** afegeix-lo només quan la resposta faci néixer una pregunta immediata i relacionada. Pot demanar una aclaració, una conseqüència o una comparació directa.
4. **Tancament:** atura la conversa quan el dubte queda resolt. No afegeixis torns per arribar a una llargada determinada.

El conjunt ha d'ensenyar converses de diversos tipus: d'un torn quan n'hi ha prou, i de més torns quan el fil ho demana. «Multitorn» és una capacitat del dataset, no una quota per registre.

### Evita

- Referències a fitxes, corpus, títols, seccions, files, gràfics o identificadors interns.
- Preguntes de plantilla repetides: «Què és X?», «Quan passa X?» per cada concepte.
- Respostes que comencen a mig fil, són només una llista o repeteixen l'enunciat.
- Seguiments sobre un tema nou o preguntes afegides només per allargar el xat.
- Premisses incorrectes que ningú tindria motiu de creure.
- Detalls que la font no sosté o que presenten una hipòtesi com un fet.

## Prova de lectura humana

Llegeix la conversa sense consultar la font. Reescriu-la o descarta-la si alguna resposta és «no»:

1. Entenc què vol saber la persona i per què ho preguntaria?
2. La pregunta sonaria normal dita en veu alta?
3. La resposta contesta el dubte i s'entén sense completar-la amb la fitxa?
4. Cada seguiment surt de manera natural del torn anterior?
5. Els fets i el grau de certesa coincideixen amb les fonts?
6. He tret tot el llenguatge intern del procés de recerca?

La cobertura no és una quota de preguntes. Un fet pot quedar registrat a l'inventari sense conversa si no hi ha una manera natural d'ensenyar-lo.

## Format

Una línia JSONL representa una conversa completa. Els missatges alternen `user` i `assistant`:

```json
{"messages":[{"role":"user","content":"La Passa i la Marratxa són el mateix tipus de ball?"},{"role":"assistant","content":"No ben bé..."},{"role":"user","content":"I les parelles que van al davant tenen algun nom especial?"},{"role":"assistant","content":"Sí..."}]}
```

La conversa exportable contindrà només `messages`. Fonts, permisos, decisions i estat de revisió viuen als fitxers interns de procedència, mai dins del missatge de l'assistent.

## Drets i procedència

Abans d'aprovar un registre, comprova totes les fonts que en sostenen les afirmacions i registra'n la procedència i les condicions d'ús. Un exemple de calibratge no és automàticament reutilitzable com a dada d'entrenament. Les mostres de `knowledge/examples/` estan marcades com a no exportables fins que es revisin els drets.

## Maia Knowledge

Font principal: `docs/temes/`.

Per cada candidat, guarda la conversa a `knowledge/review/` i la seva procedència a `knowledge/work/`. Revisa exactitud, naturalitat, continuïtat i drets. Només després de la revisió passa a l'export. Les relacions entre documents s'utilitzen quan una pregunta humana realment les necessita, no només perquè comparteixen tema.

## Maia Language

Font principal: `docs/parla/`. Només s'utilitza parla humana que compleix els criteris del corpus per a veu originària, època contemporània, aptitud lingüística, qualitat de transcripció i drets.

No s'inventen respostes perquè «sonin andorranes». Cal preservar el text humà original i separar aquest flux de Knowledge. Els exemples de Language només s'afegiran quan hi hagi fragments elegibles i amb procedència comprovada.

## Fases

1. Fixar el criteri amb els exemples de `knowledge/examples/`.
2. Afegir registres petits a `knowledge/review/`, amb procedència i justificació del dubte humà.
3. Revisar cada conversa amb la prova de lectura humana i comprovar les fonts.
4. Detectar duplicats i preguntes de plantilla abans de sumar cobertura.
5. Inspeccionar el corpus per blocs i registrar també allò que no té una pregunta natural.
6. Preparar el flux separat de Language quan hi hagi material elegible.
7. Crear els splits finals només quan revisió, procedència, deduplicació i agrupació evitin filtracions.
8. Validar JSONL, alternança de torns, camps permesos, duplicats i cobertura; publicar un report dels resultats.

## Definició de fet

Un registre està llest quan és natural sense la font, respon el dubte completament, només afirma allò que les fonts sostenen, té procedència verificable i no és una variant redundant d'un altre. El projecte complet només estarà llest quan Knowledge i Language hagin passat els seus controls independents, tinguin splits sense filtracions i disposin d'informes de cobertura i exclusions.
