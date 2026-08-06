"""BoolNexa circuit layout v1.3 — obstacle-aware, net-safe wiring.

The layout layer owns geometry only. Boolean synthesis/topology is intentionally
left untouched here.

Permanent drawing invariants:
- orthogonal wires only;
- wires never pass through unrelated gate bodies;
- different logical nets may cross but never share a fan-out trunk;
- every real gate input/output has at least a 10 px horizontal straight run;
- OR/NOR/XOR/XNOR inputs use a 14 px straight approach for curve clearance;
- NAND/NOR/XNOR bubbles are contacted at their visible boundary.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass

from .circuit_router import Rect, route_orthogonal
from .gate import CircuitGraph, GateKind


@dataclass(frozen=True)
class PositionedNode:
    id: str
    kind: str
    label: str
    expression: str
    level: int
    x: int
    y: int
    width: int
    height: int


@dataclass(frozen=True)
class RoutedWire:
    source: str
    target: str
    points: tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class CircuitLayout:
    width: int
    height: int
    nodes: list[PositionedNode]
    wires: list[RoutedWire]


def _target_pin_y(target: PositionedNode, target_input: int, input_count: int) -> int:
    if input_count <= 1:
        return target.y + target.height // 2
    top = target.y + int(target.height * 0.28)
    bottom = target.y + int(target.height * 0.72)
    if input_count == 2:
        return top if target_input == 0 else bottom
    return round(top + (bottom - top) * target_input / (input_count - 1))


def _source_point(source: PositionedNode) -> tuple[int, int]:
    """Return the true visible output connection point for a node."""
    x = source.x + source.width
    # NAND/NOR/XNOR bodies reserve 7 px for the output bubble, while the
    # rendered r=4 bubble extends one pixel beyond the nominal node width.
    if source.kind in {"NAND", "NOR", "XNOR"}:
        x += 1
    return x, source.y + source.height // 2


def _cubic(value0: float, control1: float, control2: float, value3: float, t: float) -> float:
    u = 1.0 - t
    return (
        u * u * u * value0
        + 3.0 * u * u * t * control1
        + 3.0 * u * t * t * control2
        + t * t * t * value3
    )


def _or_input_boundary_x(target: PositionedNode, pin_y: int) -> int:
    """X coordinate where a horizontal input meets the rendered OR-family curve.

    Uses the same rear cubic Bezier curve as circuit_svg_renderer._or_svg.
    """
    x, y, w, h = target.x, target.y, target.width, target.height
    bubble = 7 if target.kind in {"NOR", "XNOR"} else 0
    body_w = w - bubble

    y0, y1, y2, y3 = y + h, y + h * 0.68, y + h * 0.32, y
    x0, x1, x2, x3 = x + 4, x + body_w * 0.22, x + body_w * 0.22, x + 4

    lo, hi = 0.0, 1.0
    for _ in range(28):
        t = (lo + hi) / 2.0
        curve_y = _cubic(y0, y1, y2, y3, t)
        if curve_y > pin_y:
            lo = t
        else:
            hi = t
    t = (lo + hi) / 2.0
    return round(_cubic(x0, x1, x2, x3, t))


def _target_point(
    target: PositionedNode,
    target_input: int,
    input_count: int,
) -> tuple[int, int]:
    """Return the true visible gate-boundary input point."""
    pin_y = _target_pin_y(target, target_input, input_count)
    if target.kind in {"OR", "NOR", "XOR", "XNOR"}:
        return _or_input_boundary_x(target, pin_y), pin_y
    return target.x, pin_y


GATE_PORT_STRAIGHT = 10
OR_FAMILY_INPUT_STRAIGHT = 14
FANOUT_TRUNK_BASE = 28
FANOUT_NET_LANE_SPACING = 18


def _is_gate(node: PositionedNode) -> bool:
    return node.kind not in {"INPUT", "OUTPUT", "CONSTANT"}


def _source_stub(source: PositionedNode, start: tuple[int, int]) -> tuple[int, int]:
    """Mandatory straight output run for real gates; external pins are exempt."""
    if not _is_gate(source):
        return start
    return start[0] + GATE_PORT_STRAIGHT, start[1]


def _target_stub(target: PositionedNode, end: tuple[int, int]) -> tuple[int, int]:
    """Mandatory straight input run for real gates; external pins are exempt."""
    if not _is_gate(target):
        return end
    straight = OR_FAMILY_INPUT_STRAIGHT if target.kind in {"OR", "NOR", "XOR", "XNOR"} else GATE_PORT_STRAIGHT
    return end[0] - straight, end[1]


def _obstacles(
    positioned: list[PositionedNode],
    source_id: str,
    target_id: str,
    clearance: int = 14,
) -> list[Rect]:
    result = []
    for node in positioned:
        if node.id in {source_id, target_id}:
            continue
        # INPUT/OUTPUT labels are presentation pins, not gate bodies.
        if node.kind in {"INPUT", "OUTPUT", "CONSTANT"}:
            continue
        result.append(
            Rect(
                node.x,
                node.y,
                node.x + node.width,
                node.y + node.height,
            ).inflated(clearance)
        )
    return result


def _fanout_lane_by_source(
    positioned: list[PositionedNode],
    fanout_counts: Counter,
) -> dict[str, int]:
    """Assign deterministic, distinct X lanes to independent fan-out nets.

    Previously every source at the same level used the same ``start.x + 28``
    trunk. Two independent inputs such as A and B could therefore render on
    top of one another and appear electrically shorted. The lane is assigned
    per *source net*, so branches from one source still share their trunk while
    unrelated sources can never occupy that same vertical trunk line.
    """
    fanout_sources = [
        node for node in positioned
        if fanout_counts.get(node.id, 0) > 1
    ]
    fanout_sources.sort(key=lambda node: (node.level, node.y, node.x, node.id))

    lanes: dict[str, int] = {}
    per_level: dict[int, int] = defaultdict(int)
    for node in fanout_sources:
        lanes[node.id] = per_level[node.level]
        per_level[node.level] += 1
    return lanes


def layout_circuit(
    graph: CircuitGraph,
    *,
    horizontal_spacing: int = 205,
    vertical_spacing: int = 118,
    margin_x: int = 55,
    margin_y: int = 45,
) -> CircuitLayout:
    levels: dict[int, list] = defaultdict(list)
    for node in graph.nodes:
        levels[node.level].append(node)

    maximum_rows = max((len(nodes) for nodes in levels.values()), default=1)
    positioned: list[PositionedNode] = []
    lookup: dict[str, PositionedNode] = {}

    for level in sorted(levels):
        nodes = sorted(
            levels[level],
            key=lambda node: (
                0 if node.kind == GateKind.INPUT else 1,
                node.label,
                node.id,
            ),
        )
        total_height = (len(nodes) - 1) * vertical_spacing
        available_height = (maximum_rows - 1) * vertical_spacing
        start_y = margin_y + max(0, available_height - total_height) // 2

        for index, node in enumerate(nodes):
            width = 62 if node.kind in {GateKind.INPUT, GateKind.OUTPUT} else 78
            height = (
                56
                if node.kind in {
                    GateKind.AND, GateKind.OR, GateKind.XOR,
                    GateKind.NAND, GateKind.NOR, GateKind.XNOR,
                }
                else 46
            )
            item = PositionedNode(
                id=node.id,
                kind=node.kind.value,
                label=node.label,
                expression=node.expression,
                level=node.level,
                x=margin_x + level * horizontal_spacing,
                y=start_y + index * vertical_spacing,
                width=width,
                height=height,
            )
            positioned.append(item)
            lookup[item.id] = item

    fanout_counts = Counter(w.source for w in graph.wires)
    fanout_index: dict[str, int] = defaultdict(int)
    fanout_lanes = _fanout_lane_by_source(positioned, fanout_counts)

    routed: list[RoutedWire] = []
    for wire in graph.wires:
        source = lookup[wire.source]
        target = lookup[wire.target]
        target_node = graph.node_by_id(wire.target)
        start = _source_point(source)
        end = _target_point(target, wire.target_input, len(target_node.inputs))

        obstacles = _obstacles(positioned, wire.source, wire.target)

        # Permanent 10 px port invariant.
        route_start = _source_stub(source, start)
        route_end = _target_stub(target, end)

        if fanout_counts[wire.source] > 1:
            lane = fanout_lanes[wire.source]
            trunk_x = max(
                route_start[0],
                start[0] + FANOUT_TRUNK_BASE + lane * FANOUT_NET_LANE_SPACING,
            )
            idx = fanout_index[wire.source]
            fanout_index[wire.source] += 1

            trunk = (trunk_x, route_start[1])
            branch_start = (trunk_x, route_end[1])

            tail = route_orthogonal(
                branch_start,
                route_end,
                obstacles,
                extra_x=[trunk_x + 18 + idx * 8, route_end[0] - 24],
            )
            core = [route_start, trunk, branch_start, *tail[1:]]
        else:
            core = list(
                route_orthogonal(
                    route_start,
                    route_end,
                    obstacles,
                    extra_x=[route_start[0] + 30, route_end[0] - 30],
                )
            )

        # Never compress away mandatory port stubs.
        points_list = [start]
        if route_start != start:
            points_list.append(route_start)
        points_list.extend(core[1:] if core and core[0] == route_start else core)
        if route_end != end:
            if not points_list or points_list[-1] != route_end:
                points_list.append(route_end)
            points_list.append(end)
        elif not points_list or points_list[-1] != end:
            points_list.append(end)

        routed.append(RoutedWire(wire.source, wire.target, tuple(points_list)))

    max_level = max((node.level for node in graph.nodes), default=0)
    return CircuitLayout(
        width=margin_x * 2 + max_level * horizontal_spacing + 120,
        height=margin_y * 2 + max(1, maximum_rows - 1) * vertical_spacing + 80,
        nodes=positioned,
        wires=routed,
    )
