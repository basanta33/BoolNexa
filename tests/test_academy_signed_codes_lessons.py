from pathlib import Path

ROOT = Path(__file__).parents[1]
APP = (ROOT / "digital_logic_lab" / "digital_logic_lab.py").read_text(encoding="utf-8")
LESSONS = (ROOT / "digital_logic_lab" / "academy_binary_signed_codes.py").read_text(encoding="utf-8")


def test_lessons_seven_and_eight_are_registered():
    assert 'route="/academy/unit-1/signed-binary"' in APP
    assert 'route="/academy/unit-1/digital-codes"' in APP


def test_signed_binary_covers_twos_complement_and_range():
    assert "Two's complement" in LESSONS
    assert "11110011" in LESSONS
    assert "−128 to +127" in LESSONS
    assert "check_twos" in LESSONS
    assert "check_range" in LESSONS


def test_digital_codes_covers_bcd_gray_and_characters():
    assert "Binary-Coded Decimal (BCD)" in LESSONS
    assert "0101 1001" in LESSONS
    assert "Gray code" in LESSONS
    assert "ASCII decimal 65" in LESSONS
    assert "check_bcd" in LESSONS
    assert "check_gray" in LESSONS


def test_lessons_connect_to_real_boolnexa_tools():
    assert 'href="/tools/number-systems"' in LESSONS
    assert 'href="/"' in LESSONS
    assert "Unit 1 · Lesson 7 of 10" in LESSONS
    assert "Unit 1 · Lesson 8 of 10" in LESSONS
