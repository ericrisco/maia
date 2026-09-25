# Índex d’audició del corpus de parla andorrana

Aquesta és la porta d’entrada a la revisió humana. Les transcripcions, els descriptors acústics i les puntuacions ASR només prioritzen fragments; cap decisió lingüística entra al graf fins que s’escolta el WAV.

## Ordre recomanat

0. [Índex de persones](../persones/INDEX.md) — 66 fitxes de font, 60 persones canòniques i enllaç a cada informe.
1. [Resum per persona](resum-estat-audicio.md) — 60 persones canòniques i 686 clips totals.
2. [Sessions canòniques](auditoria-sessions-canoniques.html) — cua curta amb cobertura per persona; els manifests són sessio-01.tsv, sessio-02.tsv, sessio-03.tsv, sessio-04.tsv, sessio-05.tsv, sessio-06.tsv.
3. [Formes escasses](auditoria-formes-escasses.html) — 30 clips sobre 10 formes amb cobertura baixa.
   [Primera cua de formes escasses](cua-audicio-formes-escasses-prioritaria.md) — 10 clips, un per forma, per iniciar l'escolta.
4. [Cua de quarantena](auditoria-quarantena-20s.html) — 15 clips de pa-044, pa-047 i pa-050.
5. [Cua completa](auditoria-cua.html) — 656 intervals generals.
6. [Fonts pendents](fonts-pendents.tsv) — 4 pendents de permís, 11 candidats preanalitzats i 0 referències noves per recollir; no formen part del recompte canònic.

## Registres i guies

- [Registre general](registre-audicio.tsv) — camps humans de decisió, variant, fonètica, prosòdia i nota.
- [Registre de formes escasses](registre-audicio-formes-escasses.tsv) — separat del registre general.
- [Guia de formes escasses](guia-audicio-formes-escasses.tsv) — criteris d’escolta per forma.
- [Perfil acústic de formes escasses](analisi-acustica-formes-escasses.tsv) — descriptors instrumentals, sense anotació fonètica.
- [Auditoria de cobertura de formes](auditoria-cobertura-formes.tsv) — les 35 formes candidates.
- [Quadern de formes representatives](quadern-formes-representatives.md) — tres contextos ASR temporals per forma i enllaç a les fitxes, sempre pendents d'audició.
- [Quadern d'evidència gramatical](quadern-evidencia-gramatica.md) — 10.458 contextos de nou categories, amb exemples per persona i estat provisional.
- [Auditoria de cobertura per persona](auditoria-cobertura-sessions.tsv) — 60 persones canòniques.
- [Informe llegible de cobertura per font](auditoria-cobertura-persones.md) — 66 fitxes amb informe, 35 formes, àudio, transcripció i procedència.
- [Auditoria de format d'àudio](auditoria-format-audio.md) — 66 WAV font vàlids i 656 clips d'audició normalitzats a PCM mono 16 kHz.
- [Mapa de prospecció](mapa-prospeccio.md) — 66 fonts canòniques, 11 candidats separats i 4 referències bloquejades per permís.
- [Auditoria dels candidats separats](auditoria-candidats.md) — 11 expedients, 124 clips i 371 files de formes fora del cànon.
- [Integritat de transcripcions candidates](auditoria-integritat-transcripcions-candidats.tsv) — 124/124 clips amb WAV, ASR small i ASR base locals, hash d'àudio i estat de derivació.
- [Reproductor complet dels candidats](auditoria-candidats-completa.html) — 124 clips locals dels 11 expedients, amb exportació separada de decisions humanes.
- [Primera cua prioritària de candidats](cua-audicio-candidats-prioritaria.md) — 20 clips, una primera mostra de cadascuna de les 11 veus candidates; tots els camps humans comencen en `pendent`.
- [Reproductor de la cua prioritària](auditoria-cua-candidats-prioritaria.html) — anotació local amb exportació TSV; l'importador només escriu a la cua separada de candidats.
- [Graf de formes dels candidats](../grafo/README-formes-candidats.md) — capa textual independent: 100 nodes, 36 arestes i 24 formes; sense enllaç al graf canònic.
- [Graf canònic de formes escasses](../grafo/README-formes-escasses.md) — 60 nodes, 13 arestes i 10 formes amb cobertura baixa; semblança ASR pendent d'audició.

## Importació segura

Les exportacions HTML es validen amb la clau exacta `(persona, forma, clip)`. Els importadors simulen per defecte i només escriuen amb `--write`:

- `python3 importa-auditoria.py anotacions.tsv` per al registre general.
- `python3 importa-auditoria-formes-escasses.py anotacions-formes-escasses.tsv` per a la cua separada.
- `python3 importa-cua-audicio-candidats-prioritaria.py anotacions-cua-candidats-prioritaria.tsv` valida la cua candidata (afegeix `--write` només quan es vol actualitzar aquesta cua separada).

Les files continuen `pendent` fins que hi ha una decisió humana. Les veus en quarantena no entren al graf per aquesta via.

## Verificació

- `python3 verifica-corpus.py` comprova fitxers, hashes, independència, informes i registres.
- `python3 verifica-sessions-audicio.py` comprova els manifests i evita solapaments.
