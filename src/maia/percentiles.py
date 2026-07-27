"""Nearest-rank percentile, shared so two gates cannot disagree about what p95 means.

M2.09 profiles example lengths and M5.06 gates response latency. Both quote a p95, both would
otherwise carry their own three-line implementation, and the two would be free to drift — one
using ``round`` and the other ``ceil`` gives different answers on the same data, and the
disagreement is invisible because each is separately tested and separately correct-looking.
"""

from __future__ import annotations

from collections.abc import Sequence
from math import ceil
from typing import TypeVar

#: Ints for M2.09's character counts, floats for M5.06's seconds. Constrained rather than bound to
#: ``float`` so the return type is the type that went in: a length stays an ``int``.
Number = TypeVar("Number", int, float)


def nearest_rank(ordered: Sequence[Number], percentile: int) -> Number:
    """Nearest-rank percentile of an **already-sorted** sequence.

    ``ceil``, not ``round``: Python rounds halves to even, so ``round(2.5) == 2`` would make the
    median of five values the second one instead of the third.

    No interpolation. A p95 latency that no request actually took is a number the deployment log
    cannot corroborate, and the point of the M5.06 gate is to be checkable against that log.

    Raises:
        ValueError: if ``ordered`` is empty — the percentile of nothing is not zero, and returning
            zero would pass a latency gate that never measured anything.
    """
    if not ordered:
        raise ValueError("percentile of an empty sequence")
    index = min(len(ordered) - 1, max(0, ceil(percentile / 100 * len(ordered)) - 1))
    return ordered[index]
