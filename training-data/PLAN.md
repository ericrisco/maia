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

## Fites

1. Reiniciar l'estructura i acordar el patró de qualitat amb exemples.
2. Crear i revisar converses Knowledge per cobrir el corpus progressivament.
3. Auditar elegibilitat, transcripció i drets de Language abans d'extreure fragments.
4. Deduplicar, validar, generar splits i publicar informes de cobertura i exclusions.

Ara només es completa la primera fita. Els fitxers d'output s'omplen quan hi hagi registres aprovats; no es creen exports buits.
