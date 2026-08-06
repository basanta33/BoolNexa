from pathlib import Path

ROOT = Path(__file__).parents[1]
APP = (ROOT / "digital_logic_lab" / "digital_logic_lab.py").read_text(encoding="utf-8")
LESSONS = (ROOT / "digital_logic_lab" / "academy_binary_storage_mastery.py").read_text(encoding="utf-8")


def test_lessons_nine_and_ten_are_registered():
    assert 'route="/academy/unit-1/binary-storage"' in APP
    assert 'route="/academy/unit-1/mastery-challenge"' in APP


def test_storage_lesson_covers_bits_bytes_registers_and_width():
    assert "1 byte  = 8 bits" in LESSONS
    assert "Registers are small, fast storage" in LESSONS
    assert "2⁸  = 256 patterns" in LESSONS
    assert "check_byte" in LESSONS
    assert "check_storage" in LESSONS


def test_mastery_challenge_reviews_path01():
    assert "Convert 42₁₀ to binary" in LESSONS
    assert "Convert 111111₂ to hexadecimal" in LESSONS
    assert "Write −5 as 8-bit two's complement" in LESSONS
    assert "check_mastery" in LESSONS
    assert "Path 01 complete" in LESSONS


def test_final_lessons_connect_to_tools_and_path02():
    assert 'href="/tools/number-systems"' in LESSONS
    assert 'href="/tools/boolean"' in LESSONS
    assert 'href="/"' in LESSONS
    assert "Unit 1 · Lesson 9 of 10" in LESSONS
    assert "Unit 1 · Lesson 10 of 10" in LESSONS
    assert "Begin Path 02" in LESSONS
