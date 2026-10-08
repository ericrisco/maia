# Pla de Maia Training Data

## Objectiu

Preparar dos conjunts separats a partir de `docs/`:

- **Maia Knowledge**: converses útils sobre Andorra, basades en `docs/temes/`.
- **Maia Language**: mostres de llengua humana andorrana contemporània, basades en `docs/parla/` i en els criteris d'elegibilitat del corpus.

La sortida eventual és JSONL de converses. Procedència, afirmacions, drets i cobertura es mantenen en fitxers interns separats. Una conversa de revisió no és una dada d'entrenament: només s'exporta quan passa les comprovacions de contingut, naturalitat i drets.

## Estructura de treball

```text
training-data/
├── PLAN.md
├── README.md
├── scripts/
├── knowledge/
│   ├── examples/       # exemples de calibratge, mai no s'exporten
│   ├── review/         # candidats pendents de decisió
│   ├── archive/        # candidats antics i decisions substituïdes
│   ├── work/           # inventari, afirmacions, procedència i cobertura
│   ├── reports/        # qualitat, drets i cobertura
│   └── output/         # només converses aprovades
└── language/           # inventari, revisió i sortida de llengua, separats
```

No s'esborren els inventaris ni els candidats antics quan es canvia el criteri: s'arxiven perquè les decisions continuïn auditables. `output/` resta buit fins que hi hagi registres aprovats i drets compatibles amb l'ús previst.

## El mètode per crear una conversa

### 1. Trobar una necessitat humana

Llegeix el contingut de la font i pregunta't quin dubte pràctic, curiositat o confusió podria tenir algú. Escriu aquest dubte en una frase abans de redactar el xat.

Bones famílies d'intencions, quan el contingut les sosté:

- aclarir una confusió: «La Passa és un ball o una cercavila?»
- entendre com funciona una pràctica: «Com s'organitzen les parelles de la Passa?»
- situar una dada amb context: «Quan i on es pot veure el ball del Cerdà?»
- comprovar una afirmació: «És cert que la sardana ja es ballava a Andorra abans que hi arribés una cobla?»
- entendre una diferència: «Què canvia entre la dada de 2019 i la de 2024?»
- saber què es pot concloure: «Aquestes xifres expliquen per què va canviar l'assistència?»

No copiïs un títol, subtítol, fila, etiqueta ni identificador de la font per fabricar la pregunta. No cal preguntar per cada fet: si no hi ha una necessitat recognoscible, conserva el fet a l'inventari i no el converteixis en conversa.

### 2. Escriure com parlaria una persona

La pregunta ha de tenir prou context per entendre's per si sola, però no ha d'inventar una visita, una experiència personal o una conversa prèvia. Evita «Què diu aquesta secció?», «Explica'm aquesta fila» i «Què és X?» quan només siguin plantilles repetides.

Si una pregunta és massa abstracta, concreta el dubte real. Per exemple, en lloc de «Què explica el relat de la troballa?», pregunta «Per què, segons la llegenda, la imatge de Meritxell es va quedar al lloc de la gavernera?».

### 3. Respondre el dubte, no resumir la font

Comença per la resposta directa. Afegeix només el context que ajudi a entendre-la. Fes servir frases completes i distingeix entre fet, llegenda, interpretació, estimació i dada d'enquesta. Si les fonts no permeten afirmar una cosa, digues-ho clarament i breument.

No arrenquis amb una capçalera o un tros de llista. No repeteixis la pregunta en altres paraules. No afegeixis detalls només per fer la resposta més llarga.

### 4. Decidir si és multitorn

Un torn és suficient quan resol el dubte. Afegeix un seguiment només si la resposta anterior fa probable una pregunta immediata sobre el mateix assumpte: aclarir un terme que acaba d'aparèixer, preguntar per una conseqüència directa o comprovar el límit d'una conclusió.

El seguiment ha de dependre del torn anterior i la resposta ha de contestar-lo. No afegeixis «i què més?», una pregunta de control, ni una dada no relacionada per arribar a dos torns. Si el dubte nou és independent, fes un registre separat.

### 5. Revisar el xat sense la font al davant

Un altre lector ha de poder llegir només la conversa i respondre «sí» a tot això:

1. Entenc quin dubte té la persona i per què és raonable?
2. La pregunta sonaria normal dita en veu alta?
3. La primera resposta resol exactament el que s'ha preguntat?
4. Si hi ha seguiment, surt de manera natural de la resposta anterior?
5. Cada detall és verificable i el grau de certesa és correcte?
6. La conversa evita parlar de fitxes, seccions, files, corpus o identificadors interns?

Qualsevol «no» vol dir reescriure o descartar el candidat. La cobertura no justifica conservar una pregunta artificial.

## Cobertura sense preguntes forçades

L'inventari ha de registrar què conté cada document i quines unitats s'han revisat. La cobertura del dataset compta només converses aprovades, però no obliga a convertir cada unitat en una pregunta. Els fets sense una demanda humana clara queden documentats com a «sense conversa adequada», amb el motiu. Això permet distingir una omissió del procés d'una decisió editorial deliberada.

Les converses entre documents només s'escriuen quan una persona podria tenir un dubte que realment requereixi relacionar-los. No es combinen dades només perquè comparteixen tema o parròquia.

## Drets i procedència

Abans d'incloure cap registre a `output/`, comprova la procedència i els drets de totes les fonts que sustenten la resposta. La font i la seva llicència s'han de documentar segons el protocol del repositori abans d'entrar al conjunt d'entrenament. Una dada correcta no és automàticament reutilitzable. Els candidats amb permisos pendents romanen a `review/` o a l'arxiu; no s'exporten.

## Maia Language

Maia Language té un flux independent. Només s'utilitza material humà que compleixi els criteris del corpus per a veu originària, època contemporània, aptitud lingüística, qualitat de transcripció i drets. No s'inventen respostes per imitar un parlant. Els fragments es mantenen tan literals com sigui possible i s'agrupen per peça/parlant abans de dividir train, validation i test.

## Flux de cada lot

1. Revisar una font i les seves condicions d'ús.
2. Registrar les unitats de coneixement i la seva procedència.
3. Proposar només converses amb una necessitat humana clara.
4. Revisar exactitud, naturalitat, continuïtat i drets.
5. Validar els formats i revisar el diff.
6. Arxivar els candidats descartats o substituïts; actualitzar cobertura només amb evidència revisada.
7. Aprovar i exportar únicament registres que superin totes les portes de qualitat i drets.

Treballar en lots petits. Cada lot funcional es revisa, valida, commet i puja abans de començar el següent, segons l'objectiu del projecte.
