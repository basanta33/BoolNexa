"""BoolNexa Sprint 6.6.4 — optimized NOR-only technology mapping.

Goals:
- preserve strict NOR-only realization;
- reuse structurally identical source subexpressions;
- reuse intentionally shared technology nodes;
- cancel redundant NOR self-inversion pairs;
- avoid re-expanding already realized intermediate results.
"""

from __future__ import annotations

from .boolean_engine import Node, parse_expression


def _source_key(node: Node) -> tuple:
    if node.op in {"VAR", "CONST"}:
        return (node.op, node.value)
    if node.op == "NOT":
        return ("NOT", _source_key(node.left))
    left = _source_key(node.left)
    right = _source_key(node.right)
    if node.op in {"AND", "OR", "XOR", "XNOR", "NAND", "NOR"} and right < left:
        left, right = right, left
    return (node.op, left, right)


class _NorFactory:
    def __init__(self) -> None:
        self._gate_cache: dict[tuple[int, int], Node] = {}

    def gate(self, left: Node, right: Node) -> Node:
        a, b = left, right
        if id(b) < id(a):
            a, b = b, a
        key = (id(a), id(b))
        if key not in self._gate_cache:
            self._gate_cache[key] = Node(op="NOR", left=a, right=b)
        return self._gate_cache[key]

    @staticmethod
    def _is_self_nor(node: Node) -> bool:
        return (
            node.op == "NOR"
            and node.left is not None
            and node.left is node.right
        )

    def invert(self, value: Node) -> Node:
        # NOR(NOR(X,X), NOR(X,X)) = X.
        if self._is_self_nor(value):
            return value.left
        return self.gate(value, value)

    def logical_or(self, left: Node, right: Node) -> Node:
        p = self.gate(left, right)
        return self.invert(p)

    def logical_and(self, left: Node, right: Node) -> Node:
        # De Morgan: AB = NOR(A',B').
        return self.gate(self.invert(left), self.invert(right))

    def logical_xnor(self, left: Node, right: Node) -> Node:
        # Canonical four-NOR XNOR.
        p = self.gate(left, right)
        q = self.gate(left, p)
        r = self.gate(right, p)
        return self.gate(q, r)

    def logical_xor(self, left: Node, right: Node) -> Node:
        # Five-NOR XOR = four-NOR XNOR + one NOR inverter.
        return self.invert(self.logical_xnor(left, right))


def map_node_to_nor(node: Node) -> Node:
    factory = _NorFactory()
    memo: dict[tuple, Node] = {}

    def visit(current: Node) -> Node:
        key = _source_key(current)
        if key in memo:
            return memo[key]

        if current.op in {"VAR", "CONST"}:
            result = Node(op=current.op, value=current.value)
        elif current.op == "NOT":
            result = factory.invert(visit(current.left))
        elif current.op == "AND":
            result = factory.logical_and(
                visit(current.left),
                visit(current.right),
            )
        elif current.op == "OR":
            result = factory.logical_or(
                visit(current.left),
                visit(current.right),
            )
        elif current.op == "XOR":
            result = factory.logical_xor(
                visit(current.left),
                visit(current.right),
            )
        elif current.op == "XNOR":
            result = factory.logical_xnor(
                visit(current.left),
                visit(current.right),
            )
        elif current.op == "NOR":
            result = factory.gate(
                visit(current.left),
                visit(current.right),
            )
        else:
            raise ValueError(
                f"Unsupported Boolean operation for NOR mapping: {current.op}"
            )

        memo[key] = result
        return result

    return visit(node)


def map_expression_to_nor(expression: str) -> Node:
    return map_node_to_nor(parse_expression(expression))
