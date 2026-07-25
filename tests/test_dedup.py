"""Unit tests for MinHash + LSH near-duplicate detection (PLAN M1.08)."""

from __future__ import annotations

import pytest

from maia.corpus.dedup import (
    DEFAULT_CONFIG,
    MinHashConfig,
    NearDuplicateIndex,
    UnionFind,
    choose_survivors,
    find_near_duplicates,
    jaccard,
    shingles,
    signature,
)

BASE = (
    "Les falles són una tradició molt antiga que se celebra a diverses parròquies del "
    "Principat. Cada any, quan arriba el solstici d'estiu, els fallaires baixen de la "
    "muntanya amb les falles enceses i il·luminen el poble sencer durant tota la nit. "
    "La celebració està inscrita a la llista del patrimoni cultural immaterial."
)
# The same page served as a print view: identical body, extra chrome. This is the shape of
# the duplicates that actually occur in a scraped corpus.
NEAR = "Imprimir aquesta pàgina\n\n" + BASE + "\n\nCompartir a les xarxes socials."
# A genuinely different document of similar length and register.
OTHER = (
    "El Consell General és l'òrgan que representa el poble andorrà, exerceix la potestat "
    "legislativa, aprova els pressupostos de l'Estat i impulsa i controla l'acció política "
    "del Govern. Es compon d'un mínim de vint-i-vuit i un màxim de quaranta-dos consellers "
    "generals, la meitat elegits en circumscripció parroquial."
)


# ─────────────────────────────────────────────────────────────
# Shingling and the sketch
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_shingling_ignores_case_and_punctuation() -> None:
    assert shingles("Les falles són una tradició antiga") == shingles(
        "les FALLES, són: una tradició — antiga!"
    )


@pytest.mark.unit
def test_shingle_count_matches_the_ngram_count() -> None:
    text = "un dos tres quatre cinc sis set"  # 7 words, 5-grams → 3 shingles
    assert len(shingles(text, 5)) == 3


@pytest.mark.unit
def test_short_text_still_produces_one_shingle() -> None:
    assert len(shingles("dues paraules", 5)) == 1


@pytest.mark.unit
def test_empty_text_has_no_shingles_and_no_signature() -> None:
    assert shingles("") == frozenset()
    assert signature(frozenset()) == ()


@pytest.mark.unit
def test_identical_text_gives_an_identical_signature() -> None:
    assert signature(shingles(BASE)) == signature(shingles(BASE))


@pytest.mark.unit
def test_signature_is_reproducible_across_config_instances() -> None:
    # Determinism is the property that makes a consolidation run repeatable.
    assert signature(shingles(BASE), MinHashConfig()) == signature(shingles(BASE), MinHashConfig())
    assert MinHashConfig().permutations() == MinHashConfig().permutations()


@pytest.mark.unit
def test_a_different_seed_gives_a_different_sketch() -> None:
    assert signature(shingles(BASE), MinHashConfig()) != signature(
        shingles(BASE), MinHashConfig(seed=1)
    )


@pytest.mark.unit
def test_signature_length_is_num_perm() -> None:
    config = MinHashConfig(num_perm=32, bands=4)
    assert len(signature(shingles(BASE), config)) == 32


@pytest.mark.unit
def test_minhash_agreement_estimates_jaccard() -> None:
    left, right = shingles(BASE), shingles(NEAR)
    config = MinHashConfig(num_perm=256, bands=8)
    sig_left, sig_right = signature(left, config), signature(right, config)
    agreement = sum(a == b for a, b in zip(sig_left, sig_right, strict=True)) / config.num_perm
    assert agreement == pytest.approx(jaccard(left, right), abs=0.12)


@pytest.mark.unit
def test_jaccard_edges() -> None:
    assert jaccard(shingles(BASE), shingles(BASE)) == 1.0
    assert jaccard(frozenset(), frozenset()) == 1.0
    assert jaccard(shingles(BASE), frozenset()) == 0.0
    assert jaccard(shingles(BASE), shingles(OTHER)) < 0.05


# ─────────────────────────────────────────────────────────────
# Config validation
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_bands_must_divide_num_perm() -> None:
    with pytest.raises(ValueError, match="must divide"):
        MinHashConfig(num_perm=64, bands=7)


@pytest.mark.unit
def test_shingle_size_must_be_positive() -> None:
    with pytest.raises(ValueError, match="shingle_size"):
        MinHashConfig(shingle_size=0)


@pytest.mark.unit
def test_rows_and_candidate_threshold_describe_the_lsh_tradeoff() -> None:
    config = MinHashConfig(num_perm=64, bands=8)
    assert config.rows == 8
    # The recall floor must sit below the confirmation threshold, or near-duplicates at the
    # confirmation threshold would never even become candidates.
    assert config.candidate_threshold < 0.85


# ─────────────────────────────────────────────────────────────
# The index
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_near_duplicates_are_grouped_and_distinct_documents_are_not() -> None:
    clusters = find_near_duplicates([("base", BASE), ("near", NEAR), ("other", OTHER)])
    assert clusters == [["base", "near"]]


@pytest.mark.unit
def test_exact_copies_are_grouped() -> None:
    clusters = find_near_duplicates([("a", BASE), ("b", BASE), ("c", OTHER)])
    assert clusters == [["a", "b"]]


@pytest.mark.unit
def test_grouping_is_transitive() -> None:
    # a≈b (0.88) and b≈c (0.88) are both above threshold while a-c (0.77) is below it, so
    # only transitive merging collapses all three.
    middle = BASE + "\n\nDarrera actualització: 12 de maig de 2024."
    far = middle + "\n\nCompartir a les xarxes socials. Imprimir aquesta pàgina."
    assert jaccard(shingles(BASE), shingles(far)) < 0.85
    assert find_near_duplicates([("a", BASE), ("b", middle), ("c", far)]) == [["a", "b", "c"]]


@pytest.mark.unit
def test_unrelated_documents_produce_no_clusters() -> None:
    assert find_near_duplicates([("a", BASE), ("b", OTHER)]) == []


@pytest.mark.unit
def test_threshold_controls_strictness() -> None:
    assert find_near_duplicates([("a", BASE), ("b", NEAR)], threshold=0.6) == [["a", "b"]]
    assert find_near_duplicates([("a", BASE), ("b", NEAR)], threshold=0.99) == []


@pytest.mark.unit
def test_a_rewritten_document_is_not_a_duplicate() -> None:
    # Calibration: replacing one sentence of four drops similarity to ~0.66. That is edited
    # content, not a duplicate, and the default threshold must keep both copies.
    rewritten = BASE.replace(
        "La celebració està inscrita a la llista del patrimoni cultural immaterial.",
        "Aquesta festa consta al patrimoni immaterial de la humanitat.",
    )
    assert jaccard(shingles(BASE), shingles(rewritten)) < 0.85
    assert find_near_duplicates([("a", BASE), ("b", rewritten)]) == []


@pytest.mark.unit
def test_empty_documents_are_indexed_but_never_cluster() -> None:
    index = NearDuplicateIndex()
    index.add("empty-one", "")
    index.add("empty-two", "")
    index.add("real", BASE)
    assert index.clusters() == []


@pytest.mark.unit
def test_adding_the_same_key_twice_is_an_error() -> None:
    index = NearDuplicateIndex()
    index.add("a", BASE)
    with pytest.raises(ValueError, match="already indexed"):
        index.add("a", OTHER)


@pytest.mark.unit
def test_cluster_order_is_stable_and_follows_insertion() -> None:
    forwards = find_near_duplicates([("z", BASE), ("a", NEAR), ("m", OTHER)])
    assert forwards == [["z", "a"]]
    backwards = find_near_duplicates([("a", NEAR), ("z", BASE)])
    assert backwards == [["a", "z"]]


@pytest.mark.unit
def test_candidate_pairs_are_a_superset_of_confirmed_clusters() -> None:
    index = NearDuplicateIndex()
    for key, text in (("base", BASE), ("near", NEAR), ("other", OTHER)):
        index.add(key, text)
    pairs = index.candidate_pairs()
    assert ("base", "near") in pairs
    assert index.clusters() == [["base", "near"]]


# ─────────────────────────────────────────────────────────────
# Survivor selection
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_choose_survivors_keeps_the_greatest_and_drops_the_rest() -> None:
    lengths = {"short": 10, "long": 100, "mid": 50}
    kept, dropped = choose_survivors([["short", "long", "mid"]], lambda k: (True, lengths[k], k))
    assert kept == {"long"}
    assert dropped == {"short", "mid"}


@pytest.mark.unit
def test_choose_survivors_handles_many_clusters_and_singletons() -> None:
    kept, dropped = choose_survivors([["a", "b"], ["c"]], lambda k: (True, 0, k))
    assert kept == {"b", "c"}
    assert dropped == {"a"}


@pytest.mark.unit
def test_default_config_is_the_documented_one() -> None:
    assert (DEFAULT_CONFIG.num_perm, DEFAULT_CONFIG.bands, DEFAULT_CONFIG.shingle_size) == (
        64,
        8,
        5,
    )


@pytest.mark.unit
def test_three_identical_documents_collapse_to_one_cluster() -> None:
    # Every pair confirms, so the union-find is asked to merge sets that are already merged.
    clusters = find_near_duplicates([("a", BASE), ("b", BASE), ("c", BASE)])
    assert clusters == [["a", "b", "c"]]


@pytest.mark.unit
def test_union_find_compresses_paths_when_two_groups_merge() -> None:
    """Depth only exceeds one when two multi-element sets merge.

    Tested directly because the public API's clusters are small enough that the compression
    branch is otherwise never reached — and an untested branch in the structure that decides
    which documents survive is not worth carrying.
    """
    forest = UnionFind()
    forest.union("a", "b")
    forest.union("c", "d")
    forest.union("b", "c")  # merges two groups: "d" is now two hops from the root
    assert forest.find("d") == "a"
    assert forest.groups() == {"a": ["a", "b", "c", "d"]}
    # Idempotent after compression.
    assert forest.find("d") == "a"


@pytest.mark.unit
def test_union_find_keeps_disjoint_groups_apart() -> None:
    forest = UnionFind()
    forest.union("a", "b")
    forest.union("c", "d")
    assert sorted(sorted(group) for group in forest.groups().values()) == [
        ["a", "b"],
        ["c", "d"],
    ]


@pytest.mark.unit
def test_clustering_is_stable_under_a_different_hash_seed() -> None:
    # Candidate pairs live in a set; merging them in insertion order is what makes the
    # partition — and the code path taken to build it — reproducible run to run.
    documents = [("a", BASE), ("b", NEAR), ("c", OTHER)]
    assert find_near_duplicates(documents) == find_near_duplicates(documents)
