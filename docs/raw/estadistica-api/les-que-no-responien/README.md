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

## Les dotze que segueixen sense respondre

**Aquestes no donen temps d'espera: donen un estat HTTP diferent de 200**, que
és el `502` que el corpus ja tenia documentat per a les divisions 402 i 411.

| idDivision | Taula |
| ---: | --- |
| 391, 402, 411 | Assalariats, massa salarial i salari mitjà **per sector i edat** |
| 778-783 | Assalariats, massa salarial i salari mitjà **per sexe**, i per sector i sexe |
| 246, 247 | Abonaments per servei i tràfic telefònic |
| 558 | Autoritzacions d'immigració d'hivern acordades per quota |

**Per a aquestes val la regla del corpus**: **retallar `showColumns` a un
període per any i, si encara falla, retallar el rang d'anys.** **No s'hi ha
aplicat en aquesta tanda.**

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
