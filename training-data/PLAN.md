# Pla de treball de Maia Training Data

## Objectiu

Preparar dos datasets per a fine-tuning, amb cobertura traçable i sense barrejar coneixement enciclopèdic amb senyal de parla real.

- **Knowledge** respon preguntes naturals sobre Andorra amb fets verificables a `docs/temes/`.
- **Language** conserva formes reals del català andorrà contemporani a `docs/parla/`. No s'inventen respostes per imitar una veu local.

## Com ha de sonar Maia Knowledge

Cada conversa parteix d'un dubte que algú podria tenir sense conèixer les fitxes del corpus. La primera pregunta dona el context necessari. La resposta comença resolent el dubte i després explica el matís que ajuda a entendre'l.

Les repreguntes segueixen el mateix fil: poden aclarir una paraula, preguntar «i això encara es fa?», explorar una conseqüència o comprovar una dada sorprenent. No serveixen per anar recollint una dada diferent de cada paràgraf. Les preguntes curtes són bones quan el context ja és a la conversa.

La conversa acostuma a tenir dos o tres torns d'usuari. No s'allarga per complir una quota. Cada resposta ha de ser completa, directa i natural llegida en veu alta; pot referir-se al que s'acaba de dir, però no pot quedar en un fragment incomprensible fora de context.

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

## Flux de creació i revisió

1. Tria un tema i llegeix la fitxa sencera, les fonts citades i les notes de drets.
2. Escriu el dubte humà i la resposta factual que el resol.
3. Afegeix només seguiments que una persona faria després d'escoltar la resposta.
4. Fes una lectura cega: sense mirar les fonts, comprova que el diàleg flueix i que cada resposta és clara.
5. Verifica cada afirmació i cada límit contra les fonts. Registra font, llicència, atribució i condicions a `provenance.jsonl`.
6. Desa converses candidates a `knowledge/review/`. Mantén els exemples de calibratge separats.
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
