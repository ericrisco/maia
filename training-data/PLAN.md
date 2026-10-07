# Pla de Maia Training Data

## Propòsit

Preparar converses útils per a un assistent, a partir del corpus `docs/`, sense
convertir cada secció en una pregunta ni afegir-hi informació de fora.

Hi ha dos fluxos separats:

- **Knowledge** respon preguntes sobre Andorra amb informació de `docs/temes/`.
- **Language** conserva llengua contemporània produïda per persones a
  `docs/parla/`. No s'hi redacten respostes artificials per imitar una veu local.

## Fase actual: calibratge

Abans de reprendre la producció, revisar els exemples de
`knowledge/review/EXEMPLES.md` i confirmar que el to, la naturalitat i la
progressió dels torns són els desitjats. Els exemples són mostres de calibratge,
no una declaració de cobertura del corpus.

## Com crear converses de Knowledge

1. **Comença per una necessitat humana.** Tria què vol entendre, aclarir,
   comparar o comprovar la persona. No parteixis d'un títol, una secció o una
   fila que s'hagi de cobrir.
2. **Escriu la pregunta com es faria parlant.** Ha de tenir sentit encara que la
   persona no conegui el corpus ni la fitxa. No inventis una biografia per
   justificar la pregunta.
3. **Respon de seguida al dubte.** Dona el context necessari, explica les
   distincions que importen i conserva els límits de l'evidència. Evita recitar
   dades sense explicar per què responen la pregunta.
4. **Afegeix seguiments només quan neixin del diàleg.** Cada nova pregunta ha de
   sorgir d'una cosa concreta que acaba de dir l'assistent i ha d'aportar un pas
   útil. No hi ha una llargada obligatòria: una bona conversa pot tenir un sol
   intercanvi.
5. **Separa conversa i auditoria.** Els missatges contenen només la conversa.
   Fonts, llicències, afirmacions sostingudes, límits i cobertura van a
   `knowledge/review/provenance.jsonl`.

### Preguntes que cal evitar

- «Què explica la secció X de la fitxa Y?»
- «Què indica aquesta fila?» o «I dos topònims que en surten?»
- fragments que pressuposen que l'usuari ha vist una taula o un document;
- preguntes successives que només existeixen per omplir més torns;
- preguntes que demanen una dada aïllada quan una persona normal preguntaria
  pel seu significat, context o límit.

### Revisió de cada conversa

- La pregunta inicial sona plausible fora d'un examen i no delata l'estructura de
  la font.
- La resposta resol la pregunta abans d'afegir context.
- Cada seguiment té una causa visible en el torn anterior; si es pot eliminar
  sense perdre res, s'elimina.
- El diàleg no força una mateixa plantilla ni repeteix el mateix tipus de
  seguiment en registres consecutius.
- Cada afirmació factual està sostinguda per la font indicada. Llegendes,
  interpretacions, ficció, hipòtesis i fets documentats queden distingits.
- La llicència permet l'ús previst i la procedència dona l'atribució requerida.
- No s'exposa al missatge cap ID intern, estat de revisió ni nota del pipeline.

## Registre i creixement

Els exemples aprovats es guarden com una conversa JSONL per línia a
`knowledge/review/conversations.jsonl`, amb només `messages` i rols alterns
`user` / `assistant`. La procedència es guarda en una línia corresponent de
`provenance.jsonl`.

La cobertura es controla per separat: una conversa pot resoldre una necessitat
amb diverses unitats de coneixement, i una unitat no obliga a fabricar una
pregunta. Les unitats no cobertes han de quedar identificades i, si s'exclouen,
cal justificar-ho.

Abans de crear registres a escala:

1. aprovar el calibratge;
2. regenerar l'inventari de `docs/temes/` i establir l'estat de cobertura;
3. treballar tema a tema, agrupant fets quan serveixin la mateixa necessitat;
4. auditar drets i procedència abans d'incorporar contingut;
5. deduplicar, revisar naturalitat i factualitat, i només llavors crear splits i
   exports no buits.

Cada registre nou passa revisió i validació abans d'incorporar-se. El flux de Git
acordat és un commit i un push per conversa.

## Flux de Language

Inspecciona totes les peces de `docs/parla/`. Inclou només material elegible,
amb drets, consentiment i fiabilitat de transcripció revisats. Conserva la veu
humana; no generis preguntes i respostes fictícies per fer-la semblar
andorrana. Separa els splits per peça o parlant per evitar filtracions entre
train, validation i test.

## Exports

No creïs fitxers de split buits ni declaris el dataset preparat fins que la
cobertura, els drets, la deduplicació i la partició s'hagin revisat. Els
missatges finals no inclouran metadades internes.
