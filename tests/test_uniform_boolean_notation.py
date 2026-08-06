from pathlib import Path

from digital_logic_lab.boolean_engine import Node
from digital_logic_lab.realization_policy import RealizationPreset
from digital_logic_lab.realization_strategy import realize_preset


def test_nand_node_display_uses_complemented_product_not_arrow() -> None:
    node = Node("NAND", left=Node("VAR", value="A"), right=Node("VAR", value="C"))
    assert node.display() == "(A·C)'"
    assert "↑" not in node.display()


def test_nor_node_display_uses_complemented_sum_not_arrow() -> None:
    node = Node("NOR", left=Node("VAR", value="A"), right=Node("VAR", value="C"))
    assert node.display() == "(A + C)'"
    assert "↓" not in node.display()


def test_realized_graph_normalized_notation_contains_no_arrow_symbols() -> None:
    for preset in (RealizationPreset.NAND_ONLY, RealizationPreset.NOR_ONLY):
        graph = realize_preset("AB+AC'", preset).graph
        assert "↑" not in graph.normalized_expression
        assert "↓" not in graph.normalized_expression


def test_circuit_generator_does_not_offer_xor_preferred_mode() -> None:
    source = Path(__file__).resolve().parents[1] / "digital_logic_lab" / "logic_circuit_lab.py"
    text = source.read_text(encoding="utf-8")
    assert '"XOR Preferred"' not in text
    assert '"XOR_PREFERRED": RealizationPreset.XOR_PREFERRED' not in text
