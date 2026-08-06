from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/"digital_logic_lab"/"academy_hdl_path12.py"
APP=ROOT/"digital_logic_lab"/"digital_logic_lab.py"
CAT=ROOT/"digital_logic_lab"/"academy_route_catalog.py"

def test_lesson3_present():
    t=MOD.read_text(encoding="utf-8")
    assert "def sequential_hdl_registers_clocks_lesson" in t
    assert "PATH 12 · LESSON 03" in t

def test_lesson3_topics():
    t=MOD.read_text(encoding="utf-8")
    for term in (
        "Sequential logic stores state across time",
        "Clock edges define synchronous update moments",
        "Clocked HDL infers flip-flops",
        "Non-blocking assignment models simultaneous register updates",
        "Registers can include enables",
        "Reset establishes a defined initial state",
        "Counters are simple sequential systems",
        "Shift registers move data through stages",
        "Clock-domain boundaries require care",
        "Timing constraints define required performance",
        "Trace a 4-bit synchronous counter",
    ):
        assert term in t

def test_lesson3_checks():
    t=MOD.read_text(encoding="utf-8")
    for m in ("def check_register","def check_edge","def check_nonblocking"):
        assert m in t

def test_lesson3_route():
    route="/academy/unit-12/sequential-hdl-registers-clocks"
    assert f'route="{route}"' in APP.read_text(encoding="utf-8")
    assert route in CAT.read_text(encoding="utf-8")
    assert CAT.read_text(encoding="utf-8").count("/academy/unit-12/")>=3

def test_lesson4_link():
    t=MOD.read_text(encoding="utf-8")
    assert "Next · Finite-State Machines & Control Logic" in t
    assert "/academy/unit-12/finite-state-machines-control-logic" in t

def test_simulator_fix_preserved():
    assert "State.handle_gate_click(cell_key)" in APP.read_text(encoding="utf-8")
