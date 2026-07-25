"""Tests for the QLoRA training configuration (PLAN M3.01)."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from maia.training.config import (
    BUDGET_EUR,
    DEFAULT_TARGET_MODULES,
    GPU_EUR_PER_HOUR,
    MAX_FULL_RUNS,
    TrainingConfig,
    estimate,
    load_config,
    render,
    within_budget,
)


def config(**overrides: object) -> TrainingConfig:
    return TrainingConfig.model_validate({"dataset_version": "v1", **overrides})


# ─────────────────────────────────────────────────────────────
# The spec's starting hyperparameters
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_defaults_are_the_specs_starting_hyperparameters() -> None:
    default = config()
    assert (default.r, default.lora_alpha, default.lora_dropout) == (16, 32, 0.05)
    assert default.learning_rate == 2e-4
    assert default.lr_scheduler == "cosine"
    assert default.warmup_ratio == 0.03
    assert default.epochs == 3
    assert default.max_seq_len == 4_096
    assert default.load_in_4bit and default.quant_type == "nf4"
    assert default.compute_dtype == "bfloat16"


@pytest.mark.unit
def test_the_target_modules_are_all_attention_and_mlp_projections() -> None:
    assert set(DEFAULT_TARGET_MODULES) == {
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
        "gate_proj",
        "up_proj",
        "down_proj",
    }
    assert config().target_modules == DEFAULT_TARGET_MODULES


@pytest.mark.unit
def test_the_effective_batch_size_is_the_product() -> None:
    assert config(per_device_batch_size=2, gradient_accumulation_steps=8).effective_batch_size == 16
    assert config(per_device_batch_size=4, gradient_accumulation_steps=8).effective_batch_size == 32


# ─────────────────────────────────────────────────────────────
# Reproducibility
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_an_unknown_key_is_an_error_not_a_silently_ignored_setting() -> None:
    """A typo'd key is how two runs come to differ for reasons nobody can reconstruct."""
    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        TrainingConfig.model_validate({"dataset_version": "v1", "learnign_rate": 3e-4})


@pytest.mark.unit
def test_a_config_is_frozen() -> None:
    with pytest.raises(ValidationError, match="frozen"):
        config().r = 32


@pytest.mark.unit
def test_a_config_round_trips_through_yaml(tmp_path: Path) -> None:
    original = config(r=32, lora_alpha=64, epochs=2)
    path = tmp_path / "run.yaml"
    path.write_text(original.to_yaml(), encoding="utf-8")
    assert load_config(path) == original


@pytest.mark.unit
def test_the_yaml_is_sorted_so_diffs_are_readable(tmp_path: Path) -> None:
    written = yaml.safe_load(config().to_yaml())
    assert list(written) == sorted(written)


@pytest.mark.unit
def test_a_yaml_that_is_not_a_mapping_is_refused(tmp_path: Path) -> None:
    path = tmp_path / "run.yaml"
    path.write_text("- just\n- a list\n", encoding="utf-8")
    with pytest.raises(ValueError, match="expected a mapping"):
        load_config(path)


@pytest.mark.unit
def test_a_yaml_with_a_typo_is_refused(tmp_path: Path) -> None:
    path = tmp_path / "run.yaml"
    path.write_text("dataset_version: v1\nepocs: 3\n", encoding="utf-8")
    with pytest.raises(ValidationError):
        load_config(path)


@pytest.mark.unit
def test_the_seed_is_part_of_the_config() -> None:
    """ "Reproducible from a YAML + seed" — so the seed lives in the YAML."""
    assert "seed" in yaml.safe_load(config().to_yaml())


# ─────────────────────────────────────────────────────────────
# The experiment name
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_name_follows_the_latxa_pattern() -> None:
    assert config().name == "exp_v1_r16lr2e4e3"


@pytest.mark.unit
def test_the_name_changes_with_every_component_it_claims() -> None:
    base = config().name
    assert config(r=32, lora_alpha=64).name != base
    assert config(learning_rate=1e-4).name != base
    assert config(epochs=2).name != base
    assert config(dataset_version="v2").name != base


@pytest.mark.unit
def test_the_name_is_derived_not_stored() -> None:
    """So it cannot describe settings the config does not have."""
    assert "name" not in yaml.safe_load(config().to_yaml())


@pytest.mark.unit
@pytest.mark.parametrize(
    ("lr", "expected"),
    [(2e-4, "2e4"), (1e-4, "1e4"), (5e-5, "5e5"), (3e-4, "3e4"), (1.5e-4, "1p5e4")],
)
def test_the_lr_id_has_no_sign_characters(lr: float, expected: str) -> None:
    assert config(learning_rate=lr).lr_id == expected
    assert "-" not in config(learning_rate=lr).name.split("_", 2)[2]


@pytest.mark.unit
def test_the_dataset_version_is_constrained_to_name_safe_characters() -> None:
    with pytest.raises(ValidationError):
        config(dataset_version="v1 with spaces")
    with pytest.raises(ValidationError):
        config(dataset_version="")


# ─────────────────────────────────────────────────────────────
# Coherence rules
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_alpha_below_r_is_refused() -> None:
    """It scales the adapter down, which is almost always a mistake rather than a choice."""
    with pytest.raises(ValidationError, match="scales the adapter down"):
        config(r=32, lora_alpha=16)


@pytest.mark.unit
def test_alpha_equal_to_r_is_allowed() -> None:
    assert config(r=16, lora_alpha=16).lora_alpha == 16


@pytest.mark.unit
@pytest.mark.parametrize(("device", "accumulation"), [(1, 8), (8, 8), (1, 1), (4, 16)])
def test_an_effective_batch_outside_16_32_is_refused(device: int, accumulation: int) -> None:
    with pytest.raises(ValidationError, match="chosen for 16-32"):
        config(per_device_batch_size=device, gradient_accumulation_steps=accumulation)


@pytest.mark.unit
def test_disabling_4bit_is_refused() -> None:
    """12B in bf16 does not fit the 80 GB this phase budgets for."""
    with pytest.raises(ValidationError, match="not QLoRA"):
        config(load_in_4bit=False)


@pytest.mark.unit
@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("r", 2),
        ("r", 256),
        ("lora_dropout", 0.5),
        ("learning_rate", 0.0),
        ("learning_rate", 0.1),
        ("warmup_ratio", 0.5),
        ("epochs", 0),
        ("epochs", 9),
        ("max_seq_len", 128),
        ("max_seq_len", 100_000),
        ("quant_type", "int8"),
        ("compute_dtype", "float32"),
        ("lr_scheduler", "exponential"),
    ],
)
def test_a_value_outside_the_specs_range_is_refused(field: str, value: object) -> None:
    with pytest.raises(ValidationError):
        config(**{field: value})


# ─────────────────────────────────────────────────────────────
# Cost
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_estimate_brackets_the_specs_own_figure() -> None:
    """The spec says 3-6 h for 3 epochs over 12k examples."""
    (low_hours, high_hours), _ = estimate(config(epochs=3), 12_000)
    assert low_hours == pytest.approx(3.0)
    assert high_hours == pytest.approx(6.0)


@pytest.mark.unit
def test_the_cost_brackets_use_the_price_band() -> None:
    _, (low_eur, high_eur) = estimate(config(epochs=3), 12_000)
    assert low_eur == pytest.approx(3.0 * min(GPU_EUR_PER_HOUR))
    assert high_eur == pytest.approx(6.0 * max(GPU_EUR_PER_HOUR))


@pytest.mark.unit
def test_more_epochs_cost_more() -> None:
    (_, two), _ = estimate(config(epochs=2), 12_000)
    (_, three), _ = estimate(config(epochs=3), 12_000)
    assert three > two


@pytest.mark.unit
def test_a_run_inside_the_budget_is_reported_as_such() -> None:
    """12k over 3 epochs, worst case 18 EUR, inside the 15-40 band."""
    assert within_budget(config(epochs=3), 12_000)
    assert "✓ estimate" in render(config(), 12_000)


@pytest.mark.unit
def test_a_run_the_budget_cannot_cover_is_flagged() -> None:
    """Worst case, because a run that only fits if the GPU is cheap and fast will overrun."""
    assert not within_budget(config(epochs=5), 100_000)
    rendered = render(config(epochs=5), 100_000)
    assert "✗ estimate" in rendered
    assert "exceeds the budget" in rendered
    assert f"{MAX_FULL_RUNS} full runs" in rendered


@pytest.mark.unit
def test_the_budget_band_is_the_plans() -> None:
    assert BUDGET_EUR == (15.0, 40.0)
    assert MAX_FULL_RUNS == 3


@pytest.mark.unit
@pytest.mark.parametrize("examples", [0, -1])
def test_estimating_over_no_examples_is_refused(examples: int) -> None:
    with pytest.raises(ValueError, match="examples must be positive"):
        estimate(config(), examples)


# ─────────────────────────────────────────────────────────────
# Reporting
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_summary_names_the_run_and_its_settings() -> None:
    rendered = render(config())
    assert rendered.startswith("exp_v1_r16lr2e4e3")
    assert "r=16 alpha=32" in rendered
    assert "lr=0.0002 cosine warmup=3%" in rendered
    assert "4-bit nf4 / bfloat16" in rendered
    assert "seed: 20260725" in rendered


@pytest.mark.unit
def test_the_summary_omits_the_estimate_when_the_size_is_unknown() -> None:
    assert "estimate" not in render(config())
