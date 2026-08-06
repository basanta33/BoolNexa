from pathlib import Path

ROOT = Path(__file__).parents[1]
APP = (ROOT / "digital_logic_lab" / "digital_logic_lab.py").read_text(encoding="utf-8")
LESSONS = (ROOT / "digital_logic_lab" / "academy_binary_advanced.py").read_text(encoding="utf-8")


def test_lessons_five_and_six_are_registered():
    assert 'route="/academy/unit-1/octal-and-hexadecimal"' in APP
    assert 'route="/academy/unit-1/binary-arithmetic"' in APP
    assert "octal_hex_lesson" in APP
    assert "binary_arithmetic_lesson" in APP


def test_octal_hex_lesson_has_grouping_examples_and_practice():
    assert "101 110" in LESSONS
    assert "1110 1101" in LESSONS
    assert "check_hex" in LESSONS
    assert "check_octal" in LESSONS
    assert 'href="/tools/number-systems"' in LESSONS


def test_binary_arithmetic_has_addition_subtraction_and_tool_links():
    assert "1 + 1 = 10" in LESSONS
    assert "1011₂ + 0110₂" in LESSONS
    assert "11010₂ − 00111₂" in LESSONS
    assert "check_addition" in LESSONS
    assert "check_subtraction" in LESSONS
    assert 'href="/"' in LESSONS


def test_lesson_navigation_continues_path01():
    assert "Unit 1 · Lesson 5 of 10" in LESSONS
    assert "Unit 1 · Lesson 6 of 10" in LESSONS
    assert 'href="/academy/unit-1/signed-binary"' in LESSONS
