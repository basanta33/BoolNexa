from digital_logic_lab.circuit_engine import build_circuit
from digital_logic_lab.circuit_layout import layout_circuit


def _wire(layout, source: str, target: str):
    for wire in layout.wires:
        if wire.source == source and wire.target == target:
            return wire
    raise AssertionError(f"missing wire {source} -> {target}")


def test_two_input_gate_uses_distinct_input_y_positions() -> None:
    graph = build_circuit("AB")
    layout = layout_circuit(graph)

    and_node = next(node for node in graph.nodes if node.kind.value == "AND")
    wa = _wire(layout, "input_A", and_node.id)
    wb = _wire(layout, "input_B", and_node.id)

    assert wa.points[-1][1] != wb.points[-1][1]


def test_a_fanout_uses_short_shared_trunk() -> None:
    graph = build_circuit("AB+AC'")
    layout = layout_circuit(graph)

    a_wires = [wire for wire in layout.wires if wire.source == "input_A"]
    assert len(a_wires) == 2

    # Both branches leave A through the same first trunk X coordinate.
    assert a_wires[0].points[1][0] == a_wires[1].points[1][0]
    assert a_wires[0].points[1][1] == a_wires[1].points[1][1]


def test_ab_ac_not_has_separate_or_input_endpoints() -> None:
    graph = build_circuit("AB+AC'")
    layout = layout_circuit(graph)

    or_node = next(node for node in graph.nodes if node.kind.value == "OR")
    incoming = [wire for wire in layout.wires if wire.target == or_node.id]

    assert len(incoming) == 2
    assert incoming[0].points[-1][1] != incoming[1].points[-1][1]


def test_c_to_not_to_second_and_is_separate_path() -> None:
    graph = build_circuit("AB+AC'")
    layout = layout_circuit(graph)

    not_node = next(node for node in graph.nodes if node.kind.value == "NOT")
    second_and = next(
        node for node in graph.nodes
        if node.kind.value == "AND" and not_node.id in node.inputs
    )

    c_not = _wire(layout, "input_C", not_node.id)
    not_and = _wire(layout, not_node.id, second_and.id)

    assert c_not.points[-1][0] <= not_and.points[0][0]
    assert not_and.points[-1][0] > not_and.points[0][0]


def test_all_routes_remain_orthogonal() -> None:
    graph = build_circuit("AB+AC'")
    layout = layout_circuit(graph)

    for wire in layout.wires:
        for first, second in zip(wire.points, wire.points[1:]):
            assert first[0] == second[0] or first[1] == second[1]


def test_independent_fanout_nets_use_distinct_vertical_trunks() -> None:
    """A and B must never render on the same fan-out trunk lane."""
    from digital_logic_lab.realization_policy import RealizationPreset
    from digital_logic_lab.realization_strategy import realize_preset

    graph = realize_preset("A^B", RealizationPreset.NAND_ONLY).graph
    layout = layout_circuit(graph)

    a_wires = [wire for wire in layout.wires if wire.source == "input_A"]
    b_wires = [wire for wire in layout.wires if wire.source == "input_B"]
    assert len(a_wires) > 1
    assert len(b_wires) > 1

    # Every branch of one net shares its own trunk X.
    a_trunks = {wire.points[1][0] for wire in a_wires}
    b_trunks = {wire.points[1][0] for wire in b_wires}
    assert len(a_trunks) == 1
    assert len(b_trunks) == 1

    # Independent nets must not share the same vertical trunk.
    assert a_trunks.isdisjoint(b_trunks)



def test_or_family_input_straight_run_is_four_pixels_longer() -> None:
    """OR-family inputs get 14 px of straight approach; AND stays at 10 px."""
    for expression, gate_kind in [("A+B", "OR"), ("A^B", "XOR")]:
        graph = build_circuit(expression)
        layout = layout_circuit(graph)
        gate = next(node for node in graph.nodes if node.kind.value == gate_kind)
        incoming = [wire for wire in layout.wires if wire.target == gate.id]
        assert incoming
        for wire in incoming:
            assert wire.points[-1][0] - wire.points[-2][0] == 14
            assert wire.points[-1][1] == wire.points[-2][1]

    from digital_logic_lab.circuit_layout import PositionedNode, _target_stub
    for kind in ("NOR", "XNOR"):
        node = PositionedNode("g", kind, kind, kind, 1, 100, 40, 70, 50)
        assert _target_stub(node, (104, 54)) == (90, 54)

    graph = build_circuit("AB")
    layout = layout_circuit(graph)
    gate = next(node for node in graph.nodes if node.kind.value == "AND")
    incoming = [wire for wire in layout.wires if wire.target == gate.id]
    assert incoming
    for wire in incoming:
        assert wire.points[-1][0] - wire.points[-2][0] == 10
