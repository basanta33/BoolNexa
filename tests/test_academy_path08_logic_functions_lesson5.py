from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/"digital_logic_lab"/"academy_alu_path08.py"
APP=ROOT/"digital_logic_lab"/"digital_logic_lab.py"
CAT=ROOT/"digital_logic_lab"/"academy_route_catalog.py"

def test_path08_lesson5_present():
    t=MOD.read_text(encoding="utf-8")
    assert "def logic_operations_function_selection_lesson" in t
    assert "PATH 08 · LESSON 05" in t
    assert "Logic Operations & Function Selection" in t

def test_lesson5_teaches_logic_unit():
    t=MOD.read_text(encoding="utf-8")
    for term in ("Bitwise logic across a word","AND, OR, XOR and NOT","Parallel logic hardware","Function selection codes","Arithmetic versus logic result","Logic operations and flags"): assert term in t

def test_lesson5_interactive_checks():
    t=MOD.read_text(encoding="utf-8")
    for term in ("def check_bitwise","def check_xor","def check_logic_select"): assert term in t

def test_lesson5_route_registered():
    t=APP.read_text(encoding="utf-8")
    assert "logic_operations_function_selection_lesson" in t
    assert 'route="/academy/unit-8/logic-function-selection"' in t

def test_catalog_keeps_lesson5_and_newer_path08_routes():
    t=CAT.read_text(encoding="utf-8")
    assert "/academy/unit-8/logic-function-selection" in t
    assert t.count("/academy/unit-8/") >= 5


def test_lesson5_advances_to_live_lesson6():
    t=MOD.read_text(encoding="utf-8")
    assert "Next · ALU Control & Operation Encoding" in t
    assert 'href="/academy/unit-8/alu-control"' in t
