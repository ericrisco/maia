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
  RESPOSTA: {"totalCount": N, "paginatedDocuments": [{"document": {...}}]}.
  Els `highlights` arriben amb la codificacio trencada; les metadades i el blob,
  no. No fer servir mai els highlights: el text bo es llegeix del blob.
  CERCA (les dues regles que decideixen si trobes una cosa o no):
    1) Entre COMETES es cerca la frase sencera. Sense cometes es un OR de
       paraules i dona centenars de resultats inutils.
    2) `orderBy` BUIT ordena per rellevancia, i es l'unica manera de trobar un
       document antic: amb l'ordre per data, una llei del 1993 queda enterrada
       sota mil edictes del 2026 que comparteixen una paraula.
  El script amb les dues regles aplicades:
  `02-DOCS/raw/operations/gap-audit-scripts/bopa.py cerca | baixa`.
  TAULES: cal convertir-les abans d'esborrar les etiquetes HTML, o una matriu
  de sancions queda com una columna de xifres soltes i el document sembla
  llegit quan no ho es.
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

## Fins on arriba enrere, i què vol dir

**El BOPA comença el 1989**, i **això té dues conseqüències que el corpus ha
comprovat les dues el mateix dia.**

**La primera és que hi ha coses que s'hi donaven per absents i hi són.** **La
Llei de l'Escola Andorrana del 2 de maig del 1989** es donava per «anterior a la
sèrie consultable»: **surt al butlletí núm. 9, del 19 de maig del 1989**. **Hi
és per dos mesos.**

**La segona és que hi ha coses que no hi seran mai, i ara es pot dir per què.**
**La llei de creació de l'Escola nacional andorrana d'esquí és del 23 de
setembre del 1988** i **el reglament de creació dels Arxius Nacionals, del 22 de
desembre del 1975**. **No són buits de cerca: són anteriors al medi.**

**La regla que se'n deriva**: **abans de declarar que una norma andorrana no es
pot trobar, mirar-ne la data.** **Del 1989 ençà, hi és.**

## Buscar-hi i no trobar-hi també és un resultat

**Dues vegades el 17-09-2026, la cerca exhaustiva al BOPA va tancar un buit
dient que no.** **La memòria anual de la CNAAD**, obligatòria des del 2022, **no
s'hi ha publicat mai**; i **la frase «informació reservada d'Estat» dona dos
documents a tot el Butlletí i tots dos són lleis, cap acte de declaració.**
**En tots dos casos la via queda descartada, no pendent**, i **això val tant com
trobar el document.**

## Related

- [El Concordat del 2008](../temes/institucions/coprincipat/el-concordat-del-2008.md) — el primer buit que aquesta via va tancar.
