"""Smoke tests: the package imports and every pipeline subpackage is present."""

import importlib

import pytest

import maia


@pytest.mark.unit
def test_version_is_exposed() -> None:
    assert isinstance(maia.__version__, str)
    assert maia.__version__


@pytest.mark.unit
@pytest.mark.parametrize(
    "subpackage",
    ["scraping", "corpus", "synth", "training", "evaluation", "rag", "serving"],
)
def test_pipeline_subpackages_import(subpackage: str) -> None:
    module = importlib.import_module(f"maia.{subpackage}")
    assert module.__doc__, f"maia.{subpackage} must document its purpose"
