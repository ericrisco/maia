# Pla de Maia Training Data

## Objectiu

Preparar dos conjunts separats a partir de `docs/`:

- **Maia Knowledge**: respostes útils sobre Andorra, basades en `docs/temes/`.
- **Maia Language**: mostres de català andorrà contemporani extretes de parla
  humana elegible a `docs/parla/`.

Knowledge no és un qüestionari sobre les fitxes. Cada conversa ha de resoldre
una necessitat que una persona podria tenir. Language no inventa diàlegs per
imitar una veu local.

## Punt de partida

El primer conjunt de converses s'ha retirat del fitxer actiu perquè la revisió
va detectar preguntes que depenien de títols i seccions, respostes fragmentàries
i seguiments afegits per rutina. Les tres converses actuals són mostres de
calibratge, no dades d'entrenament aprovades. L'inventari, la procedència i les
decisions de cobertura es conserven per reprendre la feina amb traçabilitat.

No generarem més registres fins que aquestes mostres passin una lectura humana.
Si una mostra falla, la reescriurem abans d'ampliar el conjunt.

## Com redactar Knowledge

1. **Comença per la intenció.** Escriu en una frase què vol esbrinar la persona:
   entendre una història, planificar una visita, aclarir una diferència o
   comprovar una afirmació.
2. **Redacta la pregunta sense el document al davant.** No facis servir
   «aquesta secció», «aquesta fila», «la fitxa» ni cap referència que exigeixi
   haver llegit la font.
3. **Contesta el dubte primer.** Després afegeix només el context que ajudi a
   entendre la resposta. No deixis frases penjades ni llistes sense explicar-ne
   la relació.
4. **Segueix el fil de la persona.** Una conversa pot tenir un sol intercanvi.
   Afegeix un torn quan la resposta obri un dubte concret que una persona podria
   plantejar. No facis preguntes de confirmació només per allargar-la.
5. **Respecta el que se sap.** Distingim fets, llegendes, interpretacions,
   hipòtesis i buits. Si el corpus no permet resoldre una pregunta, digues-ho
   sense inventar una resposta.
6. **Llegeix només el diàleg.** Si no s'entén sense la fitxa, encara no és una
   conversa útil.

### Abans d'aprovar un registre

- La pregunta inicial sona com una petició real, no com un exercici d'extracció.
- La resposta és directa, completa i prou breu per a la pregunta.
- Cada seguiment és conseqüència del torn anterior i afegeix informació útil.
- No hi ha afirmacions que no estiguin sostingudes per les fonts declarades.
- Les fonts permeten la redistribució i l'atribució queda registrada.
- El missatge visible no conté IDs, notes editorials ni llenguatge del pipeline.

Quan hi hagi dubte entre una conversa llarga i una curta, conserva només els
intercanvis que una persona faria de debò.

## Estructura i fitxers

- `knowledge/review/conversations.jsonl`: missatges visibles per a l'usuari.
- `knowledge/review/provenance.jsonl`: una línia paral·lela amb fonts, drets,
  afirmacions sostingudes, límits i estat de revisió.
- `knowledge/review/EXEMPLES.md`: criteris i mostres de calibratge.
- `knowledge/work/`: inventari i estat de cobertura regenerables.
- `knowledge/reports/`: resum d'inventari i cobertura.
- `knowledge/output/`: splits finals, només quan estiguin revisats.
- `language/`: procés separat per a la llengua humana elegible.

Les mostres de calibratge duen `review_status: approved_sample`. No compten com
a registres aprovats ni cobreixen unitats de contingut. La procedència manté el
mateix ordre que `conversations.jsonl`.

## Seqüència de treball

1. Llegir i validar aquestes mostres amb una persona.
2. Corregir les mostres fins que sonin naturals i siguin factualment sòlides.
3. Reprendre Knowledge per tema, partint d'intencions humanes i revisant els
   drets abans d'incorporar cada conversa.
4. Revisar cobertura per unitat sense forçar una pregunta per cada fragment.
   Registrar exclusions i buits amb una raó clara.
5. Deduplicar i separar train, validation i test per grup de contingut.
6. Reprendre Language només amb material humà que compleixi drets, consentiment,
   origen, contemporaneïtat i qualitat de transcripció.
7. Validar els formats, les fonts, els splits i els informes abans de publicar
   cap export.

Els passos es fan incrementalment. Cada canvi funcional es revisa i es valida
abans del seu commit i push.

## Criteri d'acabament

Knowledge només estarà llest quan el corpus rellevant estigui cobert, les
converses siguin naturals, les fonts permetin l'ús, no hi hagi duplicats
inútils, els splits siguin vàlids i existeixi un informe de cobertura.

Language només estarà llest quan totes les peces candidates s'hagin revisat,
només s'hi inclogui material elegible, es preservi la parla humana, els splits
evitin filtracions i existeixi un informe d'inclusions i exclusions.
i seguiments afegits per rutina. Les tres converses actuals són mostres de
