"""Sprint 6.6.5 regression tests: universal-gate connection integrity."""

from digital_logic_lab.circuit_layout import GATE_PORT_STRAIGHT, layout_circuit
from digital_logic_lab.gate import GateKind
from digital_logic_lab.realization_engine import build_realized_circuit
from digital_logic_lab.realization_policy import (
    RealizationPreset,
    realization_policy_for_preset,
)


def _policy(preset):
    return realization_policy_for_preset(preset)


def _inverter_gates(graph, kind):
    """Universal gates whose two logical inputs are the exact same signal."""
    return [
        node for node in graph.nodes
        if node.kind == kind
        and len(node.inputs) == 2
        and node.inputs[0] == node.inputs[1]
    ]


def _assert_two_physical_inputs(graph, kind):
    layout = layout_circuit(graph)
    pos = {node.id: node for node in layout.nodes}

    inverter_nodes = _inverter_gates(graph, kind)
    assert inverter_nodes, f"Expected at least one {kind.value} inverter."

    for gate in inverter_nodes:
        incoming = [w for w in graph.wires if w.target == gate.id]
        assert len(incoming) == 2
        assert {w.target_input for w in incoming} == {0, 1}
        assert incoming[0].source == incoming[1].source

        routed = [w for w in layout.wires if w.target == gate.id]
        assert len(routed) == 2

        # Two physical terminals must end at different y coordinates.
        endpoints = {w.points[-1] for w in routed}
        assert len(endpoints) == 2
        assert len({p[1] for p in endpoints}) == 2

        # Each terminal gets its own >=10 px straight horizontal final run.
        for wire in routed:
            before, end = wire.points[-2], wire.points[-1]
            assert before[1] == end[1]
            assert end[0] - before[0] >= GATE_PORT_STRAIGHT


def test_gate_port_straight_is_ten_pixels():
    assert GATE_PORT_STRAIGHT == 10


def test_nand_not_connects_both_physical_inputs():
    # A' realized with NAND must be NAND(A,A).
    graph = build_realized_circuit("A'", _policy(RealizationPreset.NAND_ONLY))
    assert graph.statistics.counts == {"NAND": 1}
    _assert_two_physical_inputs(graph, GateKind.NAND)


def test_nand_and_output_inverter_connects_both_inputs():
    # AB = NAND(NAND(A,B), NAND(A,B)).
    graph = build_realized_circuit("AB", _policy(RealizationPreset.NAND_ONLY))
    assert graph.statistics.counts == {"NAND": 2}
    _assert_two_physical_inputs(graph, GateKind.NAND)


def test_nand_or_input_inverters_connect_both_inputs():
    # A+B = NAND(NAND(A,A), NAND(B,B)).
    graph = build_realized_circuit("A+B", _policy(RealizationPreset.NAND_ONLY))
    assert graph.statistics.counts == {"NAND": 3}
    _assert_two_physical_inputs(graph, GateKind.NAND)


def test_nor_not_connects_both_physical_inputs():
    graph = build_realized_circuit("A'", _policy(RealizationPreset.NOR_ONLY))
    assert graph.statistics.counts == {"NOR": 1}
    _assert_two_physical_inputs(graph, GateKind.NOR)


def test_nor_or_output_inverter_connects_both_inputs():
    graph = build_realized_circuit("A+B", _policy(RealizationPreset.NOR_ONLY))
    assert graph.statistics.counts == {"NOR": 2}
    _assert_two_physical_inputs(graph, GateKind.NOR)
