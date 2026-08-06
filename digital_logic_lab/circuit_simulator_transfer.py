"""Transfer generated BoolNexa circuits into the interactive simulator.

This module deliberately transfers the *graph*, not the rendered SVG.  It is
kept pure so the generator, simulator and tests can share the same contract.
"""

from __future__ import annotations

from copy import deepcopy

from .circuit_layout import layout_circuit
from .gate import CircuitGraph, GateKind
from .circuit_visual_model import _compact_internal_labels, _signal_labels

_SIMULATOR_GATE_KINDS = {
    GateKind.INPUT,
    GateKind.NOT,
    GateKind.AND,
    GateKind.NAND,
    GateKind.OR,
    GateKind.NOR,
    GateKind.XOR,
    GateKind.XNOR,
    GateKind.OUTPUT,
}


def _blank_gate(gate_type: str, *, x: int, y: int, label: str, num_inputs: int) -> dict:
    gate = {
        "type": gate_type,
        "value": 0,
        "value_bar": 1,
        "num_inputs": num_inputs,
        "x": int(x),
        "y": int(y),
        "label": label,
        "prev_clk": 0,
        "clock_mode": "manual",
        "clock_interval": 1,
        "seg_a": 0,
        "seg_b": 0,
        "seg_c": 0,
        "seg_d": 0,
        "seg_e": 0,
        "seg_f": 0,
        "seg_g": 0,
        "hex_char": "0",
        "outputs": {},
    }
    for idx in range(1, max(7, num_inputs + 1)):
        gate[f"input{idx}_src"] = ""
    return gate


def circuit_graph_to_simulator_project(graph: CircuitGraph) -> dict:
    """Return simulator project data for a generated combinational graph.

    The generated circuit's topology is preserved exactly, including duplicate
    physical inputs on NAND/NOR gates used as inverters.
    """
    unsupported = sorted(
        node.kind.value for node in graph.nodes if node.kind not in _SIMULATOR_GATE_KINDS
    )
    if unsupported:
        raise ValueError(
            "Simulator transfer does not yet support generated node kind(s): "
            + ", ".join(sorted(set(unsupported)))
        )

    layout = layout_circuit(graph)
    positions = {node.id: node for node in layout.nodes}
    semantic_labels = _signal_labels(graph)
    display_labels = _compact_internal_labels(graph, semantic_labels)
    gates: dict[str, dict] = {}
    gate_keys: list[str] = []

    for node in graph.nodes:
        gate_type = node.kind.value
        num_inputs = len(node.inputs)
        if node.kind == GateKind.INPUT:
            num_inputs = 0
        elif node.kind == GateKind.OUTPUT:
            num_inputs = 1
        elif node.kind == GateKind.NOT:
            num_inputs = 1
        elif node.kind in {GateKind.XOR, GateKind.XNOR}:
            num_inputs = 2
        else:
            num_inputs = max(2, num_inputs)

        pos = positions[node.id]
        gate = _blank_gate(
            gate_type,
            x=pos.x,
            y=pos.y,
            label=(node.label if node.kind in {GateKind.INPUT, GateKind.OUTPUT} else display_labels.get(node.id, "")),
            num_inputs=num_inputs,
        )
        gate["generated_expression"] = semantic_labels.get(node.id, node.label)
        gate["generated_net"] = display_labels.get(node.id, "")
        gates[node.id] = gate
        gate_keys.append(node.id)

    for wire in graph.wires:
        target = gates[wire.target]
        slot = wire.target_input + 1
        target[f"input{slot}_src"] = wire.source

    return {
        "gates": deepcopy(gates),
        "gate_keys": gate_keys,
        "wire_offsets": {},
        "annotations": {},
        "annotation_keys": [],
    }
