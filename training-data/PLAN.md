# Pla editorial de Maia Training Data

## Objectiu d'aquesta fase

Crear converses que sonin com preguntes reals sobre Andorra. No convertim fitxes en qüestionaris ni generem una pregunta per cada dada. Primer decidim quin dubte podria tenir una persona; després comprovem si el corpus permet respondre'l.

El treball de dades es divideix en dos conjunts que no es barregen:

- **Knowledge**: respostes sobre Andorra basades en `docs/temes/` i les seves fonts.
- **Language**: parla humana autèntica, seleccionada de `docs/parla/` segons `docs/CONTRACT.md`.

Knowledge i Language s'elaboren en tandes separades. Les mostres de Knowledge fixen el criteri editorial; després es continua fitxa a fitxa sense reduir l'objectiu de cobertura completa.

## Per què el lot anterior no servia

Preguntes com «Què explica la secció…?» o «Què indica aquesta fila?» només tenen sentit per a algú que està mirant una fitxa. No són dubtes espontanis. Sovint provoquen respostes tallades —«apel·lació al Consell General»— o fragments de plantilla —«I dos topònims que en surten»— en lloc d'una resposta conversacional.

Canviar el nom de la secció per una paràfrasi no ho arregla. Cal canviar el punt de partida: la necessitat de la persona, no l'estructura del document.

## Cicle per crear una conversa

1. **Troba un dubte humà.** Escriu en una frase per què algú ho preguntaria: vol entendre una discrepància, prendre una decisió, corregir una idea, situar un fet o saber què implica una norma.
2. **Descarta la pregunta de fitxa.** Si necessita frases com «aquesta secció», «aquesta fila», «segons el document» o «què diu la fitxa», torna al pas 1.
3. **Llegeix la font sencera.** Comprova la resposta i el context necessari. No converteixis cada frase, xifra o cel·la en un registre propi.
4. **Respon directament.** La primera frase ha de resoldre el dubte. Després afegeix el matís que evitaria una conclusió equivocada.
5. **Afegeix seguiment només si neix de la conversa.** Ha de preguntar una cosa nova que la primera resposta faci venir al cap. No forcis el multitorn.
6. **Mantén la veu humana.** La persona no sap quina fitxa s'ha consultat. L'assistent tampoc narra el procés de cerca.
7. **Marca els límits.** Conserva dates, abast, incerteses i desacords entre fonts. No omplis buits amb intuïcions.
8. **Llegeix-ho en veu alta.** Si sembla un examen, un guió promocional o una visita guiada per la fitxa, reescriu-ho o descarta-ho.
9. **Registra la traça fora del diàleg.** Fonts, llicències, evidències i decisions editorials van a procedència, mai al text que entrenarà el model.

## Formes de conversa que sí poden funcionar

- **Dubte pràctic:** «Amb el salari mínim, dona per pagar un lloguer?»
- **Discrepància:** «Per què les dades de població donen dos totals diferents?»
- **Premissa equivocada:** «La Passa és un ball?»
- **Conseqüència o abast:** «Si una comunitat no s'inscriu, vol dir que no pot existir?»
- **Context històric:** «Per què es va deixar de fer servir l'excomunió per cobrar deutes?»
- **Seguiment real:** «Això vol dir que podem saber quanta gent del país segueix cada religió?»

Són patrons possibles, no plantilles per omplir. No cal cobrir cada tipus amb una quota.

## Regles per als seguiments

- Un torn únic és millor que un seguiment artificial.
- El seguiment reprèn una idea que acaba de sortir i demana informació nova.
- No repeteix la pregunta inicial amb altres paraules.
- No serveix per encabir una dada que quedava fora.
- Si la primera resposta ja resol el dubte i no provoca cap pregunta natural, la conversa s'acaba.

## Estructura de treball

```text
training-data/
├── README.md
├── PLAN.md
├── scripts/        # ordres i validacions comunes
├── knowledge/
│   ├── scripts/    # inventari, cobertura i validadors Knowledge
│   ├── review/       # converses candidates i exemples editorials
│   ├── work/         # traça i cobertura internes
│   ├── reports/      # qualitat, cobertura i exclusions
│   └── output/       # només dades revisades per a l'ús previst
└── language/
    ├── scripts/    # selecció i validadors Language
    ├── review/       # candidats de parla per revisar
    ├── work/         # selecció i incertesa de transcripcions
    ├── reports/      # peces incloses i excloses
    └── output/       # només dades revisades per a l'ús previst
```

El fitxer `knowledge/review/conversations.jsonl` és el lot visible de converses candidates. Una línia correspon a una conversa completa, amb missatges alternats `user` i `assistant`. No és una sortida final fins que passa revisió editorial, factual i de drets. La traça associada es desa a `knowledge/review/provenance.jsonl`.

Els `output/` només s'omplen amb registres aprovats per al destí concret. Un directori buit vol dir que encara no hi ha cap lot publicable; les mostres de treball han de ser visibles a `review/`, no amagades en fitxers interns.

## Llindar mínim de revisió

Abans d'acceptar una conversa, comprova:

1. S'entén sense haver vist la fitxa?
2. Es veu per què una persona ho preguntaria?
3. La primera resposta contesta directament?
4. La conversa sona plausible en veu alta?
5. Cada afirmació es pot sostenir amb una font de Maia?
6. El seguiment aporta informació nova i no és forçat?
7. La resposta conserva dates, límits i matisos importants?
8. La procedència i els drets estan registrats?

Una resposta «no» a les preguntes 1, 2, 3 o 5 vol dir reescriure o descartar. Un seguiment que falla la 6 s'elimina sense descartar la resta de la conversa.

## Procés de treball

1. Aprovar l'estil amb unes poques mostres diverses.
2. Recórrer les fitxes tema a tema i redactar converses només quan hi hagi un dubte natural.
3. Revisar cada conversa contra les fonts i anotar-ne la procedència.
4. Fer una revisió de naturalitat i duplicats sobre el lot complet.
5. Separar conjunts relacionats abans de crear `train`, `validation` i `test`.
6. Exportar només després de validar drets, contingut i format.

No hi ha quota de registres. Cobrir una dada no justifica una pregunta dolenta.

## Cobertura completa de Knowledge

- Recorre **totes** les fitxes de `docs/temes/`, incloent-ne cada secció, taula i llista. Cap carpeta temàtica queda fora per ser petita, especialitzada o difícil de preguntar.
- Fes servir l'inventari i les unitats d'evidència de `knowledge/work/` per registrar què queda cobert, pendent o descartat amb motiu.
- Representa el coneixement útil amb una o més converses només quan hi ha un dubte humà natural. Agrupa fets que una persona relacionaria; no generis preguntes artificials per omplir buits de cobertura.
- Conserva límits, cronologia, discrepàncies i buits explícits. Una qüestió irresoluble també es pot representar amb una resposta honesta sobre què no se sap.
- El report final ha de mostrar quines fitxes i quines unitats d'evidència s'han cobert, què s'ha exclòs i per què. «Tots els fitxers llegits» no prova per si sol que s'hagi cobert tot el coneixement útil.

## Cobertura completa de Language

- Inspecciona totes les peces de `docs/parla/`.
- Inclou només veu originària, contemporània i marcada `apte_llengua: true`, amb transcripció prou fiable i procedència registrada.
- Conserva la intervenció humana. No inventis preguntes o respostes per convertir un monòleg en diàleg, no normalitzis la varietat andorrana cap al català genèric i no expandis fragments amb un LLM.
- Si una conversa real està transcrita, mantén-la en ordre i agrupa-la per peça i parlant abans de separar splits. Registra fragments exclosos i el motiu.
- El report ha d'enumerar totes les peces, les elegibles utilitzades i les exclusions. Cap peça queda implícitament ignorada.

## Commits, splits i preparació per entrenar

- Cada conversa nova o modificada al JSONL de revisió és un commit propi i un push a `main`. Els canvis de pla, estructura i validadors poden tenir commits funcionals separats.
- No copiïs candidats a `output/` fins que la conversa i la seva procedència hagin passat revisió factual, editorial i de drets per al destí previst.
- Abans de crear `train`, `validation` i `test`, agrupa per fitxa, tema, source document i conversa d'origen. Cap reformulació o torn gairebé duplicat pot caure en un altre split.
- Abans de declarar-ho preparat per entrenar, valida totes les línies JSONL, els rols i l'ordre dels torns, continguts no buits, hashes de procedència, duplicats, drets i cobertura. Publica els recomptes i exclusions.

## Definition of Done per conversa

- El dubte és independent de la fitxa i té una motivació humana recognoscible.
- La resposta és directa, natural i fidel a l'evidència.
- Cada seguiment és espontani i aporta informació nova; si no, s'elimina.
- La conversa i la seva procedència estan separades.
- La conversa no és una variant redundant d'una altra.
