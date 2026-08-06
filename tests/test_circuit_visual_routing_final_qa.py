from digital_logic_lab.circuit_layout import layout_circuit
from digital_logic_lab.circuit_svg_renderer import render_circuit_graph_svg
from digital_logic_lab.circuit_visual_model import build_circuit_visual_from_graph
from digital_logic_lab.realization_policy import RealizationPreset
from digital_logic_lab.realization_strategy import realize_preset


def _graph(expression: str, preset: RealizationPreset):
    return realize_preset(expression, preset).graph


def _label_box(label: str, x: float, baseline_y: float):
    width = max(10.0, len(label) * 7.4 + 8.0)
    return (x - width / 2.0, baseline_y - 12.0, x + width / 2.0, baseline_y + 4.0)


def _overlap(a, b, padding=0.0):
    return not (
        a[2] + padding <= b[0] or b[2] + padding <= a[0]
        or a[3] + padding <= b[1] or b[3] + padding <= a[1]
    )


def test_nand_xor_a_and_b_fanout_trunks_are_physically_distinct():
    graph = _graph("A^B", RealizationPreset.NAND_ONLY)
    layout = layout_circuit(graph)
    a = [w for w in layout.wires if w.source == "input_A"]
    b = [w for w in layout.wires if w.source == "input_B"]
    assert len(a) > 1 and len(b) > 1
    assert {w.points[1][0] for w in a}.isdisjoint({w.points[1][0] for w in b})


def test_nand_ab_plus_ac_not_keeps_a_b_c_input_nets_distinct():
    graph = _graph("AB+AC'", RealizationPreset.NAND_ONLY)
    layout = layout_circuit(graph)
    trunks = {}
    for source in ("input_A", "input_B", "input_C"):
        wires = [w for w in layout.wires if w.source == source]
        if len(wires) > 1:
            trunks[source] = {w.points[1][0] for w in wires}
    names = list(trunks)
    for i, first in enumerate(names):
        for second in names[i + 1:]:
            assert trunks[first].isdisjoint(trunks[second])


def test_dense_nand_and_nor_labels_do_not_cover_gate_bodies():
    for preset in (RealizationPreset.NAND_ONLY, RealizationPreset.NOR_ONLY):
        visual = build_circuit_visual_from_graph(_graph("AB+AC'", preset))
        gates = [
            (n.x - 5, n.y - 5, n.x + n.width + 5, n.y + n.height + 5)
            for n in visual.nodes if n.kind not in {"INPUT", "OUTPUT", "CONSTANT"}
        ]
        for wire in visual.wires:
            if not wire.label:
                continue
            box = _label_box(wire.label, wire.label_x, wire.label_y)
            assert all(not _overlap(box, gate, padding=2.0) for gate in gates)


def test_svg_draws_wires_then_labels_then_gate_nodes():
    svg = render_circuit_graph_svg(_graph("AB+AC'", RealizationPreset.NAND_ONLY))
    wire_pos = svg.find('<path class="wire"')
    label_pos = svg.find('<text class="signal-label"')
    gate_pos = min(
        pos for pos in (
            svg.find('<g class="gate nand"'),
            svg.find('<g class="gate nor"'),
            svg.find('<g class="gate and"'),
            svg.find('<g class="gate or"'),
        ) if pos >= 0
    )
    assert 0 <= wire_pos < label_pos < gate_pos


def test_non_electrical_crossings_use_bridge_not_junction():
    graph = _graph("AC+AC'", RealizationPreset.NAND_ONLY)
    visual = build_circuit_visual_from_graph(graph)
    assert visual.crossings
    svg = render_circuit_graph_svg(graph)
    assert svg.count('class="crossing-bridge"') == len(visual.crossings)
    assert svg.count('class="crossing-through"') == len(visual.crossings)
