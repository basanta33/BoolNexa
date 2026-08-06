"""Data models for BoolNexa logic circuits."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class GateKind(str, Enum):
    INPUT="INPUT"; CONSTANT="CONSTANT"; BUFFER="BUFFER"; NOT="NOT"
    AND="AND"; OR="OR"; XOR="XOR"; NAND="NAND"; NOR="NOR"; XNOR="XNOR"; OUTPUT="OUTPUT"

@dataclass(frozen=True)
class GateNode:
    id: str
    kind: GateKind
    label: str
    expression: str
    inputs: tuple[str, ...] = ()
    level: int = 0

@dataclass(frozen=True)
class Wire:
    source: str
    target: str
    target_input: int

@dataclass(frozen=True)
class CircuitStatistics:
    variables: int
    inputs: int
    outputs: int
    total_gates: int
    logic_depth: int
    counts: dict[str, int]

@dataclass(frozen=True)
class CircuitGraph:
    expression: str
    normalized_expression: str
    variables: list[str]
    nodes: list[GateNode]
    wires: list[Wire]
    output_node: str
    statistics: CircuitStatistics
    def node_by_id(self, node_id: str) -> GateNode:
        for node in self.nodes:
            if node.id == node_id:
                return node
        raise KeyError(node_id)
