# Pla de Maia Training Data

## Objectiu

Crear dos conjunts independents a partir de `docs/`:

- **Maia Knowledge** respon preguntes sobre Andorra amb informació de `docs/temes/`.
- **Maia Language** conserva trets del català andorrà contemporani a partir de parla humana elegible a `docs/parla/`.

No barregem coneixement enciclopèdic amb exemples de parla. La correcció, la naturalitat i els drets de reutilització passen per davant del volum.

## Què va fallar i què canvia

Les primeres preguntes seguien els títols i les seccions de les fitxes. Això produïa preguntes de lector («què explica aquesta secció?»), respostes sense context i seguiments que només repartien una resposta en diversos torns. A més, les converses i la procedència es guardaven en dos fitxers paral·lels; una desalineació podia atribuir una font equivocada a una conversa.

Ara cada registre de revisió conté **la conversa i la seva procedència al mateix objecte JSONL**. La sortida entrenable només n'exporta `messages`. Les mostres d'aquest començament tenen estat `approved_sample`: serveixen per acordar el criteri, però no entrenen el model ni compten com a cobertura.

## Com escriure preguntes que faria una persona

1. **Comença per una curiositat o una necessitat concreta.** Per exemple: entendre una paraula, aclarir dues versions que semblen incompatibles, situar una obra durant una visita o saber què es conserva avui.
2. **No facis que l'usuari parli com qui ha llegit la fitxa.** Evita «què explica la secció», «què indica aquesta fila» i «segons el document».
3. **Dona context només quan ajuda.** No inventis familiars, records, plans ni experiències personals. «Per què les pintures no són totes a l'església?» és prou natural sense inventar una visita.
4. **Contesta tota la pregunta en aquell torn.** No amaguis la dada principal per crear un seguiment. Cada resposta ha de tenir sentit si la conversa s'acaba allí.
5. **Afegeix un seguiment només si neix de la resposta.** Ha de demanar una cosa nova que probablement voldria saber la mateixa persona. No cal arribar a un nombre fix de torns.
6. **Mantén el fil i els referents clars.** «I què se n'ha quedat a l'església?» és vàlid després d'haver parlat de les pintures de Santa Coloma. Sense aquell antecedent, no ho és.
7. **Llegeix el diàleg en veu alta.** Si sona a qüestionari, a plantilla o a prova de comprensió lectora, reescriu-lo o descarta'l.

## Patró d'una conversa bona

Una conversa pot tenir una o més parelles usuari-assistent. La forma habitual és:

```text
usuari: pregunta concreta i autosuficient
assistent: resposta directa amb el context necessari
usuari: seguiment natural que demana informació nova
assistent: resposta al seguiment, sense repetir tota la conversa
```

No fabriquem multitorn. Una pregunta resolta en una resposta és millor que afegir torns artificials. Si hi ha seguiment, no pot dependre d'un «això» sense antecedent, repetir la resposta anterior ni canviar de tema sense motiu.

## Criteris de contingut

- La resposta surt del corpus i no afegeix fets plausibles però no documentats.
- Distingeix fets, llegendes, interpretacions, hipòtesis i buits d'informació.
- La primera frase respon la pregunta. El text és natural, complet i prou breu per al dubte plantejat.
- Una premissa equivocada es corregeix amb tacte i amb el fet correcte.
- Una resposta negativa diu què se sap i quin límit té la font; no converteix «no consta» en «no existeix».
- Agrupem dades quan una pregunta humana les necessitaria juntes. No fem una pregunta per cada unitat de l'inventari.
- Abans d'aprovar un registre, revisem que les fonts permetin la redistribució. La procedència queda vinculada al mateix registre.

## Estructura

```text
training-data/
├── README.md
├── PLAN.md
├── knowledge/
│   ├── review/
│   │   ├── records.jsonl       # conversa i procedència junts
│   │   ├── conversations.jsonl # export revisable, només messages aprovats
│   │   ├── EXEMPLES.md         # criteri editorial i exemples
│   │   └── unit-decisions.jsonl
│   ├── scripts/                # inventari i validació de Knowledge
│   ├── work/                   # inventari i estat regenerables
│   ├── reports/                # cobertura i qualitat
│   └── output/                 # només exportacions entrenables
└── language/                   # pipeline separat de parla humana
```

Un registre de `records.jsonl` inclou `record_id`, `review_status`, `messages`, fonts, afirmacions sostingudes, límits, grup de divisió i `unit_ids`. Cada línia és autocontinguda; no s'aparella amb una altra línia per posició. El validador genera `review/conversations.jsonl` amb els registres aprovats i només els seus `messages`; no hi inclou mostres. Els splits finals d'`output/` també contindran només `{"messages":[...]}`.

## Seqüència de treball

1. Revisar els exemples de calibratge i ajustar el criteri editorial.
2. Per a cada tema, comprovar primer les fonts i els drets.
3. Identificar quina pregunta humana resol el coneixement; si no n'hi ha cap de natural, registrar la decisió i no forçar un exemple.
4. Redactar una conversa completa. Crear seguiments només quan aportin una resposta nova i coherent.
5. Revisar-la sense mirar la fitxa; després verificar cada afirmació i la procedència.
6. Validar l'estructura i la coherència dels registres. Deduplicar per intenció i contingut, no només per text exacte.
7. Revisar cobertura sense convertir-la en una quota. Preparar exports i splits quan hi hagi un volum revisat suficient.
8. Treballar Maia Language després i amb regles pròpies d'origen, consentiment, contemporaneïtat i qualitat de transcripció.

## Definició d'acabament

**Knowledge**: el contingut entrenable del corpus queda cobert sense preguntes artificials; les respostes són correctes, naturals i fonamentades; les fonts permeten l'ús; no hi ha duplicació inútil; i els exports, splits i informes són vàlids.

**Language**: s'han revisat les peces candidates; només s'hi inclou parla humana elegible i prou fiable; es conserva la veu original; els splits eviten filtracions entre fragments relacionats; i hi ha un informe d'inclusions i exclusions.
