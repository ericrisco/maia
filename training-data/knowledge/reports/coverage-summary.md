# Cobertura de Maia Knowledge

Informe generat amb `scripts/build_coverage_inventory.py`.
La cobertura és per document citat i és només un límit inferior: una cita no prova que totes les seccions, files o afirmacions del document tinguin conversa.

## Inventari

- Fitxers Markdown a `docs/temes/`: **1477**.
- Fitxes factuals (`type: article`): **1348**.
- Índexs (`type: index`): **129**; s'usen per navegar, no com a font factual autònoma.
- Seccions: **11884**.
- Files de taula incloent capçaleres: **19056**.
- Elements de llista: **14348**.
- Enllaços Markdown: **17005**.

## Cobertura citada per tema principal

| Tema | Fitxes article | Amb conversa citada | Sense conversa citada |
|---|---:|---:|---:|
| `costums` | 23 | 3 | 20 |
| `cultura` | 72 | 2 | 70 |
| `economia` | 95 | 0 | 95 |
| `esports` | 272 | 0 | 272 |
| `gastronomia` | 15 | 0 | 15 |
| `historia` | 226 | 0 | 226 |
| `institucions` | 338 | 1 | 337 |
| `llengua` | 43 | 0 | 43 |
| `persones` | 43 | 0 | 43 |
| `politica` | 19 | 0 | 19 |
| `societat` | 142 | 0 | 142 |
| `territori` | 49 | 0 | 49 |
| `vida-quotidiana` | 11 | 0 | 11 |

**Total:** 1348 fitxes article; **6** tenen almenys una conversa citada i **1342** encara no en tenen.

## Límits

- La cobertura citada només indica que una conversa apunta a la fitxa. No acredita cobertura de cada secció, taula, fila, llista, data o excepció.
- Els registres de revisió poden tenir drets pendents i no són exports d'entrenament.
- La font de veritat és el corpus actual; torneu a generar aquest informe després de canvis a `docs/temes/` o als registres de procedència.
