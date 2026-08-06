"""BoolNexa Sprint 6.5.2 — XOR/XNOR decomposition and basic-gate mapping.

This module performs technology-independent Boolean-node rewriting before
the circuit graph is built. It does not modify the user's source expression.

Current mapping rules:
- XOR is kept when allowed.
- XOR is decomposed to AND/OR/NOT when XOR is disallowed.
- XNOR is kept when allowed.
- XNOR is decomposed to AND/OR/NOT when XNOR is disallowed.
- If the chosen policy cannot realize a required operation, a clear error
  is raised instead of silently introducing a forbidden gate.
"""

from __future__ import annotations

from .boolean_engine import Node, parse_expression
from .gate import GateKind
from .realization_policy import RealizationPolicy


class RealizationError(ValueError):
    """Raised when a Boolean function cannot be realized under a policy."""


def _not(node: Node) -> Node:
    return Node(op="NOT", left=node)


def _and(left: Node, right: Node) -> Node:
    return Node(op="AND", left=left, right=right)


def _or(left: Node, right: Node) -> Node:
    return Node(op="OR", left=left, right=right)


def _xor(left: Node, right: Node) -> Node:
    return Node(op="XOR", left=left, right=right)


def _xnor(left: Node, right: Node) -> Node:
    return Node(op="XNOR", left=left, right=right)


def _clone(node: Node | None) -> Node | None:
    if node is None:
        return None
    return Node(
        op=node.op,
        value=getattr(node, "value", None),
        left=_clone(getattr(node, "left", None)),
        right=_clone(getattr(node, "right", None)),
    )


def _basic_xor(left: Node, right: Node) -> Node:
    """A XOR B = A'B + AB'."""
    return _or(
        _and(_not(_clone(left)), _clone(right)),
        _and(_clone(left), _not(_clone(right))),
    )


def _basic_xnor(left: Node, right: Node) -> Node:
    """A XNOR B = AB + A'B'."""
    return _or(
        _and(_clone(left), _clone(right)),
        _and(_not(_clone(left)), _not(_clone(right))),
    )


def _require(policy: RealizationPolicy, *kinds: GateKind) -> None:
    missing = [kind for kind in kinds if not policy.allows(kind)]
    if missing:
        names = ", ".join(kind.value for kind in missing)
        raise RealizationError(
            "Selected gate policy cannot realize this function with the "
            f"currently implemented mapper. Missing allowed gate(s): {names}."
        )


def map_node_to_policy(node: Node, policy: RealizationPolicy) -> Node:
    """Return a rewritten Boolean node tree that obeys the gate policy."""

    if node.op in {"VAR", "CONST"}:
        return _clone(node)

    if node.op == "NOT":
        child = map_node_to_policy(node.left, policy)
        if policy.allows(GateKind.NOT):
            return _not(child)
        if policy.allows(GateKind.NAND) or policy.allows(GateKind.NOR):
            raise RealizationError(
                "NOT through universal gates is handled by the dedicated "
                "NAND/NOR technology mapper."
            )
        raise RealizationError(
            "NOT is required but is not allowed by the selected policy."
        )

    if node.op == "AND":
        left = map_node_to_policy(node.left, policy)
        right = map_node_to_policy(node.right, policy)
        if policy.allows(GateKind.AND):
            return _and(left, right)
        raise RealizationError(
            "AND is required but is not allowed by the selected policy."
        )

    if node.op == "OR":
        left = map_node_to_policy(node.left, policy)
        right = map_node_to_policy(node.right, policy)
        if policy.allows(GateKind.OR):
            return _or(left, right)
        raise RealizationError(
            "OR is required but is not allowed by the selected policy."
        )

    if node.op == "XOR":
        left = map_node_to_policy(node.left, policy)
        right = map_node_to_policy(node.right, policy)
        if policy.allows(GateKind.XOR):
            return _xor(left, right)
        _require(policy, GateKind.AND, GateKind.OR, GateKind.NOT)
        return _basic_xor(left, right)

    if node.op == "XNOR":
        left = map_node_to_policy(node.left, policy)
        right = map_node_to_policy(node.right, policy)
        if policy.allows(GateKind.XNOR):
            return _xnor(left, right)
        _require(policy, GateKind.AND, GateKind.OR, GateKind.NOT)
        return _basic_xnor(left, right)

    raise RealizationError(
        f"Unsupported Boolean operation for mapping: {node.op}"
    )


def map_expression_to_policy(
    expression: str,
    policy: RealizationPolicy,
) -> Node:
    return map_node_to_policy(parse_expression(expression), policy)
