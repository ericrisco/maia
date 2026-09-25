# Revisió — producció de tabac, 1973–2025

- **Unitat:** `docs/temes/economia/tabac/quant-tabac-es-cull-avui.md`
- **Hash revisat:** `a300fe05822306f09fce3da154302f4624d149baff2133dc26a5b4009621239a`
- **Decisió:** aprovada per a coneixement, amb abast limitat a Estadística.
- **Data:** 2026-09-25.
- **Revisió humana:** no; revisió assistida per model.

## Fonts, drets i evidència

La fitxa `02-DOCS/raw/sources/estadistica-ad.md` ja registrava titularitat i
condicions: la secció 6 de l'avís legal aplica CC BY 4.0 a la informació
estadística pròpia, amb atribució, tractament propi i data d'actualització quan
consti, sense suggerir patrocini. Abans de l'exportació s'hi han afegit les
peces exactes: nota A107, publicació NP_A107_20250721 (21-07-2025), i divisions
2404/2405 de la captura API del 18-09-2026. La nota A107, p. 5, prescriu citar
les dades del Departament d'Agricultura, Ministeri de Medi Ambient, Agricultura
i Ramaderia, tractades pel Departament d'Estadística. La procedència, llicència
i atribució de la captura també consten a `docs/raw/estadistica-api/resta-del-cataleg/README.md`.

Es llegiren les pàgines 1, 3, 4 i 5 de la nota; les pàgines 3–5 es renderitzaren
a `docs/raw/curacio/a107-review/` i es contrastaren visualment. La p. 3 conté
la taula parroquial i la discrepància entre el seu paràgraf i la taula. La p. 4
conté la descripció de l'evolució i el gràfic amb el rètol 1.047.036. La p. 5
conté la citació i metodologia. El bolcat de l'API s'ha comprovat fila per fila
per a totes les 53 observacions de 2404 i les 424 observacions de 2405.

## Resultats del contrast

- Divisió 2404: 53 valors anuals continus, 1973–2025; màxim capturat el 1997
  (1.047.038 kg), mínim el 2020 (106.799 kg). Recalculats −69,0% entre 1997 i
  2000, i +8,7% entre 2024 i 2025.
- Divisió 2405: vuit sèries anuals contínues (set parròquies i total), 1973–2025;
  424 valors. En set anys la suma de les parròquies difereix de la fila total:
  2013 (+1 kg), 2014 (−2), 2016 (+1), 2017 (+2), 2019 (+1), 2020 (+1) i 2024
  (+1). Les diferències s'han registrat sense ajustar dades.
- A107, p. 3: el paràgraf atribueix −28,6% a Sant Julià; la taula ho atribueix a
  Escaldes-Engordany i dona −1,9% a Sant Julià. No s'ha corregit l'original.
- A107, p. 4: el text parla del màxim de 1996 i 1997; el gràfic retola 1.047.036
  kg. La divisió 2404 dona 1.023.232 el 1996 i 1.047.038 el 1997. Les dues
  presentacions i els dos quilos de diferència es registren explícitament.
- S'han retirat les afirmacions sobre superfície, rendiment per hectàrea i
  suport/subvenció: depenien de fonts diferents, una d'elles amb redistribució
  no acreditada. També s'han retirat navegació `Related` i metacomentaris sobre
  el corpus. Les explicacions causals de l'A107 només es presenten com allò que
  la nota afirma, no com a efectes mesurats per la taula.

El fitxer aprovat acaba amb `Buits registrats`, enumera què no s'ha consultat i
no transforma l'absència de dades en una conclusió sobre el món. La decisió i
l'exportació conserven els hashes i localitzadors concrets.
