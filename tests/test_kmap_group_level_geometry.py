from digital_logic_lab.kmap_engine import build_kmap
from digital_logic_lab.kmap_renderer import serialize_kmap


def _outline(expr, minterm, group):
    data = serialize_kmap(build_kmap(expr))[0]
    for row in data["rows"]:
        for cell in row:
            if cell["minterm"] == minterm:
                return next(o for o in cell["outlines"] if o["group"] == str(group))
    raise AssertionError(minterm)


def test_adjacent_pair_merges_as_one_continuous_loop():
    m7 = _outline("AB + AC'", "m7", 2)
    m6 = _outline("AB + AC'", "m6", 2)
    assert m7["right"].startswith("0 ")
    assert m6["left"].startswith("0 ")
    assert m7["radius_top_right"] == "0px"
    assert m7["radius_bottom_right"] == "0px"
    assert m6["radius_top_left"] == "0px"
    assert m6["radius_bottom_left"] == "0px"
    assert m7["top_offset"] == m6["top_offset"]
    assert m7["bottom_offset"] == m6["bottom_offset"]


def test_horizontal_wrap_opens_only_at_physical_outer_edges():
    m4 = _outline("AB + AC'", "m4", 1)
    m6 = _outline("AB + AC'", "m6", 1)
    assert m4["left"].startswith("0 ") and m4["left_offset"] == "-3px"
    assert m6["right"].startswith("0 ") and m6["right_offset"] == "-3px"
    assert m4["radius_top_left"] == "0px"
    assert m4["radius_bottom_left"] == "0px"
    assert m6["radius_top_right"] == "0px"
    assert m6["radius_bottom_right"] == "0px"
    # inward ends stay rounded, matching textbook open wrap brackets.
    assert m4["radius_top_right"] == "9px"
    assert m6["radius_top_left"] == "9px"
