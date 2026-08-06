from digital_logic_lab.circuit_svg_renderer import render_circuit_svg


def test_and_uses_curved_gate_path_not_rectangle() -> None:
    svg = render_circuit_svg("AB")
    assert 'class="gate and"' in svg
    assert "<path" in svg
    assert ">AND<" not in svg


def test_or_uses_ansi_profile() -> None:
    svg = render_circuit_svg("A+B")
    assert 'class="gate or"' in svg
    assert " C " in svg


def test_not_uses_triangle_and_bubble() -> None:
    svg = render_circuit_svg("A'")
    assert 'class="gate not"' in svg
    assert "<polygon" in svg
    assert 'class="bubble"' in svg


def test_xor_has_extra_input_curve() -> None:
    svg = render_circuit_svg("A^B")
    assert 'class="xor-mark"' in svg


def test_fanout_has_junction_dot() -> None:
    svg = render_circuit_svg("AB+AC'")
    assert 'class="junction"' in svg


def test_reference_circuit_contains_no_text_gate_boxes() -> None:
    svg = render_circuit_svg("AB+AC'")
    assert ">AND<" not in svg
    assert ">OR<" not in svg
    assert ">NOT<" not in svg
