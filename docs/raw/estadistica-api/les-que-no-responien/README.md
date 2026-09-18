# Les divisions que semblava que l'API no servia

**Baixat el 18-09-2026**, **després de descobrir que el problema no era el
servidor sinó el temps d'espera del client.**

## Què va passar

**El bolcat general del catàleg va donar setze divisions per KO**, totes amb
`TimeoutError` repetit. **El client d'`estadistica_api.py` té el temps d'espera
per defecte a 60 segons.**

**Provades de nou amb 900 segons, quatre responen**:

| idDivision | Taula | Temps | Valors |
| ---: | --- | ---: | ---: |
| **70** | Exportacions per països, en valor | **86 s** | 81.335 |
| 71 | Exportacions per països, en quantitat | — | 81.335 |
| **76** | Importacions per països, en valor | **110 s** | 92.516 |
| 77 | Importacions per països, en quantitat | — | 92.516 |

**347.702 valors**, **229 països a cada taula**, **1993-2026**.

## Les dotze que donaven `500`/`502`, i la regla de retall aplicada

**Aquestes no donen temps d'espera: donen un estat HTTP diferent de 200.**
**El 18-09-2026 s'hi ha aplicat la regla del corpus** —**retallar `showColumns`
a un període per any i, si encara falla, retallar el rang d'anys a 1990, 2000 i
2010**— i **set de les dotze responen.**

**Fitxer: `divisions-retallades-2026-09-18.tsv` · 10.930 valors · només
desembres.**

| idDivision | Taula | Resultat |
| ---: | --- | --- |
| **778** | Nombre d'assalariats per sexe | **OK, 60 desembres (1966-2023)** |
| **779** | Nombre d'assalariats per sector i sexe | **OK, 60 desembres** |
| **780** | Massa salarial per sexe | **OK, 60 desembres** |
| **781** | Massa salarial per sector i sexe | **OK, 60 desembres** |
| **782** | Salari mitjà per sexe | **OK, 58 desembres** |
| **783** | Salari mitjà per sector i sexe | **OK, 60 desembres** |
| **558** | Autoritzacions d'immigració d'hivern per quota | **OK, 67 desembres** |
| 391 | Assalariats per sector i edat | `500` sencera, `502` retallada |
| 402 | Massa salarial per sector i edat | `500` sencera, `502` retallada |
| 411 | Salari mitjà per sector i edat | `500` sencera, `502` retallada |
| 246 | Abonaments per servei | `500` a totes les variants |
| 247 | Tràfic telefònic | `500` a totes les variants |

**Cinc divisions de 2.709 queden fora de l'abast del corpus.** **Les tres del
creuament sector × edat i les dues de telefonia**, i **per a aquestes la regla
de retall no serveix**: retallar als desembres no baixa el `500` de les 246 i
247, i converteix el `500` de les 391, 402 i 411 en `502` sense arribar mai a
un 200.

## Defecte provat a la divisió 779 (i a la 783)

**La columna de les dones està desplaçada una fila**: cada valor porta
l'etiqueta del sector següent. **Provat per suma**: els divuit sectors dels
homes sumen 24.409 contra un total publicat de 24.410, i **els de les dones
sumen 22.463 contra 22.595**; **els 132 que falten són el primer valor de la
columna «sexe indeterminat»**, i **desplaçant la columna una fila la suma és
exacta.** Destil·lat a
[`vuitanta-cinc-coma-nou.md`](../../../temes/societat/dones/vuitanta-cinc-coma-nou.md).

**No feu servir les etiquetes de sector de la columna femenina sense
corregir-les.**

## Font i drets

- **Departament d'Estadística del Govern d'Andorra**,
  `https://sig.govern.ad/SIGDDE.Public/estadistiquesdades/api/`.
- **Llicència: CC BY 4.0.** Fitxa de font: `docs/fonts/estadistica-ad.md`.

## Columnes

`idDivision · taula · codi · serie · periode · valor` — valors normalitzats.
**El nom del país és dins de la columna `serie`**, amb el codi numèric al final
(`EXPORTACIONS EN VALOR. DESTÍ A ESPANYA. CODI 724`).

## Advertències d'ús

- **Les exportacions valen zero del 1993 al 1996**: **la sèrie d'exportacions
  comença el 1997**, la d'importacions el 1993.
- **El darrer any és parcial.** **Compteu els mesos abans de sumar-los.**
- **Les taules «en quantitat» i «en valor» no tenen la mateixa unitat** i no es
  poden dividir l'una per l'altra sense saber quina és la de quantitat, que la
  font no declara.
