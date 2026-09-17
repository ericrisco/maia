---
type: font
id: bopa
title: "Butlletí Oficial del Principat d'Andorra (BOPA)"
titular: Govern del Principat d'Andorra
autor: institucional
publicacio: "BOPA, des del 1989. Arxiu en linia complet."
url: https://www.bopa.ad/
llicencia: "Publicacio oficial de l'Estat andorra. Sense llicencia explicita al portal; es la font autentica del dret publicat."
redistribucio: pendent
data_consulta: 2026-09-17
abast: >
  Font oficial per a tot el bloc normatiu del corpus. Consultada per primera
  vegada el 17-09-2026, quan es va establir com arribar-hi.
notes: >
  COM S'HI ARRIBA, perque el portal es una aplicacio JavaScript i no serveix res
  per HTTP directe. L'API Azure del BOPA es PUBLICA i respon SENSE CAP CLAU:
    POST https://bopaazurefunctions.azurewebsites.net/api/GetPaginatedDocuments2Indexes
    {"textSearch":"...","temaFilter":[],"dateFilter":[],"organismeFilter":[],
     "butlletiFilter":"<num>","anyFilter":[],"size":20,"skip":0,
     "orderBy":"DataPublicacioButlleti desc, DataArticle desc","searchMode":1}
  Cada resultat porta un objecte `document` amb `metadata_storage_path`, que es
  la URL del blob public amb l'HTML. El blob es llegible per nom i NO es pot
  enumerar: el contenidor respon 404 a la llista.
  FILTRES: `butlletiFilter` funciona amb el numero de butlleti com a text.
  `anyFilter` i `dateFilter` van donar 400 en totes les formes provades.
  L'HTML del blob ve en UTF-16: cal descodificar-lo abans de res.
  `GetFilters` retorna l'arbre d'organismes i temes, tambe sense clau.
tema: fonts
veu: compilada
epoca: contemporania
apte_llengua: false
timestamp: 2026-09-18T00:30:00Z
tags: [font, dret, normativa, institucional]
---

# BOPA — Butlletí Oficial del Principat d'Andorra

## Per què aquesta fitxa existeix

**El corpus tenia vint-i-vuit buits que remetien al BOPA i cap manera d'arribar-hi.**
**El portal és una aplicació JavaScript**: qualsevol petició HTTP directa torna
la closca. **Durant tota una sessió es va donar per bloquejat.**

**No ho està.** **L'API del BOPA és pública i respon sense cap clau**, i les
instruccions per fer-la servir són a les notes d'aquesta fitxa.

## El que això obre

**Tot el dret publicat andorrà des del 1989**, article per article, amb el
sumari, el número de butlletí, l'any, la data de publicació i l'enllaç al
document. **És la font autèntica**, i **substitueix els reculls de tercers per a
qualsevol pregunta sobre què diu una norma i quan es va publicar.**

## Related

- [El Concordat del 2008](../temes/institucions/coprincipat/el-concordat-del-2008.md) — el primer buit que aquesta via va tancar.
