from pathlib import Path

ROOT = Path(__file__).parents[1]
APP = (ROOT / "digital_logic_lab" / "digital_logic_lab.py").read_text(encoding="utf-8")
LESSONS = (ROOT / "digital_logic_lab" / "academy_binary_conversions.py").read_text(encoding="utf-8")
PLACE = (ROOT / "digital_logic_lab" / "academy_binary_place_value.py").read_text(encoding="utf-8")


def test_lessons_three_and_four_are_registered():
    assert 'route="/academy/unit-1/decimal-to-binary"' in APP
    assert 'route="/academy/unit-1/binary-to-decimal"' in APP
    assert "decimal_to_binary_lesson" in APP
    assert "binary_to_decimal_lesson" in APP


def test_conversion_lessons_have_worked_examples_and_interaction():
    assert "45 ÷ 2 = 22 remainder 1" in LESSONS
    assert "101101₂" in LESSONS
    assert "check_decimal_to_binary" in LESSONS
    assert "check_binary_to_decimal" in LESSONS
    assert "Quick check" in LESSONS


def test_conversion_lessons_use_real_number_system_lab():
    assert LESSONS.count('href="/tools/number-systems"') >= 2
    assert "Open Number System Laboratory" in LESSONS


def test_path01_lesson_count_is_consistent():
    assert "Unit 1 · Lesson 2 of 10" in PLACE
    assert "Unit 1 · Lesson 3 of 10" in LESSONS
    assert "Unit 1 · Lesson 4 of 10" in LESSONS
