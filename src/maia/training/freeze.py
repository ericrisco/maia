"""Freezing the candidate — PLAN M3.07, and the DoD-F3 gate.

*"≥1 checkpoint beating base on AndBench-val, reproducible YAML, linked W&B run, cost recorded.
``maia-12b-cand1`` exists. Validated by Tech Lead (reproducibility) + PO (quality)."*

DoD-F3 lists four requirements and they are not decoration: three of them exist so that the fourth —
the score — can be **believed later**. A checkpoint that beats the base is worth nothing in six
months if nobody can say which config produced it, which data it saw, or what it cost. So freezing
is a gate, and :func:`freeze` refuses to produce a candidate with any of the four missing.

The requirement the plan does not spell out but every one of them depends on: **which dataset**. A
config plus a seed reproduces a run only against the same data, and the dataset is the thing most
likely to have moved on — M2.07 appends, M2.05 filters, M2.08 re-splits. So the candidate keeps
the **dataset digest** (M2.10's, over the whole file) alongside the config digest, and
:func:`verify_reproducible` can later say *this candidate was trained on data that no longer exists*
rather than leaving someone to discover it by getting different numbers.

Publication follows the plan's *"final variants published as branches of one HF repo"*: one model
repo, one **revision** per candidate, so `cand1` and `cand2` are comparable and neither overwrites
the other. The Hub client is **blocked-by-resource**; :class:`ModelHub` is the seam.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from maia.training.config import TrainingConfig
from maia.training.iteration import CLEAR_MARGIN, beats

#: Files a LoRA adapter checkpoint must contain to be loadable. A directory missing either is not a
#: checkpoint, however much else it holds.
REQUIRED_FILES = ("adapter_config.json", "adapter_model.safetensors")

#: The model repo every candidate is a revision of.
DEFAULT_REPO = "ericrisco/maia-12b"


class NotFrozenError(RuntimeError):
    """Raised when a candidate is missing something DoD-F3 requires."""


class ModelHub(Protocol):
    """The slice of ``huggingface_hub.HfApi`` used here. Blocked-by-resource."""

    def create_repo(self, repo_id: str, *, repo_type: str, private: bool, exist_ok: bool) -> object:
        """Create (or accept the existence of) a model repo."""

    def create_branch(self, *, repo_id: str, branch: str, repo_type: str, exist_ok: bool) -> object:
        """Create the revision this candidate is published as."""

    def upload_folder(
        self,
        *,
        repo_id: str,
        folder_path: str,
        repo_type: str,
        revision: str,
        commit_message: str,
    ) -> object:
        """Commit the adapter into a revision."""


def digest_directory(path: Path) -> str:
    """A digest over a checkpoint's contents.

    Over the **files**, sorted by relative path, rather than over a manifest someone wrote: the
    point is to detect that the weights changed, and a manifest can be edited to say they did not.
    """
    hasher = hashlib.sha256()
    for file in sorted(item for item in path.rglob("*") if item.is_file()):
        hasher.update(str(file.relative_to(path)).encode("utf-8"))
        hasher.update(b"\0")
        hasher.update(file.read_bytes())
    return hasher.hexdigest()


def config_digest(config: TrainingConfig) -> str:
    """A digest of the config, so the YAML can be shown to be the one that ran."""
    return hashlib.sha256(config.to_yaml().encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Candidate:
    """One frozen candidate and its DoD-F3 evidence."""

    name: str
    config: TrainingConfig
    checkpoint: Path
    score: float
    base_score: float
    dataset_digest: str
    wandb_url: str
    cost_eur: float
    epoch: int = 0
    #: The checkpoint's digest **at the moment of freezing**. Captured rather than recomputed on
    #: demand: a property that re-reads the files can never detect that they changed, which would
    #: make the integrity check decorative.
    checkpoint_digest: str = ""

    @property
    def margin(self) -> float:
        """How far above the base this candidate scores."""
        return self.score - self.base_score

    def manifest(self) -> dict[str, object]:
        """Everything needed to believe the score later."""
        return {
            "name": self.name,
            "experiment": self.config.name,
            "base_model": self.config.base_model,
            "epoch": self.epoch,
            "score": self.score,
            "base_score": self.base_score,
            "margin": round(self.margin, 6),
            "dataset_digest": self.dataset_digest,
            "config_digest": config_digest(self.config),
            "checkpoint_digest": self.checkpoint_digest,
            "wandb_url": self.wandb_url,
            "cost_eur": round(self.cost_eur, 2),
            "config": json.loads(self.config.model_dump_json()),
        }

    def to_json(self) -> str:
        """The manifest, for committing beside the adapter."""
        return json.dumps(self.manifest(), ensure_ascii=False, indent=2)


def missing_requirements(
    config: TrainingConfig,
    checkpoint: Path,
    *,
    score: float,
    base_score: float,
    dataset_digest: str,
    wandb_url: str,
    cost_eur: float,
    margin: float = CLEAR_MARGIN,
) -> list[str]:
    """Everything DoD-F3 asks for that is not present.

    Each entry says what is missing **and why it is required**, because the temptation at this gate
    is to freeze anyway and fill the evidence in later — and later the run has been deleted from the
    GPU box.
    """
    problems: list[str] = []
    if not beats(score, base_score, margin=margin):
        problems.append(
            f"score {score:.3f} does not beat the base {base_score:.3f} by {margin:.3f}; DoD-F3 "
            "requires ≥1 checkpoint beating base clearly, and a smaller difference is noise"
        )
    if not checkpoint.is_dir():
        problems.append(f"checkpoint {checkpoint} is not a directory; there is nothing to freeze")
    else:
        for required in REQUIRED_FILES:
            if not (checkpoint / required).is_file():
                problems.append(
                    f"checkpoint is missing {required}; without it the adapter cannot be loaded, "
                    "whatever else the directory holds"
                )
    if not dataset_digest:
        problems.append(
            "no dataset digest; a config and a seed reproduce a run only against the same data, "
            "and the dataset is the thing most likely to have moved on"
        )
    if not wandb_url:
        problems.append(
            "no W&B run linked; DoD-F3 requires it, and the loss curve lives only there"
        )
    if cost_eur <= 0:
        problems.append(
            "no cost recorded; DoD-F3 requires it, and it is unrecoverable once the GPU is released"
        )
    return problems


def freeze(
    config: TrainingConfig,
    checkpoint: Path,
    *,
    name: str,
    score: float,
    base_score: float,
    dataset_digest: str,
    wandb_url: str,
    cost_eur: float,
    epoch: int = 0,
    margin: float = CLEAR_MARGIN,
) -> Candidate:
    """Freeze a candidate, or refuse.

    Raises:
        NotFrozenError: listing every DoD-F3 requirement that is missing. Freezing with the evidence
            "to be filled in later" is how a candidate ends up unreproducible: by later, the GPU box
            is gone.
    """
    problems = missing_requirements(
        config,
        checkpoint,
        score=score,
        base_score=base_score,
        dataset_digest=dataset_digest,
        wandb_url=wandb_url,
        cost_eur=cost_eur,
        margin=margin,
    )
    if problems:
        raise NotFrozenError(
            f"{name} does not meet DoD-F3:\n" + "\n".join(f"  - {problem}" for problem in problems)
        )
    return Candidate(
        name=name,
        config=config,
        checkpoint=checkpoint,
        score=score,
        base_score=base_score,
        dataset_digest=dataset_digest,
        wandb_url=wandb_url,
        cost_eur=cost_eur,
        epoch=epoch,
        checkpoint_digest=digest_directory(checkpoint),
    )


def verify_reproducible(
    candidate: Candidate, *, config: TrainingConfig, dataset_digest: str
) -> list[str]:
    """Check a frozen candidate against the config and data available **now**.

    The question this answers is the one asked six months later: *can this run be repeated?* A
    mismatch is reported rather than raised, because the answer is usually "no, and here is what
    changed", which is information rather than an error.
    """
    problems: list[str] = []
    if config_digest(config) != config_digest(candidate.config):
        problems.append(
            f"the config has changed since {candidate.name} was frozen; re-running it would not "
            "reproduce the candidate"
        )
    if dataset_digest != candidate.dataset_digest:
        problems.append(
            f"{candidate.name} was trained on dataset {candidate.dataset_digest[:16]}… but the "
            f"dataset now digests to {dataset_digest[:16]}… — the training data no longer exists "
            "in the form that produced this model"
        )
    if (
        candidate.checkpoint_digest
        and candidate.checkpoint.is_dir()
        and digest_directory(candidate.checkpoint) != candidate.checkpoint_digest
    ):
        problems.append(
            f"the checkpoint at {candidate.checkpoint} has changed on disk since it was frozen"
        )
    return problems


def branch_for(candidate: Candidate) -> str:
    """The Hub revision this candidate is published as.

    One repo, one revision per candidate — the plan's *"final variants published as branches of one
    HF repo"* — so `cand1` and `cand2` stay comparable and neither overwrites the other.
    """
    return candidate.name


def stage(candidate: Candidate, staging_dir: Path) -> Path:
    """Copy the adapter and write the manifest beside it.

    Raises:
        NotFrozenError: if the staging directory already holds a different candidate. The hub
            commits the whole folder, so a leftover adapter would be published under this
            candidate's name — the D-0016 finding, in a third shape.
    """
    staging_dir.mkdir(parents=True, exist_ok=True)
    existing = sorted(item for item in staging_dir.iterdir() if item.name != "candidate.json")
    stale = [
        item
        for item in existing
        if item.name not in {file.name for file in candidate.checkpoint.iterdir()}
    ]
    if stale:
        raise NotFrozenError(
            f"{staging_dir} already holds {stale[0].name} from another candidate; the hub commits "
            "the whole folder, so it would be published under this candidate's name"
        )
    for file in sorted(item for item in candidate.checkpoint.iterdir() if item.is_file()):
        (staging_dir / file.name).write_bytes(file.read_bytes())
    (staging_dir / "candidate.json").write_text(candidate.to_json(), encoding="utf-8")
    return staging_dir


def publish(
    candidate: Candidate,
    hub: ModelHub,
    staging_dir: Path,
    *,
    repo_id: str = DEFAULT_REPO,
    private: bool = True,
) -> str:
    """Publish a frozen candidate as a revision of the model repo. Returns the revision.

    Private by default, as everywhere else in this project: a public model is a decision, not a
    side effect of freezing one.
    """
    stage(candidate, staging_dir)
    revision = branch_for(candidate)
    hub.create_repo(repo_id, repo_type="model", private=private, exist_ok=True)
    hub.create_branch(repo_id=repo_id, branch=revision, repo_type="model", exist_ok=True)
    hub.upload_folder(
        repo_id=repo_id,
        folder_path=str(staging_dir),
        repo_type="model",
        revision=revision,
        commit_message=(
            f"{candidate.name}: {candidate.config.name}, "
            f"{candidate.score:.3f} ({candidate.margin:+.3f} vs base)"
        ),
    )
    return revision


def render(candidate: Candidate, *, repo_id: str = DEFAULT_REPO) -> str:
    """Human-readable summary of a frozen candidate — the DoD-F3 evidence in one place."""
    return "\n".join(
        [
            f"{candidate.name} — {candidate.config.name}"
            + (f", epoch {candidate.epoch}" if candidate.epoch else ""),
            f"  score: {candidate.score:.3f} ({candidate.margin:+.3f} vs base "
            f"{candidate.base_score:.3f})",
            f"  dataset: {candidate.dataset_digest[:16]}…",
            f"  config:  {config_digest(candidate.config)[:16]}…",
            f"  W&B:     {candidate.wandb_url}",
            f"  cost:    €{candidate.cost_eur:.2f}",
            f"  publish: {repo_id}@{branch_for(candidate)}",
            "  DoD-F3 also needs Tech Lead sign-off (reproducibility) and PO sign-off (quality); "
            "neither is computable from here",
        ]
    )


def read_candidate(path: Path) -> Candidate:
    """Read a committed ``candidate.json`` back.

    Raises:
        ValueError: if the file is not a candidate manifest.
    """
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return Candidate(
            name=str(payload["name"]),
            config=TrainingConfig.model_validate(payload["config"]),
            checkpoint=path.parent,
            score=float(payload["score"]),
            base_score=float(payload["base_score"]),
            dataset_digest=str(payload["dataset_digest"]),
            wandb_url=str(payload["wandb_url"]),
            cost_eur=float(payload["cost_eur"]),
            epoch=int(payload.get("epoch", 0)),
            checkpoint_digest=str(payload.get("checkpoint_digest", "")),
        )
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        raise ValueError(f"{path}: not a candidate manifest ({error})") from error


def next_name(existing: Iterable[str], *, prefix: str = "cand") -> str:
    """The next candidate name — ``cand1``, ``cand2``, … — never reusing one.

    Reusing a name would make two different models answer to the same revision, and the older
    comparison would silently start referring to the newer weights.
    """
    used = {
        int(name[len(prefix) :])
        for name in existing
        if name.startswith(prefix) and name[len(prefix) :].isdigit()
    }
    return f"{prefix}{max(used, default=0) + 1}"


def existing_names(candidates: Sequence[Candidate]) -> list[str]:
    """The names already taken."""
    return [candidate.name for candidate in candidates]
