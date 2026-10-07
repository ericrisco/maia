# Pla: converses que comencen amb un dubte humà

## Què volem entrenar

`Maia Knowledge` ha d'ensenyar Maia a entendre què vol saber algú sobre Andorra,
respondre amb naturalitat i mantenir el fil quan la persona pregunta una cosa
més. Els fets han de sortir de `docs/temes/`.

`Maia Language` és un projecte separat: només pot ensenyar llengua humana
autèntica de `docs/parla/`, amb els permisos i criteris d'elegibilitat
documentats. No convertim monòlegs en entrevistes inventades.

No partim de «quin paràgraf falta convertir en pregunta?». Partim d'una
necessitat recognoscible: què intentaria aclarir algú, i quina resposta li
permetria continuar la conversa?

## Per què no serveixen els exemples anteriors

Preguntes com «Què explica la secció “El relat”?» pressuposen que l'usuari ha
vist la fitxa i n'ha memoritzat els encapçalaments. «Què indica aquesta fila?»
depèn d'una taula absent de la conversa. Respostes com «I dos topònims que en
surten:» o «Tres coses que el corpus registra per separat:» són fragments, no
respostes. Una dada separada per guions tampoc explica què significa ni per què
és pertinent.

Per tant, rebutgem preguntes que només es poden entendre consultant el document
font, i respostes que no contesten amb una frase completa. La font pot guiar la
redacció, però no ha d'aparèixer com a interfície de la conversa.

## El mètode: de la necessitat a la conversa

### 1. Trobar una situació que generi un dubte

Per cada tema, escriu una targeta de treball amb:

- **Situació:** què ha sentit, llegit o vol aclarir aquesta persona?
- **Pregunta inicial:** quina és la manera més directa i natural de demanar-ho?
- **Què ha d'entendre:** quina idea o distinció resol el dubte?
- **Límit:** què no permet afirmar el corpus?
- **Fonts:** quines fitxes sostenen cada afirmació?

La situació és una eina editorial i no s'exporta. No atribueixis a l'usuari una
experiència personal inventada («ahir hi vaig anar»), però tampoc converteixis
totes les preguntes en formulacions de llibre de text. Una persona pot parlar
amb naturalitat sense explicar la seva biografia: «Això també es fa a Ordino?»
o «Vols dir que les dues xifres compten coses diferents?»

### 2. Redactar la primera pregunta com una persona

Prioritza preguntes que neixen de motius corrents:

- una idea que la persona dona per feta pot ser falsa;
- dues dades semblen contradir-se;
- vol saber què passarà, com funciona o què ha de distingir;
- ha sentit un terme i en vol el sentit en context;
- vol entendre una causa, però les fonts potser només en documenten una part;
- la resposta anterior li suggereix una conseqüència concreta.

No cal afegir context fictici per fer-la «humana». La naturalitat ve de la
intenció, del vocabulari planer i de no fer explicar a l'usuari el que ja es
desprèn de la conversa. Evita preguntes de catàleg («Què explica la secció...»,
«Quins són els tres elements...»), preguntes massa solemnes i introduccions
que ningú no faria en una consulta normal.

### 3. Fer que cada seguiment neixi de la resposta

Escriu la resposta inicial abans del seguiment. Després pregunta't què podria
demanar algú en haver-la llegit. El seguiment pot aclarir un pronom («I la
d'Ordino?»), comprovar una conseqüència («Això vol dir que...?»), demanar una
comparació o preguntar pel límit d'una explicació.

Cada torn ha de tenir sentit en aquell punt de la conversa. No hi afegeixis
«I què més?» ni preguntes independents només per assolir un nombre de torns.
Dues interaccions ben resoltes són millors que sis d'artificials. La majoria de
registres tindran dos o tres intercanvis; fes-los més llargs només quan el fil
ho demani de debò. No obliguis cada registre a ser multitorn: una pregunta
resolta completament en un torn és millor que una conversa allargada a la força.

### 4. Contestar com un assistent, no com una fitxa

- Respon primer la pregunta concreta.
- Escriu frases completes i comprensibles sense veure cap document.
- Afegeix només el context que ajudi a entendre o a matisar la resposta.
- Corregeix una premissa equivocada amb tacte i explica la distinció correcta.
- Separa el que la font afirma del que només es podria inferir.
- Si no se sap, digues què no consta i evita omplir el buit amb una explicació plausible.
- No recitis l'article ni amunteguis dades només perquè són a la font.
- No comencis amb una rèplica ornamental («Bona pregunta!») ni repeteixis la
  pregunta abans de respondre-la.
- Fes servir noms i xifres quan ajudin a resoldre el dubte; explica què
  representen, en lloc de deixar-los com una llista deslligada.

### 5. Revisar amb fonts obertes

Per a cada conversa, la revisió ha de poder traçar les afirmacions factuals fins
a les fitxes de Maia i comprovar els drets de les fonts. La procedència queda en
fitxers de revisió; mai dins del JSONL de missatges. Si dues fonts discrepen,
explica la discrepància quan sigui rellevant, sense decidir arbitràriament qui
té raó.

## La prova de qualitat

Valora cada criteri de 0 a 2:

1. **Intenció:** és clar què vol resoldre l'usuari?
2. **Naturalitat:** ho podria dir algú que no ha vist la fitxa?
3. **Fil:** cada seguiment parteix de la resposta prèvia?
4. **Resposta:** l'assistent contesta directament amb frases completes?
5. **Fidelitat:** totes les afirmacions són sostingudes per les fonts?

Cal obtenir almenys 9/10 i cap zero. Són motius de rebuig immediat: pregunta
que cita seccions o files sense context, resposta fragmentària, seguiment sense
relació, fet inventat o atribució personal inventada. Si cal explicar la
pregunta amb «a la fitxa hi ha un apartat que...», torna-la a escriure.

Llegeix tota la conversa en veu alta i sense mirar les fonts. Si sona com un
qüestionari o l'assistent no sembla escoltar, no l'aprovis.

## Cobertura sense forçar preguntes

Primer s'audita què sap el corpus de cada tema. Després s'agrupen els fets que
una persona preguntaria junts i es decideix si donen peu a una conversa útil.
No cal una pregunta per dada, fila o paràgraf. Els fets importants que no
encaixin en una pregunta natural queden anotats a la cobertura, no es converteixen
en qüestionari. Abans d'afegir un registre, compara'l amb els aprovats per
detectar duplicats d'intenció i de resposta.

## Estructura i estats

```text
training-data/
├── README.md
├── PLAN.md
├── knowledge/
│   ├── review/
│   │   ├── EXEMPLES.md       # calibratge editorial, no dades d'entrenament
│   │   ├── conversations.jsonl
│   │   └── provenance.jsonl
│   ├── work/                 # inventari i cobertura per font/fet
│   ├── output/               # només converses aprovades, missatges sols
│   ├── reports/              # cobertura, qualitat, drets i splits
│   ├── scripts/
│   └── archive/               # lots antics, preservats però exclosos
└── language/                 # flux independent, segons autenticitat i permisos
```

Cada conversa de revisió té un identificador i un estat fora del contingut dels
missatges. Només els registres aprovats i amb drets comprovats s'exporten. Els
fitxers de `output/` contenen una línia JSONL per conversa i només `messages`;
cap ID, comentari, font ni puntuació editorial.

Els registres antics no s'han d'allargar ni donar per bons per inèrcia. Cal
revisar-los des de zero amb aquesta prova; un registre que la falli queda fora
de les sortides aprovades.

## Ordre de treball

1. Revisar els exemples de calibratge i acordar el patró de qualitat.
2. Escollir un tema i llegir les fitxes relacionades, no només una secció.
3. Escriure un lot petit de converses des de necessitats d'usuari.
4. Revisar fil, naturalitat, exactitud, procedència i drets; rebutjar o reescriure les que fallin.
5. Revisar duplicats i anotar cobertura que no s'hagi pogut convertir en conversa.
6. Aprovar, assignar split per grup de fonts relacionades i exportar.
7. Repetir el cicle tema a tema. No escalar fins que un lot petit passi la revisió.
8. Treballar Maia Language només amb converses humanes reals, elegibles i autoritzades.

La prioritat és correcció, naturalitat i cobertura traçable. El nombre de
registres no és una mètrica d'èxit per si sol.

## Porta d'entrada per a cada registre nou

Abans d'afegir-lo a `review/conversations.jsonl`, escriu-lo com un diàleg pla i
passa aquestes preguntes:

1. La primera pregunta expressa un dubte que algú podria tenir sense haver llegit
   les fonts?
2. La resposta resol aquest dubte en llenguatge corrent i amb prou context?
3. El seguiment surt d'una paraula, una dada o una idea de la resposta anterior?
4. Si traiem el seguiment, la conversa perd alguna cosa? Si no, potser sobra.
5. Les fonts sostenen cada afirmació i també els límits que s'hi expliquen?

Només després de passar aquesta lectura s'afegeixen metadades de revisió,
procedència, drets i split. Els exemples de `knowledge/review/EXEMPLES.md`
serveixen per calibrar la veu, no per copiar-ne les plantilles.
