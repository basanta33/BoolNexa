from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/"digital_logic_lab"/"academy_hdl_path12.py"
APP=ROOT/"digital_logic_lab"/"digital_logic_lab.py"
CAT=ROOT/"digital_logic_lab"/"academy_route_catalog.py"

def test_lesson2_present():
    t=MOD.read_text(encoding="utf-8")
    assert "def combinational_hdl_design_modules_lesson" in t
    assert "PATH 12 · LESSON 02" in t

def test_lesson2_topics():
    t=MOD.read_text(encoding="utf-8")
    for term in (
        "Combinational HDL maps directly from Boolean relationships",
        "Ports define the module boundary",
        "Bitwise operators build gate-level logic",
        "Vectors represent multi-bit buses",
        "Conditional operators infer multiplexers",
        "Procedural combinational blocks describe decisions",
        "Incomplete assignments can infer latches",
        "Case statements describe decoders and selectors",
        "Hierarchy scales large designs",
        "Synthesis sees hardware, not source-code cleverness",
        "Trace a 4-to-1 multiplexer design",
    ):
        assert term in t

def test_lesson2_checks():
    t=MOD.read_text(encoding="utf-8")
    for m in ("def check_comb","def check_module","def check_blocking"):
        assert m in t

def test_lesson2_route():
    route="/academy/unit-12/combinational-hdl-design-modules"
    assert f'route="{route}"' in APP.read_text(encoding="utf-8")
    assert route in CAT.read_text(encoding="utf-8")
    assert CAT.read_text(encoding="utf-8").count("/academy/unit-12/")>=2

def test_lesson3_link():
    t=MOD.read_text(encoding="utf-8")
    assert "Next · Sequential HDL, Registers & Clocks" in t
    assert "/academy/unit-12/sequential-hdl-registers-clocks" in t

def test_simulator_fix_preserved():
    assert "State.handle_gate_click(cell_key)" in APP.read_text(encoding="utf-8")
