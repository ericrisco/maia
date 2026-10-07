# Pla de Maia Training Data

## Objectiu

Preparar dos conjunts separats a partir de `docs/`:

- **Maia Knowledge** respon dubtes reals sobre Andorra amb fets documentats a `docs/temes/`.
- **Maia Language** conserva català andorrà contemporani de parlants reals a partir de `docs/parla/`.

El primer pilot de Knowledge ha demostrat que una conversa pot ser multitorn i continuar sonant com un qüestionari. Per això, la qualitat de la conversa es revisa abans d'ampliar registres o comptar cobertura.

## Estructura

```text
training-data/
├── PLAN.md
├── README.md
├── knowledge/
│   ├── review/       # guia, exemples de calibratge, candidats, procedència i arxiu
│   ├── work/         # inventari i estat de revisió
│   ├── scripts/      # inventari, validació i exportació
│   ├── reports/      # cobertura, qualitat i exclusions
│   └── output/       # train, validation i test aprovats
└── language/
    ├── review/       # peces candidates i procedència
    ├── work/         # elegibilitat i fiabilitat de transcripció
    ├── scripts/
    ├── reports/
    └── output/       # train, validation i test aprovats
```

No cal esborrar `training-data/` per canviar el criteri editorial. L'inventari, la procedència i les decisions de drets es conserven encara que es retiri un pilot.

## Criteri de conversa

1. Llegeix la fitxa i les fonts abans d'escriure.
2. Troba el dubte que algú voldria resoldre: una confusió, una comparació, una dada que no quadra, una explicació o una història que vol recordar.
3. Escriu la pregunta com la formularia aquesta persona sense tenir la fitxa davant. No esmentis seccions, títols, files, colors interns ni «el corpus» si l'usuari no ho ha tret.
4. Respon el dubte directament. Dona prou context per entendre la resposta i marca els límits quan afectin la conclusió.
5. Afegeix un seguiment només si la resposta anterior provoca una pregunta plausible. Cada torn ha d'aportar una cosa nova.
6. Atura't quan el fil queda resolt. Una conversa pot tenir un sol intercanvi; no hi ha quota de torns.
7. Si no hi ha una pregunta humana que justifiqui el contingut, no la forcis. Registra el document com a revisat sense conversa natural.

No inventis una història personal per fer més vistosa la pregunta. Un context genèric i breu és acceptable quan concreta el dubte («No entenc per què...»); una biografia fictícia no.

## Calibratge i producció

### Fase 1 — Calibratge editorial

Llegir `knowledge/review/CONVERSATION-GUIDE.md` i `knowledge/review/EXEMPLES.md`. Els exemples mostren el to; no són registres ni compten per a cobertura.

### Fase 2 — Pilot revisable

Crear un pilot petit de temes diferents. Revisar cada conversa en veu alta, només llegint els missatges d'usuari. Descartar o reescriure qualsevol pregunta que sembli una ordre per extreure informació d'una fitxa.

### Fase 3 — Producció per dubte

Recórrer `docs/temes/` sense generar una pregunta per secció o per fet. Una fitxa pot produir zero, una o diverses converses. Registrar les fonts, els drets i les afirmacions que sosté cada conversa a `provenance.jsonl`.

### Fase 4 — Cobertura i revisió

Separar la revisió de la fitxa de la cobertura del dataset. Una dada llegida no compta com a entrenada fins que apareix en una resposta aprovada. Revisar naturalitat, continuïtat, precisió, límits, duplicats i drets.

### Fase 5 — Exportació

Només els registres aprovats i elegibles passen a `output/`. Agrupar converses relacionades abans de crear els splits per evitar variants gairebé iguals entre train, validation i test.

### Fase 6 — Maia Language

Treballar-lo separadament. Incloure només material elegible i fiable. Preservar la parla humana; no inventar respostes ni reformular-la com a català estàndard.

## Regles de resposta

- No exposis procedència, etiquetes editorials o metadades dins del diàleg.
- No presentis llegendes com a fets històrics.
- Si les fonts discrepen, explica la discrepància i què la resol o la deixa oberta.
- Si la dada és històrica, no la presentis com a norma actual.
- Evita respostes telegràfiques i llistes que l'usuari no necessita.
- No afegeixis dades per fer més llarga una resposta.

## Format dels fitxers

Una conversa per línia JSONL. Cada conversa conté només `messages` amb rols `user` i `assistant`. La procedència i l'estat de revisió es guarden en fitxers separats. Els exemples editorials i els pilots rebutjats no s'exporten.

## Prioritats

1. Correctesa i drets d'ús.
2. Pregunta que una persona faria de debò.
3. Resposta directa, natural i prou completa.
4. Seguiments que continuen el mateix fil.
5. Cobertura útil i varietat sense duplicats.
6. Volum.

No augmentarem el volum a costa de cap prioritat anterior.
