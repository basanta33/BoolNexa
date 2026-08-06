from digital_logic_lab.circuit_engine import build_circuit
from digital_logic_lab.circuit_layout import layout_circuit
from digital_logic_lab.circuit_router import Rect


def _segment_hits_gate(a, b, rect):
    x1, y1 = a
    x2, y2 = b
    if x1 == x2:
        if not (rect.left < x1 < rect.right):
            return False
        lo, hi = sorted((y1, y2))
        return max(lo, rect.top) < min(hi, rect.bottom)
    if y1 == y2:
        if not (rect.top < y1 < rect.bottom):
            return False
        lo, hi = sorted((x1, x2))
        return max(lo, rect.left) < min(hi, rect.right)
    return True


def test_no_wire_runs_through_unrelated_gate_body():
    graph = build_circuit("AB+AC'")
    layout = layout_circuit(graph)
    nodes = {n.id: n for n in layout.nodes}

    for wire in layout.wires:
        for node in layout.nodes:
            if node.id in {wire.source, wire.target}:
                continue
            if node.kind in {"INPUT", "OUTPUT", "CONSTANT"}:
                continue
            rect = Rect(node.x, node.y, node.x + node.width, node.y + node.height)
            for a, b in zip(wire.points, wire.points[1:]):
                assert not _segment_hits_gate(a, b, rect), (
                    wire.source, wire.target, node.id, a, b
                )


def test_all_wire_segments_are_orthogonal():
    graph = build_circuit("AB+AC'")
    layout = layout_circuit(graph)
    for wire in layout.wires:
        for a, b in zip(wire.points, wire.points[1:]):
            assert a[0] == b[0] or a[1] == b[1]


def test_two_input_gates_have_two_distinct_entry_points():
    graph = build_circuit("AB+AC'")
    layout = layout_circuit(graph)
    for gate in [n for n in graph.nodes if n.kind.value in {"AND", "OR"}]:
        incoming = [w for w in layout.wires if w.target == gate.id]
        assert len(incoming) == 2
        assert incoming[0].points[-1] != incoming[1].points[-1]


def test_crossings_do_not_create_graph_connections():
    graph = build_circuit("AB+CD")
    # Router may allow visual crossings, but connectivity still comes solely
    # from graph wires. Each binary gate has exactly two incoming graph edges.
    for gate in [n for n in graph.nodes if n.kind.value in {"AND", "OR"}]:
        assert len(gate.inputs) == 2
