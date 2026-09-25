# Revisió: població dels 44 pobles

- **Data:** 25-09-2026.
- **Unitat inicial:** `docs/temes/societat/demografia/quaranta-quatre-pobles.md`.
- **Decisió:** aprovada per a `final-corpus/coneixement/societat/demografia/la-poblacio-dels-44-pobles-d-andorra-2010-2025.md`.
- **Abast:** verificació de dades, càlculs, redacció, límits inferencials i permís de redistribució. No és una revisió humana.

## Fonts i permís

La unitat usa la captura `docs/raw/estadistica-api/poblacio/poblacio-api-2026-09-18.tsv`, baixada el 18-09-2026, i la seva fitxa de procedència. La fitxa de font del Departament d'Estadística registra CC BY 4.0 per a la informació estadística pròpia i redistribució amb atribució; la fitxa específica documenta les divisions 797 i 1096, el període i els defectes coneguts. S'ha actualitzat l'abast de `docs/fonts/estadistica-ad.md` perquè inclogui l'API i exigeixi procedència per captura.

## Comprovacions i canvis

- Les 44 sèries de la divisió 1096 tenen valors tant el 2010 com el 2025. El total de 70.290 a 89.058 prové de la divisió 797.
- Es van contrastar els vuit valors més baixos el 2025; els valors i les parròquies coincideixen amb el TSV.
- El rànquing original s'anomenava «els que més creixen», però ometia Llumeneres (1→4) i els Plans (10→40), els multiplicadors més alts del conjunt. També deia que sis de vuit eren de Canillo o Ordino quan n'eren set. S'ha substituït per un rànquing explícit dels vuit multiplicadors més alts entre sèries amb almenys 100 habitants el 2010: Tarter, Incles, Serrat, Ransol, Soldeu, Erts, Llorts i Sornàs. Amb aquest llindar, set són de Canillo o Ordino.
- El Tarter i Soldeu sumen 873 habitants el 2010 i 2.242 el 2025; s'ha retirat la interpretació causal sobre esquí/Grandvalira.
- S'han comprovat Pas de la Casa, Sispony, Andorra la Vella (nucli) i totes les sumes parroquials enfront de les sèries del TSV. Els multiplicadors i percentatges publicats concorden amb els valors arrodonits.
- S'ha retirat l'afirmació que el creixement de Canillo és el doble que qualsevol altra parròquia: la segona variació relativa és ×1,41, no la meitat de ×2,04.
- S'han eliminat referències editorials no sostingudes pel conjunt, anotacions de treball antigues i la possible confusió entre les 44 entrades publicades i tots els nuclis habitats. El text deixa explícit que el conjunt no explica causes i conserva el defecte d'etiquetatge de Sant Julià.

## Límits

La decisió aprova la reproducció i l'exactitud de les afirmacions incloses respecte de la captura datada; no converteix aquesta captura en dades actuals, no valida la metodologia del padró i no resol els criteris amb què el Departament defineix «poble». L'article identifica la sèrie com a població registrada, no estimada.
