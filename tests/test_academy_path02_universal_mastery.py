from pathlib import Path

ROOT = Path(__file__).parents[1]
APP = (ROOT / "digital_logic_lab" / "digital_logic_lab.py").read_text(encoding="utf-8")
LESSONS = (ROOT / "digital_logic_lab" / "academy_boolean_universal_mastery.py").read_text(encoding="utf-8")


def test_lessons_nine_and_ten_are_registered():
    assert 'route="/academy/unit-2/universal-implementation"' in APP
    assert 'route="/academy/unit-2/mastery-challenge"' in APP


def test_universal_gate_lesson_has_nand_nor_and_demorgan():
    assert "NAND-only building blocks" in LESSONS
    assert "NOR-only building blocks" in LESSONS
    assert "(AB)' = A' + B'" in LESSONS
    assert "(A+B)' = A'B'" in LESSONS
    assert "check_nand_not" in LESSONS
    assert "check_nor_not" in LESSONS


def test_mastery_lesson_reviews_boolean_path_and_practical_design():
    assert "Boolean Algebra & Logic Gates Mastery" in LESSONS
    assert "Which gate outputs 1 when two inputs are different?" in LESSONS
    assert "Simplify A + AB" in LESSONS
    assert "four-variable truth table" in LESSONS
    assert "Design F = A'B + AC" in LESSONS
    assert "check_mastery" in LESSONS


def test_final_path02_lessons_integrate_real_tools_and_complete_path():
    assert LESSONS.count('href="/tools/boolean"') >= 2
    assert LESSONS.count('href="/tools/circuit"') >= 2
    assert LESSONS.count('href="/"') >= 2
    assert "Path 02 · Lesson 9 of 10" in LESSONS
    assert "Path 02 · Lesson 10 of 10" in LESSONS
    assert "Path 02 complete" in LESSONS
