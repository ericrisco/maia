---
type: knowledge-fiche
title: Salari i remuneració de les dones a Andorra
description: "Sèries estadístiques de salari per sexe, les diferències entre mesures i els límits que impedeixen atribuir-ne les causes."
topic: societat
source_doc: docs/temes/societat/dones/vuitanta-cinc-coma-nou.md
review_status: complete-with-unresolved
sources:
  - source_id: estadistica-ad
    source_doc: docs/fonts/estadistica-ad.md
    url: https://www.estadistica.ad/
    location: "API del Departament d'Estadística: divisions 408 i 417; divisions 780–783; enquesta «Remuneració bruta dels assalariats per … i sexe» (2015–2024); dades preservades a docs/raw/estadistica-api/treball-mercat/ i docs/raw/estadistica-api/les-que-no-responien/."
    llicencia: CC BY 4.0 per a la informació estadística pròpia, llevat d'indicació contrària
    redistribucio: si
related_fiches:
  - knowledge/societat/fichas/dones-index-de-fitxes.md
  - knowledge/societat/fichas/llei-igualtat.md
  - knowledge/societat/fichas/sufragi-femeni.md
  - knowledge/societat/fichas/treball.md
  - knowledge/societat/fichas/la-piramide-de-prestigi.md
  - knowledge/societat/fichas/el-salari-minim-de-362-pessetes-a-9-euros.md
---

# Salari i remuneració de les dones a Andorra

Les dades disponibles descriuen diverses dimensions de la remuneració femenina. No són una única sèrie homogènia: les mitjanes de desembre, la massa salarial agregada i l'enquesta de remuneració amb desglossaments per categories responen preguntes diferents.

## Evolució del salari mitjà

La comparació mensual del desembre situa el salari mitjà de les dones en el 55,8% del masculí el 1967 i en el 85,9% el 2025. El punt més baix de la sèrie és el de 1967; el més alt, el de 2025. La progressió no és regular: la relació retrocedeix entre 1970 i 1975 i torna a baixar, més moderadament, entre 2000 i 2005. La dada de 1975 no permet explicar per què es va produir aquell descens.

La diferència en euros tampoc segueix el mateix patró que la proporció. El 1990 era d'uns 278 euros mensuals, el 2010 d'uns 553 i el 2025 d'uns 493. Una proporció més alta no implica que la distància monetària baixi al mateix ritme.

La comparació recull mitjanes mensuals de tots els assalariats d'un període concret. Per si sola no controla jornada, ocupació, antiguitat, contracte ni composició sectorial, i no permet afirmar quant es paga a dues persones per una feina equivalent.

## Mesures que no s'han de confondre

La massa salarial registra el total abonat a cada grup i combina el nombre de persones amb els salaris individuals. El desembre de 2025, les dones van representar el 43,6% de la massa salarial recollida; el 1990 n'havien representat el 33%. Aquesta proporció no és el salari mitjà femení ni la proporció de dones assalariades.

L'enquesta de remuneració bruta de 2024 permet comparar mitjanes dins categories de jornada, contracte, estudis, sector i ocupació. Les relacions dones/homes varien segons el tall: 73,1% en jornada completa, 74,1% amb contracte indefinit, 51,0% amb contracte temporal, 92,4% al sector públic i parapúblic i 64,6% al privat. Aquestes categories aporten context, però no equivalen necessàriament a comparar la mateixa feina, experiència i responsabilitat. Algunes cel·les d'ocupació tenen molt poques persones; les dues mitjanes per sobre del 100% s'han de llegir amb aquesta limitació.

La nota anual de gènere basada en dades de la CASS també presenta una sèrie diferent: el 2024 situa el salari mitjà femení en el 80,7% del masculí. Aquesta mitjana anual no coincideix amb el 85,0% de la comparació de desembre del mateix any. La diferència no és una contradicció automàtica: les sèries provenen de mesures i períodes de referència diferents. Cap de les dues, per si sola, identifica una causa.

## Qualitat de les dades i correccions

La sèrie de massa salarial i salari mitjà per sexe (divisions 408 i 417) es va recuperar mensualment, en blocs de períodes més curts, entre juliol de 1966 i juny de 2026. En canvi, les altres divisions del bolcat de treball es van conservar principalment per als mesos de desembre, a causa de les limitacions de resposta de l'API.

La revisió va detectar dues columnes femenines desalineades a les taules per sector: la divisió 779, sobre nombre d'assalariats, i la 783, sobre salari mitjà. Es van corregir les etiquetes desplaçades abans d'interpretar els valors sectorials. També es va excloure la columna femenina de la divisió 1055 sobre antiguitat, perquè repetia els valors de la divisió 1051 sobre edat en tres anys comprovats. Aquest defecte no invalida la sèrie d'edat.

Les divisions 402 i 411, que creuarien sector i edat amb massa salarial i salari mitjà, continuaven retornant errors HTTP després de limitar les consultes als desembres i a diversos anys de prova. El corpus no en disposa de resultats.

## Punts que continuen oberts

- Les dades disponibles no aïllen completament l'efecte de la mateixa ocupació, responsabilitat, antiguitat i condicions contractuals. Els talls de l'enquesta redueixen part de la incertesa, però no constitueixen una mesura causal de discriminació salarial.
- La caiguda de la relació entre dones i homes del 1970 al 1975 no té una explicació documentada en les sèries consultades.
- No s'han recuperat els creuaments sector × edat de les divisions 402 i 411. La font consultada descriu els codis i els errors, però no ofereix les dades.
- La font estadística no explica per si sola què va provocar els canvis observats al llarg del temps. No s'atribueixen a una llei, a la conjuntura econòmica ni a una transformació concreta sense evidència addicional.

## Fitxes relacionades

- [Índex de coneixement sobre les dones](dones-index-de-fitxes.md): situa aquesta sèrie dins d'una branca temàtica més àmplia.
- [La Llei 6/2022 d'igualtat](llei-igualtat.md): conté obligacions legals relacionades amb dades desagregades i la seva pròpia sèrie anual salarial.
- [El sufragi femení](sufragi-femeni.md): permet distingir canvis en drets polítics de les mesures contemporànies de remuneració.
- [Treball](treball.md): registra l'estacionalitat i la sèrie d'assalariats del país.
- [La piràmide de prestigi](la-piramide-de-prestigi.md): relaciona les mitjanes salarials per origen amb una descripció sociològica del prestigi percebut.
- [El salari mínim](el-salari-minim-de-362-pessetes-a-9-euros.md): contrasta el llindar legal amb les dades sobre salaris efectivament declarats.
