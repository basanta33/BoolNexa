from pathlib import Path
ROOT = Path(__file__).parents[1]
APP = (ROOT / "digital_logic_lab" / "digital_logic_lab.py").read_text(encoding="utf-8")
LESSONS = (ROOT / "digital_logic_lab" / "academy_kmap_intro_two.py").read_text(encoding="utf-8")

def test_path03_lessons_one_and_two_are_registered():
    assert 'route="/academy/unit-3/kmap-introduction"' in APP
    assert 'route="/academy/unit-3/two-variable-kmaps"' in APP

def test_intro_teaches_kmap_foundations():
    assert "2 variables → 4 cells" in LESSONS
    assert "Gray-code order: 00 → 01 → 11 → 10" in LESSONS
    assert "Groups are rectangular" in LESSONS
    assert "Opposite edges are adjacent" in LESSONS
    assert "check_cells" in LESSONS
    assert "check_adjacency" in LESSONS

def test_two_variable_lesson_maps_and_simplifies():
    assert "Two-Variable Karnaugh Maps" in LESSONS
    assert "A'B' + A'B = A'" in LESSONS
    assert "3 cells ✗" in LESSONS
    assert "F = 1" in LESSONS
    assert "check_group" in LESSONS
    assert "check_simplify" in LESSONS

def test_real_tool_integration():
    assert LESSONS.count('href="/tools/boolean"') >= 2
    assert 'href="/tools/circuit"' in LESSONS
    assert "Path 03 · Lesson 1" in LESSONS
    assert "Path 03 · Lesson 2" in LESSONS
