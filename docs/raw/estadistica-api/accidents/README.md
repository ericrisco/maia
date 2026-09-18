# Accidents laborals i viaris per l'API d'Estadística

**Baixat el 18-09-2026** de l'API pública descrita a
[`../README.md`](../README.md).

| | |
| --- | --- |
| **Fitxer** | `accidents-api-2026-09-18.tsv` — **1.395 valors** |
| **Columnes** | `idDivision · taula · codi · serie · periode · valor` |
| **Font** | **Departament d'Estadística** |
| **Llicència** | **CC BY 4.0** — **redistribució: sí**, amb atribució |
| **Abast** | **17 divisions**; **2011-2025** per als accidents laborals, **2015-2025** per als viaris |

## Quatre defectes de la font, comprovats

1. **Divisió 1477 (tipus de lesió), any 2021: «Esquinçada» val 1.336**, que és
   **exactament el total d'aquell any**. **És un error de la font**, i **el 2025
   la mateixa sèrie cau a 288 i «Sobreesforç/estirament» puja a 268**: hi ha
   **una recategorització** enmig. **El corpus no cita aquesta taula per sèrie**,
   només pels anys que no hi entren.
2. **Divisió 1478 (lloc del cos) té menys columnes que anys**: el bolcat en
   conserva les que la font dona i **no completa els forats**.
3. **El tram d'edat «de 16 a 24 anys» val 0 fins al 2013** i després
   **1, 10, 37, 53, 70, 128**… **Això no és una tendència: és que el tram no es
   codificava.** El corpus **no llegeix aquesta sèrie com un creixement.**
4. **Els accidents viaris per tipus canvien de codificació el 2019**: «Altres»
   cau de **489 a 280** i les categories concretes s'omplen de cop. **El total
   sí que és comparable; el desglossament, només del 2019 ençà.**

## Nota sobre el «lloc de l'accident»

**La divisió 1474 dona, cada any, gairebé el 100% dels accidents «en el lloc de
treball»** i **entre zero i un a «Altres»**. **La taula no distingeix els
accidents *in itinere***: o no es compten, o es compten com els altres. `La font
no ho explica.`
