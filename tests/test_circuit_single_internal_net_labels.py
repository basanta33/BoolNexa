from collections import Counter

from digital_logic_lab.circuit_visual_model import build_circuit_visual_from_graph
from digital_logic_lab.realization_policy import RealizationPreset
from digital_logic_lab.realization_strategy import realize_preset


def _visual(expression, preset):
    graph = realize_preset(expression, preset).graph
    return build_circuit_visual_from_graph(graph)


def _internal_labels(visual):
    return [
        wire.label for wire in visual.wires
        if wire.label.startswith("N") and wire.label[1:].isdigit()
    ]


def test_nor_xor_each_internal_net_label_is_rendered_once():
    labels = _internal_labels(_visual("A^B", RealizationPreset.NOR_ONLY))
    counts = Counter(labels)
    assert labels
    assert all(count == 1 for count in counts.values())


def test_nand_xor_each_internal_net_label_is_rendered_once():
    labels = _internal_labels(_visual("A^B", RealizationPreset.NAND_ONLY))
    counts = Counter(labels)
    assert labels
    assert all(count == 1 for count in counts.values())


def test_primary_input_labels_can_still_repeat_on_fanout():
    visual = _visual("A^B", RealizationPreset.NOR_ONLY)
    labels = [wire.label for wire in visual.wires if wire.label]
    assert labels.count("A") >= 1
    assert labels.count("B") >= 1


def test_final_function_label_remains_visible():
    for preset in (RealizationPreset.NAND_ONLY, RealizationPreset.NOR_ONLY):
        visual = _visual("A^B", preset)
        labels = [wire.label for wire in visual.wires if wire.label]
        assert "A ⊕ B" in labels
