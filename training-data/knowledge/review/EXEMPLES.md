# Mostres de calibratge: Maia Knowledge

Aquestes converses serveixen per decidir l'estil abans de crear més registres. No són exemples d'una plantilla que cal omplir, ni dades aprovades per entrenar.

## Com reconèixer una bona pregunta

- Podria fer-la algú que no ha obert cap article?
- Expressa un dubte concret amb paraules normals?
- Té context només quan ajuda a entendre la pregunta?
- El seguiment és una curiositat nova que neix de la resposta?

Evitem preguntes com «Què explica la secció X?», «Què indica aquesta fila?» o «Resumeix-me aquesta fitxa». També evitem fabricar una situació personal només per disfressar una pregunta d'examen.

## Mostra 1: aclarir dues coses que es confonen

```text
Usuari: Quina diferència hi ha entre la Passa i la Marratxa? Sempre les confonc.
Assistent: La Marratxa és una dansa; la Passa és una cercavila de parelles de fadrins. A la Passa, les parelles que es casaran aquell any van al davant i la resta se situa per edat.
Usuari: I totes dues es fan el dilluns de la festa major?
Assistent: Sí. La Passa es fa al migdia del dilluns, i la Marratxa també es balla aquell dilluns. La informació disponible no concreta l'hora de la Marratxa.
Usuari: Els «majors fadrins» són els que es casen aquell any, doncs?
Assistent: Exacte: així s'anomenen les parelles que es casaran durant l'any i que obren la Passa. No consta si també organitzen la festa.
```

## Mostra 2: no resoldre una discrepància a la força

```text
Usuari: La Marratxa commemora el Pareatge? Em ballen les dates: he trobat el 7 i el 8 de setembre.
Assistent: Segons la tradició de la dansa, la primera ballada va ser el 7 de setembre de 1278. La fitxa del Pareatge situa la signatura a Lleida el dia 8. Les dues dates no quadren i la discrepància continua oberta.
Usuari: Podria ser que la dansa es ballés la vigília?
Assistent: És una possibilitat, però les fonts disponibles no ho demostren. El que podem dir és que la Marratxa s'associa tradicionalment amb el Pareatge; no podem presentar la primera ballada com un fet verificat.
```

## Mostra 3: respondre amb el límit de la font

```text
Usuari: A la Passa, com decideixen qui forma parella amb qui?
Assistent: La informació disponible no ho explica. Sí que descriu l'ordre de la cercavila: les parelles que es casaran aquell any van al davant, i la resta va darrere de més grans a més joves.
Usuari: I si algú no té parella?
Assistent: Això tampoc no hi consta. No seria correcte deduir com ho resolen només a partir de l'ordre de la cercavila.
```

## Mostres que rebutgem

```text
Usuari: Què explica la secció «Quan es balla» de la fitxa «La Marratxa»?
Assistent: Es balla el dilluns.
```

La pregunta depèn d'una fitxa que l'usuari no ha dit que tingui. La resposta és telegràfica i ha perdut la dada útil: dilluns de la festa major de Sant Julià de Lòria.

```text
Usuari: La Passa és una dansa?
Assistent: No.
Usuari: I què més?
Assistent: És una cercavila.
```

El seguiment existeix només per dividir una resposta que hauria de ser completa des del principi.

## Revisió de cada conversa

1. Llegeix només els missatges, sense títol de font ni metadades.
2. Comprova que la pregunta inicial sembli espontània i s'entengui sola.
3. Comprova que cada resposta resolgui primer el dubte i que cap torn no es limiti a repetir.
4. Contrasta cada dada amb la font i conserva les incerteses.
5. Registra font, drets, afirmacions i estat de revisió a `provenance.jsonl`.
6. Si la conversa sembla un examen, una fitxa o una entrevista fabricada, reescriu-la o descarta-la.
