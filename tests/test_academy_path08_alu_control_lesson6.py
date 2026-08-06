from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/"digital_logic_lab"/"academy_alu_path08.py"
APP=ROOT/"digital_logic_lab"/"digital_logic_lab.py"
CAT=ROOT/"digital_logic_lab"/"academy_route_catalog.py"

def test_path08_lesson6_present():
    t=MOD.read_text(encoding="utf-8")
    assert "def alu_control_operation_encoding_lesson" in t
    assert "PATH 08 · LESSON 06" in t
    assert "ALU Control & Operation Encoding" in t

def test_lesson6_teaches_control_encoding():
    t=MOD.read_text(encoding="utf-8")
    for term in ("From instruction to ALU operation","How many control bits?","Example ALU control table","Control signals inside the ALU","Reserved and illegal codes","Decoder design and verification"):
        assert term in t

def test_lesson6_has_interactive_checks():
    t=MOD.read_text(encoding="utf-8")
    for term in ("def check_opcode","def check_control_width","def check_illegal_code"):
        assert term in t

def test_lesson6_route_registered():
    t=APP.read_text(encoding="utf-8")
    assert "alu_control_operation_encoding_lesson" in t
    assert 'route="/academy/unit-8/alu-control"' in t

def test_catalog_keeps_lesson6_and_newer_path08_routes():
    t=CAT.read_text(encoding="utf-8")
    assert "/academy/unit-8/alu-control" in t
    assert t.count("/academy/unit-8/") >= 6


def test_lesson6_advances_to_live_lesson7():
    t=MOD.read_text(encoding="utf-8")
    assert "Next · ALU Flags & Comparisons" in t
    assert 'href="/academy/unit-8/alu-flags-comparisons"' in t
