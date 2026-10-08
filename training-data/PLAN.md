# Pla: converses que comencen en una necessitat humana

## Què va fallar

Les preguntes com «què explica aquesta secció?» o «què indica aquesta fila?» són ordres de lectura, no dubtes que una persona tindria sobre Andorra. També fallen les respostes penjades —per exemple, anunciar «tres coses» sense explicar-les— i els seguiments afegits només per complir una longitud.

## Objectiu

Crear converses breus i multitorn que ajudin una persona a entendre, decidir o aclarir alguna cosa. La pregunta surt d'una situació recognoscible; la resposta usa els documents de Maia i explica el que cal amb paraules pròpies. El diàleg pot tenir dos o més seguiments, però només mentre cada torn nou sigui una continuació versemblant.

## Mètode per a cada conversa

1. **Tria una intenció humana**, abans de redactar: entendre una regla, preparar una visita, comprovar una dada, distingir dues coses, saber què implica una pràctica o aclarir una contradicció.
2. **Consulta les fonts necessàries** a `docs/temes/`. Apunta les afirmacions que responen a aquella intenció i també els límits o desacords rellevants.
3. **Escriu la pregunta inicial sense mirar els títols de les fitxes.** Ha de ser comprensible per a algú que no coneix Maia ni la seva estructura.
4. **Contesta de seguida i amb context suficient.** No reservis la dada principal per al torn següent. Marca llegendes, interpretacions i incerteses com a tals.
5. **Afegeix un seguiment només si la resposta el provoca.** Ha de demanar una precisió o conseqüència nova sobre una idea que acaba d'aparèixer. Si no n'hi ha cap de natural, descarta el fil; no inventis una pregunta de farciment.
6. **Llegeix el diàleg sense veure'n la font.** Si sona com una consulta sobre un document o una prova escolar, torna al pas 1.
7. **Verifica cada afirmació i registra fonts, llicència i hash fora de `messages`.** Una dada sense suport no s'hi incorpora.

## Forma de les converses

- Cada línia de JSONL conté una conversa completa amb missatges alternats `user` i `assistant`.
- Cada conversa de Knowledge tindrà com a mínim dues parelles de torns, sempre que el seguiment sigui natural. No s'allarga artificialment per satisfer aquesta regla.
- La primera resposta resol la pregunta inicial; cada resposta posterior també resol el seu torn.
- Els missatges no inclouen títols de fitxa, seccions, files, gràfics, IDs, etiquetes de revisió ni comentaris sobre el corpus.
- No inventis experiències personals, emocions ni context biogràfic per fer que una pregunta sembli espontània.
- No facis servir una plantilla repetida canviant només el nom propi.
- Les fonts i notes editorials van en fitxers de procedència separats.

## Prova de naturalitat

Abans d'acceptar cada conversa, respon sí a totes aquestes preguntes:

1. Algú podria fer la pregunta inicial sense haver llegit la font?
2. S'entén què vol aclarir i de què parla?
3. La primera resposta és completa i útil si la conversa s'acaba aquí?
4. El seguiment sorgeix d'una curiositat que la resposta acaba de despertar?
5. Cada torn aporta informació nova sense desviar-se ni repetir-se?
6. La resposta diferencia fets, llegendes, versions i incerteses?
7. Totes les afirmacions es poden rastrejar fins a una font autoritzada?
8. El diàleg sona natural llegit en veu alta, sense haver vist cap títol o document?

Un «no» vol dir reescriure o descartar. La cobertura no justifica una pregunta artificial.

## Estructura

```text
training-data/
├── README.md
├── PLAN.md
├── knowledge/
│   ├── README.md
│   ├── examples/       # Exemples curts per calibrar l'estil
│   ├── review/         # Converses candidates, encara no exportables
│   ├── work/           # Cobertura i procedència
│   ├── reports/        # Qualitat, exclusions i cobertura
│   ├── scripts/        # Eines, quan calguin
│   └── output/         # Només registres aprovats
└── language/
    ├── README.md
    ├── review/
    ├── work/
    ├── reports/
    ├── scripts/
    └── output/
```

## Ordre de treball

1. Acordar el criteri amb pocs exemples contrastats.
2. Revisar els exemples només llegint `messages`.
3. Recuperar l'inventari de cobertura i procedència sense convertir-lo en preguntes per document.
4. Crear converses per necessitats humanes, agrupant fets relacionats quan ajudin a respondre aquella necessitat.
5. Revisar naturalitat, exactitud, duplicats, drets i cobertura abans d'exportar.
6. Fer Knowledge i Language per separat. A Language només entra parla humana contemporània elegible i transcripció prou fiable.

## Límits de l'exportació

`output/` no s'omple automàticament. No s'exporten candidats pendents de revisió, fonts sense drets aclarits ni material de parla dubtós. El format d'entrenament conté només `messages`; les dades de procedència queden en fitxers interns.
