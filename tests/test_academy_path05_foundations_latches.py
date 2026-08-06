from pathlib import Path
ROOT=Path(__file__).parents[1]
APP=(ROOT/"digital_logic_lab"/"digital_logic_lab.py").read_text(encoding="utf-8")
LESSONS=(ROOT/"digital_logic_lab"/"academy_sequential_foundations_latches.py").read_text(encoding="utf-8")

def test_routes():
    assert 'route="/academy/unit-5/sequential-foundations"' in APP
    assert 'route="/academy/unit-5/latches"' in APP

def test_foundations():
    for x in ["Present state and next state","Feedback creates storage","level-sensitive versus edge-triggered","Why clocks matter","check_state"]: assert x in LESSONS

def test_latches():
    for x in ["Active-high NOR SR latch","active-low inputs","forbidden SR condition","transparent while its enable is active","check_sr","check_d"]: assert x in LESSONS

def test_navigation():
    assert 'href="/academy/unit-5/latches"' in LESSONS
    assert 'href="/academy/unit-5/sequential-foundations"' in LESSONS
    assert "Path 05 · Lesson 1" in LESSONS and "Path 05 · Lesson 2" in LESSONS
