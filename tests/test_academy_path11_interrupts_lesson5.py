from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/"digital_logic_lab"/"academy_embedded_path11.py"
APP=ROOT/"digital_logic_lab"/"digital_logic_lab.py"
CAT=ROOT/"digital_logic_lab"/"academy_route_catalog.py"

def test_lesson5_present():
    text=MOD.read_text(encoding="utf-8")
    assert "def interrupts_priorities_isr_design_lesson" in text
    assert "PATH 11 · LESSON 05" in text

def test_lesson5_topics():
    text=MOD.read_text(encoding="utf-8")
    for term in ("An interrupt redirects execution to an event handler","Interrupt sources can be internal or external","The interrupt controller manages pending work","Priority decides precedence","Interrupt latency is a real-time quantity","ISR execution time also affects responsiveness","Keep interrupt handlers bounded and non-blocking","Shared data creates concurrency hazards","Interrupt flags must be handled correctly","Critical sections trade protection for latency","Trace a UART receive interrupt"):
        assert term in text

def test_lesson5_checks():
    text=MOD.read_text(encoding="utf-8")
    for method in ("def check_isr","def check_latency","def check_priority"):
        assert method in text

def test_lesson5_route():
    route="/academy/unit-11/interrupts-priorities-isr-design"
    assert f'route="{route}"' in APP.read_text(encoding="utf-8")
    assert route in CAT.read_text(encoding="utf-8")
    assert CAT.read_text(encoding="utf-8").count("/academy/unit-11/")>=5

def test_lesson6_link():
    text=MOD.read_text(encoding="utf-8")
    assert "Next · Real-Time Scheduling, Tasks & Determinism" in text
    assert "/academy/unit-11/real-time-scheduling-tasks-determinism" in text

def test_simulator_fix_preserved():
    assert "State.handle_gate_click(cell_key)" in APP.read_text(encoding="utf-8")
