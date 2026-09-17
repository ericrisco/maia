# `docs/raw/estadistica-xifres/` — Andorra en xifres

**Andorra en xifres 2024**, 127 pàgines, publicat el **9 de desembre del 2025**.
Edició del **Departament d'Estadística** amb la Cambra de Comerç i Andorra
Business. **Dipòsit legal AND.577-2025 · ISBN 978-99920-82-34-8.**

| | |
| --- | --- |
| **Font** | [Departament d'Estadística](https://www.estadistica.ad/) · Govern d'Andorra |
| **URL original** | `https://sig.govern.ad/SIGDDE.Public/Files/Documents/Publicacions/Andorra en Xifres. Any 2024.pdf` |
| **Titular** | Govern d'Andorra — el document porta «© Govern d'Andorra» |
| **Llicència** | **CC BY 4.0** per a la informació estadística pròpia segons l'avís legal del Departament, conservat a `../estadistica-poblacio/avis-legal-2026-09-13.txt` |
| **Redistribució** | **sí** per a les dades, amb atribució i data. **Les imatges no**: són cedides per tercers —Andorra Turisme, Servei Fotogràfic del Govern, Comú de Canillo, Andorran Banking, CASS— i queden fora |
| **Data de consulta** | 2026-09-17 |
| **Fitxa de font del corpus** | [`estadistica-ad`](../../fonts/estadistica-ad.md) |
| **`apte_dataset`** | **sí** per al text i les taules; **no** per a les imatges |

`andorra-en-xifres-2024.txt` és l'extracció local amb `pdftotext -layout`. El
volum del **2020** també és accessible a la mateixa carpeta del servidor; els
anys 2021, 2022, 2023 i 2025 tornen 404 amb aquest patró d'URL.

## Quines edicions hi ha, i què en falta

Sondejant el patró d'URL any per any: **2018, 2019, 2020 i 2024 responen 200**;
2009-2017, 2021, 2022, 2023 i 2025 responen **404**. La carpeta en conserva el
**2024** i el **2020**.

## `pib-serie-2000-2019-20.png` — una sèrie que només existeix com a gràfic

L'edició del 2020 publica l'**evolució de l'estimació del PIB nominal
(2000-2019)** exclusivament com a **gràfic de barres**. `pdftotext -layout` no en
recupera cap valor: només els eixos. Per llegir-la s'ha renderitzat la pàgina 20
amb `pdftoppm -f 20 -l 20 -r 200 -png` i s'han mesurat les vint barres en píxels.

**Calibratge.** L'escala s'ha ajustat per mínims quadrats contra els **quatre
anys que la mateixa edició publica en taula** (2016: 2.616,9 · 2017: 2.655,8 ·
2018: 2.725,3 · 2019: 2.818,4 milions d'euros). El pendent resultant és de
**10,58 milions d'euros per píxel** i el calibratge reprodueix els quatre
ancoratges amb un error màxim de **5 milions (0,2%)**.

**Xifres derivades** (arrodonides a la desena de milions; **no són dades
oficials**, són lectura de gràfic):

| Any | PIB nominal (M€) | | Any | PIB nominal (M€) |
| --- | --- | --- | --- | --- |
| 2000 | 1.640 | | 2010 | 2.610 |
| 2001 | 1.820 | | 2011 | 2.610 |
| 2002 | 1.930 | | 2012 | 2.510 |
| 2003 | 2.130 | | 2013 | **2.430** (mínim) |
| 2004 | 2.370 | | 2014 | 2.490 |
| 2005 | 2.550 | | 2015 | 2.530 |
| 2006 | 2.750 | | 2016 | 2.620 |
| 2007 | **2.880** (màxim) | | 2017 | 2.660 |
| 2008 | 2.770 | | 2018 | 2.730 |
| 2009 | 2.640 | | 2019 | 2.820 |

**Control independent.** Les variacions interanuals que se'n deriven (+11,0% el
2001, +4,6% el 2007, −3,7% el 2008, −5,0% el 2009, −4,0% el 2012, +3,1% el 2019)
coincideixen amb la **línia vermella de variació anual** dibuixada al mateix
gràfic, que es llegeix contra l'eix esquerre i que el corpus no ha fet servir per
calibrar. Les dues lectures són independents i donen el mateix relat.

**On s'usa**: [`temes/economia/transformacio-economica/andorra-2020.md`](../../temes/economia/transformacio-economica/andorra-2020.md).
