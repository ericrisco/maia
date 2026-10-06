# Maia Language

Dataset separat per conservar llengua humana andorrana contemporània a partir
de `docs/parla/`. Aquest pilot no genera preguntes ni diàlegs nous: primer cal
inspeccionar quines peces contenen torns humans identificables, transcripcions
fiables i permisos de redistribució suficients.

Quan una font és un monòleg o no identifica els torns, no li atribuïm una
conversa inventada. La feina de Language començarà després de fixar els criteris
d'elegibilitat i revisar el material.

El primer inventari troba 45 entrades, 40 peces de parla i 38 peces que passen
els filtres bàsics de metadades. Hi ha 8.449 spans d'incertesa i cap parella de
torns explícita `user`/`assistant`. Les 40 referències a fonts tenen
redistribució pendent. El report és a `reports/eligibility.json`; no hi ha
encara material publicable per entrenar.
