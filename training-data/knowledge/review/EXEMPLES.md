# Guia d'exemples per a Maia Knowledge

Aquestes mostres calibren el to i l'estructura. No són registres finals d'entrenament. Les mostres vigents també apareixen a `conversations.jsonl` i duen `approved_sample` a la procedència.

## Converses que funcionen

### Planificar una festa

```text
Usuari: Ens agradaria veure una festa de l'ossa aquest hivern. A Ordino i a Encamp la fan per les mateixes dates?
Assistent: No, són en moments diferents. L'Última Ossa d'Ordino se celebra la primera setmana de desembre, durant la fira de Nadal. El ball d'Encamp es fa el dilluns de Carnaval.
Usuari: Ah, doncs si només podem anar-hi per Carnaval, ens toca Encamp?
Assistent: Sí. Si hi aneu per Carnaval, la festa que encaixa és la d'Encamp. La d'Ordino és al desembre.
```

La pregunta conté una decisió real. El seguiment la resol amb la diferència de calendari.

### Aclarir dues versions d'una llegenda

```text
Usuari: A casa sempre m'havien dit que els minairons sortien d'una herba. Després he llegit que els tenien dins d'un canó. Com quadren les dues versions?
Assistent: Les dues imatges formen part de les llegendes. Alguns relats fan néixer els minairons de l'herba menaironera; després, l'amo els guarda en un canó. La tradició no acaba de resoldre si neixen de la llavor o si el minairó mateix n'és la llavor.
Usuari: I quin perill hi ha, si algú destapa el canó?
Assistent: En poden sortir milers de cop i demanar feina. Segons la llegenda, si l'amo no els en mana, el maten.
```

La primera pregunta compara dues idees que la persona ja ha sentit. La resposta conserva la incertesa de la font.

### Distingir una broma antiga d'una activitat actual

```text
Usuari: Els itineraris per trobar el Tamarro són una continuació de la cacera que feien abans?
Assistent: Comparteixen el personatge, però el plantejament és diferent. La cacera tradicional era una broma pesada: feien anar algú a buscar una bèstia imaginària. Avui el Tamarro també és una mascota i el protagonista d'itineraris familiars per la natura.
Usuari: O sigui que no és un animal que es pugui veure de veritat?
Assistent: Exacte. El Tamarro és una criatura del folklore, no un animal real. Els itineraris són una activitat turística, no una cerca d'una espècie que visqui als boscos.
```

El seguiment surt d'una ambigüitat concreta: si la criatura és real o forma part del joc.

## Patrons que no funcionen

```text
Usuari: Què explica la secció «El relat» de la fitxa «La troballa de Meritxell»?
Assistent: Se la va endur a Canillo i la va posar sobre l'altar major.
```

Això demana extreure una secció i la resposta comença a mitja història. Cal reformular-ho des del dubte d'una persona i donar el context necessari.

```text
Usuari: Què indica aquesta fila?
Assistent: 2014 — verd, 57,7 — morat, 56,4.
```

Sense context, no se sap quin gràfic es mira ni què vol dir la resposta. Si la dada és útil, cal explicar-la en una pregunta real amb els valors i les categories identificats.

```text
Usuari: Els minairons surten d'una herba?
Assistent: Sí.
Usuari: I de quina herba?
Assistent: De l'herba menaironera.
```

El segon torn no amplia gaire la resposta. És millor contestar l'origen amb el context rellevant en un sol torn, tret que la persona pregunti després per un aspecte nou.

## Checklist abans d'aprovar

- La pregunta inicial podria aparèixer en una conversa normal?
- S'entén sense veure la fitxa, el títol d'una secció ni un gràfic ocult?
- La resposta contesta directament i dona context suficient?
- Cada torn següent neix de la resposta anterior i demana una cosa nova?
- S'ha respectat la diferència entre fet, tradició oral, interpretació i incertesa?
- Les afirmacions tenen suport en les fonts declarades i els drets permeten redistribuir-les?
- Si elimino un seguiment, la conversa empitjora? Si no, l'elimino.

Qualsevol resposta «no» obliga a corregir o rebutjar el registre. No s'accepta una pregunta només per cobrir una unitat del corpus.
