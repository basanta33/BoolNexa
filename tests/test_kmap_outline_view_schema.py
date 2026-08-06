from pathlib import Path
import ast

def test_kmap_outline_view_has_directional_offsets():
    source = (Path(__file__).parents[1] / "digital_logic_lab" / "boolean_lab.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "KMapOutlineView")
    names = {n.target.id for n in cls.body if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name)}
    assert {"top_offset","right_offset","bottom_offset","left_offset","wrap_horizontal","wrap_vertical"} <= names
