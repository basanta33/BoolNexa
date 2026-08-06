from pathlib import Path

SOURCE = (
    Path(__file__).parents[1] / "digital_logic_lab" / "boolean_lab.py"
).read_text(encoding="utf-8")


def test_five_variable_map_marks_vertical_reflection_axis():
    assert "BooleanLabState.kmap_column_codes.length() == 8" in SOURCE
    assert 'left="calc(19.6rem - 2px)"' in SOURCE
    assert 'border_left="4px double #94A3B8"' in SOURCE


def test_six_variable_map_marks_horizontal_reflection_axis_too():
    assert "BooleanLabState.kmap_row_codes.length() == 8" in SOURCE
    assert 'top="calc(17.6rem - 2px)"' in SOURCE
    assert 'border_top="4px double #94A3B8"' in SOURCE


def test_group_outlines_render_above_reflection_guides():
    assert 'z_index="6"' in SOURCE
