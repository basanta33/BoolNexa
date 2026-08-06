"""Obstacle-aware orthogonal router for BoolNexa logic circuits.

Rules:
- never route through a gate body;
- wires may cross other wires;
- crossings are not electrical junctions;
- electrical junction dots are rendered only for actual graph fan-out;
- all wire segments remain horizontal/vertical;\n- gate ports are given mandatory straight stubs by the layout layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Iterable


@dataclass(frozen=True)
class Rect:
    left: int
    top: int
    right: int
    bottom: int

    def inflated(self, margin: int) -> "Rect":
        return Rect(
            self.left - margin,
            self.top - margin,
            self.right + margin,
            self.bottom + margin,
        )


def _point_inside(rect: Rect, p: tuple[int, int]) -> bool:
    x, y = p
    return rect.left < x < rect.right and rect.top < y < rect.bottom


def _segment_hits_rect(
    a: tuple[int, int],
    b: tuple[int, int],
    rect: Rect,
) -> bool:
    """True when segment passes through the interior of rect."""
    x1, y1 = a
    x2, y2 = b

    if x1 == x2:
        x = x1
        if not (rect.left < x < rect.right):
            return False
        low, high = sorted((y1, y2))
        return max(low, rect.top) < min(high, rect.bottom)

    if y1 == y2:
        y = y1
        if not (rect.top < y < rect.bottom):
            return False
        low, high = sorted((x1, x2))
        return max(low, rect.left) < min(high, rect.right)

    raise ValueError("Router only supports orthogonal segments.")


def _clear_segment(
    a: tuple[int, int],
    b: tuple[int, int],
    obstacles: Iterable[Rect],
) -> bool:
    return not any(_segment_hits_rect(a, b, rect) for rect in obstacles)


def compress_orthogonal(points: list[tuple[int, int]]) -> tuple[tuple[int, int], ...]:
    if len(points) <= 2:
        return tuple(points)

    result = [points[0]]
    for point in points[1:]:
        result.append(point)
        while len(result) >= 3:
            a, b, c = result[-3], result[-2], result[-1]
            if (a[0] == b[0] == c[0]) or (a[1] == b[1] == c[1]):
                result.pop(-2)
            else:
                break
    return tuple(result)


def route_orthogonal(
    start: tuple[int, int],
    end: tuple[int, int],
    obstacles: list[Rect],
    *,
    extra_x: Iterable[int] = (),
    extra_y: Iterable[int] = (),
) -> tuple[tuple[int, int], ...]:
    """Find a shortest low-bend Manhattan route around rectangular obstacles."""

    # Build a compact visibility grid from obstacle edges and endpoints.
    xs = {start[0], end[0]}
    ys = {start[1], end[1]}

    for rect in obstacles:
        xs.update((rect.left, rect.right))
        ys.update((rect.top, rect.bottom))

    xs.update(int(v) for v in extra_x)
    ys.update(int(v) for v in extra_y)

    xs = sorted(xs)
    ys = sorted(ys)

    points = [
        (x, y)
        for x in xs
        for y in ys
        if (x, y) in {start, end}
        or not any(_point_inside(rect, (x, y)) for rect in obstacles)
    ]
    point_set = set(points)

    # Connect nearest visible neighbours horizontally and vertically.
    neighbours: dict[tuple[int, int], list[tuple[int, int]]] = {p: [] for p in points}

    by_y: dict[int, list[tuple[int, int]]] = {}
    by_x: dict[int, list[tuple[int, int]]] = {}
    for p in points:
        by_y.setdefault(p[1], []).append(p)
        by_x.setdefault(p[0], []).append(p)

    for group in by_y.values():
        group.sort()
        for a, b in zip(group, group[1:]):
            if _clear_segment(a, b, obstacles):
                neighbours[a].append(b)
                neighbours[b].append(a)

    for group in by_x.values():
        group.sort(key=lambda p: p[1])
        for a, b in zip(group, group[1:]):
            if _clear_segment(a, b, obstacles):
                neighbours[a].append(b)
                neighbours[b].append(a)

    # Dijkstra with a bend penalty to favour textbook-style routes.
    # State keeps previous direction.
    queue: list[tuple[int, int, tuple[int, int], str | None]] = []
    heappush(queue, (0, 0, start, None))
    best: dict[tuple[tuple[int, int], str | None], int] = {(start, None): 0}
    parent: dict[
        tuple[tuple[int, int], str | None],
        tuple[tuple[int, int], str | None] | None,
    ] = {(start, None): None}

    end_state = None
    while queue:
        cost, bends, point, direction = heappop(queue)
        state = (point, direction)
        if best.get(state) != cost:
            continue
        if point == end:
            end_state = state
            break

        for nxt in neighbours[point]:
            new_dir = "H" if nxt[1] == point[1] else "V"
            distance = abs(nxt[0] - point[0]) + abs(nxt[1] - point[1])
            bend = 1 if direction is not None and direction != new_dir else 0
            new_cost = cost + distance + bend * 28
            new_state = (nxt, new_dir)
            if new_cost < best.get(new_state, 10**18):
                best[new_state] = new_cost
                parent[new_state] = state
                heappush(queue, (new_cost, bends + bend, nxt, new_dir))

    if end_state is None:
        # Safe deterministic fallback outside obstacles.
        lane_y = min([start[1], end[1], *(r.top for r in obstacles)] or [0]) - 30
        return compress_orthogonal([start, (start[0], lane_y), (end[0], lane_y), end])

    path = []
    state = end_state
    while state is not None:
        path.append(state[0])
        state = parent[state]
    path.reverse()
    return compress_orthogonal(path)
