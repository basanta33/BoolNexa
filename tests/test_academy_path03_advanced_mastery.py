from pathlib import Path
ROOT = Path(__file__).parents[1]
APP = (ROOT / "digital_logic_lab" / "digital_logic_lab.py").read_text(encoding="utf-8")
LESSONS = (ROOT / "digital_logic_lab" / "academy_kmap_advanced_mastery.py").read_text(encoding="utf-8")
PREVIOUS = (ROOT / "digital_logic_lab" / "academy_kmap_five_six.py").read_text(encoding="utf-8")

def test_lessons_nine_and_ten_are_registered():
    assert 'route="/academy/unit-3/advanced-strategy"' in APP
    assert 'route="/academy/unit-3/mastery-challenge"' in APP

def test_advanced_strategy_is_educationally_complete():
    assert "Select essential prime implicants first" in LESSONS
    assert "static-1 hazard" in LESSONS
    assert "Consensus term BC" in LESSONS
    assert "algorithmic minimisation" in LESSONS
    assert "check_strategy" in LESSONS
    assert "check_hazard" in LESSONS

def test_mastery_challenge_checks_and_applies_learning():
    assert "Karnaugh Map Mastery Challenge" in LESSONS
    assert "grade_mastery" in LESSONS
    assert "F(A,B,C,D)=Σm(0,2,5,7,8,10,13,15)" in LESSONS
    assert "minimal SOP expression" in LESSONS
    assert "Explain, don't just calculate" in LESSONS
    assert "Path 03 completion" in LESSONS

def test_navigation_and_real_tool_integration():
    assert 'href="/academy/unit-3/advanced-strategy"' in PREVIOUS
    assert 'href="/academy/unit-3/mastery-challenge"' in LESSONS
    assert LESSONS.count('href="/tools/boolean"') >= 2
    assert LESSONS.count('href="/tools/circuit"') >= 2
    assert "Path 03 · Lesson 9" in LESSONS
    assert "Path 03 · Lesson 10" in LESSONS
