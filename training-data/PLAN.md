# Pla de Maia Training Data

## Propòsit

Preparar dos conjunts independents a partir de `docs/`:

- **Knowledge** ensenya a respondre preguntes sobre Andorra amb informació traçable de `docs/temes/`.
- **Language** conserva parla humana autèntica i elegible de `docs/parla/`.

No s'han de barrejar. La prioritat és que cada exemple sigui correcte, útil i natural. El volum ve després.

## Per què refem el procés editorial

Una conversa no és humana només perquè tingui diversos torns. Les preguntes del tipus «què explica aquesta secció?» o «què vol dir aquesta fila?» depenen del document obert. També hi ha respostes fragmentàries que no resolen cap dubte. Aquests patrons no serveixen per ensenyar un assistent a conversar.

Els registres antics es conserven fins que decidim com revisar-los. No s'han de tractar com a aprovats només perquè siguin a `conversations.jsonl`.

## Flux per crear una conversa Knowledge

1. **Tria una necessitat humana.** Escriu què vol aclarir la persona: una confusió, una decisió, una discrepància, una comparació o un límit del que se sap.
2. **Comprova que el corpus ho pot respondre.** Revisa les fonts, les llicències, els límits i les fitxes relacionades. Si els drets no permeten l'ús previst o no estan resolts, no passis el contingut a una dada d'entrenament.
3. **Escriu el fil de l'usuari.** La primera pregunta ha de tenir sentit sense cap document al davant. Cada seguiment ha de néixer d'una resposta anterior. No afegeixis torns per arribar a una quota.
4. **Redacta la resposta.** Contesta de seguida. Dona el context que eviti una conclusió falsa. Separa fets, tradició, hipòtesi i desconegut. No escriguis fragments com «i dos topònims que en surten».
5. **Fes la revisió editorial i factual.** Llegeix només els missatges d'usuari. Si sonen com una llista de preguntes d'examen, reescriu-la. Revisa cada afirmació de la resposta contra la font.
6. **Registra procedència i cobertura.** La traçabilitat queda fora del diàleg. No hi posis identificadors interns ni notes editorials.

## Regles de conversa

- La pregunta inicial expressa una intenció recognoscible i és autosuficient.
- Els seguiments poden reprendre el context amb pronoms i referències normals.
- Una seqüència habitual té dos o tres intercanvis, però també pot tenir-ne un o quatre si el dubte ho demana.
- Cada resposta resol la pregunta abans d'afegir matisos.
- El to és català clar i natural. No s'hi afegeixen falques col·loquials ni experiències inventades.
- La resposta pot dir que no se sap. No resol una discrepància a base d'endevinar.
- Les preguntes sobre títols, seccions, files o «què diu la fitxa» només s'accepten si la persona té una necessitat documental explícita.
- No es creen variants gairebé idèntiques per augmentar el recompte.

## Porta d'acceptació

Una conversa només passa a dades aprovades si compleix tots aquests punts:

| Criteri | Comprovació |
|---|---|
| Intenció | Es pot resumir en una frase com «vol aclarir…»? |
| Autonomia | S'entén la primera pregunta sense accés a Maia ni a una fitxa? |
| Continuïtat | Cada seguiment respon a una cosa que acaba de dir l'assistent? |
| Naturalitat | Llegits sols, els torns d'usuari sonen com un fil humà? |
| Resposta | El primer enunciat contesta el dubte? |
| Fidelitat | Cada fet i cada matís estan sostinguts per fonts elegibles? |
| Utilitat | L'exemple ensenya una resposta útil, no només una dada aïllada? |
| Drets | La reutilització prevista està permesa i registrada? |

Un sol «no» vol dir reescriure o excloure. No es compensa un criteri fallit amb una puntuació mitjana.

## Estructura

```text
training-data/
├── PLAN.md
├── README.md
├── knowledge/
│   ├── candidates/       # Esborranys encara no aprovats
│   ├── review/           # Guia, calibratge, dades revisades i procedència
│   ├── work/             # Inventari i cobertura per document
│   ├── reports/          # Qualitat, drets, exclusions i cobertura
│   ├── scripts/          # Inventari, validació, deduplicació i splits
│   └── output/           # Exports aprovats; no s'entrena des de review/
└── language/
    ├── review/           # Fragments humans verificats i procedència
    ├── work/             # Elegibilitat i fiabilitat de transcripció
    ├── reports/
    ├── scripts/
    └── output/
```

`knowledge/review/calibration.jsonl` és un joc petit d'exemples de referència. No compta com a dada activa ni com a cobertura. `knowledge/review/conversations.jsonl` conserva els registres de treball; un registre només es considera aprovat quan ha passat la porta editorial i de drets.

## Maia Knowledge

Inventariar totes les fitxes de `docs/temes/`, les unitats útils, les relacions, les incerteses i els drets. Cobrir els fets amb converses orientades a necessitats humanes. Els exemples comparatius o de síntesi poden connectar fitxes quan cada pas de la resposta està documentat.

Els drets pendents s'han de marcar com a pendents. No es pot presentar cap export com a redistribuïble mentre una font necessària no tingui condicions compatibles confirmades.

Abans de crear `train`, `validation` i `test`, deduplicar i separar per tema/font o grup relacionat. Un tema o una paràfrasi de la mateixa resposta no pot aparèixer a train i test.

## Maia Language

La font és `docs/parla/`. Requereix `veu: originaria`, `epoca: contemporania` i `apte_llengua: true`, a més de drets compatibles i transcripció verificada. Les respostes provenen de parla humana real, amb normalització mínima i registrada. No s'inventa parla ni s'omplen buits amb text generat.

Els segments d'una mateixa peça, conversa o parlant s'han de mantenir junts als splits per reduir la filtració entre train i test.

## Definició de fet

Knowledge només està acabat quan totes les fitxes elegibles s'han inspeccionat, les unitats útils estan cobertes, els drets són traçables, els exemples han passat la revisió editorial, factual i de duplicats, i els tres exports són vàlids.

Language només està acabat quan totes les peces s'han inspeccionat, les transcripcions i els drets estan verificats, la parla humana es conserva, els splits eviten filtracions i els exports són vàlids.
