# Export de Maia Knowledge

Generat per `scripts/export_approved.py`. Cada línia dels JSONL conté una conversa amb `messages`; no hi ha camps interns.

- Converses aprovades exportades: **36**.
- Fitxes `docs/temes/` representades: **17**.
- Converses de revisió no exportables: **0**.

| Split | Converses |
|---|---:|
| `train` | 23 |
| `validation` | 9 |
| `test` | 4 |

## Fonts incloses

- `docs/temes/costums/danses/el-ball-de-lossa-dencamp.md` → `validation`
- `docs/temes/costums/danses/la-marratxa.md` → `validation`
- `docs/temes/costums/danses/les-festes-de-lossa.md` → `validation`
- `docs/temes/costums/religiositat/el-registre-dentitats-religioses.md` → `train`
- `docs/temes/cultura/arquitectura/els-estripagecs.md` → `test`
- `docs/temes/cultura/arquitectura/sant-joan-de-caselles.md` → `test`
- `docs/temes/cultura/arquitectura/sant-marti-de-la-cortinada.md` → `test`
- `docs/temes/cultura/llegendes/el-minairo.md` → `validation`
- `docs/temes/cultura/llegendes/el-tamarro.md` → `test`
- `docs/temes/economia/banca-i-fiscalitat/a-andorra-si-que-hi-havia-impost.md` → `train`
- `docs/temes/gastronomia/plats/el-trinxat.md` → `train`
- `docs/temes/gastronomia/plats/lescudella-de-sant-antoni.md` → `validation`
- `docs/temes/institucions/comuns-i-parroquies/les-set-parroquies.md` → `train`
- `docs/temes/institucions/coprincipat/el-coprincipat.md` → `train`
- `docs/temes/persones/charles-romeu.md` → `train`
- `docs/temes/societat/demografia/dues-maneres-de-comptar-la-poblacio.md` → `train`
- `docs/temes/territori/clima-i-muntanya/el-clima.md` → `train`

Aquesta exportació és parcial. El recompte de fitxes representades no acredita cobertura exhaustiva del coneixement del corpus.
