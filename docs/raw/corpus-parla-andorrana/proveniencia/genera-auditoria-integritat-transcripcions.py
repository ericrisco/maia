"""Audita la coherència estructural de les transcripcions ASR per font."""
from __future__ import annotations

import csv
import json
import re
import wave
from pathlib import Path

ROOT = Path(__file__).parents[1]
TRANS = ROOT / "transcripcions"
OUT = ROOT / "proveniencia" / "auditoria-integritat-transcripcions.tsv"
VTT_CUE = re.compile(r"^\d\d:\d\d:\d\d\.\d{3} --> \d\d:\d\d:\d\d\.\d{3}$", re.MULTILINE)


def main() -> None:
    rows: list[dict[str, str]] = []
    for audio in sorted((ROOT / "audios").glob("pa-*/audio.wav")):
        pid = audio.parent.name
        txt_path = TRANS / f"{pid}.txt"
        vtt_path = TRANS / f"{pid}.vtt"
        json_path = TRANS / f"{pid}.json"
        errors: list[str] = []
        try:
            with wave.open(str(audio)) as handle:
                duration_s = handle.getnframes() / handle.getframerate()
        except (OSError, EOFError, wave.Error) as exc:
            duration_s = 0.0
            errors.append(f"audio:{type(exc).__name__}")
        txt = txt_path.read_text(encoding="utf-8") if txt_path.exists() else ""
        vtt = vtt_path.read_text(encoding="utf-8") if vtt_path.exists() else ""
        if not txt.strip():
            errors.append("TXT buit")
        if not vtt.strip():
            errors.append("VTT buit")
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
            segments = data.get("transcription", [])
            ends = [int(segment.get("offsets", {}).get("to", 0)) for segment in segments]
            texts = [segment.get("text", "").strip() for segment in segments]
            if not segments or not any(texts):
                errors.append("JSON sense segments textuals")
            if ends != sorted(ends):
                errors.append("timestamps no ordenats")
            max_end_ms = max(ends, default=0)
        except (OSError, json.JSONDecodeError, AttributeError, TypeError, ValueError) as exc:
            segments, max_end_ms = [], 0
            errors.append(f"JSON:{type(exc).__name__}")
        if duration_s and max_end_ms > (duration_s * 1000) + 1500:
            errors.append("timestamp fora de la durada del WAV")
        rows.append(
            {
                "id_persona": pid,
                "txt_caracters": str(len(txt.strip())),
                "vtt_cues": str(len(VTT_CUE.findall(vtt))),
                "json_segments": str(len(segments)),
                "durada_audio_s": f"{duration_s:.3f}",
                "max_timestamp_ms": str(max_end_ms),
                "estat": "complet" if not errors else "pendent",
                "nota": "; ".join(errors),
            }
        )
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        fields = list(rows[0])
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    complete = sum(row["estat"] == "complet" for row in rows)
    print(f"{len(rows)} transcripcions auditades · completes={complete} · {OUT}")


if __name__ == "__main__":
    main()
