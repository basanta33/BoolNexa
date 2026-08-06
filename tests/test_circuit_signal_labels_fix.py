from digital_logic_lab.circuit_visual_model import build_circuit_visual_from_graph
from digital_logic_lab.realization_policy import RealizationPreset
from digital_logic_lab.realization_strategy import realize_preset


def _visual(expression, preset=RealizationPreset.NAND_ONLY):
    graph = realize_preset(expression, preset).graph
    return build_circuit_visual_from_graph(graph)


def test_internal_wires_use_stable_compact_net_names():
    visual = _visual("AB+AC'")
    labels = [w.label for w in visual.wires if w.label]
    nets = [x for x in labels if x.startswith("N")]
    assert nets
    assert all(x[1:].isdigit() for x in nets)


def test_primary_inputs_and_final_expression_remain_visible():
    visual = _visual("AB+AC'")
    labels = [w.label for w in visual.wires if w.label]
    assert "A" in labels and "B" in labels and "C" in labels
    assert "AB + AC'" in labels
    assert visual.expression == "AB + AC'"


def test_full_intermediate_semantics_are_preserved_on_nodes():
    visual = _visual("AB+AC'")
    expressions = [n.expression for n in visual.nodes]
    assert "(AB)'" in expressions
    assert "C'" in expressions
    assert "(AC')'" in expressions


def test_compact_names_are_deterministic_across_rebuilds():
    expected = [w.label for w in _visual("AB+AC'").wires]
    for _ in range(25):
        assert [w.label for w in _visual("AB+AC'").wires] == expected
