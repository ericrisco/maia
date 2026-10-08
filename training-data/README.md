# Maia Training Data

Aquest espai prepara dos datasets separats a partir del corpus de Maia:

- **Maia Knowledge**: converses per respondre preguntes sobre Andorra, a partir de `docs/temes/`.
- **Maia Language**: senyal lingüístic humà contemporani, a partir de `docs/parla/`; no s'hi inventen veus ni respostes.

## Estat actual

Hem reiniciat la calibració perquè les preguntes anteriors sonaven com consultes sobre fitxes i taules. `knowledge/examples/` conté quatre converses noves per revisar naturalitat i seguiments. Són exemples editorials, no exports d'entrenament. No hi ha fitxers finals ni particions train/validation/test.

Les fonts, drets i notes de revisió van en fitxers separats dels missatges. Una font amb drets pendents no es pot exportar.

## Mapa

- `PLAN.md`: criteris de conversa i fases del projecte.
- `scripts/`: lector i inventari del corpus.
- `knowledge/examples/`: converses de calibració i procedència.
- `knowledge/review/`: converses candidates, criteris editorials i procedència abans d'aprovació.
- `knowledge/work/`: cobertura i estat de revisió de les fitxes.
- `knowledge/output/`: reservat per als exports aprovats.
- `language/work/`: inventari i estat d'elegibilitat de les peces de parla.
- `language/output/`: reservat per als fragments elegibles i els splits.

Knowledge i Language no es barregen. Vegeu els README de cada àrea i el [pla de conversa](PLAN.md) abans d'afegir registres.
