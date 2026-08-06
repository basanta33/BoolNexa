from pathlib import Path
ROOT = Path(__file__).parents[1]
APP = (ROOT / "digital_logic_lab" / "digital_logic_lab.py").read_text(encoding="utf-8")
LESSONS = (ROOT / "digital_logic_lab" / "academy_kmap_three_four.py").read_text(encoding="utf-8")
PREVIOUS = (ROOT / "digital_logic_lab" / "academy_kmap_intro_two.py").read_text(encoding="utf-8")

def test_lessons_three_and_four_are_registered():
    assert 'route="/academy/unit-3/three-variable-kmaps"' in APP
    assert 'route="/academy/unit-3/four-variable-kmaps"' in APP

def test_three_variable_kmap_content():
    assert "2³ = 8" in LESSONS
    assert '"00", "01", "11", "10"' in LESSONS
    assert "One group of 4 → A'" in LESSONS
    assert "A'B'C' + A'B'C = A'B'" in LESSONS
    assert "00 ↔ 10" in LESSONS
    assert "check_three_cells" in LESSONS
    assert "check_pair" in LESSONS

def test_four_variable_kmap_content():
    assert "2⁴ = 16" in LESSONS
    assert "The four corners form a group" in LESSONS
    assert "Possible group sizes are 1, 2, 4, 8 or 16" in LESSONS
    assert "Overlap when it helps" in LESSONS
    assert "check_four_cells" in LESSONS
    assert "check_corner" in LESSONS

def test_navigation_and_real_tools():
    assert 'href="/academy/unit-3/three-variable-kmaps"' in PREVIOUS
    assert 'href="/academy/unit-3/four-variable-kmaps"' in LESSONS
    assert LESSONS.count('href="/tools/boolean"') >= 2
    assert 'href="/tools/circuit"' in LESSONS
    assert "Path 03 · Lesson 3" in LESSONS
    assert "Path 03 · Lesson 4" in LESSONS
