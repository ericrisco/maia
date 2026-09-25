# Revisió: edat, sexe i nacionalitat de la població

- **Data:** 25-09-2026.
- **Unitat inicial:** `docs/temes/societat/demografia/la-mateixa-gent-quinze-anys-mes-gran.md`.
- **Decisió final:** aprovada amb reescriptura per a `final-corpus/coneixement/societat/demografia/edat-i-nacionalitat-de-la-poblacio-d-andorra-2010-2025.md`.
- **Revisió:** assistida per model; no hi ha hagut revisió humana.

## Fonts, termes i càlculs

S'ha contrastat el text amb `docs/raw/estadistica-api/resta-del-cataleg/resta-cataleg-api-2026-09-18.tsv`, captura de l'API pública del Departament d'Estadística baixada el 18-09-2026. La font documenta CC BY 4.0 per a dades estadístiques pròpies amb atribució a `docs/raw/estadistica-api/l-api-publica-del-departament-d-estadistica.md`; s'ha afegit una fitxa específica del bolcat i s'ha ampliat `docs/fonts/estadistica-ad.md` abans d'exportar-lo.

S'han validat amb càlculs sobre el TSV:

- **Divisió 1100**, població per edat en trams d'un any: màxims modals i recomptes de 2010, 2015, 2020 i 2025; totals; els sis grups d'edat de 2010 i 2025; els recomptes de zero i un any; i les quatre taxes de dependència calculades amb la fórmula indicada.
- **Divisió 1098**, població per sexe i edat en trams quinquennals: totals de 2025 i sumes dels grups 0–14, 25–39, 40–54, 65–79 i 80 o més.
- **Divisió 1099**, població per edat quinquennal i nacionalitat: totes les cel·les incloses a la taula reescrita i els extrems del percentatge d'andorrans, recomputats contra les cinc categories de cada grup.

Les comprovacions programàtiques sobre les tres divisions han acabat correctament. La captura és datada; el resultat no es presenta com una consulta actualitzada ni com un seguiment de persones.

## Correccions editorials i factuals

- S'han retirat les explicacions que atribuïen l'augment de la cohort modal a l'arribada de gent de fora, la composició per sexe a immigració/esperança de vida, i el canvi de taxa de dependència a persones arribades de fora. Les taules no mesuren aquestes causes.
- S'ha tret l'afirmació que els nombres de dos períodes són necessàriament les mateixes persones i la projecció retòrica sobre qui hi haurà el 2035.
- S'han conservat com a recompte descriptiu les diferències per sexe i nacionalitat. «Nacionalitat» no s'ha convertit en passaport, origen, lloc de naixement ni via d'adquisició.
- El text antic afirmava que no hi havia categoria de 100 anys o més. El localitzador `idDivision=1100`, codi `0101010100060100`, etiqueta exacta `DE 99 ANYS O MÉS`, ho desmenteix. La nota de límit ara diu que el grup és obert i que no permet separar 99 anys de 100 o més.
- Les comparacions selectives s'identifiquen com a tals; s'han eliminat anotacions de construcció de la wiki i navegació entre articles.

## Abast i límits

L'aprovació cobreix l'exactitud aritmètica de les afirmacions conservades respecte de les tres divisions de la captura i la seva redacció no causal. No valida una definició demogràfica externa de cada categoria ni permet seguir persones, identificar fluxos migratoris, deduir el lloc de naixement o predir la composició futura. El triatge preliminar `demografia-edat-nacionalitat-pending-01.md` registra per què la unitat va quedar fora de l'exportació abans de completar aquesta revisió.
