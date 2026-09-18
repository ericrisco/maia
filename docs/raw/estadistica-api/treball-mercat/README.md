# Mercat de treball per l'API d'Estadística

**Baixat el 18-09-2026** de l'API pública descrita a
[`../README.md`](../README.md).

| | |
| --- | --- |
| **Fitxers** | `treball-mercat-api-2026-09-18.tsv` — **47.827 valors** · `massa-salarial-desembres-2026-09-18.tsv` — **29.960 valors** |
| **Columnes** | `idDivision · taula · codi · serie · periode · valor` |
| **Font** | **Departament d'Estadística** |
| **Llicència** | **CC BY 4.0** — **redistribució: sí**, amb atribució |
| **Abast** | prefixos `010202` massa salarial i salari mitjà, `010203` taxa d'activitat, `010204` demandants d'ocupació, `010206` inspecció de treball |

## Per què hi ha dos fitxers, i és una regla

**Les divisions de massa salarial i salari mitjà són mensuals des del juliol del
1966.** **L'URL que l'API proposa per a cadascuna fa 5.922 caràcters i el
servidor retorna `500`.**

**S'han demanat només els desembres**, retallant el paràmetre `showColumns`, i
**les setze divisions han respost**. **És la mateixa regla que ja havia calgut
per a la sèrie d'assalariats**: si l'API respon `500`, l'URL és massa llarg.

**El desembre no és una tria arbitrària**: és **el mes que el corpus ja feia
servir per a la sèrie d'assalariats** i el que la font fa servir de referència
anual.

## El que no hi és

- **Divisions 402 i 411** —`MASSA SALARIAL PER SECTOR D'ACTIVITAT (NIVELL 1) I
  EDAT` i `SALARI MITJÀ PER SECTOR D'ACTIVITAT (NIVELL 1) I EDAT`— **van
  retornar `502` fins i tot amb els desembres.** **Es poden tornar a demanar amb
  un rang d'anys més curt.**
- **Els mesos que no són desembre.** Es baixen amb el mateix guió traient el
  filtre, divisió per divisió i amb un rang curt.

## El que aquest bolcat ha obert

- **La bretxa salarial per sexe, desembre a desembre des del 1966**:
  **55,8% el 1967, 85,9% el 2025** —
  [vuitanta-cinc coma nou](../../../temes/societat/dones/vuitanta-cinc-coma-nou.md).
- **Els demandants d'ocupació a final de mes des del gener del 2008**, que és
  **el que Andorra publica en lloc d'una taxa d'atur** —
  [l'ajut per desocupació involuntària](../../../temes/societat/treball/lajut-per-desocupacio-involuntaria.md).

## Una precaució sobre les cel·les petites

**Les taules creuades per sector i sexe tenen cel·les amb molt poques
persones.** El desembre del 2025, la construcció dona **9.388,88 €** de salari
mitjà per a les dones. **Aquestes mitjanes no es poden citar soles**: caldria el
nombre d'assalariades per sector per ponderar-les, i aquest bolcat no el porta.
