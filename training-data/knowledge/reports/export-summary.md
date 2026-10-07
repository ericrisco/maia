# Export de Maia Knowledge

Generat per `scripts/export_approved.py`. Cada línia dels JSONL conté una conversa amb `messages`; no hi ha camps interns.

- Converses aprovades exportades: **5**.
- Fitxes `docs/temes/` representades: **4**.
- Converses de revisió no exportables: **0**.

| Split | Converses |
|---|---:|
| `train` | 2 |
| `validation` | 3 |
| `test` | 0 |

## Fonts incloses

- `docs/temes/cultura/cinc-anys-i-el-cinema-es-lunica-cosa-que-puja.md` → `validation`
- `docs/temes/economia/ramaderia-i-agricultura/qui-cobra-els-ajuts-agraris.md` → `train`
- `docs/temes/societat/educacio/lescola-andorrana-ha-passat-al-davant.md` → `train`
- `docs/temes/societat/sanitat/de-que-es-mor-a-andorra.md` → `validation`

Aquesta exportació és parcial. El recompte de fitxes representades no acredita cobertura exhaustiva del coneixement del corpus.
