from itertools import product

from digital_logic_lab.gate import GateKind
from digital_logic_lab.realization_engine import build_realized_circuit
from digital_logic_lab.realization_policy import (
    RealizationPreset,
    realization_policy_for_preset,
)


def _nand_graph(expression: str):
    return build_realized_circuit(
        expression,
        realization_policy_for_preset(RealizationPreset.NAND_ONLY),
    )


def _eval(graph, values):
    result = {}
    for node in sorted(graph.nodes, key=lambda n: n.level):
        if node.kind == GateKind.INPUT:
            result[node.id] = int(values[node.label])
        elif node.kind == GateKind.CONSTANT:
            result[node.id] = int(node.label)
        elif node.kind == GateKind.NAND:
            result[node.id] = 1 - (
                result[node.inputs[0]] & result[node.inputs[1]]
            )
        elif node.kind == GateKind.OUTPUT:
            result[node.id] = result[node.inputs[0]]
    return result[graph.output_node]


def test_ab_plus_ac_not_exact_four_nand_topology():
    graph = _nand_graph("AB + AC'")
    nand = [n for n in graph.nodes if n.kind == GateKind.NAND]
    assert len(nand) == 4

    inputs = {n.label: n.id for n in graph.nodes if n.kind == GateKind.INPUT}
    a, b, c = inputs["A"], inputs["B"], inputs["C"]

    n1 = next(n for n in nand if set(n.inputs) == {a, b})
    n2 = next(n for n in nand if n.inputs == (c, c))
    n3 = next(n for n in nand if set(n.inputs) == {a, n2.id})
    n4 = next(n for n in nand if set(n.inputs) == {n1.id, n3.id})

    assert graph.node_by_id(graph.output_node).inputs == (n4.id,)

    for av, bv, cv in product((0, 1), repeat=3):
        values = {"A": av, "B": bv, "C": cv}
        expected = (av & bv) | (av & (1-cv))
        assert _eval(graph, values) == expected


def test_second_function_a_plus_bc_not_is_equivalent():
    graph = _nand_graph("A + BC'")
    for a, b, c in product((0, 1), repeat=3):
        expected = a | (b & (1-c))
        assert _eval(graph, {"A": a, "B": b, "C": c}) == expected


def test_nand_inverter_has_two_graph_connections():
    graph = _nand_graph("A'")
    nand = next(n for n in graph.nodes if n.kind == GateKind.NAND)
    assert nand.inputs[0] == nand.inputs[1]
    wires = [w for w in graph.wires if w.target == nand.id]
    assert len(wires) == 2
    assert {w.target_input for w in wires} == {0, 1}
