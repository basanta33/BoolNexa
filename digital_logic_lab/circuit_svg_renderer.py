"""Professional ANSI/IEEE-style SVG renderer for BoolNexa circuits."""

from __future__ import annotations

from collections import Counter
from html import escape

from .circuit_engine import build_circuit
from .circuit_visual_model import (
    build_circuit_visual,
    build_circuit_visual_from_graph,
)
from .gate import CircuitGraph


def _wire_svg(wire) -> str:
    return f'<path class="wire" d="{escape(wire.path)}" />'


def _wire_label_svg(wire, source_count: int) -> str:
    if not wire.label:
        return ""
    if wire.source.startswith("input_") and source_count <= 1:
        return ""
    return (
        f'<text class="signal-label" x="{wire.label_x}" y="{wire.label_y}" '
        f'text-anchor="middle">{escape(wire.label)}</text>'
    )


def _input_svg(node) -> str:
    cy = node.y + node.height / 2
    return (
        f'<g class="io input">'
        f'<text x="{node.x}" y="{cy + 5}" text-anchor="start">{escape(node.label)}</text>'
        f'<line x1="{node.x + 20}" y1="{cy}" x2="{node.x + node.width}" y2="{cy}" />'
        f'</g>'
    )


def _output_svg(node) -> str:
    cy = node.y + node.height / 2
    return (
        f'<g class="io output">'
        f'<line x1="{node.x}" y1="{cy}" x2="{node.x + node.width - 20}" y2="{cy}" />'
        f'<text x="{node.x + node.width}" y="{cy + 5}" text-anchor="end">{escape(node.label)}</text>'
        f'</g>'
    )


def _and_svg(node, inverted: bool = False) -> str:
    x, y, w, h = node.x, node.y, node.width, node.height
    bubble = 7 if inverted else 0
    bw = w - bubble
    mid = y + h / 2
    right = x + bw
    d = (
        f"M {x} {y} L {x+bw*.48} {y} "
        f"C {x+bw*.83} {y} {right} {y+h*.22} {right} {mid} "
        f"C {right} {y+h*.78} {x+bw*.83} {y+h} {x+bw*.48} {y+h} "
        f"L {x} {y+h} Z"
    )
    extra = (
        f'<circle class="bubble" cx="{right+4}" cy="{mid}" r="4" />'
        if inverted
        else ""
    )
    css_class = "nand" if inverted else "and"
    return (
        f'<g class="gate {css_class}"><path d="{d}" />{extra}'
        f'<title>{escape(node.expression)}</title></g>'
    )


def _or_svg(node, xor: bool = False, inverted: bool = False) -> str:
    x, y, w, h = node.x, node.y, node.width, node.height
    bubble = 7 if inverted else 0
    bw = w - bubble
    right = x + w - bubble
    mid = y + h / 2
    d = (
        f"M {x+4} {y} "
        f"C {x+bw*.35} {y+2} {x+bw*.68} {y+4} {right} {mid} "
        f"C {x+bw*.68} {y+h-4} {x+bw*.35} {y+h-2} {x+4} {y+h} "
        f"C {x+bw*.22} {y+h*.68} {x+bw*.22} {y+h*.32} {x+4} {y} Z"
    )
    xor_line = (
        f'<path class="xor-mark" d="M {x-3} {y+2} '
        f'C {x+bw*.14} {y+h*.32} {x+bw*.14} {y+h*.68} '
        f'{x-3} {y+h-2}" />'
        if xor
        else ""
    )
    extra = (
        f'<circle class="bubble" cx="{right+4}" cy="{mid}" r="4" />'
        if inverted
        else ""
    )
    if xor and inverted:
        css_class = "xnor"
    elif xor:
        css_class = "xor"
    elif inverted:
        css_class = "nor"
    else:
        css_class = "or"
    return (
        f'<g class="gate {css_class}"><path d="{d}" />'
        f'{xor_line}{extra}<title>{escape(node.expression)}</title></g>'
    )


def _not_svg(node) -> str:
    x, y, w, h = node.x, node.y, node.width, node.height
    mid, r = y + h / 2, 5
    tip = x + w - r * 2
    return (
        f'<g class="gate not"><polygon points="{x},{y+4} {x},{y+h-4} {tip},{mid}" />'
        f'<circle class="bubble" cx="{tip+r}" cy="{mid}" r="{r}" />'
        f'<title>{escape(node.expression)}</title></g>'
    )


def _buffer_svg(node) -> str:
    x, y, w, h = node.x, node.y, node.width, node.height
    return (
        f'<g class="gate buffer"><polygon points="{x},{y+4} {x},{y+h-4} {x+w},{y+h/2}" />'
        f'<title>{escape(node.expression)}</title></g>'
    )


def _fallback_svg(node) -> str:
    return (
        f'<g class="gate fallback"><rect x="{node.x}" y="{node.y}" '
        f'width="{node.width}" height="{node.height}" rx="7" />'
        f'<text x="{node.x+node.width/2}" y="{node.y+node.height/2+4}" '
        f'text-anchor="middle">{escape(node.kind)}</text>'
        f'<title>{escape(node.expression)}</title></g>'
    )


def _node_svg(node) -> str:
    kind = node.kind.upper()
    if kind == "INPUT":
        return _input_svg(node)
    if kind == "OUTPUT":
        return _output_svg(node)
    if kind == "AND":
        return _and_svg(node)
    if kind == "NAND":
        return _and_svg(node, inverted=True)
    if kind == "OR":
        return _or_svg(node)
    if kind == "NOR":
        return _or_svg(node, inverted=True)
    if kind == "XOR":
        return _or_svg(node, xor=True)
    if kind == "XNOR":
        return _or_svg(node, xor=True, inverted=True)
    if kind == "NOT":
        return _not_svg(node)
    if kind == "BUFFER":
        return _buffer_svg(node)
    return _fallback_svg(node)


def _junctions(visual) -> str:
    counts = Counter(w.source for w in visual.wires)
    lookup = {n.id: n for n in visual.nodes}
    dots = []
    for source, count in counts.items():
        if count > 1 and source in lookup:
            node = lookup[source]
            # Junctions are shown only on actual shared graph sources.
            # The renderer never creates dots at ordinary wire crossings.
            junction_x = node.x + node.width
            if node.kind.upper() in {"NAND", "NOR", "XNOR"}:
                junction_x += 1
            dots.append(
                f'<circle class="junction" cx="{junction_x}" '
                f'cy="{node.y+node.height/2}" r="3.4" />'
            )
    return "".join(dots)



def _crossing_gaps(visual) -> str:
    """Render explicit non-electrical wire bridges at every true crossing.

    A simple plus sign is visually ambiguous, particularly in dense NOR
    realizations.  BoolNexa therefore masks the crossing and redraws the
    horizontal conductor as a small bridge.  The bridge is purely visual: no
    junction dot is added and graph connectivity is unchanged.
    """
    marks = []
    for x, y in visual.crossings:
        marks.append(
            f'<g class="wire-crossing">'
            f'<circle class="crossing-mask" cx="{x}" cy="{y}" r="5.5" />'
            # Restore the vertical conductor after the white mask.  Without
            # this, the mask makes the vertical net look physically broken.
            f'<path class="crossing-through" d="M {x} {y-7} L {x} {y+7}" />'
            f'<path class="crossing-bridge" '
            f'd="M {x-7} {y} C {x-4} {y-7}, {x+4} {y-7}, {x+7} {y}" />'
            f'</g>'
        )
    return "".join(marks)

def _render_visual(visual) -> str:
    counts = Counter(w.source for w in visual.wires)
    wires = "".join(_wire_svg(w) for w in visual.wires)
    labels = "".join(
        _wire_label_svg(w, counts[w.source]) for w in visual.wires
    )
    nodes = "".join(_node_svg(n) for n in visual.nodes)
    aria = escape(f"Logic circuit for {visual.expression}")

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {visual.width} {visual.height}" '
        f'width="100%" height="100%" role="img" aria-label="{aria}">'
        '<style>'
        '.wire{fill:none;stroke:#263247;stroke-width:2.1;stroke-linecap:round;stroke-linejoin:round;}'
        '.gate path,.gate polygon,.gate rect{fill:#fff;stroke:#172033;stroke-width:2.2;stroke-linejoin:round;}'
        '.gate .bubble{fill:#fff;stroke:#172033;stroke-width:2;}'
        '.xor-mark{fill:none!important;stroke:#172033!important;stroke-width:2.1!important;}'
        '.io line{stroke:#263247;stroke-width:2.1;}'
        '.io text,.gate text,.signal-label{font-family:Arial,Helvetica,sans-serif;font-size:14px;font-weight:700;fill:#172033;}'
        '.signal-label{font-size:13px;paint-order:stroke;stroke:#fff;stroke-width:5px;stroke-linejoin:round;}'
        '.input text{fill:#2548a8}.output text{fill:#08704d}.junction{fill:#263247}'
        '.wire-crossing .crossing-mask{fill:#fff;stroke:none}.wire-crossing .crossing-through,.wire-crossing .crossing-bridge{fill:none;stroke:#263247;stroke-width:2.1;stroke-linecap:round}'
        '</style>'
        # Layer order is deliberate: geometry first, then labels, then gate
        # bodies. Routing/label placement should already avoid overlaps; this
        # final ordering guarantees gate symbols remain visually authoritative.
        + wires
        + _crossing_gaps(visual)
        + _junctions(visual)
        + labels
        + nodes
        + '</svg>'
    )


def render_circuit_graph_svg(graph: CircuitGraph) -> str:
    return _render_visual(build_circuit_visual_from_graph(graph))


def render_circuit_svg(expression: str) -> str:
    return _render_visual(build_circuit_visual(expression))
