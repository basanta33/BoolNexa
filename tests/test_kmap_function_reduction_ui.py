from pathlib import Path

from digital_logic_lab.kmap_engine import build_kmap
from digital_logic_lab.kmap_renderer import serialize_kmap


def test_function_reduction_kmap_plot_serializes_gray_code_cells_and_groups() -> None:
    result = build_kmap("AB + AB'")
    facets = serialize_kmap(result)

    assert result.simplified_expression == "A"
    assert result.groups
    assert facets
    assert any(
        cell["groups"] != ""
        for facet in facets
        for row in facet["rows"]
        for cell in row
    )


def test_boolean_lab_exposes_combined_reduce_function_kmap_workflow() -> None:
    source = Path(__file__).parents[1] / "digital_logic_lab" / "boolean_lab.py"
    text = source.read_text(encoding="utf-8")

    assert "def reduce_function" in text
    assert "Reduce function + K-map" in text
    assert "FUNCTION REDUCTION · KARNAUGH MAP" in text
    assert "K-map plot & grouping" in text
