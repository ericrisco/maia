# Pla de treball de Maia Training Data

## Objectiu

Preparar dos datasets per a fine-tuning, amb cobertura traçable i sense barrejar coneixement enciclopèdic amb senyal de parla real.

- **Knowledge** respon preguntes naturals sobre Andorra amb fets verificables a `docs/temes/`.
- **Language** conserva formes reals del català andorrà contemporani a `docs/parla/`. No s'inventen respostes per imitar una veu local.

## Com ha de sonar Maia Knowledge

Cada conversa parteix d'un dubte que algú podria tenir sense conèixer les fitxes del corpus. La primera pregunta dona el context necessari. La resposta comença resolent el dubte i després explica el matís que ajuda a entendre'l.

Les repreguntes segueixen el mateix fil: poden aclarir una paraula, preguntar «i això encara es fa?», explorar una conseqüència o comprovar una dada sorprenent. No serveixen per anar recollint una dada diferent de cada paràgraf. Les preguntes curtes són bones quan el context ja és a la conversa.

Cada registre és una conversa multitorn: té almenys dos torns d'usuari. El seguiment ha de néixer de la resposta anterior i obrir un pas nou del mateix dubte. Si no surt cap repregunta natural, no s'inventa per omplir una quota: es busca un altre angle o s'ajorna el registre. Cada resposta resol el torn completament i sona natural llegida en veu alta. Pot fer servir el context de la conversa, però mai queda com un fragment que només s'entén llegint la fitxa.

### Angles que poden donar preguntes humanes

- sorpresa o aparent contradicció: «Com pot ser que…?»
- comprovació d'una idea: «Això vol dir que…?»
- distinció entre conceptes propers: «És el mateix que…?»
- significat o conseqüència: «I això què canviava?»
- passat i present: «Encara es fa així?»
- incertesa o desacord: «Se sap del cert?»
- context pràctic: «Quan ho podria veure?»

Són idees per inspirar-se, no plantilles. Cal variar la manera d'entrar al tema i evitar preguntes que semblin generades per un formulari.

### Respostes i límits

- Contesta primer la pregunta; dona només el context pertinent.
- Situa les dates i pràctiques en el període que la font documenta.
- Separa fet, tradició, interpretació i hipòtesi.
- Si dues fonts discrepen, explica què diu cadascuna; no inventis una reconciliació.
- Si el corpus no ho resol, digues-ho amb claredat i concreta què sí que se sap.
- Corregeix premisses errònies amb naturalitat i sense renyar.
- No mencionis fitxes, seccions, IDs, estats interns ni procedència dins del diàleg.

## Porta de qualitat abans d'afegir una conversa

Una conversa només entra a `knowledge/review/conversations.jsonl` quan passa tots aquests controls:

1. **Pregunta inicial humana**: planteja una curiositat, una decisió pràctica o una confusió plausible; no demana explicar una secció, una fitxa, una fila o un fragment.
2. **Resposta resolutiva**: la primera frase respon el dubte. La resposta dona el context imprescindible i es pot llegir sola com a resposta a aquell torn.
3. **Seguiment real**: hi ha almenys una repregunta amb referents clars, informació nova i continuïtat. No és una pregunta de comprovació afegida mecànicament.
4. **Diàleg autònom**: una persona que no ha vist el corpus entén de què parlen. No apareixen expressions com «la fitxa diu», «a la secció», «el corpus registra» ni instruccions editorials.
5. **Fets i límits**: cada afirmació està coberta per les fonts. Tradició, interpretació, dada històrica i fet verificat no es confonen; els buits es diuen clarament.
6. **Drets i utilitat**: la procedència queda registrada. Si la reutilització per entrenar està prohibida o pendent, la conversa pot servir per calibratge intern però no es promou a l'export.

Una pregunta sintàcticament correcta no passa si sona a qüestionari sobre el document. Una resposta que comença «I dos topònims que en surten:» o «Tres coses que el corpus registra per separat:» no és una resposta completa i s'ha de reescriure, no retocar només al final.

## Flux de creació i revisió

1. Tria un tema i llegeix la fitxa sencera, les fonts citades i les notes de drets.
2. Escriu el dubte humà i la resposta factual que el resol.
3. Afegeix només seguiments que una persona faria després d'escoltar la resposta.
4. Fes una lectura cega: sense mirar les fonts, comprova que el diàleg flueix i que cada resposta és clara.
5. Verifica cada afirmació i cada límit contra les fonts. Registra font, llicència, atribució i condicions a `provenance.jsonl`.
6. Desa a `knowledge/review/` només les converses que hagin passat la porta de qualitat. Mantén els exemples de calibratge separats i exclosos de l'entrenament.
7. Actualitza la cobertura només per als fets realment resolts. Deduplica i revisa drets abans d'exportar.
8. Quan hi hagi prou material, agrupa converses relacionades abans de crear train/validation/test per evitar que reformulacions similars caiguin en splits diferents.

No s'exporta una conversa si no passa la lectura natural, la verificació factual i la revisió de drets.

## Maia Language

Inclou només material que compleixi `veu: originaria`, `epoca: contemporania` i `apte_llengua: true`, amb drets adequats i transcripció prou verificada. La resposta ha de provenir de la persona enregistrada i conservar-ne el lèxic i la sintaxi; no s'estandarditza ni es reescriu com si fos una conversa nova. Les peces incertes s'exclouen o es limiten als fragments verificats. Els splits s'agrupen per peça o parlant per evitar filtracions.

## Abast i definició de finalització

L'objectiu és completar Knowledge i Language; l'estructura, l'inventari i els exemples només en són els primers passos. No es limita l'abast a una mostra ni a un nombre fix de converses.

Per a Knowledge, s'ha de revisar tot `docs/temes/`, incloent-hi els continguts útils de cada secció, llista i taula. `knowledge/work/coverage.csv` és l'inventari de seguiment: cada document ha d'acabar cobert per una o més converses, o marcat amb un motiu explícit d'exclusió, falta de font o límit de drets. Una fitxa amb una conversa parcial continua parcial. Les dades canviants que la constitució del projecte reserva per a recuperació no s'exporten com a fets permanents del fine-tuning.

Per a Language, s'han d'auditar totes les fitxes de `docs/parla/`. Cada fragment inclòs ha de complir els criteris de veu, època i aptitud, tenir drets i ús registrats, i una transcripció escoltada i prou fiable. Les peces no verificades o incertes continuen fora de l'export fins que s'aclareixin.

Un dataset no es considera acabat fins que:

- Knowledge cobreix o justifica explícitament l'exclusió de cada document i contingut entrenable del corpus.
- Language registra la decisió per a cada peça i només inclou fragments humans verificats i autoritzats.
- Les preguntes són naturals, les converses segueixen el fil i les respostes reflecteixen els límits de les fonts.
- La procedència i les condicions d'ús es poden rastrejar per registre.
- Duplicats i filtracions entre splits s'han revisat; train, validation i test són JSONL vàlids i estan agrupats per evitar leakage.
- Els informes expliquen la cobertura, les exclusions, els drets i les limitacions.

Els fitxers d'output s'omplen quan hi hagi registres aprovats; no es creen exports buits ni es compten els exemples de calibratge com a dades d'entrenament.
