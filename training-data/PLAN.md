# Pla per crear converses de Maia

## Objectiu

Preparar dos datasets separats a partir del corpus de `docs/`:

- **Maia Knowledge**: respostes correctes sobre Andorra, basades en `docs/temes/`.
- **Maia Language**: català andorrà contemporani extret de parla humana elegible a
  `docs/parla/`.

La font aporta els fets o la parla. No dicta l'escena, la pregunta ni el to de la
conversa. No cal convertir cada paràgraf en un registre.

## Criteri principal: ha de semblar una conversa que algú iniciaria

Abans d'escriure, resumeix el dubte en una frase: què vol entendre la persona i
per què li seria útil saber-ho? Si només es pot descriure com «pregunta sobre la
secció X», no és una bona candidata.

Les preguntes poden néixer d'una curiositat, una confusió habitual, una decisió
pràctica o una comparació que algú faria de debò. No inventis que l'usuari ha
viscut una experiència concreta. Dona a la pregunta prou context perquè
s'entengui sense veure el corpus. No facis que l'usuari parli com un editor, un
arxiver o algú que està llegint els encapçalaments interns de la fitxa, llevat
que la pregunta sigui explícitament sobre aquella font.

### Senyals que una pregunta no funciona

- Demana «què explica la secció...» o «què indica aquesta fila...» sense
  explicar quin dubte intenta resoldre la persona.
- Només es pot entendre si es coneix el títol d'una fitxa, un subtítol o una
  etiqueta del corpus.
- És una instrucció d'extracció («enumera», «resumeix la secció») que cap
  persona faria en una conversa normal.
- El seguiment diu «i què més?» o canvia de tema sense reprendre la resposta.
- El diàleg repeteix el mateix motlle o afegeix un segon intercanvi només per
  semblar multitorn.
- La resposta comença amb un fragment sense subjecte («I dos topònims...»)
  o queda incompleta si se separa del títol de la font.

### Abans i després

**No:** «Què explica la secció “Les dues que queden” de la fitxa de l'ossa?»

**Sí:** «L'ossa encara es representa en algun lloc d'Andorra?»

**No:** «Què indica aquesta fila del gràfic?»

**Sí, si el dubte és real:** «Aquest gràfic diu que el català baixa, però el text
de la pàgina afirma que puja. Quina de les dues coses mostren les dades?»

No facis servir la segona mena de formulació si la persona no tindria accés al
gràfic o si la contradicció no és rellevant per entendre el tema.

## Com construir cada conversa

1. Llegeix les fonts i descompon el document en afirmacions verificables. Anota
   què se sap, què és incert i quines afirmacions depenen d'una data o font.
2. Escriu fora del diàleg quin dubte humà resoldrà la conversa i quins fets
   cobrirà.
3. Formula la pregunta amb paraules corrents. Afegeix context només quan faci
   falta per entendre el dubte.
4. Respon directament i amb frases completes. Afegeix el context necessari,
   no tot el contingut de la fitxa.
5. Afegeix seguiments quan el fil els justifiqui. Fes servir converses d'un
   intercanvi i de diversos; no hi ha una llargada obligatòria.
6. Llegeix-ho en veu alta sense mirar la font. Si sembla un examen, una
   entrevista artificial o una fitxa disfressada de diàleg, reescriu-ho.
7. Contrasta cada afirmació amb les fonts i registra la procedència i les
   condicions de reutilització fora del text de conversa.

## Respostes

- Comença amb una resposta clara, no amb una etiqueta o un fragment de l'article.
- Escriu en català natural i entenedor. Evita imitar el to de notes de recerca.
- Distingeix fets, tradicions, hipòtesis i versions discrepants.
- No completis buits amb coneixement extern o deduccions no justificades.
- Si la pregunta parteix d'una premissa falsa, corregeix-la amb tacte i respon el
  dubte que probablement hi ha al darrere.
- No deixis frases tallades ni respostes que només s'entenguin amb el títol de la
  font.

## Cobertura exhaustiva sense preguntes artificials

El coneixement del corpus no s'ha de retallar per fer el dataset més fàcil.
Cal inventariar tots els documents i els seus fets rellevants, i vincular cada
fet a una conversa aprovada o deixar-ne una exclusió justificada a l'auditoria.
Es poden agrupar fets relacionats en una conversa quan una persona els
demanaria junts. Si cap pregunta sobre un detall no sona humana, conserva'l a
l'inventari i explica per què no s'ha convertit en conversa.

La cobertura es mesura sobre fets revisats, no comptant només fitxes amb almenys
un exemple. Una fitxa amb molts fets i una pregunta genèrica no és cobertura
completa.

Per a cada conversa, revisa: naturalitat, context suficient, resposta directa,
dependència entre torns, cobertura dels fets previstos, exactitud, matisos,
redundància i drets. Els exemples de `knowledge/review/EXEMPLES.md` mostren
formes possibles, no una plantilla que calgui repetir.

## Knowledge i Language no es barregen

Knowledge pot redactar respostes naturals, però tots els fets han de sortir de
les fonts de Maia i cada registre ha de tenir procedència i revisió de drets.
Les sortides d'entrenament contenen només `messages`; la procedència i les notes
editorials queden a `review/`.

Language només incorpora material humà autèntic amb drets compatibles i
transcripció prou fiable. No inventis preguntes d'entrevistador ni converteixis
un monòleg en una conversa fictícia. Mantén fragments consecutius de la mateixa
peça o parlant al mateix split.

## Passos

1. Inventariar tots els documents i els fets de Knowledge, i revisar elegibilitat
   i drets de les peces de Language.
2. Crear converses candidates de tema en tema, amb procedència i mapa de
   cobertura al costat.
3. Revisar cada pregunta amb el criteri humà d'aquest pla; reescriure les que
   sonin a qüestionari documental.
4. Aprovar exactitud, naturalitat, cobertura i drets abans d'exportar.
5. Assignar splits per font o grup de coneixement per evitar filtracions entre
   train, validation i test.
6. Validar el format i publicar informes de cobertura per fet, qualitat,
   exclusions i drets pendents.

El JSONL final és una línia per conversa:

```json
{"messages":[{"role":"user","content":"..."},{"role":"assistant","content":"..."}]}
```

Cada registre exportat ha de contenir preguntes i respostes completes. Cap
metadata interna, cites de revisió o identificador editorial no s'afegeix a
`messages`.

## Criteri d'acceptació

Una persona que no ha vist el corpus entén per què es pregunta i què respon
Maia. La resposta és exacta i natural. Si hi ha seguiment, reprèn el fil. Tots
els fets rellevants consten en una conversa o en una exclusió justificada. Cada
afirmació factual té una font compatible. Si falla algun d'aquests punts, el
registre continua en revisió o es descarta.
