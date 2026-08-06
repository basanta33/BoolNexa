from pathlib import Path
from digital_logic_lab.boolean_engine import generate_truth_table

SOURCE = (
    Path(__file__).parents[1] / "digital_logic_lab" / "boolean_lab.py"
).read_text(encoding="utf-8")


def test_engine_produces_visible_intermediate_columns():
    compact = generate_truth_table("A(B+C')", include_intermediate=False)
    expanded = generate_truth_table("A(B+C')", include_intermediate=True)
    assert compact.intermediate_headers == []
    assert expanded.intermediate_headers == ["C'", "B + C'"]


def test_toggle_refreshes_full_visible_source_pipeline():
    start = SOURCE.index("def set_show_intermediate")
    end = SOURCE.index("def load_example", start)
    body = SOURCE[start:end]
    assert "self.show_intermediate = value" in body
    assert "self._apply_source_expression(self.expression)" in body
