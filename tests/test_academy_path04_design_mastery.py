from pathlib import Path
ROOT = Path(__file__).parents[1]
APP = (ROOT / "digital_logic_lab" / "digital_logic_lab.py").read_text(encoding="utf-8")
LESSONS = (ROOT / "digital_logic_lab" / "academy_combinational_design_mastery.py").read_text(encoding="utf-8")
PREVIOUS = (ROOT / "digital_logic_lab" / "academy_decoders_encoders.py").read_text(encoding="utf-8")

def test_lessons_nine_and_ten_are_registered():
    assert 'route="/academy/unit-4/integrated-design"' in APP
    assert 'route="/academy/unit-4/mastery-challenge"' in APP

def test_integrated_design_teaches_engineering_workflow():
    assert "Begin with the specification" in LESSONS
    assert "Choose the right abstraction" in LESSONS
    assert "tiny arithmetic selector" in LESSONS
    assert "Optimise after correctness" in LESSONS
    assert "Propagation delay" in LESSONS
    assert "check_workflow" in LESSONS
    assert "check_block" in LESSONS

def test_mastery_has_real_capstone():
    assert "Combinational Logic Mastery Challenge" in LESSONS
    assert "grade_mastery" in LESSONS
    assert "two-input decision unit" in LESSONS
    assert "Y1 = M'A1 + MB1" in LESSONS
    assert "EQ = (A1 XNOR B1)(A0 XNOR B0)" in LESSONS
    assert "Verification checklist" in LESSONS
    assert "Path 04 complete" in LESSONS

def test_navigation_and_real_tools():
    assert 'href="/academy/unit-4/integrated-design"' in PREVIOUS
    assert 'href="/academy/unit-4/mastery-challenge"' in LESSONS
    assert LESSONS.count('href="/tools/boolean"') >= 2
    assert LESSONS.count('href="/tools/circuit"') >= 2
    assert 'href="/"' in LESSONS
    assert "Path 04 · Lesson 9" in LESSONS
    assert "Path 04 · Lesson 10" in LESSONS
