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
s'entengui sense veure el corpus.

### Abans i després

**No:** «Què explica la secció “Les dues que queden” de la fitxa de l'ossa?»

**Sí:** «L'ossa encara es representa en algun lloc d'Andorra?»

**No:** «Què indica aquesta fila del gràfic?»

**Sí, si el dubte és real:** «Aquest gràfic diu que el català baixa, però el text
de la pàgina afirma que puja. Quina de les dues coses mostren les dades?»

No facis servir la segona mena de formulació si la persona no tindria accés al
gràfic o si la contradicció no és rellevant per entendre el tema.

## Com construir cada conversa

1. Llegeix les fonts primàries disponibles i identifica el fet que respon el
   dubte, els matisos i allò que no se sap.
2. Escriu una pregunta com l'escriuria algú en una conversa: natural, directa i
   sense vocabulari editorial del corpus.
3. Respon primer la pregunta. Afegeix només el context necessari per entendre
   la resposta; no enumeris tot el que saps del tema.
4. Continua el fil només quan la resposta faci sorgir una pregunta probable. El
   seguiment ha de dependre d'una cosa concreta que s'acaba de dir.
5. Llegeix el diàleg en veu alta, sense mirar les fonts. Si sembla un examen,
   una entrevista artificial o dues preguntes independents, reescriu-lo o
   deixa'l en un sol intercanvi.
6. Contrasta cada afirmació amb les fonts i registra la procedència i les
   condicions de reutilització fora del text de conversa.

La mida habitual és de dos intercanvis, però un intercanvi és millor que un
seguiment forçat. No hi ha quota de registres per fitxa.

## Respostes

- Comença amb una resposta clara, no amb una etiqueta o un fragment de l'article.
- Escriu en català natural i entenedor. Evita imitar el to de notes de recerca.
- Distingeix fets, tradicions, hipòtesis i versions discrepants.
- No completis buits amb coneixement extern o deduccions no justificades.
- Si la pregunta parteix d'una premissa falsa, corregeix-la amb tacte i respon el
  dubte que probablement hi ha al darrere.
- No deixis frases tallades ni respostes que només s'entenguin amb el títol de la
  font.

## Cobertura sense preguntes de farciment

L'inventari ha de cobrir tots els documents i assenyalar quins coneixements
importants s'han revisat. Això no vol dir que cada dada hagi de tenir la seva
pròpia pregunta. Agrupa fets quan una persona els demanaria junts; deixa fora
detalls sense un ús conversacional clar i registra el motiu a l'auditoria.

Per a cada conversa, revisa: naturalitat, context suficient, resposta directa,
dependència entre torns, exactitud, matisos, redundància i drets. Els exemples
de `knowledge/review/EXEMPLES.md` són calibratge editorial, no registres que
s'hagin d'imitar literalment.

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

1. Mantenir els inventaris complets i separar Knowledge de Language.
2. Crear candidats petits i revisables, amb procedència al costat.
3. Aplicar el criteri humà d'aquest pla; descartar o reescriure els que sonin a
   qüestionari documental.
4. Aprovar exactitud, naturalitat i drets abans d'exportar.
5. Assignar splits per font o grup de coneixement per evitar filtracions entre
   train, validation i test.
6. Validar el format i publicar informes de cobertura, qualitat i exclusions.

El JSONL final és una línia per conversa:

```json
{"messages":[{"role":"user","content":"..."},{"role":"assistant","content":"..."}]}
```

Cada registre exportat ha de contenir preguntes i respostes completes. Cap
metadata interna, cites de revisió o identificador editorial no s'afegeix a
`messages`.

## Criteri d'acceptació

Una persona que no ha vist el corpus entén per què es pregunta i què respon
Maia. La resposta és exacta i natural. El seguiment és espontani i reprèn el fil.
Cada frase factual té una font compatible. Si algun d'aquests punts falla, el
registre continua en revisió o es descarta.
