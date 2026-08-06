from digital_logic_lab.circuit_engine import build_circuit
from digital_logic_lab.circuit_validator import (
    topology_signature,
    validate_expression_equivalence,
)
from digital_logic_lab.gate import GateKind


def test_ab_plus_ac_not_topology() -> None:
    graph = build_circuit("AB + AC'")
    counts = graph.statistics.counts
    assert counts["AND"] == 2
    assert counts["OR"] == 1
    assert counts["NOT"] == 1
    assert graph.statistics.total_gates == 4
    assert graph.statistics.logic_depth == 3

    and_nodes = [node for node in graph.nodes if node.kind == GateKind.AND]
    not_nodes = [node for node in graph.nodes if node.kind == GateKind.NOT]
    or_nodes = [node for node in graph.nodes if node.kind == GateKind.OR]

    assert len(and_nodes) == 2
    assert len(not_nodes) == 1
    assert len(or_nodes) == 1

    not_id = not_nodes[0].id
    second_and = [
        node for node in and_nodes
        if not_id in node.inputs
    ]
    assert len(second_and) == 1


def test_reference_expressions_are_logically_equivalent() -> None:
    expressions = [
        "AB",
        "A+B",
        "A'",
        "AB+AC",
        "AB+AC'",
        "A(B+C')",
        "(A+B)C",
        "A^B",
    ]
    for expression in expressions:
        assert validate_expression_equivalence(expression) == [], expression


def test_parentheses_change_topology() -> None:
    a = topology_signature("A(B+C')")
    b = topology_signature("AB+AC'")
    assert a["total_gates"] == 3
    assert b["total_gates"] == 4


def test_primary_input_a_is_shared_for_fanout() -> None:
    graph = build_circuit("AB+AC'")
    a_inputs = [
        node for node in graph.nodes
        if node.kind == GateKind.INPUT and node.label == "A"
    ]
    assert len(a_inputs) == 1


def test_no_accidental_gate_subexpression_deduplication() -> None:
    graph = build_circuit("AB+AB")
    and_nodes = [node for node in graph.nodes if node.kind == GateKind.AND]
    assert len(and_nodes) == 2
