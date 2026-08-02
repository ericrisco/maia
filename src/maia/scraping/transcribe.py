"""Local speech-to-text on Apple silicon — PLAN M1.13, the half that was assumed to need a GPU.

The plan treats transcription as blocked-by-resource: ``whisper-large-v3-ca`` needs a GPU, so
:class:`~maia.scraping.radio.Transcriber` was left as a seam with no implementation. On an Apple
silicon machine that assumption is wrong. **MLX runs whisper on the integrated GPU**, and a 2m17s
editorial transcribes in 85 seconds with ``whisper-small`` on an M4 — no CUDA, no cloud, no API
key, no per-minute billing. Verified against real RTVA audio before this module was written.

That matters beyond convenience. It means the oral subcorpus can be built incrementally on the
machine that already has the audio, and re-run when a better model appears, instead of waiting for
a rented GPU and paying for every experiment.

**Two dependencies, both optional and both imported lazily.** ``mlx-whisper`` only exists on Apple
silicon, and ``imageio-ffmpeg`` ships a static ffmpeg binary so the host needs no system install —
whisper shells out to ffmpeg to decode MP3, and requiring a Homebrew package would put a manual
step between the corpus and anyone rebuilding it. Neither is imported at module scope, so the rest
of the package (and CI, which is Linux) is unaffected.

**Language is pinned to Catalan, and that is not a default worth leaving to detection.** Whisper's
language identification runs on the first 30 seconds; on Andorran Catalan it can land on Spanish or
Occitan, and the entire programme is then transcribed *as* that language — which does not fail, it
produces fluent wrong text. Passing ``language="ca"`` removes the possibility.

**What this does not do is judge the transcript.** M1.13's existing filters do that:
:func:`~maia.scraping.radio.looks_hallucinated` catches whisper inventing captions over silence,
and merging plus oral cleaning turn segments into §3.1 documents. This module produces
:class:`~maia.scraping.radio.Segment` objects and stops there.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from maia.schemas import CorpusDocument
from maia.scraping.radio import ProgrammeSpec, Segment, transcribe_programme

#: Default model. ``large-v3-turbo`` is the accuracy/speed point that makes a daily job practical:
#: near-large quality at several times the speed. ``whisper-large-v3-ca`` — the Catalan fine-tune
#: the plan names — has no MLX conversion published; when one exists it is a one-line change here,
#: and it should be measured against this rather than assumed better.
DEFAULT_MODEL = "mlx-community/whisper-large-v3-turbo"

#: A smaller model for smoke-testing the pipeline without a multi-gigabyte download.
SMALL_MODEL = "mlx-community/whisper-small-mlx"

#: Pinned, never detected. See the module docstring: misdetection does not fail, it produces
#: fluent wrong text.
LANGUAGE = "ca"


class TranscriptionUnavailableError(RuntimeError):
    """Raised when local transcription cannot run, with what to do about it."""


def ensure_ffmpeg() -> str:
    """Put a usable ``ffmpeg`` on ``PATH`` and return its directory.

    Whisper invokes ``ffmpeg`` by name to decode audio. ``imageio-ffmpeg`` ships a static binary
    under a versioned filename (``ffmpeg-macos-aarch64-v7.1``), which whisper will not find, so a
    plain ``ffmpeg`` symlink is created next to it.

    Raises:
        TranscriptionUnavailableError: if no ffmpeg can be provided.
    """
    try:
        import imageio_ffmpeg
    except ImportError as exc:
        raise TranscriptionUnavailableError(
            "no ffmpeg: install the optional dependency with `uv add --optional audio "
            "imageio-ffmpeg`, or put ffmpeg on PATH yourself"
        ) from exc

    executable = Path(imageio_ffmpeg.get_ffmpeg_exe())
    directory = executable.parent
    plain = directory / "ffmpeg"
    if not plain.exists():
        try:
            plain.symlink_to(executable)
        except OSError as exc:  # read-only install, or a race with a parallel run
            raise TranscriptionUnavailableError(
                f"cannot expose ffmpeg as a plain name at {plain}: {exc}"
            ) from exc

    path = os.environ.get("PATH", "")
    if str(directory) not in path.split(os.pathsep):
        os.environ["PATH"] = f"{directory}{os.pathsep}{path}"
    return str(directory)


@dataclass
class MlxTranscriber:
    """A :class:`~maia.scraping.radio.Transcriber` running whisper locally through MLX.

    Apple silicon only. The model is downloaded on first use and cached by ``huggingface_hub``;
    the first call therefore takes noticeably longer than the rest, which is worth knowing before
    concluding a batch job has hung.
    """

    model: str = DEFAULT_MODEL
    language: str = LANGUAGE

    def transcribe(self, audio: Path) -> Sequence[Segment]:
        """Transcribe ``audio`` into time-stamped segments.

        Raises:
            TranscriptionUnavailableError: when MLX or ffmpeg is missing — with the install
                command, because "ModuleNotFoundError: mlx_whisper" is not an answer to "why can I
                not build the oral corpus".
            FileNotFoundError: when the audio does not exist. Whisper's own error for a missing
                file is an ffmpeg exit code, which sends the reader in the wrong direction.
        """
        if not audio.is_file():
            raise FileNotFoundError(f"no audio at {audio}")
        ensure_ffmpeg()
        try:
            import mlx_whisper
        except ImportError as exc:
            raise TranscriptionUnavailableError(
                "mlx-whisper is not installed (Apple silicon only): "
                "`uv add --optional audio mlx-whisper`"
            ) from exc

        result = mlx_whisper.transcribe(
            str(audio),
            path_or_hf_repo=self.model,
            language=self.language,
            word_timestamps=False,
        )
        return [
            Segment(
                start=float(segment["start"]),
                end=float(segment["end"]),
                text=str(segment["text"]).strip(),
            )
            for segment in result.get("segments", ())
        ]


@dataclass(frozen=True)
class ManifestEntry:
    """One line of the M1.13 acquisition manifest."""

    path: Path
    page_url: str
    programme: str
    broadcast: str

    def spec(self) -> ProgrammeSpec:
        """§3.1 provenance, matching what the acquisition step recorded."""
        return ProgrammeSpec(
            programme=self.programme, url=self.page_url, topic=("editorial", "actualitat")
        )


def read_manifest(path: Path) -> list[ManifestEntry]:
    """Read the manifest written by ``maia-rtva-editorial``.

    Audio paths are resolved relative to the manifest, so a directory can be moved or copied to
    another machine without rewriting it.

    Raises:
        ValueError: on a line missing a field the transcription needs. Skipping it would silently
            drop an episode from the corpus.
    """
    entries: list[ManifestEntry] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
            entries.append(
                ManifestEntry(
                    path=path.parent / str(record["path"]),
                    page_url=str(record["page_url"]),
                    programme=str(record["programme"]),
                    broadcast=str(record["broadcast"]),
                )
            )
        except (ValueError, KeyError, TypeError) as exc:
            raise ValueError(f"{path}:{number}: unreadable manifest entry: {exc}") from exc
    return entries


def transcribe_manifest(
    entries: Sequence[ManifestEntry],
    transcriber: MlxTranscriber | None = None,
    *,
    fetched_at: datetime | None = None,
    on_progress: object = None,
) -> list[CorpusDocument]:
    """Transcribe every episode in a manifest into §3.1 documents.

    A failing episode is skipped rather than fatal — over a year of daily audio there will be a
    truncated download — but the caller is told, because a batch that quietly produces fewer
    documents than it had inputs is how a corpus ends up with holes nobody can date.
    """
    engine = transcriber or MlxTranscriber()
    stamp = fetched_at or datetime.now(UTC)
    documents: list[CorpusDocument] = []
    for entry in entries:
        try:
            produced = transcribe_programme(engine, entry.path, entry.spec(), fetched_at=stamp)
        except (FileNotFoundError, RuntimeError, OSError) as exc:
            if callable(on_progress):
                on_progress(entry, None, exc)
            continue
        documents.extend(produced)
        if callable(on_progress):
            on_progress(entry, len(produced), None)
    return documents


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point: transcribe an acquisition manifest into §3.1 JSONL."""
    parser = argparse.ArgumentParser(
        description="Transcribe RTVA audio locally on Apple silicon (M1.13). Runs whisper through "
        "MLX on the integrated GPU: no CUDA, no cloud, no API key. Output is no-redistribute — "
        "grounding and register only."
    )
    parser.add_argument("manifest", type=Path, help="the manifest from maia-rtva-editorial")
    parser.add_argument("--out", type=Path, help="write §3.1 JSONL here")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument(
        "--small", action="store_true", help=f"use {SMALL_MODEL} to smoke-test the pipeline"
    )
    parser.add_argument("--limit", type=int, help="at most this many episodes")
    args = parser.parse_args(argv)

    if not args.manifest.is_file():
        print(f"error: no manifest at {args.manifest}", file=sys.stderr)
        return 1
    try:
        entries = read_manifest(args.manifest)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if not entries:
        print(f"error: {args.manifest} lists no episodes", file=sys.stderr)
        return 1
    if args.limit:
        entries = entries[: args.limit]

    def report(entry: ManifestEntry, count: int | None, error: Exception | None) -> None:
        if error is not None:
            print(f"  {entry.broadcast}: FAILED — {error}", file=sys.stderr)
        else:
            print(f"  {entry.broadcast}: {count} document(s)")

    model = SMALL_MODEL if args.small else args.model
    print(f"{len(entries)} episode(s), model {model}")
    try:
        documents = transcribe_manifest(entries, MlxTranscriber(model=model), on_progress=report)
    except TranscriptionUnavailableError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"{len(documents)} document(s) from {len(entries)} episode(s)")
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("w", encoding="utf-8") as handle:
            for document in documents:
                handle.write(json.dumps(document.model_dump(mode="json"), ensure_ascii=False))
                handle.write("\n")
        print(f"wrote {args.out}")
    return 0 if documents else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
