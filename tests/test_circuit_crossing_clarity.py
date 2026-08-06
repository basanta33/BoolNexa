from digital_logic_lab.circuit_svg_renderer import render_circuit_graph_svg
from digital_logic_lab.circuit_visual_model import build_circuit_visual_from_graph
from digital_logic_lab.realization_policy import RealizationPreset
from digital_logic_lab.realization_strategy import realize_preset


def _graph(expression: str, preset: RealizationPreset):
    return realize_preset(expression, preset).graph


def test_ac_plus_ac_not_detects_non_electrical_crossing() -> None:
    """Regression: the A/C fan-out geometry contains a true wire crossing."""
    visual = build_circuit_visual_from_graph(
        _graph("AC+AC'", RealizationPreset.NAND_ONLY)
    )
    assert visual.crossings


def test_ac_plus_ac_not_svg_marks_crossing_as_bridge_not_junction() -> None:
    svg = render_circuit_graph_svg(
        _graph("AC+AC'", RealizationPreset.NAND_ONLY)
    )
    assert 'class="wire-crossing"' in svg
    assert 'class="crossing-mask"' in svg
    assert 'class="crossing-bridge"' in svg


def test_nor_realization_uses_same_non_electrical_crossing_bridge_rule() -> None:
    """NOR-only dense routing must never fall back to ambiguous plus crossings."""
    graph = _graph("AC+AC'", RealizationPreset.NOR_ONLY)
    visual = build_circuit_visual_from_graph(graph)
    assert visual.crossings

    svg = render_circuit_graph_svg(graph)
    assert svg.count('class="wire-crossing"') == len(visual.crossings)
    assert svg.count('class="crossing-bridge"') == len(visual.crossings)


def test_true_fanout_still_uses_junction_dot() -> None:
    svg = render_circuit_graph_svg(
        _graph("AB+AC'", RealizationPreset.NAND_ONLY)
    )
    assert 'class="junction"' in svg


def test_crossing_bridge_keeps_vertical_conductor_visually_continuous() -> None:
    """The bridge mask must never make the crossed vertical net look broken."""
    svg = render_circuit_graph_svg(_graph("AB+AC'", RealizationPreset.BASIC_ONLY))
    assert 'class="wire-crossing"' in svg
    assert 'class="crossing-through"' in svg
    assert svg.count('class="crossing-through"') == svg.count('class="wire-crossing"')
