"""Tests for the shared nearest-rank percentile (M2.09 and M5.06 both quote a p95)."""

from __future__ import annotations

import pytest

from maia.percentiles import nearest_rank


@pytest.mark.unit
def test_nearest_rank_returns_a_value_that_is_actually_in_the_data() -> None:
    """No interpolation: a p95 no request took cannot be corroborated against the deploy log."""
    assert nearest_rank([1, 2, 3, 4, 5], 50) == 3
    assert nearest_rank([1.0, 2.0, 3.0, 4.0], 95) == 4.0
    assert nearest_rank([7], 95) == 7


@pytest.mark.unit
def test_ceil_not_round_so_the_median_of_five_is_the_third() -> None:
    """``round(2.5) == 2`` in Python — banker's rounding would pick the second of five."""
    assert nearest_rank([10, 20, 30, 40, 50], 50) == 30


@pytest.mark.unit
def test_the_percentile_of_nothing_is_an_error_not_zero() -> None:
    """Returning 0.0 here would silently pass the M5.06 latency gate on an empty measurement."""
    with pytest.raises(ValueError, match="empty"):
        nearest_rank([], 95)
