"""Pure geometry helpers for unambiguous simulator wire crossings.

The interactive simulator keeps its original electrical path for hit-testing.
This module derives a *display* path in which a horizontal conductor jumps over
an unrelated vertical conductor.  The vertical conductor is never cut, so a
crossing cannot accidentally look like a junction or a broken net.
"""
from __future__ import annotations

from dataclasses import dataclass
import re

_NUM = r"-?\d+(?:\.\d+)?"
_POINT_RE = re.compile(rf"[ML]\s*({_NUM})\s+({_NUM})")


@dataclass(frozen=True)
class Segment:
    x1: float; y1: float; x2: float; y2: float
    index: int

    @property
    def horizontal(self) -> bool:
        return abs(self.y1 - self.y2) < 1e-6 and abs(self.x1 - self.x2) > 1e-6

    @property
    def vertical(self) -> bool:
        return abs(self.x1 - self.x2) < 1e-6 and abs(self.y1 - self.y2) > 1e-6


def _points(path: str) -> list[tuple[float, float]]:
    return [(float(x), float(y)) for x, y in _POINT_RE.findall(path)]


def _segments(path: str) -> list[Segment]:
    pts = _points(path)
    return [Segment(*pts[i], *pts[i + 1], i) for i in range(len(pts) - 1)]


def _strict_between(v: float, a: float, b: float, margin: float = 5.0) -> bool:
    lo, hi = sorted((a, b))
    return lo + margin < v < hi - margin


def _same_net(a: dict, b: dict) -> bool:
    # Fan-out branches from the exact same source are electrically common and
    # must not be drawn as non-electrical crossings.
    return str(a.get("src_key", "")) == str(b.get("src_key", ""))


def crossing_points(wires: list[dict]) -> dict[int, dict[int, list[float]]]:
    """Return horizontal-segment crossing x positions for each wire.

    Only strict interior H/V intersections of different source nets count.
    Endpoint touches remain ordinary connections/terminations.
    """
    result: dict[int, dict[int, list[float]]] = {}
    for i, a in enumerate(wires):
        for j in range(i + 1, len(wires)):
            b = wires[j]
            if _same_net(a, b):
                continue
            for sa in _segments(str(a.get("d", ""))):
                for sb in _segments(str(b.get("d", ""))):
                    h, v, owner = (sa, sb, i) if sa.horizontal and sb.vertical else ((sb, sa, j) if sb.horizontal and sa.vertical else (None, None, None))
                    if h is None:
                        continue
                    if _strict_between(v.x1, h.x1, h.x2) and _strict_between(h.y1, v.y1, v.y2):
                        result.setdefault(owner, {}).setdefault(h.index, []).append(v.x1)
    return result


def _fmt(v: float) -> str:
    return str(int(v)) if abs(v - round(v)) < 1e-6 else f"{v:.2f}".rstrip("0").rstrip(".")


def _display_path(path: str, jumps: dict[int, list[float]], radius: float = 6.0) -> str:
    pts = _points(path)
    if len(pts) < 2 or not jumps:
        return path
    parts = [f"M {_fmt(pts[0][0])} {_fmt(pts[0][1])}"]
    for idx, ((x1, y1), (x2, y2)) in enumerate(zip(pts, pts[1:])):
        xs = sorted(set(jumps.get(idx, [])), reverse=x2 < x1)
        if abs(y1 - y2) < 1e-6 and xs:
            direction = 1.0 if x2 > x1 else -1.0
            for cx in xs:
                before = cx - direction * radius
                after = cx + direction * radius
                parts.append(f"L {_fmt(before)} {_fmt(y1)}")
                # A compact upward schematic jump. Vertical conductor remains
                # continuous underneath this arc.
                parts.append(
                    f"C {_fmt(cx - direction * radius * 0.55)} {_fmt(y1 - radius)} "
                    f"{_fmt(cx + direction * radius * 0.55)} {_fmt(y1 - radius)} "
                    f"{_fmt(after)} {_fmt(y1)}"
                )
            parts.append(f"L {_fmt(x2)} {_fmt(y2)}")
        else:
            parts.append(f"L {_fmt(x2)} {_fmt(y2)}")
    return " ".join(parts)


def add_crossing_bridges(wires: list[dict]) -> list[dict]:
    """Populate ``display_d`` without altering the electrical/hit-test path."""
    crossings = crossing_points(wires)
    for idx, wire in enumerate(wires):
        wire["display_d"] = _display_path(str(wire.get("d", "")), crossings.get(idx, {}))
    return wires
