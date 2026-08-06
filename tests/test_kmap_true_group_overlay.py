from digital_logic_lab.kmap_engine import build_kmap
from digital_logic_lab.kmap_renderer import serialize_kmap


def _segments(expr):
    return serialize_kmap(build_kmap(expr))[0]["segments"]


def test_adjacent_pair_is_one_group_level_segment():
    segs = _segments("AB + AC'")
    red = [s for s in segs if s["group"] == "2"]
    assert len(red) == 1
    assert red[0]["open_left"] == "false"
    assert red[0]["open_right"] == "false"
    assert "9.8rem" in red[0]["width"]


def test_horizontal_wrap_is_two_outward_open_segments():
    segs = _segments("AB + AC'")
    blue = [s for s in segs if s["group"] == "1"]
    assert len(blue) == 2
    assert any(s["open_left"] == "true" for s in blue)
    assert any(s["open_right"] == "true" for s in blue)
    assert all(s["border_left"].startswith("0") for s in blue if s["open_left"] == "true")
    assert all(s["border_right"].startswith("0") for s in blue if s["open_right"] == "true")
