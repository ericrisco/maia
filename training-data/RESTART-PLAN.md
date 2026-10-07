# Reinici editorial de Maia Training Data

## Decisió

El corpus existent queda congelat com a material de referència. No s'hi afegeixen
registres nous ni se'n generen noves exportacions fins a validar el mètode nou.
Els exemples de `knowledge/starter/` són un pilot per revisar amb una persona;
no són encara una promesa de cobertura ni un dataset final.

## Objectiu del pilot

Ensenyar a Maia a respondre com una assistent útil sobre Andorra. La persona
pregunta per un dubte que tindria en una conversa real. Maia explica el fet
amb naturalitat, conserva el context històric i admet quan les fonts no ho
resolen.

El multitorn ha de sonar com una conversa que continua perquè la primera
resposta ha obert un dubte relacionat. No s'allarguen diàlegs per extreure més
fets d'una fitxa.

## Estructura nova de treball

```text
training-data/
├── RESTART-PLAN.md
├── knowledge/
│   ├── starter/
│   │   ├── README.md
│   │   ├── conversations.jsonl  # petit pilot, sense metadata interna
│   │   └── provenance.jsonl    # fonts, drets i revisió per exemple
│   ├── review/                  # corpus anterior, congelat durant el pilot
│   ├── work/                   # inventari i cobertura; no és text d'entrenament
│   └── output/                 # exportació antiga: no usar fins a nova revisió
└── language/
    ├── starter/                 # separat; només s'omplirà amb parla autèntica
    └── work/                    # elegibilitat i traçabilitat de les fonts
```

Knowledge i Language continuen separats. Cap exemple de `knowledge` serveix
per ensenyar la manera de parlar andorrana. A Language no es redacten diàlegs
inventats: s'hi treballarà quan hi hagi fragments autèntics verificats i drets
compatibles.

## Procés per cada conversa

1. Escollir una idea que el corpus pugui explicar i llegir la fitxa sencera, no
   només el fragment que l'ha fet aparèixer.
2. Escriure una pregunta inicial que algú faria sense tenir la fitxa al davant.
3. Redactar una resposta directa i clara. No convertir-la en una llista de tot
   el que conté la font.
4. Afegir un seguiment només si és una rèplica versemblant a la resposta.
   Normalment n'hi ha prou amb dos o tres intercanvis.
5. Contrastar cada afirmació amb el corpus i les fonts originals. Marcar què és
   una interpretació, una llegenda o una incertesa.
6. Fer una lectura en veu alta sense veure el títol de la fitxa. Si sembla un
   examen, un resum escolar o una consulta a una base de dades, reescriure-la.
7. Registrar procedència i drets abans de considerar-la per a cap exportació.
8. Revisar duplicats i comprovar que la conversa ensenya una resposta útil,
   no una formulació nova del mateix exemple.

## Regles de conversa

- La primera pregunta ha de contenir el context mínim perquè s'entengui sola.
- No preguntar «què diu la secció», «què indica la fila» o «resumeix la fitxa».
- No fer seguiments telegràfics com «i això?» sense un antecedent clar.
- No cal forçar una pregunta final ni una llargada mínima.
- La resposta comença per resoldre el dubte; després afegeix només el context
  necessari.
- No inventar experiències, intencions ni detalls per fer el diàleg més viu.
- Quan la font no ho sap, dir què falta i limitar l'afirmació a la font.
- Variar les intencions reals: entendre una regla, aclarir una contradicció,
  situar una tradició, comprovar una idea o demanar-ne la conseqüència.
- No generar preguntes per cada paràgraf o fila. La cobertura es mesura a part.

## Seqüència de treball

1. Revisar aquests exemples i acordar el criteri editorial.
2. Ajustar la guia amb els comentaris.
3. Crear registres nous per lots petits, amb procedència al costat.
4. Revisar els registres i exportar només els aprovats.
5. Auditar cobertura, duplicats, splits i drets abans de preparar l'entrenament.
6. Abordar Maia Language en un flux separat, només amb material humà elegible.

No s'amplia el volum fins que el pilot soni natural i sigui fidel a les fonts.
