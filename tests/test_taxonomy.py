"""Tests for the generation taxonomy (PLAN M2.01)."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest
import yaml

from maia.schemas import CorpusDocument, License, Registre, Source
from maia.synth.taxonomy import (
    MAX_NODES,
    MIN_NODES,
    REQUIRED_BRANCHES,
    NotApprovedError,
    Taxonomy,
    TaxonomyNode,
    check_retrievable,
    check_taxonomy,
    load_taxonomy,
    main,
    render,
    require_approved,
)

SHIPPED = Path(__file__).resolve().parents[1] / "configs" / "taxonomy.yaml"


def node(
    node_id: str, *, keywords: list[str] | None = None, weight: float = 1.0
) -> dict[str, object]:
    return {
        "id": node_id,
        "label": f"Etiqueta de {node_id}",
        "keywords": keywords or [node_id.split("/")[-1]],
        "weight": weight,
    }


def taxonomy_payload(nodes: list[dict[str, object]], **overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {"version": "test", "approved": False, "nodes": nodes}
    payload.update(overrides)
    return payload


def full_nodes(count: int = MIN_NODES) -> list[dict[str, object]]:
    """A structurally valid node list: every required branch, padded to ``count``."""
    nodes = [node(f"{branch}/node-{index}") for branch in REQUIRED_BRANCHES for index in range(2)]
    while len(nodes) < count:
        nodes.append(node(f"historia/extra-{len(nodes)}"))
    return nodes[:count]


# ─────────────────────────────────────────────────────────────
# The shipped draft
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_the_shipped_draft_is_structurally_valid() -> None:
    report = check_taxonomy(load_taxonomy(SHIPPED))
    assert report.ok, [f.reason for f in report.findings]
    assert MIN_NODES <= report.nodes <= MAX_NODES


@pytest.mark.unit
def test_the_shipped_draft_covers_every_required_branch() -> None:
    report = check_taxonomy(load_taxonomy(SHIPPED))
    assert set(REQUIRED_BRANCHES) <= set(report.branches)


@pytest.mark.unit
def test_the_shipped_draft_is_deliberately_not_approved() -> None:
    """M2.01 is a PO gate: the draft must not be able to run generation as shipped."""
    taxonomy = load_taxonomy(SHIPPED)
    assert taxonomy.approved is False
    with pytest.raises(NotApprovedError, match="not approved"):
        require_approved(taxonomy)


@pytest.mark.unit
def test_the_shipped_draft_teaches_where_to_look_things_up() -> None:
    # The node behind the `no_ho_se` type and D8: citable details live in RAG, not the weights.
    taxonomy = load_taxonomy(SHIPPED)
    lookup = taxonomy.node("legal/on-consultar")
    assert "BOPA" in lookup.keywords
    assert lookup.weight > 1.0


@pytest.mark.unit
def test_the_shipped_draft_weights_the_andorran_lexicon_up() -> None:
    taxonomy = load_taxonomy(SHIPPED)
    lexicon = [n for n in taxonomy.nodes if n.branch == "lexic"]
    assert lexicon
    assert all(node.weight >= 1.5 for node in lexicon)


# ─────────────────────────────────────────────────────────────
# Node validation
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
@pytest.mark.parametrize(
    "node_id",
    ["nobranch", "Historia/Pareatges", "historia/", "/pareatges", "historia//x", "historia/a_b"],
)
def test_a_malformed_node_id_is_rejected(node_id: str) -> None:
    with pytest.raises(ValueError, match="must be 'branch/slug'"):
        TaxonomyNode.model_validate(node(node_id))


@pytest.mark.unit
def test_a_well_formed_id_exposes_its_branch() -> None:
    assert TaxonomyNode.model_validate(node("historia/pareatges-1278")).branch == "historia"


@pytest.mark.unit
def test_a_node_needs_at_least_one_keyword() -> None:
    # Keywords are how the sampler finds grounding passages; none means no grounding.
    with pytest.raises(ValueError):
        TaxonomyNode.model_validate({"id": "historia/x", "label": "X", "keywords": []})


@pytest.mark.unit
def test_a_blank_keyword_is_rejected() -> None:
    with pytest.raises(ValueError, match="empty keyword"):
        TaxonomyNode.model_validate({"id": "historia/x", "label": "X", "keywords": ["ok", "  "]})


@pytest.mark.unit
def test_years_written_bare_in_yaml_are_accepted() -> None:
    """YAML types ``1278`` as an int, and a PO writing it unquoted is entirely natural.

    Failing on it would be user-hostile for a file whose whole purpose is to be hand-edited.
    """
    parsed = yaml.safe_load(
        "id: historia/pareatges\nlabel: Pareatges\nkeywords: [pareatge, 1278]\n"
    )
    assert parsed["keywords"][1] == 1278  # YAML really did make it an int
    assert TaxonomyNode.model_validate(parsed).keywords == ["pareatge", "1278"]


@pytest.mark.unit
@pytest.mark.parametrize("weight", [0.0, -1.0, 5.1])
def test_weight_must_be_a_sane_multiplier(weight: float) -> None:
    with pytest.raises(ValueError):
        TaxonomyNode.model_validate(node("historia/x", weight=weight))


@pytest.mark.unit
def test_unknown_node_fields_are_rejected() -> None:
    with pytest.raises(ValueError):
        TaxonomyNode.model_validate({**node("historia/x"), "prioritat": "alta"})


# ─────────────────────────────────────────────────────────────
# Taxonomy validation
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_duplicate_node_ids_are_rejected() -> None:
    with pytest.raises(ValueError, match="duplicate node ids: historia/x"):
        Taxonomy.model_validate(taxonomy_payload([node("historia/x"), node("historia/x")]))


@pytest.mark.unit
def test_approval_requires_a_name() -> None:
    # An approved-by-nobody gate is not a gate.
    with pytest.raises(ValueError, match="requires approved_by"):
        Taxonomy.model_validate(taxonomy_payload(full_nodes(), approved=True))


@pytest.mark.unit
def test_approval_with_a_name_is_accepted() -> None:
    taxonomy = Taxonomy.model_validate(
        taxonomy_payload(full_nodes(), approved=True, approved_by="Eric Risco")
    )
    require_approved(taxonomy)  # does not raise
    assert taxonomy.approved_by == "Eric Risco"


@pytest.mark.unit
@pytest.mark.parametrize("count", [MIN_NODES - 1, MAX_NODES + 1])
def test_the_node_count_range_is_enforced(count: int) -> None:
    nodes = full_nodes(MIN_NODES)
    while len(nodes) < count:
        nodes.append(node(f"historia/pad-{len(nodes)}"))
    report = check_taxonomy(Taxonomy.model_validate(taxonomy_payload(nodes[:count])))
    assert any("outside the" in finding.reason for finding in report.findings)


@pytest.mark.unit
@pytest.mark.parametrize("count", [MIN_NODES, MAX_NODES])
def test_the_range_edges_are_accepted(count: int) -> None:
    nodes = full_nodes(MIN_NODES)
    while len(nodes) < count:
        nodes.append(node(f"historia/pad-{len(nodes)}"))
    assert check_taxonomy(Taxonomy.model_validate(taxonomy_payload(nodes))).ok


@pytest.mark.unit
def test_a_missing_required_branch_is_a_finding() -> None:
    nodes = [n for n in full_nodes() if not str(n["id"]).startswith("legal/")]
    report = check_taxonomy(Taxonomy.model_validate(taxonomy_payload(nodes)))
    assert any("missing required branch(es): legal" in f.reason for f in report.findings)


@pytest.mark.unit
def test_a_one_node_branch_is_a_finding() -> None:
    nodes = [*full_nodes(), node("extra/only-one")]
    report = check_taxonomy(Taxonomy.model_validate(taxonomy_payload(nodes)))
    assert any("not a branch" in f.reason for f in report.findings)


@pytest.mark.unit
def test_the_report_counts_nodes_per_branch() -> None:
    report = check_taxonomy(Taxonomy.model_validate(taxonomy_payload(full_nodes())))
    assert report.branches["legal"] == 2
    assert sum(report.branches.values()) == report.nodes


@pytest.mark.unit
def test_node_lookup_raises_on_an_unknown_id() -> None:
    taxonomy = Taxonomy.model_validate(taxonomy_payload(full_nodes()))
    assert taxonomy.node("legal/node-0").branch == "legal"
    with pytest.raises(KeyError):
        taxonomy.node("legal/no-existeix")


@pytest.mark.unit
def test_ids_is_what_the_topic_field_must_be_one_of() -> None:
    taxonomy = Taxonomy.model_validate(taxonomy_payload(full_nodes()))
    assert "legal/node-0" in taxonomy.ids
    assert len(taxonomy.ids) == len(taxonomy.nodes)


# ─────────────────────────────────────────────────────────────
# Loading
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_a_non_mapping_file_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "taxonomy.yaml"
    path.write_text("- just\n- a\n- list\n", encoding="utf-8")
    with pytest.raises(ValueError, match="expected a YAML mapping"):
        load_taxonomy(path)


@pytest.mark.unit
def test_a_schema_error_names_the_offending_node(tmp_path: Path) -> None:
    # A taxonomy that silently loaded half its nodes would produce a dataset with silent holes.
    path = tmp_path / "taxonomy.yaml"
    path.write_text(
        yaml.safe_dump(taxonomy_payload([{"id": "MAJUSCULES/x", "label": "X", "keywords": ["x"]}])),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="branch/slug"):
        load_taxonomy(path)


@pytest.mark.unit
def test_a_taxonomy_round_trips_through_yaml(tmp_path: Path) -> None:
    path = tmp_path / "taxonomy.yaml"
    original = Taxonomy.model_validate(taxonomy_payload(full_nodes()))
    path.write_text(yaml.safe_dump(original.model_dump()), encoding="utf-8")
    assert load_taxonomy(path).ids == original.ids


# ─────────────────────────────────────────────────────────────
# Groundability
# ─────────────────────────────────────────────────────────────


def document(text: str, index: int) -> CorpusDocument:
    return CorpusDocument(
        text=text,
        source=Source.GOVERN,
        url=f"https://www.govern.ad/{index}",  # type: ignore[arg-type]
        fetched_at=datetime(2026, 8, 1, tzinfo=UTC),
        lang="ca",
        license=License.PUBLIC_OFFICIAL,
        registre=Registre.ESTANDARD,
    )


@pytest.mark.unit
def test_a_node_with_enough_passages_is_groundable() -> None:
    taxonomy = Taxonomy.model_validate(
        taxonomy_payload([node("cultura/falles", keywords=["falles"]), node("cultura/altre")])
    )
    corpus = [document(f"Les falles del solstici, document {i}.", i) for i in range(6)]
    findings = check_retrievable(taxonomy, corpus, min_passages=5)
    assert [finding.locator for finding in findings] == ["cultura/altre"]


@pytest.mark.unit
def test_a_node_that_retrieves_nothing_is_reported() -> None:
    """Found here, it costs a command; found during generation, it costs the whole batch.

    §3.2 rejects ungrounded examples, so a node that retrieves too little simply produces
    nothing — after the API spend for every other node.
    """
    taxonomy = Taxonomy.model_validate(taxonomy_payload([node("legal/x", keywords=["inexistent"])]))
    findings = check_retrievable(taxonomy, [document("Un text qualsevol.", 0)])
    assert findings
    assert "retrieve 0 passage(s)" in findings[0].reason


@pytest.mark.unit
def test_keyword_matching_is_case_insensitive() -> None:
    taxonomy = Taxonomy.model_validate(taxonomy_payload([node("cultura/x", keywords=["FALLES"])]))
    corpus = [document(f"les falles, document {i}.", i) for i in range(3)]
    assert check_retrievable(taxonomy, corpus, min_passages=3) == []


@pytest.mark.unit
def test_any_keyword_matching_is_enough() -> None:
    taxonomy = Taxonomy.model_validate(
        taxonomy_payload([node("cultura/x", keywords=["inexistent", "falles"])])
    )
    corpus = [document(f"Les falles, document {i}.", i) for i in range(3)]
    assert check_retrievable(taxonomy, corpus, min_passages=3) == []


# ─────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_cli_validates_the_shipped_draft(capsys: pytest.CaptureFixture[str]) -> None:
    assert main([str(SHIPPED)]) == 0
    out = capsys.readouterr().out
    assert "NOT APPROVED" in out
    assert "legal=" in out


@pytest.mark.unit
def test_cli_require_approved_gates_the_draft(capsys: pytest.CaptureFixture[str]) -> None:
    assert main([str(SHIPPED), "--require-approved"]) == 1
    assert "not approved" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_fails_a_structurally_broken_taxonomy(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "taxonomy.yaml"
    path.write_text(
        yaml.safe_dump(taxonomy_payload([node("historia/x"), node("legal/y")])), encoding="utf-8"
    )
    assert main([str(path)]) == 1
    out = capsys.readouterr().out
    assert "outside the" in out


@pytest.mark.unit
def test_cli_reports_unretrievable_nodes(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    taxonomy_path = tmp_path / "taxonomy.yaml"
    nodes = full_nodes()
    taxonomy_path.write_text(yaml.safe_dump(taxonomy_payload(nodes)), encoding="utf-8")
    corpus_path = tmp_path / "corpus.jsonl"
    corpus_path.write_text(
        f"{document('Un text que no esmenta cap node.', 0).model_dump_json()}\n", encoding="utf-8"
    )
    assert main([str(taxonomy_path), "--corpus", str(corpus_path)]) == 0  # a warning, not a failure
    out = capsys.readouterr().out
    assert "more thin nodes" in out


@pytest.mark.unit
def test_cli_reports_a_broken_yaml_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "taxonomy.yaml"
    path.write_text("- not a mapping\n", encoding="utf-8")
    assert main([str(path)]) == 1
    assert "expected a YAML mapping" in capsys.readouterr().err


@pytest.mark.unit
def test_cli_reports_a_missing_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main([str(tmp_path / "absent.yaml")]) == 1
    assert "no such file" in capsys.readouterr().err


@pytest.mark.unit
def test_render_shows_findings(tmp_path: Path) -> None:
    report = check_taxonomy(Taxonomy.model_validate(taxonomy_payload([node("historia/x")])))
    rendered = render(report, tmp_path / "taxonomy.yaml")
    assert "✗" in rendered
    assert "1 nodes" in rendered


@pytest.mark.unit
def test_keywords_written_as_a_bare_string_is_rejected_clearly() -> None:
    # Another easy hand-edit slip: `keywords: pareatge` instead of `keywords: [pareatge]`.
    # The coercion passes non-lists straight through so pydantic can say what it wanted.
    parsed = yaml.safe_load("id: historia/x\nlabel: X\nkeywords: pareatge\n")
    with pytest.raises(ValueError, match="valid list"):
        TaxonomyNode.model_validate(parsed)
