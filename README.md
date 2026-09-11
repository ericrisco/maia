# maia — el cervell andorrà

Corpus obert de coneixement andorrà: història, llengua, institucions, costums i
parla, documentat amb la seva procedència i navegable com una base de coneixement.

Aquest repositori conté **el contenidor i el contingut**, no el model. La feina
d'entrenament i avaluació viu en una fase posterior.

## Què hi ha aquí

| Ruta | Què és |
| --- | --- |
| `docs/` | El corpus. S'obre directament com a vault d'Obsidian. |
| `docs/temes/` | Coneixement compilat, organitzat per dominis. |
| `docs/parla/` | Transcripcions de parla andorrana, literals. |
| `docs/fonts/` | Una fitxa per font: titular, llicència, redistribució. |
| `src/cervell/` | L'eina que valida el corpus i genera el contracte i l'índex. |
| `schema/corpus.toml` | La font de veritat: camps, enums i regles. |

## La distinció que ho ordena tot

Cada document declara **qui va produir el text** i **de quina època és la llengua**:

```yaml
veu: originaria | compilada        # verbatim andorrà, o redactat per un agent
epoca: contemporania | historica   # llengua d'avui, o d'un altre temps
apte_llengua                        # derivat: sí ⟺ originaria ∧ contemporania
```

Un text sobre Andorra no és el mateix que un text **en** andorrà. La derivació és
una regla, no un criteri: així no es discuteix document a document.

## Ús

```bash
uv sync
uv run cervell check docs/    # valida tot el corpus
uv run pytest                 # la suite
```

El contracte d'entrada viu a `docs/CONTRACT.md` i **es genera** des de
`schema/corpus.toml`. No s'edita a mà: el que llegeix una persona i el que
comprova la màquina surten de la mateixa font, i per això no poden divergir.

## Llicència

Per determinar. Cada font del corpus declara la seva a la seva fitxa.
