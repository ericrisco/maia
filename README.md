# maia — el cervell andorrà

Corpus obert de coneixement andorrà: història, llengua, institucions, costums i
parla, documentat amb la seva procedència i navegable com una base de coneixement.

Aquest repositori conté **el contenidor i el contingut**, no el model. La feina
d'entrenament i avaluació viu en una fase posterior.

## Estat del projecte

**Obtenció inicial del corpus tancada el 24 de setembre de 2026.** Inventari
editorial: 1.347 articles, 618 fitxes de font i 40 documents de parla. La
fase següent és la curació i preparació de datasets, amb una avaluació
independent reservada abans de generar exemples d'entrenament.

El [registre de tancament](docs/raw/estat-projecte/tancament-obtencio-v1.md)
conserva els pendents i els criteris de la fase següent. Tancar la recopilació
no certifica que tot el material sigui apte per entrenar.

La curació ja ha començat per tandes. L'[inventari inicial](docs/raw/curacio/mapa-inicial.md)
classifica cada fitxer com a no revisat, en revisió, aprovat, pendent o
exclòs. El [corpus final](final-corpus/README.md) conté ara catorze unitats de coneixement amb fonts, termes, localitzadors i revisió model-assistida registrats: sèries de població per poble, edat, sexe, nacionalitat i registre històric, naixements, defuncions i migració; lectures històriques d’ajuts per esquí i desocupació; una síntesi de la sentència constitucional 2026-25-RE; una lectura de l’estructura del Consell General; lectures sobre superàvits i crèdits per a habitatge i sanitat, barems d’ajuts socials i normativa d’allaus; i una síntesi de les lleis de 2018 sobre vaga i acció sindical, més una lectura de la producció de tabac entre 1973 i 2025. L’esborrany jurídic dels mesos cotitzats continua pendent a `docs/temes/`. No s’ha fet cap entrenament.

## Què hi ha aquí

| Ruta | Què és |
| --- | --- |
| `docs/` | El corpus. S'obre directament com a vault d'Obsidian. |
| `docs/temes/` | Coneixement compilat, organitzat per dominis. |
| `docs/parla/` | Transcripcions i candidats de parla, amb procedència i estat de verificació per fitxa. |
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
