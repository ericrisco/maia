# Comparació internacional i TIC per l'API d'Estadística

**Baixat el 18-09-2026** de l'API pública descrita a
[`../README.md`](../README.md).

| | |
| --- | --- |
| **Fitxer** | `comparacio-internacional-api-2026-09-18.tsv` — **50.726 valors** |
| **Columnes** | `idDivision · taula · codi · serie · periode · valor` |
| **Font** | **Departament d'Estadística** |
| **Llicència** | **CC BY 4.0** — **redistribució: sí**, amb atribució |
| **Abast** | **306 divisions** del prefix `0303`: sistema d'indicadors en estadística comunitària europea, indicadors de l'Estratègia Europa 2020, indicadors de globalització, societat de la informació i enquesta TIC |
| **Divisions que no responen** | **8** |

## El que aquest bolcat ha obert

**La taxa d'atur.** **El corpus havia escrit que Andorra no en publicava cap.**
**En publica**: **1,8% el 2018, 2,2% el 2019, 3,1% el 2020, 3,3% el 2021, 2,1%
el 2022 i 1,6% el 2023**, amb **taxa d'ocupació (15-64) del 80,7% al 83,2%** i
**taxa d'activitat del 81,2% al 84,6%.** Escrit a
[l'ajut per desocupació involuntària](../../../temes/societat/treball/lajut-per-desocupacio-involuntaria.md).

**L'assoliment d'educació superior als 30-34 anys**: **41,8% el 2018, 48,0% el
2023**, i **per sexe el 2020: dones 42,4%, homes 32,4%.**

## El defecte que travessa tot el sistema d'indicadors

**Cada taula té una finestra d'anys vàlida diferent i cap no ho declara.**

| Taula | Anys amb dades | Anys trencats |
| --- | --- | --- |
| **Pobresa i exclusió social (taxes)** | **2021-2024** | **2018, 2019, 2020** valen `0`, `0,1` o `0,2` |
| **Mercat laboral (taxes)** | **2018-2023** | **2024** val `0` i `0,8` |
| **Educació** | **2018-2023** | **2024** val `0,6` |

**I hi ha una segona cosa que convé saber**: **on aquestes taules se solapen amb
l'enquesta de condicions de vida** (`../pobresa/`), **donen exactament els
mateixos valors**. **No són dues mesures: és la mateixa sèrie servida dues
vegades**, i **la còpia del sistema europeu és la que té la finestra trencada.**

**Conclusió pràctica**: **aquesta font val per al que l'enquesta no publica**
—taxa d'atur, taxa d'ocupació, assoliment d'educació superior— **i per a la
resta val més l'original.**

## Una taula que no es pot citar tal com està

**`INDICADORS D'ANDORRA EN L'ESTRATÈGIA EUROPA 2020. OCUPACIÓ`** té dotze
files sota un sol títol i **no totes mesuren el mateix**. **Les tres de «taxa
d'ocupació per nivell d'educació assolit» sumen 100,0** —36,8 + 35,7 + 27,5— i
**per tant són una distribució dels ocupats, no taxes d'ocupació**, encara que
l'etiqueta digui «taxa». **El corpus no en cita cap fins que no es pugui
comprovar què és cada fila.**

## El que queda sense explotar

**Tota l'enquesta TIC** —competències digitals, activitats a internet, comerç
electrònic, administració electrònica, big data, assessors en TIC— **creuada per
edat, sexe, nivell d'estudis, nivell d'ingressos i situació laboral**; **els
indicadors de globalització i comerç internacional**; i **els indicadors
d'energia i medi ambient del sistema europeu.**
