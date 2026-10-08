# Pla per a converses de Maia Training Data

## Punt de partida

Les primeres preguntes semblaven etiquetes enganxades a fragments d'una fitxa: «Què explica la secció…?». Una persona que no té la fitxa al davant no les faria. Les respostes també fallaven quan començaven a mitja idea o feien referència al corpus.

Recomencem el calibratge editorial amb converses de mostra. Les converses antigues no s'han d'exportar ni donar per bones automàticament; abans de recuperar-ne cap, cal reescriure-la i verificar-la.

## Com volem que soni

Imaginem una conversa breu amb un assistent que sap coses d'Andorra. La persona pregunta perquè té un dubte real, no perquè està resolent un exercici sobre un document.

- La pregunta inicial funciona sense cap fitxa, títol de secció ni context inventat.
- Pot ser directa o portar una mica de context que una persona diria de debò. No posem a la boca de l'usuari una biografia o una experiència que no cal.
- El seguiment neix de la resposta: demana aclarir, entendre una conseqüència o saber-ne un detall relacionat.
- «I això?», «per què?» i «com es fa?» només serveixen si el referent és clar en aquell punt de la conversa.
- Preferim les paraules corrents. Expliquem un terme tècnic quan és necessari per contestar.
- No cal que cada conversa recorri una llista fixa de tipus de pregunta. La varietat ha de sortir dels temes i dels dubtes, no d'una plantilla.

## Com escrivim les respostes

1. Contestar primer la pregunta concreta.
2. Afegir el context que permet entendre la resposta, sense resumir tota la fitxa.
3. Respondre cada seguiment a la llum del que ja s'ha dit, sense repetir la resposta anterior.
4. Distingir una dada, una interpretació i una llegenda. No convertir una associació en una causa.
5. Si el corpus no permet respondre, dir-ho amb naturalitat i concretar què falta. No omplir el buit amb una suposició.
6. Escriure en català clar i viu, sense col·loquialismes posats per fer teatre ni fórmules com «segons el corpus».

## Verificació abans d'afegir una conversa

- Comprovem cada dada a la font que sosté l'article i revisem si els seus drets permeten l'ús previst.
- Respectem períodes, unitats, denominadors, noms i graus d'incertesa.
- El seguiment aporta una resposta nova i no és una pregunta independent disfressada de continuació.
- Llegim el diàleg seguit. Si sona a qüestionari, a cercador o a text generat per omplir una quota, el reescrivim o el descartem.
- Les mostres de `knowledge/review/examples.jsonl` fixen el to; no són registres aprovats ni entren automàticament en cap export.

## Flux de treball

1. Revisar i aprovar el to amb les mostres.
2. Afegir converses a `knowledge/review/conversations.jsonl` només quan estiguin verificades; guardar-hi l'evidència i la procedència als registres de revisió.
3. Revisar els registres antics un per un. Reescriure o descartar; mai aprovar-los en bloc.
4. Mirar cobertura i duplicats per detectar buits. No fabricar converses per completar una quota.
5. Revisar els drets abans d'exportar i separar train, validation i test per tema o font quan calgui.
6. Mantenir `Maia Language` separada: només parla humana autèntica, autoritzada i prou fiable; no inventar-hi diàlegs.

## Estructura

- `knowledge/review/`: mostres editorials, candidats i evidència de revisió.
- `knowledge/work/`: inventaris regenerables del corpus.
- `knowledge/reports/`: cobertura i resultats de qualitat.
- `knowledge/output/`: només exports revisats i aprovats.
- `language/`: flux separat per a material lingüístic autèntic.

No considerem acabat cap dataset pel nombre de registres. El criteri és que les converses siguin naturals, correctes, útils, traçables i permeses per les fonts.
