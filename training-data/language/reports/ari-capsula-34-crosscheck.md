# Comprovació de la transcripció — AR+I #34

- **Peça:** «Les falles d’Andorra», Albert Roig, 23:17.
- **Àudio de referència:** `docs/raw/parla/ari-capsula-34/source-audio.wav` (fitxer local aportat a l’espai de treball; no modificat).
- **Mètode:** comparació amb un segon reconeixement automàtic, `whisper.cpp` `large-v3-turbo-q5_0`, català. No s’ha fet una verificació humana escoltant cada fragment.
- **Resultat:** el segon reconeixement coincideix amb fragments clars de la transcripció existent, però no resol els tokens marcats com a incerts, com «Ves/Vesos». També inventa veu durant el silenci inicial («Fins demà!») i repeteix una frase moltes vegades durant el silenci final.
- **Decisió:** la transcripció continua **no verificada**. La coincidència entre dos reconeixements automàtics no és prova suficient per exportar text de parla. No s’ha creat cap registre de Language.
- **Pas pendent:** escoltar i contrastar manualment els fragments candidats; descartar els incerts i els silencis. Comprovar també la varietat del parlant per a aquesta peça, sense inferir-la només de la sèrie o del títol.
