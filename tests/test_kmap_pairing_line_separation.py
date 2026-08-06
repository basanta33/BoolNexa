"""Regression tests for Mano-style K-map pairing lanes and header geometry."""

from pathlib import Path

from digital_logic_lab.kmap_engine import build_kmap
from digital_logic_lab.kmap_renderer import serialize_kmap


def _cell_outlines(expression: str, minterm: str):
    result = serialize_kmap(build_kmap(expression))[0]
    for row in result["rows"]:
        for cell in row:
            if cell["minterm"] == minterm:
                return cell["outlines"]
    raise AssertionError(f"{minterm} not found")


def test_overlapping_pairing_lines_have_distinct_insets():
    # m6 belongs to both implicants for AB + AC'. Do not assume a fixed
    # G1/G2 numbering; group ordering is an implementation detail.
    outlines = _cell_outlines("AB + AC'", "m6")
    assert len(outlines) == 2
    assert outlines[0]["group"] != outlines[1]["group"]
    assert outlines[0]["inset"] != outlines[1]["inset"]


def test_horizontal_wrap_still_opens_at_physical_edges():
    # AC' is the wrap group containing m4 and m6. Locate the shared group
    # dynamically instead of assuming it is always numbered G1.
    m4_outlines = _cell_outlines("AB + AC'", "m4")
    m6_outlines = _cell_outlines("AB + AC'", "m6")
    assert len(m4_outlines) == 1
    wrap_group = m4_outlines[0]["group"]
    m6_wrap = next(o for o in m6_outlines if o["group"] == wrap_group)
    assert m4_outlines[0]["left"].startswith("0 ")
    assert m6_wrap["right"].startswith("0 ")


def test_kmap_axis_uses_function_label_and_corner_anchored_diagonal():
    source = (Path(__file__).parents[1] / "digital_logic_lab" / "boolean_lab.py").read_text(encoding="utf-8")
    assert "kmap_function_label" in source
    assert 'top="-4.35rem"' in source
    assert 'left="-3.15rem"' in source
    assert 'top="-2.25rem"' in source
    assert 'left="-2.25rem"' in source
    assert 'width="3.182rem"' in source
    assert 'transform="rotate(45deg)"' in source
    assert 'top="-4.05rem"' not in source
    assert 'left="-2.95rem"' not in source
