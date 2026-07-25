"""Tests for publishing the dataset to Hugging Face (PLAN M2.11)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from uuid import UUID, uuid5

import pytest

from maia.corpus.publish import RestrictedContentError, StaleStagingError
from maia.schemas import (
    CorpusDocument,
    DatasetExample,
    ExampleType,
    License,
    Registre,
    Source,
    Split,
    compute_id,
)
from maia.synth.distribution import profile
from maia.synth.publish import (
    DATASET_LICENSE,
    SPLIT_FILES,
    DatasetManifest,
    FrozenTestSplitError,
    dataset_card,
    licences_of,
    publishable,
    read_corpus,
    read_dataset,
    render,
    restricted,
    stage,
    untraceable,
    upload_dataset,
    verify_staged,
)
from maia.synth.validate import split_digest

_NAMESPACE = UUID("6ba7b817-9dad-11d1-80b4-00c04fd430c8")


def document(index: int, licence: License = License.PUBLIC_OFFICIAL) -> CorpusDocument:
    text = f"El comú de la parròquia gestiona el territori. Passatge {index} de {licence.value}."
    return CorpusDocument.model_validate(
        {
            "id": compute_id(text),
            "text": text,
            "source": Source.JURIDIC.value,
            "url": f"https://www.portaljuridicandorra.ad/{index}",
            "fetched_at": "2026-07-25T10:00:00+00:00",
            "license": licence.value,
            "registre": Registre.ESTANDARD.value,
            "lang": "ca",
        }
    )


PUBLIC = [document(index) for index in range(4)]
PRIVATE = document(99, License.NO_REDISTRIBUTE)
CORPUS = {doc.id: doc for doc in [*PUBLIC, PRIVATE]}
ABSENT = document(1_000)


def example(
    tag: str,
    *,
    kind: ExampleType = ExampleType.QA,
    split: Split = Split.TRAIN,
    grounding: list[CorpusDocument] | None = None,
) -> DatasetExample:
    cites = kind.requires_grounding()
    return DatasetExample.model_validate(
        {
            "id": str(uuid5(_NAMESPACE, tag)),
            "messages": [
                {"role": "user", "content": f"Què fa el comú? ({tag})"},
                {"role": "assistant", "content": "Gestiona el territori de la parròquia."},
            ],
            "type": kind.value,
            "topic": "institucions/comuns" if cites else "general_ca/instrucat",
            "grounding_ids": sorted({d.id for d in (grounding or PUBLIC[:1])}) if cites else [],
            "generator": "claude-opus-5",
            "judge_score": 0.9 if cites else 0.0,
            "split": split.value,
        }
    )


def dataset(size: int = 100) -> list[DatasetExample]:
    """§3.2-compliant type shares and 90/5/5 splits, all grounded in public text."""
    examples: list[DatasetExample] = []
    for index in range(size):
        position = index % 100
        if position < 8:
            kind = ExampleType.NO_HO_SE
        elif position < 25:
            kind = ExampleType.GENERAL_CA
        else:
            kind = ExampleType.QA
        if position < 90:
            split = Split.TRAIN
        elif position < 95:
            split = Split.VAL
        else:
            split = Split.TEST
        examples.append(
            example(f"e{index}", kind=kind, split=split, grounding=[PUBLIC[index % len(PUBLIC)]])
        )
    return examples


@dataclass
class FakeHub:
    """The injected Hugging Face client — records what it was asked to do."""

    created: list[tuple[str, bool]] = field(default_factory=list)
    uploaded: list[tuple[str, str]] = field(default_factory=list)

    def create_repo(self, repo_id: str, *, repo_type: str, private: bool, exist_ok: bool) -> object:
        self.created.append((repo_id, private))
        return None

    def upload_folder(
        self, *, repo_id: str, folder_path: str, repo_type: str, commit_message: str
    ) -> object:
        self.uploaded.append((repo_id, folder_path))
        return None


# ─────────────────────────────────────────────────────────────
# Provenance is licence
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_an_examples_licences_are_those_of_its_grounding() -> None:
    """A §3.2 example carries no licence of its own."""
    found, missing = licences_of(example("a", grounding=[PUBLIC[0], PRIVATE]), CORPUS)
    assert found == {License.PUBLIC_OFFICIAL.value, License.NO_REDISTRIBUTE.value}
    assert missing == []


@pytest.mark.unit
def test_an_example_grounded_in_restricted_text_is_restricted() -> None:
    """The generator answered *from* that passage, so the example derives from it."""
    grounded = example("bad", grounding=[PRIVATE])
    assert restricted([grounded], CORPUS) == [grounded]


@pytest.mark.unit
def test_one_restricted_passage_among_several_is_enough() -> None:
    mixed = example("mixed", grounding=[PUBLIC[0], PUBLIC[1], PRIVATE])
    assert restricted([mixed], CORPUS) == [mixed]


@pytest.mark.unit
def test_an_example_grounded_only_in_public_text_is_publishable() -> None:
    assert restricted([example("ok", grounding=[PUBLIC[0]])], CORPUS) == []


@pytest.mark.unit
def test_an_ungrounded_example_cites_nothing_and_is_publishable() -> None:
    assert restricted([example("gc", kind=ExampleType.GENERAL_CA)], CORPUS) == []
    assert untraceable([example("gc", kind=ExampleType.GENERAL_CA)], CORPUS) == []


@pytest.mark.unit
def test_an_example_citing_an_absent_passage_is_untraceable() -> None:
    """ "We could not check" is not a licence."""
    orphan = example("orphan", grounding=[ABSENT])
    assert untraceable([orphan], CORPUS) == [orphan]
    assert restricted([orphan], CORPUS) == []


@pytest.mark.unit
def test_restricted_and_untraceable_are_counted_separately() -> None:
    """One is a data-cleaning problem, the other is a verification failure."""
    examples = [
        example("ok", grounding=[PUBLIC[0]]),
        example("bad", grounding=[PRIVATE]),
        example("orphan", grounding=[ABSENT]),
    ]
    kept, blocked, unknown = publishable(examples, CORPUS, private=False)
    assert [item.id for item in kept] == [examples[0].id]
    assert [item.id for item in blocked] == [examples[1].id]
    assert [item.id for item in unknown] == [examples[2].id]


@pytest.mark.unit
def test_a_private_drop_publishes_everything() -> None:
    """The restricted text is exactly what makes the private drop useful for RAG."""
    examples = [example("ok"), example("bad", grounding=[PRIVATE])]
    kept, blocked, unknown = publishable(examples, CORPUS, private=True)
    assert len(kept) == 2
    assert blocked == [] and unknown == []


@pytest.mark.unit
def test_a_public_drop_without_the_corpus_is_refused() -> None:
    """Provenance cannot be established, and a public upload cannot be taken back."""
    with pytest.raises(RestrictedContentError, match="needs the corpus to establish provenance"):
        publishable([example("a")], None, private=False)


@pytest.mark.unit
def test_a_private_drop_needs_no_corpus() -> None:
    kept, _, _ = publishable([example("a")], None, private=True)
    assert len(kept) == 1


# ─────────────────────────────────────────────────────────────
# The collision with the frozen test split
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_withholding_a_test_example_fails_the_drop() -> None:
    """Publishing a test set different from the frozen one breaks Phase 4 comparability.

    Resolving that is a decision — re-freeze, or re-run generation without those passages — not
    something a publish step should make on someone's behalf.
    """
    examples = [
        *dataset(20),
        example("restricted-test", split=Split.TEST, grounding=[PRIVATE]),
    ]
    frozen = split_digest(examples, Split.TEST)
    with pytest.raises(FrozenTestSplitError, match="would differ from the frozen one"):
        publishable(examples, CORPUS, private=False, frozen_test_digest=frozen)


@pytest.mark.unit
def test_a_test_split_that_changed_since_the_freeze_fails_the_drop() -> None:
    examples = dataset(100)
    with pytest.raises(FrozenTestSplitError, match=r"but .* was frozen"):
        publishable(examples, CORPUS, private=False, frozen_test_digest="0" * 64)


@pytest.mark.unit
def test_a_matching_freeze_lets_the_drop_through() -> None:
    examples = dataset(100)
    frozen = split_digest(examples, Split.TEST)
    kept, blocked, _ = publishable(examples, CORPUS, private=False, frozen_test_digest=frozen)
    assert len(kept) == 100
    assert blocked == []


@pytest.mark.unit
def test_without_a_freeze_no_test_claim_is_checked() -> None:
    examples = [*dataset(20), example("restricted-test", split=Split.TEST, grounding=[PRIVATE])]
    kept, blocked, _ = publishable(examples, CORPUS, private=False)
    assert len(blocked) == 1
    assert len(kept) == 20


# ─────────────────────────────────────────────────────────────
# Staging
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_staging_writes_one_file_per_split(tmp_path: Path) -> None:
    manifest = stage(dataset(100), tmp_path / "drop", repo_id="x/maia-dataset")
    for split, relative in SPLIT_FILES.items():
        assert (tmp_path / "drop" / relative).is_file()
        assert manifest.files[relative] == manifest.by_split[split.value]
    assert manifest.examples == 100
    assert (tmp_path / "drop" / "manifest.json").is_file()
    assert (tmp_path / "drop" / "README.md").is_file()


@pytest.mark.unit
def test_a_split_with_no_examples_writes_no_file(tmp_path: Path) -> None:
    manifest = stage([example("a")], tmp_path / "drop", repo_id="x/y")
    assert SPLIT_FILES[Split.TRAIN] in manifest.files
    assert SPLIT_FILES[Split.TEST] not in manifest.files
    assert not (tmp_path / "drop" / SPLIT_FILES[Split.TEST]).exists()


@pytest.mark.unit
def test_the_manifest_records_both_digests(tmp_path: Path) -> None:
    examples = dataset(100)
    manifest = stage(examples, tmp_path / "drop", repo_id="x/y")
    assert manifest.test_digest == split_digest(examples, Split.TEST)
    assert len(manifest.dataset_digest) == 64
    payload = json.loads((tmp_path / "drop" / "manifest.json").read_text(encoding="utf-8"))
    assert payload["test_digest"] == manifest.test_digest


@pytest.mark.unit
def test_a_stale_staging_directory_is_refused(tmp_path: Path) -> None:
    """The hub commits the whole folder, so a leftover private file would ride along (D-0016)."""
    drop = tmp_path / "drop"
    stage(dataset(20), drop, repo_id="x/y")
    with pytest.raises(StaleStagingError, match="already holds"):
        stage(dataset(20), drop, repo_id="x/y")


@pytest.mark.unit
def test_reusing_the_staging_directory_clears_it_first(tmp_path: Path) -> None:
    drop = tmp_path / "drop"
    stage(dataset(100), drop, repo_id="x/y")
    (drop / "data" / "leftover.jsonl").write_text("{}\n", encoding="utf-8")
    manifest = stage(dataset(100), drop, repo_id="x/y", reuse_dir=True)
    assert not (drop / "data" / "leftover.jsonl").exists()
    assert verify_staged(drop, manifest) == []


@pytest.mark.unit
def test_staging_excludes_restricted_examples_and_counts_them(tmp_path: Path) -> None:
    examples = [*dataset(100), example("bad", grounding=[PRIVATE])]
    manifest = stage(examples, tmp_path / "drop", repo_id="x/y", private=False, corpus=CORPUS)
    assert manifest.examples == 100
    assert manifest.excluded_restricted == 1
    assert "no-redistribute" in render(manifest)


# ─────────────────────────────────────────────────────────────
# Verification of what was staged
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_clean_drop_verifies(tmp_path: Path) -> None:
    drop = tmp_path / "drop"
    manifest = stage(dataset(100), drop, repo_id="x/y")
    assert verify_staged(drop, manifest) == []


@pytest.mark.unit
def test_a_file_the_manifest_does_not_describe_is_a_problem(tmp_path: Path) -> None:
    """The hub commits the folder, not the manifest: an unaccounted file is unchecked."""
    drop = tmp_path / "drop"
    manifest = stage(dataset(100), drop, repo_id="x/y")
    (drop / "data" / "extra.jsonl").write_text(
        f"{example('sneaky').model_dump_json()}\n", encoding="utf-8"
    )
    problems = verify_staged(drop, manifest)
    assert any("not in the manifest" in problem for problem in problems)


@pytest.mark.unit
def test_a_missing_staged_file_is_a_problem(tmp_path: Path) -> None:
    drop = tmp_path / "drop"
    manifest = stage(dataset(100), drop, repo_id="x/y")
    (drop / SPLIT_FILES[Split.TEST]).unlink()
    problems = verify_staged(drop, manifest)
    assert any("staged file is missing" in problem for problem in problems)


@pytest.mark.unit
def test_a_truncated_staged_file_is_a_problem(tmp_path: Path) -> None:
    drop = tmp_path / "drop"
    manifest = stage(dataset(100), drop, repo_id="x/y")
    path = drop / SPLIT_FILES[Split.TRAIN]
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text("\n".join(lines[:-5]) + "\n", encoding="utf-8")
    problems = verify_staged(drop, manifest)
    assert any("file holds" in problem for problem in problems)
    assert any("staged files hold" in problem for problem in problems)


# ─────────────────────────────────────────────────────────────
# §3.2 re-checked on what is published
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_compliant_drop_has_no_type_violations(tmp_path: Path) -> None:
    manifest = stage(dataset(100), tmp_path / "drop", repo_id="x/y")
    assert manifest.type_violations == []


@pytest.mark.unit
def test_withholding_examples_can_break_3_2_and_that_is_reported(tmp_path: Path) -> None:
    """The shares validated before exclusion are not the shares going out."""
    # Every general_ca example is grounded in restricted text, so the mix vanishes from the drop.
    examples = [example(f"qa{index}", grounding=[PUBLIC[0]]) for index in range(80)]
    examples += [
        example(f"gc{index}", kind=ExampleType.GENERAL_CA).model_copy(
            update={"grounding_ids": [PRIVATE.id], "type": ExampleType.QA}
        )
        for index in range(20)
    ]
    manifest = stage(examples, tmp_path / "drop", repo_id="x/y", private=False, corpus=CORPUS)
    assert manifest.type_violations
    assert "✗" in render(manifest)


@pytest.mark.unit
def test_a_public_upload_breaking_3_2_is_refused(tmp_path: Path) -> None:
    """Publishing a dataset the project's own schema calls invalid is not a caveat."""
    examples = [example(f"qa{index}", grounding=[PUBLIC[0]]) for index in range(50)]
    hub = FakeHub()
    with pytest.raises(RestrictedContentError, match=r"breaks §3\.2"):
        upload_dataset(
            examples,
            hub,
            tmp_path / "drop",
            repo_id="x/y",
            private=False,
            corpus=CORPUS,
        )
    assert hub.uploaded == []


@pytest.mark.unit
def test_a_private_upload_breaking_3_2_still_goes_through(tmp_path: Path) -> None:
    """A private drop is a working artifact, not a publication."""
    examples = [example(f"qa{index}", grounding=[PUBLIC[0]]) for index in range(50)]
    hub = FakeHub()
    manifest = upload_dataset(examples, hub, tmp_path / "drop", repo_id="x/y", private=True)
    assert manifest.type_violations
    assert hub.uploaded


# ─────────────────────────────────────────────────────────────
# The dataset card
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_card_has_hub_front_matter(tmp_path: Path) -> None:
    stage(dataset(100), tmp_path / "drop", repo_id="x/maia-dataset")
    card = (tmp_path / "drop" / "README.md").read_text(encoding="utf-8")
    assert card.startswith("---\n")
    assert f"license: {DATASET_LICENSE}" in card
    assert "  - ca" in card
    assert "size_categories:" in card
    for split in ("train", "validation", "test"):
        assert f"- split: {split}" in card


@pytest.mark.unit
def test_the_card_carries_the_distribution_report(tmp_path: Path) -> None:
    """Writing a second description would let the two disagree."""
    stage(dataset(100), tmp_path / "drop", repo_id="x/y")
    card = (tmp_path / "drop" / "README.md").read_text(encoding="utf-8")
    assert "# Dataset distribution" in card
    assert "## Types" in card


@pytest.mark.unit
def test_the_card_states_the_limits_that_matter() -> None:
    manifest = DatasetManifest(
        repo_id="x/y",
        private=False,
        schema_version="3.2",
        examples=100,
        by_split={"train": 90, "val": 5, "test": 5},
        by_type={"qa": 75, "no_ho_se": 8, "general_ca": 17},
        test_digest="d" * 64,
        dataset_digest="e" * 64,
    )
    card = dataset_card(manifest, profile([]))
    assert "register and lexicon only" in card
    assert "never to imitate an identifiable person" in card
    assert "`no_ho_se` examples deliberately teach the model to decline" in card
    assert "test split is frozen" in card
    assert "d" * 64 in card


@pytest.mark.unit
def test_the_card_declares_what_was_withheld() -> None:
    manifest = DatasetManifest(
        repo_id="x/y",
        private=False,
        schema_version="3.2",
        examples=100,
        by_split={"train": 100},
        by_type={"qa": 100},
        test_digest="",
        dataset_digest="",
        excluded_restricted=7,
        excluded_untraceable=2,
    )
    card = dataset_card(manifest, profile([]))
    assert "7 example(s) were **withheld**" in card
    assert "2 because their grounding could not be verified" in card
    assert "subset of the one used internally" in card


@pytest.mark.unit
@pytest.mark.parametrize(
    ("count", "label"),
    [(500, "n<1K"), (5_000, "1K<n<10K"), (12_000, "10K<n<100K"), (250_000, "100K<n<1M")],
)
def test_the_size_category_matches_the_hub_buckets(count: int, label: str) -> None:
    manifest = DatasetManifest(
        repo_id="x/y",
        private=True,
        schema_version="3.2",
        examples=count,
        by_split={"train": count},
        by_type={"qa": count},
        test_digest="",
        dataset_digest="",
    )
    card = dataset_card(manifest, profile([]))
    assert f"  - {label}" in card


# ─────────────────────────────────────────────────────────────
# Uploading
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_private_upload_creates_the_repo_and_commits(tmp_path: Path) -> None:
    hub = FakeHub()
    manifest = upload_dataset(dataset(100), hub, tmp_path / "drop", repo_id="x/y")
    assert hub.created == [("x/y", True)]
    assert hub.uploaded == [("x/y", str(tmp_path / "drop"))]
    assert manifest.private


@pytest.mark.unit
def test_a_public_upload_needs_the_corpus(tmp_path: Path) -> None:
    hub = FakeHub()
    with pytest.raises(RestrictedContentError):
        upload_dataset(dataset(100), hub, tmp_path / "drop", repo_id="x/y", private=False)
    assert hub.created == []


@pytest.mark.unit
def test_a_public_upload_with_clean_provenance_goes_through(tmp_path: Path) -> None:
    hub = FakeHub()
    examples = dataset(100)
    manifest = upload_dataset(
        examples,
        hub,
        tmp_path / "drop",
        repo_id="x/y",
        private=False,
        corpus=CORPUS,
        frozen_test_digest=split_digest(examples, Split.TEST),
    )
    assert hub.created == [("x/y", False)]
    assert not manifest.private
    assert manifest.excluded_restricted == 0


@pytest.mark.unit
def test_an_upload_that_does_not_verify_never_reaches_the_hub(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    hub = FakeHub()
    monkeypatch.setattr(
        "maia.synth.publish.verify_staged", lambda directory, manifest: ["something is wrong"]
    )
    with pytest.raises(RuntimeError, match="does not verify"):
        upload_dataset(dataset(100), hub, tmp_path / "drop", repo_id="x/y")
    assert hub.uploaded == []


# ─────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────


def write_dataset(path: Path, examples: list[DatasetExample]) -> Path:
    path.write_text("".join(f"{e.model_dump_json()}\n" for e in examples), encoding="utf-8")
    return path


def write_corpus(path: Path) -> Path:
    path.write_text("".join(f"{d.model_dump_json()}\n" for d in CORPUS.values()), encoding="utf-8")
    return path


def write_freeze(path: Path, examples: list[DatasetExample]) -> Path:
    test = sorted(str(e.id) for e in examples if e.split is Split.TEST)
    path.write_text(
        json.dumps(
            {
                "version": "1",
                "split": "test",
                "count": len(test),
                "digest": split_digest(examples, Split.TEST),
                "ids": test,
            }
        ),
        encoding="utf-8",
    )
    return path


@pytest.mark.unit
def test_cli_dry_run_stages_without_uploading(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from maia.synth.publish import main

    source = write_dataset(tmp_path / "dataset.jsonl", dataset(100))
    assert (
        main(
            [
                str(source),
                "--repo-id",
                "x/y",
                "--staging-dir",
                str(tmp_path / "drop"),
                "--dry-run",
            ]
        )
        == 0
    )
    printed = capsys.readouterr().out
    assert "nothing uploaded" in printed
    assert "private" in printed


@pytest.mark.unit
def test_cli_public_dry_run_checks_provenance_and_the_freeze(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from maia.synth.publish import main

    examples = dataset(100)
    source = write_dataset(tmp_path / "dataset.jsonl", examples)
    corpus = write_corpus(tmp_path / "corpus.jsonl")
    freeze = write_freeze(tmp_path / "freeze.json", examples)
    assert (
        main(
            [
                str(source),
                "--repo-id",
                "x/y",
                "--staging-dir",
                str(tmp_path / "drop"),
                "--corpus",
                str(corpus),
                "--freeze",
                str(freeze),
                "--public",
                "--dry-run",
            ]
        )
        == 0
    )
    assert "PUBLIC" in capsys.readouterr().out


@pytest.mark.unit
def test_cli_refuses_a_public_drop_without_the_corpus(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from maia.synth.publish import main

    source = write_dataset(tmp_path / "dataset.jsonl", dataset(100))
    assert (
        main(
            [
                str(source),
                "--repo-id",
                "x/y",
                "--staging-dir",
                str(tmp_path / "d"),
                "--public",
                "--dry-run",
            ]
        )
        == 1
    )
    assert "needs the corpus" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_refuses_when_the_freeze_would_change(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from maia.synth.publish import main

    examples = [*dataset(20), example("bad-test", split=Split.TEST, grounding=[PRIVATE])]
    source = write_dataset(tmp_path / "dataset.jsonl", examples)
    corpus = write_corpus(tmp_path / "corpus.jsonl")
    freeze = write_freeze(tmp_path / "freeze.json", examples)
    assert (
        main(
            [
                str(source),
                "--repo-id",
                "x/y",
                "--staging-dir",
                str(tmp_path / "d"),
                "--corpus",
                str(corpus),
                "--freeze",
                str(freeze),
                "--public",
                "--dry-run",
            ]
        )
        == 1
    )
    assert "differ from the frozen one" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_reports_a_missing_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    from maia.synth.publish import main

    assert main([str(tmp_path / "absent.jsonl"), "--repo-id", "x/y"]) == 1
    assert "no such file" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_refuses_a_stale_staging_dir(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from maia.synth.publish import main

    source = write_dataset(tmp_path / "dataset.jsonl", dataset(100))
    drop = tmp_path / "drop"
    args = [str(source), "--repo-id", "x/y", "--staging-dir", str(drop), "--dry-run"]
    assert main(args) == 0
    assert main(args) == 1
    assert "already holds" in capsys.readouterr().err
    assert main([*args, "--reuse-staging-dir"]) == 0


@pytest.mark.unit
def test_cli_uploads_through_the_injected_hub(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """The Hub session is blocked-by-resource, so the seam is patched — not the logic."""
    from maia.synth.publish import main

    hub = FakeHub()
    monkeypatch.setattr("maia.synth.publish.hf_hub", lambda *a, **k: hub)
    source = write_dataset(tmp_path / "dataset.jsonl", dataset(100))
    assert main([str(source), "--repo-id", "x/y", "--staging-dir", str(tmp_path / "drop")]) == 0
    assert hub.uploaded
    assert "nothing uploaded" not in capsys.readouterr().out


@pytest.mark.unit
def test_reading_a_dataset_and_corpus_round_trips(tmp_path: Path) -> None:
    source = write_dataset(tmp_path / "dataset.jsonl", dataset(10))
    corpus = write_corpus(tmp_path / "corpus.jsonl")
    assert len(read_dataset(source)) == 10
    assert set(read_corpus([corpus])) == set(CORPUS)


@pytest.mark.unit
def test_the_summary_names_untraceable_examples_separately(tmp_path: Path) -> None:
    """ "We cannot show it is clean" reads differently from "we know it is restricted"."""
    examples = [*dataset(100), example("orphan", grounding=[ABSENT])]
    manifest = stage(examples, tmp_path / "drop", repo_id="x/y", private=False, corpus=CORPUS)
    assert manifest.excluded_untraceable == 1
    assert "provenance unverifiable" in render(manifest)


@pytest.mark.unit
def test_cli_reports_a_staged_drop_that_does_not_verify(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    from maia.synth.publish import main

    source = write_dataset(tmp_path / "dataset.jsonl", dataset(100))
    monkeypatch.setattr(
        "maia.synth.publish.verify_staged", lambda directory, manifest: ["data/train.jsonl: bad"]
    )
    assert (
        main([str(source), "--repo-id", "x/y", "--staging-dir", str(tmp_path / "d"), "--dry-run"])
        == 1
    )
    assert "does not verify" in capsys.readouterr().err
