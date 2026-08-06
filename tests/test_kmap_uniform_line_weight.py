from pathlib import Path

SOURCE = (
    Path(__file__).parents[1] / "digital_logic_lab" / "boolean_lab.py"
).read_text(encoding="utf-8")


def test_kmap_grid_uses_same_three_pixel_weight_as_group_outlines():
    assert 'border="3px solid #111827"' in SOURCE
