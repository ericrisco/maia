# Maia Language

Flux separat per preservar català andorrà contemporani produït per persones a
`docs/parla/`. Només s'hi incorporarà material elegible amb drets i fiabilitat
de transcripció revisats. No s'hi generaran respostes artificials.

## Inventari i estat actual

Genera l'inventari de peces i comprova les metadades i les fonts amb:

```bash
python3 training-data/language/scripts/build_language_inventory.py --check
```

L'informe és a `reports/eligibility-status.md`; l'inventari detallat, a
`work/source-inventory.json`. Aquests fitxers no copien les transcripcions ni
aproven automàticament cap fragment.

En la revisió del 7 d'octubre de 2026 hi ha 40 peces amb `type: parla`. Cap no
està llesta per exportar: 27 entrevistes del Consell General tenen drets de
redistribució pendents; 8 peces d'AR+I necessiten comprovació de llicència per
vídeo; i 3 peces d'AR+I tenen llicència CC BY identificada per peça, però la
transcripció continua sense verificar contra l'àudio. Dues peces no estan
marcades com a mostra de llengua. El consentiment i la llicència de
redistribució es revisen per separat.
