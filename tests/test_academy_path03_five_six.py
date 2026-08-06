from pathlib import Path

ROOT = Path(__file__).parents[1]
APP = (ROOT / "digital_logic_lab" / "digital_logic_lab.py").read_text(encoding="utf-8")
LESSONS = (ROOT / "digital_logic_lab" / "academy_kmap_five_six.py").read_text(encoding="utf-8")
PREVIOUS = (ROOT / "digital_logic_lab" / "academy_kmap_groups_pos.py").read_text(encoding="utf-8")


def test_lessons_seven_and_eight_are_registered():
    assert 'route="/academy/unit-3/five-variable-kmaps"' in APP
    assert 'route="/academy/unit-3/six-variable-kmaps"' in APP


def test_five_variable_lesson_matches_boolnexa_layout():
    assert "2⁵ = 32 cells" in LESSONS
    assert "single 4×8 Gray-code map" in LESSONS
    assert '"000", "001", "011", "010", "110", "111", "101", "100"' in LESSONS
    assert "reflection boundary" in LESSONS
    assert "100 ↔ 000" in LESSONS
    assert "check_five_cells" in LESSONS
    assert "check_five_columns" in LESSONS


def test_six_variable_lesson_matches_boolnexa_layout():
    assert "2⁶ = 64 cells" in LESSONS
    assert "one 8×8 Gray-code map" in LESSONS
    assert "Rows ABC:" in LESSONS
    assert "Columns DEF:" in LESSONS
    assert "vertical and horizontal fold boundaries" in LESSONS
    assert "check_six_cells" in LESSONS
    assert "check_six_shape" in LESSONS


def test_navigation_and_real_tool_integration():
    assert 'href="/academy/unit-3/five-variable-kmaps"' in PREVIOUS
    assert 'href="/academy/unit-3/six-variable-kmaps"' in LESSONS
    assert LESSONS.count('href="/tools/boolean"') >= 2
    assert 'href="/tools/circuit"' in LESSONS
    assert "Path 03 · Lesson 7" in LESSONS
    assert "Path 03 · Lesson 8" in LESSONS
