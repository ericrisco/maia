"""Tests for local transcription on Apple silicon (PLAN M1.13).

``mlx-whisper`` is Apple-silicon only and CI is Linux, so the library is exercised through a
stand-in module injected into ``sys.modules``. What that verifies is the part this module owns:
the language pin, the segment mapping, the ffmpeg plumbing and the batch behaviour.
"""

from __future__ import annotations

import json
import sys
import types
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest

from maia.schemas import License, Registre, Source
from maia.scraping.radio import Segment
from maia.scraping.transcribe import (
    DEFAULT_MODEL,
    LANGUAGE,
    SMALL_MODEL,
    MlxTranscriber,
    TranscriptionUnavailableError,
    ensure_ffmpeg,
    main,
    read_manifest,
    transcribe_manifest,
)

STAMP = datetime(2026, 8, 2, tzinfo=UTC)
PAGE = "https://www.rtva.ad/ca/programes/l-editorial-avui-sera-un-bon-dia-31-03-2026"

# Shortened from the real transcription of 2026-03-31, produced by whisper-small on an M4.
REAL_SEGMENTS = [
    {"start": 0.0, "end": 7.0, "text": " Bon dia, Andorra. Són les 8 del matí."},
    {
        "start": 7.0,
        "end": 18.0,
        "text": " Si tirem la vista endarrere els darrers mesos, no fem altra cosa "
        "que parlar de la crisi del creixement, i de com fer que el vaixell "
        "faci un viatge el menys brusc possible.",
    },
    {
        "start": 18.0,
        "end": 30.0,
        "text": " El vaixell és el país i la col·lisió és el col·lapse. I ens en seguiran parlant: "
        "serà el tema de les properes eleccions generals d'aquí un any.",
    },
]


def _fake_mlx(monkeypatch: pytest.MonkeyPatch, segments: list[dict[str, Any]]) -> dict[str, Any]:
    """Install a stand-in `mlx_whisper` and return the kwargs it was called with."""
    captured: dict[str, Any] = {}

    def _transcribe(audio: str, **kwargs: Any) -> dict[str, Any]:
        captured.update(audio=audio, **kwargs)
        return {"segments": segments, "text": " ".join(s["text"] for s in segments)}

    module = types.ModuleType("mlx_whisper")
    module.transcribe = _transcribe  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "mlx_whisper", module)
    return captured


def _fake_ffmpeg(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    """Install a stand-in `imageio_ffmpeg` whose binary lives under a versioned name."""
    binary = tmp_path / "ffmpeg-macos-aarch64-v7.1"
    binary.write_text("#!/bin/sh\n", encoding="utf-8")
    module = types.ModuleType("imageio_ffmpeg")
    module.get_ffmpeg_exe = lambda: str(binary)  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "imageio_ffmpeg", module)
    return binary


# ── the language pin ─────────────────────────────────────────────────────────


@pytest.mark.unit
def test_catalan_is_pinned_rather_than_detected(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Whisper identifies language from the first 30 seconds, and on Andorran Catalan it can land
    on Spanish or Occitan — after which it transcribes the whole programme *as* that language.
    That does not fail; it produces fluent wrong text, which is the worst possible outcome for a
    corpus whose entire purpose is the language."""
    captured = _fake_mlx(monkeypatch, REAL_SEGMENTS)
    _fake_ffmpeg(monkeypatch, tmp_path)
    audio = tmp_path / "a.mp3"
    audio.write_bytes(b"ID3")

    MlxTranscriber().transcribe(audio)
    assert captured["language"] == "ca"
    assert LANGUAGE == "ca"
    assert captured["path_or_hf_repo"] == DEFAULT_MODEL


@pytest.mark.unit
def test_the_model_is_overridable_for_a_cheap_smoke_test(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    captured = _fake_mlx(monkeypatch, REAL_SEGMENTS)
    _fake_ffmpeg(monkeypatch, tmp_path)
    audio = tmp_path / "a.mp3"
    audio.write_bytes(b"ID3")

    MlxTranscriber(model=SMALL_MODEL).transcribe(audio)
    assert captured["path_or_hf_repo"] == SMALL_MODEL


# ── segments ─────────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_whisper_output_becomes_segments_with_the_leading_space_stripped(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Whisper prefixes every segment with a space. Left in, it survives merging and shows up
    inside the corpus text."""
    _fake_mlx(monkeypatch, REAL_SEGMENTS)
    _fake_ffmpeg(monkeypatch, tmp_path)
    audio = tmp_path / "a.mp3"
    audio.write_bytes(b"ID3")

    segments = MlxTranscriber().transcribe(audio)
    assert len(segments) == 3
    assert isinstance(segments[0], Segment)
    assert segments[0].text.startswith("Bon dia")
    assert segments[0].start == 0.0
    assert segments[2].end == 30.0


@pytest.mark.unit
def test_a_result_with_no_segments_is_empty_not_an_error(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Silence is a legitimate outcome; M1.13's own filters decide what to do about it."""
    _fake_mlx(monkeypatch, [])
    _fake_ffmpeg(monkeypatch, tmp_path)
    audio = tmp_path / "a.mp3"
    audio.write_bytes(b"ID3")
    assert MlxTranscriber().transcribe(audio) == []


@pytest.mark.unit
def test_missing_audio_says_so_instead_of_failing_inside_ffmpeg(tmp_path: Path) -> None:
    """Whisper's own error for a missing file is an ffmpeg exit code, which sends the reader
    looking for a decoding problem."""
    with pytest.raises(FileNotFoundError, match="no audio at"):
        MlxTranscriber().transcribe(tmp_path / "nope.mp3")


# ── ffmpeg plumbing ──────────────────────────────────────────────────────────


@pytest.mark.unit
def test_ffmpeg_is_exposed_under_the_plain_name_whisper_looks_for(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """`imageio-ffmpeg` ships the binary as `ffmpeg-macos-aarch64-v7.1`; whisper shells out to
    `ffmpeg`. Without the symlink the transcription fails with a confusing FileNotFoundError from
    inside a subprocess."""
    binary = _fake_ffmpeg(monkeypatch, tmp_path)
    monkeypatch.setenv("PATH", "/usr/bin")

    directory = ensure_ffmpeg()
    assert directory == str(tmp_path)
    assert (tmp_path / "ffmpeg").is_symlink()
    assert (tmp_path / "ffmpeg").resolve() == binary.resolve()
    assert str(tmp_path) in __import__("os").environ["PATH"]


@pytest.mark.unit
def test_ffmpeg_setup_is_idempotent(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """A batch calls this once per episode; the second call must not fail on an existing link."""
    _fake_ffmpeg(monkeypatch, tmp_path)
    assert ensure_ffmpeg() == ensure_ffmpeg()


@pytest.mark.unit
def test_a_missing_dependency_names_the_install_command(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """ "ModuleNotFoundError: mlx_whisper" is not an answer to "why can I not build the corpus"."""
    monkeypatch.setitem(sys.modules, "imageio_ffmpeg", None)
    with pytest.raises(TranscriptionUnavailableError, match="imageio-ffmpeg"):
        ensure_ffmpeg()

    _fake_ffmpeg(monkeypatch, tmp_path)
    monkeypatch.setitem(sys.modules, "mlx_whisper", None)
    audio = tmp_path / "a.mp3"
    audio.write_bytes(b"ID3")
    with pytest.raises(TranscriptionUnavailableError, match="mlx-whisper"):
        MlxTranscriber().transcribe(audio)


# ── the manifest ─────────────────────────────────────────────────────────────


def _manifest(tmp_path: Path, count: int = 2) -> Path:
    directory = tmp_path / "audio"
    directory.mkdir()
    path = directory / "manifest.jsonl"
    with path.open("w", encoding="utf-8") as handle:
        for index in range(count):
            name = f"2026-03-{29 + index}.mp3"
            (directory / name).write_bytes(b"ID3")
            handle.write(
                json.dumps(
                    {
                        "broadcast": f"2026-03-{29 + index}",
                        "programme": "Avui serà un bon dia",
                        "page_url": PAGE,
                        "audio_url": "https://cdn/x.mp3",
                        "path": name,
                        "bytes": 3,
                        "licence": "no-redistribute",
                    }
                )
                + "\n"
            )
    return path


@pytest.mark.unit
def test_audio_paths_resolve_relative_to_the_manifest(tmp_path: Path) -> None:
    """So a directory can be copied to another machine without rewriting it."""
    path = _manifest(tmp_path)
    entries = read_manifest(path)
    assert len(entries) == 2
    assert entries[0].path == path.parent / "2026-03-29.mp3"
    assert entries[0].path.is_file()
    assert entries[0].spec().url == PAGE


@pytest.mark.unit
def test_a_malformed_manifest_line_is_an_error_not_a_skip(tmp_path: Path) -> None:
    """Skipping it drops an episode from the corpus, and nothing downstream can tell which."""
    path = tmp_path / "m.jsonl"
    path.write_text('{"broadcast": "2026-03-29"}\n', encoding="utf-8")
    with pytest.raises(ValueError, match="unreadable manifest entry"):
        read_manifest(path)

    path.write_text("not json\n", encoding="utf-8")
    with pytest.raises(ValueError, match="unreadable manifest entry"):
        read_manifest(path)


# ── batch behaviour ──────────────────────────────────────────────────────────


class FakeTranscriber:
    def __init__(self, segments: list[Segment], fail_on: str | None = None) -> None:
        self.segments = segments
        self.fail_on = fail_on

    def transcribe(self, audio: Path) -> list[Segment]:
        if self.fail_on and self.fail_on in audio.name:
            raise OSError("truncated file")
        return self.segments


def _segments() -> list[Segment]:
    """Enough text to clear the 200-character minimum for a §3.1 document."""
    return [
        Segment(index * 6.0, index * 6.0 + 6.0, f"{text} " * 2)
        for index, text in enumerate(
            [
                "Bon dia, Andorra. Són les vuit del matí i avui parlem de la crisi del creixement.",
                "La canalla torna a l'escola i moltes famílies encara no saben els horaris.",
                "Caldrà que el Govern ho aclareixi abans de plegar aquesta setmana.",
            ]
        )
    ]


@pytest.mark.unit
def test_a_manifest_becomes_no_redistribute_oral_documents(tmp_path: Path) -> None:
    """The licence and register come from M1.13 and are not this module's to choose."""
    entries = read_manifest(_manifest(tmp_path, count=1))
    documents = transcribe_manifest(
        entries,
        FakeTranscriber(_segments()),  # type: ignore[arg-type]
        fetched_at=STAMP,
    )
    assert documents
    for document in documents:
        assert document.source is Source.RTVA
        assert document.license is License.NO_REDISTRIBUTE
        assert document.registre is Registre.ANDORRA_PARLAT_ORAL
        assert document.fetched_at == STAMP
        assert str(document.url) == PAGE


@pytest.mark.unit
def test_one_bad_episode_does_not_end_the_batch_but_is_reported(tmp_path: Path) -> None:
    """Over a year of daily audio there will be a truncated download. A batch that quietly
    produces fewer documents than it had inputs is how a corpus ends up with holes nobody can
    date."""
    entries = read_manifest(_manifest(tmp_path, count=2))
    seen: list[tuple[str, int | None, str | None]] = []

    documents = transcribe_manifest(
        entries,
        FakeTranscriber(_segments(), fail_on="2026-03-29"),  # type: ignore[arg-type]
        on_progress=lambda entry, count, error: seen.append(
            (entry.broadcast, count, str(error) if error else None)
        ),
    )
    assert documents
    assert seen[0][0] == "2026-03-29"
    assert seen[0][1] is None
    assert "truncated" in (seen[0][2] or "")
    assert seen[1][1] is not None


@pytest.mark.unit
def test_progress_reporting_is_optional(tmp_path: Path) -> None:
    entries = read_manifest(_manifest(tmp_path, count=1))
    assert transcribe_manifest(entries, FakeTranscriber(_segments()))  # type: ignore[arg-type]


# ── the CLI ──────────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_cli_transcribes_a_manifest_to_jsonl(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    manifest = _manifest(tmp_path, count=1)
    monkeypatch.setattr(
        "maia.scraping.transcribe.MlxTranscriber",
        lambda **kwargs: FakeTranscriber(_segments()),
    )
    out = tmp_path / "rtva.jsonl"
    assert main([str(manifest), "--out", str(out), "--small"]) == 0

    printed = capsys.readouterr().out
    assert SMALL_MODEL in printed
    assert "document(s) from 1 episode(s)" in printed
    assert out.read_text(encoding="utf-8").count("no-redistribute") >= 1


@pytest.mark.unit
def test_the_cli_reports_a_failed_episode_and_exits_non_zero_when_all_fail(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    manifest = _manifest(tmp_path, count=1)
    monkeypatch.setattr(
        "maia.scraping.transcribe.MlxTranscriber",
        lambda **kwargs: FakeTranscriber([], fail_on="2026"),
    )
    assert main([str(manifest)]) == 1
    assert "FAILED" in capsys.readouterr().err


@pytest.mark.unit
def test_the_cli_says_what_to_install_when_transcription_is_unavailable(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    manifest = _manifest(tmp_path, count=1)

    def _unavailable(**kwargs: Any) -> None:
        raise TranscriptionUnavailableError("mlx-whisper is not installed (Apple silicon only)")

    monkeypatch.setattr("maia.scraping.transcribe.MlxTranscriber", _unavailable)
    assert main([str(manifest)]) == 1
    assert "Apple silicon" in capsys.readouterr().err


@pytest.mark.unit
def test_the_cli_rejects_a_missing_empty_or_broken_manifest(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([str(tmp_path / "nope.jsonl")]) == 1
    assert "no manifest" in capsys.readouterr().err

    empty = tmp_path / "empty.jsonl"
    empty.write_text("\n", encoding="utf-8")
    assert main([str(empty)]) == 1
    assert "lists no episodes" in capsys.readouterr().err

    broken = tmp_path / "broken.jsonl"
    broken.write_text("{}\n", encoding="utf-8")
    assert main([str(broken)]) == 1
    assert "unreadable manifest entry" in capsys.readouterr().err


@pytest.mark.unit
def test_the_cli_limit_narrows_the_batch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    manifest = _manifest(tmp_path, count=2)
    monkeypatch.setattr(
        "maia.scraping.transcribe.MlxTranscriber",
        lambda **kwargs: FakeTranscriber(_segments()),
    )
    assert main([str(manifest), "--limit", "1"]) == 0
    assert "1 episode(s)" in capsys.readouterr().out


@pytest.mark.unit
def test_a_read_only_ffmpeg_directory_reports_rather_than_crashes(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """The binary can land in a read-only cache, or two parallel runs can race to create the link.
    Either way the useful message is "here is what I could not do", not an OSError from symlink."""
    binary = _fake_ffmpeg(monkeypatch, tmp_path)

    def _refuse(*args: object, **kwargs: object) -> None:
        raise OSError("read-only file system")

    monkeypatch.setattr(Path, "symlink_to", _refuse)
    (tmp_path / "ffmpeg").unlink(missing_ok=True)
    with pytest.raises(TranscriptionUnavailableError, match="plain name"):
        ensure_ffmpeg()
    assert binary.exists()


@pytest.mark.unit
def test_the_cli_without_out_still_reports(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Counting what a manifest yields before committing the corpus to disk is a real use."""
    manifest = _manifest(tmp_path, count=1)
    monkeypatch.setattr(
        "maia.scraping.transcribe.MlxTranscriber",
        lambda **kwargs: FakeTranscriber(_segments()),
    )
    assert main([str(manifest)]) == 0
    printed = capsys.readouterr().out
    assert "document(s) from 1 episode(s)" in printed
    assert "wrote" not in printed


@pytest.mark.unit
def test_a_failure_with_no_progress_callback_is_still_survived(tmp_path: Path) -> None:
    """The reporting is optional; the skipping is not."""
    entries = read_manifest(_manifest(tmp_path, count=2))
    documents = transcribe_manifest(
        entries,
        FakeTranscriber(_segments(), fail_on="2026-03-29"),  # type: ignore[arg-type]
    )
    assert documents  # the second episode still produced its documents
