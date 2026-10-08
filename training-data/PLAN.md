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
- Les mostres de `knowledge/review/examples.jsonl` i `knowledge/review/EXEMPLES.md` fixen el to; no són registres aprovats ni entren automàticament en cap export.

## Disseny de converses multitorn

Una conversa és una petita interacció que tindria sentit en una conversa real. No és una fitxa convertida en interrogatori.

- Comença amb un dubte que algú podria tenir sense haver llegit les fonts: una confusió habitual, una comparació, una dada sorprenent o una pregunta pràctica.
- La primera resposta resol el dubte i dona el context imprescindible. No obre una llista de punts perquè l'usuari els vagi demanant.
- Cada torn següent ha de tenir un vincle visible amb la resposta anterior: aclarir un terme, provar una conseqüència, demanar un exemple o comprovar una interpretació.
- No imposem tres torns ni cap altra quota. Una conversa acaba quan el dubte queda resolt; afegir torns buits empitjora l'exemple.
- La persona usuària pot equivocar-se o formular una premissa discutible. L'assistent la corregeix amb tacte i explica la distinció útil.
- Les preguntes sobre una secció, una fitxa, una fila o «el que diu el document» només s'admeten quan la persona ha explicat que està llegint aquell document i això és rellevant.
- Les respostes no poden començar a mitja frase, prometre contingut que no arriba, ni substituir la resposta per una etiqueta o un fragment de l'article.
- No inventem context personal per fer més humana la pregunta. «M'he mudat fa poc» només s'usa si la resposta en depèn i no exigeix atribuir fets al parlant.

### Revisió en veu alta

Llegim només els missatges, en ordre, sense mirar títols ni metadades. Per cada torn preguntem: «Una persona diria això aquí?», «S'entén a què es refereix?» i «La resposta contesta exactament el que li acaben de preguntar?». Si falla una d'aquestes comprovacions, es reescriu la conversa sencera o s'exclou.

Per a cada candidat, qui revisa ha de poder identificar internament les afirmacions factuals i les fonts que les sostenen. Aquest rastre va al registre de revisió, mai al missatge d'entrenament.

## Flux de treball

1. Revisar el to amb les mostres i ajustar-les abans de generar més registres.
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
