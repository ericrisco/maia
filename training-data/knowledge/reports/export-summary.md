# Export de Maia Knowledge

Generat per `scripts/export_approved.py`. Cada línia dels JSONL conté una conversa amb `messages`; no hi ha camps interns.

- Converses aprovades exportades: **30**.
- Fitxes `docs/temes/` representades: **19**.
- Converses de revisió no exportables: **0**.

| Split | Converses |
|---|---:|
| `train` | 26 |
| `validation` | 3 |
| `test` | 1 |

## Fonts incloses

- `docs/temes/costums/danses/el-ball-de-lossa-dencamp.md` → `train`
- `docs/temes/costums/danses/la-marratxa.md` → `train`
- `docs/temes/costums/danses/les-festes-de-lossa.md` → `train`
- `docs/temes/cultura/cinc-anys-i-el-cinema-es-lunica-cosa-que-puja.md` → `validation`
- `docs/temes/cultura/llegendes/la-dama-blanca-daubinya.md` → `train`
- `docs/temes/economia/banca-i-fiscalitat/a-andorra-si-que-hi-havia-impost.md` → `train`
- `docs/temes/economia/comerc/les-mateixes-besties-passaven-dues-vegades-pel-cens.md` → `train`
- `docs/temes/economia/ramaderia-i-agricultura/qui-cobra-els-ajuts-agraris.md` → `train`
- `docs/temes/historia/antic-regim/el-rei-es-sobira-pero-no-ho-es-tot-sol.md` → `train`
- `docs/temes/institucions/consell-general/si-els-dos-senyors-no-sentenien-decidia-el-poble.md` → `train`
- `docs/temes/societat/demografia/dues-maneres-de-comptar-la-poblacio.md` → `train`
- `docs/temes/societat/demografia/setanta-nou-anys-de-padro.md` → `train`
- `docs/temes/societat/educacio/lescola-andorrana-ha-passat-al-davant.md` → `train`
- `docs/temes/societat/habitatge/dos-tercos-del-pais-viuen-de-lloguer.md` → `train`
- `docs/temes/societat/habitatge/un-de-cada-tres-el-compra-una-societat.md` → `test`
- `docs/temes/societat/proteccio-social/el-gini-ha-pujat-vuit-punts.md` → `train`
- `docs/temes/societat/sanitat/de-que-es-mor-a-andorra.md` → `validation`
- `docs/temes/territori/clima-i-muntanya/que-es-va-mesurar-a-lallau-darinsal.md` → `train`
- `docs/temes/territori/geografia-fisica/de-que-esta-fet-el-pais.md` → `train`

Aquesta exportació és parcial. El recompte de fitxes representades no acredita cobertura exhaustiva del coneixement del corpus.
