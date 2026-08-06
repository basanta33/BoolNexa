from pathlib import Path
ROOT=Path(__file__).parents[1]
APP=(ROOT/"digital_logic_lab"/"digital_logic_lab.py").read_text(encoding="utf-8")
LESSONS=(ROOT/"digital_logic_lab"/"academy_sequential_integration_mastery.py").read_text(encoding="utf-8")
PREVIOUS=(ROOT/"digital_logic_lab"/"academy_fsm_design.py").read_text(encoding="utf-8")

def test_routes():
    assert 'route="/academy/unit-5/integrated-design"' in APP
    assert 'route="/academy/unit-5/mastery-challenge"' in APP

def test_integrated_design():
    for x in ["Think in datapath + control","timed process controller","State register","Cycle-by-cycle reasoning","Timing still matters","Verification plan","check_block","check_timing"]: assert x in LESSONS

def test_mastery():
    for x in ["Sequential Logic Mastery Challenge","grade_mastery","pedestrian crossing controller","Safety rule","vehicle_green and pedestrian_green must NEVER","Implementation architecture","Path 05 complete"]: assert x in LESSONS

def test_engineering_safety():
    assert "Real traffic-control systems require additional safety states" in LESSONS
    assert "Asynchronous external requests are synchronized" in LESSONS
    assert "Unused state encodings recover safely" in LESSONS

def test_navigation():
    assert 'href="/academy/unit-5/integrated-design"' in PREVIOUS
    assert 'href="/academy/unit-5/mastery-challenge"' in LESSONS
    assert "Path 05 · Lesson 9" in LESSONS and "Path 05 · Lesson 10" in LESSONS
