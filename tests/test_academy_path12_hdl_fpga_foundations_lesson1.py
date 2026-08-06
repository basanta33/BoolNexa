from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/"digital_logic_lab"/"academy_hdl_path12.py"
APP=ROOT/"digital_logic_lab"/"digital_logic_lab.py"
CAT=ROOT/"digital_logic_lab"/"academy_route_catalog.py"
CONTENT=ROOT/"digital_logic_lab"/"academy_content.py"

def test_path12_lesson1_present():
    t=MOD.read_text(encoding="utf-8")
    assert "def hdl_fpga_foundations_lesson" in t
    assert "PATH 12 · LESSON 01" in t
    assert "HDL & FPGA Foundations" in t

def test_lesson1_topics():
    t=MOD.read_text(encoding="utf-8")
    for term in (
        "HDLs describe hardware, not a sequence of software instructions",
        "Common HDLs include Verilog/SystemVerilog and VHDL",
        "An FPGA is reconfigurable digital hardware",
        "FPGA logic is built from configurable resources",
        "A LUT implements small Boolean functions",
        "Synthesis translates HDL into implementable hardware",
        "Implementation assigns logic to physical FPGA resources",
        "Simulation verifies behaviour before programming hardware",
        "Combinational and sequential HDL describe different hardware",
        "Parallel hardware is the key FPGA advantage",
        "Trace the FPGA design flow",
    ):
        assert term in t

def test_lesson1_checks():
    t=MOD.read_text(encoding="utf-8")
    for m in ("def check_hdl","def check_fpga","def check_synth"):
        assert m in t

def test_path12_route_catalog_curriculum():
    route="/academy/unit-12/hdl-fpga-foundations"
    assert f'route="{route}"' in APP.read_text(encoding="utf-8")
    assert route in CAT.read_text(encoding="utf-8")
    assert CAT.read_text(encoding="utf-8").count("/academy/unit-12/")>=1
    assert '{"number": 12, "title": "HDL, FPGA and Digital System Design", "hours": 8, "lessons": 8' in CONTENT.read_text(encoding="utf-8")

def test_lesson2_link():
    t=MOD.read_text(encoding="utf-8")
    assert "Next · Combinational HDL Design & Modules" in t
    assert "/academy/unit-12/combinational-hdl-design-modules" in t

def test_simulator_fix_preserved():
    assert "State.handle_gate_click(cell_key)" in APP.read_text(encoding="utf-8")
