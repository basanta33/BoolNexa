from digital_logic_lab.circuit_visual_model import build_circuit_visual_from_graph
from digital_logic_lab.realization_policy import RealizationPreset
from digital_logic_lab.realization_strategy import realize_preset


def _label_box(label: str, x: float, baseline_y: float):
    width = max(10.0, len(label) * 7.4 + 8.0)
    return (x - width / 2.0, baseline_y - 12.0, x + width / 2.0, baseline_y + 4.0)


def _overlap(a, b, padding=0.0):
    return not (
        a[2] + padding <= b[0]
        or b[2] + padding <= a[0]
        or a[3] + padding <= b[1]
        or b[3] + padding <= a[1]
    )


def _segment_hits_box(a, b, box, padding=4.0):
    left, top, right, bottom = box
    left -= padding
    top -= padding
    right += padding
    bottom += padding
    x1, y1 = a
    x2, y2 = b
    if y1 == y2:
        lo, hi = sorted((x1, x2))
        return top < y1 < bottom and max(lo, left) < min(hi, right)
    if x1 == x2:
        lo, hi = sorted((y1, y2))
        return left < x1 < right and max(lo, top) < min(hi, bottom)
    return False


def _path_points(path: str):
    parts = path.replace("M", "").replace("L", "").split()
    nums = [float(v) for v in parts]
    return list(zip(nums[0::2], nums[1::2]))


def _assert_labels_clear(visual) -> None:
    gates = [node for node in visual.nodes if node.kind not in {"INPUT", "OUTPUT", "CONSTANT"}]
    wire_segments = []
    for wire in visual.wires:
        points = _path_points(wire.path)
        wire_segments.extend(zip(points, points[1:]))

    seen = []
    for wire in visual.wires:
        if not wire.label:
            continue
        box = _label_box(wire.label, wire.label_x, wire.label_y)
        assert box[0] >= 0 and box[1] >= 0
        assert box[2] <= visual.width and box[3] <= visual.height
        for gate in gates:
            gate_box = (gate.x - 5, gate.y - 5, gate.x + gate.width + 5, gate.y + gate.height + 5)
            assert not _overlap(box, gate_box, padding=2.0), (wire, gate)
        for a, b in wire_segments:
            assert not _segment_hits_box(a, b, box), (wire, a, b)
        for old in seen:
            assert not _overlap(box, old, padding=4.0), wire
        seen.append(box)


def test_nand_xor_signal_labels_avoid_gates_wires_and_other_text() -> None:
    graph = realize_preset("A^B", RealizationPreset.NAND_ONLY).graph
    _assert_labels_clear(build_circuit_visual_from_graph(graph))


def test_nor_ab_plus_ac_not_dense_labels_avoid_gates_and_wires() -> None:
    graph = realize_preset("AB+AC'", RealizationPreset.NOR_ONLY).graph
    visual = build_circuit_visual_from_graph(graph)
    _assert_labels_clear(visual)
    # The long inverter signal is shown once on its fan-out trunk rather than
    # printed twice over the two physical NOR inputs.
    internal_labels = [w.label for w in visual.wires if w.label.startswith("N")]
    assert internal_labels
    assert all(len(label) <= 4 for label in internal_labels)
