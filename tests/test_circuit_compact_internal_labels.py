from digital_logic_lab.circuit_visual_model import build_circuit_visual_from_graph
from digital_logic_lab.realization_policy import RealizationPreset
from digital_logic_lab.realization_strategy import realize_preset


def _labels(expression, preset):
    graph = realize_preset(expression, preset).graph
    visual = build_circuit_visual_from_graph(graph)
    return visual, [w.label for w in visual.wires if w.label]


def test_nand_xor_compact_internal_labels():
    visual, labels = _labels("A^B", RealizationPreset.NAND_ONLY)
    assert any(x.startswith("N") for x in labels)
    assert "A ⊕ B" in labels


def test_nor_xor_compact_internal_labels():
    visual, labels = _labels("A^B", RealizationPreset.NOR_ONLY)
    nets = [x for x in labels if x.startswith("N")]
    assert nets
    assert all(len(x) <= 4 for x in nets)
    assert "A ⊕ B" in labels
    assert any(len(n.expression) > 2 for n in visual.nodes if n.kind not in {"INPUT","OUTPUT","CONSTANT"})
