# Pla per crear converses naturals de Maia

## Objectiu

Preparar dades perquè Maia sàpiga parlar de manera útil sobre Andorra. Cada
conversa ha de començar amb una curiositat real i ha de continuar només quan
la resposta obre una pregunta que una persona probablement faria.

Knowledge i Language tenen objectius diferents i no es barregen:

- **Knowledge** ensenya què diu el corpus sobre Andorra.
- **Language** conserva català andorrà contemporani extret de parla humana.

## Criteri principal: primer la intenció humana

Abans d'escriure cap pregunta, resumiu en una frase el dubte de la persona.
Exemples: «no entén com es reparteixen els escons», «vol saber si una llegenda
és pròpia d'Andorra» o «veu una contradicció entre dues dades».

Escriviu la pregunta com si parléssiu amb algú que en sap. La persona no coneix
el títol de la fitxa, els seus apartats, les seves taules ni les paraules del
pipeline. Per tant, no pregunteu què explica una secció ni què indica una fila.

La pregunta pot ser col·loquial, però no cal inventar una biografia o una
escena personal. Feu servir expressions normals com «no ho acabo d'entendre»,
«però llavors…?» o «això vol dir que…?» quan encaixin amb el dubte.

### Senyals de mala pregunta

Rebutgeu o reescriviu qualsevol registre que:

- pregunti «què explica aquesta secció?» o «què indica aquesta fila?»;
- depengui d'un títol de fitxa, d'un epígraf o d'una taula que la persona no ha
  vist;
- sigui una ordre d'extracció disfressada de conversa;
- es pugui contestar amb un fragment que no resolgui la pregunta;
- comenci una llista o una explicació i la deixi penjada;
- afegeixi torns només per arribar a una llargada fixada.

No feu que cada registre sembli una pregunta d'examen. La curiositat pot néixer
d'una sorpresa, una contradicció, una conseqüència pràctica, una comparació o
un límit del que se sap.

## Com escriure una conversa multitorn

1. **Obriu amb el dubte principal.** La primera resposta ha de resoldre'l sense
   obligar la persona a preguntar el que faltava.
2. **Feu que el seguiment neixi de la resposta.** Pot demanar una conseqüència,
   comprovar una inferència, aclarir una paraula o comparar amb una altra cosa.
3. **Manteniu el fil.** Cada torn ha d'entendre's amb el context de la conversa,
   sense canviar de tema de cop ni repetir una pregunta ja resolta.
4. **Acabeu quan el dubte s'ha resolt.** No forceu un nombre fix de torns.
   Una resposta pot tancar la conversa; una altra pot obrir dos o tres
   seguiments útils.
5. **Varieu la forma perquè varia la curiositat.** No genereu paraphrases de la
   mateixa pregunta per aparentar diversitat.

Una conversa final és una llista de missatges alternats `user` i `assistant`.
Les respostes són completes, clares i proporcionades al que s'ha preguntat.
No acaben en encapçalaments, introduccions penjades ni promeses de donar una
llista que després no arriba.

## Què pot preguntar una persona

No són plantilles obligatòries. Serveixen per trobar intencions diferents:

- **Aclarir:** «No ho acabo d'entendre: per què calen vots dels dos grups?»
- **Comprovar una deducció:** «Així, amb setze vots ja n'hi ha prou?»
- **Seguir una conseqüència:** «I si el Consell es dissol, qui en manté les funcions?»
- **Contrastar dues coses:** «La bandera ja era oficial quan la descriuen el 1904?»
- **Distingir relat i fet:** «Els minairons són una tradició només d'aquí?»
- **Relacionar temes:** «Això té a veure amb la reforma que va ampliar el vot?»
- **Reconèixer un límit:** «Se sap per què es van triar aquests colors?»

La pregunta no ha de contenir la resposta. Tampoc no ha de ser tan vaga que
Maia no pugui saber què vol aclarir la persona.

## Com respondre

- Contesteu primer la pregunta concreta.
- Doneu només el context necessari perquè la resposta s'entengui.
- Separeu fets documentats, relats tradicionals, interpretacions i dades
  pendents de verificar.
- Si la pregunta parteix d'una premissa falsa, corregiu-la amb naturalitat i
  expliqueu breument què se sap.
- Si el corpus no resol el dubte, digueu-ho. No ompliu el buit amb una
  explicació plausible.
- No convertiu una resposta en una fitxa, una llista de camps o un resum de tot
  el document.

## Flux de producció

1. **Calibrar l'estil.** Llegir `knowledge/examples/EXEMPLES.md`. Són mostres
   editorials, no dades d'entrenament ni unitats de cobertura.
2. **Triar una curiositat.** Llegir la fitxa i anotar el dubte humà que pot
   aclarir. La nota no apareix als missatges.
3. **Comprovar la font.** Revisar la fitxa, la font original, els drets i els
   límits que el corpus registra.
4. **Redactar el fil sencer.** Escriure la pregunta inicial, la resposta i els
   seguiments que realment se'n desprenen.
5. **Revisar cada afirmació.** La procedència queda en un fitxer separat i
   permet localitzar les fonts i comprovar els fets.
6. **Fer lectura cega.** Llegir només els missatges, en veu alta. Si sona com
   una pregunta d'examen o com una fitxa recitada, reescriure-la o descartar-la.
7. **Afegir registres petits.** Crear tandes curtes i revisar tots els torns
   abans de començar la tanda següent.
8. **Revalidar l'existent.** Cap conversa queda aprovada només perquè ja sigui
   al fitxer de revisió. Llegir-la amb aquests criteris, reescriure-la,
   arxivar-la o excloure-la. Mantenir-ne la procedència alineada.
9. **Exportar al final.** No generar `train`, `validation` ni `test` fins que
   els registres, les fonts, la cobertura i la separació dels conjunts s'hagin
   revisat.

## Criteris per acceptar un registre

- La persona podria fer la pregunta sense haver llegit el corpus.
- La pregunta expressa una necessitat concreta i no apunta a una secció o fila.
- La primera resposta resol el dubte inicial.
- Cada seguiment surt del que s'acaba de dir i afegeix una curiositat real.
- El nombre i la llargada dels torns no segueixen una plantilla rígida.
- Les respostes sonen com una conversa informada, no com una base de dades.
- Les afirmacions es poden verificar i els límits de la font queden clars.
- No hi ha preguntes repetides amb paraules diferents ni informació inventada.
- Llegit sense cap document al davant, el fil sona com una conversa que podria
  passar entre una persona curiosa i algú que en sap.
- Cada resposta resol la pregunta del seu torn. No és un títol, un inici de
  frase ni un fragment que només té sentit dins la fitxa.

## Estructura

```text
training-data/
├── README.md
├── PLAN.md
├── knowledge/
│   ├── README.md
│   ├── examples/
│   │   ├── README.md
│   │   └── EXEMPLES.md       # calibratge editorial, no s'entrena
│   ├── review/
│   │   ├── README.md
│   │   ├── conversations.jsonl
│   │   └── provenance.jsonl
│   ├── work/                 # inventaris i candidats regenerables
│   ├── reports/              # cobertura i qualitat
│   └── output/               # exportacions després de la revisió
└── language/
    ├── README.md
    ├── review/                # fragments humans i procedència
    ├── work/                  # selecció regenerable
    ├── reports/
    └── output/                # text literal, separat de Knowledge
```

Les converses Knowledge revisades s'emmagatzemen a `knowledge/review/`. La
procedència sempre queda separada dels missatges. Les mostres de
`knowledge/examples/EXEMPLES.md` no compten com a registres ni com a cobertura.
Els registres que ja existien s'han de revalidar un per un; no s'infereix que
siguin bons pel fet d'estar al fitxer.

## Language

Language continua separat. Només utilitza parla humana elegible del corpus.
Conserva les paraules i construccions de les persones i no inventa respostes
per imitar el català andorrà. La seva política d'inclusió, incertesa i
procedència es documenta a `language/README.md`.
