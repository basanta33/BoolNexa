from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/"digital_logic_lab"/"academy_alu_path08.py"
APP=ROOT/"digital_logic_lab"/"digital_logic_lab.py"
CAT=ROOT/"digital_logic_lab"/"academy_route_catalog.py"
CONTENT=ROOT/"digital_logic_lab"/"academy_content.py"
MODELS=ROOT/"digital_logic_lab"/"academy"/"models.py"

def test_path08_lesson1_present():
    t=MOD.read_text(encoding="utf-8")
    assert "def binary_addition_subtraction_lesson" in t
    assert "PATH 08 · LESSON 01" in t
    assert "Binary Addition, Subtraction & Arithmetic Hardware" in t

def test_arithmetic_foundations_present():
    t=MOD.read_text(encoding="utf-8")
    for term in ("full adder","carry-out","two's-complement","A + (~B) + 1","Carry-out is not signed overflow","arithmetic logic unit"): assert term in t

def test_interactive_checks_present():
    t=MOD.read_text(encoding="utf-8")
    for term in ("def check_add","def check_subtract","def check_carry","1011₂ + 0110₂"): assert term in t

def test_route_registered():
    t=APP.read_text(encoding="utf-8")
    assert "binary_addition_subtraction_lesson" in t
    assert 'route="/academy/unit-8/binary-arithmetic-hardware"' in t

def test_path08_catalog_content_and_v2_artwork_registered():
    assert '8: (' in CAT.read_text(encoding="utf-8")
    assert '"Computer Arithmetic and ALU Design"' in CONTENT.read_text(encoding="utf-8")
    models = MODELS.read_text(encoding="utf-8")
    assert '8: "/academy/combinational.svg"' in models
    assert '8: ("/academy/unit-8/binary-arithmetic-hardware", "Begin ALU design")' in models

def test_lesson1_advances_to_live_lesson2():
    text = MOD.read_text(encoding="utf-8")
    assert "Next · Carry, Overflow & Status Flags" in text
    assert 'href="/academy/unit-8/carry-overflow-flags"' in text
