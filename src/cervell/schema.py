"""L'esquema: la font de veritat del corpus, llegida com a dada.

El contracte que llegeix una persona, les regles que aplica el validador i les
columnes de l'índex surten tots d'aquí. Per això `schema/corpus.toml` és dada i
no codi: dues fonts divergeixen, una sola no pot.
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Literal

Severity = Literal["error", "warning"]


class Veu(StrEnum):
    """Qui va produir el text."""

    ORIGINARIA = "originaria"
    COMPILADA = "compilada"


class Epoca(StrEnum):
    """De quan és la llengua del text."""

    CONTEMPORANIA = "contemporania"
    HISTORICA = "historica"


def derive_aptitude(veu: Veu, epoca: Epoca) -> bool:
    """Un text SOBRE Andorra no és un text EN andorrà.

    Apte com a model de llengua si i només si el va produir algú parlant
    andorrà i la llengua és d'avui. És una regla i no un criteri perquè no
    s'hagi de discutir document a document: ni la revisió humana converteix
    prosa compilada en parla andorrana.
    """
    return veu is Veu.ORIGINARIA and epoca is Epoca.CONTEMPORANIA


@dataclass(frozen=True, slots=True)
class FieldSpec:
    """Un camp del frontmatter, tal com el declara l'esquema."""

    name: str
    required: bool
    description: str
    enum: str | None = None
    pattern: str | None = None
    type: str | None = None
    derived: bool = False


@dataclass(frozen=True, slots=True)
class RuleSpec:
    """Una regla del catàleg. L'id és estable; els tests i la spec s'hi refereixen."""

    id: str
    severity: Severity
    message: str


@dataclass(frozen=True, slots=True)
class Derivation:
    """Com es deriva un camp d'altres."""

    field: str
    rule: str
    explanation: str


@dataclass(frozen=True, slots=True)
class Schema:
    """L'esquema complet, ja tipat."""

    version: str
    vault_root: str
    derivation: Derivation
    enums: dict[str, list[str]]
    fields: dict[str, FieldSpec]
    font_fields: dict[str, FieldSpec]
    rules: dict[str, RuleSpec]


def _fields(raw: dict[str, dict[str, object]]) -> dict[str, FieldSpec]:
    return {
        name: FieldSpec(
            name=name,
            required=bool(spec.get("required", False)),
            description=str(spec.get("description", "")),
            enum=str(spec["enum"]) if "enum" in spec else None,
            pattern=str(spec["pattern"]) if "pattern" in spec else None,
            type=str(spec["type"]) if "type" in spec else None,
            derived=bool(spec.get("derived", False)),
        )
        for name, spec in raw.items()
    }


def load(path: Path) -> Schema:
    """Llegeix l'esquema des del seu fitxer TOML."""
    raw = tomllib.loads(path.read_text(encoding="utf-8"))
    meta = raw["meta"]
    der = raw["derivation"]
    return Schema(
        version=str(meta["version"]),
        vault_root=str(meta["vault_root"]),
        derivation=Derivation(
            field=str(der["field"]),
            rule=str(der["rule"]),
            explanation=str(der["explanation"]).strip(),
        ),
        enums={k: [str(v) for v in vs] for k, vs in raw["enums"].items()},
        fields=_fields(raw["fields"]),
        font_fields=_fields(raw["font_fields"]),
        rules={
            rid: RuleSpec(
                id=rid,
                severity="warning" if spec["severity"] == "warning" else "error",
                message=str(spec["message"]),
            )
            for rid, spec in raw["rules"].items()
        },
    )
