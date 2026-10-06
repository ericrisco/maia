# Pla de Maia Training Data

## Què preparem

Dos conjunts separats a partir de `docs/`:

- **Maia Knowledge**: respostes útils i correctes a preguntes reals sobre Andorra.
- **Maia Language**: català andorrà contemporani extret de parla humana elegible.

La cobertura de Knowledge ha de ser exhaustiva, però això no vol dir convertir
cada paràgraf en una pregunta. Cada unitat útil queda coberta per una conversa
natural o exclosa amb un motiu. Language no es fabrica: només conserva torns
humans existents.

## Estàndard de conversa

Una conversa parteix d'un dubte, una decisió o una curiositat que podria tenir
algú sense haver obert la font. La pregunta no parla de fitxes, apartats, taules,
files, fragments ni del corpus. Tampoc inventa un personatge o una situació
només per fer entrar una dada.

Escriu primer la resposta que aquella persona necessitaria. Després decideix si
hi ha una pregunta de seguiment que realment sorgiria de la resposta. Cada torn
ha de fer avançar la conversa; repetir la resposta com a pregunta no compta.
Un intercanvi complet és millor que allargar-la artificialment.

Les preguntes poden ser breus i directes, o incloure context quan aquest context
és natural: «Em sonava que era per Carnaval; ara es fa al desembre?» El context
no és una plantilla. No comencis sempre amb «M'he embolicat», «És veritat» o
«Si jo...».

Les respostes:

1. resolen el dubte des de la primera frase;
2. donen el context mínim perquè s'entenguin soles;
3. distingeixen un fet documentat d'una interpretació;
4. diuen clarament quan la font no permet respondre una part;
5. no sonen com una fitxa, una llista de camps o un examen.

Llegeix el diàleg sencer en veu alta. Si sembla escrit per demostrar que s'ha
llegit un document, reescriu-lo. Si la pregunta només és una dada amb un signe
d'interrogació al davant, busca el dubte humà que la faria necessària; si no n'hi
ha cap, no creïs aquella conversa.

## Procés per a cada conversa

1. Llegeix la fitxa sencera i les fonts citades. Defineix en una frase què vol
   saber la persona.
2. Escriu l'intercanvi sencer sense mirar els noms de les seccions.
3. Comprova cada afirmació contra l'evidència. No omplis els buits amb intuïcions.
4. Retalla salutacions, repeticions i seguiments que no aportin informació nova.
5. Llegeix-ho en veu alta i revisa-ho amb `knowledge/review/EXEMPLES.md`.
6. Desa només `messages` al JSONL. Desa evidència, drets i estat de revisió a la
   traça paral·lela.
7. Valida el registre i la cobertura. Mantén-lo fora dels splits publicables
   fins que tingui revisió humana i drets compatibles amb l'ús previst.
8. Revisa el diff, fes un commit per conversa i empeny-lo a `main` abans de
   començar la següent.

## Estructura

```text
training-data/
├── README.md
├── PLAN.md
├── scripts/
├── knowledge/
│   ├── work/       # inventari, evidència, relacions i exclusions
│   ├── review/     # converses actives, traça, rúbrica i exemples
│   ├── output/     # splits publicables, només després de les revisions
│   └── reports/    # cobertura, qualitat, drets i exclusions
└── language/
    ├── work/       # elegibilitat i selecció de fragments
    ├── review/     # candidats literals i procedència
    ├── output/     # splits publicables
    └── reports/    # peces incloses, exclusions i cobertura
```

Els registres antics es conserven a `knowledge/review/quarantine/` per poder-los
revisar més endavant. No són exemples aprovats ni s'incorporen a les converses
actives. Els fitxers `output/` es mantenen buits fins que hi hagi registres
aprovats i aptes per publicar.

## Cobertura i qualitat

Per cada fitxa de `docs/temes/`, cal revisar fets, noms, dates, xifres, relacions,
cronologia, matisos i incerteses. La cobertura es mesura contra aquestes unitats,
no pel nombre de preguntes. Es poden combinar diverses unitats en una conversa
si una persona les connectaria de debò; no cal una conversa per fila o fragment.

Abans d'exportar Knowledge, cal deduplicar converses que ensenyin el mateix,
separar grups relacionats entre train, validation i test, validar els missatges,
la traça, els drets i la cobertura, i registrar exclusions i limitacions.

Per Language s'apliquen els criteris de `docs/CONTRACT.md`: només parla humana
elegible, transcripció prou fiable i drets resolts. No es generen preguntes o
respostes per fer que un monòleg sembli una conversa.

## Criteri per avançar

Primer revisarem aquestes mostres i acordarem l'estàndard. Després reprenem el
corpus tema a tema, conversa a conversa. Cada registre passa per la mateixa
revisió de naturalitat, fidelitat, cobertura i drets. El volum no és un criteri
d'acceptació.
