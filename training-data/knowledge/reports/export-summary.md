# Export de Maia Knowledge

Generat per `scripts/export_approved.py`. Cada línia dels JSONL conté una conversa amb `messages`; no hi ha camps interns.

- Converses aprovades exportades: **15**.
- Fitxes `docs/temes/` representades: **10**.
- Converses de revisió no exportables: **0**.

| Split | Converses |
|---|---:|
| `train` | 11 |
| `validation` | 3 |
| `test` | 1 |

## Fonts incloses

- `docs/temes/costums/danses/el-ball-de-lossa-dencamp.md` → `train`
- `docs/temes/costums/danses/la-marratxa.md` → `train`
- `docs/temes/costums/danses/les-festes-de-lossa.md` → `train`
- `docs/temes/cultura/cinc-anys-i-el-cinema-es-lunica-cosa-que-puja.md` → `validation`
- `docs/temes/cultura/llegendes/la-dama-blanca-daubinya.md` → `train`
- `docs/temes/economia/ramaderia-i-agricultura/qui-cobra-els-ajuts-agraris.md` → `train`
- `docs/temes/societat/educacio/lescola-andorrana-ha-passat-al-davant.md` → `train`
- `docs/temes/societat/habitatge/un-de-cada-tres-el-compra-una-societat.md` → `test`
- `docs/temes/societat/sanitat/de-que-es-mor-a-andorra.md` → `validation`
- `docs/temes/territori/geografia-fisica/de-que-esta-fet-el-pais.md` → `train`

Aquesta exportació és parcial. El recompte de fitxes representades no acredita cobertura exhaustiva del coneixement del corpus.
