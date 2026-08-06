from digital_logic_lab.circuit_engine import build_circuit
from digital_logic_lab.circuit_layout import GATE_PORT_STRAIGHT, layout_circuit
from digital_logic_lab.realization_policy import RealizationPreset
from digital_logic_lab.realization_strategy import realize_preset


EXEMPT = {"INPUT", "OUTPUT", "CONSTANT"}


def _node_map(layout):
    return {node.id: node for node in layout.nodes}


def _assert_port_invariants(graph):
    layout = layout_circuit(graph)
    nodes = _node_map(layout)

    for wire in layout.wires:
        source = nodes[wire.source]
        target = nodes[wire.target]
        points = wire.points
        assert len(points) >= 2

        if source.kind not in EXEMPT:
            a, b = points[0], points[1]
            assert a[1] == b[1], (wire, "gate output must leave horizontally")
            assert b[0] - a[0] >= GATE_PORT_STRAIGHT, (
                wire,
                "gate output straight run is shorter than 6 px",
            )

        if target.kind not in EXEMPT:
            a, b = points[-2], points[-1]
            assert a[1] == b[1], (wire, "gate input must enter horizontally")
            assert b[0] - a[0] >= GATE_PORT_STRAIGHT, (
                wire,
                "gate input straight run is shorter than 6 px",
            )


def test_port_constant_is_ten_pixels():
    assert GATE_PORT_STRAIGHT == 10


def test_basic_circuit_obeys_gate_port_invariants():
    _assert_port_invariants(build_circuit("AB + AC'"))


def test_xor_preferred_obeys_gate_port_invariants():
    result = realize_preset("A^B", RealizationPreset.XOR_PREFERRED)
    _assert_port_invariants(result.graph)


def test_basic_xor_expansion_obeys_gate_port_invariants():
    result = realize_preset("A^B", RealizationPreset.BASIC_ONLY)
    _assert_port_invariants(result.graph)


def test_nand_only_obeys_gate_port_invariants():
    result = realize_preset("A^B", RealizationPreset.NAND_ONLY)
    _assert_port_invariants(result.graph)


def test_nor_only_obeys_gate_port_invariants():
    result = realize_preset("A^B", RealizationPreset.NOR_ONLY)
    _assert_port_invariants(result.graph)


def test_external_input_and_output_pins_are_exempt():
    graph = build_circuit("AB")
    layout = layout_circuit(graph)
    nodes = _node_map(layout)

    input_wires = [w for w in layout.wires if nodes[w.source].kind == "INPUT"]
    output_wires = [w for w in layout.wires if nodes[w.target].kind == "OUTPUT"]
    assert input_wires
    assert output_wires

