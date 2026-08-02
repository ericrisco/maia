"""What MAIA is published under — one definition, because three could disagree.

The dataset licence was written in three places: the dataset card generator, the HF upload, and the
legal gate that checks the card. D-0043 changed two of them and missed the third, and the result
was worse than either licence on its own: the gate **required** the card to say `cc-by-4.0` while
the upload declared `cc-by-sa-4.0`, so the published artifact would have contradicted itself about
the one thing a downstream user has to be able to trust. The tests did not catch it because the
generator and the checker were wrong in the same direction, which is what a duplicated constant
buys you.

**The dataset is CC-BY-SA-4.0.** Not a preference. The corpus includes CC-BY-SA-3.0 Viquipèdia
text; share-alike is viral; a §3.2 example generated from one of those passages is a derivative of
it. CC-BY-4.0 would grant permission to relicense — including into a closed product — that the
upstream licence does not give us the authority to grant. CC-BY-SA-4.0 is the upgrade path 3.0
explicitly allows. Confirmed by the PO on 2026-08-02.

Publishing under the wrong licence is the one mistake in this project that a later commit cannot
fix: once a third party has redistributed under the terms announced, that use is legitimate and
cannot be withdrawn. Hence one constant, imported everywhere, and a test asserting the three
call sites agree.

**The model stays Apache-2.0.** Whether trained weights are a derivative work of their training
text is an open legal question this project does not answer; the plan's choice is unchanged.
"""

from __future__ import annotations

#: SPDX-style identifier of the published dataset's licence. See the module docstring.
DATASET_LICENSE = "cc-by-sa-4.0"

#: Human-readable form, for card prose.
DATASET_LICENSE_LABEL = "CC-BY-SA-4.0"

#: The model's licence, unchanged from the plan.
MODEL_LICENSE = "apache-2.0"


def states_dataset_licence(text: str) -> bool:
    """Whether ``text`` names the dataset licence.

    Both the hyphenated identifier and the spaced prose form count, since a card written by hand
    would reasonably use either. Matching is done here rather than at each call site so the legal
    gate cannot end up accepting a form the generator never emits — or, as happened once,
    demanding one that names the wrong licence entirely.
    """
    lowered = text.lower()
    return DATASET_LICENSE in lowered or DATASET_LICENSE.replace("-", " ") in lowered
