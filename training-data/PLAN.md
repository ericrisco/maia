# Pla de Maia Training Data

## Objectiu

Preparar dos conjunts separats a partir de `docs/`:

- **Maia Knowledge** respon preguntes reals sobre Andorra amb coneixement de `docs/temes/`.
- **Maia Language** conserva llengua humana autèntica de `docs/parla/`; no es creen respostes artificials per imitar-la.

La sortida d'entrenament és una conversa JSONL amb missatges `user` i `assistant`. Les fonts, drets, afirmacions i notes de revisió queden en fitxers interns separats.

## Estructura

```text
training-data/
├── PLAN.md
├── README.md
├── scripts/                 # validació i generació, quan existeixin
├── knowledge/
│   ├── examples/            # calibratge; mai no s'exporta
│   ├── review/              # candidats pendents de revisió humana
│   ├── archive/             # esborranys descartats o substituïts
│   ├── work/                # inventari i cobertura interns
│   ├── reports/             # resultats de qualitat i cobertura
│   └── output/              # només registres aprovats
└── language/                # inventari i selecció lingüística separats
```

No es mou cap registre a `output/` només perquè el seu fet sigui correcte. També ha de passar el filtre de naturalitat, procedència i drets.

## Com trobar una conversa

Parteix d'una necessitat recognoscible: entendre una tradició, aclarir una confusió, situar una dada, saber què implica una norma o comprovar si una afirmació és segura. La pregunta no ha de dependre d'haver llegit una fitxa.

Abans d'escriure-la, resumeix per a tu mateix el dubte en una frase. Si només pots formular-lo copiant el títol, una secció, una fila o un identificador de la font, encara no has trobat una pregunta humana.

Escriu la pregunta amb el vocabulari que faria servir una persona. Dona el context imprescindible perquè s'entengui sola. No inventis una biografia, una visita, una conversa prèvia ni una motivació personal per fer-la semblar real.

### Senyals per descartar una pregunta

- Demana què diu una secció, una taula, una fila, una fitxa o el corpus.
- És un «què és X?» mecànic que es podria aplicar a qualsevol entrada.
- Pregunta una dada aïllada sense cap motiu ni context suficient.
- Presuposa una premissa falsa que ningú no tindria motiu per creure.
- S'ha escrit només perquè una afirmació del registre de cobertura encara no té pregunta.
- Té una resposta que sona bé però no es pot derivar de les fonts.

No cal convertir cada fet en una pregunta. Una dada sense una demanda humana clara pot quedar documentada a `work/` sense entrar al dataset.

## Escriure la resposta

Contesta de seguida la pregunta concreta. Escriu com ho explicaries a algú, no com ompliries una cel·la.

- Fes servir frases completes i identifica persones, llocs, períodes i unitats.
- Inclou només el context necessari per entendre la resposta.
- Presenta una llegenda com a llegenda, una interpretació com a interpretació i una dada com a dada.
- No converteixis correlació en causa.
- Si les fonts discrepen o no permeten concloure, explica el límit de manera breu i concreta.
- No comencis amb un fragment, una capçalera, una llista nua o «el corpus diu».
- No afegeixis fets per fer la resposta més rodona.

Una bona resposta pot ser curta. La mida segueix la pregunta, no la llargada de la font.

## Quan fer-la multitorn

Una conversa pot tenir un torn o diversos. No hi ha una quota de seguiments.

Escriu un seguiment només si algú, després de llegir l'última resposta, tindria una pregunta probable que continua el mateix dubte. El seguiment pot aclarir un terme que acaba d'aparèixer, preguntar per una conseqüència directa o comprovar si una conclusió és vàlida.

No afegeixis «i què més?», una pregunta de control ni un canvi de tema per allargar-la. Si la resposta ja resol la necessitat, acaba la conversa. Si la nova pregunta obre un altre fil, crea un registre separat.

## Revisió de naturalitat

Llegeix només la conversa, sense mirar la font, i comprova:

1. Entenc què vol saber la persona i per què ho pregunta?
2. La pregunta sonaria normal dita en veu alta?
3. La resposta resol el dubte completament i amb el context just?
4. El seguiment surt de la resposta anterior i conserva el fil?
5. He tret qualsevol referència a l'estructura interna de Maia?
6. Cada fet i cada matís es poden comprovar a les fonts?
7. Els drets permeten l'ús previst?

Si la conversa falla en naturalitat, reescriu-la o descarta-la. No la conservis només per cobrir una afirmació.

## Flux de treball

1. Calibrar el to amb `knowledge/examples/`. Aquests registres no s'entrenen.
2. Crear candidats en lots petits a `knowledge/review/`; registrar les fonts i els drets al fitxer de procedència paral·lel.
3. Revisar naturalitat, exactitud, cobertura i drets abans d'aprovar cap candidat.
4. Actualitzar l'inventari de cobertura només amb converses aprovades; les afirmacions sense pregunta humana clara poden quedar fora.
5. Deduplicar i separar train, validation i test agrupant converses sobre el mateix contingut.
6. Auditar `language/` amb el filtre d'autenticitat, època, transcripció i drets. No omplir-lo amb imitacions generades.

Cada lot és un step separat: validar JSONL i diffs, revisar els fitxers preparats, fer commit i push abans de començar el lot següent.
