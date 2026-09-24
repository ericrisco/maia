---
type: index
title: "Registre de canvis del cervell andorrà"
---

# Registre de canvis del cervell andorrà

Aquesta pàgina explica, commit a commit, què entra al corpus i per què. Cada
entrada correspon a un commit del repositori i en repeteix el títol: per trobar
el canvi exacte, cerqueu el títol a `git log`. Cada entrada diu quina font s'ha
incorporat o revisat, quins articles en depenen, on és el material de partida
i quin diari de treball documenta la troballa i els seus límits.

Les entrades s'afegeixen al final. No es reescriuen: si una font canvia, se'n
fa una entrada nova.

## Abans d'aquest registre

Fins al 24 de setembre de 2026 el repositori acumulava 2.733 commits locals
sense publicar. Es van publicar tots de cop, amb una sola intervenció a
l'historial: `docs/raw/estadistica-api/resta-del-cataleg/resta-cataleg-api-2026-09-18.tsv`
(102,6 MB) supera el límit de 100 MB de GitHub i es va migrar a Git LFS a tots
els commits on apareix. El contingut del fitxer no ha canviat.

La descripció d'aquells commits és al seu missatge (`git log`). Aquest registre
comença amb la tanda següent: la revisió del cervell per relació amb Andorra i
les fonts arxivístiques incorporades entre el 22 i el 25 de setembre de 2026.

## Entrades


### 1. 🧹 retira del cervell el material sense relació amb Andorra

Revisió document a document del brain: un fitxer no es considera andorrà només perquè contingui la paraula «Andorra». S'eliminen cinc blocs EWA sense relació amb el país (l'homònim de Budapest 1939–1940, la genealogia Belfort/Delvert/Carla, l'arxiu familiar de Chciuk, el dossier Stempowski i el catàleg SPP) i el capítol de David Crystal sobre l'anglès mundial, que no aportava cap dada andorrana; la dada bibliogràfica es manté a l'article de manlleus. Es conserven explícitament els dossiers de Miranda, Girona, Viadiu i Grumbach perquè alimenten Els passadors. La nota de Fontargente perd l'apèndix sense dades andorranes. El detall fitxer a fitxer (5.310 baixes) és a 2026-09-23-revisio-brain-andorra-deletes.tsv.

- Fitxa retirada: `fonts/david-crystal-english-worldwide.md`
- Material de partida: 8 fitxers a `raw/sdd/ewa/budapest-homonym/`, `raw/sdd/ewa/chciuk-celt/family-archive/`, `raw/sdd/ewa/chciuk-celt/jerzy-stempowski/`, `raw/sdd/ewa/chciuk-celt/krzysztof-tutaj/spp/`, `raw/sdd/ewa/chciuk-celt/miranda/`, `raw/sdd/ewa/eloise-fontargente/` …
- Diari de treball: `raw/worklog/2026-09-23-revisio-brain-andorra-deletes.tsv`
- Diari de treball: `raw/worklog/2026-09-23-revisio-brain-andorra.md`
