# Procedència — candidat RTVA — DJ Neura

- **Font:** RTVA, *Freqüència Electrònica*, entrevista a DJ Neura (Julià Aláez Ortiz).
- **Pàgina:** https://www.rtva.ad/programes/entrevista-dj-neura
- **Actiu original:** URL directa conservada a `source-url.txt`; còpia local `audio-original.mp3`.
- **Àudio WAV:** `audio.wav`, 16 kHz, mono, PCM; SHA-256 `215137090848657e1aae31f5cf3ca144ffdd83e2358ac14905f11754403f91aa`.
- **MP3 original:** SHA-256 `02d0856611082534b956121557ce01db00e7b8391db07b0423c7fd9472df0502`.
- **ASR:** `asr/dj-neura.*` i `asr/dj-neura-base.*`, `whisper-cli`, llengua `ca`, beam 5, 8 fils.
- **Anàlisi:** `informe.md`, `formes.tsv`, `formes-consens.tsv` i `comparacio-asr.md`; cobreixen les 35 formes candidates de la matriu.
- **Clips d'audició:** `formes-clips.tsv`, `quadern-clips-formes.md`, 10 WAV representatius i `auditoria.html`.
- **Perfil acústic:** `analisi-acustica.tsv` i `analisi-acustica.md` amb durada, F0, energia, centroid i pauses; descriptors pendents d'audició.
- **Formants:** `formants.tsv` i `formants.md` amb F0/F1/F2/F3 dels 10 clips; mesures exploratòries pendents d'audició.
- **Veus provisionals:** `segments-speaker-provisional.tsv`, `segmentacio-veus.md` i `formes-dj-neura-provisional.tsv`; la heurística assigna 36 segments a `dj-neura-probable`, 21 a `entrevistador-probable` i deixa 85 indeterminats.
- **Tercera ASR:** `qa-greedy.tsv` i `informe-qa-greedy.md`; 10 clips reprocessats amb beam 1 (3 dobles, 2 d'un model i 5 sense coincidència).
- **Termes:** RTVA no declara una llicència oberta a la pàgina; els derivats es conserven per a recerca local i no es redistribueix l'original.

DJ Neura queda fora del recompte canònic fins a separar la seva veu de la persona entrevistadora i completar l'audició dels clips.
