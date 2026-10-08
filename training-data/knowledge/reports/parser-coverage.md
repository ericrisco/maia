# Cobertura del parser de Knowledge

Generat recorrent docs/temes/ amb scripts/parse_corpus.py. El parser conserva els blocs Markdown en ordre i les metadades del frontmatter; no crea preguntes ni divideix per longitud.

| Mesura | Resultat |
|---|---:|
| Documents processats | 1477 |
| Errors | 0 |
| Títols i seccions | 12224 |
| Taules | 3141 |
| Files de taules | 16311 |
| Enllaços Markdown | 18668 |
| Blocs semàntics | 46901 |

## Errors

Cap error de lectura o parseig.

Els marcadors partial, unknown, divergence, resolved i uncertain són pistes lèxiques. El text es conserva íntegre i aquests marcadors no substitueixen la revisió editorial.
