# Export de Maia Knowledge

Generat per `scripts/export_approved.py`. Cada línia dels JSONL conté una conversa amb `messages`; no hi ha camps interns.

- Converses aprovades exportades: **18**.
- Fitxes `docs/temes/` representades: **4**.
- Converses de revisió no exportables: **0**.

| Split | Converses |
|---|---:|
| `train` | 16 |
| `validation` | 1 |
| `test` | 1 |

## Fonts incloses

- `docs/temes/costums/danses/la-marratxa.md` → `validation`
- `docs/temes/costums/religiositat/el-registre-dentitats-religioses.md` → `train`
- `docs/temes/cultura/arquitectura/els-estripagecs.md` → `test`
- `docs/temes/institucions/coprincipat/el-coprincipat.md` → `train`

Aquesta exportació és parcial. El recompte de fitxes representades no acredita cobertura exhaustiva del coneixement del corpus.
