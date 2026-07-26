"""Tests for freezing the DoD-F3 candidate (PLAN M3.07)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import pytest

from maia.training.config import TrainingConfig
from maia.training.freeze import (
    DEFAULT_REPO,
    REQUIRED_FILES,
    Candidate,
    NotFrozenError,
    branch_for,
    config_digest,
    digest_directory,
    existing_names,
    freeze,
    missing_requirements,
    next_name,
    publish,
    read_candidate,
    render,
    stage,
    verify_reproducible,
)

DATASET = "d" * 64
WANDB = "https://wandb.ai/maia/exp/abc123"


def config(**overrides: object) -> TrainingConfig:
    return TrainingConfig.model_validate({"dataset_version": "v1", **overrides})


def checkpoint(tmp_path: Path, *, complete: bool = True, weights: bytes = b"weights") -> Path:
    directory = tmp_path / "checkpoint-epoch-2"
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "adapter_config.json").write_text('{"r": 16}', encoding="utf-8")
    if complete:
        (directory / "adapter_model.safetensors").write_bytes(weights)
    return directory


def frozen(tmp_path: Path, **overrides: object) -> Candidate:
    base = {
        "name": "cand1",
        "score": 0.62,
        "base_score": 0.50,
        "dataset_digest": DATASET,
        "wandb_url": WANDB,
        "cost_eur": 12.5,
        "epoch": 2,
    }
    return freeze(config(), checkpoint(tmp_path), **{**base, **overrides})  # type: ignore[arg-type]


@dataclass
class FakeHub:
    created: list[str] = field(default_factory=list)
    branches: list[str] = field(default_factory=list)
    uploads: list[tuple[str, str, str]] = field(default_factory=list)

    def create_repo(self, repo_id: str, *, repo_type: str, private: bool, exist_ok: bool) -> object:
        self.created.append(f"{repo_id}:{repo_type}:{'private' if private else 'PUBLIC'}")
        return None

    def create_branch(self, *, repo_id: str, branch: str, repo_type: str, exist_ok: bool) -> object:
        self.branches.append(branch)
        return None

    def upload_folder(
        self,
        *,
        repo_id: str,
        folder_path: str,
        repo_type: str,
        revision: str,
        commit_message: str,
    ) -> object:
        self.uploads.append((repo_id, revision, commit_message))
        return None


# ─────────────────────────────────────────────────────────────
# The gate — every DoD-F3 requirement
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_complete_candidate_freezes(tmp_path: Path) -> None:
    candidate = frozen(tmp_path)
    assert candidate.name == "cand1"
    assert candidate.margin == pytest.approx(0.12)


@pytest.mark.unit
def test_a_score_that_does_not_beat_the_base_clearly_is_refused(tmp_path: Path) -> None:
    """A smaller difference is noise, and DoD-F3's word is "clearly"."""
    with pytest.raises(NotFrozenError, match="does not beat the base"):
        frozen(tmp_path, score=0.505)


@pytest.mark.unit
def test_a_missing_dataset_digest_is_refused(tmp_path: Path) -> None:
    """A config and a seed reproduce a run only against the same data."""
    with pytest.raises(NotFrozenError, match="no dataset digest"):
        frozen(tmp_path, dataset_digest="")


@pytest.mark.unit
def test_a_missing_wandb_run_is_refused(tmp_path: Path) -> None:
    with pytest.raises(NotFrozenError, match="no W&B run linked"):
        frozen(tmp_path, wandb_url="")


@pytest.mark.unit
@pytest.mark.parametrize("cost", [0.0, -1.0])
def test_an_unrecorded_cost_is_refused(tmp_path: Path, cost: float) -> None:
    """Unrecoverable once the GPU is released."""
    with pytest.raises(NotFrozenError, match="no cost recorded"):
        frozen(tmp_path, cost_eur=cost)


@pytest.mark.unit
def test_a_checkpoint_that_is_not_a_directory_is_refused(tmp_path: Path) -> None:
    with pytest.raises(NotFrozenError, match="nothing to freeze"):
        freeze(
            config(),
            tmp_path / "absent",
            name="cand1",
            score=0.62,
            base_score=0.50,
            dataset_digest=DATASET,
            wandb_url=WANDB,
            cost_eur=10.0,
        )


@pytest.mark.unit
def test_a_checkpoint_missing_its_weights_is_refused(tmp_path: Path) -> None:
    """A directory missing the adapter is not a checkpoint, however much else it holds."""
    with pytest.raises(NotFrozenError, match=r"adapter_model\.safetensors"):
        freeze(
            config(),
            checkpoint(tmp_path, complete=False),
            name="cand1",
            score=0.62,
            base_score=0.50,
            dataset_digest=DATASET,
            wandb_url=WANDB,
            cost_eur=10.0,
        )


@pytest.mark.unit
def test_every_missing_requirement_is_listed_at_once(tmp_path: Path) -> None:
    """So the gate does not have to be run five times to learn five things."""
    problems = missing_requirements(
        config(),
        tmp_path / "absent",
        score=0.50,
        base_score=0.50,
        dataset_digest="",
        wandb_url="",
        cost_eur=0.0,
    )
    assert len(problems) == 5
    # Each entry names what is missing *and* why, so the gate does not read as a bare checklist.
    assert all(";" in problem for problem in problems)


@pytest.mark.unit
def test_the_required_files_are_what_makes_an_adapter_loadable() -> None:
    assert set(REQUIRED_FILES) == {"adapter_config.json", "adapter_model.safetensors"}


# ─────────────────────────────────────────────────────────────
# The manifest
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_manifest_carries_everything_needed_to_believe_the_score(tmp_path: Path) -> None:
    manifest = frozen(tmp_path).manifest()
    for key in (
        "score",
        "base_score",
        "margin",
        "dataset_digest",
        "config_digest",
        "checkpoint_digest",
        "wandb_url",
        "cost_eur",
        "config",
    ):
        assert key in manifest, key
    assert manifest["margin"] == pytest.approx(0.12)


@pytest.mark.unit
def test_the_checkpoint_digest_is_over_the_files_not_a_manifest(tmp_path: Path) -> None:
    """A manifest can be edited to say the weights did not change; the files cannot."""
    first = digest_directory(checkpoint(tmp_path / "a"))
    same = digest_directory(checkpoint(tmp_path / "b"))
    different = digest_directory(checkpoint(tmp_path / "c", weights=b"other weights"))
    assert first == same
    assert first != different


@pytest.mark.unit
def test_the_config_digest_changes_with_the_config() -> None:
    assert config_digest(config()) == config_digest(config())
    assert config_digest(config()) != config_digest(config(r=32, lora_alpha=64))


@pytest.mark.unit
def test_a_candidate_round_trips_through_its_manifest(tmp_path: Path) -> None:
    candidate = frozen(tmp_path)
    path = candidate.checkpoint / "candidate.json"
    path.write_text(candidate.to_json(), encoding="utf-8")
    restored = read_candidate(path)
    assert restored.name == candidate.name
    assert restored.config == candidate.config
    assert restored.score == candidate.score
    assert restored.dataset_digest == candidate.dataset_digest


@pytest.mark.unit
@pytest.mark.parametrize("payload", ["not json", "{}", '{"name": "x"}'])
def test_an_unreadable_manifest_is_refused(tmp_path: Path, payload: str) -> None:
    path = tmp_path / "candidate.json"
    path.write_text(payload, encoding="utf-8")
    with pytest.raises(ValueError, match="not a candidate manifest"):
        read_candidate(path)


# ─────────────────────────────────────────────────────────────
# Reproducibility, asked six months later
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_an_unchanged_world_reproduces(tmp_path: Path) -> None:
    candidate = frozen(tmp_path)
    assert verify_reproducible(candidate, config=config(), dataset_digest=DATASET) == []


@pytest.mark.unit
def test_a_changed_dataset_is_reported(tmp_path: Path) -> None:
    """The question asked later is "can this run be repeated?" — and usually the data moved."""
    candidate = frozen(tmp_path)
    problems = verify_reproducible(candidate, config=config(), dataset_digest="e" * 64)
    assert any("no longer exists in the form that produced this model" in p for p in problems)


@pytest.mark.unit
def test_a_changed_config_is_reported(tmp_path: Path) -> None:
    candidate = frozen(tmp_path)
    problems = verify_reproducible(
        candidate, config=config(learning_rate=1e-4), dataset_digest=DATASET
    )
    assert any("the config has changed" in p for p in problems)


@pytest.mark.unit
def test_changed_weights_on_disk_are_reported(tmp_path: Path) -> None:
    candidate = frozen(tmp_path)
    (candidate.checkpoint / "adapter_model.safetensors").write_bytes(b"tampered")
    problems = verify_reproducible(candidate, config=config(), dataset_digest=DATASET)
    assert any("has changed on disk" in p for p in problems)


@pytest.mark.unit
def test_a_missing_checkpoint_directory_makes_no_weight_claim(tmp_path: Path) -> None:
    candidate = frozen(tmp_path)
    gone = Candidate(
        name=candidate.name,
        config=candidate.config,
        checkpoint=tmp_path / "gone",
        score=candidate.score,
        base_score=candidate.base_score,
        dataset_digest=candidate.dataset_digest,
        wandb_url=candidate.wandb_url,
        cost_eur=candidate.cost_eur,
    )
    assert verify_reproducible(gone, config=config(), dataset_digest=DATASET) == []


# ─────────────────────────────────────────────────────────────
# Naming and publication
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_candidate_names_never_repeat() -> None:
    """Reusing one would make two models answer to the same revision."""
    assert next_name([]) == "cand1"
    assert next_name(["cand1"]) == "cand2"
    assert next_name(["cand1", "cand2", "cand5"]) == "cand6"
    assert next_name(["something-else"]) == "cand1"


@pytest.mark.unit
def test_existing_names_are_read_from_the_candidates(tmp_path: Path) -> None:
    candidate = frozen(tmp_path)
    assert existing_names([candidate]) == ["cand1"]
    assert next_name(existing_names([candidate])) == "cand2"


@pytest.mark.unit
def test_each_candidate_is_its_own_revision(tmp_path: Path) -> None:
    """One repo, one revision per candidate, so neither overwrites the other."""
    assert branch_for(frozen(tmp_path)) == "cand1"
    assert branch_for(frozen(tmp_path, name="cand2")) == "cand2"


@pytest.mark.unit
def test_staging_copies_the_adapter_and_writes_the_manifest(tmp_path: Path) -> None:
    candidate = frozen(tmp_path)
    staged = stage(candidate, tmp_path / "staging")
    assert (staged / "adapter_model.safetensors").read_bytes() == b"weights"
    assert json.loads((staged / "candidate.json").read_text(encoding="utf-8"))["name"] == "cand1"


@pytest.mark.unit
def test_a_staging_directory_holding_another_candidate_is_refused(tmp_path: Path) -> None:
    """The hub commits the whole folder, so a leftover adapter would be published as this one."""
    staging = tmp_path / "staging"
    staging.mkdir()
    (staging / "adapter_model_from_another_run.safetensors").write_bytes(b"stale")
    with pytest.raises(NotFrozenError, match="from another candidate"):
        stage(frozen(tmp_path), staging)


@pytest.mark.unit
def test_restaging_the_same_candidate_is_allowed(tmp_path: Path) -> None:
    candidate = frozen(tmp_path)
    stage(candidate, tmp_path / "staging")
    stage(candidate, tmp_path / "staging")


@pytest.mark.unit
def test_publishing_creates_the_repo_the_branch_and_commits(tmp_path: Path) -> None:
    hub = FakeHub()
    revision = publish(frozen(tmp_path), hub, tmp_path / "staging")
    assert revision == "cand1"
    assert hub.created == [f"{DEFAULT_REPO}:model:private"]
    assert hub.branches == ["cand1"]
    repo, rev, message = hub.uploads[0]
    assert (repo, rev) == (DEFAULT_REPO, "cand1")
    assert "0.620" in message and "+0.120" in message


@pytest.mark.unit
def test_publishing_is_private_by_default_and_public_is_a_choice(tmp_path: Path) -> None:
    hub = FakeHub()
    publish(frozen(tmp_path), hub, tmp_path / "staging", private=False)
    assert "PUBLIC" in hub.created[0]


@pytest.mark.unit
def test_the_repo_is_configurable(tmp_path: Path) -> None:
    hub = FakeHub()
    publish(frozen(tmp_path), hub, tmp_path / "staging", repo_id="x/y")
    assert hub.uploads[0][0] == "x/y"


# ─────────────────────────────────────────────────────────────
# The report
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_report_gathers_the_dod_evidence_in_one_place(tmp_path: Path) -> None:
    rendered = render(frozen(tmp_path))
    assert "cand1 — exp_v1_r16lr2e4e3, epoch 2" in rendered
    assert "0.620 (+0.120 vs base 0.500)" in rendered
    assert WANDB in rendered
    assert "€12.50" in rendered
    assert f"{DEFAULT_REPO}@cand1" in rendered


@pytest.mark.unit
def test_the_report_says_the_sign_offs_are_not_computable(tmp_path: Path) -> None:
    rendered = render(frozen(tmp_path))
    assert "Tech Lead sign-off" in rendered
    assert "PO sign-off" in rendered
    assert "neither is computable from here" in rendered


@pytest.mark.unit
def test_a_candidate_without_an_epoch_omits_it(tmp_path: Path) -> None:
    assert ", epoch" not in render(frozen(tmp_path, epoch=0))
