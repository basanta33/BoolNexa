from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/"digital_logic_lab"/"academy_alu_path08.py"
APP=ROOT/"digital_logic_lab"/"digital_logic_lab.py"
CAT=ROOT/"digital_logic_lab"/"academy_route_catalog.py"

def test_path08_lesson4_present():
    t=MOD.read_text(encoding="utf-8")
    assert "def arithmetic_operations_datapaths_lesson" in t
    assert "PATH 08 · LESSON 04" in t
    assert "Arithmetic Operations & Datapaths" in t

def test_lesson4_teaches_datapath_operations():
    t=MOD.read_text(encoding="utf-8")
    for term in ("What is a datapath?","Reusing one adder","Increment and decrement","Operand conditioning","Transfer operations","Control word idea"): assert term in t

def test_lesson4_interactive_checks():
    t=MOD.read_text(encoding="utf-8")
    for term in ("def check_datapath","def check_increment","def check_transfer"): assert term in t

def test_lesson4_route_registered():
    t=APP.read_text(encoding="utf-8")
    assert "arithmetic_operations_datapaths_lesson" in t
    assert 'route="/academy/unit-8/arithmetic-datapaths"' in t

def test_catalog_keeps_lesson4_and_newer_path08_routes():
    t=CAT.read_text(encoding="utf-8")
    assert "/academy/unit-8/arithmetic-datapaths" in t
    assert t.count("/academy/unit-8/") >= 4


def test_lesson4_advances_to_live_lesson5():
    t=MOD.read_text(encoding="utf-8")
    assert "Next · Logic Operations & Function Selection" in t
    assert 'href="/academy/unit-8/logic-function-selection"' in t
