from pathlib import Path
import ast

SOURCE_PATH = Path(__file__).parents[1] / "digital_logic_lab" / "boolean_lab.py"
SOURCE = SOURCE_PATH.read_text(encoding="utf-8")


def _helpers():
    tree = ast.parse(SOURCE)
    wanted = {"_parse_sigma_m_numbers", "_sigma_m_to_expression"}
    nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in wanted]
    module = ast.Module(body=nodes, type_ignores=[])
    ns = {}
    exec(compile(module, str(SOURCE_PATH), "exec"), ns)
    return ns


def test_sigma_m_uses_explicit_variable_count():
    assert 'minterm_variable_count: str = "3"' in SOURCE
    assert "set_minterm_variable_count" in SOURCE
    h = _helpers()
    assert h["_sigma_m_to_expression"]("0,1,2,3", 2) != h["_sigma_m_to_expression"]("0,1,2,3", 3)


def test_sigma_m_displays_canonical_expression_and_runs_same_pipeline():
    start = SOURCE.index("def generate_from_minterms")
    end = SOURCE.index("def set_show_intermediate", start)
    body = SOURCE[start:end]
    assert "self.expression = source_expression" in body
    assert "self._apply_source_expression(source_expression)" in body


def test_sigma_m_range_depends_on_selected_width():
    h = _helpers()
    try:
        h["_sigma_m_to_expression"]("4", 2)
    except ValueError:
        pass
    else:
        raise AssertionError("m4 must be rejected for 2 variables")
