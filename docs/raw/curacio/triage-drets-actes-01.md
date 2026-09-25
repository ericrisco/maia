# Triage d'elegibilitat: actes històriques del Consell

- Tanda: `triage-rights-actes-01`
- Data: 2026-09-24
- Unitats inicials classificades: 160 articles (133 d'institucions i 27 d'història)
- Decisió: `pending`; cap unitat aprovada ni exportada en aquesta tanda.
- Motiu comú verificat: totes les unitats declaren `font: actes-historiques-consell-general`. La fitxa `docs/fonts/actes-historiques-consell-general.md` marca `redistribucio: pendent`; diu que als llibres d'actes i documents precedents no hi consta nota de drets, mentre que la síntesi de 2024 prohibeix expressament la reproducció. Aquests dos règims no s'han de confondre.
- Mètode: per a cada fitxer, hash actual confrontat amb inventari congelat i font declarada confrontada amb el frontmatter; aplicat el bloqueig de drets com a porta d'elegibilitat.
- Límit: aquesta tanda no ha revisat les afirmacions dels 160 articles contra els originals. Les decisions són pendents per drets, no una aprovació factual ni una conclusió que l'ús sigui prohibit. Per reobrir-les cal aclarir els drets de les transcripcions primàries; després cal revisar contingut, cites, buits i duplicats abans d'aprovar cap unitat.
- Evidència per unitat: ledger `decisions.jsonl`, camp `batch_id=triage-rights-actes-01`, amb hash d'entrada, article, font i mètode registrats.

## Comprovacions

- `python scripts/curacio_corpus.py --write` i `--check`: passen; 25.585 unitats, amb 1.217 sense revisar, 173 pendents, una aprovada i 24.194 excloses. Les 160 d'aquesta tanda consten dins les pendents.
- `python scripts/curacio_corpus.py --self-test` i `python scripts/build_final_manifest.py --self-test`: passen; decisions vàlides acceptades i casos invàlids rebutjats.
- `python scripts/export_final_corpus.py --check` i `python scripts/build_final_manifest.py --check`: passen per l'única unitat aprovada.
- `uv run cervell render --check docs`: passa després de regenerar `docs/index.md` perquè inclogui el document jurídic existent.
- `python scripts/check_links.py docs` i `python scripts/check_links.py final-corpus`: passen, amb 3.067 i 4 documents respectivament.
- `bash scripts/verify.sh`: no passa. La comprovació de format informa 6.137 infraccions sota `docs/raw/corpus-parla-andorrana/`, directori preexistent no modificat en aquesta tanda. Mypy informa 11 fitxers correctes i pytest passa amb 27 proves. La comprovació de renderització va fallar inicialment per l'índex desactualitzat i passa després de regenerar-lo.
- `git diff --check`: passa.
