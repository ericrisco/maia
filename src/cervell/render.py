"""Genera el contracte i l'índex des de l'esquema i el corpus.

Aquests fitxers NO s'editen a mà. El text que llegeix una persona i la regla que
aplica la màquina surten de la mateixa font: per això el criteri "seguir el
contracte produeix un document que passa" es pot garantir en lloc de prometre.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cervell.schema import FieldSpec, Schema

if TYPE_CHECKING:
    from cervell.model import Corpus, Doc

AVIS = (
    "<!-- GENERAT des de schema/corpus.toml. No l'editeu a mà: "
    "els canvis es perden i la comprovació falla amb R012. -->"
)


def _taula_camps(fields: dict[str, FieldSpec]) -> str:
    files = ["| Camp | Obligatori | Valors | Què hi va |", "| --- | --- | --- | --- |"]
    for name, spec in fields.items():
        obligatori = "**sí**" if spec.required else "no"
        if spec.enum:
            valors = f"enum `{spec.enum}`"
        elif spec.pattern:
            valors = "per forma"
        elif spec.type:
            valors = f"`{spec.type}`"
        else:
            valors = "text lliure"
        desc = " ".join(spec.description.split())
        files.append(f"| `{name}` | {obligatori} | {valors} | {desc} |")
    return "\n".join(files)


def contract(schema: Schema) -> str:
    """El contracte d'entrada, llegible, generat des de l'esquema."""
    enums = "\n".join(
        f"- `{nom}` — {' · '.join(f'`{v}`' for v in valors)}"
        for nom, valors in schema.enums.items()
    )
    regles = "\n".join(
        f"| `{rid}` | {'**avís**' if r.severity == 'warning' else 'error'} | {r.message} |"
        for rid, r in sorted(schema.rules.items())
    )
    return f"""{AVIS}

# Contracte d'entrada del cervell andorrà

> Esquema v{schema.version} · arrel de la bóveda: `{schema.vault_root}/`

Qualsevol document que entri al corpus compleix això. El que no ho compleix no
entra: la comprovació falla i us diu quin document i quin camp.

## La distinció que ho ordena tot

Un text **sobre** Andorra no és un text **en** andorrà. Per això cada document
declara dos fets independents, i l'aptitud com a model de llengua se'n **deriva**:

```
{schema.derivation.field} = {schema.derivation.rule}
```

{schema.derivation.explanation}

És una regla i no un criteri perquè no s'hagi de discutir document a document.
Conseqüència contraintuïtiva que val la pena recordar: **la revisió humana no
canvia la veu**. Un article compilat que algú revisa i corregeix és més fiable
com a coneixement i segueix sent compilat — el va escriure un agent.

## Valors tancats

{enums}

## Camps d'un document de corpus

{_taula_camps(schema.fields)}

## Camps d'una fitxa de font

Una fitxa per **font**, no per document. Cinquanta articles del mateix fons
referencien la mateixa fitxa: duplicar la llicència a cada document garanteix
que d'aquí a sis mesos n'hi hagi cinquanta versions divergents.

{_taula_camps(schema.font_fields)}

## Com s'afegeix un document

1. Si la font encara no té fitxa, escriviu-la a `{schema.vault_root}/fonts/<id>.md`.
2. Escriviu el document a la branca que li toca. La **ruta ha de correspondre**
   al camp `tema`.
3. Calculeu `apte_llengua` amb la regla de dalt. No l'inventeu: si no quadra, la
   comprovació ho detecta.
4. Executeu `uv run cervell check {schema.vault_root}/`.
5. Regenereu l'índex. No l'editeu a mà.

Afegir una branca nova és **crear un directori**. `tema` es valida per forma i no
contra una llista tancada, precisament perquè el contracte no faci nosa.

## Les regles

| Id | Severitat | Què comprova |
| --- | --- | --- |
{regles}

Els **avisos** s'imprimeixen i no canvien el codi de sortida. Avui només `R005`:
la procedència es registra sempre amb el seu valor real, però no veta l'entrada
(constitució §24). El registre existeix perquè la decisió segueixi sent
reversible i es pugui separar el corpus per porcions de llicència.
"""


def index(corpus: Corpus) -> str:
    """El catàleg llegible per màquina: què hi ha i de quina mena, sense obrir res."""
    from collections import defaultdict

    per_tema: dict[str, list[Doc]] = defaultdict(list)
    for d in corpus.docs:
        per_tema[d.tema or "(sense tema)"].append(d)

    aptes = sum(1 for d in corpus.docs if d.apte_llengua)
    linies = [
        AVIS.replace("des de schema/corpus.toml", "des del corpus"),
        "",
        "# Índex del cervell andorrà",
        "",
        f"**{len(corpus.docs)}** documents · **{len(corpus.fonts)}** fonts · "
        f"**{aptes}** aptes com a model de llengua · **{len(per_tema)}** temes amb contingut.",
        "",
    ]
    if not corpus.docs:
        linies += [
            "> El corpus és buit. Això és un estat vàlid: el contenidor funciona sense contingut.",
            "",
        ]

    for tema in sorted(per_tema):
        linies += [
            f"## {tema}",
            "",
            "| Document | Tema | Veu | Època | Apte | Font |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
        for d in sorted(per_tema[tema], key=lambda x: x.path.name):
            rel = d.path.relative_to(corpus.vault_root).as_posix()
            apte = "sí" if d.apte_llengua else "no"
            linies.append(
                f"| [{d.title or d.path.stem}]({rel}) | `{d.tema}` | {d.veu} | {d.epoca} | {apte} | `{d.font}` |"
            )
        linies.append("")

    if corpus.fonts:
        linies += [
            "## Fonts",
            "",
            "| Id | Titular | Llicència | Redistribució |",
            "| --- | --- | --- | --- |",
        ]
        for fid in sorted(corpus.fonts):
            f = corpus.fonts[fid]
            rel = f.path.relative_to(corpus.vault_root).as_posix()
            linies.append(
                f"| [`{fid}`]({rel}) | {f.data.get('titular', '')} | "
                f"{f.data.get('llicencia', '')} | {f.redistribucio} |"
            )
        linies.append("")

    return "\n".join(linies)
