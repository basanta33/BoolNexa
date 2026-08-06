from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/"digital_logic_lab"/"academy_hdl_path12.py"
APP=ROOT/"digital_logic_lab"/"digital_logic_lab.py"
CAT=ROOT/"digital_logic_lab"/"academy_route_catalog.py"

def test_lesson6_present():
    t=MOD.read_text(encoding="utf-8")
    assert "def fpga_synthesis_constraints_timing_lesson" in t
    assert "PATH 12 · LESSON 06" in t

def test_lesson6_topics():
    t=MOD.read_text(encoding="utf-8")
    for term in (
        "Synthesis converts RTL into a technology-aware implementation",
        "Resource reports reveal what the design consumes",
        "Timing constraints define the performance target",
        "Static timing analysis checks paths without input vectors",
        "Slack tells whether timing passes or fails",
        "The critical path limits maximum clock frequency",
        "Placement and routing affect real delays",
        "Pipelining trades latency for clock speed",
        "I/O timing also needs constraints",
        "False and multicycle paths must be declared carefully",
        "Trace a timing-closure workflow",
    ):
        assert term in t

def test_lesson6_checks():
    t=MOD.read_text(encoding="utf-8")
    for m in ("def check_constraint","def check_slack","def check_critical"):
        assert m in t

def test_lesson6_route():
    route="/academy/unit-12/fpga-synthesis-constraints-timing"
    assert f'route="{route}"' in APP.read_text(encoding="utf-8")
    assert route in CAT.read_text(encoding="utf-8")
    assert CAT.read_text(encoding="utf-8").count("/academy/unit-12/")>=6

def test_lesson7_link():
    t=MOD.read_text(encoding="utf-8")
    assert "Next · FPGA Memories, DSP Blocks & Pipelining" in t
    assert "/academy/unit-12/fpga-memories-dsp-pipelining" in t

def test_simulator_fix_preserved():
    assert "State.handle_gate_click(cell_key)" in APP.read_text(encoding="utf-8")
