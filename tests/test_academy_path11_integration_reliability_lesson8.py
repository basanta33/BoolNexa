from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/"digital_logic_lab"/"academy_embedded_path11.py"
APP=ROOT/"digital_logic_lab"/"digital_logic_lab.py"
CAT=ROOT/"digital_logic_lab"/"academy_route_catalog.py"

def test_lesson8_present():
    t=MOD.read_text(encoding="utf-8")
    assert "def embedded_system_integration_reliability_debugging_lesson" in t
    assert "PATH 11 · LESSON 08" in t

def test_lesson8_topics():
    t=MOD.read_text(encoding="utf-8")
    for term in (
        "Integration connects the complete signal-and-software path",
        "Startup sequencing establishes a known safe state",
        "Watchdogs detect missing software progress",
        "Brownout detection protects low-voltage operation",
        "Fault containment limits propagation",
        "Timeouts convert indefinite waiting into bounded behaviour",
        "Assertions and diagnostics expose impossible states",
        "Debugging starts by observing the right layer",
        "Reproduce faults before changing code",
        "Integration testing crosses subsystem boundaries",
        "Trace an integrated fault-and-recovery scenario",
        "Path 11 integration checkpoint",
    ):
        assert term in t

def test_lesson8_checks():
    t=MOD.read_text(encoding="utf-8")
    for m in ("def check_watchdog","def check_brownout","def check_fault"):
        assert m in t

def test_lesson8_route_and_completion():
    route="/academy/unit-11/embedded-system-integration-reliability-debugging"
    assert f'route="{route}"' in APP.read_text(encoding="utf-8")
    assert route in CAT.read_text(encoding="utf-8")
    assert CAT.read_text(encoding="utf-8").count("/academy/unit-11/")==8
    t=MOD.read_text(encoding="utf-8")
    assert "PATH 11 COMPLETE" in t
    assert "Lesson 9" not in t

def test_simulator_fix_preserved():
    assert "State.handle_gate_click(cell_key)" in APP.read_text(encoding="utf-8")
