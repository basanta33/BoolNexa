"""Functional validation helpers for BoolNexa generated circuits."""

from __future__ import annotations

from itertools import product

from .boolean_engine import evaluate_expression
from .circuit_engine import build_circuit
from .gate import GateKind


def evaluate_generated_circuit(expression: str, values: dict[str, int]) -> int:
    graph = build_circuit(expression)
    results: dict[str, int] = {}

    for node in sorted(graph.nodes, key=lambda n: n.level):
        if node.kind == GateKind.INPUT:
            results[node.id] = int(values[node.label])
        elif node.kind == GateKind.CONSTANT:
            results[node.id] = int(node.label)
        elif node.kind == GateKind.NOT:
            results[node.id] = 1 - results[node.inputs[0]]
        elif node.kind == GateKind.AND:
            results[node.id] = results[node.inputs[0]] & results[node.inputs[1]]
        elif node.kind == GateKind.OR:
            results[node.id] = results[node.inputs[0]] | results[node.inputs[1]]
        elif node.kind == GateKind.XOR:
            results[node.id] = results[node.inputs[0]] ^ results[node.inputs[1]]
        elif node.kind == GateKind.OUTPUT:
            results[node.id] = results[node.inputs[0]]
        else:
            raise ValueError(f"Unsupported gate kind in validator: {node.kind}")

    return results[graph.output_node]


def validate_expression_equivalence(expression: str) -> list[dict[str, object]]:
    graph = build_circuit(expression)
    variables = graph.variables
    mismatches: list[dict[str, object]] = []

    for bits in product((0, 1), repeat=len(variables)):
        values = dict(zip(variables, bits))
        expected = int(evaluate_expression(expression, values))
        actual = evaluate_generated_circuit(expression, values)
        if expected != actual:
            mismatches.append(
                {
                    "inputs": values,
                    "expected": expected,
                    "actual": actual,
                }
            )
    return mismatches


def topology_signature(expression: str) -> dict[str, object]:
    graph = build_circuit(expression)
    return {
        "counts": dict(graph.statistics.counts),
        "total_gates": graph.statistics.total_gates,
        "logic_depth": graph.statistics.logic_depth,
        "inputs": list(graph.variables),
        "normalized": graph.normalized_expression,
    }
