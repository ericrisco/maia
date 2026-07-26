"""Tests for running the training on Colab (PLAN M3, revised platform)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from maia.training.colab import (
    BF16_CAPABLE,
    COLAB_GPUS,
    GUARDED_NAMES,
    PLANNED_VRAM_GIB,
    NotebookPlan,
    build_notebook,
    check_no_hyperparameters,
    enterprise_command,
    fits,
    largest_batch,
    render_fit,
    resume_from,
    supports_dtype,
    usable,
    vram_estimate,
    write_notebook,
)
from maia.training.config import TrainingConfig


def config(**overrides: object) -> TrainingConfig:
    return TrainingConfig.model_validate({"dataset_version": "v1", **overrides})


def plan(**overrides: object) -> NotebookPlan:
    base = {
        "config_path": "configs/train/full-r16.yaml",
        "dataset_path": "data/dataset.jsonl",
        "gpu": "A100-40GB",
    }
    return NotebookPlan(**{**base, **overrides})  # type: ignore[arg-type]


# ─────────────────────────────────────────────────────────────
# VRAM — the plan assumed 80 GB and Colab has less
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_default_config_fits_every_colab_card() -> None:
    """The useful finding: 12B QLoRA is far lighter than the 80 GB the plan budgeted for."""
    estimate = vram_estimate(config())
    assert estimate < 16
    assert all(fits(config(), gpu) for gpu in COLAB_GPUS)
    assert PLANNED_VRAM_GIB == 80


@pytest.mark.unit
def test_vram_grows_with_batch_sequence_and_rank() -> None:
    base = vram_estimate(config())
    assert vram_estimate(config(per_device_batch_size=4, gradient_accumulation_steps=4)) > base
    assert vram_estimate(config(max_seq_len=8_192)) > base
    assert vram_estimate(config(r=64, lora_alpha=128)) > base


@pytest.mark.unit
def test_a_configuration_too_large_for_a_card_does_not_fit() -> None:
    huge = config(max_seq_len=32_768, per_device_batch_size=16, gradient_accumulation_steps=2)
    assert not fits(huge, "T4")
    assert "does not fit" in render_fit(huge, gpus=["T4"]) or "largest micro-batch" in render_fit(
        huge, gpus=["T4"]
    )


@pytest.mark.unit
def test_an_unknown_gpu_raises_rather_than_reporting_a_bad_fit() -> None:
    """A silent False would read as "too big" when the real problem is the question."""
    with pytest.raises(KeyError, match="unknown GPU"):
        fits(config(), "RTX-4090")
    with pytest.raises(KeyError, match="unknown GPU"):
        supports_dtype(config(), "RTX-4090")


@pytest.mark.unit
def test_the_largest_micro_batch_is_reported() -> None:
    """The honest response to a small card is to halve the micro-batch and double accumulation."""
    biggest = largest_batch(config(), "T4")
    assert biggest > 0
    assert largest_batch(config(), "A100-80GB") > biggest


@pytest.mark.unit
def test_a_configuration_that_fits_no_micro_batch_reports_zero() -> None:
    assert largest_batch(config(max_seq_len=32_768, r=128, lora_alpha=256), "T4") == 0


# ─────────────────────────────────────────────────────────────
# bf16 — what VRAM arithmetic alone would miss
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_t4_fits_the_run_and_still_cannot_run_it() -> None:
    """Fitting in VRAM is not the same as being able to run: bf16 needs Ampere or newer."""
    assert fits(config(), "T4")
    assert not supports_dtype(config(), "T4")
    assert not usable(config(), "T4")
    assert "T4" not in BF16_CAPABLE


@pytest.mark.unit
def test_an_ampere_card_runs_bf16() -> None:
    for gpu in ("L4", "A100-40GB", "A100-80GB"):
        assert supports_dtype(config(), gpu)
        assert usable(config(), gpu)


@pytest.mark.unit
def test_a_t4_is_usable_with_fp16() -> None:
    assert usable(config(compute_dtype="float16"), "T4")


@pytest.mark.unit
def test_the_report_explains_why_the_t4_is_rejected() -> None:
    rendered = render_fit(config(), gpus=["T4"])
    assert "✗ T4" in rendered
    assert "bf16 needs Ampere or newer" in rendered
    assert "learning rate was not chosen for it" in rendered


@pytest.mark.unit
def test_the_report_says_the_estimate_is_an_estimate() -> None:
    assert "estimated, not measured" in render_fit(config())


# ─────────────────────────────────────────────────────────────
# Resuming — on Colab this is not optional
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_no_output_directory_means_a_fresh_run(tmp_path: Path) -> None:
    assert resume_from(config(), tmp_path) is None


@pytest.mark.unit
def test_an_empty_output_directory_means_a_fresh_run(tmp_path: Path) -> None:
    (tmp_path / config().name).mkdir(parents=True)
    assert resume_from(config(), tmp_path) is None


@pytest.mark.unit
def test_the_newest_checkpoint_is_chosen_by_number_not_mtime(tmp_path: Path) -> None:
    """A resumed run rewrites older files, so mtime stops meaning "most trained"."""
    directory = tmp_path / config().name
    directory.mkdir(parents=True)
    for number in (1, 2, 10):
        (directory / f"checkpoint-{number}").mkdir()
    # Touch the oldest last, so mtime disagrees with training progress.
    (directory / "checkpoint-1").touch()
    found = resume_from(config(), tmp_path)
    assert found is not None
    assert found.name == "checkpoint-10"


@pytest.mark.unit
def test_both_checkpoint_naming_conventions_are_recognised(tmp_path: Path) -> None:
    """HF writes checkpoint-{step}; M3.03 names them checkpoint-epoch-{n}."""
    directory = tmp_path / config().name
    directory.mkdir(parents=True)
    (directory / "checkpoint-epoch-2").mkdir()
    found = resume_from(config(), tmp_path)
    assert found is not None and found.name == "checkpoint-epoch-2"


@pytest.mark.unit
def test_files_and_unrelated_directories_are_ignored(tmp_path: Path) -> None:
    directory = tmp_path / config().name
    directory.mkdir(parents=True)
    (directory / "checkpoint-3").mkdir()
    (directory / "checkpoint-99").write_text("a file, not a checkpoint", encoding="utf-8")
    (directory / "runs").mkdir()
    found = resume_from(config(), tmp_path)
    assert found is not None and found.name == "checkpoint-3"


# ─────────────────────────────────────────────────────────────
# The generated notebook
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_notebook_is_a_valid_ipynb_document() -> None:
    notebook = build_notebook(config(), plan())
    assert notebook["nbformat"] == 4
    cells = notebook["cells"]
    assert isinstance(cells, list) and cells
    assert all(cell["cell_type"] in {"code", "markdown"} for cell in cells)
    # Round-trips as JSON, which is what Colab will read.
    assert json.loads(json.dumps(notebook)) == notebook


@pytest.mark.unit
def test_the_notebook_reads_the_committed_yaml() -> None:
    """The decision this module exists for."""
    source = json.dumps(build_notebook(config(), plan()))
    assert (
        "load_config('configs/train/full-r16.yaml')"
        in source.replace('\\"', "'").replace('\\\\"', "'")
        or "configs/train/full-r16.yaml" in source
    )
    assert "load_config" in source


@pytest.mark.unit
def test_the_notebook_declares_no_hyperparameters() -> None:
    """A notebook that redeclares them lets the YAML and the cell that ran disagree."""
    assert check_no_hyperparameters(build_notebook(config(), plan())) == []


@pytest.mark.unit
@pytest.mark.parametrize("name", ["learning_rate", "r", "max_seq_len", "seed", "target_modules"])
def test_an_inlined_hyperparameter_is_caught(name: str) -> None:
    notebook = build_notebook(config(), plan())
    cells = notebook["cells"]
    assert isinstance(cells, list)
    cells.append({"cell_type": "code", "source": [f"{name} = 32\n"], "metadata": {}})
    offences = check_no_hyperparameters(notebook)
    assert offences
    assert name in offences[0]


@pytest.mark.unit
def test_a_comparison_is_not_an_assignment() -> None:
    """`r == 32` is a check, not a redefinition."""
    notebook = build_notebook(config(), plan())
    cells = notebook["cells"]
    assert isinstance(cells, list)
    cells.append({"cell_type": "code", "source": ["assert r == 32\n"], "metadata": {}})
    assert check_no_hyperparameters(notebook) == []


@pytest.mark.unit
def test_markdown_cells_are_not_scanned_for_assignments() -> None:
    notebook = build_notebook(config(), plan())
    cells = notebook["cells"]
    assert isinstance(cells, list)
    cells.append({"cell_type": "markdown", "source": ["learning_rate = 3e-4\n"], "metadata": {}})
    assert check_no_hyperparameters(notebook) == []


@pytest.mark.unit
def test_the_notebook_resumes_rather_than_starting_over() -> None:
    """Colab cuts sessions off before a 3-6 h run finishes."""
    source = json.dumps(build_notebook(config(), plan()))
    assert "resume_from(config)" in source
    assert "resume_from_checkpoint" in source


@pytest.mark.unit
def test_the_notebook_asserts_the_gpu_can_run_the_config() -> None:
    source = json.dumps(build_notebook(config(), plan()))
    assert "assert usable(config" in source


@pytest.mark.unit
def test_the_notebook_reports_the_gpu_it_actually_got() -> None:
    """Colab does not always allocate what was requested."""
    assert "nvidia-smi" in json.dumps(build_notebook(config(), plan()))


@pytest.mark.unit
def test_the_notebook_uses_colab_secrets_not_literal_tokens() -> None:
    source = json.dumps(build_notebook(config(), plan()))
    assert "userdata.get('WANDB_API_KEY')" in source
    assert "userdata.get('HF_TOKEN')" in source


@pytest.mark.unit
def test_the_notebook_uploads_the_checkpoints_off_the_runtime() -> None:
    """Checkpoints outlive the runtime only if they leave it."""
    source = json.dumps(build_notebook(config(), plan()))
    assert "upload_folder" in source


@pytest.mark.unit
def test_the_notebook_records_the_expected_vram_and_the_card() -> None:
    notebook = build_notebook(config(), plan(gpu="L4"))
    cells = notebook["cells"]
    assert isinstance(cells, list)
    heading = "".join(cells[0]["source"])
    assert "GiB estimated" in heading
    assert "L4" in heading
    assert config().name in heading


@pytest.mark.unit
def test_the_notebook_declares_a_gpu_runtime() -> None:
    metadata = build_notebook(config(), plan())["metadata"]
    assert isinstance(metadata, dict)
    assert metadata["accelerator"] == "GPU"


@pytest.mark.unit
def test_the_repo_and_branch_are_configurable() -> None:
    source = json.dumps(build_notebook(config(), plan(branch="feature/x", repo="https://x/y")))
    assert "--branch feature/x" in source
    assert "https://x/y" in source


@pytest.mark.unit
def test_the_guarded_names_cover_every_hyperparameter_in_the_config() -> None:
    """So a field added to TrainingConfig cannot quietly become inlineable."""
    fields = set(TrainingConfig.model_fields) - {
        "dataset_version",
        "base_model",
        "wandb_project",
        "output_dir",
        "load_in_4bit",
        "quant_type",
        "compute_dtype",
        "lr_scheduler",
        "epochs",
    }
    assert fields <= set(GUARDED_NAMES), fields - set(GUARDED_NAMES)


# ─────────────────────────────────────────────────────────────
# Writing it out
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_writing_produces_a_file_colab_can_open(tmp_path: Path) -> None:
    path = write_notebook(config(), plan(), tmp_path / "nb" / "run.ipynb")
    assert path.is_file()
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert loaded["nbformat"] == 4
    assert loaded["metadata"]["accelerator"] == "GPU"


@pytest.mark.unit
def test_writing_refuses_a_notebook_that_shadows_the_config(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def shadowing(config_: TrainingConfig, plan_: NotebookPlan) -> dict[str, object]:
        return {
            "cells": [{"cell_type": "code", "source": ["learning_rate = 3e-4\n"], "metadata": {}}],
            "nbformat": 4,
        }

    monkeypatch.setattr("maia.training.colab.build_notebook", shadowing)
    with pytest.raises(ValueError, match="assigns hyperparameters"):
        write_notebook(config(), plan(), tmp_path / "run.ipynb")


# ─────────────────────────────────────────────────────────────
# Colab Enterprise
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_enterprise_command_is_returned_not_run() -> None:
    """It costs money and starts a GPU, so launching it is the caller's."""
    command = enterprise_command(
        "gs://maia/notebooks/run.ipynb",
        project="andornet-163209",
        runtime_template="projects/x/locations/europe-west4/notebookRuntimeTemplates/t",
        output_uri="gs://maia/executions",
        display_name="exp_v1_r16lr2e4e3",
    )
    assert command[:4] == ["gcloud", "colab", "executions", "create"]
    assert "--project=andornet-163209" in command
    assert "--gcs-notebook-uri=gs://maia/notebooks/run.ipynb" in command
    assert "--gcs-output-uri=gs://maia/executions" in command
    assert "--display-name=exp_v1_r16lr2e4e3" in command


@pytest.mark.unit
def test_the_enterprise_region_is_configurable() -> None:
    command = enterprise_command(
        "gs://x/n.ipynb",
        project="p",
        region="us-central1",
        runtime_template="t",
        output_uri="gs://x/out",
        display_name="d",
    )
    assert "--region=us-central1" in command


# ─────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_cli_writes_the_notebook_and_prints_the_enterprise_command(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from maia.training.colab import main

    config_path = tmp_path / "run.yaml"
    config_path.write_text(config().to_yaml(), encoding="utf-8")
    out = tmp_path / "nb" / "run.ipynb"
    assert main([str(config_path), "--gpu", "L4", "--out", str(out)]) == 0
    printed = capsys.readouterr().out
    assert "GiB estimated peak" in printed
    assert "gcloud \\" in printed or "gcloud" in printed
    assert json.loads(out.read_text(encoding="utf-8"))["nbformat"] == 4


@pytest.mark.unit
def test_cli_refuses_a_gpu_that_cannot_run_the_config(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The T4 case: it has the memory and not the precision."""
    from maia.training.colab import main

    config_path = tmp_path / "run.yaml"
    config_path.write_text(config().to_yaml(), encoding="utf-8")
    assert main([str(config_path), "--gpu", "T4", "--out", str(tmp_path / "x.ipynb")]) == 1
    captured = capsys.readouterr()
    assert "bf16 needs Ampere or newer" in captured.out
    assert "cannot run on T4" in captured.err


@pytest.mark.unit
def test_cli_reports_a_missing_config(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    from maia.training.colab import main

    assert main([str(tmp_path / "absent.yaml")]) == 1
    assert "no such file" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_reports_an_unreadable_config(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from maia.training.colab import main

    config_path = tmp_path / "run.yaml"
    config_path.write_text("- not a mapping\n", encoding="utf-8")
    assert main([str(config_path)]) == 1
    assert "expected a mapping" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_refuses_to_write_a_notebook_that_shadows_the_config(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    from maia.training.colab import main

    monkeypatch.setattr(
        "maia.training.colab.build_notebook",
        lambda config_, plan_: {
            "cells": [{"cell_type": "code", "source": ["r = 64\n"], "metadata": {}}],
            "nbformat": 4,
        },
    )
    config_path = tmp_path / "run.yaml"
    config_path.write_text(config().to_yaml(), encoding="utf-8")
    assert main([str(config_path), "--out", str(tmp_path / "x.ipynb")]) == 1
    assert "assigns hyperparameters" in capsys.readouterr().err
