# Scripts de Language

`build_language_inventory.py` escaneja `docs/parla/`, construeix la selecció per peça, extreu fragments literals, busca parelles de conversa que ja existeixen en la transcripció i registra permisos per vídeo. No genera cap pregunta ni reescriu cap torn humà.

Executa'l des de l'arrel de Maia:

```bash
PYTHONPATH=src python3 training-data/language/scripts/build_language_inventory.py
```

Les captures locals de YouTube serveixen per registrar la llicència del vídeo concret; no acrediten que la transcripció sigui correcta ni substitueixen el permís general de la font.
