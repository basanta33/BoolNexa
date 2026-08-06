from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/"digital_logic_lab"/"academy_alu_path08.py"
APP=ROOT/"digital_logic_lab"/"digital_logic_lab.py"
CAT=ROOT/"digital_logic_lab"/"academy_route_catalog.py"

def test_path08_lesson7_present():
    t=MOD.read_text(encoding="utf-8")
    assert "def alu_flags_comparisons_lesson" in t
    assert "PATH 08 · LESSON 07" in t
    assert "ALU Flags & Comparisons" in t

def test_lesson7_teaches_comparison_logic():
    t=MOD.read_text(encoding="utf-8")
    for term in ("Equality from subtraction","Signed less-than","Why overflow matters","Unsigned less-than","One subtraction, many conditions","Comparison result generation"):
        assert term in t

def test_lesson7_has_interactive_checks():
    t=MOD.read_text(encoding="utf-8")
    for term in ("def check_equality","def check_signed_compare","def check_unsigned_compare"):
        assert term in t

def test_lesson7_route_registered():
    t=APP.read_text(encoding="utf-8")
    assert "alu_flags_comparisons_lesson" in t
    assert 'route="/academy/unit-8/alu-flags-comparisons"' in t

def test_catalog_keeps_lesson7_and_final_path08_route():
    text=CAT.read_text(encoding="utf-8")
    assert "/academy/unit-8/alu-flags-comparisons" in text
    assert text.count("/academy/unit-8/") >= 7


def test_lesson7_advances_to_live_lesson8():
    text=MOD.read_text(encoding="utf-8")
    assert "Next · Complete ALU Architecture" in text
    assert 'href="/academy/unit-8/integrated-alu-design"' in text
