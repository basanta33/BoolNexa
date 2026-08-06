from pathlib import Path
from digital_logic_lab.kmap_engine import build_kmap
from digital_logic_lab.kmap_renderer import serialize_kmap


def _cell(serialized, minterm):
    for row in serialized[0]['rows']:
        for cell in row:
            if cell['minterm'] == f'm{minterm}':
                return cell
    raise AssertionError(minterm)


def _outline(cell, group):
    return next(o for o in cell['outlines'] if o['group'] == str(group))


def test_horizontal_wrap_opens_through_outer_edges():
    s = serialize_kmap(build_kmap("AB + AC'"))
    left = _outline(_cell(s, 4), 1)
    right = _outline(_cell(s, 6), 1)
    assert left['left'] == '0 solid transparent'
    assert left['left_offset'].startswith('-')
    assert left['right'] != '0 solid transparent'
    assert right['right'] == '0 solid transparent'
    assert right['right_offset'].startswith('-')
    assert right['left'] != '0 solid transparent'


def test_normal_pair_has_consistent_group_layer_across_overlap():
    s = serialize_kmap(build_kmap("AB + AC'"))
    m7 = _outline(_cell(s, 7), 2)
    m6 = _outline(_cell(s, 6), 2)
    assert m7['top_offset'] == m6['top_offset']
    assert m7['bottom_offset'] == m6['bottom_offset']
    assert m7['right'] == '0 solid transparent'
    assert m6['left'] == '0 solid transparent'


def test_function_symbol_not_embedded_in_axis_corner():
    source = (Path(__file__).resolve().parents[1] / 'digital_logic_lab' / 'boolean_lab.py').read_text(encoding='utf-8')
    assert 'rx.text(\n                    "F",\n                    position="absolute"' not in source
