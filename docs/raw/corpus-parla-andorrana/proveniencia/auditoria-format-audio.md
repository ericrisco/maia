# Auditoria de format d'àudio

Les **66 fonts** originals conserven el seu format d'origen: 2 a 16000 Hz/1 canals, 64 a 44100 Hz/2 canals. Els **656 clips d'audició** estan normalitzats a 656 a 16000 Hz/1 canals.

- Fonts amb encapçalament WAV vàlid: **66/66**.
- Clips d'audició en PCM mono 16 kHz: **656/656**.
- La normalització només afecta els clips derivats; els WAV font no es reescriuen.
- Aquest control valida el contenidor i el format, no la identitat de veu ni cap tret fonètic.

Font de dades: `auditoria-integritat-audio.tsv`.
