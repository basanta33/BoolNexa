from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/"digital_logic_lab"/"academy_alu_path08.py"
APP=ROOT/"digital_logic_lab"/"digital_logic_lab.py"
CAT=ROOT/"digital_logic_lab"/"academy_route_catalog.py"

def test_path08_capstone_present():
    text=MOD.read_text(encoding="utf-8")
    assert "def integrated_alu_design_capstone_lesson" in text
    assert "PATH 08 · LESSON 08 · PATH FINALE" in text
    assert "Complete ALU Architecture & Design Challenge" in text

def test_capstone_integrates_entire_alu():
    text=MOD.read_text(encoding="utf-8")
    for term in ("Complete ALU block architecture","Integrated operation table","Result selection and flag timing","Datapath/control separation","Engineering verification checklist","Design a 4-bit educational ALU","Path 08 concept map"):
        assert term in text

def test_capstone_interactive_checks():
    text=MOD.read_text(encoding="utf-8")
    for term in ("def check_capstone_control","def check_capstone_flag","def check_capstone_verify"):
        assert term in text

def test_capstone_route_registered():
    text=APP.read_text(encoding="utf-8")
    assert "integrated_alu_design_capstone_lesson" in text
    assert 'route="/academy/unit-8/integrated-alu-design"' in text

def test_path08_has_all_eight_live_routes():
    assert CAT.read_text(encoding="utf-8").count("/academy/unit-8/") == 8

def test_path08_completion_present():
    text=MOD.read_text(encoding="utf-8")
    assert "PATH 08 · COMPLETE" in text
    assert "Computer Arithmetic & ALU Design complete" in text
    assert "Return to Academy" in text
