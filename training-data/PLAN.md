# Pla de Maia Training Data

## Propòsit

Preparar dos conjunts independents. **Knowledge** cobreix coneixement útil
documentat a `docs/temes/`. **Language** conserva llengua humana elegible de
`docs/parla/`. Una conversa de Knowledge no és una pregunta sobre una fitxa:
comença amb un dubte que podria tenir algú que no ha llegit el corpus.

## Com escriure una conversa de Knowledge

1. Llegeix el document font i les seves relacions. Separa els fets comprovats,
   les interpretacions, les discrepàncies i els buits.
2. Escriu una nota de treball: **«La persona vol aclarir…»**. Ha de descriure
   una necessitat humana, no l'acció de consultar un document.
3. Formula la pregunta inicial amb prou context perquè s'entengui per si sola.
   No parlis de fitxes, seccions, files, gràfics o IDs interns.
4. Contesta directament i amb context suficient. No comencis amb un fragment
   penjat ni afegeixis fets que la font no sosté.
5. Continua el diàleg només quan la resposta anterior faci sorgir una pregunta
   real. Cada seguiment ha d'aportar informació nova i mantenir el mateix fil.
6. Llegeix els missatges sense títols ni procedència. Si sonen a qüestionari o
   a una plantilla amb noms substituïts, reescriu o descarta l'exemple.
7. Registra fonts, afirmacions comprovades, motiu de la consulta i drets en un
   fitxer separat. Una mostra amb drets pendents no és exportable.

No hi ha una quota de torns per a cada registre. Les primeres cinc mostres són
multitorn expressament perquè es pugui revisar si el fil funciona. En producció,
un sol torn és preferible a un seguiment artificial.

## Porta editorial

Abans d'afegir una conversa a `knowledge/review/`, comprova que:

- la pregunta inicial s'entén sense consultar el corpus i té un motiu creïble;
- la primera frase de cada resposta resol la pregunta d'aquell torn;
- el seguiment neix del que s'acaba de dir i no és una dada independent;
- les respostes sonen com ajuda experta, no com notes enganxades;
- cada afirmació factual té suport identificable;
- les discrepàncies i els límits del corpus no s'amaguen;
- la procedència i les condicions d'ús estan anotades per separat.

Si falla un criteri, no es compta com a cobertura: es reescriu o es descarta.

## Estructura

```text
training-data/
├── README.md
├── PLAN.md
├── knowledge/
│   ├── examples/       # Cinc mostres internes de calibratge; no exportables
│   ├── review/         # Futurs candidats pendents de revisió
│   ├── work/           # Futurs registres de cobertura i evidència
│   ├── reports/        # Futurs reports de cobertura, qualitat i drets
│   └── output/         # Buit fins que hi hagi dades aprovades i splits
└── language/
    ├── examples/       # Exemples humans elegibles, només quan n'hi hagi
    ├── review/         # Revisió de fragments i condicions d'ús
    ├── work/           # Elegibilitat, transcripció i procedència
    ├── reports/        # Inclusió, exclusions i drets
    └── output/         # Buit fins que hi hagi dades aprovades i splits
```

Cada línia de `conversations.jsonl` és un objecte `{"messages": [...]}`. El
fitxer de procedència associat té una línia per conversa, en el mateix ordre.
La procedència no entra a l'export entrenable.

## Etapes

1. Revisar aquestes cinc mostres i ajustar el criteri editorial.
2. Un cop fixat el criteri, tornar a inspeccionar els documents de Knowledge i
   escriure candidats per temes, amb procedència i drets.
3. Auditar Language peça a peça; incloure només parla humana elegible i fiable.
4. Mesurar cobertura per unitat de coneixement, deduplicar i revisar drets.
5. Crear els splits només després d'aprovar els registres i les fonts.
6. Validar els exports i publicar informes de cobertura, exclusions i qualitat.

No s'afegeix volum per arribar a una quota. Els fets volàtils s'han de recuperar
actualitzats, no memoritzar com si fossin permanents.
