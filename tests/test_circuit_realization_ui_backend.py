from digital_logic_lab.circuit_svg_renderer import render_circuit_graph_svg
from digital_logic_lab.realization_policy import RealizationPreset
from digital_logic_lab.realization_strategy import realize_preset


def test_realized_graph_can_be_rendered_directly():
    result = realize_preset("A^B", RealizationPreset.NAND_ONLY)
    svg = render_circuit_graph_svg(result.graph)
    assert "<svg" in svg
    assert 'class="gate nand"' in svg


def test_nor_realized_graph_uses_nor_shapes():
    result = realize_preset("A+B", RealizationPreset.NOR_ONLY)
    svg = render_circuit_graph_svg(result.graph)
    assert 'class="gate nor"' in svg


def test_basic_realization_does_not_render_xor_for_xor_expression():
    result = realize_preset("A^B", RealizationPreset.BASIC_ONLY)
    svg = render_circuit_graph_svg(result.graph)
    assert 'class="gate xor"' not in svg
    assert 'class="gate and"' in svg
    assert 'class="gate or"' in svg


def test_xor_preferred_realization_renders_xor():
    result = realize_preset("A^B", RealizationPreset.XOR_PREFERRED)
    svg = render_circuit_graph_svg(result.graph)
    assert 'class="gate xor"' in svg
