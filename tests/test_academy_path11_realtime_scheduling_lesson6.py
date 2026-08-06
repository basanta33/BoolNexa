from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/"digital_logic_lab"/"academy_embedded_path11.py"
APP=ROOT/"digital_logic_lab"/"digital_logic_lab.py"
CAT=ROOT/"digital_logic_lab"/"academy_route_catalog.py"

def test_lesson6_present():
    t=MOD.read_text(encoding="utf-8")
    assert "def real_time_scheduling_tasks_determinism_lesson" in t
    assert "PATH 11 · LESSON 06" in t

def test_lesson6_topics():
    t=MOD.read_text(encoding="utf-8")
    for term in ("Real-time correctness includes timing","Hard and soft real-time requirements differ","An RTOS organizes concurrent embedded work","Tasks move between execution states","Pre-emptive scheduling improves urgent response","Periodic tasks have timing parameters","CPU utilization alone is not the whole proof","Blocking and priority inversion threaten timing","Queues separate producers and consumers","Determinism means bounded, explainable timing","Trace a periodic control task"):
        assert term in t

def test_lesson6_checks():
    t=MOD.read_text(encoding="utf-8")
    for m in ("def check_rtos","def check_deadline","def check_preemption"):
        assert m in t

def test_lesson6_route():
    route="/academy/unit-11/real-time-scheduling-tasks-determinism"
    assert f'route="{route}"' in APP.read_text(encoding="utf-8")
    assert route in CAT.read_text(encoding="utf-8")
    assert CAT.read_text(encoding="utf-8").count("/academy/unit-11/")>=6

def test_lesson7_link():
    t=MOD.read_text(encoding="utf-8")
    assert "Next · UART, SPI, I²C & Peripheral Communication" in t
    assert "/academy/unit-11/uart-spi-i2c-peripheral-communication" in t

def test_simulator_fix_preserved():
    assert "State.handle_gate_click(cell_key)" in APP.read_text(encoding="utf-8")
