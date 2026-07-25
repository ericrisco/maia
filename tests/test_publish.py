"""Tests for parquet staging and the private HF dataset upload (PLAN M1.09).

The upload itself is blocked-by-resource (needs ``HF_TOKEN`` + network); :class:`FakeHub`
records what would have been sent, so every refusal and the whole staging path are verified
offline.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from pathlib import Path

import pyarrow.parquet as pq
import pytest

from maia.corpus.publish import (
    DATA_PREFIX,
    MANIFEST_NAME,
    SCHEMA_VERSION,
    Manifest,
    RestrictedContentError,
    corpus_schema,
    hf_hub,
    main,
    read_parquet,
    render,
    restricted,
    stage,
    upload_corpus,
    verify_staged,
    write_parquet,
)
from maia.schemas import CorpusDocument, Legal, License, Rang, Registre, Source

STAMP = datetime(2026, 8, 1, 12, 30, tzinfo=UTC)

PROSE = (
    "Les falles són una tradició molt antiga que se celebra a diverses parròquies del "
    "Principat. Cada any, quan arriba el solstici d'estiu, els fallaires baixen de la "
    "muntanya amb les falles enceses."
)


def doc(
    text: str = PROSE,
    *,
    source: Source = Source.GOVERN,
    url: str = "https://www.govern.ad/pagina",
    license: License = License.PUBLIC_OFFICIAL,
    topic: list[str] | None = None,
    speaker: str | None = None,
    legal: Legal | None = None,
    registre: Registre = Registre.ESTANDARD,
) -> CorpusDocument:
    return CorpusDocument(
        text=text,
        source=source,
        url=url,  # type: ignore[arg-type]
        fetched_at=STAMP,
        lang="ca",
        topic=topic or [],
        license=license,
        registre=registre,
        speaker=speaker,
        legal=legal,
    )


LEGAL_DOC = doc(
    "Constitució del Principat d'Andorra — Article 5\n\nLa Declaració Universal dels Drets "
    "Humans és vigent a Andorra.",
    source=Source.JURIDIC,
    url="https://www.portaljuridicandorra.ad/constitucio",
    legal=Legal(rang=Rang.CONSTITUCIO, article="5", consolidacio_data=date(1993, 5, 4)),
)
SPEECH_DOC = doc(
    PROSE,
    source=Source.CONSELL_DIARI_SESSIONS,
    url="https://www.consellgeneral.ad/diari/1",
    speaker="Maria Font",
    registre=Registre.ANDORRA_PARLAT,
)
RESTRICTED_DOC = doc(
    PROSE + " Text de premsa.",
    source=Source.BOPA,
    url="https://www.bopa.ad/x",
    license=License.NO_REDISTRIBUTE,
)


@dataclass
class FakeHub:
    """Records the calls a real ``HfApi`` would have received."""

    created: list[dict[str, object]] = field(default_factory=list)
    uploads: list[dict[str, object]] = field(default_factory=list)

    def create_repo(self, repo_id: str, *, repo_type: str, private: bool, exist_ok: bool) -> object:
        self.created.append(
            {"repo_id": repo_id, "repo_type": repo_type, "private": private, "exist_ok": exist_ok}
        )
        return None

    def upload_folder(
        self, *, repo_id: str, folder_path: str, repo_type: str, commit_message: str
    ) -> object:
        self.uploads.append(
            {
                "repo_id": repo_id,
                "folder_path": folder_path,
                "repo_type": repo_type,
                "commit_message": commit_message,
            }
        )
        return None


# ─────────────────────────────────────────────────────────────
# The parquet schema
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_schema_is_explicit_and_versioned() -> None:
    schema = corpus_schema()
    assert schema.names == [
        "id",
        "text",
        "source",
        "url",
        "fetched_at",
        "lang",
        "topic",
        "license",
        "registre",
        "speaker",
        "legal",
    ]
    assert schema.metadata[b"maia_schema_version"] == SCHEMA_VERSION.encode()
    # Only the genuinely optional §3.1 fields are nullable.
    nullable = {name for name in schema.names if schema.field(name).nullable}
    assert nullable == {"speaker", "legal"}


@pytest.mark.unit
def test_a_corpus_without_legal_documents_gets_the_same_schema(tmp_path: Path) -> None:
    """Two drops must concatenate, which inference would not guarantee.

    Inferred schemas differ when a column is all-null: a corpus with no legal documents would
    type ``legal`` as null and refuse to concatenate with one that has them.
    """
    plain = tmp_path / "plain.parquet"
    mixed = tmp_path / "mixed.parquet"
    write_parquet([doc()], plain)
    write_parquet([doc(), LEGAL_DOC], mixed)
    assert pq.read_schema(plain) == pq.read_schema(mixed)


@pytest.mark.unit
def test_round_trip_preserves_every_field(tmp_path: Path) -> None:
    originals = [
        doc(topic=["cultura", "tradicions"]),
        LEGAL_DOC,
        SPEECH_DOC,
    ]
    path = tmp_path / "corpus.parquet"
    assert write_parquet(originals, path) == 3
    restored = read_parquet(path)
    assert restored == originals


@pytest.mark.unit
def test_round_trip_keeps_timezone_and_dates(tmp_path: Path) -> None:
    path = tmp_path / "corpus.parquet"
    write_parquet([LEGAL_DOC], path)
    restored = read_parquet(path)[0]
    assert restored.fetched_at == STAMP
    assert restored.fetched_at.tzinfo is not None
    assert restored.legal is not None
    assert restored.legal.consolidacio_data == date(1993, 5, 4)


@pytest.mark.unit
def test_round_trip_revalidates_the_id(tmp_path: Path) -> None:
    # read_parquet goes through the §3.1 validator, so a corrupted id would raise here.
    path = tmp_path / "corpus.parquet"
    write_parquet([doc()], path)
    assert read_parquet(path)[0].id == doc().id


# ─────────────────────────────────────────────────────────────
# Staging
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_stage_writes_one_parquet_per_source(tmp_path: Path) -> None:
    manifest = stage([doc(), LEGAL_DOC, SPEECH_DOC], tmp_path, repo_id="ericrisco/maia-corpus")
    assert set(manifest.files) == {
        f"{DATA_PREFIX}/govern.parquet",
        f"{DATA_PREFIX}/juridic.parquet",
        f"{DATA_PREFIX}/consell_diari_sessions.parquet",
    }
    assert all(v == 1 for v in manifest.files.values())
    for relative in manifest.files:
        assert (tmp_path / relative).is_file()


@pytest.mark.unit
def test_manifest_describes_the_drop(tmp_path: Path) -> None:
    manifest = stage(
        [doc(), doc(url="https://www.govern.ad/b"), LEGAL_DOC],
        tmp_path,
        repo_id="ericrisco/maia-corpus",
    )
    assert manifest.documents == 3
    assert manifest.private is True
    assert manifest.schema_version == SCHEMA_VERSION
    assert manifest.by_source == {"govern": 2, "juridic": 1}
    assert manifest.by_license == {"public-official": 3}
    assert manifest.no_redistribute == 0

    payload = json.loads((tmp_path / MANIFEST_NAME).read_text(encoding="utf-8"))
    assert payload["documents"] == 3
    assert payload["private"] is True
    assert payload["no_redistribute"] == 0


@pytest.mark.unit
def test_manifest_flags_restricted_documents(tmp_path: Path) -> None:
    manifest = stage([doc(), RESTRICTED_DOC], tmp_path, repo_id="ericrisco/maia-corpus")
    assert manifest.no_redistribute == 1
    assert "no-redistribute" in render(manifest)


@pytest.mark.unit
def test_staging_an_empty_corpus_is_refused(tmp_path: Path) -> None:
    # An empty commit would look like a successful upload while publishing nothing.
    with pytest.raises(ValueError, match="empty corpus"):
        stage([], tmp_path, repo_id="ericrisco/maia-corpus")


@pytest.mark.unit
def test_verify_staged_reads_everything_back(tmp_path: Path) -> None:
    manifest = stage([doc(), LEGAL_DOC, RESTRICTED_DOC], tmp_path, repo_id="x/y")
    report = verify_staged(tmp_path, manifest)
    assert report.total == 3
    assert report.valid == 3
    assert report.no_redistribute == 1
    assert report.by_source == {"govern": 1, "juridic": 1, "bopa": 1}


# ─────────────────────────────────────────────────────────────
# The compliance wall
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_restricted_lists_only_unpublishable_documents() -> None:
    assert restricted([doc(), LEGAL_DOC, RESTRICTED_DOC]) == [RESTRICTED_DOC]


@pytest.mark.unit
def test_a_public_repo_refuses_restricted_content(tmp_path: Path) -> None:
    """The wall between grounding-only and published.

    The corpus is *allowed* to carry no-redistribute text — the private drop exists so it can.
    Staging it for a public repo is what must be impossible.
    """
    with pytest.raises(RestrictedContentError, match="no-redistribute"):
        stage([doc(), RESTRICTED_DOC], tmp_path, repo_id="ericrisco/maia-corpus", private=False)


@pytest.mark.unit
def test_the_refusal_names_the_offending_sources(tmp_path: Path) -> None:
    with pytest.raises(RestrictedContentError, match="bopa"):
        stage([RESTRICTED_DOC], tmp_path, repo_id="x/y", private=False)


@pytest.mark.unit
def test_a_public_repo_is_allowed_when_everything_is_publishable(tmp_path: Path) -> None:
    manifest = stage([doc(), LEGAL_DOC], tmp_path, repo_id="x/y", private=False)
    assert manifest.private is False
    assert manifest.no_redistribute == 0
    assert "PUBLIC" in render(manifest)


@pytest.mark.unit
def test_nothing_is_written_when_staging_is_refused(tmp_path: Path) -> None:
    # The refusal must come before any file is created, or a later run could upload a folder
    # that still holds restricted parquet from the failed attempt.
    with pytest.raises(RestrictedContentError):
        stage([RESTRICTED_DOC], tmp_path, repo_id="x/y", private=False)
    assert list(tmp_path.iterdir()) == []


# ─────────────────────────────────────────────────────────────
# Upload
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_upload_creates_a_private_dataset_repo_and_commits(tmp_path: Path) -> None:
    hub = FakeHub()
    manifest = upload_corpus([doc(), LEGAL_DOC], hub, tmp_path, repo_id="ericrisco/maia-corpus")
    assert hub.created == [
        {
            "repo_id": "ericrisco/maia-corpus",
            "repo_type": "dataset",
            "private": True,
            "exist_ok": True,
        }
    ]
    assert len(hub.uploads) == 1
    upload = hub.uploads[0]
    assert upload["repo_id"] == "ericrisco/maia-corpus"
    assert upload["repo_type"] == "dataset"
    assert upload["folder_path"] == str(tmp_path)
    assert "2 documents" in str(upload["commit_message"])
    assert manifest.documents == 2


@pytest.mark.unit
def test_upload_is_private_by_default_and_public_must_be_asked_for(tmp_path: Path) -> None:
    hub = FakeHub()
    upload_corpus([doc()], hub, tmp_path / "a", repo_id="x/y")
    assert hub.created[0]["private"] is True
    upload_corpus([doc()], hub, tmp_path / "b", repo_id="x/y", private=False)
    assert hub.created[1]["private"] is False


@pytest.mark.unit
def test_upload_refuses_restricted_content_before_touching_the_hub(tmp_path: Path) -> None:
    hub = FakeHub()
    with pytest.raises(RestrictedContentError):
        upload_corpus([RESTRICTED_DOC], hub, tmp_path, repo_id="x/y", private=False)
    assert hub.created == []
    assert hub.uploads == []


@pytest.mark.unit
def test_a_custom_commit_message_is_used(tmp_path: Path) -> None:
    hub = FakeHub()
    upload_corpus([doc()], hub, tmp_path, repo_id="x/y", commit_message="F1 drop")
    assert hub.uploads[0]["commit_message"] == "F1 drop"


@pytest.mark.unit
def test_upload_fails_loudly_if_the_drop_does_not_round_trip(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Nothing is committed unless what was staged reads back intact.

    The guard exists to catch a bug in staging or in the parquet schema, so the only way to
    exercise it is to inject that disagreement: staging is stubbed to over-report its row
    count while writing a single document.
    """
    hub = FakeHub()

    def lying_stage(documents: object, staging_dir: Path, **kwargs: object) -> Manifest:
        write_parquet([doc()], staging_dir / DATA_PREFIX / "govern.parquet")
        return Manifest(
            repo_id="x/y",
            private=True,
            schema_version=SCHEMA_VERSION,
            documents=99,
            by_source={"govern": 99},
            by_license={"public-official": 99},
            files={f"{DATA_PREFIX}/govern.parquet": 99},
        )

    monkeypatch.setattr("maia.corpus.publish.stage", lying_stage)
    with pytest.raises(RuntimeError, match="does not round-trip"):
        upload_corpus([doc()], hub, tmp_path, repo_id="x/y")
    assert hub.created == []
    assert hub.uploads == []


@pytest.mark.unit
def test_hf_hub_builds_a_real_client_without_contacting_anything() -> None:
    # Constructing HfApi is offline; the token is only used when a call is made.
    hub = hf_hub(token="hf_not-a-real-token")
    assert hasattr(hub, "create_repo")
    assert hasattr(hub, "upload_folder")


# ─────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────


def _corpus_file(path: Path, documents: list[CorpusDocument]) -> Path:
    path.write_text("".join(f"{d.model_dump_json()}\n" for d in documents), encoding="utf-8")
    return path


@pytest.mark.unit
def test_cli_dry_run_stages_without_uploading(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    corpus = _corpus_file(tmp_path / "corpus.jsonl", [doc(), LEGAL_DOC])
    staging = tmp_path / "staging"
    assert (
        main(
            [
                str(corpus),
                "--repo-id",
                "ericrisco/maia-corpus",
                "--staging-dir",
                str(staging),
                "--dry-run",
            ]
        )
        == 0
    )
    out = capsys.readouterr().out
    assert "private" in out
    assert "dry run" in out
    assert (staging / DATA_PREFIX / "govern.parquet").is_file()
    assert (staging / MANIFEST_NAME).is_file()


@pytest.mark.unit
def test_cli_refuses_a_public_drop_with_restricted_content(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    corpus = _corpus_file(tmp_path / "corpus.jsonl", [doc(), RESTRICTED_DOC])
    exit_code = main(
        [
            str(corpus),
            "--repo-id",
            "ericrisco/maia-corpus",
            "--staging-dir",
            str(tmp_path / "staging"),
            "--public",
            "--dry-run",
        ]
    )
    assert exit_code == 1
    assert "no-redistribute" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_rejects_invalid_input_rather_than_uploading_it(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "corpus.jsonl"
    path.write_text(f"{doc().model_dump_json()}\n{{bad}}\n", encoding="utf-8")
    assert (
        main([str(path), "--repo-id", "x/y", "--staging-dir", str(tmp_path / "s"), "--dry-run"])
        == 1
    )
    assert "failed §3.1 validation" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_reports_a_missing_input(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert (
        main(
            [
                str(tmp_path / "absent.jsonl"),
                "--repo-id",
                "x/y",
                "--staging-dir",
                str(tmp_path / "s"),
                "--dry-run",
            ]
        )
        == 1
    )
    assert "no such file" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_refuses_an_empty_corpus(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "empty.jsonl"
    path.write_text("\n\n", encoding="utf-8")
    assert (
        main([str(path), "--repo-id", "x/y", "--staging-dir", str(tmp_path / "s"), "--dry-run"])
        == 1
    )
    assert "empty corpus" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_live_path_uploads_through_the_injected_hub(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    # The only part of the live path that needs HF_TOKEN + network is hf_hub(); swapping it
    # exercises everything else the real command would do.
    hub = FakeHub()
    monkeypatch.setattr("maia.corpus.publish.hf_hub", lambda: hub)
    corpus = _corpus_file(tmp_path / "corpus.jsonl", [doc(), LEGAL_DOC])
    staging = tmp_path / "staging"
    exit_code = main(
        [str(corpus), "--repo-id", "ericrisco/maia-corpus", "--staging-dir", str(staging)]
    )
    assert exit_code == 0
    out = capsys.readouterr().out
    assert "dry run" not in out
    assert "ericrisco/maia-corpus (private)" in out
    assert hub.created[0]["private"] is True
    assert hub.uploads[0]["folder_path"] == str(staging)
