# Maia Training Data

Àrea de treball per preparar dos conjunts de fine-tuning separats a partir de `docs/`:

- **Maia Knowledge** respon preguntes sobre Andorra amb informació documentada a `docs/temes/`.
- **Maia Language** conserva català andorrà contemporani de parlants reals a partir de `docs/parla/`.

No es barregen. Les converses de Knowledge han de partir de preguntes que una persona faria de debò. No es generen automàticament a partir de títols, seccions o files. Maia Language preserva material humà i no crea respostes fictícies.

```text
training-data/
├── PLAN.md
├── knowledge/
│   ├── review/       # calibratge, candidats, procedència i arxiu
│   ├── work/         # inventari i cobertura interna
│   ├── scripts/
│   ├── reports/
│   └── output/       # exports aprovats
└── language/
    ├── review/
    ├── work/
    ├── scripts/
    ├── reports/
    └── output/       # exports aprovats
```

El pilot anterior de Knowledge s'ha arxivat després de detectar preguntes que sonaven a extracció de fitxes. Ara s'està calibrant el nou criteri amb cinc exemples editorials. Aquests exemples no són registres d'entrenament; la cua activa és buida. L'inventari i la procedència anteriors es conserven per auditoria.

Consulta [`PLAN.md`](PLAN.md), la [guia de conversa](knowledge/review/CONVERSATION-GUIDE.md) i les [mostres de calibratge](knowledge/review/EXEMPLES.md).
