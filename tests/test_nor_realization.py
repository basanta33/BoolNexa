from itertools import product

from digital_logic_lab.gate import GateKind
from digital_logic_lab.realization_engine import build_realized_circuit
from digital_logic_lab.realization_policy import (
    RealizationPreset,
    realization_policy_for_preset,
)


def _eval_graph(graph, values):
    result = {}

    for node in sorted(graph.nodes, key=lambda n: n.level):
        if node.kind == GateKind.INPUT:
            result[node.id] = int(values[node.label])
        elif node.kind == GateKind.CONSTANT:
            result[node.id] = int(node.label)
        elif node.kind == GateKind.NOT:
            result[node.id] = 1 - result[node.inputs[0]]
        elif node.kind == GateKind.AND:
            result[node.id] = (
                result[node.inputs[0]] & result[node.inputs[1]]
            )
        elif node.kind == GateKind.OR:
            result[node.id] = (
                result[node.inputs[0]] | result[node.inputs[1]]
            )
        elif node.kind == GateKind.XOR:
            result[node.id] = (
                result[node.inputs[0]] ^ result[node.inputs[1]]
            )
        elif node.kind == GateKind.XNOR:
            result[node.id] = 1 - (
                result[node.inputs[0]] ^ result[node.inputs[1]]
            )
        elif node.kind == GateKind.NAND:
            result[node.id] = 1 - (
                result[node.inputs[0]] & result[node.inputs[1]]
            )
        elif node.kind == GateKind.NOR:
            result[node.id] = 1 - (
                result[node.inputs[0]] | result[node.inputs[1]]
            )
        elif node.kind == GateKind.OUTPUT:
            result[node.id] = result[node.inputs[0]]
        else:
            raise AssertionError(node.kind)

    return result[graph.output_node]


def _expected(expression, values):
    a = values.get("A", 0)
    b = values.get("B", 0)
    c = values.get("C", 0)

    if expression == "A'":
        return 1 - a
    if expression == "AB":
        return a & b
    if expression == "A+B":
        return a | b
    if expression == "A^B":
        return a ^ b
    if expression == "A^B^C":
        return a ^ b ^ c
    if expression == "AB+AC'":
        return (a & b) | (a & (1 - c))

    raise AssertionError(expression)


def _assert_nor_only_and_equivalent(expression, variables):
    policy = realization_policy_for_preset(RealizationPreset.NOR_ONLY)
    graph = build_realized_circuit(expression, policy)

    logical_kinds = {
        node.kind
        for node in graph.nodes
        if node.kind not in {
            GateKind.INPUT,
            GateKind.CONSTANT,
            GateKind.OUTPUT,
        }
    }

    assert logical_kinds == {GateKind.NOR}

    for bits in product((0, 1), repeat=len(variables)):
        values = dict(zip(variables, bits))
        assert _eval_graph(graph, values) == _expected(expression, values)


def test_not_maps_to_nor_only():
    _assert_nor_only_and_equivalent("A'", ["A"])


def test_and_maps_to_nor_only():
    _assert_nor_only_and_equivalent("AB", ["A", "B"])


def test_or_maps_to_nor_only():
    _assert_nor_only_and_equivalent("A+B", ["A", "B"])


def test_xor_maps_to_five_nor_network():
    policy = realization_policy_for_preset(RealizationPreset.NOR_ONLY)
    graph = build_realized_circuit("A^B", policy)

    assert graph.statistics.counts == {"NOR": 5}
    _assert_nor_only_and_equivalent("A^B", ["A", "B"])


def test_three_input_xor_sum_maps_to_nor_only():
    _assert_nor_only_and_equivalent("A^B^C", ["A", "B", "C"])


def test_mixed_expression_maps_to_nor_only():
    _assert_nor_only_and_equivalent("AB+AC'", ["A", "B", "C"])
