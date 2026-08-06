from pathlib import Path

SOURCE = (Path(__file__).parents[1] / "digital_logic_lab" / "boolean_lab.py").read_text(encoding="utf-8")

def test_kmap_has_dynamic_function_label():
    assert 'kmap_function_label: str = ""' in SOURCE
    assert '"F(" + ",".join(result.variables) + ")"' in SOURCE
    assert 'BooleanLabState.kmap_function_label' in SOURCE

def test_diagonal_is_anchored_from_grid_wrapper():
    # A 3.182rem line at 45° has 2.25rem x/y projection, so starting at
    # (-2.25rem, -2.25rem) terminates at the grid's (0, 0) corner.
    assert 'top="-2.25rem"' in SOURCE
    assert 'left="-2.25rem"' in SOURCE
    assert 'width="3.182rem"' in SOURCE
    assert 'transform="rotate(45deg)"' in SOURCE

def test_old_floating_abc_header_geometry_removed():
    assert 'top="-4.05rem"' not in SOURCE
    assert 'left="-2.95rem"' not in SOURCE
