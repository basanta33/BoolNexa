"""Presentation model for BoolNexa logic-circuit diagrams.

Visible-schematic rules:
- keep circuit topology untouched;
- use ordinary BoolNexa Boolean notation, never NAND/NOR arrow notation;
- show the original user function on the final output wire;
- place signal labels in clear space, away from gate bodies and wire strokes.
"""

from __future__ import annotations

from dataclasses import dataclass

from .boolean_engine import parse_expression
from .circuit_engine import build_circuit
from .circuit_layout import CircuitLayout, RoutedWire, layout_circuit
from .gate import CircuitGraph, GateKind


@dataclass(frozen=True)
class CircuitVisualNode:
    id: str
    kind: str
    label: str
    expression: str
    x: int
    y: int
    width: int
    height: int


@dataclass(frozen=True)
class CircuitVisualWire:
    source: str
    target: str
    path: str
    label: str
    label_x: float
    label_y: float


@dataclass(frozen=True)
class CircuitVisual:
    expression: str
    width: int
    height: int
    nodes: list[CircuitVisualNode]
    wires: list[CircuitVisualWire]
    crossings: list[tuple[float, float]]
    total_gates: int
    logic_depth: int
    gate_counts: dict[str, int]


def _path(points: tuple[tuple[int, int], ...]) -> str:
    if not points:
        return ""
    pieces = [f"M {points[0][0]} {points[0][1]}"]
    for x, y in points[1:]:
        pieces.append(f"L {x} {y}")
    return " ".join(pieces)


def _label_box(label: str, x: float, baseline_y: float) -> tuple[float, float, float, float]:
    """Conservative SVG text box estimate for collision testing."""
    width = max(10.0, len(label) * 7.4 + 8.0)
    height = 16.0
    return (
        x - width / 2.0,
        baseline_y - 12.0,
        x + width / 2.0,
        baseline_y + 4.0,
    )


def _boxes_overlap(
    first: tuple[float, float, float, float],
    second: tuple[float, float, float, float],
    padding: float = 0.0,
) -> bool:
    return not (
        first[2] + padding <= second[0]
        or second[2] + padding <= first[0]
        or first[3] + padding <= second[1]
        or second[3] + padding <= first[1]
    )


def _segment_hits_box(
    a: tuple[int, int],
    b: tuple[int, int],
    box: tuple[float, float, float, float],
    padding: float = 3.0,
) -> bool:
    left, top, right, bottom = box
    left -= padding
    top -= padding
    right += padding
    bottom += padding
    x1, y1 = a
    x2, y2 = b

    if y1 == y2:
        low, high = sorted((x1, x2))
        return top < y1 < bottom and max(low, left) < min(high, right)
    if x1 == x2:
        low, high = sorted((y1, y2))
        return left < x1 < right and max(low, top) < min(high, bottom)
    return False


def _gate_boxes(layout: CircuitLayout) -> list[tuple[float, float, float, float]]:
    boxes = []
    for node in layout.nodes:
        if node.kind in {"INPUT", "OUTPUT", "CONSTANT"}:
            continue
        # Small visual clearance prevents text appearing to touch the gate.
        boxes.append((node.x - 5, node.y - 5, node.x + node.width + 5, node.y + node.height + 5))
    return boxes


def _best_label_position(
    label: str,
    wire: RoutedWire,
    layout: CircuitLayout,
    occupied_labels: list[tuple[float, float, float, float]],
) -> tuple[float, float]:
    """Choose a collision-free signal-label position.

    Labels are treated as schematic objects, not decoration: their estimated
    text boxes may not overlap a gate body, any routed wire, or a previously
    placed signal label.  The search keeps the circuit topology/layout fixed
    and moves only the text.
    """
    if not label:
        return 0.0, 0.0

    horizontal: list[tuple[float, float, float]] = []
    for (x1, y1), (x2, y2) in zip(wire.points, wire.points[1:]):
        if y1 == y2 and x1 != x2:
            left, right = sorted((float(x1), float(x2)))
            horizontal.append((right - left, left, right))
    horizontal.sort(reverse=True)

    gate_boxes = _gate_boxes(layout)
    all_segments = [
        (a, b)
        for routed in layout.wires
        for a, b in zip(routed.points, routed.points[1:])
    ]

    def clear(x: float, baseline_y: float) -> bool:
        box = _label_box(label, x, baseline_y)
        # Keep the complete text inside the schematic viewport.
        if box[0] < 4 or box[2] > layout.width - 4:
            return False
        if box[1] < 4 or box[3] > layout.height - 4:
            return False
        if any(_boxes_overlap(box, gate_box, padding=3.0) for gate_box in gate_boxes):
            return False
        if any(_boxes_overlap(box, existing, padding=5.0) for existing in occupied_labels):
            return False
        if any(_segment_hits_box(a, b, box, padding=4.0) for a, b in all_segments):
            return False
        occupied_labels.append(box)
        return True

    # Search progressively farther above/below each horizontal run.  Long
    # expressions often cannot physically fit in the inter-gate gap, so the
    # wider offsets deliberately place them in a clear annotation lane while
    # leaving gates and wires untouched.
    vertical_offsets = (
        -12.0, 18.0, -28.0, 34.0, -44.0, 50.0,
        -60.0, 66.0, -76.0, 82.0, -92.0, 98.0,
        -108.0, 114.0, -124.0, 130.0,
    )

    for _, left, right in horizontal:
        center = (left + right) / 2.0
        # Center is preferred.  Quarter-point anchors are useful for long
        # labels when another nearby wire occupies the center lane.
        anchors = (
            center,
            left + (right - left) * 0.35,
            left + (right - left) * 0.65,
        )
        y = next(
            float(y1)
            for (x1, y1), (x2, y2) in zip(wire.points, wire.points[1:])
            if y1 == y2 and x1 != x2
            and abs(min(x1, x2) - left) < 0.01
            and abs(max(x1, x2) - right) < 0.01
        )
        for offset in vertical_offsets:
            for x in anchors:
                candidate_y = y + offset
                if clear(x, candidate_y):
                    return x, candidate_y

    # A vertical-only path is unusual, but search around its midpoint using
    # the same strict collision rules.
    if wire.points:
        x, y = wire.points[len(wire.points) // 2]
        for dx in (18.0, -18.0, 36.0, -36.0, 54.0, -54.0):
            for dy in (-16.0, 20.0, -36.0, 40.0, -56.0, 60.0):
                if clear(float(x) + dx, float(y) + dy):
                    return float(x) + dx, float(y) + dy

    # Last-resort deterministic scan over empty schematic space.  This is
    # preferable to knowingly drawing text over a gate or conductor.
    width = _label_box(label, 0.0, 0.0)[2] - _label_box(label, 0.0, 0.0)[0]
    x0 = max(width / 2.0 + 6.0, 10.0)
    x1 = layout.width - width / 2.0 - 6.0
    if x0 <= x1:
        y_values = list(range(20, max(21, layout.height - 8), 14))
        for baseline_y in y_values:
            x = x0
            while x <= x1:
                if clear(x, float(baseline_y)):
                    return x, float(baseline_y)
                x += 18.0

    # Extremely defensive fallback: retain a deterministic coordinate.  The
    # normal candidate/scan paths above are expected to resolve all supported
    # BoolNexa circuits and regression tests enforce the known dense cases.
    if horizontal:
        _, left, right = horizontal[0]
        return (left + right) / 2.0, 12.0
    if wire.points:
        x, _ = wire.points[0]
        return float(x), 12.0
    return 0.0, 12.0

def _source_expression(expression: str) -> str:
    """Normalize the user's expression using BoolNexa's visible notation."""
    try:
        text = parse_expression(expression).display()
    except Exception:
        text = expression
    return text.replace("·", "")


def _needs_grouping(label: str) -> bool:
    return any(token in label for token in (" + ", " ⊕ "))


def _factor(label: str) -> str:
    return f"({label})" if _needs_grouping(label) else label


def _complement(label: str) -> str:
    atomic_identifier = (
        label.replace("_", "").isalnum()
        and " " not in label
        and not (
            len(label) > 1
            and label.isalpha()
            and label.isupper()
        )
    )

    if len(label) == 1 or atomic_identifier:
        return f"{label}'"
    return f"({label})'"


def _product(left: str, right: str) -> str:
    return f"{_factor(left)}{_factor(right)}"


def _sum(left: str, right: str) -> str:
    return f"{left} + {right}"


def _xor(left: str, right: str) -> str:
    return f"{left} ⊕ {right}"


def _signal_labels(graph: CircuitGraph) -> dict[str, str]:
    """Compute human-readable signal names from graph semantics."""
    labels: dict[str, str] = {}

    for node in sorted(graph.nodes, key=lambda item: item.level):
        kind = node.kind

        if kind in {GateKind.INPUT, GateKind.CONSTANT}:
            labels[node.id] = node.label
            continue

        if kind == GateKind.OUTPUT:
            labels[node.id] = _source_expression(graph.expression)
            continue

        inputs = [labels[input_id] for input_id in node.inputs]

        if kind == GateKind.BUFFER:
            labels[node.id] = inputs[0]
        elif kind == GateKind.NOT:
            labels[node.id] = _complement(inputs[0])
        elif kind == GateKind.AND:
            labels[node.id] = _product(inputs[0], inputs[1])
        elif kind == GateKind.OR:
            labels[node.id] = _sum(inputs[0], inputs[1])
        elif kind == GateKind.XOR:
            labels[node.id] = _xor(inputs[0], inputs[1])
        elif kind == GateKind.XNOR:
            labels[node.id] = _complement(_xor(inputs[0], inputs[1]))
        elif kind == GateKind.NAND:
            if node.inputs[0] == node.inputs[1]:
                labels[node.id] = _complement(inputs[0])
            else:
                labels[node.id] = _complement(_product(inputs[0], inputs[1]))
        elif kind == GateKind.NOR:
            if node.inputs[0] == node.inputs[1]:
                labels[node.id] = _complement(inputs[0])
            else:
                labels[node.id] = _complement(_sum(inputs[0], inputs[1]))
        else:
            labels[node.id] = node.label

    return labels


def _compact_internal_labels(graph: CircuitGraph, semantic_labels: dict[str, str]) -> dict[str, str]:
    """Use stable short net names on wires while preserving full semantics."""
    compact: dict[str, str] = {}
    index = 1
    for node in sorted(graph.nodes, key=lambda item: (item.level, item.id)):
        if node.kind in {GateKind.INPUT, GateKind.CONSTANT, GateKind.OUTPUT}:
            compact[node.id] = semantic_labels.get(node.id, node.label)
        else:
            compact[node.id] = f"N{index}"
            index += 1
    return compact


def _proper_wire_crossings(layout: CircuitLayout) -> list[tuple[float, float]]:
    """Return non-electrical interior crossings between independent nets.

    A crossing is reported only when a horizontal segment and a vertical
    segment intersect strictly inside *both* segments.  Endpoints are excluded
    so legitimate gate contacts and branch endpoints are never treated as
    crossings.  Wires from the same source net are electrically common and are
    likewise excluded.
    """
    found: set[tuple[int, int]] = set()

    for index, first in enumerate(layout.wires):
        for second in layout.wires[index + 1:]:
            if first.source == second.source:
                continue

            for a1, a2 in zip(first.points, first.points[1:]):
                first_horizontal = a1[1] == a2[1] and a1[0] != a2[0]
                first_vertical = a1[0] == a2[0] and a1[1] != a2[1]
                if not (first_horizontal or first_vertical):
                    continue

                for b1, b2 in zip(second.points, second.points[1:]):
                    second_horizontal = b1[1] == b2[1] and b1[0] != b2[0]
                    second_vertical = b1[0] == b2[0] and b1[1] != b2[1]
                    if first_horizontal == second_horizontal:
                        continue
                    if not (second_horizontal or second_vertical):
                        continue

                    if first_horizontal:
                        h1, h2, v1, v2 = a1, a2, b1, b2
                    else:
                        h1, h2, v1, v2 = b1, b2, a1, a2

                    x = v1[0]
                    y = h1[1]
                    h_left, h_right = sorted((h1[0], h2[0]))
                    v_top, v_bottom = sorted((v1[1], v2[1]))

                    # Strict inequalities deliberately exclude T/end contacts.
                    if h_left < x < h_right and v_top < y < v_bottom:
                        found.add((x, y))

    return [(float(x), float(y)) for x, y in sorted(found, key=lambda p: (p[1], p[0]))]

def build_circuit_visual_from_graph(graph: CircuitGraph) -> CircuitVisual:
    layout = layout_circuit(graph)
    signal_labels = _signal_labels(graph)
    display_labels = _compact_internal_labels(graph, signal_labels)

    wires = []
    occupied_labels: list[tuple[float, float, float, float]] = []
    label_occurrences: dict[str, int] = {}
    for wire in layout.wires:
        label = display_labels.get(wire.source, "")

        target_node = graph.node_by_id(wire.target)
        if target_node.kind == GateKind.OUTPUT:
            label = _source_expression(graph.expression)

        # Generated internal nets are identified once at their source.
        # Primary inputs may remain repeated on branches because A/B/C labels
        # help students follow fan-out.  Output expressions are also shown once.
        occurrence = label_occurrences.get(wire.source, 0)
        label_occurrences[wire.source] = occurrence + 1
        if label.startswith("N") and label[1:].isdigit():
            visible_label = label if occurrence == 0 else ""
        else:
            visible_label = label

        label_x, label_y = _best_label_position(
            visible_label,
            wire,
            layout,
            occupied_labels,
        )

        wires.append(
            CircuitVisualWire(
                source=wire.source,
                target=wire.target,
                path=_path(wire.points),
                label=visible_label,
                label_x=label_x,
                label_y=label_y,
            )
        )

    source_expression = _source_expression(graph.expression)

    return CircuitVisual(
        expression=source_expression,
        width=layout.width,
        height=layout.height,
        nodes=[
            CircuitVisualNode(
                id=node.id,
                kind=node.kind,
                label=node.label,
                expression=signal_labels.get(node.id, node.expression),
                x=node.x,
                y=node.y,
                width=node.width,
                height=node.height,
            )
            for node in layout.nodes
        ],
        wires=wires,
        crossings=_proper_wire_crossings(layout),
        total_gates=graph.statistics.total_gates,
        logic_depth=graph.statistics.logic_depth,
        gate_counts=dict(graph.statistics.counts),
    )


def build_circuit_visual(expression: str) -> CircuitVisual:
    return build_circuit_visual_from_graph(build_circuit(expression))
