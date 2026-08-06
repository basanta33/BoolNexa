from itertools import product

from digital_logic_lab.gate import GateKind
from digital_logic_lab.realization_policy import (
    RealizationPreset,
    realization_policy_for_preset,
)
from digital_logic_lab.realization_engine import build_realized_circuit


def _eval_graph(graph, values):
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
        elif node.kind == GateKind.NOR:
            result[node.id] = 1 - (
                result[node.inputs[0]] | result[node.inputs[1]]
            )
        elif node.kind == GateKind.OUTPUT:
            result[node.id] = result[node.inputs[0]]
        else:
            raise AssertionError(
                f"Strict universal realization leaked {node.kind}"
            )
    return result[graph.output_node]


def _expected(expression, values):
    a = values.get("A", 0)
    b = values.get("B", 0)
    c = values.get("C", 0)
    if expression == "A^B":
        return a ^ b
    if expression == "AB+AC'":
        return (a & b) | (a & (1-c))
    if expression == "(A+B)(A+C)":
        return (a | b) & (a | c)
    if expression == "(A^B)+(A^B)C":
        x = a ^ b
        return x | (x & c)
    raise AssertionError(expression)


def _assert_equivalent(expression, variables, preset):
    policy = realization_policy_for_preset(preset)
    graph = build_realized_circuit(expression, policy)

    allowed = (
        GateKind.NAND
        if preset == RealizationPreset.NAND_ONLY
        else GateKind.NOR
    )
    logical = {
        n.kind for n in graph.nodes
        if n.kind not in {
            GateKind.INPUT, GateKind.CONSTANT, GateKind.OUTPUT
        }
    }
    assert logical == {allowed}

    for bits in product((0, 1), repeat=len(variables)):
        values = dict(zip(variables, bits))
        assert _eval_graph(graph, values) == _expected(expression, values)

    return graph


def test_nand_xor_stays_exactly_four_gates():
    graph = _assert_equivalent(
        "A^B", ["A", "B"], RealizationPreset.NAND_ONLY
    )
    assert graph.statistics.counts == {"NAND": 4}


def test_nor_xor_stays_exactly_five_gates():
    graph = _assert_equivalent(
        "A^B", ["A", "B"], RealizationPreset.NOR_ONLY
    )
    assert graph.statistics.counts == {"NOR": 5}


def test_nand_mixed_expression_is_compact_and_equivalent():
    graph = _assert_equivalent(
        "AB+AC'", ["A", "B", "C"], RealizationPreset.NAND_ONLY
    )
    assert graph.statistics.total_gates <= 6


def test_nor_mixed_expression_has_bounded_growth_and_is_equivalent():
    graph = _assert_equivalent(
        "AB+AC'", ["A", "B", "C"], RealizationPreset.NOR_ONLY
    )
    assert graph.statistics.total_gates <= 10


def test_repeated_xor_subexpression_is_reused_in_nand_mapping():
    graph = _assert_equivalent(
        "(A^B)+(A^B)C",
        ["A", "B", "C"],
        RealizationPreset.NAND_ONLY,
    )
    # Without structural reuse, the two A^B branches would each cost four
    # NAND gates before the remaining logic is even added.
    assert graph.statistics.total_gates < 10


def test_repeated_xor_subexpression_is_reused_in_nor_mapping():
    graph = _assert_equivalent(
        "(A^B)+(A^B)C",
        ["A", "B", "C"],
        RealizationPreset.NOR_ONLY,
    )
    assert graph.statistics.total_gates < 12


def test_factored_expression_remains_bounded_in_both_families():
    for preset in (
        RealizationPreset.NAND_ONLY,
        RealizationPreset.NOR_ONLY,
    ):
        graph = _assert_equivalent(
            "(A+B)(A+C)",
            ["A", "B", "C"],
            preset,
        )
        assert graph.statistics.total_gates <= 8
