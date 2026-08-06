from digital_logic_lab.circuit_svg_renderer import render_circuit_svg
from digital_logic_lab.circuit_visual_model import build_circuit_visual


def test_visual_model_matches_backend_statistics() -> None:
    visual = build_circuit_visual("AB + AC'")
    assert visual.total_gates == 4
    assert visual.logic_depth == 3
    assert visual.gate_counts["AND"] == 2


def test_svg_contains_professional_gate_geometry() -> None:
    svg = render_circuit_svg("AB + AC'")

    assert "<svg" in svg
    assert 'class="gate and"' in svg
    assert 'class="gate or"' in svg
    assert 'class="gate not"' in svg
    assert 'class="bubble"' in svg
    assert "aria-label" in svg

    # Professional renderer uses shapes instead of text labels in gate bodies.
    assert ">AND<" not in svg
    assert ">OR<" not in svg
    assert ">NOT<" not in svg


def test_svg_contains_orthogonal_wire_paths() -> None:
    svg = render_circuit_svg("AB + AC'")
    assert 'class="wire"' in svg
    assert "M " in svg
    assert "L " in svg


def test_svg_contains_fanout_junction() -> None:
    svg = render_circuit_svg("AB + AC'")
    assert 'class="junction"' in svg
