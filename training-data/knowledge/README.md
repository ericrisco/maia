# Maia Knowledge

Conjunt de converses sobre Andorra basades en `docs/temes/`. La unitat de treball és un dubte humà, no una secció ni un fet aïllat.

- [`review/`](review/): guia, pilot de calibratge, candidats actius i procedència.
- `work/`: inventari i estat de revisió per fitxa.
- `scripts/`: generació d'inventari i, més endavant, validació i exportació.
- `reports/`: cobertura, qualitat i exclusions.
- `output/`: només splits aprovats i elegibles per a l'ús previst.

El pilot anterior està arxivat i no compta com a cobertura. La producció nova comença amb un candidat sobre el Ball de l'Ossa d'Encamp; encara no hi ha exports aprovats. Per reconstruir l'inventari i el report, executa `python3 training-data/knowledge/scripts/build_document_inventory.py` des de l'arrel de `maia/`.

El format de cada registre és una conversa JSONL amb `messages` i només els rols `user` i `assistant`. La procedència i els drets van en un fitxer separat.
