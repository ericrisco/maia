# Pla: converses que una persona preguntaria de debò

## Objectiu

Crear exemples de Maia Knowledge que ensenyin a respondre dubtes reals sobre Andorra. Cada conversa ha de començar amb una necessitat recognoscible, donar una resposta útil i continuar només si la resposta convida una pregunta nova. El contingut factual ha de sortir de `docs/temes/`; les preguntes poden sonar naturals, però no poden afegir fets.

Maia Language és una feina separada. Només pot ensenyar llengua a partir de material humà elegible de `docs/parla/`.

## Abans d'escriure

Per cada possible conversa, anota internament una frase: **què vol aclarir la persona?** Exemples: distingir dues tradicions, entendre una dada que sorprèn, planificar una visita, reconciliar dues versions o saber què no es pot afirmar.

Després verifica que el corpus contingui una resposta suficient. Si només hi ha un fragment a mig fer, una inferència de l'autor o un buit, respon amb aquest límit o descarta el tema. No converteixis qualsevol dada en una pregunta.

## Escriure com parla un usuari, no com s'indexa una fitxa

- Comença pel dubte de la persona, no pel títol, secció, fila, gràfic o ID del document.
- Escriu una pregunta concreta i autònoma. Evita «què explica…», «què indica aquesta fila?» i pronoms sense referent.
- Dona el context mínim perquè s'entengui. No inventis un viatge, una emoció, una experiència personal ni una premissa que no calgui per preguntar.
- Fes servir paraules normals. No afegeixis argot, errades, falques o oralitat fingida per fer veure que és una conversa real.
- A les respostes no parlis de «la fitxa», «el corpus», IDs o estats editorials. Per expressar límits, digues què indiquen les fonts disponibles o què no hi consta. Anomena una font pública només quan ajudi a entendre d'on surt una versió o per què hi ha una discrepància.
- Alterna intencions quan el contingut ho permet: aclarir una confusió, comparar, preguntar per una data o lloc, entendre una conseqüència, demanar una explicació pràctica o comprovar un límit del que se sap.
- No facis servir una plantilla repetida per a cada document. Si la pregunta es pot emplenar canviant només el nom d'una tradició, revisa-la.

## Conversa multitorn

Cada registre de calibratge i de producció ha de tenir almenys **dues parelles** `user` → `assistant`. La segona pregunta ha de néixer de la resposta anterior: demanar una precisió, aclarir una conseqüència o explorar una comparació ja oberta.

No canviïs de tema només per arribar a dos torns. Si no hi ha cap seguiment natural, busca una necessitat inicial que permeti un fil real o no creïs el registre. No allarguis una conversa més enllà del punt en què el dubte queda resolt.

Cada resposta ha de ser útil encara que el diàleg s'acabi després d'aquella resposta. Contesta primer; després afegeix només el context necessari. Evita llistes de camps, fragments penjats i respostes que només serveixen per preparar el torn següent.

## Fidelitat al corpus

- Separa un fet documentat d'una llegenda, una interpretació o una afirmació d'una font secundària.
- No converteixis «la font diu» en una certesa més àmplia que la font.
- Davant de versions incompatibles, exposa qui diu què i deixa clar si el corpus no ho resol.
- Davant d'un buit, digues què se sap i què no consta. No inventis una causa ni presentis el silenci del corpus com a prova que una cosa no existeix.
- No copiïs paràgrafs llargs. Resumeix amb paraules pròpies i conserva els matisos importants.
- Mantén les fonts, hashes, drets i notes d'avaluació fora de `messages`, a la procedència interna.

## Revisió humana abans d'acceptar

Llegeix només els missatges, sense títol ni font. Accepta el registre únicament si passa totes aquestes preguntes:

1. **La pregunta inicial sona possible?** Algú que no ha vist la fitxa la podria fer tal com està escrita?
2. **S'entén de què parla?** No necessita un referent ocult ni informació editorial.
3. **La resposta ajuda de seguida?** Contesta la pregunta abans d'afegir context.
4. **El seguiment és natural?** És fàcil entendre per què la resposta anterior ha provocat aquella pregunta?
5. **Cada resposta tanca el seu torn?** No és un teaser, una frase tallada ni una resposta deliberadament incompleta.
6. **Tot és fidel?** Cada fet és rastrejable i les incerteses queden visibles.
7. **Sona escrit per ajudar?** És clar i directe, sense imitar una persona concreta ni farcir amb expressions col·loquials.
8. **Aporta varietat útil?** No duplica una conversa existent amb sinònims superficials.

Una sola resposta «no» implica reescriure o descartar. Una pregunta plausible no salva una resposta incorrecta; una resposta correcta no salva una pregunta artificial.

## Estructura i flux de treball

```text
training-data/
├── README.md
├── PLAN.md
├── knowledge/
│   ├── README.md
│   ├── examples/       # Calibratge revisat; no exportable automàticament
│   ├── review/         # Candidats pendents de revisió
│   ├── work/           # Cobertura, procedència i anotacions internes
│   ├── scripts/        # Eines de validació i generació, quan n'hi hagi
│   ├── reports/        # Cobertura, qualitat, duplicats i exclusions
│   └── output/         # Només converses aprovades i amb drets revisats
└── language/
    ├── README.md
    ├── review/
    ├── work/
    ├── scripts/
    ├── reports/
    └── output/
```

Treballar en aquest ordre:

1. Revisar i aprovar els exemples de calibratge.
2. Mantenir l'inventari complet de `docs/temes/` i `docs/parla/` separat.
3. Crear converses de Knowledge per necessitat humana, no una pregunta per secció.
4. Registrar cobertura i procedència fora de les converses.
5. Revisar naturalitat, fidelitat, drets i duplicats abans d'exportar.
6. Afegir exemples de Language només quan la veu, l'època i la fiabilitat de la transcripció els facin elegibles.
7. Fer splits agrupant per tema o peça, per reduir filtracions entre train, validation i test.

Una línia de JSONL representa una conversa completa. Els fitxers de `output/` només contenen `messages`; cap candidat no hi arriba automàticament.
