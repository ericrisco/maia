# Pla editorial del dataset

## Objectiu

Crear exemples que ensenyin Maia a respondre preguntes que una persona faria
realment. El valor és que la conversa resolgui un dubte, no que esmenti cada
apartat del corpus. Cobertura i naturalitat es revisen alhora, però cap dada
no s'ha de convertir en una pregunta forçada per poder marcar-la com a coberta.

## Com escriure una conversa de Knowledge

1. Llegeix la fitxa sencera i segueix els enllaços necessaris. Revisa correccions,
   excepcions, desacords, límits temporals i buits.
2. Tria una idea concreta que resolgui un dubte humà: una confusió habitual,
   una decisió pràctica, una dada sorprenent o una curiositat amb context.
3. Escriu la pregunta sense fer veure que la persona ha llegit la fitxa. Afegeix
   només el context que li caldria per fer-se entendre.
4. Contesta el dubte de seguida. Escriu com parlaria un assistent: clar, breu i
   sense repetir l'estructura, els títols ni les frases de la font.
5. Continua només si la resposta desperta una pregunta següent concreta. El
   seguiment ha de dependre del que s'acaba de dir. Una conversa pot tenir un
   sol intercanvi; no hi ha quota de torns.
6. Comprova cada fet, xifra i matís contra les fonts. Digues qui sosté una
   interpretació quan no és un fet establert. Conserva les discrepàncies i la
   incertesa en llenguatge planer.
7. Llegeix tota la conversa en veu alta. Si sona com un examen, una cerca dins
   d'un document o un qüestionari generat, reescriu-la o descarta-la.
8. Desa la conversa i la procedència en fitxers separats. Revisa llicència,
   atribució i permís d'ús abans d'exportar-la.

### Multitorn natural

Un bon fil fa un pas recognoscible: aclarir una paraula, entendre una
conseqüència, preguntar pel lloc o el moment, o comprovar una possible
confusió. No facis que l'usuari pregunti successivament per cada dada de la
fitxa. No afegeixis una pregunta del tipus «i què més?» només per allargar el
registre. No inventis biografia ni experiències personals per fer-lo semblar
real.

### Rebutja o reescriu

- «Què explica la secció…?», «què indica aquesta fila?» o preguntes que només
  tenen sentit amb la fitxa oberta.
- Preguntes de plantilla repetides per cobrir noms, dates i xifres sense cap
  motiu humà.
- Respostes que comencen amb etiquetes internes o que deixen la frase a mitges.
- Seguiments que demanen una dada sense cap relació amb la resposta anterior.
- Afirmacions actuals basades només en una font antiga, o certeses que esborren
  una divergència del corpus.

## Knowledge i cobertura

Les fonts factuals són `docs/temes/` i les seves fonts originals registrades a
`docs/fonts/` i `docs/raw/`. Quan comenci la producció, s'inventariaran fitxes,
seccions, taules, llistes i afirmacions rellevants. Per cada peça es decidirà
si dona lloc a una conversa útil, ja està coberta, es repeteix o no es pot usar.
La cobertura es mesurarà sobre aquest inventari; el recompte de preguntes per
si sol no prova que el corpus estigui ben cobert.

## Language

`language/` només pot ensenyar llengua provinent de parlants humans identificats
al corpus. No es redacten preguntes d'entrevistador que s'han eliminat, ni es
converteix un monòleg en una conversa fictícia. Primer cal confirmar la
transcripció, els drets i que l'estructura real permeti el format d'entrenament.
Si no hi ha intercanvi humà autèntic, no es fabrica un torn d'usuari per omplir
un JSONL de xat.

## Estat i passos següents

1. Revisar aquests exemples i acordar el llindar de naturalitat.
2. Construir l'inventari exhaustiu de Knowledge i registrar drets per font.
3. Escriure i revisar converses en lots petits, sense preguntes automàtiques.
4. Revisar exactitud, naturalitat, redundància, cobertura i drets.
5. Exportar només registres aprovats als splits de destinació i publicar un
   informe de cobertura i exclusions.
6. Auditar `docs/parla/` abans de crear registres de Language.

No es generen splits d'entrenament fins que hi hagi registres aprovats i una
revisió de drets completa.
