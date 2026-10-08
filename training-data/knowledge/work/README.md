# Feina de Knowledge

`coverage.csv` enumera tots els fitxers Markdown de `docs/temes/`. Tots comencen amb estat `pending`; cap fitxer es considera revisat només perquè aparegui a l'inventari.

Per reconstruir els inventaris de Knowledge i Language des de l'arrel de Maia, executa `python3 training-data/scripts/inventory.py`. El generador conserva les metadades del frontmatter i no marca cap font com a apte per entrenar.
