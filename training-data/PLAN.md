# Pla de treball: converses que sonin humanes

## Problema que corregim

Les preguntes com «Què explica la secció X de la fitxa Y?» pressuposen que l'usuari veu un document i vol un resum. No són una bona mostra d'una conversa amb un assistent que coneix Andorra. Les respostes fragmentàries tampoc resolen el dubte.

## Objectiu editorial

Crear converses breus i multitorn que parteixin de dubtes reals. La persona pot preguntar per una dada, una confusió, una conseqüència o un detall que li ha cridat l'atenció. No ha de conèixer el títol de la fitxa ni el vocabulari intern de Maia.

Cada torn de seguiment ha de néixer del que s'acaba de dir. No afegim torns per complir una llargada fixa. Una conversa curta i resolta és millor que una de llarga amb farciment.

### Regles per redactar

1. Llegir els missatges seguits, sense veure títols ni metadades. Si sona a qüestionari, reescriure.
2. La primera pregunta ha de tenir sentit per si sola i expressar un dubte que una persona podria tenir.
3. Respondre primer el que s'ha preguntat; després afegir només el context necessari.
4. Fer que cada seguiment demani una cosa nova i tingui un referent clar.
5. Corregir una premissa equivocada amb tacte. Separar fets, interpretacions i llegendes.
6. Quan la font no permet concloure una cosa, dir-ho i concretar què falta.
7. No inventar una experiència personal de l'usuari ni fer veure que una dada és més actual del que és.
8. No començar amb fragments, etiquetes, «segons el corpus» ni frases que depenen d'una fitxa absent.
9. Variar la forma segons el tema. No omplir una quota de preguntes factuals, comparatives o de síntesi.

## Estructura d'un registre

Una línia de JSONL per conversa, amb missatges alterns `user` i `assistant`. L'export no conté identificadors interns ni metadades del pipeline. Les fonts, els drets, les afirmacions verificades i l'estat de revisió s'anoten en fitxers separats.

Les mostres de `knowledge/review/examples.jsonl` només calibren l'estil: no són dades aprovades i no s'exporten automàticament.

## Fases

1. **Calibratge:** revisar aquestes mostres en veu alta i ajustar el criteri editorial.
2. **Evidència:** per cada candidata, identificar afirmacions i unitats font; comprovar la font original, els drets i l'atribució abans d'incorporar-la.
3. **Redacció:** escriure una conversa completa, amb seguiments motivats per la resposta anterior.
4. **Revisió:** verificar exactitud, naturalitat, traçabilitat, drets, incerteses i duplicats. Reescriure o descartar si falla algun punt.
5. **Cobertura:** afegir converses per coneixement documentat i relacions entre fitxes; no perseguir una quota de volum.
6. **Exportació:** només quan hi hagi prou registres revisats, deduplicar i separar train/validation/test per evitar que reformulacions del mateix coneixement quedin repartides.
7. **Maia Language:** treballar-ho en paral·lel només quan la parla sigui autèntica, prou fiable i autoritzada. No inventar converses ni barrejar aquest objectiu amb Knowledge.

## Criteri per acceptar una conversa

- La pregunta sona natural i s'entén fora de la font.
- La resposta contesta el dubte amb informació sostinguda per les fonts.
- Cada seguiment és coherent, necessari i aporta una resposta nova.
- Els límits de la informació queden clars.
- La traçabilitat i els drets estan documentats.
- Una persona editora la pot llegir com una conversa, no com una fitxa convertida en preguntes.
