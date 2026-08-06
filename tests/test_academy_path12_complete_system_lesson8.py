from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/"digital_logic_lab"/"academy_hdl_path12.py"
APP=ROOT/"digital_logic_lab"/"digital_logic_lab.py"
CAT=ROOT/"digital_logic_lab"/"academy_route_catalog.py"

def test_lesson8_present():
    t=MOD.read_text(encoding="utf-8")
    assert "def complete_fpga_system_design_deployment_lesson" in t
    assert "PATH 12 · LESSON 08" in t

def test_lesson8_topics():
    t=MOD.read_text(encoding="utf-8")
    for term in (
        "System design starts from measurable requirements",
        "Top-level architecture connects reusable blocks",
        "Clock and reset architecture must be deliberate",
        "Pin and I/O constraints connect HDL to the board",
        "Implementation must satisfy both resource and timing limits",
        "The bitstream configures the FPGA fabric",
        "Volatile configuration may require boot storage",
        "Hardware bring-up verifies the real board",
        "Integrated logic analyzers expose internal signals",
        "Simulation and hardware debug complement each other",
        "Trace a complete FPGA deployment workflow",
        "Path 12 integration checkpoint",
    ):
        assert term in t

def test_lesson8_checks():
    t=MOD.read_text(encoding="utf-8")
    for m in ("def check_bitstream","def check_io","def check_ila"):
        assert m in t

def test_lesson8_route_and_completion():
    route="/academy/unit-12/complete-fpga-system-design-deployment"
    assert f'route="{route}"' in APP.read_text(encoding="utf-8")
    assert route in CAT.read_text(encoding="utf-8")
    assert CAT.read_text(encoding="utf-8").count("/academy/unit-12/")==8
    t=MOD.read_text(encoding="utf-8")
    assert "PATH 12 COMPLETE" in t
    assert "Lesson 9" not in t

def test_simulator_fix_preserved():
    assert "State.handle_gate_click(cell_key)" in APP.read_text(encoding="utf-8")
