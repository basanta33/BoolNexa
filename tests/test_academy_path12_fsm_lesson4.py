from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/"digital_logic_lab"/"academy_hdl_path12.py"
APP=ROOT/"digital_logic_lab"/"digital_logic_lab.py"
CAT=ROOT/"digital_logic_lab"/"academy_route_catalog.py"

def test_lesson4_present():
    t=MOD.read_text(encoding="utf-8")
    assert "def finite_state_machines_control_logic_lesson" in t
    assert "PATH 12 · LESSON 04" in t

def test_lesson4_topics():
    t=MOD.read_text(encoding="utf-8")
    for term in (
        "An FSM stores one of a finite set of states",
        "States represent meaningful control phases",
        "Transitions define when the controller moves",
        "Moore outputs depend on state",
        "Mealy outputs can respond to inputs immediately",
        "A common HDL FSM structure separates three concerns",
        "Default assignments prevent unintended storage",
        "State encoding maps symbolic states into bits",
        "Illegal-state recovery improves robustness",
        "FSMs coordinate datapaths",
        "Trace a simple transaction controller",
    ):
        assert term in t

def test_lesson4_checks():
    t=MOD.read_text(encoding="utf-8")
    for m in ("def check_fsm","def check_moore","def check_mealy"):
        assert m in t

def test_lesson4_route():
    route="/academy/unit-12/finite-state-machines-control-logic"
    assert f'route="{route}"' in APP.read_text(encoding="utf-8")
    assert route in CAT.read_text(encoding="utf-8")
    assert CAT.read_text(encoding="utf-8").count("/academy/unit-12/")>=4

def test_lesson5_link():
    t=MOD.read_text(encoding="utf-8")
    assert "Next · Testbenches, Simulation & Verification" in t
    assert "/academy/unit-12/testbenches-simulation-verification" in t

def test_simulator_fix_preserved():
    assert "State.handle_gate_click(cell_key)" in APP.read_text(encoding="utf-8")
