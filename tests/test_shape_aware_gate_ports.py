from digital_logic_lab.circuit_engine import build_circuit
from digital_logic_lab.circuit_layout import GATE_PORT_STRAIGHT, layout_circuit
from digital_logic_lab.realization_policy import RealizationPreset
from digital_logic_lab.realization_strategy import realize_preset


OR_FAMILY = {"OR", "NOR", "XOR", "XNOR"}
EXEMPT = {"INPUT", "OUTPUT", "CONSTANT"}


def _nodes(layout):
    return {node.id: node for node in layout.nodes}


def _assert_shape_aware_ports(graph):
    layout = layout_circuit(graph)
    nodes = _nodes(layout)

    for wire in layout.wires:
        source = nodes[wire.source]
        target = nodes[wire.target]
        pts = wire.points

        if source.kind not in EXEMPT:
            assert pts[0][1] == pts[1][1]
            assert pts[1][0] - pts[0][0] >= GATE_PORT_STRAIGHT

        if target.kind not in EXEMPT:
            assert pts[-2][1] == pts[-1][1]
            assert pts[-1][0] - pts[-2][0] >= GATE_PORT_STRAIGHT

        if target.kind in OR_FAMILY:
            # The rear curve bows right of the rectangular x coordinate at
            # ordinary symmetric input-pin heights. The wire must terminate
            # on that curve, not in the empty space to its left.
            assert pts[-1][0] > target.x


def test_or_inputs_touch_curved_gate_boundary():
    graph = build_circuit("A+B")
    layout = layout_circuit(graph)
    nodes = _nodes(layout)
    target = next(n for n in layout.nodes if n.kind == "OR")
    incoming = [w for w in layout.wires if w.target == target.id]
    assert len(incoming) == 2
    assert all(w.points[-1][0] > target.x for w in incoming)


def test_xor_inputs_touch_curved_gate_boundary():
    graph = build_circuit("A^B")
    _assert_shape_aware_ports(graph)


def test_nor_realization_uses_shape_aware_ports():
    result = realize_preset("A+B", RealizationPreset.NOR_ONLY)
    _assert_shape_aware_ports(result.graph)


def test_nand_realization_preserves_six_pixel_rule():
    result = realize_preset("A^B", RealizationPreset.NAND_ONLY)
    _assert_shape_aware_ports(result.graph)


def test_basic_example_preserves_six_pixel_rule():
    _assert_shape_aware_ports(build_circuit("AB + AC'"))
