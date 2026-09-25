---
type: article
title: Edat i nacionalitat de la població d'Andorra (2010–2025)
description: "Les taules oficials mostren com canvia la població per edat, sexe i nacionalitat entre 2010 i 2025; són fotografies agregades, no un seguiment de persones."
tema: temes/societat/demografia
veu: compilada
epoca: contemporania
apte_llengua: false
font: estadistica-ad
timestamp: 2026-09-25T03:40:00Z
tags: [demografia, societat, poblacio, estadistica, envelliment]
---

# Edat i nacionalitat de la població d'Andorra (2010–2025)

El Departament d'Estadística publica taules de població per edat, sexe i
nacionalitat. La captura consultada, baixada el 18-09-2026, cobreix els anys
2010–2025. Aquesta lectura es basa en tres sèries de l'API pública: divisió
1100, edat any per any; divisió 1098, sexe i edat en trams de cinc anys; i
divisió 1099, nacionalitat i edat en trams de cinc anys. La fitxa de
procedència `docs/raw/estadistica-api/resta-del-cataleg/README.md` descriu la
captura i les limitacions de cada sèrie.

## Canvis en l'estructura per edat

La franja d'edat amb el nombre més alt de persones passa de 38 anys el 2010 a
53 anys el 2025. Aquests són els màxims de cada fotografia anual seleccionada;
les taules no segueixen les mateixes persones al llarg del temps.

| Any | Edat amb el valor més alt | Persones en aquella edat |
| --- | ---: | ---: |
| 2010 | 38 | 1.470 |
| 2015 | 43 | 1.433 |
| 2020 | 48 | 1.546 |
| 2025 | 53 | 1.635 |

El nombre registrat per a l'edat modal de cada període augmenta un 11,2% entre
2010 i 2025 (de 1.470 a 1.635). Les dades agregades no permeten determinar si
el canvi prové de migracions, canvis de residència, revisions del registre o
d'altres factors.

| Edats | 2010 | 2025 | Variació |
| --- | ---: | ---: | ---: |
| 0–14 | 11.508 | 9.589 | −16,7% |
| 15–24 | 7.438 | 9.386 | +26,2% |
| 25–39 | 18.841 | 19.864 | +5,4% |
| 40–54 | 18.055 | 22.633 | +25,4% |
| 55–64 | 6.977 | 13.481 | +93,2% |
| 65 o més | 7.471 | 14.105 | +88,8% |
| **Total** | **70.290** | **89.058** | **+26,7%** |

Entre 2010 i 2025, el total augmenta en 18.768 persones i el grup de 0–14
anys disminueix en 1.919. Dels sis trams de la taula, aquest és l'únic que
baixa. El grup de 55–64 anys gairebé es dobla; el de 65 anys o més també
augmenta, un 88,8%.

La taula per edat d'un any registra 632 persones de zero anys el 2010 i 346 el
2025 (−45,3%). Per a un any d'edat, els valors són 694 i 434, respectivament.

La taxa de dependència següent es calcula com la població de 0–14 anys més la
de 65 anys o més, dividida per la població de 15–64 anys. Els percentatges són
resultats d'aquest càlcul sobre la divisió 1100; no indiquen per si sols
ocupació, activitat laboral ni dependència econòmica.

| Any | Taxa calculada |
| --- | ---: |
| 2010 | 37,0% |
| 2015 | 39,1% |
| 2020 | 38,2% |
| 2025 | 36,2% |

La taxa calculada és més baixa el 2025 que el 2010. La caiguda del grup de
menors de 15 anys i l'augment del grup de 15–64 intervenen en el resultat; la
taula no n'identifica les causes.

## Distribució per sexe en trams d'edat seleccionats

La divisió 1098 publica les categories «HOME» i «DONA» per a cada grup
quinquennal. El 2025, les sumes de les categories són 46.282 i 42.776,
respectivament. La relació agregada és d'1,082 homes per dona. Alguns trams:

| Tram d'edat | Homes | Dones | Homes per cada 100 dones |
| --- | ---: | ---: | ---: |
| 0–14 | 4.832 | 4.757 | 102 |
| 25–39 | 10.745 | 9.119 | 118 |
| 40–54 | 11.743 | 10.890 | 108 |
| 65–79 | 5.413 | 5.251 | 103 |
| 80 o més | 1.469 | 1.972 | 75 |

Les diferències entre aquests grups són descriptives. Aquesta taula no
identifica migració ni explica diferències d'esperança de vida.

## Nacionalitat registrada en alguns grups d'edat

La divisió 1099 agrupa la nacionalitat en cinc categories. La taula mostra
quatre trams seleccionats de 2025; els percentatges d'andorrans s'han calculat
com el nombre de la categoria «ANDORRANA» dividit pel total de les cinc
categories del mateix tram.

| Edat | Andorrana | Espanyola | Portuguesa | Francesa | Altres | % andorrana |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 0–4 | 1.929 | 200 | 11 | 45 | 148 | 82,7% |
| 40–44 | 2.219 | 1.546 | 1.012 | 305 | 1.959 | 31,5% |
| 50–54 | 3.082 | 2.035 | 1.143 | 420 | 1.226 | 39,0% |
| 85 o més | 713 | 731 | 27 | 94 | 143 | 41,7% |

En els grups quinquennals de la sèrie, el percentatge andorrà és més baix a
40–44 anys (31,5%) i més alt a 0–4 anys (82,7%). Entre 50–54 anys la taula
registra 1.143 persones de nacionalitat portuguesa; entre 0–4 anys, 11. Són
recomptes de nacionalitat per tram, no dades sobre lloc de naixement,
ascendència o adquisició de nacionalitat.

## Buits registrats i límits de les sèries

- Les dades són distribucions agregades per període; no identifiquen persones
  ni constitueixen un seguiment longitudinal. No permeten dir que les persones
  del grup modal en dos anys diferents siguin les mateixes.
- La divisió 1100 arriba fins a «99 anys o més». Les persones de 99, 100 o més
  anys no es poden separar dins d'aquesta categoria.
- La divisió 1098 té una categoria oberta de «85 anys o més»; per això no
  informa separadament les edats superiors.
- Les taules no informen el lloc de naixement, el moment d'arribada al país,
  la via d'adquisició de nacionalitat ni les causes dels canvis observats.
- Les dades de 2025 descriuen aquell període i aquesta captura, no una
  projecció per al 2035 ni la població actual en una data posterior.
- Les categories de sexe i nacionalitat es reprodueixen segons les etiquetes
  de la font; aquesta fitxa no n'amplia les definicions.
