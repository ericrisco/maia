# Comprovació automàtica de la transcripció — AR+I #66

- **Peça:** «La dansa tradicional d’Andorra: el contrapàs», Teo Armengol, 16:44.
- **Llicència de la peça:** YouTube declara Creative Commons Attribution (reuse allowed) a les metadades capturades el 2026-10-09. La llicència no valida la transcripció ni l’origen lingüístic del parlant.
- **Àudio de referència:** `docs/raw/parla/ari-capsula-66/source-audio.webm`, SHA-256 `1e173932a8e22f94f7c3beb511141251b0c09e276b2f4c1379fbdd79b62cea75`. Durada detectada: 1004,281 s.
- **Conversió per a ASR:** `docs/raw/parla/ari-capsula-66/verification/source-audio-16k-mono.wav`, SHA-256 `8948c0c7396934a1b65f29fba253c1a631cbfe75798cb4ea4c6a322f72c934cc`; coincideix amb el hash 16 kHz mono ja anotat al material de partida.
- **Mètode:** segon reconeixement amb `whisper.cpp` 1.9.1, model `large-v3-turbo-q5_0`, idioma català. Sortida SRT: `docs/raw/parla/ari-capsula-66/verification/whisper-large-v3-turbo.srt`.
- **Comparació:** la transcripció existent té 207 segments i 197 marques d’incertesa. El segon ASR en produeix 713. Una comparació automàtica per intervals d’un minut, ignorant majúscules, puntuació i tokens marcats com a incerts, dona semblances textuals entre 0,83 i 0,97. **No són taxes d’encert ni un WER**: només localitzen trams que convé escoltar.
- **Discrepàncies candidates:** la transcripció existent comença a 00:00:13.790, mentre el segon ASR situa «Un poble és el que són les seves tradicions» des de 00:00:00; cap al minut 3, el text existent deixa `[?m'he] [?entrat]` incert i el segon ASR proposa «m'he enterat». El segon ASR també llegeix sense marca «confrari» i «ex-dansaire», que la transcripció existent marca com a incerts. Cap d’aquestes propostes queda confirmada sense escolta humana.
- **Decisió:** la transcripció continua **no verificada**. La coincidència entre dos reconeixements automàtics no és una comprovació humana. No s’ha creat cap registre de sortida de Language.
- **Pas pendent:** escoltar els trams discrepants i les paraules marcades, revisar fidelitat de tota la transcripció i confirmar separadament la varietat lingüística del parlant.
