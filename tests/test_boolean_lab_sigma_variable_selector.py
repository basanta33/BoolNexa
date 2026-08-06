from pathlib import Path
import ast

SOURCE_PATH = Path(__file__).parents[1] / "digital_logic_lab" / "boolean_lab.py"
SOURCE = SOURCE_PATH.read_text(encoding="utf-8")


def _helpers():
    tree = ast.parse(SOURCE)
    wanted = {"_parse_sigma_m_numbers", "_sigma_m_to_expression"}
    nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in wanted]
    module = ast.Module(body=nodes, type_ignores=[])
    namespace = {}
    exec(compile(module, str(SOURCE_PATH), "exec"), namespace)
    return namespace


def test_sigma_variable_selector_exists():
    assert 'minterm_variable_count: str = "3"' in SOURCE
    assert '["2", "3", "4", "5", "6"]' in SOURCE
    assert "set_minterm_variable_count" in SOURCE


def test_same_minterms_expand_differently_for_different_widths():
    h = _helpers()
    convert = h["_sigma_m_to_expression"]
    assert convert("0,1,2,3", 2) == "A'B' + A'B + AB' + AB"
    assert convert("0,1,2,3", 3) == "A'B'C' + A'B'C + A'BC' + A'BC"


def test_selected_width_controls_valid_range():
    h = _helpers()
    convert = h["_sigma_m_to_expression"]
    try:
        convert("0,4", 2)
    except ValueError as exc:
        assert "0 and 3" in str(exc)
    else:
        raise AssertionError("m4 must be invalid for two variables")


def test_six_variables_allow_63():
    h = _helpers()
    assert h["_sigma_m_to_expression"]("63", 6) == "ABCDEF"
