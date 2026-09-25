---
type: corpus-independent
name: corpus-parla-andorrana
language: ca-AD
status: en-construccio
linked_to_existing_corpus: false
---

# Corpus independent de parla andorrana

Aquest directori és un subcorpus independent dins la documentació de Maia. No
s'enllaça amb cap fitxa de `docs/temes/`, `docs/fonts/` ni amb l'índex actual.
La finalitat és reunir mostres audiovisuals públiques de persones que parlen amb
una varietat andorrana identificable, conservar-ne la procedència i produir una
transcripció i una anàlisi lingüística per parlant.

La frontera amb la resta de la documentació es comprova a
`proveniencia/auditoria-aillament-brain.md`: les referències semàntiques fora
d'aquest directori han de ser zero.

L'auditoria de l'objectiu es manté a `ESTAT-OBJECTIU.md`; separa el que ja està
verificat del que encara requereix escolta humana.

El [mapa de prospecció](proveniencia/mapa-prospeccio.md) manté separats els 66 registres canònics, els 11 candidats i les quatre fonts que encara requereixen permís.

## Abast i criteri d'inclusió

Cada persona tindrà una fitxa pròpia, un identificador estable i una o més
mostres. Només s'inclourà una persona quan la font permeti identificar-la i hi
hagi veu audible suficient; l'etiqueta «parla andorrana» serà una hipòtesi de
recerca, no una afirmació automàtica. Es registrarà l'edat aproximada, lloc de
socialització lingüística quan la font ho permeti, situació comunicativa,
durada útil i qualitat de l'àudio.

El corpus objectiu és de 50–100 persones. La primera fase valida el protocol
amb una mostra petita de fonts de RTVA, Consell General, Govern i YouTube abans
de fer créixer el conjunt.

## Estructura

- `persones/`: fitxa i identificació de cada parlant.
  L'[Índex de persones](persones/INDEX.md) reuneix les 66 fitxes amb la font, l'estat i l'enllaç a cada informe.
- `audios/`: derivats locals d'àudio, amb hash i llicència/termes registrats.
- `transcripcions/`: transcripció amb marques temporals i incerteses.
- `persones/`: informe de trets fonètics, morfosintàctics, lèxics, prosòdics i
  pragmàtics observables per parlant.
- `proveniencia/`: URL, data de consulta, canal, títol, permís o termes d'ús i
  cadena de transformació. `analisi-metrics.tsv` recull mètriques regenerables
  de ritme, pauses i confiança de l'ASR; `cobertura.tsv` verifica els artefactes
  mínims de cada persona.
- `grafo/`: nodes i arestes del graf independent de parlants, fonts i trets.

## Estat inicial

El registre `persones.tsv` és l'autoritat de cobertura. Una persona només passa
a `analitzada` quan existeixen l'àudio, la transcripció i l'informe; les fonts
només localitzades queden com `candidata` fins que se'n comprova la veu i els
termes d'ús.

## Primera prospecció

El registre actual conté **66 registres de font corresponents a 60 persones canòniques**; totes les mostres tenen àudio local,
transcripció ASR, informe i fitxa de procedència. Les 12 fonts d'Andorra Recerca
i Innovació declaren Creative Commons Attribution; les 33 del Consell General i
les 17 de RTVA no declaren una llicència oberta i es tracten com a còpies locals
per a recerca. Les quatre mostres pa-051—pa-054 provenen de l'Arxiu d'Etnografia
d'Andorra i tenen termes d'ús educatiu i investigador sense difusió. Les sis mostres pa-055—pa-060 provenen del canal del Consell General i les sis mostres pa-061—pa-066 provenen de RTVA i es conserven com a derivats locals de recerca sense llicència oberta declarada. Els 66 informes són provisionals: 12 tenen estat
`analitzada-provisional-automatica`, 51 tenen revisió contextual manual de metadades (`analitzada-provisional-contextual`) i pa-044, pa-047 i pa-050 queden en
`quarantena-asr` per incidències de repetició; els trets
compartits encara no són resultats dialectològics fins que es revisin contra
l'àudio.

Les transcripcions són ASR amb probabilitats de token. Una forma només entra al
graf com a tret compartit si es comprova contra l'àudio i apareix en diversos
parlants; els errors ortogràfics de Whisper es mantenen marcats i no es
presenten com a dialectalisme.

`proveniencia/analisi-acustica-densa.tsv` afegeix descriptors densos de quantils d'energia, F0, espectre i intervals de veu per prioritzar fragments; no és una anotació fonètica.

`proveniencia/cua-audicio-small-equilibrada.tsv` és una mostra operativa de 100 clips: cobreix els 63 parlants amb ocurrències small i les 20 formes candidates, amb F0/F1/F2/F3 disponibles quan es poden mesurar. El quadern `proveniencia/quadern-audicio-small-equilibrada.md` la presenta per començar una revisió equilibrada; tots els camps humans continuen buits fins a escoltar l'àudio.

`proveniencia/analisi-prosodia.tsv` resumeix la proporció d'activitat de veu,
l'energia, els creuaments per zero i una estimació espectral orientativa de F0 per
als 66 WAV. Són mesures de priorització acústica; no substitueixen l'escolta ni
l'anotació fonètica.
La cua `proveniencia/cua-audicio.tsv` conté 656 intervals prioritzats (20 formes
per parlant quan hi ha ocurrència) amb estat d'audició pendent; 384 tenen també
coincidència temporal entre les dues passades ASR. Els 656 clips locals de
`proveniencia/clips/` cobreixen tota la cua: 384 corresponen a aquests
solapaments i 272 s'han extret directament del WAV quan no n'hi havia; tots
tenen hash al seu manifest.
El graf conserva també una vista estricta (`grafo/trets-consens.tsv`) amb 19 formes
que apareixen en almenys tres parlants en les dues passades ASR; continua pendent
de confirmació auditiva.
`grafo/arestes-parlants-consens.tsv` relaciona directament 1.386 parelles de parlants
que comparteixen almenys tres d'aquestes formes, sempre com a semblança textual
provisional.
El graf inclou també una agrupació acústica exploratòria de les 63 veus actives
en quatre clústers, documentada a `proveniencia/resum-clusters-prosodia.md`;
no es una clasificación dialectal.

La tercera passada ASR `proveniencia/qa-beam.tsv` cobreix les 63 veus actives;
`proveniencia/qa-quarantena.tsv` afegeix nou finestres de control per a les tres
veus en quarantena. Cap d'aquestes passades substitueix l'escolta humana.
La quarta passada `proveniencia/qa-clips.tsv` cobreix els 656 clips de la cua;
452 coincideixen textualment amb la forma candidata i 204 divergeixen, sempre
com a evidència automàtica pendent d'escolta.
La passada independent `proveniencia/qa-clips-base.tsv` recupera 321 formes;
`proveniencia/qa-clips-consens.tsv` conserva els 263 clips coincidents en els
dos models i manté separats els textos de cada passada. Les divergències entre
models queden visibles i no es tracten com a errors confirmats.
El graf derivat d'aquesta passada conserva 18 trets amb almenys tres veus i
1.222 relacions de parelles a `grafo/trets-qa.tsv` i
`grafo/arestes-parlants-qa.tsv`; és una capa textual provisional separada del
graf consensual anterior.
La capa estricta de doble model queda a `grafo/trets-base-consens.tsv`,
`grafo/arestes-parlants-base-consens.tsv` i
`grafo/graf-parlants-base-consens.mmd`; també és evidència textual pendent
d'audició.
Els descriptors acústics dels 263 clips consensuals es conserven a
`proveniencia/analisi-acustica-consens.tsv` i les seves medianes per forma a
`proveniencia/resum-acustica-formes-consens.tsv`; només serveixen per ordenar
l'escolta i l'anàlisi prosòdica.
La passada base conserva també l'alineació tokenitzada a
`proveniencia/qa-consens-tokens-base.tsv`: 249 clips tenen timestamp de la forma
i 14 requereixen escolta perquè no hi ha token localitzat.
`proveniencia/analisi-acustica-normalitzada-consens.tsv` compara cada consens
amb la mediana acústica del mateix parlant, reduint l'efecte de veu i microfonia
en la selecció prosòdica.
`proveniencia/analisi-formants-consens.tsv` conserva 250 files de mesura al centre dels tokens consensuals localitzats (161 valors F0 i 249 valors per a cadascun de F1, F2 i F3); `resum-formants-consens.tsv` en dona medianes per a 20 formes. Són mesures exploratòries per orientar l'audició i no confirmen cap patró dialectal.
`proveniencia/analisi-trajectories-formants.tsv` desglossa aquests tokens en cinc punts temporals (1.250 files) i afegeix intensitat; el resum conserva les medianes d'inici i final per a les 20 formes. Aquesta trajectòria també és instrumental i queda pendent d'audició.
`proveniencia/evidencia-gramatica.tsv` conserva 10.458 contextos textuals candidats de nou categories (pronoms, possessius, perífrasis, negació, incoatius i contacte); `resum-evidencia-gramatica.tsv` els resumeix per als 66 registres de font. Són patrons ASR localitzables, no etiquetes confirmades.
`proveniencia/repertori-evidencia.tsv` explicita quines dimensions del repertori
tenen evidència i quines continuen buides per a cada persona.
La cua final `proveniencia/prioritat-audicio.tsv` ordena els 656 clips en 303
casos de triple consens, 63 de doble ASR, 86 d'una sola passada i 204
divergents.
En els 109 clips forts s'ha fet una tercera descodificació greedy: `proveniencia/qa-clips-forts-consens.tsv` conserva 81 coincidències entre els tres models, 24 entre dos i 4 d'un sol model. Aquesta passada només ordena l'escolta.
La cua operativa `proveniencia/registre-audicio-forts-divergencies.tsv` redueix les divergències a 28 files amb els tres textos i els camps humans buits; el quadern Markdown les agrupa per persona.
`proveniencia/analisi-acustica-divergencies.tsv` afegeix a aquestes 28 files durada, F0, formants, intensitat i deltes respecte a la veu de cada persona.
La cua QA més ampla té 309 tokens localitzats en una passada i queda mesurada a `proveniencia/analisi-formants-qa.tsv`, separada del bloc de 250 consensos de dos models.
La regeneració JSON de la cua sencera localitza 451 ocurrències en 439 dels 656 clips; `proveniencia/analisi-formants-cua-small.tsv` en conserva les mesures, sempre com a evidència d'una passada small.
La capa `grafo/trets-small-token.tsv` relaciona les 20 formes amb 63 parlants actius; `grafo/arestes-parlants-small-token.tsv` conserva 1.140 parelles que comparteixen almenys tres formes i `grafo/matriu-formes-small-token.tsv` desplega 1.320 cel·les.
La cua `proveniencia/quadern-formes-small-token.md` les ordena per cobertura i probabilitat per començar la confirmació auditiva per forma, no per persona aïllada.
`grafo/nodes-small-token.tsv` resumeix també cada parlant: formes localitzades, ocurrències i confiança mediana, inclosos els tres perfils sense token small.
`proveniencia/persones-canonics.tsv` agrupa els 66 registres en 60 persones canòniques; la vista `grafo/*-canonics.tsv` recalcula formes, nodes, arestes i matriu sense duplicar les sis persones amb dues mostres.
`proveniencia/analisi-acustica-clips.tsv` conserva també descriptors acústics
per clip per comparar veu, energia, F0 orientativa, espectre i pauses durant
l'audició.
El full operatiu per a la revisió és `proveniencia/registre-audicio.tsv`: agrupa
clip, transcripció QA, prioritat, descriptors i els camps humans de confirmació.
La cua de formes addicionals té el seu registre separat a
`proveniencia/registre-audicio-formes-escasses.tsv`, amb 30 claus i els mateixos
camps d'anotació, per no barrejar-la amb els 656 intervals generals.
Les fitxes individuals inclouen també exemples localitzables de cada forma a
`proveniencia/evidencia-formes.tsv` (2.014 fragments ASR pendents d'escolta).
Els 303 clips de triple consens tenen timestamps de la quarta passada a
`proveniencia/qa-clips-json.tsv`.
`proveniencia/qa-formes-tokens.tsv` avalua el mateix bloc: 309 coincidències
tokenitzades i quatre clips sense coincidència, amb probabilitat i segons
absoluts.
La primera cua d'escolta estricta queda a `proveniencia/candidats-forts.tsv`:
109 clips amb triple consens i probabilitat tokenitzada mínima de 0,80.
El quadern navegable `proveniencia/quadern-audicio-forts.md` els agrupa per
persona i enllaça directament l'àudio, el text i els temps tokenitzats.
També hi ha un reproductor local a `proveniencia/auditoria-forts.html` amb
filtres i exportació de les anotacions.
`proveniencia/evidencia-formes-vtt.tsv` afegeix 3.326 ocurrències candidates amb
interval temporal de la VTT per obrir-les directament al WAV.
Les dimensions de revisió es basen en `proveniencia/referencies-linguistiques.md`
i el repertori tabular de `grafo/repertori-referencia.tsv`, sense donar per
confirmat cap tret abans de l'audició.
La seva aplicació per persona queda a `grafo/repertori-aplicat.tsv` (1.188 files),
amb els indicadors automàtics i el camp separat per a l'observació auditiva.
La matriu `grafo/matriu-formes.tsv` conserva les 35 formes candidates per a
cadascuna de les 66 fitxes de font i separa recompte ASR, clip disponible i
coincidència textual.
La matriu ampliada `grafo/matriu-formes-linguistics.tsv` conserva 18.744 cel·les
per als 284 trets discursius, territorials i gramaticals del graf lingüístic.



## Eines de revisió actual

La primera cua operativa canònica són `proveniencia/sessions/sessio-01.tsv` i
`sessio-02.tsv`, `sessio-05.tsv` i `sessio-06.tsv` (89 clips canònics). `proveniencia/auditoria-sessions-canoniques.html`
permet escoltar-los i exportar anotacions; `proveniencia/guia-audicio-sessions-canoniques.tsv`
fixa els aspectes lingüístics que cal revisar per forma. Les fitxes implicades
mostren aquesta selecció amb `proveniencia/actualitza-informes-sessions-canoniques.py`.
Les anotacions es projecten al registre mestre només després de passar per
`proveniencia/importa-auditoria-sessions-canoniques.py`.
`proveniencia/auditoria-cobertura-sessions.tsv` resumeix la cobertura per persona:
57 dels 60 parlants canònics tenen un clip seleccionat i les tres veus en
quarantena queden separades fins a l'audició.

El graf textual dels 11 candidats queda separat a `grafo/README-formes-candidats.md`: 100 nodes forma-candidat, 36 arestes i 24 formes, sense enllaç al graf canònic. Les coincidències són exploratòries i continuen pendents d'audició.

La capa acústica canònica queda separada a `grafo/README-acustic-canonic.md`,
`grafo/nodes-acustic-canonic.tsv`, `grafo/arestes-acustic-canonic.tsv` i
`grafo/graf-acustic-canonic.mmd`; és una semblança instrumental exploratòria,
no una classificació dialectal.

## Decisió de fase

Amb 60 persones canòniques (66 registres de font), la fase de recol·lecció queda tancada dins l'objectiu de 50–100. Les quatre veus de l'Arxiu d'Etnografia amplien la cobertura rural, generacional i femenina; la validació lingüística continua oberta perquè les anàlisis encara són provisionals. Pa-044, pa-047 i pa-050 conserven l'àudio i les transcripcions, però queden fora del graf fins a revisar-los auditivament i confirmar els segments atribuïbles. `fonts-pendents.tsv` conserva quatre permisos pendents i onze candidats separats en preanàlisi; Roser Suñé, Carine Montaner, Jaume Tomàs, Robert Guirao i Mireia Pedescoll són les incorporacions més recents, amb àudio local però torns encara per separar. La feina oberta passa a ser la revisió auditiva de les 656 files de `cua-audicio.tsv`, incloses les tres veus en quarantena i els candidats fora del cànon. Per tant, es pot considerar tancada la fase de captació, però no el corpus analitzat. Les tres veus en quarantena tenen ara una resegmentació auxiliar de 237 finestres de 20 segons (`proveniencia/qa-quarantena-20s.tsv`); això millora la localització del discurs, però no substitueix l’audició humana.

analisi-linguistica.tsv resumeix marcadors discursius, clítics, perífrasis, repetició i lèxic territorial a partir de l'ASR; són candidats textuals.

`proveniencia/resum-cobertura-fonts.tsv` resumeix els 66 registres per canal: 33 del Consell General, 17 de RTVA, 12 d'Andorra Recerca i Innovació i 4 de l'Arxiu d'Etnografia; també separa URLs de YouTube i llicències declarades.

Cada una de les 66 fitxes desplega també les 18 dimensions del repertori (vocalisme, morfologia, fonosintaxi, fonètica, lèxic, sintaxi, pragmàtica, prosòdia i variació) amb els buits d'evidència visibles; `proveniencia/actualitza-informes-repertori.py` ho regenera.

`proveniencia/quadern-sessions-canoniques.md` conserva una versió Markdown dels 89 clips de les sessions 01–02, 05 i 06, amb enllaç al WAV, tots dos ASR, prioritat, guia lingüística i camps d'anotació.

`proveniencia/auditoria-objectiu.tsv` manté una matriu machine-readable dels requisits: separa el que està assolit (cobertura, fonts, àudio, informes i grafs) del que continua pendent (audició humana i quarantena).

`proveniencia/auditoria-identitat-linguistica.tsv` separa la procedència andorrana de la confirmació lingüística: les 60 persones tenen una font contextual, amb la coincidència nominal de Carles Sasplugas marcada com a compatible però no verificada; per a totes continua pendent confirmar socialització, llengües d'ús i veu.
