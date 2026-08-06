from pathlib import Path
ROOT=Path(__file__).parents[1]
APP=(ROOT/"digital_logic_lab"/"digital_logic_lab.py").read_text(encoding="utf-8")
LESSONS=(ROOT/"digital_logic_lab"/"academy_flipflops_clocking.py").read_text(encoding="utf-8")
PREVIOUS=(ROOT/"digital_logic_lab"/"academy_sequential_foundations_latches.py").read_text(encoding="utf-8")

def test_routes():
    assert 'route="/academy/unit-5/flip-flops"' in APP
    assert 'route="/academy/unit-5/clock-timing"' in APP

def test_flipflops():
    for x in ["Edge-triggered D flip-flop","JK flip-flop","T flip-flop","Q(next) = JQ' + K'Q","Q(next) = T ⊕ Q","Characteristic versus excitation thinking","Asynchronous preset and clear"]: assert x in LESSONS

def test_timing():
    for x in ["Setup time","Hold time","Clock-to-Q","Tclock ≥ tCQ(max) + tlogic(max) + tsetup","Metastability","two-flip-flop synchronizer","multi-bit buses"]: assert x in LESSONS

def test_navigation():
    assert 'href="/academy/unit-5/flip-flops"' in PREVIOUS
    assert 'href="/academy/unit-5/clock-timing"' in LESSONS
    assert "Path 05 · Lesson 3" in LESSONS and "Path 05 · Lesson 4" in LESSONS
