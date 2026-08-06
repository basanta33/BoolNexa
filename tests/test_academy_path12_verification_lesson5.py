from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/"digital_logic_lab"/"academy_hdl_path12.py"
APP=ROOT/"digital_logic_lab"/"digital_logic_lab.py"
CAT=ROOT/"digital_logic_lab"/"academy_route_catalog.py"

def test_lesson5_present():
    t=MOD.read_text(encoding="utf-8")
    assert "def testbenches_simulation_verification_lesson" in t
    assert "PATH 12 · LESSON 05" in t

def test_lesson5_topics():
    t=MOD.read_text(encoding="utf-8")
    for term in (
        "A testbench surrounds the design under test",
        "DUT identifies the hardware being verified",
        "Stimulus explores normal and corner-case behaviour",
        "Clock and reset generation establish simulation timing",
        "Waveforms expose signal behaviour over time",
        "Self-checking testbenches compare actual and expected results",
        "Assertions turn requirements into executable checks",
        "Directed and randomized tests serve different purposes",
        "Coverage asks what has actually been exercised",
        "Verification should include failure and recovery paths",
        "Trace verification of a 4-to-1 multiplexer",
    ):
        assert term in t

def test_lesson5_checks():
    t=MOD.read_text(encoding="utf-8")
    for m in ("def check_testbench","def check_dut","def check_assertion"):
        assert m in t

def test_lesson5_route():
    route="/academy/unit-12/testbenches-simulation-verification"
    assert f'route="{route}"' in APP.read_text(encoding="utf-8")
    assert route in CAT.read_text(encoding="utf-8")
    assert CAT.read_text(encoding="utf-8").count("/academy/unit-12/")>=5

def test_lesson6_link():
    t=MOD.read_text(encoding="utf-8")
    assert "Next · FPGA Synthesis, Constraints & Timing" in t
    assert "/academy/unit-12/fpga-synthesis-constraints-timing" in t

def test_simulator_fix_preserved():
    assert "State.handle_gate_click(cell_key)" in APP.read_text(encoding="utf-8")
