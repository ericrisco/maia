# Pla de Maia Training Data

## Objectiu

Preparar dos datasets independents a partir de `docs/`:

- **Maia Knowledge** ensenya a respondre preguntes útils sobre Andorra amb fets documentats a `docs/temes/`.
- **Maia Language** conserva fragments de català andorrà contemporani produïts per persones a `docs/parla/`.

Knowledge conté respostes redactades i no és una mostra de parla autèntica. Language no s'amplia amb respostes inventades. Els missatges visibles per al model no inclouen IDs, rutes ni camps interns de procedència.

## Estructura

```text
training-data/
├── PLAN.md
├── README.md
├── knowledge/
│   ├── examples/       # Mostres d'estil, mai exportables
│   ├── review/         # Converses noves pendents de revisió humana
│   ├── archive/        # Esborranys rebutjats, fora de la cobertura
│   ├── work/           # Inventari, evidències i cobertura auditables
│   ├── reports/        # Volum, errors i estat de cobertura
│   ├── scripts/        # Eines de generació i control
│   └── output/         # Train/validation/test només després d'aprovació
└── language/
    ├── review/         # Selecció i decisions editorials
    ├── work/           # Fragments i selecció de treball
    ├── reports/
    └── output/
```

## Flux de Knowledge

1. **Entendre una font abans de convertir-la en conversa.** Llegir la fitxa sencera i anotar afirmacions, matisos, contradiccions i buits. No convertir cada títol, fila o paràgraf en una pregunta.
2. **Triar un dubte que algú tindria.** Pensar en una situació normal: preparar una visita, aclarir un terme que ha sentit, entendre una norma antiga, resoldre una contradicció o completar una conversa anterior.
3. **Escriure la primera pregunta sense dependència del corpus.** Ha d'incloure el context mínim perquè s'entengui sense haver obert una fitxa. No dir «la secció», «aquesta fila», «el gràfic» ni copiar el títol de l'article.
4. **Respondre com una persona experta i útil.** Donar la resposta principal primer; explicar els noms locals; afegir només el context que ajudi a entendre-la. Distingir fets, afirmacions atribuïdes a una font i interpretacions.
5. **Continuar només si la conversa ho demana.** El seguiment ha de néixer de la resposta anterior i resoldre una curiositat plausible. No cal forçar un diàleg: un torn pot ser suficient; sovint en basten dos o tres. No hi ha quota de torns.
6. **Mantenir els límits del corpus.** Si falten dades o les fonts discrepen, dir-ho amb claredat. No inventar causes, detalls ni motivacions per fer la resposta més rodona.
7. **Anotar la procedència a part.** Cada registre de revisió porta evidències, fonts, drets i una empremta dels missatges. Aquests camps serveixen per revisar, no apareixen a la conversa d'entrenament.
8. **Revisar llegint només el diàleg.** Llegir en veu alta les preguntes i respostes sense metadades. Si sona com un examen o com un resum d'una fitxa, reescriure'l.

## Porta de qualitat per a cada conversa

Una conversa només passa a `review/` quan totes aquestes comprovacions són positives:

- La pregunta inicial sona com una cosa que algú preguntaria i s'entén tota sola.
- La pregunta neix d'una necessitat o curiositat recognoscible; no d'una unitat interna del corpus.
- La resposta contesta directament abans d'afegir context.
- Cada seguiment demana una cosa nova i surt del torn anterior; no és una pregunta posada per allargar el registre.
- Els torns tenen una llargada natural i no repeteixen la mateixa dada.
- Cada afirmació factual, xifra, data i matís té evidència identificable.
- Les incerteses, discrepàncies i buits es presenten sense resoldre'ls amb intuïcions.
- La procedència i els drets de totes les fonts estan registrats.

Si falla naturalitat, es reescriu o es rebutja. Si falla l'evidència, es corregeix o es retira. Una mostra editorial pot ensenyar l'estil encara que els drets de la font impedeixin entrenar-hi; per això les mostres i els candidats viuen en directoris separats.

## Cobertura

L'inventari recorre totes les fitxes de `docs/temes/`, incloses seccions, llistes, taules i links. La cobertura és sobre afirmacions útils, no sobre el nombre de converses. Una conversa pot cobrir més d'una afirmació relacionada, i una afirmació pot quedar coberta per una conversa existent. Les exclusions han d'indicar-ne el motiu. Els esborranys rebutjats no compten.

Treballar per tema en tandes petites: llegir, seleccionar els dubtes de valor, redactar, verificar, revisar en veu alta i registrar procedència. No generar variacions cosmètiques ni perseguir un volum prefixat.

## Maia Language

Incloure només material amb `veu == originaria`, `epoca == contemporania` i `apte_llengua == true`. Revisar transcripcions incertes i preservar lèxic, sintaxi i estil de la persona amb normalització mínima. No redactar respostes noves en la veu d'un parlant. Agrupar qualsevol split per peça o parlant per evitar filtracions.

## Exports i ordre de treball

Els directoris `output/` es mantenen buits fins que els registres hagin passat revisió humana, comprovació de drets, deduplicació i control de filtracions entre splits. Els fitxers finals contenen només missatges `user` i `assistant`; evidència, drets i notes continuen a la capa de revisió.

Seqüència del projecte: estructura i criteris editorials → exemples aprovats d'estil → revisió de cobertura per tema → registres de Knowledge → selecció de Language → validació global → splits i exports. Validar cada pas abans de començar el següent i no barrejar els dos datasets.
