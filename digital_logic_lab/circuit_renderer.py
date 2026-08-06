"""Serialization helpers for circuit UI and future SVG export."""
from __future__ import annotations
from .circuit_layout import CircuitLayout
from .gate import CircuitGraph

def serialize_circuit(graph: CircuitGraph, layout: CircuitLayout) -> dict[str, object]:
    return {
        "expression":graph.normalized_expression,
        "variables":list(graph.variables),
        "statistics":{"variables":graph.statistics.variables,"inputs":graph.statistics.inputs,"outputs":graph.statistics.outputs,
                      "total_gates":graph.statistics.total_gates,"logic_depth":graph.statistics.logic_depth,"counts":dict(graph.statistics.counts)},
        "width":layout.width,"height":layout.height,
        "nodes":[{"id":n.id,"kind":n.kind,"label":n.label,"expression":n.expression,"level":n.level,"x":n.x,"y":n.y,"width":n.width,"height":n.height} for n in layout.nodes],
        "wires":[{"source":w.source,"target":w.target,"points":[{"x":x,"y":y} for x,y in w.points]} for w in layout.wires],
    }
