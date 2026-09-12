"""Carrega el corpus del disc i el tipa. No jutja: això són les regles.

La invariant que importa: un document malformat MAI fa petar la càrrega. Es
registra a `unparsed` i la comprovació segueix, perquè un validador que s'atura
al primer error obliga a arreglar el corpus d'un en un.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n(.*)\Z", re.DOTALL)
ENLLAC = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
WIKILINK = re.compile(r"\[\[([^\]]+)\]\]")
CITA = re.compile(r"^>\s?(.+)$", re.MULTILINE)
GENERATS = {"CONTRACT.md", "index.md", "README.md"}

# Subarbres de la bóveda que NO són corpus. `raw/` guarda el material de
# partida —extractes de fonts, notes de consulta, registres de procedència— i
# els seus .md no han de passar pel contracte: no són documents del corpus,
# són la matèria primera d'on surten.
FORA_DEL_CORPUS = {"raw"}


@dataclass(frozen=True, slots=True)
class Unparsed:
    """Un document que no s'ha pogut llegir, amb el motiu."""

    path: Path
    reason: str


@dataclass(frozen=True, slots=True)
class Font:
    """Una fitxa de font. Una per FONT, no per document."""

    path: Path
    id: str
    data: dict[str, Any]

    @property
    def redistribucio(self) -> str:
        return str(self.data.get("redistribucio", ""))


@dataclass(frozen=True, slots=True)
class Doc:
    """Un document de corpus."""

    path: Path
    data: dict[str, Any]
    body: str
    links: list[str] = field(default_factory=list)
    wikilinks: list[str] = field(default_factory=list)
    cites: list[str] = field(default_factory=list)

    def _s(self, key: str) -> str:
        return str(self.data.get(key, ""))

    @property
    def title(self) -> str:
        return self._s("title")

    @property
    def tema(self) -> str:
        return self._s("tema")

    @property
    def veu(self) -> str:
        return self._s("veu")

    @property
    def epoca(self) -> str:
        return self._s("epoca")

    @property
    def font(self) -> str:
        return self._s("font")

    @property
    def apte_llengua(self) -> bool:
        return bool(self.data.get("apte_llengua", False))


@dataclass(frozen=True, slots=True)
class Corpus:
    """El corpus sencer, ja llegit."""

    vault_root: Path
    docs: list[Doc]
    fonts: dict[str, Font]
    unparsed: list[Unparsed]


def _split(text: str) -> tuple[dict[str, Any], str] | None:
    m = FRONTMATTER.match(text)
    if not m:
        return None
    data = yaml.safe_load(m.group(1))
    if not isinstance(data, dict):
        return None
    return data, m.group(2)


def load_corpus(root: Path) -> Corpus:
    """Llegeix tot l'arbre. Un corpus buit és un corpus vàlid."""
    docs: list[Doc] = []
    fonts: dict[str, Font] = {}
    unparsed: list[Unparsed] = []

    if not root.exists():
        return Corpus(vault_root=root, docs=[], fonts={}, unparsed=[])

    for md in sorted(root.rglob("*.md")):
        if md.name in GENERATS:
            continue
        if FORA_DEL_CORPUS.intersection(md.relative_to(root).parts[:-1]):
            continue
        text = md.read_text(encoding="utf-8")
        try:
            parts = _split(text)
        except yaml.YAMLError as exc:
            unparsed.append(Unparsed(md, f"YAML invàlid: {exc.__class__.__name__}"))
            continue
        if parts is None:
            unparsed.append(Unparsed(md, "sense frontmatter o frontmatter no és un mapa"))
            continue
        data, body = parts

        if data.get("type") == "font":
            fid = str(data.get("id", md.stem))
            fonts[fid] = Font(path=md, id=fid, data=data)
            continue

        docs.append(
            Doc(
                path=md,
                data=data,
                body=body,
                links=[
                    dest for _, dest in ENLLAC.findall(body) if not dest.startswith(("http", "#"))
                ],
                wikilinks=WIKILINK.findall(body),
                cites=[c.strip() for c in CITA.findall(body) if c.strip()],
            )
        )

    return Corpus(vault_root=root, docs=docs, fonts=fonts, unparsed=unparsed)
