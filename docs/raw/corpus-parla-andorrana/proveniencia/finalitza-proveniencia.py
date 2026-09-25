"""Completa la fitxa de procedència local per a una persona amb àudio."""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parents[1]


def main(pid: str) -> None:
    folder = ROOT / "proveniencia" / pid
    source = json.loads((folder / "source.info.json").read_text())
    audio = ROOT / "audios" / pid / "audio.wav"
    digest = hashlib.sha256(audio.read_bytes()).hexdigest()
    license_name = source.get("license")
    is_open = bool(license_name and "creative commons" in license_name.lower())
    if is_open:
        terms = (
            "La font declara una llicència oberta; qualsevol redistribució del "
            "derivat ha de conservar-ne l'atribució i els termes."
        )
    elif license_name:
        terms = (
            f"La font declara els termes d'ús «{license_name}»; el derivat es "
            "conserva només per a recerca i no es redistribueix."
        )
    else:
        terms = (
            "L'àudio sense llicència oberta es conserva només com a derivat local "
            "de recerca i no es redistribueix."
        )
    body = f'''# Procedència — {pid}

- **Font:** {source.get("title", "")}
- **Canal:** {source.get("channel", source.get("uploader", ""))}
- **URL:** {source.get("webpage_url", "")}
- **Publicació:** {source.get("upload_date", "")}
- **Durada declarada:** {source.get("duration", "")} segons.
- **Llicència declarada:** {license_name or "no declarada; llicència estàndard de YouTube"}.
- **Consulta i descàrrega:** {date.today().isoformat()}.
- **Derivat local:** `../audios/{pid}/audio.wav`; SHA-256 `{digest}`.
- **ASR:** `whisper-cli`, model `ggml-small.bin`, llengua `ca`, 8 fils.

{terms} El JSON de la transcripció conserva els tokens i les probabilitats; la
versió `-marcada.txt` fa visibles les conjectures de l'ASR.
'''
    (folder / "README.md").write_text(body)
    print(folder / "README.md")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("ús: python finalitza-proveniencia.py pa-004")
    main(sys.argv[1])
