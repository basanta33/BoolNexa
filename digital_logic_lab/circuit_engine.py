"""BoolNexa circuit engine v1.5.

Preserves the structural parse tree of ordinary user expressions while also
supporting shared subgraphs deliberately created by technology mappers.

Rule:
- distinct Node objects remain distinct gates;
- the exact same Node object reused by a mapper becomes one shared gate
  with fan-out.

This lets a four-NAND XOR really contain four NAND gates without globally
deduplicating ordinary student-entered expressions.
"""

from __future__ import annotations

from collections import Counter

from .boolean_engine import Node, parse_expression, variables_for
from .circuit_graph import validate_circuit
from .gate import CircuitGraph, CircuitStatistics, GateKind, GateNode, Wire


_OPERATION_KIND = {
    "NOT": GateKind.NOT,
    "AND": GateKind.AND,
    "OR": GateKind.OR,
    "XOR": GateKind.XOR,
    "XNOR": GateKind.XNOR,
    "NAND": GateKind.NAND,
    "NOR": GateKind.NOR,
}


class _Builder:
    def __init__(self) -> None:
        self.nodes: list[GateNode] = []
        self.wires: list[Wire] = []
        self.input_ids: dict[str, str] = {}
        self.constant_ids: dict[str, str] = {}
        self.object_ids: dict[int, str] = {}
        self.counter = 0

    def _next_id(self, prefix: str) -> str:
        self.counter += 1
        return f"{prefix.lower()}_{self.counter:03d}"

    def _find(self, node_id: str) -> GateNode:
        for node in self.nodes:
            if node.id == node_id:
                return node
        raise KeyError(node_id)

    def build_node(self, node: Node) -> str:
        object_key = id(node)
        if object_key in self.object_ids:
            return self.object_ids[object_key]

        if node.op == "VAR":
            if node.value in self.input_ids:
                node_id = self.input_ids[node.value]
                self.object_ids[object_key] = node_id
                return node_id
            node_id = f"input_{node.value}"
            gate = GateNode(
                node_id, GateKind.INPUT, node.value, node.value, (), 0
            )
            self.nodes.append(gate)
            self.input_ids[node.value] = node_id
            self.object_ids[object_key] = node_id
            return node_id

        if node.op == "CONST":
            if node.value in self.constant_ids:
                node_id = self.constant_ids[node.value]
                self.object_ids[object_key] = node_id
                return node_id
            node_id = f"const_{node.value}"
            gate = GateNode(
                node_id, GateKind.CONSTANT, node.value, node.value, (), 0
            )
            self.nodes.append(gate)
            self.constant_ids[node.value] = node_id
            self.object_ids[object_key] = node_id
            return node_id

        if node.op == "NOT":
            source = self.build_node(node.left)
            source_node = self._find(source)
            node_id = self._next_id("not")
            gate = GateNode(
                node_id,
                GateKind.NOT,
                "NOT",
                node.display(),
                (source,),
                source_node.level + 1,
            )
            self.nodes.append(gate)
            self.wires.append(Wire(source, node_id, 0))
            self.object_ids[object_key] = node_id
            return node_id

        if node.op not in _OPERATION_KIND:
            raise ValueError(f"Unsupported Boolean operation: {node.op}")

        left = self.build_node(node.left)
        right = self.build_node(node.right)
        kind = _OPERATION_KIND[node.op]
        node_id = self._next_id(kind.value)
        gate = GateNode(
            id=node_id,
            kind=kind,
            label=kind.value,
            expression=node.display(),
            inputs=(left, right),
            level=max(self._find(left).level, self._find(right).level) + 1,
        )
        self.nodes.append(gate)
        self.wires.append(Wire(left, node_id, 0))
        self.wires.append(Wire(right, node_id, 1))
        self.object_ids[object_key] = node_id
        return node_id


def build_circuit_from_node(
    root: Node,
    *,
    source_expression: str | None = None,
    output_label: str = "F",
) -> CircuitGraph:
    normalized = root.display()
    variables = variables_for(root)

    builder = _Builder()
    root_id = builder.build_node(root)
    root_node = builder._find(root_id)

    output_id = "output_F"
    output = GateNode(
        id=output_id,
        kind=GateKind.OUTPUT,
        label=output_label,
        expression=normalized,
        inputs=(root_id,),
        level=root_node.level + 1,
    )
    builder.nodes.append(output)
    builder.wires.append(Wire(root_id, output_id, 0))

    gate_counts = Counter(
        node.kind.value
        for node in builder.nodes
        if node.kind
        not in {GateKind.INPUT, GateKind.CONSTANT, GateKind.OUTPUT}
    )

    graph = CircuitGraph(
        expression=(
            source_expression
            if source_expression is not None
            else normalized
        ),
        normalized_expression=normalized,
        variables=variables,
        nodes=builder.nodes,
        wires=builder.wires,
        output_node=output_id,
        statistics=CircuitStatistics(
            variables=len(variables),
            inputs=sum(
                node.kind == GateKind.INPUT for node in builder.nodes
            ),
            outputs=1,
            total_gates=sum(gate_counts.values()),
            logic_depth=root_node.level,
            counts=dict(sorted(gate_counts.items())),
        ),
    )
    validate_circuit(graph)
    return graph


def build_circuit(
    expression: str,
    *,
    output_label: str = "F",
) -> CircuitGraph:
    return build_circuit_from_node(
        parse_expression(expression),
        source_expression=expression,
        output_label=output_label,
    )
