"""BoolNexa NAND-only mapper — polarity-aware and order-stable.

The mapper preserves the user's left-to-right Boolean operand order for visible
signal labels while still reusing physically identical commutative NAND gates.

Example:
    AB + AC'

    N1 = NAND(A, B)       = (AB)'
    N2 = NAND(C, C)       = C'
    N3 = NAND(A, N2)      = (AC')'
    N4 = NAND(N1, N3)     = AB + AC'
"""

from __future__ import annotations

from .boolean_engine import Node, parse_expression


def _key(node: Node) -> tuple:
    if node.op in {"VAR", "CONST"}:
        return (node.op, node.value)
    if node.op == "NOT":
        return ("NOT", _key(node.left))

    left = _key(node.left)
    right = _key(node.right)

    # Structural memoization may regard commutative source expressions as
    # equivalent, but this does not change their display/input order.
    if node.op in {"AND", "OR", "XOR", "XNOR", "NAND", "NOR"} and right < left:
        left, right = right, left

    return (node.op, left, right)


class _NandMapper:
    def __init__(self) -> None:
        self._memo: dict[tuple[tuple, bool], Node] = {}
        self._nand_cache: dict[tuple[int, int], Node] = {}

    def nand(self, left: Node, right: Node) -> Node:
        """Return a shared NAND node without reordering its visible inputs.

        NAND is commutative, so the cache key is order-independent.  However,
        the Node itself preserves the left/right order from the first logical
        construction.  This keeps labels deterministic:
            NAND(A,B) -> (AB)'
        rather than randomly becoming:
            NAND(B,A) -> (BA)'
        based on Python object IDs.
        """
        key = tuple(sorted((id(left), id(right))))
        gate = self._nand_cache.get(key)
        if gate is None:
            gate = Node(op="NAND", left=left, right=right)
            self._nand_cache[key] = gate
        return gate

    def invert(self, value: Node) -> Node:
        return self.nand(value, value)

    def realize(self, node: Node, complemented: bool = False) -> Node:
        memo_key = (_key(node), complemented)
        cached = self._memo.get(memo_key)
        if cached is not None:
            return cached

        if node.op in {"VAR", "CONST"}:
            positive_key = (_key(node), False)
            positive = self._memo.get(positive_key)
            if positive is None:
                positive = Node(op=node.op, value=node.value)
                self._memo[positive_key] = positive
            result = self.invert(positive) if complemented else positive

        elif node.op == "NOT":
            result = self.realize(node.left, not complemented)

        elif node.op == "AND":
            neg = self.nand(
                self.realize(node.left, False),
                self.realize(node.right, False),
            )
            result = neg if complemented else self.invert(neg)

        elif node.op == "OR":
            pos = self.nand(
                self.realize(node.left, True),
                self.realize(node.right, True),
            )
            result = self.invert(pos) if complemented else pos

        elif node.op == "XOR":
            a = self.realize(node.left, False)
            b = self.realize(node.right, False)
            p = self.nand(a, b)
            q = self.nand(a, p)
            r = self.nand(b, p)
            xor = self.nand(q, r)
            result = self.invert(xor) if complemented else xor

        elif node.op == "XNOR":
            xor_node = Node(op="XOR", left=node.left, right=node.right)
            result = self.realize(xor_node, not complemented)

        elif node.op == "NAND":
            raw = self.nand(
                self.realize(node.left, False),
                self.realize(node.right, False),
            )
            result = self.invert(raw) if complemented else raw

        else:
            raise ValueError(
                f"Unsupported Boolean operation for NAND mapping: {node.op}"
            )

        self._memo[memo_key] = result
        return result


def map_node_to_nand(node: Node) -> Node:
    return _NandMapper().realize(node, False)


def map_expression_to_nand(expression: str) -> Node:
    return map_node_to_nand(parse_expression(expression))
