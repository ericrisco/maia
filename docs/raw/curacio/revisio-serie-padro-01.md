# Revisió: sèrie de població registrada i demografia vital

- **Data:** 25-09-2026.
- **Unitat inicial:** `docs/temes/societat/demografia/setanta-nou-anys-de-padro.md`.
- **Decisió:** aprovada després de reescriure l'abast; exportada a `final-corpus/coneixement/societat/demografia/la-poblacio-registrada-i-el-canvi-natural-1947-2025.md`.
- **Revisió:** assistida per model; no hi ha hagut revisió humana.

## Dades i procedència

S'han verificat els valors a la captura datada de l'API pública del Departament d'Estadística (`docs/raw/estadistica-api/`, baixada el 18-09-2026): divisió 1 (població registrada), 22 (naixements), 28 (defuncions), 797 (població total) i 1261 (saldo migratori publicat). La llicència declarada és CC BY 4.0 amb atribució; les condicions i l'abast dels bolcats consten a les fitxes de l'API, `resta-del-cataleg/README.md`, `poblacio/poblacio-per-l-api-d-estadistica.md` i `demografia-vital/demografia-vital-per-l-api-d-estadistica.md`.

## Resultats de la verificació

- La divisió 1 conté els 79 valors anuals de 1947 a 2025. El valor passa de 5.385 a 94.128 (×17,5). Els deu canvis interanuals negatius es troben en cinc trams: 1952–1954, 1994–1995, 2000, 2009 i 2011–2013.
- La baixada de 1952–1954 compara 6.310 el 1951 amb 5.503 el 1954; per això s'ha corregit la cronologia inicial i s'ha tret «en dos anys». També s'han afegit els descensos aïllats de 2000 (65.971→65.844) i 2009 (84.484→84.082), que el recompte original ometia.
- La caiguda interanual més gran és la de 2011: 85.015 el 2010 i 78.115 el 2011 (−6.900; −8,1%). La font no n'indica la causa. S'ha retirat la hipòtesi que la caiguda sigui més compatible amb una depuració que amb un canvi de població.
- Les divisions 22 i 28 tenen valors anuals de 1953 a 2025. S'han recomptat els saldos naturals per any i període: 2008 és el màxim anual (+638); el de 2025 és +122; l'acumulat 2020–2025 és +719. S'ha retirat el títol «El creixement vegetatiu s'acaba», que contradeia aquests saldos positius.
- La divisió 28 té el màxim anual de defuncions el 2020 (419), però la sèrie no n'indica la causa. El text ja no l'atribueix a la pandèmia.
- La divisió 1261 publica saldo migratori només per a 2016–2025; tots deu valors són positius i el màxim és 3.407 el 2023. S'ha tret l'afirmació que el saldo s'hagi girat el 2014, perquè la sèrie oficial consultada no cobreix els anys anteriors a 2016.
- El càlcul migratori anterior, que restava el canvi natural al canvi de la divisió 797, no coincideix sempre amb la divisió 1261: per exemple, 2016 dona 1.049 al càlcul anterior i 1.149 a la sèrie publicada; el 2023, 3.412 i 3.407. S'ha retirat tota la sèrie inferida en lloc d'atribuir una explicació a la diferència.
- S'ha conservat la distinció de la font entre població registrada (divisió 1) i població total (divisió 797): el 2025, 94.128 davant de 89.058. Cap de les dues s'utilitza per explicar l'altra.

## Abast de l'exportació

La versió exportada conté la sèrie registrada, els recomptes de naixements i defuncions, el canvi natural calculat i el saldo migratori publicat. S'han tret seccions tangencials sobre taxa de natalitat, nacionalitat/edat/parròquia/estat civil de la mare, mortalitat per edat i saldo per sexe; les seves afirmacions no formen part d'aquesta decisió ni es promouen automàticament a unitats aprovades. S'han eliminat també explicacions de causes i connexions amb altres temes que les taules no demostren.
