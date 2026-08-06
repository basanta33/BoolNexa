from digital_logic_lab.circuit_engine import build_circuit
from digital_logic_lab.gate import GateKind


def test_build_simple_and_circuit():
    g = build_circuit("AB")
    kinds = [n.kind for n in g.nodes]
    assert kinds.count(GateKind.INPUT) == 2
    assert kinds.count(GateKind.AND) == 1
    assert kinds.count(GateKind.OUTPUT) == 1
    assert g.statistics.total_gates == 1
    assert g.statistics.logic_depth == 1


def test_build_expression_with_not():
    g = build_circuit("AB + AC'")
    assert g.statistics.counts["AND"] == 2
    assert g.statistics.counts["OR"] == 1
    assert g.statistics.counts["NOT"] == 1
    assert g.statistics.total_gates == 4
    assert g.statistics.logic_depth == 3


def test_common_primary_inputs_are_shared_for_fanout():
    g = build_circuit("AB + AC")
    assert len([n for n in g.nodes if n.id == "input_A"]) == 1


def test_commutative_terms_preserve_entered_structure():
    """Circuit view represents the entered expression, not its simplification.

    AB + BA therefore contains two AND gates feeding an OR gate.
    Boolean reduction/deduplication belongs to the simplifier.
    """
    g = build_circuit("AB + BA")

    and_nodes = [n for n in g.nodes if n.kind == GateKind.AND]
    or_nodes = [n for n in g.nodes if n.kind == GateKind.OR]

    assert len(and_nodes) == 2
    assert len(or_nodes) == 1
    assert g.statistics.total_gates == 3
    assert g.statistics.logic_depth == 2
