from digital_logic_lab.circuit_engine import build_circuit
from digital_logic_lab.circuit_layout import layout_circuit
from digital_logic_lab.circuit_renderer import serialize_circuit


def test_layout_moves_left_to_right():
    g = build_circuit("AB + AC'")
    l = layout_circuit(g)
    p = {n.id: n for n in l.nodes}
    assert p["input_A"].x < p[g.output_node].x


def test_every_wire_is_orthogonal():
    g = build_circuit("AB + AC'")
    l = layout_circuit(g)

    for wire in l.wires:
        assert len(wire.points) >= 2
        for first, second in zip(wire.points, wire.points[1:]):
            assert first[0] == second[0] or first[1] == second[1]


def test_serialization():
    g = build_circuit("AB + AC'")
    p = serialize_circuit(g, layout_circuit(g))
    assert p["statistics"]["total_gates"] == 4
