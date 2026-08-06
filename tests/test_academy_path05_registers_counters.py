from pathlib import Path
ROOT=Path(__file__).parents[1]
APP=(ROOT/"digital_logic_lab"/"digital_logic_lab.py").read_text(encoding="utf-8")
LESSONS=(ROOT/"digital_logic_lab"/"academy_registers_counters.py").read_text(encoding="utf-8")
PREVIOUS=(ROOT/"digital_logic_lab"/"academy_flipflops_clocking.py").read_text(encoding="utf-8")

def test_routes():
    assert 'route="/academy/unit-5/registers"' in APP
    assert 'route="/academy/unit-5/counters"' in APP

def test_registers():
    for x in ["Parallel registers","SISO","SIPO","PISO","PIPO","Right shifting","Universal shift register","next Q2 ← Q3","check_shift"]: assert x in LESSONS

def test_counters():
    for x in ["3-bit up-counter","Modulo-N counters","Asynchronous (ripple) counters","Synchronous counters","Q0 = fCLK / 2","programmable counting","check_counter_mod","check_divide"]: assert x in LESSONS

def test_navigation():
    assert 'href="/academy/unit-5/registers"' in PREVIOUS
    assert 'href="/academy/unit-5/counters"' in LESSONS
    assert "Path 05 · Lesson 5" in LESSONS and "Path 05 · Lesson 6" in LESSONS
